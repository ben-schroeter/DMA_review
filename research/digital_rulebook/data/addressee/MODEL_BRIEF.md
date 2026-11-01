# Brief: second reader for restrictions the rules could not assign

Read `CODEBOOK.md` in this folder first. Your input file holds restrictions that the rule-based classifier left as `unclear` after looking at the sentence, the list lead-in, the previous sentences and the article heading. Fields: `rid` (keep it), `doc` (CELEX), `article`, `heading`, `chapeau`, `before` (up to 700 characters of the same article before this clause), `clause`, `marker`, `category`.

For each item decide from the text given and your understanding of the act (who the act regulates, who drafts its documents, who runs its procedures). If the context is truly insufficient you may open the act with curl: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:<doc> (use sparingly; never use third-party reader services).

Output one object per item:
`{"rid": ..., "formal": "private_parties|member_states|eu_institutions|no_actor|unclear", "ultimately_bound": "...", "not_a_restriction": true|false, "confidence": "high|medium|low", "reason": "one short sentence naming the actor and where it comes from"}`

- `formal` = who must act (codebook section 1). Product design requirements bind the manufacturer (or the operator for space/vehicles); documents bind whoever draws them up or submits them; procedural steps bind whoever runs the procedure.
- `ultimately_bound` = codebook section 2 (differs only for duties on states/EU bodies whose content is another actor's conduct).
- `not_a_restriction` = true if this should not have been counted at all (exemptions, permissions, saving clauses, programme objectives, titles, legal effects).
- Use `unclear` only if an actor must exist but cannot be identified even with the act in mind.

Write a JSON list to the output path in your task. Do not edit other files. Reply with counts by formal code, by confidence, and the number of not_a_restriction.
