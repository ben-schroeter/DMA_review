"""Step 1: map adopted rows to CELEX and verify title via Cellar."""
import csv, json, sys
sys.path.insert(0, ".")
from common import celex_from_identifier, sparql

rows = list(csv.DictReader(open("../data/ceps_instruments.csv")))
celexes = sorted({c for r in rows if r["status"] == "adopted" for c in celex_from_identifier(r["identifier"])})
vals = " ".join(f'"{c}"^^xsd:string' for c in celexes)
q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?celex ?w (SAMPLE(?t) AS ?title) (SAMPLE(?d) AS ?date) WHERE {{
  VALUES ?celex {{ {vals} }}
  ?w cdm:resource_legal_id_celex ?celex .
  OPTIONAL {{ ?w cdm:work_date_document ?d }}
  OPTIONAL {{ ?e cdm:expression_belongs_to_work ?w ; cdm:expression_title ?t ;
              cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> }}
}} GROUP BY ?celex ?w"""
res = {b["celex"]["value"]: {"work": b["w"]["value"], "title": b.get("title", {}).get("value", ""),
                             "date": b.get("date", {}).get("value", "")} for b in sparql(q)}
json.dump(res, open("../data/celex_works.json", "w"), indent=1)
for r in rows:
    if r["status"] != "adopted": continue
    for c in celex_from_identifier(r["identifier"]):
        t = res.get(c, {}).get("title", "MISSING")
        print(f"{c} | {r['name'][:45]:45} | {t[:110]}")
