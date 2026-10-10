"""Original Commission proposal for each adopted act (Cellar 'adopts' link), measured like the adopted text."""
import csv, json, sys, multiprocessing as mp
sys.path.insert(0, ".")
from common import sparql
P = "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"


def find():
    rows = list(csv.DictReader(open("../data/instrument_map.csv")))
    cels = sorted({c for r in rows for c in r["celex_measured"].split(";") if c[:1] == "3"})
    links = {}
    for i in range(0, len(cels), 25):
        v = " ".join(f'"{c}"^^xsd:string' for c in cels[i:i + 25])
        for b in sparql(P + f"""SELECT ?c ?pc (SAMPLE(?d) AS ?date) WHERE {{ VALUES ?c {{ {v} }}
          ?w cdm:resource_legal_id_celex ?c ; cdm:resource_legal_adopts_resource_legal ?p . ?p cdm:resource_legal_id_celex ?pc .
          OPTIONAL {{ ?p cdm:work_date_document ?d }} FILTER(CONTAINS(STR(?pc), "PC")) }} GROUP BY ?c ?pc"""):
            links.setdefault(b["c"]["value"], []).append((b.get("date", {}).get("value", "9999"), b["pc"]["value"]))
    out = {}
    for c in cels:
        cand = sorted(links.get(c, []))
        out[c] = {"proposal_celex": cand[0][1] if cand else None, "proposal_date": cand[0][0] if cand else None,
                  "all_linked_proposals": [x[1] for x in cand]}
    return out


def work(pc):
    from measure import measure, measure_from_pdf
    from common import fetch
    try:
        r = measure(pc, is_proposal=True, want_pages=False)
        html = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{pc}")
        if r["words_articles"] < 300 or "TABLE POSITION" in html or "Having regard" not in html:
            r = measure_from_pdf(pc)
        return r
    except Exception as e:
        return {"celex": pc, "error": f"{type(e).__name__}: {str(e)[:120]}"}


if __name__ == "__main__":
    links = find()
    print(sum(1 for v in links.values() if v["proposal_celex"]), "of", len(links), "acts have a linked proposal")
    print("no proposal:", [c for c, v in links.items() if not v["proposal_celex"]])
    pcs = sorted({v["proposal_celex"] for v in links.values() if v["proposal_celex"]})
    with mp.Pool(4) as pool:
        res = {r["celex"]: r for r in pool.map(work, pcs)}
    json.dump({"links": links, "measurements": res}, open("../data/proposals.json", "w"), indent=1)
    bad = {k: v.get("error") or v.get("parse_warning") for k, v in res.items() if v.get("error") or v.get("parse_warning") or not v.get("words_articles")}
    print("problems:", bad)
