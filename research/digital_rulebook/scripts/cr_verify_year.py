"""Company responses: check that a downloaded report is for the fiscal year it is filed under.

Third-party archives (annualreports.com, financialreports.eu) and the AMF storage
mechanism label files by publication year or by a year read from a title, which can be
one year off. For each report from those sources, the first 15,000 characters are searched
for title phrases with a year ("Annual Report 2019", "Document de référence 2019",
"Geschäftsbericht 2019", "for the year ended 31 December 2019", ...). The most frequent
year is the detected fiscal year. Writes data/company_responses/year_check.csv and, with
--apply, relabels the manifest (keeping the original label in 'year_labelled') when the
detected year differs and that year is not already covered.

  python3 cr_verify_year.py [--manifest FILE] [--apply]
"""
import collections, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cr_code import CACHE, ZW  # noqa: E402

DATA = os.path.join(HERE, "..", "data", "company_responses")
CHECK = ("annualreports.com", "financialreports.eu", "AMF (info-financiere.gouv.fr)")
Y = r"(20[0-2]\d)"
PATS = [rf"(?i)annual (financial )?report\s+{Y}", rf"(?i){Y}\s+annual (financial )?report", rf"(?i)integrated (annual )?report\s+{Y}",
        rf"(?i)annual review\s+{Y}", rf"(?i)registration document\s+{Y}", rf"(?i)document de r[ée]f[ée]rence\s+{Y}",
        rf"(?i)document d['’]enregistrement universel\s+{Y}", rf"(?i)rapport (financier )?annuel\s+{Y}", rf"(?i)gesch[äa]ftsbericht\s+{Y}",
        rf"(?i)jaarverslag\s+{Y}", rf"(?i)(?:relazione|bilancio)[^.]{{0,40}}\s{Y}", rf"(?i)informe anual\s+{Y}",
        rf"(?i)(?:year|exercice|exercise) (?:ended|ending|clos)[^.]{{0,30}}?{Y}", rf"(?i)fiscal (?:year )?{Y}",
        rf"(?i)(?:års|annual and sustainability) ?redovisning\s+{Y}", rf"(?i)annual and sustainability report\s+{Y}"]
PATS = [re.compile(p) for p in PATS]


def detect(text):
    c = collections.Counter()
    for rx in PATS:
        for m in rx.finditer(text):
            c[int([g for g in m.groups() if g and g.isdigit()][-1])] += 1
    return c.most_common(1)[0][0] if c else None, dict(c)


def main():
    args = sys.argv[1:]
    mp = args[args.index("--manifest") + 1] if "--manifest" in args else os.path.join(DATA, "reports_universe.json")
    rows = json.load(open(mp))
    have = {(r["company"], r["year"]) for r in rows if r.get("status") == "ok"}
    out = []
    for r in rows:
        if r.get("status") != "ok" or r.get("source") not in CHECK:
            continue
        text = ZW.sub("", open(os.path.join(CACHE, r["text_file"]), encoding="utf-8", errors="ignore").read()[:15000])
        y, counts = detect(text)
        out.append({"company": r["company"], "year": r["year"], "source": r["source"], "detected": y or "",
                    "counts": json.dumps(counts), "url": r["url"]})
        if "--apply" in args and y and y != r["year"] and (r["company"], y) not in have and 2000 <= y <= 2026:
            have.discard((r["company"], r["year"]))
            r["year_labelled"], r["year"] = r["year"], y
            have.add((r["company"], y))
    with open(os.path.join(DATA, "year_check.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "year", "source", "detected", "counts", "url"])
        w.writeheader()
        w.writerows(out)
    mism = [o for o in out if o["detected"] and o["detected"] != o["year"]]
    print(len(out), "third-party reports checked;", len(mism), "with a different detected year;",
          sum(1 for o in out if not o["detected"]), "undetermined")
    if "--apply" in args:
        rows.sort(key=lambda r: (r["company"], r["year"]))
        json.dump(rows, open(mp, "w"), indent=1)


if __name__ == "__main__":
    main()
