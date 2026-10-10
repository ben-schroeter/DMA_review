"""Add canonical fields for filtering on the website and in the workbook:
indicator `status_group` and instrument `evidence_level`. Free-text labels stay as written."""
import glob, json, os
from impact_record import OUT


def status_group(s):
    s = s.lower()
    for k, g in [("partially", "partially measured"), ("reported as activity", "reported as activity"), ("mixed", "mixed evidence"),
                 ("not achieved", "measured"), ("not measured", "not measured"), ("not yet", "not measured"),
                 ("measurable", "not measured"), ("measured", "measured")]:
        if s.startswith(k):
            return g
    return "not measured" if s else ""


def evidence_level(r):
    r = r.lower()
    if r.startswith("strong"): return "strong"
    if r.startswith("moderate"): return "moderate"
    if r.startswith("ex-ante") or r.startswith("none ex-post") or r.startswith("monitoring only"): return "ex-ante only"
    if r.startswith("none"): return "none"
    return "thin"


for f in sorted(glob.glob(os.path.join(OUT, "[35]*.json"))):
    rec = json.load(open(f))
    rec["evidence_level"] = evidence_level(rec["evidence_rating"])
    for i in rec["indicators"]:
        i["status_group"] = status_group(i["status"])
    json.dump(rec, open(f, "w"), indent=1, ensure_ascii=False)
print("normalised")
