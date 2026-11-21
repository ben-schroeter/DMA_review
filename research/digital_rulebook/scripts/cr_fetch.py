"""Company responses, step 1: find and download one annual report per company-year.

Reads data/company_responses/companies.json. For each company and each report
year (calendar year of the fiscal period end, 2016-2026):
  1. SEC EDGAR 10-K (US) or 20-F (foreign private issuers), original filings only;
  2. otherwise the ESEF report from filings.xbrl.org listed in companies.json;
  3. otherwise the PDF from the company's investor site listed in companies.json.
Each report is converted to plain text with page breaks (\f) kept for PDFs and
cached under ~/.cache/digital_rulebook/company_reports/. Writes the manifest
data/company_responses/reports.json, including the years with no report found.

SEC asks automated clients to identify themselves; the User-Agent below carries
the project contact address approved for this purpose.
"""
import datetime as dt, hashlib, json, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "company_responses")
CACHE = os.path.join(os.environ.get("RULEBOOK_CACHE", os.path.expanduser("~/.cache/digital_rulebook")), "company_reports")
SEC_UA = "EU Digital Rulebook admin@ben-schroeter.de"
WEB_UA = "Mozilla/5.0 (compatible; EU Digital Rulebook research)"
YEARS = range(int(os.environ.get("CR_FROM", "2016")), 2027)   # CR_FROM=2000 for the frequency study


def get(url, ua, binary=True, sleep=0.4, retries=6):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, "raw_" + hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(path):
        data = open(path, "rb").read()
    else:
        for i in range(retries):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    data = r.read()
                break
            except Exception as e:
                if i == retries - 1 or getattr(e, "code", None) in (403, 404):
                    raise
                # filings.xbrl.org answers 429 when polled quickly
                time.sleep(15 * (i + 1) if getattr(e, "code", None) == 429 else 2 ** (i + 1))
        open(path, "wb").write(data)
        time.sleep(sleep)
    return data if binary else data.decode("utf-8", "replace")


def sec_json(url):
    return json.loads(get(url, SEC_UA, binary=False))


# ---------- text extraction ----------
ZW = re.compile("[\u200b\u200c\u200d\u2060\ufeff\u00ad]")
BLOCK = re.compile(r"(?i)</?(p|div|br|tr|li|h[1-6]|table|section|td)\b[^>]*>")


