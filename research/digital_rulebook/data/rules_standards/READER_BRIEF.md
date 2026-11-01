# Brief: second reader, rules vs standards

1. Read `data/rules_standards/CODEBOOK.md` (in research/digital_rulebook) carefully. It defines the codes R, S, M, L, D, N and the decision rules.
2. Your input batch is a JSON list of obligations from EU digital laws and their implementing/delegated acts. Fields: `k` (id, keep it),
   `doc` (CELEX), `art`, `chapeau` (list lead-in, may be empty), `clause` (the sentence that carries the obligation).
3. **Read every item yourself and decide its code from its wording, applying the codebook.** Do not write keyword or regex scripts
   to assign codes, and do not default items you have not read: the point of this pass is human-like reading, because the
   word-list classifier is only 82% right. Work through the batch in chunks (e.g. 50 at a time) so you read each clause.
   You may use a small script only to load the input and to write your output file.
4. Write a JSON list to the output path you are given: one object per input item, `{"k": "...", "c": "R|S|M|L|D|N"}`, same order,
   every `k` exactly once.
5. Do not edit any other file, do not commit, do not use the network.
6. Reply only with: the output path, the number of items, and counts by code.
