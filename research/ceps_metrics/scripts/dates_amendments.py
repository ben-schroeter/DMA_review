"""Adoption/publication/entry-into-force dates and amending acts (corrigenda separate), from Cellar."""
import csv, json, sys
sys.path.insert(0, ".")
from common import sparql
P = "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
rows = list(csv.DictReader(open("../data/instrument_map.csv")))
cels = sorted({c for r in rows for c in r["celex_measured"].split(";") if c[:1] == "3"})
vals = " ".join(f'"{c}"^^xsd:string' for c in cels)
dates = {}
for b in sparql(P + f"""SELECT ?c (MIN(?sig) AS ?s) (MIN(?doc) AS ?d) (MIN(?pub) AS ?p) (GROUP_CONCAT(DISTINCT STR(?eif); separator="|") AS ?e) WHERE {{
  VALUES ?c {{ {vals} }} ?w cdm:resource_legal_id_celex ?c .
  OPTIONAL {{ ?w cdm:resource_legal_date_signature ?sig }} OPTIONAL {{ ?w cdm:work_date_document ?doc }}
  OPTIONAL {{ ?w cdm:work_date_creation_legacy ?pub }} OPTIONAL {{ ?w cdm:resource_legal_date_entry-into-force ?eif }}
}} GROUP BY ?c"""):
    g = lambda k: b.get(k, {}).get("value", "")
    adopt = g("s") or g("d")
    eifs = sorted(x for x in g("e").split("|") if x and x >= adopt)
    dates[b["c"]["value"]] = {"adoption_date": adopt, "oj_publication_date": g("p"), "entry_into_force": eifs[0] if eifs else ""}
amend = []
for i in range(0, len(cels), 20):
    v = " ".join(f'"{c}"^^xsd:string' for c in cels[i:i + 20])
    for rel, kind in (("resource_legal_amends_resource_legal", "amendment"), ("resource_legal_corrects_resource_legal", "corrigendum")):
        for b in sparql(P + f"""SELECT ?c ?sc (SAMPLE(?d) AS ?date) (SAMPLE(?t) AS ?title) WHERE {{
          VALUES ?c {{ {v} }} ?w cdm:resource_legal_id_celex ?c . ?s cdm:{rel} ?w ; cdm:resource_legal_id_celex ?sc .
          OPTIONAL {{ ?s cdm:work_date_document ?d }}
          OPTIONAL {{ ?e cdm:expression_belongs_to_work ?s ; cdm:expression_title ?t ;
                      cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> }}
        }} GROUP BY ?c ?sc"""):
            sc = b["sc"]["value"]
            k = "corrigendum" if (kind == "corrigendum" or "R(" in sc) else kind
            if k == "amendment" and sc[:1] != "3":
                continue                        # only adopted acts (sector 3), not proposals
            amend.append({"parent": b["c"]["value"], "celex": sc, "kind": k,
                          "date": b.get("date", {}).get("value", ""), "title": b.get("title", {}).get("value", "")})
json.dump({"dates": dates, "amendments": amend}, open("../data/dates_amendments.json", "w"), indent=1)
import collections
c = collections.Counter((a["parent"], a["kind"]) for a in amend)
print(len(dates), "dated;", len(amend), "links;", collections.Counter(a["kind"] for a in amend))
for x in ["32016R0679", "32022R1925", "32014R0910", "32006L0112", "32018L1972", "32015L2366"]:
    print(x, dates.get(x), "amendments:", c[(x, "amendment")], "corrigenda:", c[(x, "corrigendum")])
