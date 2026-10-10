"""Download agency guideline PDFs, map each to the parent act it cites most, and measure pages/words/restrictions."""
import json, re, sys, subprocess, tempfile, collections, urllib.parse
sys.path.insert(0, ".")
from common import fetch
from measure import _pages, count_restrictions, CATS, ADDR
from textparse import words

PARENTS = {"32015L2366": [r"2015/2366", r"\bPSD2\b"], "32023R1114": [r"2023/1114", r"\bMiCA(?:R)?\b"],
           "32022R2554": [r"2022/2554", r"\bDORA\b"], "32024R1624": [r"2024/1624", r"\bAMLR\b"],
           "32022R0858": [r"2022/858", r"DLT Pilot"], "32016R0679": [r"2016/679", r"\bGDPR\b"]}


def pdf_text(b):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(b); f.flush()
        return subprocess.run(["pdftotext", f.name, "-"], capture_output=True, text=True).stdout


LEGAL_BASIS = re.compile(r"(?:pursuant\s+to|in\s+accordance\s+with|under|mandate[sd]?\s+(?:in|under|by)|referred\s+to\s+in|"
                         r"conferred\s+by|laid\s+down\s+in)\s+Articles?\s+[\d(), a-z]+?\s+(?:and\s+[\d()a-z]+\s+)?of\s+"
                         r"(?:Directive|Regulation)\s+\(EU\)\s+(?:No\s+)?(2015/2366|2023/1114|2022/2554|2024/1624|2022/858)")
NUM2CELEX = {"2015/2366": "32015L2366", "2023/1114": "32023R1114", "2022/2554": "32022R2554", "2024/1624": "32024R1624", "2022/858": "32022R0858"}


def map_parent_strict(text, title, allowed, hint=None):
    """Parent = act named as legal basis in the first part of the document (or in the title)."""
    head = text[:25000]
    lb = collections.Counter(NUM2CELEX[m] for m in LEGAL_BASIS.findall(head) if NUM2CELEX[m] in allowed)
    t = title.lower()
    for key, cel in (("psd2", "32015L2366"), ("mica", "32023R1114"), ("dora", "32022R2554"), ("dlt", "32022R0858")):
        if key in t and cel in allowed:
            lb[cel] += 5
    if hint and hint in allowed and lb.get(hint):
        lb[hint] += 2
    best = lb.most_common(1)
    return (best[0][0], best[0][1], dict(lb)) if best else (None, 0, dict(lb))


def map_parent(text, allowed):
    c = collections.Counter()
    for p, pats in PARENTS.items():
        if p in allowed:
            c[p] = sum(len(re.findall(x, text)) for x in pats)
    best = c.most_common(1)
    return (best[0][0], best[0][1], dict(c)) if best and best[0][1] >= 3 else (None, 0, dict(c))


def measure_doc(url):
    b = fetch(urllib.parse.quote(url, safe=":/?&=%"), binary=True)
    if not b.startswith(b"%PDF"):
        return None, {"error": "not a PDF"}
    text = re.sub(r"-\n(?=[a-z])", "", pdf_text(b))
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    res, addr, _ = count_restrictions(paras)
    m = {"pages": _pages(b), "words_total": words(text), "restrictions_total": sum(res.values()),
         "addr_private_parties": addr["private_parties"], "addr_member_states": addr["member_states"],
         "addr_eu_institutions": addr["eu_institutions"], "addr_unclear": addr["unclear"],
         "should_count": len(re.findall(r"\bshould\b", text, re.I))}
    for c in CATS:
        m["r_" + c] = res[c]
    return text, m


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "eba":
        items = json.load(open("../data/eba_items_raw.json"))
        allowed = {"32015L2366", "32023R1114", "32022R2554", "32024R1624"}
    elif which == "esma":
        items = json.load(open("../data/esma_items_raw.json"))
        allowed = {"32023R1114", "32022R2554", "32022R0858"}
    out = []
    for it in items:
        try:
            text, m = measure_doc(it["pdf"])
        except Exception as e:
            out.append({**it, "error": str(e)[:100]}); continue
        if text is None:
            out.append({**it, **m}); continue
        parent, n, counts = map_parent_strict(text, it.get("title", ""), allowed, it.get("topic_parent_hint"))
        if parent:
            out.append({**it, "agency": which.upper(), "parent": parent, "citations": n, **m})
    json.dump(out, open(f"../data/agency_{which}.json", "w"), indent=1)
    print(len(out), "mapped;", collections.Counter(o.get("parent") for o in out))
    for o in out:
        print(o.get("parent"), o.get("date_text"), o.get("title", "")[:90], o.get("restrictions_total"), o.get("should_count"), o.get("error", ""))
