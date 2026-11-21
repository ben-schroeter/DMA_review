"""Company responses, step 3: draw the validation samples and score the hand checks.

  python3 cr_validate.py draw    -> data/company_responses/validation_sample.csv (passages, precision)
                                    data/company_responses/validation_misses.csv (recall probe)
  python3 cr_validate.py score   -> data/company_responses/validation_results.json

Precision sample: up to 25 passages per EU law, stratified by company region (US/EU/UK)
and drawn with a fixed seed. Each row gets hand-check columns:
  h_is_law      1 if the passage really refers to the EU law (0 = false match or a UK/other law)
  h_categories  the categories a reader would assign (semicolon-separated)
  h_boilerplate 1 if generic text that names the law without saying anything specific to the company
  h_amount_ok   1 if the coded amount is a law-related amount, 0 if wrong, blank if no amount
Recall probe: report-years after the law's adoption with no coded mention, searched for
looser wording (e.g. 'gatekeeper', 'EU privacy regulation') to find mentions the patterns missed.
"""
import csv, json, os, random, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "company_responses")
CACHE = os.path.join(os.environ.get("RULEBOOK_CACHE", os.path.expanduser("~/.cache/digital_rulebook")), "company_reports")
REGION = {c["id"]: ("EU" if c["hq"] in ("FR", "DE") else c["hq"])
          for c in json.load(open(os.path.join(DATA, "companies.json")))["companies"]}
ADOPTED = {"GDPR": 2016, "DMA": 2022, "AI_ACT": 2024}
LOOSE = {
    "GDPR": r"(?i)(EU|European|Union)['’]?s? (new |general )?(data protection|privacy) (regulation|law|rules)|data protection regulation",
    "DMA": r"(?i)\bgatekeepers?\b|EU digital markets (regulation|law|rules)|ex ante (regulation|rules) (for|of) (digital|online) platforms",
    "AI_ACT": r"(?i)(EU|European|Union)['’]?s? (proposed |new )?(regulation|law|rules|framework) (on|for|governing) (artificial intelligence|AI)\b|AI regulation in the (EU|European Union)",
}
H_COLS = ["h_is_law", "h_categories", "h_boilerplate", "h_amount_ok", "h_note"]


def draw():
    rows = list(csv.DictReader(open(os.path.join(DATA, "mentions.csv"), encoding="utf-8")))
    rnd = random.Random(20261121)
    sample = []
    for law in ADOPTED:
        by_region = defaultdict(list)
        for r in rows:
            if r["law"] == law:
                by_region[REGION[r["company"]]].append(r)
        quota = 25
        regions = [g for g in ("US", "EU", "UK") if by_region[g]]
        for i, g in enumerate(regions):
            k = min(len(by_region[g]), (quota - sum(1 for s in sample if s["law"] == law)) // (len(regions) - i))
            sample += rnd.sample(by_region[g], k)
    keep = ["company", "year", "law", "matched", "categories", "amounts", "boilerplate", "repeated", "list_only",
            "quote", "link", "passage"]
    with open(os.path.join(DATA, "validation_sample.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["sample_id"] + keep + H_COLS, extrasaction="ignore")
        w.writeheader()
        for i, r in enumerate(sample, 1):
            w.writerow(dict(r, sample_id=i))
    # recall probe
    panel = list(csv.DictReader(open(os.path.join(DATA, "company_year.csv"), encoding="utf-8")))
    reports = {(r["company"], r["year"]): r for r in json.load(open(os.path.join(DATA, "reports.json")))}
    misses = []
    for p in panel:
        if p["mentioned"] != "0" or int(p["year"]) < ADOPTED[p["law"]]:
            continue
        rep = reports[(p["company"], int(p["year"]))]
        text = open(os.path.join(CACHE, rep["text_file"]), encoding="utf-8").read()
        hits = [m for m in re.finditer(LOOSE[p["law"]], text)]
        q = ""
        if hits:
            m = hits[0]
            q = re.sub(r"\s+", " ", text[max(0, m.start() - 200):m.end() + 200])
        misses.append({"company": p["company"], "year": p["year"], "law": p["law"], "loose_hits": len(hits),
                       "first_hit_context": q, "h_missed_mention": "", "h_note": ""})
    with open(os.path.join(DATA, "validation_misses.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(misses[0].keys()) if misses else ["company"])
        w.writeheader()
        w.writerows(misses)
    print(len(sample), "passages sampled;", len(misses), "no-mention report-years probed",
          sum(1 for m in misses if m["loose_hits"]), "with loose hits")


def score():
    rows = list(csv.DictReader(open(os.path.join(DATA, "validation_sample.csv"), encoding="utf-8")))
    done = [r for r in rows if r["h_is_law"] != ""]
    res = {"n_sampled": len(rows), "n_checked": len(done)}
    if not done:
        return print("no hand checks yet")
    res["precision_law"] = round(sum(r["h_is_law"] == "1" for r in done) / len(done), 3)
    true = [r for r in done if r["h_is_law"] == "1"]
    cats = ["risk_factor", "compliance_cost", "fine_or_provision", "product_change", "revenue_impact",
            "legal_proceedings", "opportunity"]
    per = {}
    for c in cats:
        tp = sum(c in r["categories"].split(";") and c in r["h_categories"].split(";") for r in true)
        fp = sum(c in r["categories"].split(";") and c not in r["h_categories"].split(";") for r in true)
        fn = sum(c not in r["categories"].split(";") and c in r["h_categories"].split(";") for r in true)
        per[c] = {"tp": tp, "fp": fp, "fn": fn,
                  "precision": round(tp / (tp + fp), 2) if tp + fp else None,
                  "recall": round(tp / (tp + fn), 2) if tp + fn else None}
    res["categories"] = per
    bp = [(r["boilerplate"] == "True", r["h_boilerplate"] == "1") for r in true if r["h_boilerplate"] != ""]
    res["boilerplate_agreement"] = round(sum(a == b for a, b in bp) / len(bp), 3) if bp else None
    res["boilerplate_coded_vs_hand"] = {"both": sum(a and b for a, b in bp), "coded_only": sum(a and not b for a, b in bp),
                                        "hand_only": sum(b and not a for a, b in bp), "neither": sum(not a and not b for a, b in bp)}
    am = [r["h_amount_ok"] for r in true if r["amounts"] and r["h_amount_ok"] != ""]
    res["amounts_checked"] = len(am)
    res["amounts_law_related_share"] = round(sum(a == "1" for a in am) / len(am), 3) if am else None
    by_law = defaultdict(list)
    for r in done:
        by_law[r["law"]].append(r["h_is_law"] == "1")
    res["precision_by_law"] = {k: round(sum(v) / len(v), 3) for k, v in by_law.items()}
    mp = os.path.join(DATA, "validation_misses.csv")
    if os.path.exists(mp):
        ms = [m for m in csv.DictReader(open(mp, encoding="utf-8")) if m.get("h_missed_mention", "") != ""]
        res["recall_probe"] = {"report_years_checked": len(ms), "missed_mentions_found": sum(m["h_missed_mention"] == "1" for m in ms)}
    json.dump(res, open(os.path.join(DATA, "validation_results.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    {"draw": draw, "score": score}[sys.argv[1]]()
