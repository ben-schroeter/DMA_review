"""Crawl the ESMA library; keep final Guidelines & Recommendations in Digital Finance / Joint Committee sections."""
import json, re, sys, html as H
sys.path.insert(0, ".")
from common import fetch
BASE = "https://www.esma.europa.eu"
rows = []
for p in range(0, 400):
    h = fetch(f"{BASE}/databases-library/esma-library?page={p}")
    trs = re.findall(r"<tr>(.*?)</tr>", h, re.S)
    got = 0
    for tr in trs:
        cell = lambda k: re.sub(r"<[^>]+>|\s+", " ", (re.search(rf'field-{k}">(.*?)</td>', tr, re.S) or [None, ""])[1]).strip()
        date = (re.search(r'datetime="(\d{4}-\d{2}-\d{2})', tr) or [None, None])[1]
        title_m = re.search(r'views-field-title"><a href="([^"]+)"[^>]*>([^<]+)</a>', tr)
        pdf = (re.search(r"href=\"([^\"]+\.pdf)\"", tr) or [None, None])[1]
        if not title_m:
            continue
        got += 1
        rows.append({"date": date, "reference": cell("document-reference"), "title": H.unescape(title_m.group(2)).strip(),
                     "page_url": BASE + title_m.group(1), "sections": cell("document-section"), "type": cell("document-type"),
                     "pdf": (BASE + pdf) if pdf and pdf.startswith("/") else pdf})
    if not got:
        break
json.dump(rows, open("../data/esma_library_all.json", "w"), indent=1)
keep = [r for r in rows if "Guidelines" in r["type"] and re.search(r"Digital Finance|Joint Committee", r["sections"])
        and not re.search(r"consultation|draft|translation", r["title"], re.I)]
import collections
print(len(rows), "rows;", len(keep), "candidate guidelines")
for k in keep: print(k["date"], k["sections"][:40], "|", k["title"][:100])
json.dump([{"date_text": k["date"], "pdf": k["pdf"], "title": k["title"], "reference": k["reference"], "sections": k["sections"]}
           for k in keep if k["pdf"]], open("../data/esma_items_raw.json", "w"), indent=1)
