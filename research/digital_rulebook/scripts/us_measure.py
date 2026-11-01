"""Measure the US counterparts of the 'close' EU matches (plus GDPR -> CCPA) with the same restriction counter used for
the Sarbanes-Oxley benchmark. Texts: enacted Public Laws from govinfo (HTML from 1995, scanned Statutes at Large PDFs before),
current US Code / eCFR text where the counterpart is a section or a rule, and the CCPA as amended (CPPA PDF).
Usage (from scripts/): python3 us_measure.py"""
import html, json, os, re, subprocess, sys, urllib.request
sys.argv = [sys.argv[0], "", ""]          # benchmark_us reads argv at import; we only want its patched counter
CACHE = os.path.expanduser("~/.cache/us_texts/")
UA = {"User-Agent": "Mozilla/5.0"}

# reuse the US-adapted counter (exclusions, addressee lexicons) without running its main block
src = open("benchmark_us.py").read().split("pdf, label = sys.argv[1]")[0]
exec(compile(src, "benchmark_us_head", "exec"))
_full = open("benchmark_us.py").read()
exec(compile(re.search(r"def run\(ps\):.*?return res, addr, sample\n", _full, re.S).group(0), "benchmark_us_run", "exec"))
from textparse import words  # noqa: E402

SPECS = [
    # id, EU rows, label, kind, source, start (regex, nth occurrence), end regex
    ("dmca", [7], "Digital Millennium Copyright Act (1998)", "plaw", "PLAW-105publ304", None, None),
    ("hsr", [11], "Hart-Scott-Rodino Act, title II (1976)", "pdf", "STATUTE-90-Pg1383", (r"T\s?I\s?T\s?L\s?E\s+II\W+PREMERGER", 2), r"T\s?I\s?T\s?L\s?E\s+III\W+PARENS"),
    ("ftc5", [13], "FTC Act section 5 (15 U.S.C. 45, current)", "cornell", "https://www.law.cornell.edu/uscode/text/15/45", None, None),
    ("cpsia", [17, 103], "Consumer Product Safety Improvement Act (2008)", "plaw", "PLAW-110publ314", None, None),
    ("ccpa", [20], "California Consumer Privacy Act, as amended by the CPRA (current)", "ccpa", "ccpa", None, None),
    ("dtsa", [26], "Defend Trade Secrets Act (2016)", "plaw", "PLAW-114publ153", None, None),
    ("privacy_act", [35], "Privacy Act (1974)", "pdf", "STATUTE-88-Pg1896", (r"Public Law 93-579\s+D", 1), None),
    ("cfaa1984", [40], "Counterfeit Access Device and Computer Fraud and Abuse Act (1984)", "pdf", "STATUTE-98-Pg1837",
     (r"CHAPTER XXI\W+ACCESS DEVICES", 1), r"CHAPTER XXII\b"),
    ("cloud", [42], "CLOUD Act (2018, division V of Pub. L. 115-141)", "plaw", "PLAW-115publ141", (r"DIVISION V--", 2), r"DIVISION W--"),
    ("open_data", [43], "OPEN Government Data Act (2019, title II of Pub. L. 115-435)", "plaw", "PLAW-115publ435", (r"TITLE II--OPEN", 2), r"TITLE III--"),
    ("cpsa", [67], "Consumer Product Safety Act (1972)", "pdf", "STATUTE-86-Pg1207", None, None),
    ("bsa", [68], "Bank Secrecy Act, titles I-II (1970)", "pdf", "STATUTE-84-Pg1114-2", (r"TITLE I\W+FINANCIAL", 1), r"TITLE III\W+MARGIN"),
    ("chips", [74], "CHIPS Act of 2022 (division A of Pub. L. 117-167)", "plaw", "PLAW-117publ167", (r"SEC\. 101\.\s+SHORT TITLE", 1), r"DIVISION B--"),
    ("fisma", [78], "Federal Information Security Modernization Act (2014)", "plaw", "PLAW-113publ283", None, None),
    ("df1033", [98], "Dodd-Frank Act section 1033 (2010)", "plaw", "PLAW-111publ203", (r"SEC\. 1033\.", 1), r"SEC\. 1034\."),
    ("cfr1033", [98], "CFPB personal financial data rights rule (12 CFR part 1033)", "ecfr", "title-12.xml?part=1033", None, None),
    ("fcc15", [109], "FCC radio frequency devices rules (47 CFR part 15)", "ecfr", "title-47.xml?part=15", None, None),
]


def get(url, path):
    if not os.path.exists(path) and "ecfr.gov" in url:      # eCFR requires a compressed response
        subprocess.run(["curl", "-s", "--compressed", "-m", "300", "-A", UA["User-Agent"], "-o", path, url], check=True)
    if not os.path.exists(path):
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300).read()
        open(path, "wb").write(data)
    return path


