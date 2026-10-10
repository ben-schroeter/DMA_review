# Impact evidence records (one JSON file per instrument, named by CELEX)

Designed to feed both the workbook and the planned public website.

## Instrument level
- `celex`, `name`, `proposal`, `impact_assessment`
- `evidence_rating` — short label (e.g. "early and thin")
- `summary` — 2–3 sentence plain-language summary for the instrument page
- `last_reviewed` — date the evidence was last checked (YYYY-MM-DD)
- `indicators[]` — promises from the proposal (see below)
- `literature[]` — sources (see below)

## Indicator (promise) fields
`type`, `objective`, `indicator`, `target_or_baseline`, `evidence`, `status`
(measured / partially measured / reported as activity / mixed evidence / not measured), `sources`

## Literature (source) fields
- `id` — stable slug used for cross-references and page anchors
- `citation` — full reference; `authors`, `year`, `title`, `venue` (split out for display and sorting)
- `source_type`, `method`, `outcomes`, `direction`, `headline`, `period_geography`, `quality`
- `summary_plain` — 1–2 sentence plain-language summary for the website
- `url` — canonical link (DOI or publisher/official page); `pdf_url` where an open PDF exists
- `access` — open / abstract only / paywalled
- `archive_url` — existing Internet Archive snapshot, if any (checked read-only; nothing is submitted to the archive)
- `verified` — full text / abstract / search summary; `accessed` — date the source was checked
- `interested_party` — free text when authors or funders have a stake in the outcome, else empty
