"""Download HTML (+PDF for page counts) for every text to be measured. Cached on disk."""
import csv, json, sys, concurrent.futures as cf
sys.path.insert(0, ".")
from common import fetch

def urls(celex):
    base = "https://eur-lex.europa.eu/legal-content/EN/TXT/{}/?uri=CELEX:" + celex
    return base.format("HTML"), base.format("PDF")

def job(item):
    celex, want_pdf = item
    h, p = urls(celex)
    st = {"celex": celex}
    try:
        st["html_len"] = len(fetch(h, binary=True))
    except Exception as e:
        st["html_err"] = str(e)[:100]
    if want_pdf:
        try:
            st["pdf_len"] = len(fetch(p, binary=True))
        except Exception as e:
            st["pdf_err"] = str(e)[:100]
    return st

if __name__ == "__main__":
    items = {}
    for r in csv.DictReader(open("../data/instrument_map.csv")):
        for c in r["celex_measured"].split(";"):
            if not c.startswith("COUNCIL"):
                items[c] = True
    for c, v in json.load(open("../data/consolidated.json")).items():
        items.setdefault(v["latest"], False)
    for s in json.load(open("../data/secondary_acts.json")):
        items.setdefault(s["celex"], True)
    print(len(items), "documents", flush=True)
    log = []
    with cf.ThreadPoolExecutor(3) as ex:
        for i, st in enumerate(ex.map(job, items.items())):
            log.append(st)
            if i % 50 == 0:
                print(i, st, flush=True)
    json.dump(log, open("../data/download_log.json", "w"), indent=1)
    print("done", sum("html_err" in s for s in log), "html errors", sum("pdf_err" in s for s in log), "pdf errors")
