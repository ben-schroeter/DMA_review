"""Add (or refresh) instruments incrementally, without re-running the whole Stage-0 pipeline.

For the CELEX numbers given (main acts), this runs the same Cellar queries as secondary.py / filter_secondary.py,
consolidated.py, dates_amendments.py and proposals.py, restricted to those acts, merges the results into the existing data
files, pre-fills the text cache from Cellar (cellar_fetch.py, because EUR-Lex refuses automated requests) and measures the
new documents with measure.py, merging into data/measurements.json and data/proposals.json.

Rows themselves are added to data/instrument_map.csv and data/initial_inventory.csv beforehand (see notes/scope_2026-11.md).
Usage (from scripts/): python3 add_rows.py 32012D0243 32017D0899 ...      (or --all-new: every celex in instrument_map.csv
that has no main measurement yet)"""
import csv, json, re, sys
sys.path.insert(0, ".")
from common import sparql
from cellar_fetch import prefill

D = "../data/"
P = "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
ENG = "<http://publications.europa.eu/resource/authority/language/ENG>"


def vals(cs):
    return " ".join(f'"{c}"^^xsd:string' for c in cs)


def based_on(cels):
    out = []
    for i in range(0, len(cels), 20):
        q = P + f"""SELECT ?parent ?sc (SAMPLE(?type) AS ?t) (SAMPLE(?date) AS ?d) (SAMPLE(?title) AS ?ti) WHERE {{
 VALUES ?parent {{ {vals(cels[i:i + 20])} }}
 ?p cdm:resource_legal_id_celex ?parent .
 ?s cdm:resource_legal_based_on_resource_legal ?p ; cdm:resource_legal_id_celex ?sc .
 OPTIONAL {{ ?s cdm:work_has_resource-type ?type }} OPTIONAL {{ ?s cdm:work_date_document ?date }}
 OPTIONAL {{ ?e cdm:expression_belongs_to_work ?s ; cdm:expression_title ?title ; cdm:expression_uses_language {ENG} }}
}} GROUP BY ?parent ?sc"""
        for b in sparql(q):
            out.append({"parent": b["parent"]["value"], "celex": b["sc"]["value"],
                        "type": b.get("t", {}).get("value", "").rsplit("/", 1)[-1],
                        "date": b.get("d", {}).get("value", ""), "title": b.get("ti", {}).get("value", "")})
    return out


def filter_secondary(raw):
    """Same rules as filter_secondary.py (kept in step with it)."""
    src = open("filter_secondary.py").read()
    ns = {}
    exec(src.split("out, seen = [], set()")[0].replace('raw = json.load(open("../data/based_on_raw.json"))', "raw = []"), ns)
    body = "out, seen = [], set()" + src.split("out, seen = [], set()")[1].split("json.dump(out")[0]
    ns["raw"] = raw
    exec(body, ns)
    return ns["out"]


def consolidated(cels):
    out = {}
    for i in range(0, len(cels), 25):
        chunk = cels[i:i + 25]
        v = " ".join(f'("{c[1:5]}" "{c[5]}" "{int(c[6:])}" "{c}")' for c in chunk)
        q = P + f"""SELECT ?src (MAX(?cc) AS ?latest) (COUNT(DISTINCT ?cc) AS ?n) WHERE {{
 VALUES (?y ?t ?num ?src) {{ {v} }}
 ?c cdm:resource_legal_number_natural_celex ?num2 . FILTER(STR(?num2) = ?num)
 ?c cdm:resource_legal_id_sector ?sec . FILTER(STR(?sec) = "0")
 ?c cdm:resource_legal_type ?t2 . FILTER(STR(?t2) = ?t)
 ?c cdm:resource_legal_year ?yy . FILTER(STR(?yy) = ?y)
 ?c cdm:resource_legal_id_celex ?cc .
}} GROUP BY ?src"""
        for b in sparql(q):
            out[b["src"]["value"]] = {"latest": b["latest"]["value"], "n_versions": int(b["n"]["value"])}
    return out


