"""Rules vs standards by type of company (the six types and baseline of scripts/company_types.py), using the second-reader
codes in data/rules_standards. Writes data/rules_standards/by_company_type.json. Run from research/digital_rulebook."""
import json, glob, hashlib, collections
src = open("scripts/company_types.py").read().split("out = {")[0]
exec(compile(src, "company_types_head", "exec"))
import sys as _sys; _sys.path.insert(0, "scripts"); from rs_codes import load as _load_codes
C = _load_codes()   # rules/standards codes, harmonised with the grid's "not a duty"
key = lambda r: hashlib.sha1(((r.get("chapeau") or "")[-200:] + "|" + r["clause"]).encode()).hexdigest()[:12]
def tally(sel):
    out = {}
    for layer in ("all", "main", "secondary"):
        cnt = collections.Counter(C.get(key(r), "?") for r in sel if layer == "all" or r["kind"] == layer)
        n = sum(cnt[k] for k in "RSMLD")
        out[layer] = {"n": n, "uncoded": cnt["?"], "rules": round(cnt["R"] / n, 3) if n else None,
                      "standards": round((cnt["S"] + cnt["M"] + cnt["L"]) / n, 3) if n else None}
    laws = collections.Counter()
    for r in sel:
        if C.get(key(r)) in ("S", "M", "L"):
            laws[by_id[r["row_id"]]["name"]] += 1
    out["most_standards"] = laws.most_common(4)
    return out
res = {"baseline": tally([r for r in rows if M.get(r["row_id"], {}).get(B) == "F"])}
for t in TYPES:
    res[t] = tally([r for r in rows if t in M.get(r["row_id"], {}) and applies(M[r["row_id"]][t], r, t)])
json.dump(res, open("data/rules_standards/by_company_type.json", "w"), indent=1, ensure_ascii=False)
for k, v in res.items():
    a, m, s = v["all"], v["main"], v["secondary"]
    print(f'{NAMES[k if k != "baseline" else "B"][:38]:38s} n={a["n"]:5d} unc={a["uncoded"]:3d} rules={a["rules"]:.0%} | main {m["n"]:5d} {m["rules"] or 0:.0%} | second {s["n"]:5d} {s["rules"] or 0:.0%} | {[ (x[:26],c) for x,c in v["most_standards"][:3]]}')

# over time: by period of adoption (main act or implementing/delegated act)
PER = [("before 2015", 0, 2014), ("2015-2019", 2015, 2019), ("2020 or later", 2020, 2100)]
def period_shares(sel):
    o = {}
    for lab, a, b in PER:
        cnt = collections.Counter(C.get(key(r)) for r in sel if a <= r["year"] <= b)
        n = sum(cnt[k] for k in "RSMLD")
        o[lab] = {"n": n, "rules": round(cnt["R"] / n, 3) if n else None}
    return o
print()
for k in ["baseline"] + TYPES:
    sel = [r for r in rows if M.get(r["row_id"], {}).get(B) == "F"] if k == "baseline" else [r for r in rows if k in M.get(r["row_id"], {}) and applies(M[r["row_id"]][k], r, k)]
    res[k]["by_period"] = period_shares(sel)
    print(f'{NAMES[k if k != "baseline" else "B"][:38]:38s}', "  ".join(f'{lab}: {v["rules"]:.0%} (n={v["n"]})' if v["rules"] is not None else f"{lab}: –" for lab, v in res[k]["by_period"].items()))
json.dump(res, open("data/rules_standards/by_company_type.json", "w"), indent=1, ensure_ascii=False)
