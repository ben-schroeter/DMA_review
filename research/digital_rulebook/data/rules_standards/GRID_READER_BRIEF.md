# Brief: reader, regulatory design grid

1. Read `data/rules_standards/GRID_CODEBOOK.md` (in research/digital_rulebook) carefully. It defines the codes MM, ME, XM, XE,
   L, D, N and the decision rules. Apply rule 1 (is it a duty at all?) first.
2. Your input batch is a JSON list of obligations from EU digital laws and their implementing/delegated acts (or US statutes for
   files named us*). Fields: `k` (id, keep it), `doc` (CELEX or statute), `art`, `chapeau` (list lead-in, may be empty),
   `clause` (the sentence that carries the obligation). Read the clause together with its chapeau.
3. **Read every item yourself and decide its code from its wording, applying the codebook.** Do not write keyword or regex
   scripts to assign codes, and do not default items you have not read. Work through the batch in chunks of about 50 so that
   you read each clause. You may use a small script only to load the input, print chunks, and write your output file.
4. Write a JSON list to the output path you are given: one object per input item, `{"k": "...", "c": "MM|ME|XM|XE|L|D|N"}`,
   same order, every `k` exactly once.
5. Do not edit any other file, do not commit, do not use the network.
6. Reply only with: the output path, the number of items, and counts by code.
