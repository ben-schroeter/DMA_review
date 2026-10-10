# CEPS instruments: size, restrictions and secondary acts — method

## Scope
- Rows: the 115 instruments in `data/ceps_instruments.csv` (CEPS Table 1, July 2025, plus 8 enacted instruments added from the same table).
- Text measured per row: the original act as published in the Official Journal; for instruments still pending in October 2026, the Commission proposal (COM document). Four pending items were adopted after the CEPS snapshot and are measured on the adopted act (ViDA 2025/516, compulsory licensing 2025/2645, GDPR procedural 2025/2518, toy safety 2025/2509). PSR and PSD3 (politically agreed, not yet adopted) are measured on the 2023 Commission proposals, by choice; headline figures for the Council final compromise texts (ST 8221/26 and ST 8222/26, 17 April 2026, published 23 April) are given in the note column for comparison. Council documents use a larger page layout, so their page counts are not comparable with OJ pages.
- Where a row covers two acts (horizontal block exemptions 2023/1066 and 2023/1067), figures are summed.
- English language versions only. Source: EUR-Lex HTML for text, EUR-Lex / Cellar PDF for page counts.

## Pages
- Page count of the official PDF. For COM proposals EUR-Lex serves the document in several parts (main text, annexes); pages are summed across all parts, so they include the explanatory memorandum and the legislative financial statement.

## Words
- Words = tokens of letters/digits (hyphenated words count once).
- Split: preamble (title, citations, recitals), of which recitals (from "Whereas"); articles (enacting terms up to "Done at"); annexes; and for proposals the explanatory memorandum and legislative financial statement, reported separately.
- `words_legal_text` = preamble + articles + annexes (excludes memorandum and financial statement).
- Words in quoted amending text are counted (they are part of the act); footnotes after the signature block are not.

## Restrictions
Counted in articles and annexes only (recitals are not binding). Each marker instance is counted once; a list introduced by one "shall" counts once.

| Category | Markers |
|---|---|
| obligation | shall; must; has to / have to |
| prohibition | shall not; may not; must not; (shall be / is / are) prohibited; "no X shall" |
| restricted_permission | may only; shall only; may … only if/where/when/to the extent |
| duty_of_result | shall ensure (tagged separately: one instance can stand for a whole compliance system) |
| explicit_requirement | is/are required (to); mandatory; obliged to; an obligation to; requirement to — counted only in clauses with no other marker |

Excluded uses of "shall" (they regulate no one):
- entry into force, application, binding-ness, expiry ("shall enter into force", "shall apply", "shall be binding", "shall take effect")
- definitions and legal fictions ("shall mean", "shall be deemed / considered / construed / presumed"; "shall include / comprise" in definitions)
- amendment instructions ("is replaced by", "shall be amended as follows"); quoted text inserted by amendment instructions is skipped
- saving clauses ("shall be without prejudice", "shall not affect / prejudice / apply / preclude")
- rights, entitlements and powers ("shall have the right", "shall be entitled", "shall be empowered")
- constitutive rules, added after validation: "shall be calculated / determined in accordance with / apportioned / allocated / composed / chaired / financed / eligible / valid", "shall have jurisdiction", "shall be liable", "shall become chargeable", "shall occur", "shall have the equivalent legal effect", time-limit mechanics ("shall be suspended / interrupted / extended by")

Bare nouns such as "the obligations laid down in Article 5" are cross-references and are not counted. This narrows the "requirement(s) / obligation(s)" terms in the original method notes.

### Who the restriction binds
Each counted instance is assigned to one addressee using the grammatical subject (spaCy `en_core_web_sm` dependency parse; the agent of a passive "by …" phrase where one is present), matched against word lists:
- private_parties: providers, operators, manufacturers, undertakings, controllers, gatekeepers, financial entities, platforms, persons, etc.
- member_states: Member States and national authorities, courts, coordinators, single points of contact, CSIRTs
- eu_institutions: Commission, Council, Parliament, agencies, boards, offices, Union entities; also passive sentences about implementing or delegated acts (adopted by the Commission)
- unclear: no identifiable actor (passives with no agent, procedural rules such as "the report shall be communicated")

Pronouns ("it shall") take the addressee of the preceding counted instance in the same document.

## Consolidated versions
Restrictions are also counted in the latest consolidated version in EUR-Lex (CELEX 0…), where one exists. Consolidated texts have no recitals and no official pagination, so only restrictions are reported for them.

