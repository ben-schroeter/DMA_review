# Proposal: a second coding axis for obligations ("what is fixed")

Status: proposal, not applied. Written 6 November 2026 after a review of the rules/standards classifier.

## Problem

The current codebook (data/rules_standards/CODEBOOK.md) follows Kaplow: an obligation is a rule (R) if what complies is
knowable before acting. A duty to achieve a precisely defined result ("the payee receives the full amount", "toys shall not
contain substance X", "machinery shall be designed so that it cannot start while someone is in the danger zone") passes that
test and is coded R, even though the firm chooses how to get there. For a reader interested in how much freedom firms have,
such duties look more like standards. A second issue: some provisions coded R are not conduct duties at all (scope clauses,
presumptions, time limits, procedural rules), and should be N.

## Pilot evidence (6 November 2026)

- Hand reading of 60 randomly drawn R-coded obligations on companies (main acts): 45 prescribe an action, content, format or
  ban (75%); 4 fix only an outcome (7%); 2 require a process or plan whose content the firm designs (3%); 9 are not conduct
  duties and should be N (15%). Small sample: 95% intervals roughly 2-16% (outcome) and 7-27% (not duties).
- Wording scan of all R-coded company obligations (4,991): 9% use outcome wording ("shall ensure", "so that", "designed and
  constructed", "shall not contain/exceed", "prevent"); about 1% use process wording ("establish … procedures/policy/system").
- "Shall ensure" duties are coded R 53% of the time (all addressees), against 74% for plain obligations.

Rough effect on company obligations if applied: rules that prescribe the means about 61%, outcome rules about 7%, the rest
standards, mixed, specified later or left to member states (now: 72% rules). To be confirmed by the pilot below.

## Proposed codes (axis 2, coded for every item that is not N)

| Code | Meaning | Examples |
|---|---|---|
| A | **Action or content prescribed.** The provision names what to do, include, file, keep, publish, charge, or a specific act banned. | "Roaming providers shall charge … per kilobyte." "The white paper shall contain the following information:" "shall not present advertisements based on profiling …" |
| O | **Outcome prescribed, means open.** The provision names a result or state the firm must bring about, without saying how. | "shall ensure that the payee receives the full amount" "Toys shall not contain …" "designed so that starting is prevented while someone is in the danger zone" |
| P | **Process or management system.** The firm must set up and run a plan, policy, procedure, risk assessment or control system whose content it designs. | "shall establish … a clear and detailed strategy for …" "shall implement a risk-management system" |

Axis 1 (R/S/M/L/D/N) stays as it is. Combined categories for reporting:

- Prescriptive rule: R × A
- Outcome rule: R × O (bright-line result, free choice of means)
- Management-based duty: any × P
- Standard: S (any axis-2 value; usually O, e.g. "ensure an appropriate level of security")
- Mixed, specified later, left to member states: M, L, D as now

"Means left to the firm" = outcome rules + management-based duties + standards. This keeps the Kaplow measure comparable with
earlier results and with the US benchmark, and adds the means/outcome distinction from the regulatory design literature
(prescriptive vs performance-based vs management-based regulation; Coglianese, Nash and Olmstead 2003; May 2011).

## Decision rules (draft)

1. Code the core duty, as on axis 1. A specified action whose purpose is stated ("in order to ensure …") is A.
2. "Shall ensure that [someone] does [specified act]" is A when the act is specified; O when the clause names a state of affairs.
3. Product requirements that name a feature ("bears a serial number") are A; those that name a performance or absence of a
   hazard ("does not exceed 85 dB", "shall not contain") are O.
4. Duties to have a plan, policy, procedure or system are P even when the list of its elements is fixed; the elements themselves,
   if coded as separate items, follow rules 1-3.
5. Information duties (inform, notify, report, publish, keep records) are A.
6. Scope clauses, definitions, presumptions, time limits for authorities, and rules on who may act are N on axis 1 (fix of the
   existing N leakage).

## Plan

1. Pilot: 400 items stratified by axis-1 code, layer (main/secondary) and company type; coded by model readers with this
   codebook (same method as the axis-1 pass: reading, no keyword scripts).
2. Validation: the user hand-codes 100 of the 400; target agreement 85% or better on axis 2, and a check of the N fixes.
3. If the pilot holds, code all items (about 32,700, 43 batches as in the axis-1 pass), re-run rs_* scripts and the charts, and
   add the means/outcome split to the Rules and Company types pages.
