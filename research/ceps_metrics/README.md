# CEPS instruments: size, restrictions and secondary acts

`ceps_instruments_metrics.xlsx` — one row per instrument in the CEPS EU digital dataset (115 rows), with page and word counts, restriction counts by type and addressee, consolidated-text counts, counts of implementing/delegated acts and guidance, and national transposition measures for directives. Each implementing/delegated act and guidance document is a line item in `secondary_acts`. See `METHOD.md` (also the `method` sheet) and the `validation` sheet.

Rebuild (texts are cached in `~/.cache/ceps_metrics`, ~0.5 GB):

```
cd scripts
python3 build_map.py && python3 consolidated.py && python3 secondary.py && python3 filter_secondary.py && python3 nim.py
python3 download.py && python3 run_all.py && python3 build_workbook.py
```
Requires `spacy` with `en_core_web_sm`, `openpyxl`, and `pdfinfo` (poppler).