## Implementing / delegated acts and guidance
- From the Publications Office's Cellar database: every act linked to the instrument as its legal basis.
- Kept: implementing and delegated acts, other Commission or Council regulations and directives adopted under the act, and Commission guidance (guidelines, Commission recommendations, and Commission notices or communications whose title marks them as guidance or interpretation).
- Excluded: individual decisions (merger clearances, state-aid-style decisions), merger notices and announcements, internal rules of procedure, Parliament or ESRB recommendations, reports.
- Implementing decisions addressed to a single Member State (e.g. VAT derogations) are kept but flagged.
- Each secondary act is measured like the main act and listed as its own line item in `secondary_acts`.
- Guidance is non-binding, so its restriction counts mostly reflect obligations it restates. They are shown for completeness, not as additional restrictions.
- `guidance_web`: Commission guidance found by web search that EUR-Lex does not link to the act (e.g. AI Act guidelines). Not measured. This list is incomplete; level-3 guidance from EU agencies (EDPB, EBA, ESMA, EIOPA) is out of scope.

## Policy area
The column each instrument occupies in CEPS Table 1 (12 areas, from Research & Innovation to Finance), read from the cell positions in the CEPS PDF. `ceps_table_status` is the cell colour (enacted / proposal / planned); pending items that CEPS lists inside the cell of an enacted predecessor (e.g. PSD3 in the PSD2 cell) are labelled accordingly.

## Dates and amendments
- `adoption_date`: date of signature of the act (date of the document where no signature date is recorded); `oj_publication_date`; `entry_into_force`: the earliest entry-into-force date on or after adoption. All from Cellar.
- Amendments: acts recorded in Cellar as amending the instrument (adopted acts only). Corrigenda are listed in the `amendments` sheet but not counted as amendments. `n_amending_acts`, `first_amendment_date`, `latest_amendment_date` summarise them.

## Proposal vs adopted text
- The original Commission proposal is the earliest proposal Cellar links to the adopted act; amended proposals are not used.
- Measured like the adopted text, on the legal text only (preamble + articles + annexes; explanatory memorandum and financial statement excluded). Changes are formulas (absolute and %).
- Proposals without usable HTML (pre-1996 proposals published as scans of the OJ C series, and the 2004 VAT recast whose articles sit in image tables) are measured from the PDF text layer and marked "PDF text (approximate)".
- Not comparable (left blank, with the reason): the VAT recast (its PDF mixes struck-through text and correlation tables), the Community Design Regulation (its 1993 PDF bundles the companion Design Directive proposal) and the Merger Regulation (proposal not in EUR-Lex). Commission-only acts (block exemptions) have no legislative proposal.
- Rows that are themselves proposals have no comparison.

## EU agency guidance (EDPB, EBA, ESMA)
- Final guidelines and recommendations only; no Q&As, consultation drafts or draft technical standards (the latter are counted once adopted as delegated/implementing acts).
- EDPB: every guideline and recommendation in the EDPB document library, reviewed by hand for final status (one 2026 v1 consultation draft excluded); Article 29 Working Party guidelines endorsed by the EDPB are included and flagged. Mapped to GDPR unless the title points to ePrivacy, the Law Enforcement Directive, PSD2 or the DSA. Some endorsed WP29 documents sit on a European Commission archive domain not reachable here and are listed without measurements.
- EBA: all items of type "Guidelines" in the EBA publications listing (plus the topic-filtered listings), kept only where the document names PSD2, MiCA, DORA or the AML Regulation as its legal basis (or in its title); four older PSD2 guidelines missing from the listing were added from the EBA's legacy PSD2 page. The PSD2 complaints-procedure guidelines (EBA/GL/2017/13) could not be retrieved.
- ESMA: all "Guidelines" documents in the Digital Finance and Joint Committee sections of the ESMA library (full crawl), kept where the legal basis is MiCA, DORA or the DLT Pilot Regime, plus the MiCA crypto-asset qualification guidelines from ESMA's MiCA page.
- Joint EBA/ESMA (ESA) guidelines are counted once.
- EBA and ESMA guidelines are measured on the published final report, which also contains the rationale and the feedback on the consultation, so page and word counts overstate the guidelines themselves.
- Guidance mostly uses "should"; restriction counts (which count "shall"/"must" etc.) are low by design. `should_count` is shown alongside.

## National transposition (directives only)
Number of national implementing measures linked to the directive in EUR-Lex, and the number of Member States (including the UK before 2020) with at least one. Counts reflect what Member States notified; some notify whole codes, which inflates counts.

## Validation
Hand-coded by Claude (not an independent coder) on a random sample drawn across eras and act types:
- Tuning sample: 100 counted instances, used to refine exclusions and word lists.
- Held-out sample: 91 counted instances.
- Recall check: 100 clauses the counter did not count that contain modal-like words.
- Final check: a fresh sample of 100 instances drawn after the full run, scored with the final rules.
Results are in the `validation` sheet. Headline (final fresh sample): 84% of counted items are genuine restrictions (roughly ±7 points); the addressee is correct for 74% of those. Remaining false positives are mainly guidance paraphrasing case law ("must be interpreted as"), organisational rules ("the members shall be") and limitation-period mechanics. Most addressee errors are passive sentences with no named actor, which fall into "unclear". Treat restriction counts as approximate; addressee shares are less reliable than totals.

