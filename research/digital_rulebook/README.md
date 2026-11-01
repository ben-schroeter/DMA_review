# EU Digital Rulebook database: size, obligations, secondary acts and pending initiatives

`digital_rulebook.xlsx` — one row per EU digital initiative (136 rows: 105 adopted laws, 4 agreed, 20 in negotiation, 7 announced; the `status` column says which), with page and word counts, restriction counts by type and addressee, consolidated-text counts, counts of implementing/delegated acts and guidance, and national transposition measures for directives. Each implementing/delegated act and guidance document is a line item in `secondary_acts`. Initiatives not yet adopted carry their legislative stage (Parliament and Council positions, trilogues, agreement, latest status); the `reviews` sheet tracks guidance under revision. `scripts/migrate_database.py` keeps the sheet in step with `site/build_forthcoming.py`. The list started from the inventory by Zenner and Marcus (July 2025) and is maintained by this project. See `METHOD.md` (also the `method` sheet) and the `validation` sheet.

Rebuild (texts are cached in `~/.cache/digital_rulebook`, ~0.5 GB):

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
