"""Rules vs standards: fresh validation sample of 200 distinct clauses (130 main, 70 implementing/delegated), excluding the pilot.
Writes data/rules_standards/validation_sample.json. Run from research/digital_rulebook."""
import json, random, hashlib, glob
random.seed(557)
key = lambda x: hashlib.sha1(((x["chapeau"] or "")[-200:] + "|" + x["clause"]).encode()).hexdigest()[:12]
pilot = {key(json.loads(l)) for l in open("data/rules_standards/pilot_sample.jsonl")}
inst = [json.loads(l) for l in open("data/rules_standards/instances.jsonl")]
srcs = {}
for x in inst:
    srcs.setdefault(x["key"], set()).add(x["src"])
U = {u["k"]: u for b in sorted(glob.glob("data/rules_standards/batches/b??.json")) for u in json.load(open(b))}
main = [k for k in U if "main" in srcs[k] and k not in pilot]; sec = [k for k in U if srcs[k] == {"secondary"} and k not in pilot]
pick = random.sample(main, 130) + random.sample(sec, 70)
json.dump([dict(U[k], n=i, src="main" if i < 130 else "secondary") for i, k in enumerate(pick)], open("data/rules_standards/validation_sample.json", "w"), ensure_ascii=False)
print(len(pick))