def dates_amend(cels):
    dates, amend = {}, []
    for b in sparql(P + f"""SELECT ?c (MIN(?sig) AS ?s) (MIN(?doc) AS ?d) (MIN(?pub) AS ?p) (GROUP_CONCAT(DISTINCT STR(?eif); separator="|") AS ?e) WHERE {{
  VALUES ?c {{ {vals(cels)} }} ?w cdm:resource_legal_id_celex ?c .
  OPTIONAL {{ ?w cdm:resource_legal_date_signature ?sig }} OPTIONAL {{ ?w cdm:work_date_document ?doc }}
  OPTIONAL {{ ?w cdm:work_date_creation_legacy ?pub }} OPTIONAL {{ ?w cdm:resource_legal_date_entry-into-force ?eif }}
}} GROUP BY ?c"""):
        g = lambda k: b.get(k, {}).get("value", "")
        adopt = g("s") or g("d")
        eifs = sorted(x for x in g("e").split("|") if x and x >= adopt)
        dates[b["c"]["value"]] = {"adoption_date": adopt, "oj_publication_date": g("p"), "entry_into_force": eifs[0] if eifs else ""}
    for i in range(0, len(cels), 20):
        for rel, kind in (("resource_legal_amends_resource_legal", "amendment"), ("resource_legal_corrects_resource_legal", "corrigendum")):
            for b in sparql(P + f"""SELECT ?c ?sc (SAMPLE(?d) AS ?date) (SAMPLE(?t) AS ?title) WHERE {{
          VALUES ?c {{ {vals(cels[i:i + 20])} }} ?w cdm:resource_legal_id_celex ?c . ?s cdm:{rel} ?w ; cdm:resource_legal_id_celex ?sc .
          OPTIONAL {{ ?s cdm:work_date_document ?d }}
          OPTIONAL {{ ?e cdm:expression_belongs_to_work ?s ; cdm:expression_title ?t ; cdm:expression_uses_language {ENG} }}
        }} GROUP BY ?c ?sc"""):
                sc = b["sc"]["value"]
                k = "corrigendum" if (kind == "corrigendum" or "R(" in sc) else kind
                if k == "amendment" and sc[:1] != "3":
                    continue
                amend.append({"parent": b["c"]["value"], "celex": sc, "kind": k,
                              "date": b.get("date", {}).get("value", ""), "title": b.get("title", {}).get("value", "")})
    return dates, amend


def proposals(cels):
    links = {}
    for b in sparql(P + f"""SELECT ?c ?pc (SAMPLE(?d) AS ?date) WHERE {{ VALUES ?c {{ {vals(cels)} }}
          ?w cdm:resource_legal_id_celex ?c ; cdm:resource_legal_adopts_resource_legal ?p . ?p cdm:resource_legal_id_celex ?pc .
          OPTIONAL {{ ?p cdm:work_date_document ?d }} FILTER(CONTAINS(STR(?pc), "PC")) }} GROUP BY ?c ?pc"""):
        links.setdefault(b["c"]["value"], []).append((b.get("date", {}).get("value", "9999"), b["pc"]["value"]))
    out = {}
    for c in cels:
        cand = sorted(links.get(c, []))
        out[c] = {"proposal_celex": cand[0][1] if cand else None, "proposal_date": cand[0][0] if cand else None,
                  "all_linked_proposals": [x[1] for x in cand]}
    return out


def measure_docs(jobs):
    """jobs: list of (celex, kind). Returns list of measurement dicts (kind added)."""
    from measure import measure
    out = []
    for c, kind in jobs:
        st = prefill(c)
        try:
            r = measure(c, want_pages=(kind != "consolidated"))
            r["kind"] = kind
            if st not in ("ok", "cached"):
                r["fetch_note"] = st
        except Exception as e:
            r = {"celex": c, "kind": kind, "error": f"{type(e).__name__}: {str(e)[:150]}; fetch: {st}"}
        out.append(r)
        print(" measured", c, kind, r.get("restrictions_total"), r.get("error", ""), flush=True)
    return out


