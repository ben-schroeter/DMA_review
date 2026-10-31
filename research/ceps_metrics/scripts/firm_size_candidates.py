"""Find every sentence in the adopted main acts that sets a size test (micro, small, SME, staff or turnover figures,
user thresholds, designation as gatekeeper or very large platform). Writes data/firm_size/candidates.jsonl.
Run from research/ceps_metrics."""
import json, os, re, sys
sys.path.insert(0, "scripts")
from common import fetch
from textparse import html_to_lines, split_parts
import openpyxl

SIZE = re.compile(r"micro[- ]?enterprise|microenterprise|small (and medium[- ]sized |or medium[- ]sized )?enterprise|\bsmes?\b|small mid-cap|"
                  r"medium-sized enterprise|2003/361|\b\d[\d ,.]* (persons|employees|staff)\b|annual turnover (of|exceeding|above|below|not exceeding)|"
                  r"balance[- ]sheet total|45 million|\bsize[- ]cap|average monthly active recipients", re.I)
ART = re.compile(r"^Article\s+(\d+[a-z]?)\s*$", re.I)
wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
inst = [dict(zip(h, r)) for r in rows[1:] if r[0]]
out = []
for r in inst:
    if r["status_oct2026"] != "adopted" or not r["celex_measured"] or r["restrictions_total"] is None:
        continue
    c = r["celex_measured"].split(";")[0]
    parts = split_parts(html_to_lines(fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{c}")))
    art, head, expect = "", "", False
    for line in parts["articles"]:
        s = line.strip()
        m = ART.match(s)
        if m:
            art, head, expect = "Art. " + m.group(1), "", True
            continue
        if expect:
            expect = False
            if len(s) < 160 and not s.endswith((".", ";", ":")):
                head = s; continue
        if SIZE.search(s):
            out.append({"row_id": r["row_id"], "law": r["name"], "celex": c, "article": art, "heading": head, "text": s[:900]})
with open("data/firm_size/candidates.jsonl", "w") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
import collections
print(len(out), "sentences in", len({o["celex"] for o in out}), "laws")
for k, v in collections.Counter(o["law"] for o in out).most_common(60): print(f"{v:4d} {k}")