def slice_(text, start, end):
    if start:
        ms = list(re.finditer(start[0], text))
        if len(ms) < start[1]:
            raise ValueError(f"start {start} found {len(ms)} times")
        text = text[ms[start[1] - 1].start():]
    if end:
        m = re.search(end, text[10:])
        if m:
            text = text[:m.start() + 10]
    return text


def load(kind, source, start, end):
    """Return (text, pages)."""
    if kind == "plaw":
        t = html.unescape(re.sub(r"<[^>]+>", "", open(get(f"https://www.govinfo.gov/content/pkg/{source}/html/{source}.htm",
                                                             CACHE + source + ".htm"), encoding="utf-8", errors="ignore").read()))
        t = re.sub(r"<<NOTE:.*?>>", " ", t, flags=re.S)
        t = slice_(t, start, end)
        pages = len(re.findall(r"\[\[Page", t)) + 1
        t = re.sub(r"\[\[Page[^\]]*\]\]", " ", t)
        t = re.sub(r"(?m)^\s*(LEGISLATIVE HISTORY|Approved).*", "", t)
        t = t.split("LEGISLATIVE HISTORY")[0]
        return t, pages
    if kind == "pdf":
        raw = subprocess.run(["pdftotext", get(f"https://www.govinfo.gov/content/pkg/{source.split('-Pg')[0]}/pdf/{source}.pdf",
                                               CACHE + source + ".pdf"), "-"], capture_output=True, text=True).stdout
        t = slice_(raw, start, end)
        pages = t.count("\f") + 1
        t = re.sub(r"(?m)^\s*(\d+ STAT\. \d+|PUBLIC LAW \d+-\d+.*\d{4}|\d+ USC \d+.*|[^a-z]{0,25})\s*$", "", t.replace("\f", "\n"))
        t = t.split("LEGISLATIVE HISTORY")[0]
        return t, pages
    if kind == "cornell":
        h = open(get(source, CACHE + "ftc45.html"), encoding="utf-8", errors="ignore").read()
        h = h[h.find('id="tab_default_1"'):] if 'id="tab_default_1"' in h else h
        h = h.split('id="tab_default_2"')[0]
        t = html.unescape(re.sub(r"<[^>]+>", "\n", h))
        return t, None
    if kind == "ecfr":
        x = open(get("https://www.ecfr.gov/api/versioner/v1/full/2026-10-07/" + source, CACHE + source.replace("?", "_") + ".xml"),
                 encoding="utf-8", errors="ignore").read()
        x = re.sub(r"<(CITA|SOURCE|AUTH|EDNOTE)[^>]*>.*?</\1>", " ", x, flags=re.S)
        t = html.unescape(re.sub(r"<(P|HEAD|FP)[^>]*>", "\n\n", x))
        return re.sub(r"<[^>]+>", " ", t), None
    if kind == "ccpa":
        p = CACHE + "ccpa.pdf"
        raw = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
        pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout).group(1))
        t = raw[raw.find("1798.100"):] if "1798.100" in raw else raw
        return t, pages


def paragraphs(t):
    t = re.sub(r"-\n(?=[a-z])", "", t)
    ps = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
    return [p for p in ps if len(p.split()) > 3 or re.search(r"\b(shall|must|may)\b", p)]


out = []
for sid, rows, label, kind, source, start, end in SPECS:
    t, pages = load(kind, source, start, end)
    ps = paragraphs(t)
    joined = "\n\n".join(ps)
    rec = {"id": sid, "eu_rows": rows, "label": label, "kind": kind, "source": source, "pages": pages}
    variants = [("all_text", joined)]
    if kind in ("plaw", "pdf"):
        variants.append(("excluding_inserted_text", re.sub(r"(``|‘‘|\").*?(''|’’|\")", " ", joined, flags=re.S)))
    for name, txt in variants:
        r, a, s = run([p for p in txt.split("\n\n") if p.strip()])
        n = sum(r.values())
        rec[name] = {"words": words(txt), "restrictions_total": n, "by_category": r, "by_addressee": a,
                     "per_1000_words": round(1000 * n / max(1, words(txt)), 1)}
        json.dump(s, open(f"../data/us_map/instances_{sid}_{name}.json", "w"), indent=1)
    out.append(rec)
    v = rec.get("excluding_inserted_text", rec["all_text"])
    print(f"{sid:12} pages={pages} words={rec['all_text']['words']:>7} restr={rec['all_text']['restrictions_total']:>5} "
          f"| excl.inserted words={v['words']:>7} restr={v['restrictions_total']:>5} per1000={v['per_1000_words']}")
json.dump(out, open("../data/us_map/us_measurements.json", "w"), indent=1)