def measure_proposal(pc):
    from measure import measure, measure_from_pdf
    from common import fetch
    prefill(pc)
    try:
        r = measure(pc, is_proposal=True, want_pages=False)
        html = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{pc}")
        if r["words_articles"] < 300 or "TABLE POSITION" in html or "Having regard" not in html:
            r = measure_from_pdf(pc)
        return r
    except Exception as e:
        return {"celex": pc, "error": f"{type(e).__name__}: {str(e)[:120]}"}


def main(cels):
    cels = sorted(set(cels))
    print("acts:", cels)
    # 1. secondary acts
    raw = based_on(cels)
    braw = json.load(open(D + "based_on_raw.json"))
    braw = [r for r in braw if r["parent"] not in cels] + raw
    json.dump(braw, open(D + "based_on_raw.json", "w"), indent=1)
    sec_new = filter_secondary(raw)
    sec = json.load(open(D + "secondary_acts.json"))
    sec = [s for s in sec if s["parent"] not in cels] + sec_new
    json.dump(sec, open(D + "secondary_acts.json", "w"), indent=1)
    print("secondary acts:", len(sec_new))
    # 2. consolidated versions
    cons = json.load(open(D + "consolidated.json"))
    cnew = consolidated(cels)
    cons.update(cnew)
    json.dump(cons, open(D + "consolidated.json", "w"), indent=1)
    # 3. dates and amendments
    da = json.load(open(D + "dates_amendments.json"))
    dnew, anew = dates_amend(cels)
    da["dates"].update(dnew)
    da["amendments"] = [a for a in da["amendments"] if a["parent"] not in cels] + anew
    json.dump(da, open(D + "dates_amendments.json", "w"), indent=1)
    print("dated:", len(dnew), "amendment links:", len(anew))
    # 4. measurements: main, consolidated, secondary
    meas = json.load(open(D + "measurements.json"))
    have = {(m["celex"], m["kind"]) for m in meas if "error" not in m}
    jobs = [(c, "main") for c in cels]
    jobs += [(cnew[c]["latest"], "consolidated") for c in cels if c in cnew]
    jobs += [(s["celex"], "secondary") for s in sec_new if (s["celex"], "main") not in have]
    jobs = [j for j in dict.fromkeys(jobs) if j not in have]
    res = measure_docs(jobs)
    keys = {(r["celex"], r["kind"]) for r in res}
    meas = [m for m in meas if (m["celex"], m["kind"]) not in keys] + res
    json.dump(meas, open(D + "measurements.json", "w"), indent=1)
    # 5. proposals
    pr = json.load(open(D + "proposals.json"))
    links = proposals(cels)
    pr["links"].update(links)
    for c, v in links.items():
        pc = v["proposal_celex"]
        if pc and pc not in pr["measurements"]:
            pr["measurements"][pc] = measure_proposal(pc)
            print(" proposal", c, pc, pr["measurements"][pc].get("restrictions_total"), pr["measurements"][pc].get("error", ""))
    json.dump(pr, open(D + "proposals.json", "w"), indent=1)
    errs = [r for r in res if "error" in r or r.get("parse_warning")]
    print("done;", len(res), "documents measured;", len(errs), "with errors or warnings:", [(r["celex"], r.get("error") or r.get("parse_warning")) for r in errs][:20])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all-new" in sys.argv:
        meas = {(m["celex"], m["kind"]) for m in json.load(open(D + "measurements.json")) if "error" not in m}
        args = [c for r in csv.DictReader(open(D + "instrument_map.csv")) for c in r["celex_measured"].split(";")
                if c[:1] == "3" and (c, "main") not in meas]
    main(args)
