"""Latest consolidated version (CELEX 0...) for each measured act."""
import csv, json, sys
sys.path.insert(0, ".")
from common import sparql

rows = list(csv.DictReader(open("../data/instrument_map.csv")))
cels = sorted({c for r in rows for c in r["celex_measured"].split(";") if c[:1] == "3"})
out = {}
for i in range(0, len(cels), 25):
    chunk = cels[i:i + 25]
    vals = " ".join(f'("{c[1:5]}" "{c[5]}" "{int(c[6:])}" "{c}")' for c in chunk)
    q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?src (MAX(?cc) AS ?latest) (COUNT(DISTINCT ?cc) AS ?n) WHERE {{
 VALUES (?y ?t ?num ?src) {{ {vals} }}
 ?c cdm:resource_legal_number_natural_celex ?num2 . FILTER(STR(?num2) = ?num)
 ?c cdm:resource_legal_id_sector ?sec . FILTER(STR(?sec) = "0")
 ?c cdm:resource_legal_type ?t2 . FILTER(STR(?t2) = ?t)
 ?c cdm:resource_legal_year ?yy . FILTER(STR(?yy) = ?y)
 ?c cdm:resource_legal_id_celex ?cc .
}} GROUP BY ?src"""
    for b in sparql(q):
        out[b["src"]["value"]] = {"latest": b["latest"]["value"], "n_versions": int(b["n"]["value"])}
json.dump(out, open("../data/consolidated.json", "w"), indent=1)
print(len(cels), "acts;", len(out), "with consolidated versions")
for c in cels[:8] + ["32016R0679", "32022R1925", "32014R0910"]:
    print(c, out.get(c))
