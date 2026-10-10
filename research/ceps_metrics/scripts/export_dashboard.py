"""Export the dashboard / website datasets (JSON rows) from the workbook and the data/impact records.
Usage (from scripts/): python3 export_dashboard.py <out_dir>"""
import collections, glob, json, os, re, sys
import openpyxl

OUT = sys.argv[1]
CAUSAL = ("causal", "difference-in-difference", "event study", "event-study", "synthetic control", "regression discontinuity",
          "natural experiment", "instrumental variable", "randomi")


def is_causal(m):
    did = bool(re.search(r"\bDiD\b|\bDID\b", m))
    m = m.lower()
    return (did or any(k in m for k in CAUSAL)) and "non-causal" not in m and "not causal" not in m


wb = openpyxl.load_workbook("../ceps_instruments_metrics.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values)
I = {k: i for i, k in enumerate(rows[0])}
inst, cel2id = [], {}
for r in rows[1:]:
    g = lambda k: r[I[k]]
    if g("row_id") is None:
        continue
    for c in str(g("celex_measured")).split(";"):
        cel2id[c] = g("row_id")
    adopted = g("status_oct2026") == "adopted"
    yr = (g("adoption_date") if adopted else g("proposal_date")) or ""
    inst.append({"id": g("row_id"), "instrument": g("name"), "policy_area": g("policy_area_ceps"),
                 "status": "adopted" if adopted else "pending", "year": int(str(yr)[:4]) if yr else None,
                 "words": g("words_legal_text"), "restrictions": g("restrictions_total"), "restrictions_private": g("addr_private_parties"),
                 "secondary_acts": (g("n_implementing_acts") or 0) + (g("n_delegated_acts") or 0),
                 "evidence_level": g("impact_evidence_level"), "studies": g("n_impact_studies"), "causal_studies": g("n_causal_studies"),
                 "promises": g("n_promised_indicators"), "promises_with_evidence": g("n_indicators_measured"),
                 "impact_summary": g("impact_summary"), "source_url": g("source_url")})

studies, promises, status = [], [], collections.Counter()
for f in sorted(glob.glob("../data/impact/[35]*.json")):
    r = json.load(open(f))
    iid = cel2id[r["celex"]]
    for n, l in enumerate(r["literature"]):
        if l.get("category") == "enforcement or case law":
            continue
        studies.append({"key": f"{iid}-{n + 1}", "instrument_id": iid, "instrument": r["name"], "category": l.get("category", "evidence"),
                        "year": l.get("year"), "authors": l.get("authors"), "title": l.get("title"), "venue": l.get("venue"),
                        "source_type": l.get("source_type"), "method": l.get("method"),
                        "causal": "yes" if l.get("category", "evidence") == "evidence" and is_causal(l.get("method") or "") else "no",
                        "direction": l.get("direction"), "headline": l.get("headline"), "summary": l.get("summary_plain"),
                        "url": l.get("url"), "verified": l.get("verified"), "interested_party": l.get("interested_party") or ""})
    for n, i in enumerate(r["indicators"]):
        promises.append({"key": f"{iid}-{n + 1}", "instrument_id": iid, "type": i["type"], "objective": i["objective"],
                         "indicator": i["indicator"], "target": i["target_or_baseline"], "evidence": i["evidence"],
                         "status": i["status"], "status_group": i.get("status_group", "")})
        if i.get("status_group"):
            status[i["status_group"]] += 1

b = list(wb["benchmarks"].values)
order = ["measured", "partially measured", "mixed evidence", "reported as activity", "not measured"]
for name, data in [("instruments", inst), ("studies", studies), ("promises", promises),
                   ("promise_status", [{"status": k, "promises": status[k]} for k in order]),
                   ("benchmark", [{"text": "Sarbanes-Oxley Act (US, 2002)", "restrictions": b[1][4], "per_1000_words": b[1][8]},
                                  {"text": "Average EU act (105 adopted)", "restrictions": b[4][4], "per_1000_words": b[4][8]}])]:
    json.dump(data, open(os.path.join(OUT, name + ".json"), "w"), ensure_ascii=False)
print(len(inst), "instruments", len(studies), "sources", collections.Counter(s["category"] for s in studies),
      sum(s["causal"] == "yes" for s in studies), "causal")
