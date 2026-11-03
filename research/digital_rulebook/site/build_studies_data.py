"""Causal-study list and evidence figures for the mockup's Studies and Evidence pages. Writes site/studies_data.json."""
import collections, json, glob, re, sys, os
sys.path.insert(0, "scripts")
import openpyxl
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
inst = {r[h.index("celex_measured")].split(";")[0]: dict(zip(h, r)) for r in rows[1:] if r[0] and r[h.index("status")] == "adopted"}  # pending proposals enter once adopted
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
# Withdrawn proposals: their impact assessments and studies, in a collection of their own ("wd"), kept out of the counts above
WD = {"fida": "52023PC0360", "late-payment": "52023PC0533", "digital-services-tax": "52018PC0148", "significant-digital-presence": "52018PC0147",
      "vat-imported-distance-sales": "52023PC0262"}
for f in json.load(open("site/forthcoming_list.json")):
    c = WD.get(f["id"])
    if f["stage"] != "withdrawn" or not c or not os.path.exists(f"data/impact/{c}.json"): continue
    for l in sorted(json.load(open(f"data/impact/{c}.json"))["literature"], key=lambda l: -(l.get("year") or 0)):
        L.append([{"vat-imported-distance-sales": "VAT on imported distance sales", "significant-digital-presence": "Significant digital presence"}.get(f["id"], f["name"]) + " (withdrawn)", short(l.get("authors")), l.get("year"), l.get("title") or l.get("citation"), l.get("method"), l.get("direction") or "",
                  l.get("headline") or l.get("summary_plain") or "", l.get("url") or l.get("pdf_url") or "", l.get("interested_party", "") or "", l.get("source_class", "") or "other", "wd"])
# Forthcoming initiatives: impact assessments (or the staff documents that replace them) and studies, collection "fc", kept out of the counts above
FC_REC = {"psr": "52023PC0367", "psd3": "52023PC0366", "digital-euro": "52023PC0369", "csar": "52022PC0209", "csa-directive": "52024PC0060",
          "digital-travel": "52024PC0670", "space-act": "52025PC0335", "infosec": "52022PC0119", "digital-omnibus": "52025PC0837",
          "digital-networks-act": "52026PC0016", "cybersecurity-act-2": "52026PC0011", "cloud-ai-development-act": "52026PC0502",
          "eu-kids-act": "52026PC0681", "digital-fairness-act": "fc-digital-fairness-act"}
IA_KIND = {"full": "Commission impact assessment", "analysis": "Commission analysis of impacts (no full impact assessment)", "swd": "Commission staff working document (no impact assessment)"}
for f in json.load(open("site/forthcoming_list.json")):
    if f["stage"] == "withdrawn": continue
    c = FC_REC.get(f["id"]); lab = f["name"] + " (forthcoming)"
    if c and os.path.exists(f"data/impact/{c}.json"):
        for l in sorted(json.load(open(f"data/impact/{c}.json"))["literature"], key=lambda l: -(l.get("year") or 0)):
            L.append([lab, short(l.get("authors")), l.get("year"), l.get("title") or l.get("citation"), l.get("method"), l.get("direction") or "",
                      l.get("headline") or l.get("summary_plain") or "", l.get("url") or l.get("pdf_url") or "", l.get("interested_party", "") or "", l.get("source_class", "") or "other", "fc"])
    elif f.get("impact_assessment") in IA_KIND:
        for ref, url in zip(f["impact_assessment_docs"], f["impact_assessment_urls"]):
            L.append([lab, "European Commission", int(ref[4:8]), f'{IA_KIND[f["impact_assessment"]]}: {ref}', "ex-ante assessment", "",
                      IA_KIND[f["impact_assessment"]] + " accompanying the proposal.", url, "", "official", "fc"])
for e in json.load(open("data/literature/regulation_economics.json")):
    L.append(["Economics of regulation", short(e.get("authors")), e.get("year"), e.get("title"), e.get("method") or e.get("type"), "",
              e.get("finding") or e.get("summary_plain") or "", e.get("url") or e.get("pdf_url") or "", e.get("interested_party", "") or "", "academic" if "empirical" in (e.get("type") or "") or e.get("type") == "theory" else "other", "econ"])
out["L"] = L
out["collections"] = {k: sum(1 for x in L if k in x[10].split()) for k in ("ev", "causal", "review", "ia", "econ", "fc", "wd")}
json.dump(out, open("site/studies_data.json", "w"), ensure_ascii=False)
print(out["collections"])
