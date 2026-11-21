# Company responses: method (pilot)

Status: **pilot**, November 2026. 12 companies × 3 EU laws (GDPR, DMA, AI Act) × report years 2016–2026. Figures are not yet used on the site.

## Unit
One **annual report per company-year**. The report year is the calendar year in which the fiscal period ends (Vodafone's year to 31 March 2026 = 2026; Salesforce's year to 31 January 2026 = 2026; Apple's year to 26 September 2026 = 2026). Interim reports are not in the pilot.

## Sample
| Region | Companies | Why |
|---|---|---|
| US (4) | Alphabet, Meta, Apple, Salesforce | three DMA gatekeepers and one large non-gatekeeper platform for contrast |
| EU (4) | Orange, Capgemini (CAC 40); SAP, Deutsche Telekom (DAX) | telecoms, IT services and enterprise software: heavy GDPR exposure and AI Act providers/deployers; DMA business users |
| UK (4) | Vodafone, RELX, WPP, HSBC (FTSE 100) | telecoms, data/analytics, advertising and banking |

Selection was made for the pilot by convenience within these indices (sectors exposed to the three laws, and reports that can be retrieved as text); it is not a random sample. BT and Sage were considered and dropped because their pre-2021 reports could not be retrieved as text from here. Note that the US companies are the main DMA addressees, so DMA results will differ sharply by region by construction.

## Sources (in order of preference)
1. **SEC EDGAR**: 10-K (US) or 20-F (foreign private issuers), the original filing for each period (no amendments). For 20-Fs that place the report in an exhibit (Orange: Registration Document as Exhibit 15.1), the exhibit text is appended.
2. **filings.xbrl.org** ESEF annual financial reports, where a company stopped filing with the SEC (Orange 2024, in French).
3. **Company investor site** PDFs (Capgemini Universal Registration Documents; Deutsche Telekom Annual Reports).

UK note: Companies House holds full annual reports for UK plcs, but the copies served by its Document API are scanned images with no text layer, so they would need OCR. The FCA National Storage Mechanism has text versions but no documented public API was usable from this environment. The four UK companies all file 20-Fs with the SEC, so the 20-F is used; a 20-F for these companies reproduces the annual report's strategic report, risk section and accounts. Using a 20-F rather than the UK annual report is recorded in `reports.json` (`form`).

Gaps are kept in the manifest with `status: "not found"`.

## Finding mentions
Patterns in `law_patterns.json` (English, French and German names, the CELEX-style number, and abbreviations). Abbreviations that are ambiguous (`DMA`) count only in a report that also uses the full name. `GDPR` preceded by "UK" is logged as the **UK GDPR**, not the EU law; the UK Digital Markets, Competition and Consumers Act and non-EU AI laws (Colorado AI Act, Korea AI Basic Act) are logged separately in `uk_mentions.csv` and never counted as EU laws.

A **passage** is the paragraph containing a mention. One row per passage × law in `mentions.csv`.

## Coding (rule-based, checked by hand)
Each passage is coded from the sentence with the mention and its two neighbours:

| Field | Rule |
|---|---|
| `risk_factor` | modal verb + adverse-effect wording, or "risk"/"uncertain" |
| `compliance_cost` | cost, expense, investment, resources, burden |
| `fine_or_provision` | fine, penalty, sanction, provision, accrual, "x% of turnover" |
| `product_change` | change/launch/modify + product/service/feature, choice screens, interoperability, sideloading, consent flows, "less personalised ads" |
| `revenue_impact` | revenue, monetisation, sales, advertising demand |
| `legal_proceedings` | investigation, proceedings, appeal, court, complaint, named regulators (DPC, CNIL) |
| `opportunity` | opportunity, demand for our products, helping clients comply, competitive advantage |
| `amounts` | money amounts in the same sentences |
| `repeated` | passage ≥ 80% similar (5-word shingles) to a passage on the same law in the company's previous report |
| `list_only` | the law appears in one sentence with 3 or more law names |
| `boilerplate` | `repeated`, or `list_only` with no category other than `risk_factor` |
| `quote`, `link` | the sentence with the mention (≤ 320 characters); document link, with `#page=` for PDFs |

Mentions of a law before its adoption (DMA proposal of December 2020, AI Act proposal of April 2021) are counted as mentions of that law.

`company_year.csv` aggregates to one row per company × year × law: whether the law is mentioned, the number of passages and non-boilerplate passages, category counts, law-related amounts and one example quote with its link.

## Validation
`scripts/cr_validate.py draw` draws up to 25 passages per law, stratified by region (fixed seed), for hand-checking: is it really the EU law, which categories apply, is it boilerplate, is the amount law-related. It also probes every report-year with no coded mention (after the law's adoption) for looser wording ("gatekeeper", "EU privacy regulation") to estimate missed mentions. `cr_validate.py score` writes `validation_results.json`.

## Rebuild
```
cd scripts
python3 cr_fetch.py          # downloads to ~/.cache/digital_rulebook/company_reports, writes reports.json
python3 cr_code.py           # mentions.csv, uk_mentions.csv, company_year.csv
python3 cr_validate.py draw  # validation_sample.csv, validation_misses.csv (fill the h_ columns)
python3 cr_validate.py score # validation_results.json
```

## Pilot results (21 November 2026)

**Coverage.** 120 of 132 company-years have a report (`reports.json`). Gaps: FY2026 reports not yet published (9 companies), Orange 2025 (orange.com blocks automated access; not on filings.xbrl.org), Deutsche Telekom 2016 and 2017 (no longer on telekom.com).

**Mentions.** 526 EU-law passages (`mentions.csv`); 23 UK/other-law passages logged separately (`uk_mentions.csv`: UK GDPR 12, UK DMCC Act 9, Colorado/Korea AI laws 2).

| Law | Report-years with a mention (from first mention year) | US | EU | UK |
|---|---|---|---|---|
| GDPR (2016–) | 94 / 120 | 29/42 | 36/37 | 29/41 |
| DMA (2021–) | 26 / 62 | 16/22 | 4/19 | 6/21 |
| AI Act (2021–) | 27 / 62 | 8/22 | 9/19 | 10/21 |

Apple's 10-Ks never name the GDPR (they refer to "privacy, data security and data localization" laws in general). WPP stops naming it after 2019 and RELX after 2022.

**Validation** (`validation_sample.csv`, 75 passages, 25 per law; first-pass hand check by Claude, to be confirmed by the project lead; `validation_results.json`):

- *Is it the EU law?* 75/75 correct (precision 1.0 for all three laws). Recall probe: the 61 report-years with no coded mention were searched for looser wording; 6 had hits, none of them a real mention.
- *Categories (rule-based):* not good enough to publish. Precision / recall: fine_or_provision 0.86 / 0.86, compliance_cost 0.67 / 0.67, product_change 0.60 / 0.33, risk_factor 0.44 / 0.30, legal_proceedings 0.29 / 0.67 (picks up proceedings against *other* companies and court rulings), revenue_impact – / 0.00, opportunity 0.00 / 0.00.
- *Boilerplate:* rule and hand check agree on 51% of passages. "Repeated from last year" is not the same as boilerplate: Meta's GDPR product-change passages and Salesforce's Privacy Collective litigation repeat every year but are company-specific. Generic text is mostly laws named in a list, neutral descriptions of the law in regulatory sections (Orange, Vodafone) and glossary entries.
- *Amounts:* the only amount found in the sample (DMA gatekeeper thresholds, €7.5 billion / €75 billion) is not a company amount. Law-specific amounts are rare in annual reports.
- *Missing categories:* 12 of the 38 non-generic passages (about a third) fit none of the seven categories. 8 are **compliance measures** (Capgemini's Binding Corporate Rules, Deutsche Telekom's AI-ethics working group, Vodafone's GDPR-based global privacy policy, signing the AI Pact). 2 are **scope statements** ("telecoms operators are outside the DMA"), 1 is a GDPR compliance KPI and 1 is policy engagement.

**Recommendations for the full run**
1. Keep the pattern-based detection: it is precise and cheap.
2. Code categories by hand (or with a model checked against hand labels), not with keyword rules. Add the categories `compliance_measure`, `scope_statement` and `description_only`. Narrow `legal_proceedings` to proceedings against the company.
3. Replace the boilerplate rule with two separate fields, `repeated` (computed) and `generic` (coded).
4. Drop the automatic `amounts` field and record amounts by hand. They are rare.
5. Add a fourth UK source with OCR (Companies House) or NSM access, so that the UK sample is not limited to SEC filers.
