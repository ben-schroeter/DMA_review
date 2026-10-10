"""Acts adopted on the legal basis of each measured act (Cellar 'based_on')."""
import csv, json, sys, collections
sys.path.insert(0, ".")
from common import sparql

rows = list(csv.DictReader(open("../data/instrument_map.csv")))
cels = sorted({c for r in rows for c in r["celex_measured"].split(";") if c[:1] == "3"})
res = []
for i in range(0, len(cels), 20):
    vals = " ".join(f'"{c}"^^xsd:string' for c in cels[i:i + 20])
    q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?parent ?sc (SAMPLE(?type) AS ?t) (SAMPLE(?date) AS ?d) (SAMPLE(?title) AS ?ti) WHERE {{
 VALUES ?parent {{ {vals} }}
 ?p cdm:resource_legal_id_celex ?parent .
 ?s cdm:resource_legal_based_on_resource_legal ?p ; cdm:resource_legal_id_celex ?sc .
 OPTIONAL {{ ?s cdm:work_has_resource-type ?type }}
 OPTIONAL {{ ?s cdm:work_date_document ?date }}
 OPTIONAL {{ ?e cdm:expression_belongs_to_work ?s ; cdm:expression_title ?title ;
             cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> }}
}} GROUP BY ?parent ?sc"""
    for b in sparql(q):
        res.append({"parent": b["parent"]["value"], "celex": b["sc"]["value"],
                    "type": b.get("t", {}).get("value", "").rsplit("/", 1)[-1],
                    "date": b.get("d", {}).get("value", ""), "title": b.get("ti", {}).get("value", "")})
json.dump(res, open("../data/based_on_raw.json", "w"), indent=1)
print(len(res))
print(collections.Counter((r["celex"][0], r["type"]) for r in res).most_common(60))
