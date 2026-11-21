"""Company responses, frequency study: build the company universe and check report coverage.

Universe = Fortune 100 (2026 list) + current constituents of DAX, CAC 40, FTSE 100 and
EURO STOXX 50, restricted to companies headquartered in the EU-27, the UK or the US
(headquarters country from GLEIF; Fortune 500 companies are all US) that belong to at
least one of the six company types (universe/company_types.json, 'include' or 'borderline').

For each company it checks, for report years 2000-2026:
  - SEC EDGAR: original 10-K / 20-F / 40-F filings for the CIKs in identifiers.json;
  - filings.xbrl.org: ESEF annual financial reports for the company's LEI.
Writes data/company_responses/universe/universe.json (companies with their sources,
for cr_fetch.py) and coverage.csv (one row per company: years covered and gaps).
"""
import csv, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("CR_FROM", "2000")
from cr_fetch import sec_filings_for, get, SEC_UA, YEARS  # noqa: E402

U = os.path.join(HERE, "..", "data", "company_responses", "universe")
EU27 = set("AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split())
INDEX_DEFAULT_HQ = {"DAX": "DE", "CAC 40": "FR", "FTSE 100": "GB"}
CACHE = os.path.join(os.environ.get("RULEBOOK_CACHE", os.path.expanduser("~/.cache/digital_rulebook")), "universe")


def jget(url, sleep=0.0):
    """JSON GET with an on-disk cache and backoff on HTTP 429."""
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, re.sub(r"[^A-Za-z0-9]+", "_", url)[-180:] + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    for k in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                d = None
                break
            if e.code == 429 and k < 5:
                time.sleep(10 * (k + 1))
                continue
            raise
    json.dump(d, open(path, "w"))
    time.sleep(sleep)
    return d


def gleif_hq(lei):
    d = jget(f"https://api.gleif.org/api/v1/lei-records/{lei}")
    if not d:
        return None, None
    a = d["data"]["attributes"]["entity"]
    return a["headquartersAddress"]["country"], a["legalName"]["name"]


def esef_filings(lei):
    d = jget(f"https://filings.xbrl.org/api/entities/{lei}/filings", sleep=1.5)
    out = {}
    for f in (d or {}).get("data", []):
        a = f["attributes"]
        if not a.get("report_url"):
            continue
        y = int(a["period_end"][:4])
        url = "https://filings.xbrl.org" + a["report_url"]
        lang = re.search(r"-(en|fr|de|it|es|nl|fi|pt|el|sv|da|pl)[-./_]", a["report_url"], re.I)
        lang = lang.group(1).lower() if lang else ""
        rank = 0 if lang == "en" else 1 if lang == "" else 2       # prefer English versions
        if y not in out or rank < out[y]["_rank"]:
            out[y] = {"url": url, "period_end": a["period_end"], "country": a["country"], "language": lang, "_rank": rank}
    for v in out.values():
        v.pop("_rank")
    return out


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main():
    f100 = json.load(open(os.path.join(U, "fortune100_2026.json")))["companies"]
    eu = json.load(open(os.path.join(U, "eu_indices_2026-11.json")))["constituents"]
    ids = json.load(open(os.path.join(U, "identifiers.json")))["companies"]
    types = json.load(open(os.path.join(U, "company_types.json")))["types"]
    comps = {}
    for c in f100:
        comps[c["name"]] = {"name": c["name"], "groups": [f"Fortune 100 (#{c['rank']})"], "hq_default": "US"}
    ap = os.path.join(U, "additions.json")
    for c in (json.load(open(ap))["companies"] if os.path.exists(ap) else []):
        comps[c["name"]] = {"name": c["name"], "groups": c["groups"], "hq_default": c["hq"]}
    for c in eu:
        n = ids.get(c["name"], {}).get("same_as", c["name"])
        e = comps.setdefault(n, {"name": n, "groups": [], "hq_default": INDEX_DEFAULT_HQ.get(c["index"], "")})
        if c["index"] not in e["groups"]:
            e["groups"].append(c["index"])
    universe, cov = [], []
    for n, c in comps.items():
        i = ids.get(n, {})
        row = {"id": slug(n), "name": n, "groups": c["groups"], "sec_ciks": i.get("sec_ciks", []), "lei": i.get("lei")}
        hq, legal = (gleif_hq(row["lei"]) if row["lei"] else (None, None))
        row["hq"] = "US" if c["hq_default"] == "US" else (hq or c["hq_default"])
        row["legal_name"] = legal
        t = types.get(n)
        row["company_types"] = t["types"] if t else ""
        row["type_status"] = t["status"] if t else ""
        if i.get("exclude"):
            row["exclude"] = i["exclude"]
        elif not t:
            row["exclude"] = "fits none of the six company types"
        elif t["status"] not in ("include", "proposed"):
            row["exclude"] = t["why"]
        elif row["hq"] not in EU27 | {"GB", "US"}:
            row["exclude"] = f"headquarters outside EU-27/UK/US ({row['hq']})"
        if i.get("note"):
            row["note"] = i["note"]
        sec_years, esef = {}, {}
        if not row.get("exclude"):
            for fl in sorted(sec_filings_for(row["sec_ciks"]), key=lambda f: f["filed"]):
                y = int(fl["period_end"][:4])
                if y in YEARS and y not in sec_years:
                    sec_years[y] = fl["form"]
            if row["lei"] and row["hq"] != "US":
                esef = esef_filings(row["lei"])
        row["esef_reports"] = {str(y): v for y, v in sorted(esef.items()) if y in YEARS}
        universe.append(row)
        manual_years = {int(y) for y in json.load(open(os.path.join(U, "manual_reports.json"))).get(row["id"], {})} \
            if os.path.exists(os.path.join(U, "manual_reports.json")) and not row.get("exclude") else set()
        covered = sorted(set(sec_years) | {y for y in esef if y in YEARS} | manual_years)
        cov.append({"company": n, "groups": "; ".join(c["groups"]), "hq": row["hq"], "types": row["company_types"],
                    "type_status": row["type_status"], "excluded": row.get("exclude", ""),
                    "sec_years": len(sec_years), "sec_forms": "/".join(sorted(set(sec_years.values()))),
                    "esef_years": len([y for y in esef if y in YEARS]), "manual_years": len(manual_years),
                    "years_covered": len(covered), "first": covered[0] if covered else "", "last": covered[-1] if covered else "",
                    "missing_2000_2025": " ".join(str(y) for y in range(2000, 2026) if y not in covered)})
        print(n, row["hq"], row.get("exclude", ""), len(sec_years), len(esef), flush=True)
    manual = {}
    mp = os.path.join(U, "manual_reports.json")
    if os.path.exists(mp):
        manual = {k: v for k, v in json.load(open(mp)).items() if not k.startswith("_")}
    json.dump({"_note": "Built by scripts/cr_universe.py; see METHOD.md (frequency study).", "companies": universe,
               "web_reports": manual},
              open(os.path.join(U, "universe.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(U, "coverage.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cov[0].keys()))
        w.writeheader()
        w.writerows(cov)


if __name__ == "__main__":
    main()
