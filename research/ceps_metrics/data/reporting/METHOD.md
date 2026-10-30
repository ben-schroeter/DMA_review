# Reporting obligations: method

**What counts.** A reporting obligation is one of the obligations already counted (`scripts/restrictions.py`) whose required action is to pass information to someone else, or to create or keep it for others to inspect. Every reporting obligation is therefore also one of the obligations in the main count.

**Corpus.** Adopted acts (laws) and their implementing and delegated acts, as stored sentence by sentence by `scripts/addr_dump.py` (`data/addressee/instances_main.jsonl`, `instances_secondary.jsonl`). Obligations that the addressee second reader marked as not being obligations at all are excluded, as in the published counts. The base is 31,649 obligations; the laws differ from the published 21,374 by 25 (0.1%), the result of small re-measurement differences in a few documents.

**Types** (by the action required):
- `report_submission`: report, submit, transmit, communicate, send or provide information or documents
- `notification`: notify or inform someone of something
- `on_request`: supply information when asked
- `disclosure`: publish, make public or accessible, or inform users, consumers, data subjects or the public
- `registration`: register, or enter information in a register, database or system
- `record_keeping`: keep, retain or store records, logs, documentation or copies; document; keep at the disposal of authorities

**Also recorded:** who must act (the existing addressee coding: companies, member states, EU institutions); the recipient (Commission, EU body, European Parliament and Council, national authority, public or users, other businesses); the cadence (periodic with its period, one-off, event-driven with any deadline in hours, on request, ongoing, or not stated in the sentence); and whether an EU-institution report is a review of the act itself.

**Not counted:** sentences that only specify a report's content or format ("The report shall include …", "Dates shall be reported in UTC"); bans on disclosure (confidentiality); internal reporting to a company's own management body, board or general meeting; transposition boilerplate ("adopt and publish the laws … necessary to comply").

**How.** Rules in `scripts/reporting.py` look for a reporting verb as the main verb of the obligation (after skipping adverbials and insertions, handling passives, "be able to", coordinated verbs and "shall ensure that X notifies …"), then assign type, recipient and cadence. `scripts/reporting_summary.py` writes `summary.json`.

**Accuracy.** Rules were developed on a first sample of 300 obligations. They were then checked on samples not used for tuning: 197 of 210 obligations classified as reporting were genuine (precision 94%), and 4 of 100 obligations classified as not reporting were in fact reporting obligations. That implies the count captures about 83% of reporting obligations; the true total is likely about 6,200 rather than 5,484. The cadence of many obligations is not stated in the sentence itself (it is set elsewhere in the act, in an implementing act or by the authority), so "not stated" is a large category. See `validation_results.json` and the three `validation_*items.json` files.

**Caveat.** These are obligations in the texts, not reports filed: one annual duty that applies to 10,000 companies produces 10,000 reports a year.
