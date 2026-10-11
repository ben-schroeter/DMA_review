# Brief: independent coding of a validation sample

Read `CODEBOOK.md` in this folder. You will code 200 counted items from EU acts. You see no classifier output: code each item yourself. Fields: `vid` (keep it), `doc` (CELEX), `article`, `heading`, `chapeau` (list lead-in), `before` (preceding text of the same article), `clause`, `marker` (the word that made it count), `category`.

For each item give:
- `is_restriction`: true if the marker creates a genuine legal restriction (requires, forbids or limits conduct) per the project definition: obligations (shall/must), prohibitions, restricted permissions (may only), duties of result (shall ensure), explicit requirements. False for exemptions, permissions, legal effects, definitions, entry into force, saving clauses, objectives, titles, amendment instructions.
- `formal`: private_parties | member_states | eu_institutions | no_actor | unclear (codebook section 1)
- `ultimately_bound`: same codes (codebook section 2)
- `confidence`: high | medium | low
- `reason`: one short sentence

You may open the act with curl (https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:<doc>) where context is insufficient; never use third-party reader services. Judge each item individually; do not code by keyword script.
Write a JSON list `[{"vid":..,"is_restriction":..,"formal":..,"ultimately_bound":..,"confidence":..,"reason":..}]` to the output path given. Do not edit other files.
