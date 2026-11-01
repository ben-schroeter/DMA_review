"""Add canonical fields for filtering on the website and in the workbook:
indicator `status_group`, instrument `evidence_level` and source `category`. Free-text labels stay as written."""
import glob, json, os, re
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


EXANTE = re.compile(r"impact assessment|legislative proposal|commission proposal|explanatory note", re.I)
ENFORCE = ("enforcement", "infringement", "legal ruling", "administrative record")


def category(l):
    """ex-ante assessment: grouped with the proposal's promises; enforcement or case law: kept in the record but not counted as impact evidence."""
    st = l.get("source_type", "").lower()
    if st == "court judgment" or (l.get("method", "").lower().startswith(ENFORCE) and "implementation" not in st):
        return "enforcement or case law"
    # later amending proposals (e.g. the 2025 Digital Omnibus) carry evaluation evidence, not the initial assessment
    if EXANTE.search(st) and "omnibus" not in l.get("title", "").lower():
        return "ex-ante assessment"
    return "evidence"


def source_class(l):
    """academic / official / think tank / consultancy or industry / other; set by the search agents for new sources, inferred here for older ones."""
    if l.get("source_class"):
        return l["source_class"]
    st = l.get("source_type", "").lower()
    if re.search(r"think[- ]tank|ngo|consumer organisation|observatory|cerre|bruegel|ceps|independent monitoring", st): return "think tank"
    if re.search(r"industry|consultancy|company|trade press|stakeholder|advocacy", st) and "commission" not in st: return "consultancy or industry"
    if re.search(r"peer-reviewed|working paper|book chapter|academic|conference", st) and "jrc" not in st: return "academic"
    if re.search(r"jrc|national post-implementation|commission|agency|audit|regulator|central bank|statistic|register|parliament|government|court|official|intergovernmental|supervisory|member state|legislative|advisory|enforcement", st): return "official"
    return "other"


for f in sorted(glob.glob(os.path.join(OUT, "[35]*.json"))):
    rec = json.load(open(f))
    rec["evidence_level"] = evidence_level(rec["evidence_rating"])
    for i in rec["indicators"]:
        i["status_group"] = status_group(i["status"])
    for l in rec["literature"]:
        l["category"] = category(l)
        l["source_class"] = source_class(l)
    json.dump(rec, open(f, "w"), indent=1, ensure_ascii=False)
print("normalised")
