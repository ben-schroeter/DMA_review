"""Regulatory design grid (Coglianese): roll the reader codes in data/rules_standards/grid/bNN_coded.json up to the whole acquis,
main laws vs implementing/delegated acts, addressees, adoption periods, legal form, company types, and compare them with the
earlier rules/standards (Kaplow) codes. Writes data/rules_standards/grid/summary.json. Run from research/digital_rulebook.
Shares exclude N (not a duty)."""
import json, glob, collections, runpy, sys
G = {}
for f in sorted(glob.glob("data/rules_standards/grid/b??_coded.json")):
    for o in json.load(open(f)):
        G[o["k"]] = o["c"]
K = {}
for f in sorted(glob.glob("data/rules_standards/batches/b??_coded.json")):
    for o in json.load(open(f)):
        K[o["k"]] = o["c"]
inst = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
E = {o["celex"]: o for o in json.load(open("data/policy_eras/instruments.json")) if o["status"] == "adopted"}
SEC = {s["celex"]: s for s in json.load(open("data/secondary_acts.json"))}
AM = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
AS = [json.loads(l)["formal"] for l in open("data/addressee/v2_secondary.jsonl")]
DELIMPL = {"DEC_IMPL", "REG_IMPL", "REG_DEL", "DIR_DEL"}
CELLS = ["MM", "ME", "XM", "XE", "L", "D"]


def shares(c):
    n = sum(c[k] for k in CELLS)
    if not n:
        return {"n": 0}
    s = {k: round(c[k] / n, 3) for k in CELLS}
    s.update(n=n, means=round((c["MM"] + c["XM"]) / n, 3), ends=round((c["ME"] + c["XE"]) / n, 3),
             micro=round((c["MM"] + c["ME"]) / n, 3), macro=round((c["XM"] + c["XE"]) / n, 3),
             means_left_open=round((c["ME"] + c["XM"] + c["XE"]) / n, 3))
    return s


per = lambda d: "before 2010" if d < "2010" else ("2010-2017" if d < "2018" else "2018 or later")
form = lambda celex: {"R": "regulation", "L": "directive", "D": "decision"}.get(celex[5:6], "other")
B = collections.defaultdict(collections.Counter)
cross = collections.Counter(); missing = 0; n_tot = collections.Counter()
for x in inst:
    c = G.get(x["key"])
    if c is None:
        missing += 1; continue
    n_tot[x["src"]] += 1
    k = K.get(x["key"]); cross[(k, c)] += 1
    if x["src"] == "main":
        if x["doc"] not in E:
            continue
        law, a = x["doc"], AM[x["rid"]]; layer = "main"
    else:
        s = SEC.get(x["doc"])
        if not s or s.get("parent") not in E or s.get("type") not in DELIMPL:
            continue
        law, a = s["parent"], AS[x["rid"]]; layer = "implementing/delegated"
    B["N_" + layer][c] += 1
    if c == "N":
        continue
    p = per(E[law]["adoption_date"])
    keys = [("layer", layer), ("all", "all")]
    if layer == "main":
        keys += [("period", p), ("form", form(law)), ("addressee", a)]
        if a == "private_parties":
            keys += [("companies_period", p)]
    else:
        keys += [("secondary_by_parent_period", p)]
    if a == "private_parties":
        keys += [("companies_" + ("main" if layer == "main" else "secondary"), "all")]
    for kk in keys:
        B[kk][c] += 1
out = {"missing": missing, "coded": dict(n_tot), "not_a_duty": {k[2:]: round(v["N"] / sum(v.values()), 3) for k, v in B.items() if isinstance(k, str)},
       "groups": {f"{a}|{b}": shares(v) for (a, b), v in ((k, v) for k, v in B.items() if isinstance(k, tuple))},
       "kaplow_to_grid": {f"{a}->{b}": n for (a, b), n in sorted(cross.items(), key=lambda t: (str(t[0][0]), -t[1]))}}
# company types (same selection as scripts/company_types.py)
try:
    src = open("scripts/company_types.py").read().split("out = {")[0]
    ns = {}; exec(compile(src, "company_types_head", "exec"), ns)
    import hashlib
    key = lambda r: hashlib.sha1(((r.get("chapeau") or "")[-200:] + "|" + r["clause"]).encode()).hexdigest()[:12]
    rows, M, applies, TYPES = ns["rows"], ns["M"], ns["applies"], ns["TYPES"]
    ct = {}
    for t in ["B"] + TYPES:
        sel = [r for r in rows if (M.get(r["row_id"], {}).get(ns["B"]) == "F" if t == "B" else (t in M.get(r["row_id"], {}) and applies(M[r["row_id"]][t], r, t)))]
        c = collections.Counter(G.get(key(r)) for r in sel)
        ct[t] = {"all": shares(c), "main": shares(collections.Counter(G.get(key(r)) for r in sel if r["kind"] == "main")),
                 "secondary": shares(collections.Counter(G.get(key(r)) for r in sel if r["kind"] != "main")), "uncoded": c[None]}
    out["company_types"] = ct
except Exception as e:  # keep the main summary even if the company-type join fails
    out["company_types_error"] = repr(e)
json.dump(out, open("data/rules_standards/grid/summary.json", "w"), indent=1)
for k, v in out["groups"].items():
    if v.get("n"):
        print(f'{k:45s} n={v["n"]:6d} MM {v["MM"]:.0%} ME {v["ME"]:.0%} XM {v["XM"]:.0%} XE {v["XE"]:.0%} L {v["L"]:.0%} D {v["D"]:.0%} | means left open {v["means_left_open"]:.0%}')
print("not a duty:", out["not_a_duty"], "missing:", missing)
