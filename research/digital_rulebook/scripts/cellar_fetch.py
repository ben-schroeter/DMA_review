"""Pre-fill the download cache from the Publications Office's Cellar when EUR-Lex refuses automated requests.

For each CELEX number: find the English XHTML and PDF manifestations via SPARQL, download them, and store them in the
cache under the EUR-Lex HTML/PDF URLs that measure.py and download.py ask for, so the rest of the pipeline runs unchanged.
Usage (from scripts/): python3 cellar_fetch.py 32026R0877 [more CELEX numbers]"""
import hashlib, os, sys, urllib.request
sys.path.insert(0, ".")
from common import CACHE, sparql

Q = """PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
SELECT ?m ?type WHERE {{
  ?w cdm:resource_legal_id_celex "{celex}"^^<http://www.w3.org/2001/XMLSchema#string> .
  ?e cdm:expression_belongs_to_work ?w ; cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
  ?m cdm:manifestation_manifests_expression ?e ; cdm:manifestation_type ?type }}"""


def _get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
        return r.read()


def _item(manifestation):
    """A manifestation URI returns RDF metadata; the document is its first item (usually .../DOC_1)."""
    meta = _get(manifestation)
    if not meta.lstrip().startswith(b"<rdf:RDF"):
        return meta
    import re
    items = sorted(set(re.findall(rb'manifestation_has_item rdf:resource="([^"]+)"', meta)))
    return _get((items[0] if items else (manifestation + "/DOC_1").encode()).decode())


def _store(url, data):
    os.makedirs(CACHE, exist_ok=True)
    open(os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest()), "wb").write(data)


def prefill(celex, force=False):
    html_url = f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"
    pdf_url = f"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:{celex}"
    if not force and os.path.exists(os.path.join(CACHE, hashlib.sha1(html_url.encode()).hexdigest())):
        return "cached"
    man = {}
    for b in sparql(Q.format(celex=celex)):
        man.setdefault(b["type"]["value"], []).append(b["m"]["value"])
    xh = sorted(man.get("xhtml", []))
    if not xh:
        return f"no xhtml manifestation ({sorted(man)})"
    _store(html_url, _item(xh[-1]))
    pdfs = sorted(man.get("pdfa2a", []) + man.get("pdfa1a", []) + man.get("pdf", []))
    if pdfs:
        try:
            _store(pdf_url, _item(pdfs[-1]))
        except Exception as e:
            return f"html ok, pdf failed: {str(e)[:60]}"
    return "ok"


if __name__ == "__main__":
    for c in [a for a in sys.argv[1:] if not a.startswith("--")]:
        print(c, prefill(c, force="--force" in sys.argv))
