"""Shared headline counts for chart builders (same definitions as site/facts.py, computed from digital_rulebook.xlsx so
charts never carry typed numbers). Import from a builder run in research/digital_rulebook: from counts import N_LAWS, N_SEC, N_IMPL, N_DEL"""
import openpyxl
_wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
def _sheet(n):
    r = list(_wb[n].iter_rows(values_only=True)); return [dict(zip(r[0], x)) for x in r[1:] if any(v is not None for v in x)]
_A = [x for x in _sheet("instruments") if x["row_id"] and x["status"] == "adopted"]; _Aid = {x["row_id"] for x in _A}
_impl = [x for x in _sheet("secondary_acts") if x["parent_row_id"] in _Aid and x["kind"] in ("implementing", "delegated")]
_seen = set(); _impl = [x for x in _impl if not (x["celex"] in _seen or _seen.add(x["celex"]))]   # an act listed under two parent laws counts once
N_LAWS = len(_A); N_SEC = len(_impl)
N_IMPL = sum(x["kind"] == "implementing" for x in _impl); N_DEL = sum(x["kind"] == "delegated" for x in _impl)


# figures computed inside chart builders for the page text: site/page_figures.json, merged into site/facts.json by site/facts.py
import json as _json, os as _os
_PF = "site/page_figures.json"
def record(key, value, text=None):
    d = _json.load(open(_PF)) if _os.path.exists(_PF) else {}
    d[key] = {"value": value, "text": text if text is not None else (f"{value:,}" if isinstance(value, int) else str(value))}
    _json.dump(d, open(_PF, "w"), indent=1, ensure_ascii=False)


def nice_axis(v, n=6, pad=1.04):
    """Axis top and step for a maximum value v: the smallest round step that covers v (with a little headroom) in at most n steps."""
    for st in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000):
        top = -(-v * pad // st) * st
        if top / st <= n:
            return int(top), st
    return int(v * pad), int(v * pad)
