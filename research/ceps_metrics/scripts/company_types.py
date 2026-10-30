"""What the rules mean for six types of company, plus a baseline layer that applies to every company.

Types (by activity, not by firm: one firm can be several types):
  GK  gatekeepers and very large platforms          PL  online platforms and digital services
  CL  cloud, data and AI                           TC  telecoms
  FI  finance, payments and crypto                  PR  makers of connected products
  B   baseline: rules that apply to companies generally (GDPR, consumer law, VAT, company law, competition, IP)

For each adopted law the matrix below says which types it applies to: "F" (all its obligations on companies), a list of
article ranges (obligations in those articles of the law), or a keyword pattern (obligations whose sentence, list lead-in
or heading names that kind of company; also used for the law's implementing and delegated acts when article ranges are
given). Laws not listed (EU funding programmes, whose company obligations are grant conditions, and laws addressed to
public bodies) are not counted for any type.
Writes data/company_types/matrix.csv and summary.json. Run from research/ceps_metrics."""
import collections, csv, json, os, re
import openpyxl

TYPES = ["GK", "PL", "CL", "TC", "FI", "PR"]
NAMES = {"GK": "Gatekeepers and very large platforms", "PL": "Online platforms and digital services", "CL": "Cloud, data and AI",
         "TC": "Telecoms", "FI": "Finance, payments and crypto", "PR": "Makers of connected products", "B": "Baseline: all companies"}
VLOP = r"very large online|gatekeeper"
MKT = r"online marketplace|fulfilment service|providers? of online platforms|online interface"
B = "B"
M = {   # row_id: {type: rule}
    # baseline: companies in general
    20: {B: "F"}, 9: {B: "F"}, 2: {B: "F"}, 6: {B: "F"}, 13: {B: "F"}, 18: {B: "F"}, 28: {B: "F"}, 27: {B: "F"}, 30: {B: "F"},
    31: {B: "F"}, 8: {B: "F"}, 29: {B: "F"}, 14: {B: "F"}, 90: {B: "F"}, 111: {B: "F"}, 11: {B: "F"}, 66: {B: "F"}, 85: {B: "F"},
    4: {B: "F"}, 5: {B: "F"}, 12: {B: "F"}, 26: {B: "F"}, 89: {B: "F"}, 96: {B: "F"}, 25: {B: "F"}, 69: {B: "F"}, 87: {B: "F"},
    # platforms
    59: {"GK": "F"},
    60: {"GK": "F", "PL": ((11, 32), r"(?<!very large )online platform|hosting|intermediary|marketplace|transparency report"),
         "CL": ((11, 18), r"hosting"), "TC": ((11, 15), r"mere conduit|intermediary")},
    44: {"GK": "F", "PL": "F"}, 73: {"PL": "F"}, 115: {"GK": "F", "PL": "F"}, 71: {"GK": "F", "PL": "F"},
    84: {"GK": r"very large|online platform"}, 15: {"GK": r"video-sharing", "PL": r"video-sharing"},
    33: {"GK": r"online content-sharing", "PL": r"online content-sharing"}, 112: {"GK": "F", "PL": "F"},
    19: {"GK": r"platform operator|reporting platform", "PL": r"platform operator|reporting platform", "FI": r"financial institution|reporting financial"},
    # cloud, data, AI
    38: {"CL": "F"}, 58: {"CL": "F"}, 95: {"CL": "F"}, 37: {"CL": "F", "PR": "F"},
    76: {"PR": ((3, 12), r"connected product|data holder|manufacturer"), "CL": ((23, 36), r"data processing service|switching|interoperab")},
    64: {"CL": "F", "PR": r"high-risk|provider", "GK": r"general-purpose|deployer|transparen", "PL": r"deployer|transparen"},
    22: {"GK": VLOP, "FI": r"credit institution|financial|payment"},   # trust service providers are a specialised group outside the six types
    # telecoms
    10: {"TC": "F"}, 24: {"TC": "F"}, 32: {"TC": "F", "GK": r"number-independent", "PL": r"number-independent"}, 63: {"TC": "F"}, 91: {"TC": "F"},
    # cybersecurity across types
    61: {"GK": "F", "PL": "F", "CL": "F", "TC": "F", "PR": "F"},
    # finance
    23: {"FI": "F"}, 56: {"FI": "F"}, 57: {"FI": "F", "CL": r"ict third-party service provider"}, 68: {"FI": "F"}, 55: {"FI": "F"},
    # connected products
    83: {"PR": "F"}, 109: {"PR": "F"}, 110: {"PR": "F"}, 65: {"PR": "F"}, 17: {"PR": "F"}, 103: {"PR": "F"}, 86: {"PR": "F"},
    94: {"PR": "F"}, 81: {"PR": "F"}, 74: {"PR": "F"}, 92: {"PR": "F"},
    67: {"PR": "F", "GK": MKT, "PL": MKT}, 80: {"PR": "F", "GK": MKT, "PL": MKT}, 41: {"PR": "F", "GK": MKT, "PL": MKT},
    # law enforcement duties on service providers
    42: {"GK": "F", "PL": "F", "CL": "F", "TC": "F"}, 51: {"GK": "F", "PL": "F", "CL": "F"}, 53: {"GK": "F"},
    77: {"GK": r"hosting|intermediary|online platform", "PL": r"hosting|intermediary|online platform"},
}

wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)


def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]


I, S = sheet("instruments"), sheet("secondary_acts")
main = {r["celex_measured"]: r for r in I if r["celex_measured"] and r["status_oct2026"] == "adopted" and r["adoption_date"] and r["restrictions_total"] is not None}
sec = {r["celex"]: r for r in S if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None}
by_id = {r["row_id"]: r for r in I}
rows = [r for r in map(json.loads, open("data/reporting/reporting_instances.jsonl"))
        if r["addressee"] == "private_parties" and ((r["kind"] == "main" and r["doc"] in main) or (r["kind"] == "secondary" and r["doc"] in sec))]
for r in rows:
    r["row_id"] = main[r["doc"]]["row_id"] if r["kind"] == "main" else sec[r["doc"]]["parent_row_id"]
    r["year"] = int(str(main[r["doc"]]["adoption_date"])[:4]) if r["kind"] == "main" else int(str(sec[r["doc"]]["date"])[:4])


def art_no(a):
    m = re.match(r"Art\.\s*(\d+)", a or "")
    return int(m.group(1)) if m else None


def applies(rule, r, t=None):
    if rule == "F":
        return True
    title = (sec[r["doc"]]["title"] or "").lower() if r["kind"] == "secondary" else ""
    if t != "GK" and re.search(r"very large online|audits?\b", title):
        return False          # secondary acts for very large platforms only (e.g. DSA audits)
    text = " ".join([r.get("heading") or "", r.get("chapeau") or "", r["clause"]]).lower()
    if isinstance(rule, tuple):
        (lo, hi), kw = rule
        if r["kind"] == "main":
            n = art_no(r["article"])
            return n is not None and lo <= n <= hi
        rule = kw
    return bool(re.search(rule, text) or (title and re.search(rule, title)))


def profile(sel):
    rep = [r for r in sel if r["reporting"]]
    laws = collections.Counter(by_id[r["row_id"]]["name"] for r in sel)
    return {"obligations": len(sel), "start_2018": sum(r["year"] <= 2017 for r in sel),
            "in_implementing_delegated": sum(r["kind"] == "secondary" for r in sel),
            "since_2020": sum(r["year"] >= 2020 for r in sel),
            "reporting": len(rep), "reporting_by_type": dict(collections.Counter(r["type"] for r in rep).most_common()),
            "reporting_event": sum(r["cadence"] == "event" for r in rep), "reporting_periodic": sum(r["cadence"] == "periodic" for r in rep),
            "laws": len(laws), "top_laws": dict(laws.most_common(8)),
            "by_year": dict(sorted(collections.Counter(r["year"] for r in sel).items()))}


out = {"names": NAMES, "types": {}}
base = [r for r in rows if M.get(r["row_id"], {}).get(B) == "F"]
out["baseline"] = profile(base)
for t in TYPES:
    sel = [r for r in rows if t in M.get(r["row_id"], {}) and applies(M[r["row_id"]][t], r, t)]
    p = profile(sel)
    p["with_baseline"] = p["obligations"] + out["baseline"]["obligations"]
    p["with_baseline_start_2018"] = p["start_2018"] + out["baseline"]["start_2018"]
    out["types"][t] = p
out["not_counted_obligations"] = sum(1 for r in rows if r["row_id"] not in M)
out["not_counted_laws"] = sorted({by_id[r["row_id"]]["name"] for r in rows if r["row_id"] not in M})
os.makedirs("data/company_types", exist_ok=True)
json.dump(out, open("data/company_types/summary.json", "w"), indent=1, ensure_ascii=False)
with open("data/company_types/matrix.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["row_id", "law", "policy_area"] + [NAMES[k] for k in ["B"] + TYPES])
    for rid in sorted(M, key=lambda k: by_id[k]["name"]):
        cell = lambda k: "" if k not in M[rid] else "all" if M[rid][k] == "F" else ("articles %d-%d" % M[rid][k][0]) if isinstance(M[rid][k], tuple) else "where named"
        w.writerow([rid, by_id[rid]["name"], by_id[rid]["policy_area_ceps"]] + [cell(k) for k in ["B"] + TYPES])
print("baseline", out["baseline"]["obligations"], out["baseline"]["start_2018"])
for t in TYPES:
    p = out["types"][t]
    print(t, p["obligations"], "start2018", p["start_2018"], "rep", p["reporting"], "impl", p["in_implementing_delegated"], "laws", p["laws"], list(p["top_laws"].items())[:4])
print("not counted", out["not_counted_obligations"], out["not_counted_laws"])
