# CEPS instruments: size, restrictions and secondary acts — method

## Scope
- Rows: the 115 instruments in `data/ceps_instruments.csv` (CEPS Table 1, July 2025, plus 8 enacted instruments added from the same table).
- Text measured per row: the original act as published in the Official Journal; for instruments still pending in October 2026, the Commission proposal (COM document). Four pending items were adopted after the CEPS snapshot and are measured on the adopted act (ViDA 2025/516, compulsory licensing 2025/2645, GDPR procedural 2025/2518, toy safety 2025/2509). PSR and PSD3 were to be measured on the Council final compromise texts of 23 April 2026, but the Council register is blocked in this environment, so they are not measured.
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

## National transposition (directives only)
Number of national implementing measures linked to the directive in EUR-Lex, and the number of Member States (including the UK before 2020) with at least one. Counts reflect what Member States notified; some notify whole codes, which inflates counts.

## Validation
Hand-coded by Claude (not an independent coder) on a random sample drawn across eras and act types:
- Tuning sample: 100 counted instances, used to refine exclusions and word lists.
- Held-out sample: 91 counted instances.
- Recall check: 100 clauses the counter did not count that contain modal-like words.
- Final check: a fresh sample of 100 instances drawn after the full run, scored with the final rules.
Results are in the `validation` sheet. Treat restriction counts as approximate; addressee shares are less reliable than totals.

## Caveats
- This counts obligations, not their cost.
- Member-State obligations in directives are indirect; the real burden depends on transposition.
- EUR-Lex metadata links for very recent acts can lag; secondary-act lists may be incomplete for 2025–2026.
- Scanned older acts with little HTML text are flagged in the note column.
