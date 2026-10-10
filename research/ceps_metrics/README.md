# CEPS instruments: size, restrictions and secondary acts

`ceps_instruments_metrics.xlsx` — one row per instrument in the CEPS EU digital dataset (115 rows), with page and word counts, restriction counts by type and addressee, consolidated-text counts, counts of implementing/delegated acts and guidance, and national transposition measures for directives. Each implementing/delegated act and guidance document is a line item in `secondary_acts`. See `METHOD.md` (also the `method` sheet) and the `validation` sheet.

Rebuild (texts are cached in `~/.cache/ceps_metrics`, ~0.5 GB):

```
cd scripts
python3 build_map.py && python3 consolidated.py && python3 secondary.py && python3 filter_secondary.py && python3 nim.py
python3 download.py && python3 run_all.py && python3 build_workbook.py
```
Requires `spacy` with `en_core_web_sm`, `openpyxl`, and `pdfinfo` (poppler).

## Planned website
The findings will be published as a website at the end of the project. Everything the site needs is kept as data, not only in the workbook:
- `data/impact/<CELEX>.json` — per instrument: plain-language summary, evidence rating, promised indicators and their status, and every source with a stable `id`, link, open PDF link, Internet Archive copy, plain-language summary, access type and date checked (schema in `data/impact/SCHEMA.md`).
- `data/*.json|csv` and the workbook — metrics per instrument, secondary acts, amendments, guidance and benchmarks.
- `charts/` — figures, regenerated from the workbook by `scripts/charts.py`.
