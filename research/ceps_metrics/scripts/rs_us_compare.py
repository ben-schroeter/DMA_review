"""Rules vs standards: the 8 matched US counterparts against their EU acts (main acts, same codebook and readers).
Writes data/rules_standards/us_compare.json. Run from research/ceps_metrics."""
import json, collections, sys
sys.path.insert(0, "data/rules_standards")
C = {}
for f in ("us0", "us1"):
    for o in json.load(open(f"data/rules_standards/batches/{f}_coded.json")):
        C[o["k"]] = o["c"]
inst = [json.loads(l) for l in open("data/rules_standards/us_instances.jsonl")]
s = json.load(open("data/rules_standards/summary.json"))
EU = {o["row_id"]: o for o in s["instruments"]}
LAB = {"ftc5": "FTC Act §5", "cpsia": "CPSIA", "ccpa": "CCPA (California)", "dtsa": "Defend Trade Secrets Act", "cloud": "CLOUD Act",
       "cpsa": "Consumer Product Safety Act", "chips": "CHIPS Act", "colorado_ai": "Colorado AI Act"}
EUN = {13: "Unfair Commercial Practices", 17: "Toy Safety", 20: "GDPR", 26: "Trade Secrets", 42: "E-evidence", 67: "Product Safety", 74: "Chips Act", 64: "AI Act"}
by = collections.defaultdict(collections.Counter); tot = collections.Counter()
for x in inst:
    c = C[x["key"]]; by[x["law"]][c] += 1; tot[c] += 1
sh = lambda c: (lambda n: {"n": n, "R": round(c["R"] / n, 3), "standard_like": round((c["S"] + c["M"] + c["L"]) / n, 3)})(sum(c[k] for k in "RSMLD"))
rows = []
for law, cnt in by.items():
    row = next(x["row_id"] for x in inst if x["law"] == law); e = EU[row]["main"]
    rows.append({"pair": f"{EUN[row]} → {LAB[law]}", "row_id": row, "eu": {"n": e["n"], "R": e["R"], "standard_like": e["standard_like"]},
                 "us": sh(cnt), "us_not_obligation": cnt["N"]})
rows.sort(key=lambda r: r["eu"]["R"])
eu_tot = collections.Counter()
for r in rows:
    pass
out = {"us_total": {**sh(tot), "N": tot["N"], "codes": dict(tot)}, "pairs": rows}
# validation
from us_validation_codes import CODES
V = json.load(open("data/rules_standards/us_validation_sample.json"))
coll = lambda c: {"M": "S", "L": "S"}.get(c, c)
P = [(CODES[i], C[v["k"]]) for i, v in enumerate(V)]
keep = [(a, b) for a, b in P if a != "N" and b != "N"]
out["validation"] = {"n": len(P), "compared": len(keep), "exact_all": round(sum(a == b for a, b in P) / len(P), 3),
                     "rule_vs_standard_like": round(sum(coll(a) == coll(b) for a, b in keep) / len(keep), 3),
                     "confusion": dict(collections.Counter(f"{a}->{b}" for a, b in P))}
json.dump(out, open("data/rules_standards/us_compare.json", "w"), indent=1)
print(json.dumps(out["us_total"])); print(out["validation"])
for r in rows: print(f'{r["pair"]:52s} EU n={r["eu"]["n"]:4d} R={r["eu"]["R"]:.0%} std={r["eu"]["standard_like"]:.0%} | US n={r["us"]["n"]:3d} R={r["us"]["R"]:.0%} std={r["us"]["standard_like"]:.0%}')
w = lambda side, k: sum(r[side][k] * r[side]["n"] for r in rows) / sum(r[side]["n"] for r in rows)
print("pooled EU R", round(w("eu", "R"), 3), "std", round(w("eu", "standard_like"), 3), "| US R", round(w("us", "R"), 3), "std", round(w("us", "standard_like"), 3))
import statistics
print("median EU R", statistics.median(r["eu"]["R"] for r in rows), "US R", statistics.median(r["us"]["R"] for r in rows))
