import json, sys, urllib.request, urllib.parse
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
def get(ds, **f):
    q = urllib.parse.urlencode({**f, "format": "JSON", "lang": "EN"}, doseq=True)
    try:
        d = json.load(urllib.request.urlopen(B + ds + "?" + q, timeout=120))
    except Exception as e:
        return None, str(e)
    return d, None
def dims(ds, **f):
    d, e = get(ds, **f)
    if e: print(ds, "ERR", e); return
    for k in d["id"]:
        cat = d["dimension"][k]["category"]; lab = cat.get("label", {})
        print(" ", k, list(lab.items())[:40])
def series(ds, **f):
    d, e = get(ds, **f)
    if e: print(ds, "ERR", e); return {}
    tl = d["dimension"]["time"]["category"]["index"]; inv = {v: k for k, v in tl.items()}
    # assumes all other dims filtered to one value
    return {inv[int(k) % len(tl)]: v for k, v in d["value"].items()}
