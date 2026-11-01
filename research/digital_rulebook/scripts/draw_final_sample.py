"""Fresh validation sample after the full run (final rules), across main and secondary acts."""
import json, random, sys
sys.path.insert(0, ".")
from common import fetch
from textparse import html_to_lines, split_parts
from measure import count_restrictions
random.seed(777)
m = [x for x in json.load(open("../data/measurements.json")) if x["kind"] in ("main", "secondary") and x.get("restrictions_total")]
w = [x["restrictions_total"] for x in m]
docs = []
while len(docs) < 50:                     # sample documents in proportion to their restriction counts
    d = random.choices(m, weights=w)[0]["celex"]
    if d not in docs:
        docs.append(d)
out = []
for c in docs:
    lines = html_to_lines(fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{c}"))
    p = split_parts(lines, is_proposal=c.startswith("5") and "PC" in c)
    sink = []
    count_restrictions(p["articles"] + p["annexes"], True, sink, c)
    out += random.sample(sink, min(2, len(sink)))
random.shuffle(out)
json.dump(out[:100], open("../data/validation_sample_final.json", "w"), indent=1)
for i, x in enumerate(out[:100]):
    cl = x["clause"]; k = cl.find(x["marker"]); a = max(0, k - 140)
    print(f"{i}|{x['category'][:6]}|{x['addressee'][:6]}|{cl[a:k + 100]}")
