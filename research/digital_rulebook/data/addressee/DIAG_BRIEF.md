# Brief: code 100 "unclear" restrictions

Read `CODEBOOK.md` in this folder first. Each item in your input file is one restriction that the rule-based classifier could not assign. Fields: `doc` (CELEX), `article`, `heading` (article title), `chapeau` (list lead-in, if any), `before` (up to 700 characters of the same article before this clause), `clause`, `marker` (the word(s) that made it count: shall, must, shall ensure…), `category`, `subject` (what the parser took as the subject).

For each item decide, using only the text given (you may open the act on EUR-Lex with curl if the context is truly insufficient: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:<doc>; do not use any third-party reader service):

- `formal`: private_parties | member_states | eu_institutions | no_actor | unclear
- `ultimately_bound`: same codes (differs only for duties of result/transposition duties, see codebook)
- `cause`: the main reason the classifier failed, one of:
  - `passive_actor_in_context`: passive voice; the actor is named in the lead-in, heading or previous sentence
  - `document_producer`: a document/thing is the subject; its producer is identifiable
  - `list_lead_in`: a list point whose actor is in the lead-in
  - `pronoun_or_ellipsis`: pronoun, "such", or elided subject resolvable from context
  - `term_not_recognised`: the subject names an actor but with a term the keyword lists miss (e.g. "the InvestEU Fund", "the EIC", "the Joint Undertaking", "the issuer's management")
  - `mixed_subject`: several actors of different classes
  - `content_or_status`: no actor even in context (code formal = no_actor)
  - `not_a_restriction`: the counter should not have counted this (say why)
  - `truly_unclear`: an actor must exist but cannot be found
- `where`: where you found the actor: sentence | lead_in | heading | before | definitions | whole_article | none
- `term`: if cause is term_not_recognised or the actor is identified by a specific word, give that word or phrase (e.g. "manufacturer", "white paper offeror", "the InvestEU Fund")
- `confidence`: high | medium | low
- `reason`: one short sentence

Write a JSON list to the output path given in your task, one object per item: `{"sid": ..., "formal": ..., "ultimately_bound": ..., "cause": ..., "where": ..., "term": ..., "confidence": ..., "reason": ...}`. Do not edit other files. Reply with counts by cause and by formal code.
