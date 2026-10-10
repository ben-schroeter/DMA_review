import sys, re, csv
sys.path.insert(0, ".")
from common import fetch
rows = [r for r in csv.DictReader(open("../data/ceps_instruments.csv")) if r["status"] == "proposed"]
for r in rows:
    m = re.match(r"(\d{4})/0*(\d+)\((COD|CNS|NLE)\)", r["identifier"])
    if not m:
        print("NO PROC", r["name"], r["identifier"]); continue
    url = f"https://eur-lex.europa.eu/procedure/EN/{m.group(1)}_{m.group(2)}"
    h = fetch(url)
    t = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", h, flags=re.S)); t = re.sub(r"\s+", " ", t)
    cel = sorted(set(re.findall(r"\b[35]\d{4}(?:PC|R|L|D)\d{4}\b", t)))
    status = re.findall(r"(Procedure completed|Ongoing procedure|Procedure lapsed or withdrawn|withdrawn)", t)
    print(f"{r['name'][:40]:40} {r['identifier']:18} {sorted(set(status))} {cel}")
