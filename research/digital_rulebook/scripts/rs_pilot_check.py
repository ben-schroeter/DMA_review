"""Rules vs standards pilot: compare the word-list first pass (scripts/rs_lexicon.py) with the hand codes. Run from research/digital_rulebook."""
import sys, json, collections
sys.path.insert(0, "scripts"); sys.path.insert(0, "data/rules_standards")
from rs_lexicon import code
from pilot_codes import CODES
S = [json.loads(l) for l in open("data/rules_standards/pilot_sample.jsonl")]
P = [code(x["clause"], x["chapeau"]) for x in S]
keep = [i for i in range(200) if CODES[i] != "N" and not S[i]["doc"].startswith("5")]   # drop non-obligations and Commission guidance
coll = lambda c: {"M": "S", "L": "S"}.get(c, c)
ex = sum(P[i] == CODES[i] for i in keep); bi = sum(coll(P[i]) == coll(CODES[i]) for i in keep)
print(len(keep), "exact", round(ex / len(keep), 2), "rule vs standard-like", round(bi / len(keep), 2))
print(sorted(collections.Counter((CODES[i], P[i]) for i in keep).items()))
for grp, f in (("main", lambda i: i < 130), ("secondary", lambda i: i >= 130), ("main, companies", lambda i: i < 130 and S[i]["addressee_v2"] == "private_parties")):
    ids = [i for i in keep if f(i)]
    print(grp, len(ids), dict(collections.Counter(CODES[i] for i in ids)))
json.dump([{"n": i, "hand": CODES[i], "lexicon": P[i]} for i in range(200)], open("data/rules_standards/pilot_result.json", "w"))
