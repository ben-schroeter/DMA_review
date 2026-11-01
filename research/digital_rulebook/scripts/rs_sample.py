"""Rules vs standards (Kaplow 1992), pilot: draw 200 obligations (130 from the 105 adopted main acts, 70 from their implementing and
delegated acts), stratified by policy area for main acts. Writes data/rules_standards/pilot_sample.jsonl. Run from research/digital_rulebook."""
import json, random, collections, openpyxl
random.seed(1992)
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
ad = {str(r[h.index("celex_measured")]): dict(zip(h, r)) for r in rows[1:] if r[0] and r[h.index("status")] == "adopted"
      and r[h.index("restrictions_total")] is not None}
main = [json.loads(l) for l in open("data/addressee/instances_main.jsonl")]
fin = [json.loads(l) for l in open("data/addressee/v2_final_main.jsonl")]
M = [dict(x, rid=i, addressee_v2=f["formal"], src="main", act=ad[x["doc"]]["name"], area=ad[x["doc"]]["policy_area"])
     for i, (x, f) in enumerate(zip(main, fin)) if x["doc"] in ad and not f["model_not_a_restriction"]]
sec = [json.loads(l) for l in open("data/addressee/instances_secondary.jsonl")]
sv2 = [json.loads(l) for l in open("data/addressee/v2_secondary.jsonl")]
S = [dict(x, rid=i, addressee_v2=f["formal"], src="secondary", act=x["doc"], area="") for i, (x, f) in enumerate(zip(sec, sv2))]
by = collections.defaultdict(list)
for x in M:
    by[x["area"]].append(x)
tot = len(M); pick = []
for a, xs in sorted(by.items()):
    pick += random.sample(xs, max(2, round(130 * len(xs) / tot)))
pick = random.sample(pick, 130) if len(pick) > 130 else pick + random.sample([x for x in M if x not in pick], 130 - len(pick))
pick += random.sample(S, 70)
keep = ("src", "rid", "doc", "act", "area", "article", "chapeau", "clause", "marker", "category", "addressee_v2")
with open("data/rules_standards/pilot_sample.jsonl", "w") as f:
    for n, x in enumerate(pick):
        f.write(json.dumps({"n": n, **{k: x.get(k) for k in keep}}, ensure_ascii=False) + "\n")
print(len(M), len(S), len(pick), collections.Counter(x["area"] for x in pick[:130]))
