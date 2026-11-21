"""Write data/company_responses/universe/company_list.md (companies by main type, with report coverage) from coverage.csv."""
import csv, json, os

U = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "company_responses", "universe")
NAMES = {"GK": "Gatekeepers and very large platforms", "PL": "Online platforms and digital services", "CL": "Cloud, data and AI",
         "TC": "Telecoms", "FI": "Finance, payments and crypto", "PR": "Makers of connected products"}


def region(h):
    return "US" if h == "US" else "UK" if h == "GB" else "EU"


rows = [r for r in csv.DictReader(open(os.path.join(U, "coverage.csv"), encoding="utf-8")) if not r["excluded"]]
L = ["# Companies in the frequency study (by company type)", "",
     "Fortune 100 (2026) and DAX, CAC 40, FTSE 100 and EURO STOXX 50 constituents headquartered in the EU-27, UK or US in one of "
     "the six company types, plus additions, after the project lead's decisions (company_types.json). Each company is listed under "
     "its main type (other types in 'Also'). **Reports** = first and last report year found (2000-2025); **n** = years with a report; "
     "**Gaps** = missing years after the first. Sources: SEC 10-K/20-F, ESEF (filings.xbrl.org), company IR sites (incl. EQS-hosted "
     "files), the AMF storage mechanism (info-financiere.gouv.fr), annualreports.com.", "", f"**{len(rows)} companies.**", ""]
for t in NAMES:
    sub = sorted([r for r in rows if r["types"].split(";")[0] == t], key=lambda r: ({"US": 0, "EU": 1, "UK": 2}[region(r["hq"])], r["company"]))
    L += [f"## {NAMES[t]} ({len(sub)})", "", "| Company | Region | Also | Reports | n | Gaps | Sources |", "|---|---|---|---|---|---|---|"]
    for r in sub:
        miss = [int(x) for x in r["missing_2000_2025"].split()]
        first = int(r["first"]) if r["first"] else None
        gaps = [y for y in miss if first and y > first]
        src = [s for s, k in (("SEC", "sec_years"), ("ESEF", "esef_years"), ("IR site / archives", "manual_years")) if int(r[k])]
        last = min(int(r["last"]), 2025) if r["last"] else ""
        n = len([y for y in range(2000, 2026) if y not in miss])
        L.append(f"| {r['company']} | {region(r['hq'])} ({r['hq']}) | {', '.join(r['types'].split(';')[1:]) or '–'} | "
                 f"{r['first'] or '–'}–{last} | {n} | {' '.join(map(str, gaps)) or '–'} | {', '.join(src) or 'none yet'} |")
    L.append("")
open(os.path.join(U, "company_list.md"), "w", encoding="utf-8").write("\n".join(L))
print(len(rows))