## Caveats
- This counts obligations, not their cost.
- Member-State obligations in directives are indirect; the real burden depends on transposition.
- EUR-Lex metadata links for very recent acts can lag; secondary-act lists may be incomplete for 2025–2026.
- Scanned older acts with little HTML text are flagged in the note column.

## External benchmark: Sarbanes-Oxley Act (US)
- Text: Public Law 107-204 (116 Stat. 745, 30 July 2002), enacted version, PDF from govinfo.gov. Measured with the same counter (`scripts/benchmark_us.py`), after removing page headers, US Code margin notes and the table of contents.
- Two variants: all enacted text, and excluding text inserted into other statutes (quoted ‘‘ … ’’), mirroring how quoted amending text is skipped for EU acts.
- US-specific handling, for the benchmark only: "it shall be unlawful" counts as a prohibition; additional constitutive uses of "shall" are excluded (remain in effect, be available, be treated as, be fined/imprisoned, as it shall determine, term lengths, saving and pre-emption clauses). Addressee groups become private parties, US States, and federal government / regulators (SEC, PCAOB, GAO).
- Validation: 68% precision and 70% addressee accuracy on a fresh 40-item sample (vs 84% / 74% for EU acts), so the benchmarks sheet also shows precision-adjusted counts.
- US statutes have no recitals; compare against EU articles + annexes.

## Impact evidence (all 115 instruments)
- One record per instrument in `data/impact/<CELEX>.json` (schema in `data/impact/SCHEMA.md`), built for both the workbook and the planned website.
- Depth by tier (list in `data/impact/PROGRESS.md`):
  - Tier 1: 29 instruments with a substantial independent literature (e.g. GDPR, DMA, DSA, PSD2, roaming, merger control). Full search.
  - Tier 2: the other acts adopted before 2024. The Commission impact assessment and evaluations, plus a light search for independent studies.
  - Tier 3: acts adopted 2024–26 and pending proposals. Forecasts and early critiques only.
- `proposal_indicators`: the promises made in the original Commission proposal and impact assessment, with the evidence found for each:
  - from the financial statement: specific objectives (1.4.2), expected results and impact (1.4.3), and indicators of results and impact (1.4.4)
  - other quantified promises from the proposal or impact assessment
  - `status` is a free-text label; `status_group` maps it to one of measured, partially measured, reported as activity, mixed evidence or not measured. "Not achieved" counts as measured.
  - proposals with no indicators section carry a "note" row
- `impact_literature`: one row per source. Each row records:
  - type: Commission impact assessment, evaluation or enforcement record; Court of Auditors; peer-reviewed; working paper; policy; industry-funded
  - method; outcomes; direction; headline finding; a plain-language summary; a quality note
  - a flag where the authors or funders have a stake in the result
  - `verified`, saying what was read: the full text, an abstract, or only a search summary
  Each source also has a `category`:
  - ex-ante assessment: the initial Commission impact assessment, or the proposal itself where there was none. Shown with the proposal's promises, not as evidence of impact.
  - enforcement or case law: fines, non-compliance decisions, infringement procedures, enforcement sweeps, designations and court rulings. Kept in the record for reference, but not counted or shown as impact evidence.
  - evidence: everything else (evaluations, audits, research, statistics). Only these count towards `n_impact_studies` and `n_causal_studies`.
  Shared sources (e.g. one impact assessment for PSD3 and the PSR, or a fitness check covering several directives) appear under each instrument with the same `id`.
- Instrument summary columns:
  - `impact_evidence_level`: strong / moderate / thin / ex-ante only / none, derived from the free-text `impact_evidence_rating`
  - `n_indicators_measured`: indicators whose status group is anything other than not measured
  - `n_causal_studies`: sources whose method names a causal design (causal, DiD, event study, synthetic control, regression discontinuity, natural experiment, instrumental variables, randomised)
- Sources:
  - EUR-Lex: proposals, impact assessments and Commission reviews
  - official sources: Commission press releases, the Council register, the Court of Auditors, ENISA, BEREC, ECB, EBA, ESMA, JRC
  - research: NBER, arXiv, Crossref, CERRE, Bruegel, OECD
  - web search for working papers and policy reports
- Several publisher and repository sites (SSRN, CERRE, some Commission PDF endpoints, europarl.europa.eu) block automated access. Those sources were checked through their abstract pages or search summaries and are marked as such.
- Research was carried out by Claude instances working in parallel to a shared brief. Every number in a record comes from a source that was read. Where only a secondary report was available, the record says so.
- Internet Archive snapshots (`archive_url`) were looked up read-only through the Wayback availability API. Nothing was submitted to the archive, so many sources have no snapshot.
- Limits: coverage of non-English national studies is thin. "No study found" means none was found by these searches, not that none exists. Tier 2 and 3 records rely heavily on the Commission's own assessments.
