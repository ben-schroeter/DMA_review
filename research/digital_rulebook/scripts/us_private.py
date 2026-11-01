"""EU vs US matched pairs, counting only obligations that address private companies.
US instances (data/us_map/instances_<id>_all_text.json) were classified with the EU lexicon adapted for a few US actor terms,
which leaves many 'unclear'. Here the unclear ones are re-read with US-specific subject rules (government actors: courts,
agencies, Commission, Secretary, Director, funds and appropriations; private actors: business, manufacturer, distributor,
retailer, importer, provider, covered entity, person, carrier, recipient, applicant). The rules were only a first pass: every unclear obligation was then read by hand (PRIVATE_UNCLEAR).
EU counts come from the workbook (formal addressee, as on the Quantification page).
Writes data/us_map/us_private.json. Run from research/digital_rulebook."""
import json, re
import openpyxl

GOV = re.compile(r"\b(court|judge|clerk|agency|agencies|commission(er)?s?|secretary|director|administrator|attorney general|comptroller|inspector general|"
                 r"office of|chief (data|information|privacy)|head of|federal|government|congress|president|state|fund|amounts?|appropriat|"
                 r"board|council|department|united states)\b", re.I)
PRIV = re.compile(r"\b(business(es)?|manufacturers?|distributors?|retailers?|importers?|private labelers?|providers?|covered entit(y|ies)|"
                  r"service providers?|contractors?|third part(y|ies)|persons?|carriers?|recipients?|applicants?|employers?|operators?|sellers?|"
                  r"owners?|licensees?|companies|company|firms?|entity|entities)\b", re.I)
HEAD = re.compile(r"^[A-Z][A-Za-z ,'-]{0,60}\.?$")       # bare section headings counted by the marker (e.g. "Prohibited acts.")


def subject(clause, marker):
    k = clause.lower().find(marker.lower())
    pre = clause[max(0, k - 160):k] if k >= 0 else clause[:160]
    if HEAD.match(clause.strip()):
        return "heading"
    g = [m.end() for m in GOV.finditer(pre)]; p = [m.end() for m in PRIV.finditer(pre)]
    if g or p:
        return "government" if (g[-1] if g else -1) > (p[-1] if p else -1) else "private"
    return "unclear"


# Obligations first classified 'unclear' that address private companies, read one by one (indices into the instance files).
# Everything else that was unclear was read as government, courts, procedure, appropriations or not an obligation at all.
PRIVATE_UNCLEAR = {"cpsia": {30, 32, 34, 35, 49, 50, 51, 52, 53, 75, 77, 79, 214, 231, 241},
                   "ccpa": {39, 44, 46, 59, 71, 74, 78}, "cpsa": {87, 88, 89, 96, 118, 147},
                   "chips": {46, 75}, "cloud": {2}, "colorado_ai": {11, 14, 15, 20, 28}}
pairs = [p for p in json.load(open("data/us_map/us_comparison.json")) if p.get("included")]
# Same-job state comparator for the AI Act, measured by scripts/benchmark_colorado.py (kept out of us_comparison.json, which lists federal matches)
pairs.append({"row_id": 64, "eu_instrument": "Artificial Intelligence Act", "us_counterpart": "Colorado AI Act (SB 24-205, 2024)", "us_ids": ["colorado_ai"]})
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
inst = {r[h.index("row_id")]: dict(zip(h, r)) for r in rows[1:] if r[0]}
out = []
for p in pairs:
    e = inst[p["row_id"]]
    eu_tot, eu_priv, eu_unc = e["restrictions_total"], e["addr_private_parties"] or 0, e.get("addr_unclear") or 0
    us_priv = us_unc = us_tot = 0
    for i in p["us_ids"]:
        for n, x in enumerate(json.load(open(f"data/us_map/instances_{i}_all_text.json"))):
            us_tot += 1
            if x["addressee"] == "private_parties":
                us_priv += 1
            elif x["addressee"] == "unclear":
                us_unc += 1
                us_priv += n in PRIVATE_UNCLEAR.get(i, set())
    out.append({"row_id": p["row_id"], "eu": p["eu_instrument"], "us": p["us_counterpart"], "eu_total": eu_tot, "us_total": us_tot,
                "eu_private": eu_priv, "eu_private_max": eu_priv + eu_unc, "us_private": us_priv, "us_unclear_read": us_unc})
json.dump(out, open("data/us_map/us_private.json", "w"), indent=1)
import statistics
for o in out:
    r = o["eu_private"] / o["us_private"] if o["us_private"] else float("inf")
    print(f'{o["eu"][:34]:34s} {o["us"][:28]:28s} all {o["eu_total"]:4d}/{o["us_total"]:4d}  private EU {o["eu_private"]:4d} (≤{o["eu_private_max"]})  US {o["us_private"]:4d}  ratio {r:.1f}')
fin = [o["eu_private"] / o["us_private"] for o in out if o["us_private"]]
print("median ratio", round(statistics.median(fin), 2), "| sums EU", sum(o["eu_private"] for o in out), "US", sum(o["us_private"] for o in out))
