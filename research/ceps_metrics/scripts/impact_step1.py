"""Step 1 for every instrument: proposal objectives/indicators (LFS 1.4.x), linked impact assessment and evaluation SWDs.
Writes data/impact_raw/<CELEX>.json (machine extraction, to be reviewed when writing data/impact/<CELEX>.json)."""
import csv, json, os, re, sys
sys.path.insert(0, ".")
from common import fetch, sparql
from textparse import html_to_lines, split_parts

P = "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
OUT = "../data/impact_raw/"; os.makedirs(OUT, exist_ok=True)
props = json.load(open("../data/proposals.json"))["links"]
rows = list(csv.DictReader(open("../data/instrument_map.csv")))


def section(lines, start_rx, stop_rx, maxlines=80):
    i = next((k for k, l in enumerate(lines) if re.match(start_rx, l)), None)
    if i is None:
        return ""
    # use the last match (the first occurrence is often the table of contents)
    starts = [k for k, l in enumerate(lines) if re.match(start_rx, l)]
    i = starts[-1]
    j = next((k for k in range(i + 1, min(len(lines), i + maxlines)) if re.match(stop_rx, lines[k])), min(len(lines), i + maxlines))
    return "\n".join(lines[i:j])


def linked_swds(celexes):
    vals = " ".join(f'"{c}"^^xsd:string' for c in celexes)
    q = P + f"""SELECT DISTINCT ?sc ?t ?d WHERE {{ VALUES ?c {{ {vals} }} ?w cdm:resource_legal_id_celex ?c .
      {{ ?s ?r ?w }} UNION {{ ?w ?r ?s }}
      ?s cdm:resource_legal_id_celex ?sc . FILTER(CONTAINS(STR(?sc), "SC") || CONTAINS(STR(?sc), "DC"))
      OPTIONAL {{ ?s cdm:work_date_document ?d }}
      ?e cdm:expression_belongs_to_work ?s ; cdm:expression_title ?t ;
         cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> }}"""
    out = []
    for b in sparql(q):
        t = b["t"]["value"]
        kind = ("impact assessment" if re.search(r"IMPACT ASSESSMENT", t, re.I) and "SUMMARY" not in t.upper() else
                "IA executive summary" if re.search(r"SUMMARY OF THE IMPACT ASSESSMENT|EXECUTIVE SUMMARY", t, re.I) else
                "evaluation" if re.search(r"\bEVALUATION\b|FITNESS CHECK|REVIEW OF|ON THE APPLICATION OF|IMPLEMENTATION OF", t, re.I) else None)
        if kind:
            out.append({"celex": b["sc"]["value"], "kind": kind, "date": b.get("d", {}).get("value", ""), "title": t[:400]})
    return out


for r in rows:
    cel = r["celex_measured"].split(";")
    if not cel[0][:1] in "35":
        continue
    key = cel[0]
    fn = OUT + key + ".json"
    if os.path.exists(fn):
        continue
    rec = {"celex": key, "name": r["name"], "status": r["status_oct2026"]}
    pc = cel[0] if cel[0].startswith("5") else props.get(cel[0], {}).get("proposal_celex")
    rec["proposal"] = pc
    if pc:
        try:
            lines = html_to_lines(fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{pc}"))
            p = split_parts(lines, is_proposal=True)
            fs = p["financial_statement"] or lines
            rec["lfs_specific_objectives"] = section(fs, r"^1\.4\.2\.?", r"^1\.4\.3")
            rec["lfs_expected_results"] = section(fs, r"^1\.4\.3\.?", r"^1\.4\.4")
            rec["lfs_indicators"] = section(fs, r"^1\.4\.4\.?", r"^1\.5", 60)
            rec["memo_monitoring"] = section(p["memorandum"], r".*(Implementation plans|monitoring, evaluation and reporting)", r"^(•|\d+\.\d+\.?)\s*(Detailed|Explanatory)", 25)
        except Exception as e:
            rec["error"] = str(e)[:120]
    try:
        rec["linked_documents"] = linked_swds([c for c in cel + ([pc] if pc else []) if c])
    except Exception as e:
        rec["linked_documents_error"] = str(e)[:120]
    json.dump(rec, open(fn, "w"), indent=1, ensure_ascii=False)
    print(key, r["name"][:40], "| ind:", len(rec.get("lfs_indicators", "")), "| docs:", len(rec.get("linked_documents", [])), flush=True)
