"""Measure the Colorado AI Act (SB 24-205, signed 17 May 2024) with the same US-adapted restriction counter used for SOX and the
matched pairs, as a same-job US comparator for the EU AI Act. The enrolled bill prints new statutory text in capitals, so the
text is lower-cased before counting. Writes ../data/us_map/instances_colorado_ai_all_text.json and ../data/benchmark_colorado_ai.json.
Usage (from scripts/): python3 benchmark_colorado.py"""
import json, os, re, subprocess, sys
sys.argv = [sys.argv[0], "", ""]
src = open("benchmark_us.py").read().split("pdf, label = sys.argv[1]")[0]
exec(compile(src, "benchmark_us_head", "exec"))
_full = open("benchmark_us.py").read()
exec(compile(re.search(r"def run\(ps\):.*?return res, addr, sample\n", _full, re.S).group(0), "benchmark_us_run", "exec"))
from textparse import words  # noqa: E402

P = os.path.expanduser("~/.cache/us_texts/co_sb24_205.pdf")   # https://leg.colorado.gov/sites/default/files/2024a_205_signed.pdf
raw = subprocess.run(["pdftotext", P, "-"], capture_output=True, text=True).stdout
pages = raw.count("\f")
t = raw[raw.find("SECTION 1."):]
t = t.split("APPROVED BY THE GOVERNOR")[0].split("____")[0]
t = re.sub(r"(?m)^\s*(PAGE \d+-SENATE BILL 24-205|Capital letters or bold.*|through words or numbers.*|the act\.)\s*$", "", t)
t = re.sub(r"Capital letters or bold & italic numbers indicate new material.*?not part of\s+the act\.", " ", t, flags=re.S)
t = re.sub(r"-\n(?=[A-Za-z])", "", t).lower()
# one paragraph per numbered subsection
t = re.sub(r"\n(?=\(\w{1,5}\)\s)", "\n\n", t)
t = re.sub(r"\n(?=section \d+\.|6-1-17\d\d\.)", "\n\n", t)
ps = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", t) if p.strip()]
ps = [p for p in ps if len(p.split()) > 3 or re.search(r"\b(shall|must|may)\b", p)]
r, a, s = run(ps)
n = sum(r.values())
txt = "\n\n".join(ps)
out = {"label": "Colorado AI Act (SB 24-205, 2024)", "pages": pages, "all_text": {"words": words(txt), "restrictions_total": n, "by_category": r,
       "by_addressee": a, "per_1000_words": round(1000 * n / max(1, words(txt)), 1)}}
json.dump(s, open("../data/us_map/instances_colorado_ai_all_text.json", "w"), indent=1)
json.dump(out, open("../data/benchmark_colorado_ai.json", "w"), indent=1)
print(json.dumps(out, indent=1))
