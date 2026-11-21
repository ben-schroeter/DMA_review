"""Rank correlations between how often companies name a law and the design of its obligations on companies (standards,
management-based and general duties), raw and controlling for size. Backs the risk-management sentence on the What companies
say page (November 2026). Run from research/digital_rulebook."""
import json, glob, collections, math, csv, sys
import numpy as np
sys.path.insert(0, "scripts"); from rs_codes import load as _load
RS = _load()
GC = {}
for f in sorted(glob.glob("data/rules_standards/grid/b??_coded.json")):
    for o in json.load(open(f)): GC[o["k"]] = o["c"]
inst = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
am = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
# attention: from the company-responses builder
src = open("site/build_company_responses.py").read(); exec(src.split("W4, LM4, TM4")[0])
cel_of = {lid: str(db[l["row_id"]][ix["celex_measured"]]).split(";") for lid, l in laws.items()}
mentions = collections.Counter(); per100 = collections.defaultdict(list)
for m in men:
    mentions[m["law"]] += int(m.get("mentions") or 1)
rows = []
for lid, l in laws.items():
    cels = set(cel_of[lid]); rs = collections.Counter(); gr = collections.Counter()
    for x in inst:
        if x["src"] != "main" or x["doc"] not in cels or am[x["rid"]] != "private_parties": continue
        c = RS.get(x["key"]); g = GC.get(x["key"])
        if c and c != "N": rs[c] += 1
        if g and g != "N": gr[g] += 1
    nrs = sum(rs[k] for k in "RSMLD"); ngr = sum(gr[k] for k in ("MM", "ME", "XM", "XE", "L", "D"))
    if nrs < 20: continue
    rows.append(dict(law=lid, name=l["name"], n=nrs, companies=len(comp[lid]), mentions=mentions[lid],
                     std=(rs["S"] + rs["M"] + rs["L"]) / nrs, mgmt=gr["XM"] / ngr if ngr else np.nan, general=gr["XE"] / ngr if ngr else np.nan))
def rank(a): return np.argsort(np.argsort(a)).astype(float)
def spear(a, b):
    m = ~(np.isnan(a) | np.isnan(b)); return np.corrcoef(rank(a[m]), rank(b[m]))[0, 1], int(m.sum())
def partial(a, b, z):   # rank correlation of a and b controlling for z (size)
    m = ~(np.isnan(a) | np.isnan(b)); ra, rb, rz = rank(a[m]), rank(b[m]), rank(z[m])
    res = lambda y: y - np.polyval(np.polyfit(rz, y, 1), rz)
    return np.corrcoef(res(ra), res(rb))[0, 1]
A = {k: np.array([r[k] for r in rows], float) for k in ("n", "companies", "mentions", "std", "mgmt", "general")}
print(f"laws with >= 20 obligations on companies: {len(rows)}")
for att in ("companies", "mentions"):
    for d, lab in (("std", "standards share"), ("mgmt", "management-based share"), ("general", "general-duty share")):
        r, n = spear(A[att], A[d]); pr = partial(A[att], A[d], np.log1p(A["n"]))
        print(f"{att:9s} vs {lab:24s}: rank r = {r:+.2f} (n={n}); controlling for size: {pr:+.2f}")
named = A["companies"] >= 2
print("\namong laws named by 2+ companies:")
for d, lab in (("std", "standards share"), ("mgmt", "management-based share"), ("general", "general-duty share")):
    B = {k: v[named] for k, v in A.items()}
    r, n = spear(B["companies"], B[d]); pr = partial(B["companies"], B[d], np.log1p(B["n"]))
    print(f"companies vs {lab:24s}: rank r = {r:+.2f} (n={n}); controlling for size: {pr:+.2f}")
top = sorted(rows, key=lambda r: -r["companies"])[:8]
print("\nmost named:", [(r["name"][:28], r["companies"], f'{r["std"]:.0%}', f'{r["mgmt"]:.0%}', f'{r["general"]:.0%}') for r in top])
print("median shares, all laws:", f'std {np.nanmedian(A["std"]):.0%}', f'mgmt {np.nanmedian(A["mgmt"]):.0%}', f'general {np.nanmedian(A["general"]):.0%}')