def html_to_text(raw):
    """Tag-stripping extraction that keeps block boundaries as blank lines."""
    import html as _html
    t = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
    t = re.sub(r"(?ms)^begin \d{3} \S+$.*?^end$", " ", t)          # uuencoded files in .txt submissions
    t = re.sub(r"(?is)<(script|style|ix:header)\b.*?</\1>", " ", t)
    t = BLOCK.sub("\n\n", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = _html.unescape(t).replace("\xa0", " ")
    t = ZW.sub("", t)
    t = re.sub(r"[ \t\r]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def pdf_to_text(raw):
    tmp = os.path.join(CACHE, "_tmp.pdf")
    open(tmp, "wb").write(raw)
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", tmp, "-"], capture_output=True).stdout.decode("utf-8", "replace")
    os.remove(tmp)
    return out


def to_text(url, ua, kind):
    tpath = os.path.join(CACHE, "txt_" + hashlib.sha1(url.encode()).hexdigest() + ".txt")
    if os.path.exists(tpath):
        return open(tpath, encoding="utf-8").read()
    raw = get(url, ua)
    text = pdf_to_text(raw) if kind == "pdf" or raw[:4] == b"%PDF" else html_to_text(raw)
    open(tpath, "w", encoding="utf-8").write(text)
    # raw copies of large documents are not needed once the text exists
    if len(raw) > 1_000_000:
        os.remove(os.path.join(CACHE, "raw_" + hashlib.sha1(url.encode()).hexdigest()))
    return text


# ---------- SEC ----------
def sec_annual_filings(cik):
    d = sec_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    blocks = [d["filings"]["recent"]] + [sec_json("https://data.sec.gov/submissions/" + f["name"]) for f in d["filings"]["files"]]
    out = []
    for r in blocks:
        for i, form in enumerate(r["form"]):
            if form not in ("10-K", "10-K405", "20-F"):
                continue
            filed = r["filingDate"][i]
            period = r["reportDate"][i] or filed
            # Some 20-F records carry a date near the filing date instead of the
            # fiscal period end; foreign issuers here all have Dec/Mar year ends.
            gap = (dt.date.fromisoformat(filed) - dt.date.fromisoformat(period)).days
            if gap < 20:
                period = f"{int(filed[:4]) - 1}-12-31"
            acc = r["accessionNumber"][i]
            doc = r["primaryDocument"][i] or f"{acc}.txt"   # older filings: complete submission text file
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{doc}"
            out.append({"form": form, "filed": filed, "period_end": period, "accession": acc, "url": url})
    return out


def sec_filings_for(ciks):
    """Annual filings for a list of CIKs; an entry may be {"cik": n, "from": y, "to": y} to use a
    predecessor registrant only for some report years (e.g. old General Motors until 2008)."""
    out = []
    for c in ciks:
        c = c if isinstance(c, dict) else {"cik": c}
        for f in sec_annual_filings(c["cik"]):
            y = int(f["period_end"][:4])
            if c.get("from", 0) <= y <= c.get("to", 9999):
                out.append(f)
    return out


def sec_exhibits(url, form="20-F"):
    """Annual-report exhibits: for a 20-F, EX-15 / EX-99 (Orange files its Registration Document
    as Exhibit 15.1, Vodafone its annual report as Exhibit 99.1); for a 10-K, EX-13 (annual report
    to shareholders incorporated by reference, e.g. Wells Fargo). In a 20-F, Exhibit 13 is a certification."""
    base = url.rsplit("/", 1)[0]
    idx = get(base + "/", SEC_UA, binary=False)
    out = []
    for m in re.finditer(r'href="(/Archives/edgar/data/[^"]+\.htm)"', idx):
        name = m.group(1).rsplit("/", 1)[1].lower()
        if name == url.rsplit("/", 1)[1].lower():
            continue
        pat = (r"ex-?13|ex13|exh?_?13|exhibit_?13|dex13|annualreport" if form.startswith("10-K") else
               r"ex-?15|ex15|ex-?99|ex99|exh?_?15|exhibit_?15|exhibit_?99|registration|annualreport|dex151|dex991")
        if re.search(pat, name):
            out.append("https://www.sec.gov" + m.group(1))
    return out


def main():
    """python3 cr_fetch.py [--config FILE] [--manifest FILE] [company ids ...]
    Defaults: the pilot (data/company_responses/companies.json -> reports.json)."""
    args = sys.argv[1:]
    opt = {}
    for k in ("--config", "--manifest"):
        if k in args:
            i = args.index(k)
            opt[k] = args[i + 1]
            del args[i:i + 2]
    cfg = json.load(open(opt.get("--config", os.path.join(DATA, "companies.json"))))
    only = set(args)
    manifest_path = opt.get("--manifest", os.path.join(DATA, "reports.json"))
    old = {(r["company"], r["year"]): r for r in json.load(open(manifest_path))} if os.path.exists(manifest_path) else {}
    rows = []
    for c in cfg["companies"]:
        cid = c["id"]
        if c.get("exclude"):
            continue
        if only and cid not in only:
            rows += [r for k, r in old.items() if k[0] == cid]
            continue
        found = {}
        ciks = c.get("sec_ciks") or ([c["sec_cik"]] if c.get("sec_cik") else [])
        filings = sec_filings_for(ciks)
        for f in sorted(filings, key=lambda f: f["filed"]):
            y = int(f["period_end"][:4])
            if y in YEARS and y not in found:   # first original filing for the period
                found[y] = dict(f, source="SEC EDGAR", kind="html")
        esef = c.get("esef_reports") or {y: {"url": u} for y, u in cfg.get("esef_reports", {}).get(cid, {}).items()}
        for y, e in esef.items():
            if y.startswith("_") or int(y) in found:
                continue
            lang = e.get("language") or ("fr" if "-fr" in e["url"] else "")
            found[int(y)] = {"form": "ESEF annual financial report", "period_end": e.get("period_end", f"{y}-12-31"),
                             "url": e["url"], "source": "filings.xbrl.org", "kind": "html", "language": lang}
        for y, w in cfg.get("web_reports", {}).get(cid, {}).items():
            if y.startswith("_") or int(y) in found:
                continue
            w = w if isinstance(w, dict) else {"url": w, "source": "company website"}
            found[int(y)] = {"form": "Annual report (" + w["source"] + ")", "period_end": f"{y}-12-31", "url": w["url"],
                             "source": w["source"], "kind": "pdf"}
        for y in YEARS:
            r = {"company": cid, "year": y}
            if y not in found:
                r["status"] = "not found"
                rows.append(r)
                continue
            r.update(found[y])
            try:
                ua = SEC_UA if r["source"] == "SEC EDGAR" else WEB_UA
                try:
                    text = to_text(r["url"], ua, r["kind"])
                except Exception as e:
                    # early-2000s EDGAR records name documents that are not on the server:
                    # fall back to the complete submission text file
                    if r["source"] != "SEC EDGAR" or getattr(e, "code", None) != 404:
                        raise
                    r["url"] = r["url"].rsplit("/", 1)[0] + "/" + r["accession"] + ".txt"
                    text = to_text(r["url"], ua, r["kind"])
                if r.get("form") in ("20-F", "10-K", "10-K405") and not r["url"].endswith(".txt"):
                    ex = sec_exhibits(r["url"], r["form"])   # annual report may be an exhibit
                    parts = [(u, to_text(u, ua, "html")) for u in ex]
                    parts = [(u, t) for u, t in parts if len(t) > 100_000]
                    if parts:
                        r["exhibits"] = [u for u, _ in parts]
                        text = text + "\n\n" + "\n\n".join(t for _, t in parts)
                        r["text_file"] = "txt_" + hashlib.sha1(r["url"].encode()).hexdigest() + "_full.txt"
                        open(os.path.join(CACHE, r["text_file"]), "w", encoding="utf-8").write(text)
                r["chars"] = len(text)
                r["pages"] = text.count("\f") + 1 if r["kind"] == "pdf" else None
                r.setdefault("text_file", "txt_" + hashlib.sha1(r["url"].encode()).hexdigest() + ".txt")
                r["status"] = "ok" if len(text) > 50_000 else "too short"
            except Exception as e:
                r["status"] = f"download failed: {e}"
            r["checked"] = dt.date.today().isoformat()
            r.setdefault("language", "en")
            print(cid, y, r.get("form"), r["status"], r.get("chars"), flush=True)
            rows.append(r)
    rows.sort(key=lambda r: (r["company"], r["year"]))
    json.dump(rows, open(manifest_path, "w"), indent=1)


if __name__ == "__main__":
    main()
