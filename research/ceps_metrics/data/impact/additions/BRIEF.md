# Brief: find more empirical impact studies for recent EU digital acts

You are extending an evidence review of EU digital laws. For each act in your todo file, find **empirical ex-post studies of the act's effects** that are NOT already in the `existing` list for that act.

## What counts (include)
- Studies that measure what actually happened after the act was adopted or started to apply: effects on firms (entry, exit, investment, revenue, compliance costs, employment), consumers (prices, choice, usage, privacy outcomes), innovation (patents, VC funding, product launches, apps), markets (concentration, competition, trade), public bodies, or the act's own targets.
- Any rigorous method: difference-in-differences, event studies, synthetic control, regression discontinuity, panel regressions, structural estimation on post-adoption data, large surveys with quantified results, measurement studies (web crawls, app-store scrapes, audits of compliance with numbers), official ex-post evaluations, audits (European Court of Auditors), statistical monitoring reports with data (Eurostat, ENISA, ESMA, EBA, ECB, BEREC, national regulators), OECD/IMF/BIS/JRC empirical papers.
- Working papers count (NBER, CEPR, SSRN, arXiv, IZA, CESifo, ZEW, Bruegel, IDEAS/RePEc, university series), as do peer-reviewed articles and conference papers (e.g. ACM, USENIX, PETS, WWW for GDPR/DSA/DMA measurement studies).
- For acts that apply only since 2024–26, early measurement counts (e.g. compliance crawls, transparency-database analyses for the DSA, early market data for MiCA, survey data on AI Act readiness with numbers). Also studies of closely matched predecessor provisions only if they directly concern the act (say so in `quality`).

## What does not count (exclude)
- Opinion pieces, blog posts without data, purely legal analysis, ex-ante simulations or forecasts (including impact assessments), lobbying position papers without data, enforcement decisions and court rulings, press releases.
- Studies already in the act's `existing` list (check authors/title; same paper in a new version = duplicate).

## Search broadly
Use WebSearch (several queries per act: the act's name and acronym, "impact", "effect", "evidence", "difference-in-differences", "empirical", "evaluation", sector-specific terms, plus Google Scholar-style phrasings) and WebFetch to open abstract pages. Try SSRN, NBER, CEPR, arXiv, RePEc/IDEAS, ScienceDirect, Springer, Wiley, JSTOR abstracts, EUR-Lex for evaluation SWDs and Commission reports on application, ECA special reports, JRC repository, agency reports. Spend proportionally more effort on acts likely to have literature (big, older, or high-profile ones), but do try every act. It is fine to find nothing for some acts: report that.

## Verification rules (strict)
- Only include a study if you opened its page (abstract page, PDF or official landing page) and confirmed title, authors, year and the headline finding. Never cite from memory. Never invent numbers.
- `verified`: "full text read" only if you read the paper's results; "abstract read" if only the abstract/landing page; "summary only" if only a secondary source described it (avoid where possible).
- `url` must be the page you opened (DOI or official page preferred).
- Flag interested parties (industry associations, firms subject to the act, NGOs campaigning on it, the Commission evaluating itself) in `interested_party` (short text, empty if none).

## Output
Write a JSON file at the path given in your task: a list of objects, one per new study, with exactly these keys:
```
celex, id (short slug: firstauthor-year-keyword), authors, year (int), title, venue, url, pdf_url (or ""),
source_type (e.g. "academic working paper", "peer-reviewed article", "Commission evaluation", "ECA special report", "agency report", "OECD report", "conference paper", "survey report"),
method (be specific; name the design, e.g. "difference-in-differences on firm panel", "event study", "synthetic control", "web measurement study", "survey of 1,200 firms", "descriptive statistics"),
outcomes (short), direction ("positive" | "negative" | "mixed" | "no effect" | "descriptive"),
headline (one sentence with the key number), summary_plain (one or two plain-English sentences for a general reader, no jargon),
period_geography, quality (one short line: design strength, caveats), verified, access ("open" | "paywalled"), interested_party
```
Also include one extra object per act where you found nothing: `{"celex": "...", "none_found": true, "searched": "short note of what you searched"}`.

When done, reply with a short summary: per act, number of new studies (and how many causal designs), plus anything notable.

## Addendum (2026-10-10): think tank pieces
Also search think tanks and policy institutes for pieces assessing the act's effects since adoption, for example Bruegel, CEPS, CERRE, ECIPE, CEP (Centrum für Europäische Politik), Kiel Institute, ifo, ZEW policy briefs, DIW, IW Köln, Centre for European Reform, Lisbon Council, EPC, Jacques Delors Institute, Breughel-style national institutes, ITIF, Brookings, PIIE, CSIS, Ada Lovelace Institute, AlgorithmWatch, Future of Life Institute, Stiftung Neue Verantwortung / interface, Mercatus, Copenhagen Economics or Oxera studies.
- Include them if they assess what has happened under the act (with data, case evidence or a structured qualitative assessment). Exclude pure opinion on the proposal or forecasts.
- Add a key `source_class` to EVERY object you output (including academic ones already found): "academic" (peer-reviewed or university/research-institute working paper), "official" (EU institutions, agencies, national authorities, OECD/IMF/BIS), "think tank" (independent policy institutes and NGOs' research), or "consultancy or industry" (consultancies, trade associations, companies). Set `source_type` for think tank pieces to "think tank report" or "think tank policy brief".
- Fill `interested_party` for think tanks with known funders or positions on the act where clear (e.g. industry-funded, campaigning NGO).
