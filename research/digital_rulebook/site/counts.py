"""Shared headline counts for chart builders (same definitions as site/facts.py, computed from digital_rulebook.xlsx so
charts never carry typed numbers). Import from a builder run in research/digital_rulebook: from counts import N_LAWS, N_SEC, N_IMPL, N_DEL"""
import openpyxl
_wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
def _sheet(n):
    r = list(_wb[n].iter_rows(values_only=True)); return [dict(zip(r[0], x)) for x in r[1:] if any(v is not None for v in x)]
_A = [x for x in _sheet("instruments") if x["row_id"] and x["status"] == "adopted"]; _Aid = {x["row_id"] for x in _A}
_impl = [x for x in _sheet("secondary_acts") if x["parent_row_id"] in _Aid and x["kind"] in ("implementing", "delegated")]
N_LAWS = len(_A); N_SEC = len(_impl)
N_IMPL = sum(x["kind"] == "implementing" for x in _impl); N_DEL = sum(x["kind"] == "delegated" for x in _impl)
