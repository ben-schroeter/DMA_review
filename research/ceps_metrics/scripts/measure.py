"""Measure one EUR-Lex document: pages, words by part, restrictions by category and addressee."""
import json, os, re, subprocess, sys, tempfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import fetch
from textparse import html_to_lines, split_parts, recital_lines, words
from restrictions import strip_quoted, clauses, find_instances

CATS = ["obligation", "prohibition", "restricted_permission", "explicit_requirement", "duty_of_result"]
ADDR = ["private_parties", "member_states", "eu_institutions", "unclear"]


def _pages(data):
    if not data.startswith(b"%PDF"):
        return None
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data); f.flush()
        out = subprocess.run(["pdfinfo", f.name], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def cellar_pdf_items(celex):
    """English PDF items of a work from Cellar (multi-part documents such as COM proposals)."""
    import urllib.request, urllib.error
    from common import CACHE
    import hashlib
    key = os.path.join(CACHE, "items_" + hashlib.sha1(celex.encode()).hexdigest())
    if os.path.exists(key):
        return json.load(open(key))
    req = urllib.request.Request("https://publications.europa.eu/resource/celex/" + celex,
                                 headers={"Accept": "application/pdf", "Accept-Language": "eng"})

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        r = opener.open(req, timeout=60); body = r.read().decode("utf-8", "replace"); loc = None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace"); loc = e.headers.get("Location")
    items = re.findall(r'href="(http[^"]+/DOC_\d+)"', body) or ([loc] if loc else [])
    items = sorted({i.replace("http://", "https://") for i in items if i})
    json.dump(items, open(key, "w"))
    return items


def pdf_pages(celex):
    p = _pages(fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:{celex}", binary=True))
    if p:
        return p, "eurlex_pdf"
    total = 0
    for it in cellar_pdf_items(celex):
        n = _pages(fetch(it, binary=True))
        total += n or 0
    return (total or None), "cellar_pdf_items"


def count_restrictions(lines, with_addressee=True, sample_sink=None, doc_id=""):
    from addressee import addressee, _LAST
    _LAST["who"] = None
    res = collections.Counter()
    by_addr = collections.Counter()
    n_excl = 0
    for cl in clauses(strip_quoted(lines)):
        inst, ne = find_instances(cl)
        n_excl += ne
        for cat, a, b in inst:
            res[cat] += 1
            if with_addressee:
                who, subj = addressee(cl[:600], min(a, 599))
                by_addr[who] += 1
                if sample_sink is not None:
                    sample_sink.append({"doc": doc_id, "clause": cl[:600], "marker": cl[a:b], "category": cat,
                                        "addressee": who, "subject": subj})
    return res, by_addr, n_excl


def measure(celex, is_proposal=None, want_pages=True, with_addressee=True, sample_sink=None):
    raw = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}")
    lines = html_to_lines(raw)
    if is_proposal is None:
        is_proposal = bool(re.match(r"5\d{4}PC", celex))
    parts = split_parts(lines, is_proposal=is_proposal)
    rec = recital_lines(parts["preamble"])
    out = {"celex": celex, "n_lines": len(lines)}
    if len(" ".join(lines)) < 400 or not (parts["articles"] or parts["annexes"]):
        out["parse_warning"] = "little or no text in HTML (may be scanned/PDF only)"
    out["words_memorandum"] = words(" ".join(parts["memorandum"]))
    out["words_preamble"] = words(" ".join(parts["preamble"]))
    out["words_recitals"] = words(" ".join(rec))
    out["words_articles"] = words(" ".join(parts["articles"]))
    out["words_annexes"] = words(" ".join(parts["annexes"]))
    out["words_financial_statement"] = words(" ".join(parts["financial_statement"]))
    out["words_legal_text"] = out["words_preamble"] + out["words_articles"] + out["words_annexes"]
    if want_pages:
        try:
            out["pages"], out["pages_source"] = pdf_pages(celex)
        except Exception as e:
            out["pages"] = None; out["pages_err"] = str(e)[:80]
    res, by_addr, n_excl = count_restrictions(parts["articles"] + parts["annexes"], with_addressee, sample_sink, celex)
    for c in CATS:
        out["r_" + c] = res[c]
    out["restrictions_total"] = sum(res.values())
    for a in ADDR:
        out["addr_" + a] = by_addr[a] if with_addressee else None
    out["excluded_shall_uses"] = n_excl
    return out


if __name__ == "__main__":
    print(json.dumps(measure(sys.argv[1]), indent=1))


def pdf_text_lines(celex):
    """Text of the document's PDF(s), de-hyphenated and joined into paragraphs (fallback for scanned/table HTML)."""
    data = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:{celex}", binary=True)
    blobs = [data] if data.startswith(b"%PDF") else [fetch(i, binary=True) for i in cellar_pdf_items(celex)]
    text = ""
    for b in blobs:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(b); f.flush()
            text += subprocess.run(["pdftotext", f.name, "-"], capture_output=True, text=True).stdout + "\n"
    text = re.sub(r"-\n(?=[a-z])", "", text.replace("\f", "\n"))
    paras, cur = [], []
    for l in text.split("\n"):
        l = l.strip()
        if not l:
            if cur: paras.append(" ".join(cur)); cur = []
            continue
        if re.match(r"^(Article \d+|ANNEX|HAS ADOPTED|HAVE ADOPTED|Whereas|Having regard|Proposal for)", l) and cur:
            paras.append(" ".join(cur)); cur = []
        cur.append(l)
    if cur: paras.append(" ".join(cur))
    return paras


def measure_from_pdf(celex, is_proposal=True):
    paras = pdf_text_lines(celex)
    start = next((i for i, p in enumerate(paras) if re.match(r"^Proposal for an?\b", p, re.I)
                  and any(q.startswith("Having regard") or q.startswith("THE COUNCIL") for q in paras[i:i + 12])), 0)
    p = split_parts(paras[start:], is_proposal=False)
    rec = recital_lines(p["preamble"])
    out = {"celex": celex, "source": "PDF text (approximate)", "words_memorandum": words(" ".join(paras[:start])),
           "words_preamble": words(" ".join(p["preamble"])), "words_recitals": words(" ".join(rec)),
           "words_articles": words(" ".join(p["articles"])), "words_annexes": words(" ".join(p["annexes"])),
           "words_financial_statement": words(" ".join(p["financial_statement"]))}
    out["words_legal_text"] = out["words_preamble"] + out["words_articles"] + out["words_annexes"]
    res, by_addr, n_excl = count_restrictions(p["articles"] + p["annexes"])
    for c in CATS:
        out["r_" + c] = res[c]
    out["restrictions_total"] = sum(res.values())
    for a in ADDR:
        out["addr_" + a] = by_addr[a]
    return out
