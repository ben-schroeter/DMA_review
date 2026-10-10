"""Filter based_on links to implementing/delegated acts and guidance."""
import json, re, collections, csv
raw = json.load(open("../data/based_on_raw.json"))
ACT = {"REG_IMPL": "implementing", "DEC_IMPL": "implementing", "DIR_IMPL": "implementing",
       "REG_DEL": "delegated", "DIR_DEL": "delegated", "DEC_DEL": "delegated",
       "REG": "other Commission/Council act", "DIR": "other Commission/Council act"}
GUIDE = {"COMMUNIC", "GUIDELINE", "GUIDELINE_GEN", "RECO"}
GUIDE_TITLE = re.compile(r"guidance|guideline|interpretation|questions and answers|\bQ&A\b|frequently asked|"
                         r"application of (article|the)|clarif|best practice|recommendation", re.I)
NOT_GUIDE = re.compile(r"prior notification|non-opposition|notified concentration|invitation to|call for|"
                       r"information communicated by|publication of|list of|withdrawal of|corrigendum|summary of commission decision|"
                       r"opinion of the advisory|framework of the implementation|report on|in accordance with article 395", re.I)
out, seen = [], set()
for r in raw:
    t, sector = r["type"], r["celex"][0]
    kind = None
    if sector == "3" and t in ACT:
        kind = ACT[t]
    elif t in ("GUIDELINE", "GUIDELINE_GEN", "RECO") and sector in "35":
        kind = "guidance"
    elif t == "COMMUNIC" and sector in "35" and GUIDE_TITLE.search(r["title"]) and not NOT_GUIDE.search(r["title"]):
        kind = "guidance"
    elif t == "NOTICE" and sector in "35" and GUIDE_TITLE.search(r["title"]) and not NOT_GUIDE.search(r["title"]):
        kind = "guidance"
    if kind == "guidance" and re.match(r"5\d{4}(IP|Y)|3\d{4}Y", r["celex"]):
        kind = None                                  # Parliament / ESRB recommendations: not Commission guidance
    if kind and (r["parent"], r["celex"]) not in seen:
        seen.add((r["parent"], r["celex"]))
        individual = bool(re.search(r"authoris|derogat|on the adequate protection|in respect of (the )?(Kingdom|Republic|Grand Duchy|"
                                    r"Hungary|Romania|Ireland|Malta|Cyprus|Portugal|Italy|France|Germany|Poland|Estonia|Latvia|"
                                    r"Lithuania|Croatia|Slovenia|Slovakia|Czech|Austria|Belgium|Bulgaria|Finland|Sweden|Denmark|"
                                    r"Greece|Spain|Netherlands|Luxembourg)", r["title"]) and t == "DEC_IMPL")
        out.append({**r, "kind": kind, "addressed_to_specific_state_or_party": individual})
json.dump(out, open("../data/secondary_acts.json", "w"), indent=1)
print(len(out), collections.Counter(o["kind"] for o in out))
print("individual DEC_IMPL:", sum(o["addressed_to_specific_state_or_party"] for o in out))
c = collections.Counter(o["parent"] for o in out)
print(c.most_common(15))
