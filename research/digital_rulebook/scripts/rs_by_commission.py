"""Rules vs standards by Commission term: main acts by the Commission that proposed them, implementing/delegated acts by
the Commission in office at adoption. Shares exclude obligations coded N. Writes data/rules_standards/by_commission.json."""
import json, glob, collections, openpyxl
import sys as _sys; _sys.path.insert(0, "scripts"); from rs_codes import load as _load_codes
C = _load_codes()   # rules/standards codes, harmonised with the grid's "not a duty"
inst = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
am = [json.loads(l)["formal"] for l in open("data/addressee/v2_final_main.jsonl")]
asec = [json.loads(l)["formal"] for l in open("data/addressee/v2_secondary.jsonl")]
eras = {o["celex"]: o for o in json.load(open("data/policy_eras/instruments.json"))}
sec = {s["celex"]: s for s in json.load(open("data/secondary_acts.json"))}
TERMS = [("Delors", 1985.0), ("Santer", 1995.04), ("Prodi", 1999.7), ("Barroso I", 2004.9), ("Barroso II", 2010.1),
         ("Juncker", 2014.84), ("von der Leyen I", 2019.92), ("von der Leyen II", 2024.92)]
fy = lambda d: int(d[:4]) + (int(d[5:7]) - 1) / 12 + (int(d[8:10]) - 1) / 365
term = lambda v: [t for t, s in TERMS if s <= v][-1]
agg = collections.defaultdict(collections.Counter); acts = collections.defaultdict(set)
for x in inst:
    c = C[x["key"]]
    if c == "N":
        continue
    if x["src"] == "main":
        e = eras.get(x["doc"])
        if not e:
            continue
        t = term(fy(e["proposal_date"])); a = am[x["rid"]]; layer = "main"
    else:
        s = sec.get(x["doc"])
        if not s or not s.get("date") or s.get("parent") not in eras:
            continue
        t = term(fy(s["date"])); a = asec[x["rid"]]; layer = "secondary"
    for grp in (["all", "companies"] if a == "private_parties" else ["all"]):
        agg[(layer, grp, t)][c] += 1
    acts[(layer, t)].add(x["doc"])
out = []
for layer in ("main", "secondary"):
    for t, _ in TERMS:
        row = {"layer": layer, "commission": t, "acts": len(acts[(layer, t)])}
        for grp in ("all", "companies"):
            cnt = agg[(layer, grp, t)]; n = sum(cnt[k] for k in "RSMLD")
            row[grp] = {"n": n, "rules": round(cnt["R"] / n, 3) if n else None, "standards": round((cnt["S"] + cnt["M"] + cnt["L"]) / n, 3) if n else None}
        out.append(row)
json.dump(out, open("data/rules_standards/by_commission.json", "w"), indent=1)
for r in out:
    a, c = r["all"], r["companies"]
    if a["n"]:
        print(f'{r["layer"]:9s} {r["commission"]:16s} acts={r["acts"]:4d}  all n={a["n"]:5d} rules={a["rules"]:.0%} std={a["standards"]:.0%} | companies n={c["n"]:5d} rules={(c["rules"] or 0):.0%}')
