"""National implementing (transposition) measures per directive, from Cellar."""
import csv, json, re, sys
sys.path.insert(0, ".")
from common import sparql
rows = list(csv.DictReader(open("../data/instrument_map.csv")))
dirs = sorted({c for r in rows for c in r["celex_measured"].split(";") if re.match(r"3\d{4}L", c)})
out = {}
for d in dirs:
    q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT DISTINCT ?sc WHERE {{ ?p cdm:resource_legal_id_celex "{d}"^^xsd:string .
  ?s cdm:measure_national_implementing_implements_resource_legal ?p ; cdm:resource_legal_id_celex ?sc }}"""
    ids = [b["sc"]["value"] for b in sparql(q)]
    states = {m.group(1) for i in ids if (m := re.search(r"([A-Z]{3})_", i))}
    out[d] = {"n_measures": len(ids), "n_member_states": len(states)}
    print(d, out[d])
json.dump(out, open("../data/national_measures.json", "w"), indent=1)
