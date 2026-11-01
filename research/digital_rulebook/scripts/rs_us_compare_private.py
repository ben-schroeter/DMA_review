"""Rules vs standards, matched pairs, obligations on companies only. EU: formal addressee private parties (as elsewhere on the
site); US: classifier private parties plus the hand-read unclear items in scripts/us_private.py (PRIVATE_UNCLEAR).
Writes data/rules_standards/us_compare_private.json. Run from research/digital_rulebook."""
import json, collections, re, statistics
src = open("scripts/us_private.py").read()
PRIVATE_UNCLEAR = eval(re.search(r"PRIVATE_UNCLEAR = (\{.*?\}\})", src, re.S).group(1))
C = {}
for f in ("us0", "us1"):
    for o in json.load(open(f"data/rules_standards/batches/{f}_coded.json")):
        C[o["k"]] = o["c"]
for f in __import__("glob").glob("data/rules_standards/batches/b??_coded.json"):
    for o in json.load(open(f)):
        C[o["k"]] = o["c"]
us = [json.loads(l) for l in open("data/rules_standards/us_instances.jsonl")]
ROWS = {x["row_id"]: x["law"] for x in us}
eu = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
am = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
import openpyxl
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True); r = list(wb["instruments"].values); h = r[0]
cel2row = {str(x[h.index("celex_measured")]): x[0] for x in r[1:] if x[0]}
EUN = {13: "Unfair Commercial Practices", 17: "Toy Safety", 20: "GDPR", 26: "Trade Secrets", 42: "E-evidence", 67: "Product Safety", 74: "Chips Act", 64: "AI Act"}
LAB = {"ftc5": "FTC Act §5", "cpsia": "CPSIA", "ccpa": "CCPA (California)", "dtsa": "Defend Trade Secrets Act", "cloud": "CLOUD Act",
       "cpsa": "Consumer Product Safety Act", "chips": "CHIPS Act", "colorado_ai": "Colorado AI Act"}
E = collections.defaultdict(collections.Counter); U = collections.defaultdict(collections.Counter)
for x in eu:
    if x["src"] == "main" and cel2row.get(x["doc"]) in ROWS and am[x["rid"]] == "private_parties":
        E[cel2row[x["doc"]]][C[x["key"]]] += 1
for x in us:
    if x["addressee"] == "private_parties" or (x["addressee"] == "unclear" and x["n"] in PRIVATE_UNCLEAR.get(x["law"], set())):
        U[x["row_id"]][C[x["key"]]] += 1
sh = lambda c: (lambda n: {"n": n, "R": round(c["R"] / n, 3) if n else None, "standard_like": round((c["S"] + c["M"] + c["L"]) / n, 3) if n else None})(sum(c[k] for k in "RSMLD"))
rows = sorted([{"pair": f"{EUN[k]} → {LAB[ROWS[k]]}", "row_id": k, "eu": sh(E[k]), "us": sh(U[k])} for k in ROWS], key=lambda r: r["eu"]["R"] or 0)
pool = lambda D: sh(sum(D.values(), collections.Counter()))
out = {"pairs": rows, "eu_pooled": pool(E), "us_pooled": pool(U)}
json.dump(out, open("data/rules_standards/us_compare_private.json", "w"), indent=1)
for r in rows:
    print(f'{r["pair"]:52s} EU n={r["eu"]["n"]:4d} R={r["eu"]["R"]:.0%} | US n={r["us"]["n"]:3d} R={r["us"]["R"]:.0%}')
print("pooled", out["eu_pooled"], out["us_pooled"])
print("median R EU", statistics.median(r["eu"]["R"] for r in rows), "US", statistics.median(r["us"]["R"] for r in rows))
