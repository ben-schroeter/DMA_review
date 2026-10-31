"""Which obligations on companies apply to a firm of a given size.

Size bands follow the cut-offs the laws use (Recommendation 2003/361 and the designation thresholds):
  micro (<10 staff), small (10-49), medium (50-249), small mid-cap (250-749), large (750+),
  designated (gatekeepers, very large online platforms and search engines, general-purpose AI with systemic risk).
Every obligation applies to all sizes unless a size rule below lifts it. The rules were coded by reading every
sentence in the adopted laws that sets a size test (data/firm_size/candidates.jsonl, scripts/firm_size_candidates.py).
Only binding exemptions count. Lighter regimes (simplified documentation, lower fines, less frequent updates) and
options left to Member States are listed in LIGHTER/OPTIONAL but do not change the counts. Sector-specific size tests
that do not use the SME definition (DORA Art. 16 small and non-interconnected investment firms, bank significance)
are not modelled.
Writes data/firm_size/summary.json. Run from research/ceps_metrics."""
import collections, json, os, re

exec(open("scripts/company_types.py").read().split('out = {"names"')[0])   # rows, M, TYPES, NAMES, applies(), by_id, sec

BANDS = ["micro", "small", "medium", "small_midcap", "large", "designated"]
LABEL = {"micro": "Micro (under 10 staff)", "small": "Small (10-49)", "medium": "Medium (50-249)",
         "small_midcap": "Small mid-cap (250-749)", "large": "Large (750+)", "designated": "Designated very large firms"}
MICRO, SMALL, MEDIUM, SMC, LARGE, DESIG = range(6)


def art(r):
    m = re.match(r"Art\.\s*(\d+)", r.get("article") or "")
    return int(m.group(1)) if m else None


def text(r):
    return " ".join([r.get("chapeau") or "", r["clause"]]).lower()


def sec_title(r):
    return (sec[r["doc"]]["title"] or "").lower() if r["kind"] == "secondary" else ""


# (row_id, test, smallest band the obligation applies to, source provision)
RULES = [
    (59, lambda r: True, DESIG, "DMA: obligations bind designated gatekeepers only (Art. 3)"),
    (60, lambda r: r["kind"] == "main" and art(r) is not None and 33 <= art(r) <= 43, DESIG, "DSA Arts. 33-43: very large online platforms and search engines"),
    (60, lambda r: r["kind"] == "secondary" and re.search(r"very large online|audits?\b", sec_title(r)), DESIG, "DSA implementing and delegated acts for very large platforms (audits, VLOP reporting)"),
    (60, lambda r: r["kind"] == "main" and art(r) == 15, MEDIUM, "DSA Art. 15(2): micro and small intermediaries exempt from transparency reports"),
    (60, lambda r: r["kind"] == "main" and art(r) is not None and 20 <= art(r) <= 28 and not (art(r) == 24 and "monthly active" in text(r)),
     MEDIUM, "DSA Art. 19: Section 3 (Arts. 20-28, except Art. 24(3)) does not apply to micro and small platforms"),
    (60, lambda r: r["kind"] == "main" and art(r) is not None and 30 <= art(r) <= 32, MEDIUM, "DSA Art. 29: Section 4 (marketplaces, Arts. 30-32) does not apply to micro and small platforms"),
    (64, lambda r: r["kind"] == "main" and art(r) == 55, DESIG, "AI Act Art. 55: general-purpose AI models with systemic risk"),
    (57, lambda r: "other than microenterprises" in text(r) or "other than microenterprise" in text(r), SMALL, "DORA: obligations addressed to financial entities 'other than microenterprises'"),
    (44, lambda r: r["kind"] == "main" and art(r) in (11, 12), MEDIUM, "P2B Arts. 11(5) and 12(7): small enterprises exempt from complaint handling and mediation"),
    (61, lambda r: True, MEDIUM, "NIS2 Art. 2(1): applies to medium-sized and larger entities (telecoms providers regardless of size, see TYPE_OVERRIDE)"),
    (76, lambda r: r["kind"] == "main" and art(r) is not None and 3 <= art(r) <= 6, MEDIUM, "Data Act Art. 7(1): Chapter II does not apply to micro and small manufacturers"),
    (76, lambda r: r["kind"] == "main" and art(r) == 20 and "free of charge" in text(r), MEDIUM, "Data Act Art. 20(1): only data holders other than micro and small enterprises must provide data free of charge"),
    (80, lambda r: r["kind"] == "main" and art(r) in (24, 25), MEDIUM, "Ecodesign Arts. 24-25: unsold-products disclosure and destruction ban do not apply to micro and small enterprises (medium from 2030)"),
    (81, lambda r: r["kind"] == "main" and art(r) is not None and 50 <= art(r) <= 81 and "health data holder" in text(r), SMALL, "EHDS Art. 50: health data holder duties do not apply to microenterprises"),
    (92, lambda r: "large compan" in text(r), LARGE, "CRMA Art. 24: risk preparedness duties for large companies (over 500 staff and EUR 150 million)"),
]
TYPE_OVERRIDE = {("TC", 61): MICRO}   # NIS2 Art. 2(2)(a): public electronic communications providers regardless of size
LIGHTER = ["GDPR Art. 30(5): record-keeping exemption under 250 staff, but not where processing is risky, not occasional or involves special data (in practice rarely usable)",
           "AI Act Art. 63: microenterprises may use a simplified quality management system; Art. 99(6) lower fines for SMEs",
           "Cyber Resilience Act Art. 33(5): simplified technical documentation for micro and small; Art. 64(10): no fines on micro and small for missing the 24-hour early warning",
           "Copyright DSM Art. 17(6): lighter liability conditions for content-sharing services under three years old and under EUR 10 million turnover",
           "Platform Work Directive Art. 17: SMEs may update information yearly", "Short-Term Rental Data Regulation Art. 9: small platforms with few listings report quarterly",
           "DORA Arts. 6(5), 12(4), 25(3), 30: lighter versions for microenterprises", "Chips Act, IMERA, compulsory licensing: lower fines for SMEs"]
