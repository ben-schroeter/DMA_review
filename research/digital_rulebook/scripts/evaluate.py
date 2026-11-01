"""Score the current counter against the hand labels (tuning set 0-99, held-out 100-190)."""
import json, sys
sys.path.insert(0, "scripts")
from restrictions import find_instances
from addressee import addressee, _LAST
S = json.load(open("data/validation_sample.json"))
L = json.load(open("data/validation_labels.json"))
MAP = {"private_parties": "P", "member_states": "MS", "eu_institutions": "EU", "unclear": "U"}

def score(idx):
    tp = fp = fn = tn = 0; addr_ok = addr_n = 0
    for i in idx:
        x = S["positives"][i]; lab, true_a = L["positives"][str(i)]
        cl = x["clause"]; k = cl.find(x["marker"])
        inst = [t for t in find_instances(cl)[0] if t[1] <= k < t[2] or abs(t[1] - k) < 3]
        counted = bool(inst)
        if counted and lab: tp += 1
        elif counted and not lab: fp += 1
        elif not counted and lab: fn += 1
        else: tn += 1
        if counted and lab:
            _LAST["who"] = None
            a = MAP[addressee(cl, inst[0][1])[0]]
            addr_n += 1; addr_ok += (a == true_a)
    return {"counted_true": tp, "counted_false": fp, "missed_true": fn, "correctly_dropped": tn,
            "precision": round(tp / max(tp + fp, 1), 3), "recall_within_sample": round(tp / max(tp + fn, 1), 3),
            "addressee_accuracy": round(addr_ok / max(addr_n, 1), 3), "addressee_n": addr_n}

res = {"tuning_0_99": score(range(100)), "heldout_100_190": score(range(100, 191))}
neg = L.get("negatives", {})
if neg:
    miss = sum(v[0] for v in neg.values()); res["negatives"] = {"n": len(neg), "true_restrictions_missed": miss}
print(json.dumps(res, indent=1))
json.dump(res, open("data/validation_results.json", "w"), indent=1)
