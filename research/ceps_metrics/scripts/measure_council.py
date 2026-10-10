"""Measure the PSR / PSD3 Council final compromise texts (ST 8221/26, ST 8222/26)."""
import json, re, subprocess, sys, os
sys.path.insert(0, ".")
from common import fetch
from textparse import split_parts, recital_lines, words
from measure import count_restrictions, CATS, ADDR, _pages

DOCS = {"COUNCIL-2026-04-23-PSR": "8221", "COUNCIL-2026-04-23-PSD3": "8222"}
HEADER = re.compile(r"^\s*(\d{4}/26\s+\d+|[A-Z]{3,}\.\d\.[A-Z]\s+LIMITE\s+EN|LIMITE|EN)\s*$")
FOOTNOTE = re.compile(r"^\s{0,8}\d{1,3}\s{3,}\S")


def lines_of(pdf_bytes):
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf_bytes); f.flush()
        txt = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True).stdout
    out, in_fn = [], False
    for raw in txt.replace("\f", "\n").split("\n"):
        if HEADER.match(raw) or not raw.strip():
            in_fn = False if not raw.strip() else in_fn
            continue
        if FOOTNOTE.match(raw):
            in_fn = True; continue
        if in_fn and re.match(r"^\s{4,}\S", raw) and not re.match(r"^\s*(\(|Article|\d+\.)", raw.strip()):
            continue                     # footnote continuation
        in_fn = False
        out.append(re.sub(r"\s+", " ", raw.replace("▌", " ")).strip())
    # join wrapped lines into paragraphs: a new paragraph starts with (n), n., Article, CHAPTER, ANNEX, a capital after a full stop
    paras, cur = [], ""
    for l in out:
        new = re.match(r"^(\((?:\d{1,3}|[a-z]{1,2}|[ivx]{1,5})\)|\d+\.|Article \d|CHAPTER|TITLE|SECTION|ANNEX|Whereas|Having regard|HAVE ADOPTED|Done at|For the)", l)
        if new and cur:
            paras.append(cur); cur = l
        else:
            cur = (cur + " " + l).strip()
    if cur:
        paras.append(cur)
    return paras


res = []
for cid, n in DOCS.items():
    pdf = fetch(f"https://data.consilium.europa.eu/doc/document/ST-{n}-2026-INIT/en/pdf", binary=True)
    paras = lines_of(pdf)
    start = next(i for i, p in enumerate(paras) if "THE EUROPEAN PARLIAMENT AND THE COUNCIL OF THE EUROPEAN UNION" in p
                 or p.startswith("Having regard"))
    paras[start] = paras[start][paras[start].find("Proposal for a"):] if "Proposal for a" in paras[start] else paras[start]
    p = split_parts(paras[start:])
    rec = recital_lines(p["preamble"])
    o = {"celex": cid, "kind": "main", "council_doc": f"ST {n}/26", "pages": _pages(pdf),
         "pages_source": "Council document PDF (Council layout, not comparable with OJ pages)",
         "words_memorandum": 0, "words_preamble": words(" ".join(p["preamble"])), "words_recitals": words(" ".join(rec)),
         "words_articles": words(" ".join(p["articles"])), "words_annexes": words(" ".join(p["annexes"])),
         "words_financial_statement": 0}
    o["words_legal_text"] = o["words_preamble"] + o["words_articles"] + o["words_annexes"]
    r, a, ne = count_restrictions(p["articles"] + p["annexes"])
    for c in CATS: o["r_" + c] = r[c]
    o["restrictions_total"] = sum(r.values())
    for x in ADDR: o["addr_" + x] = a[x]
    o["excluded_shall_uses"] = ne
    res.append(o); print(json.dumps(o))
json.dump(res, open("../data/measurements_council.json", "w"), indent=1)