OPTIONAL = ["EECC Art. 17: Member States may exempt undertakings under EUR 50 million from accounting separation",
            "EECC Art. 98: Title III end-user rules do not apply to micro providers of number-independent communications (not modelled: type-specific)",
            "VAT Directive Arts. 282-292: optional small-enterprise scheme for very small turnover", "AML Regulation Art. 5: Member States may exempt small football clubs"]


def min_band(r, t=None):
    rid = r["row_id"]
    if t and (t, rid) in TYPE_OVERRIDE:
        return TYPE_OVERRIDE[(t, rid)], None
    for rr, test, band, src in RULES:
        if rr == rid and test(r):
            return band, src
    return MICRO, None


def staircase(sel, t=None):
    mb = [min_band(r, t)[0] for r in sel]
    return [sum(1 for b in mb if b <= i) for i in range(len(BANDS))]


base = [r for r in rows if M.get(r["row_id"], {}).get("B") == "F"]
out = {"bands": BANDS, "labels": LABEL, "baseline": staircase(base), "types": {}, "by_rule": {}, "lighter": LIGHTER, "optional": OPTIONAL}
allc = [r for r in rows if r["row_id"] in M]
for t in TYPES:
    sel = [r for r in rows if t in M.get(r["row_id"], {}) and applies(M[r["row_id"]][t], r, t)]
    out["types"][t] = {"name": NAMES[t], "specific": staircase(sel, t)}
# all company obligations in the laws coded for company types (each obligation once)
out["all_company_obligations"] = staircase(allc)
for r in allc:
    b, src = min_band(r)
    if src:
        out["by_rule"].setdefault(src, {"obligations": 0, "band": BANDS[b]})["obligations"] += 1
os.makedirs("data/firm_size", exist_ok=True)
json.dump(out, open("data/firm_size/summary.json", "w"), indent=1, ensure_ascii=False)
print("bands", BANDS)
print("baseline", out["baseline"])
for t, v in out["types"].items():
    print(t, v["specific"], "with baseline", [a + b for a, b in zip(v["specific"], out["baseline"])])
print("all", out["all_company_obligations"])
for k, v in sorted(out["by_rule"].items(), key=lambda x: -x[1]["obligations"]):
    print(f'{v["obligations"]:5d} {v["band"]:12s} {k}')
