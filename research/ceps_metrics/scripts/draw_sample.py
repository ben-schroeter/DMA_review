"""Draw a validation sample: counted instances (precision) and uncounted clauses with modal-like words (recall)."""
import csv, json, random, re, sys
sys.path.insert(0, ".")
from common import fetch
from textparse import html_to_lines, split_parts
from restrictions import strip_quoted, clauses, find_instances
from measure import count_restrictions

random.seed(20261010)
rows = list(csv.DictReader(open("../data/instrument_map.csv")))
docs = [c for r in rows for c in r["celex_measured"].split(";") if c[:1] in "35"]
sec = json.load(open("../data/secondary_acts.json"))
docs_sec = random.sample([s["celex"] for s in sec if s["kind"] in ("implementing", "delegated")], 12)
pick = random.sample(docs, 28) + docs_sec
pos, neg = [], []
MODALISH = re.compile(r"\b(shall|must|may|required?|requirements?|obligations?|prohibit\w*|mandatory|oblig\w+|ensure|need to|has to|have to|is to|are to)\b", re.I)
for c in pick:
    try:
        lines = html_to_lines(fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{c}"))
    except Exception:
        continue
    p = split_parts(lines, is_proposal=c.startswith("5"))
    body = p["articles"] + p["annexes"]
    sink = []
    count_restrictions(body, True, sink, c)
    pos += random.sample(sink, min(6, len(sink)))
    uncounted = [cl for cl in clauses(strip_quoted(body)) if not find_instances(cl)[0] and MODALISH.search(cl)]
    neg += [{"doc": c, "clause": u[:400]} for u in random.sample(uncounted, min(3, len(uncounted)))]
random.shuffle(pos); random.shuffle(neg)
json.dump({"positives": pos[:200], "negatives": neg[:100]}, open("../data/validation_sample.json", "w"), indent=1)
print(len(pos), len(neg))
