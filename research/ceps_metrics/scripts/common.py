"""Shared helpers: EUR-Lex / Cellar access with on-disk cache."""
import hashlib, json, os, re, time, urllib.parse, urllib.request

CACHE = os.environ.get("CEPS_CACHE", os.path.expanduser("~/.cache/ceps_metrics"))
SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
UA = {"User-Agent": "ceps-metrics research script (contact: repo owner)"}


def fetch(url, binary=False, retries=4, sleep=1.0):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(path):
        data = open(path, "rb").read()
    else:
        for i in range(retries):
            try:
                req = urllib.request.Request(url, headers=UA)
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = r.read()
                break
            except Exception:
                if i == retries - 1:
                    raise
                time.sleep(2 ** (i + 1))
        open(path, "wb").write(data)
        time.sleep(sleep)
    return data if binary else data.decode("utf-8", "replace")


def sparql(query):
    url = SPARQL + "?" + urllib.parse.urlencode(
        {"query": query, "format": "application/sparql-results+json"})
    return json.loads(fetch(url, sleep=0.3))["results"]["bindings"]


def celex_from_identifier(ident):
    """'Directive (EU) 2016/680' -> ['32016L0680']; handles old number/year forms."""
    out = []
    kind = {"Regulation": "R", "Directive": "L", "Decision": "D"}
    k = next((v for key, v in kind.items() if ident.startswith(key)), None)
    if not k:
        return out
    for a, b in re.findall(r"(\d{1,4})/(\d{1,4})", ident):
        a, b = int(a), int(b)
        if k != "L" and 1950 <= b <= 2030 and not (a >= 2015 and len(str(a)) == 4):
            year, num = b, a                       # pre-2015 regs/decisions: number/year
        else:
            year, num = a, b                       # year/number form
        if year < 100:
            year += 1900
        out.append(f"3{year}{k}{num:04d}")
    return out
