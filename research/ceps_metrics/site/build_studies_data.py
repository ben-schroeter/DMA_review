"""Causal-study list and evidence figures for the mockup's Studies and Evidence pages. Writes site/studies_data.json."""
import collections, json, glob, re, sys, os
sys.path.insert(0, "scripts")
import openpyxl
wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
inst = {r[h.index("celex_measured")].split(";")[0]: dict(zip(h, r)) for r in rows[1:] if r[0]}
src = open("scripts/build_workbook.py").read()
CAUSAL = eval(re.search(r"^CAUSAL = (\(.*?\)|\[.*?\])$", src, re.M | re.S).group(1))
def is_causal(m):
    did = bool(re.search(r"\bDiD\b|\bDID\b", m)); m = m.lower()
    return (did or any(k in m for k in CAUSAL)) and "non-causal" not in m and "not causal" not in m
def short(a):
    a = re.sub(r"\s+et al\.?", " et al.", a or "")
    if "et al." in a or len(a) < 45: return a
    names = [x.strip() for x in re.split(r",| and | & ", a) if x.strip()]
    return names[0] + " et al." if len(names) > 3 else a
S, per, cls, n_ev = [], collections.Counter(), collections.Counter(), 0
for c, r in sorted(inst.items(), key=lambda x: x[1]["row_id"]):
    try: rec = json.load(open(f"data/impact/{c}.json"))
    except FileNotFoundError: continue
    for l in sorted(rec["literature"], key=lambda l: l.get("year") or 0):
        if l.get("category") != "evidence": continue
        n_ev += 1; cls[l.get("source_class")] += 1
        if is_causal(l.get("method", "")):
            per[r["name"]] += 1
            S.append([r["name"], short(l.get("authors")), l.get("year"), l.get("title"), l.get("method"), l.get("direction"),
                      l.get("headline"), l.get("url"), l.get("interested_party", ""), l.get("source_class", "")])
lv = collections.Counter(r["impact_evidence_level"] for r in inst.values())
out = {"S": S, "n_evidence": n_ev, "n_causal": len(S), "per_instrument": per.most_common(), "levels": lv, "classes": cls,
       "strong_moderate": [(r["name"], r["impact_evidence_level"]) for r in sorted(inst.values(), key=lambda r: r["row_id"]) if r["impact_evidence_level"] in ("strong", "moderate")]}
json.dump(out, open("site/studies_data.json", "w"), ensure_ascii=False)
print(n_ev, len(S), dict(lv), dict(cls)); print(per.most_common(12)); print(out["strong_moderate"])

# Full library for the Studies page: every source with collection tags
# ev = evidence since adoption; causal; review = official evaluation, review, audit or implementation report; ia = impact assessment;
# econ = general economics of regulation (not tied to one act)
REV = re.compile(r"evaluation|review|audit|implementation report|monitoring report|fitness check|special report", re.I)
L = []
for c, r in sorted(inst.items(), key=lambda x: x[1]["row_id"]):
    try: rec = json.load(open(f"data/impact/{c}.json"))
    except FileNotFoundError: continue
    for l in sorted(rec["literature"], key=lambda l: -(l.get("year") or 0)):
        cat = l.get("category")
        if cat == "evidence":
            tags = ["ev"] + (["causal"] if is_causal(l.get("method", "")) else []) + (["review"] if l.get("source_class") == "official" and REV.search(l.get("source_type") or "") else [])
        elif cat == "ex-ante assessment":
            tags = ["ia"]
        else:
            continue
        L.append([r["name"], short(l.get("authors")), l.get("year"), l.get("title") or l.get("citation"), l.get("method"), l.get("direction") or "",
                  l.get("headline") or l.get("summary_plain") or "", l.get("url") or l.get("pdf_url") or "", l.get("interested_party", "") or "", l.get("source_class", "") or "other", " ".join(tags)])
for e in json.load(open("data/literature/regulation_economics.json")):
    L.append(["Economics of regulation", short(e.get("authors")), e.get("year"), e.get("title"), e.get("method") or e.get("type"), "",
              e.get("finding") or e.get("summary_plain") or "", e.get("url") or e.get("pdf_url") or "", e.get("interested_party", "") or "", "academic" if "empirical" in (e.get("type") or "") or e.get("type") == "theory" else "other", "econ"])
out["L"] = L
out["collections"] = {k: sum(1 for x in L if k in x[10].split()) for k in ("ev", "causal", "review", "ia", "econ")}
json.dump(out, open("site/studies_data.json", "w"), ensure_ascii=False)
print(out["collections"])
