"""The 8 matched EU-US pairs on both measures: rules vs standards (Kaplow, harmonised codes from scripts/rs_codes.py) and the
regulatory design grid (Coglianese, data/rules_standards/grid/). EU side: the main act; US side: the counterpart statute.
All obligations, and obligations on companies (EU: formal addressee private parties; US: classifier private parties plus
the hand-read unclear items in scripts/us_private.py). Writes data/rules_standards/grid/us_compare.json.
Run from research/digital_rulebook."""
import json, glob, collections, re, statistics, sys, openpyxl
sys.path.insert(0, "scripts"); from rs_codes import load
K = load()
G = {}
for f in glob.glob("data/rules_standards/grid/*_coded.json"):
    if "pilot" not in f:
        for o in json.load(open(f)):
            G[o["k"]] = o["c"]
PRIVATE_UNCLEAR = eval(re.search(r"PRIVATE_UNCLEAR = (\{.*?\}\})", open("scripts/us_private.py").read(), re.S).group(1))
us = [json.loads(l) for l in open("data/rules_standards/us_instances.jsonl")]
eu = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
am = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True); r = list(wb["instruments"].values); h = r[0]
cel2row = {c: x[0] for x in r[1:] if x[0] for c in str(x[h.index("celex_measured")]).split(";")}   # multi-CELEX rows (ESAP, E-evidence)
ROWS = {x["row_id"]: x["law"] for x in us}
EUN = {13: "Unfair Commercial Practices Directive", 17: "Toy Safety Directive", 20: "GDPR", 26: "Trade Secrets Directive", 42: "E-evidence Regulation",
       67: "General Product Safety Regulation", 74: "Chips Act", 64: "AI Act"}
LAB = {"ftc5": "FTC Act §5", "cpsia": "CPSIA", "ccpa": "CCPA (California)", "dtsa": "Defend Trade Secrets Act", "cloud": "CLOUD Act",
       "cpsa": "Consumer Product Safety Act", "chips": "CHIPS Act", "colorado_ai": "Colorado AI Act (state)"}
D = collections.defaultdict(lambda: collections.defaultdict(list))   # D[row][side_scope] -> list of (kaplow, grid)
for x in eu:
    row = cel2row.get(x["doc"])
    if x["src"] == "main" and row in ROWS:
        D[row]["eu_all"].append((K[x["key"]], G[x["key"]]))
        if am[x["rid"]] == "private_parties":
            D[row]["eu_comp"].append((K[x["key"]], G[x["key"]]))
for x in us:
    D[x["row_id"]]["us_all"].append((K[x["key"]], G[x["key"]]))
    if x["addressee"] == "private_parties" or (x["addressee"] == "unclear" and x["n"] in PRIVATE_UNCLEAR.get(x["law"], set())):
        D[x["row_id"]]["us_comp"].append((K[x["key"]], G[x["key"]]))


def stats(items):
    duties = [(k, g) for k, g in items if k != "N" and g != "N"]
    n = len(duties)
    out = {"items": len(items), "duties": n, "not_a_duty": round(1 - n / len(items), 3) if items else None}
    if not n:
        return out
    kc = collections.Counter(k for k, _ in duties); gc = collections.Counter(g for _, g in duties)
    out.update({"rule": round(kc["R"] / n, 3), "standard_like": round((kc["S"] + kc["M"] + kc["L"]) / n, 3)})
    out.update({c: round(gc[c] / n, 3) for c in ("MM", "ME", "XM", "XE", "L", "D")})
    out["micro"] = round((gc["MM"] + gc["ME"]) / n, 3); out["means_left_open"] = round((gc["ME"] + gc["XM"] + gc["XE"]) / n, 3)
    return out


pairs = []
for row in sorted(ROWS):
    pairs.append({"pair": f"{EUN[row]} → {LAB[ROWS[row]]}", "row_id": row, **{k: stats(D[row][k]) for k in ("eu_all", "us_all", "eu_comp", "us_comp")}})
pooled = {k: stats([i for row in ROWS for i in D[row][k]]) for k in ("eu_all", "us_all", "eu_comp", "us_comp")}
med = {k: {m: statistics.median(p[k][m] for p in pairs if p[k].get(m) is not None) for m in ("rule", "means_left_open", "MM", "XE")}
       for k in ("eu_all", "us_all", "eu_comp", "us_comp")}
json.dump({"pairs": pairs, "pooled": pooled, "median": med}, open("data/rules_standards/grid/us_compare.json", "w"), indent=1)
f = lambda v: "  –" if v is None else f"{100 * v:3.0f}%"
for scope in ("all", "comp"):
    print(f"\n== {'all obligations' if scope == 'all' else 'obligations on companies'}  (EU | US): duties, not-a-duty, rule share, MM ME XM XE, means left open")
    for p in pairs + [{"pair": "POOLED", **{k: pooled[k] for k in pooled}}]:
        e, u = p[f"eu_{scope}"], p[f"us_{scope}"]
        row = lambda s: f'{s["duties"]:5d} {f(s["not_a_duty"])} R{f(s.get("rule"))} | {f(s.get("MM"))}{f(s.get("ME"))}{f(s.get("XM"))}{f(s.get("XE"))} | open{f(s.get("means_left_open"))}'
        print(f'{p["pair"][:50]:50s} EU {row(e)}   US {row(u)}')
print("\nmedian", json.dumps(med))
