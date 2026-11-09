"""Rules vs standards by type of company and Commission term: main acts by the Commission that proposed them,
implementing/delegated acts by the Commission in office at adoption. Writes data/rules_standards/company_type_by_commission.json."""
import json, glob, hashlib, collections
src = open("scripts/company_types.py").read().split("out = {")[0]
exec(compile(src, "company_types_head", "exec"))
import sys as _sys; _sys.path.insert(0, "scripts"); from rs_codes import load as _load_codes
C = _load_codes()   # rules/standards codes, harmonised with the grid's "not a duty"
key = lambda r: hashlib.sha1(((r.get("chapeau") or "")[-200:] + "|" + r["clause"]).encode()).hexdigest()[:12]
TERMS = [("Delors", 1985.0), ("Santer", 1995.04), ("Prodi", 1999.7), ("Barroso I", 2004.9), ("Barroso II", 2010.1),
         ("Juncker", 2014.84), ("von der Leyen I", 2019.92), ("von der Leyen II", 2024.92)]
fy = lambda d: (lambda s: int(s[:4]) + (int(s[5:7]) - 1) / 12)(str(d))
term = lambda v: [t for t, s in TERMS if s <= v][-1]
def com(r):
    d = by_id[r["row_id"]]["proposal_date"] if r["kind"] == "main" else sec[r["doc"]]["date"]
    return term(fy(d))
res = {}
groups = {"baseline": [r for r in rows if M.get(r["row_id"], {}).get(B) == "F"]}
for t in TYPES:
    groups[t] = [r for r in rows if t in M.get(r["row_id"], {}) and applies(M[r["row_id"]][t], r, t)]
for k, sel in groups.items():
    res[k] = {}
    for layer in ("main", "secondary", "both"):
        cnt = collections.defaultdict(collections.Counter)
        for r in sel:
            if layer != "both" and r["kind"] != layer:
                continue
            c = C.get(key(r))
            if c and c != "N":
                cnt[com(r)][c] += 1
        res[k][layer] = {t: {"n": sum(cnt[t][x] for x in "RSMLD"), "rules": round(cnt[t]["R"] / sum(cnt[t][x] for x in "RSMLD"), 3)}
                         for t, _ in TERMS if sum(cnt[t][x] for x in "RSMLD")}
json.dump(res, open("data/rules_standards/company_type_by_commission.json", "w"), indent=1)
SH = ["Prodi", "Barroso I", "Barroso II", "Juncker", "von der Leyen I", "von der Leyen II"]
for layer in ("main", "secondary"):
    print("\n" + layer, " | ".join(f"{t:>14s}" for t in SH))
    for k in groups:
        cells = []
        for t in SH:
            v = res[k][layer].get(t)
            cells.append(f"{v['rules']:.0%} ({v['n']})".rjust(14) if v else "–".rjust(14))
        print(f"{NAMES[k if k != 'baseline' else 'B'][:24]:24s}", " | ".join(cells))
