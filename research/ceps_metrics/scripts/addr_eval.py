"""Score addressee classifiers on the development sets: the 300 coded diagnosis cases (all v1-unclear)
and the earlier hand-labelled validation sample (validation_sample.json + validation_labels.json)."""
import json, os, sys, collections
D = os.path.join(os.path.dirname(__file__), "..", "data")
A = os.path.join(D, "addressee")
key = lambda r: (r["doc"], r["clause"][:200], r.get("pos"))
rows = [json.loads(l) for l in open(os.path.join(A, "instances_main.jsonl"))]
v2 = [json.loads(l) for l in open(os.path.join(A, "v2_main.jsonl"))]
idx = {key(r): i for i, r in enumerate(rows)}
MAP = {"P": "private_parties", "MS": "member_states", "EU": "eu_institutions", "U": "unclear"}
def norm(x): return "none" if x in ("no_actor", "unclear") else x

# set 1: diagnosis
S = {r["sid"]: r for r in json.load(open(os.path.join(A, "diag_sample_300.json")))}
C = json.load(open(os.path.join(A, "diag_coded_300.json")))
ok1 = ok1s = n1 = 0; conf = collections.Counter(); miss = []
for c in C:
    if c["cause"] == "not_a_restriction":
        continue
    i = idx[key(S[c["sid"]])]; p = v2[i]["formal"]; n1 += 1
    ok1 += p == c["formal"]; ok1s += norm(p) == norm(c["formal"])
    conf[(c["formal"], p)] += 1
    if norm(p) != norm(c["formal"]): miss.append((c["sid"], c["formal"], p, v2[i]["how"]))
print(f"diagnosis set (v1 all unclear): v2 exact {ok1}/{n1} = {ok1/n1:.0%}; with no_actor~unclear {ok1s/n1:.0%}")
print("  how of misses:", collections.Counter(m[3] for m in miss))
print("  confusion (truth, v2):", sorted(conf.items(), key=lambda x: -x[1])[:14])
# set 2: earlier labels
vs = json.load(open(os.path.join(D, "validation_sample.json")))["positives"]; lab = json.load(open(os.path.join(D, "validation_labels.json")))["positives"]
n2 = o1 = o2 = um = 0
for k, (isr, a) in lab.items():
    if not isr: continue
    s = vs[int(k)]
    cand = [i for i, r in enumerate(rows) if r["doc"] == s["doc"] and r["clause"][:200] == s["clause"][:200] and r["marker"] == s["marker"]]
    if not cand: um += 1; continue
    i = cand[0]; t = norm(MAP[a]); n2 += 1
    o1 += norm(rows[i]["addressee"]) == t; o2 += norm(v2[i]["formal"]) == t
print(f"earlier labelled sample: matched {n2} (unmatched {um}); v1 {o1/n2:.0%}  v2 {o2/n2:.0%}")
if "-v" in sys.argv:
    for m in miss: print(m)
