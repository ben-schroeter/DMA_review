# Addressee codebook (version 2, October 2026)

Every counted restriction gets two addressee codes and, where relevant, a reason.

## 1. Formal addressee: who the text tells to act
The actor that must do (or refrain from) what the restriction requires, read from the sentence and, if needed, from its context in the same article: the list lead-in, the article heading, the previous sentence, or the act's definitions.

| Code | Includes |
|---|---|
| `private_parties` | undertakings, providers, operators, controllers, platforms, gatekeepers, financial institutions, notified bodies (private conformity assessors), natural and legal persons, users, applicants, beneficiaries of funding |
| `member_states` | Member States and any national public body: competent, supervisory, market-surveillance, data-protection, tax, customs and law-enforcement authorities; national courts; CSIRTs; public-sector bodies; contracting authorities |
| `eu_institutions` | Commission, Council, Parliament, EU agencies and bodies (EBA, ESMA, ENISA, EDPB, AI Office, Europol, AMLA, Joint Undertakings, etc.), the Board/committees set up by the act |
| `no_actor` | rules on content, form or status that bind no identifiable actor even in context: "the register shall be public", "the certificate shall be valid for five years" (if not already excluded), definitions-like provisions |
| `unclear` | an actor must exist but cannot be identified from the sentence, the article or the definitions |

Rules:
- **Passive voice**: "X shall be notified to the authority" binds whoever must notify. Take the agent if stated ("by the provider"); otherwise the actor from the list lead-in, the article heading or the previous sentence of the same paragraph.
- **Documents and content requirements**: "the technical documentation shall contain…", "the application shall include…" bind the producer of the document (who draws up, submits or publishes it), if the article makes that clear. Otherwise `no_actor`.
- **List points (a), (b), …** inherit the actor of the lead-in ("Providers shall: (a) …").
- **Pronouns and "such"**: resolve to the antecedent in the same paragraph or article.
- **Definitions**: an act-specific term takes the class of its definition ("'gatekeeper' means an undertaking…" → private).
- **Ambiguous words**: "institutions" (credit institutions = private; Union institutions = EU); "the Authority" (EBA/ESMA/EIOPA/AMLA = EU; national authority = Member States); "board" (management board of a company = private; the Board/EDPB = EU); "notified body" = private; "public sector body" = Member States.
- **Mixed subjects** ("Member States and the Commission shall…"): code the first-named actor and flag `mixed`.

## 2. Ultimately bound: who carries the burden in practice
Same codes. Differs from the formal addressee only for **duties of result and transposition duties** addressed to Member States or EU bodies whose content is conduct by another actor:
- "Member States shall ensure that providers…" → formal `member_states`, ultimately bound `private_parties`.
- "Member States shall lay down rules on penalties…" → both `member_states` (the duty is on the state).
- "The Commission shall ensure that gatekeepers comply…" → formal `eu_institutions`, ultimately bound `private_parties`.
If the content names no other actor, ultimately bound = formal.

## 3. Provenance
Each code records how it was set: `rule` (deterministic classifier), `model` (second reader), `review` (human adjudication of a disagreement), plus a short reason for anything not set by the rule's direct reading of the subject.
