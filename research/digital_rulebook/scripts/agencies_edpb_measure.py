"""Measure final EDPB guidelines/recommendations."""
import json, sys
sys.path.insert(0, ".")
from agencies_map import measure_doc
items = json.load(open("../data/agency_edpb.json"))
for it in items:
    if not it["final"] or not it["pdf"]:
        continue
    try:
        text, m = measure_doc(it["pdf"])
        it.update(m or {})
    except Exception as e:
        it["error"] = str(e)[:100]
json.dump(items, open("../data/agency_edpb.json", "w"), indent=1)
ok = [i for i in items if i.get("pages")]
print(len(items), "items;", len(ok), "measured;", sum(i.get("pages", 0) or 0 for i in ok), "pages;", [i["title"][:50] for i in items if i.get("error")])
