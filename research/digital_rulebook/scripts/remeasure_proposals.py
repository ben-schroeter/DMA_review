"""Re-measure the linked Commission proposals with the current counter, reusing the stored links in data/proposals.json."""
import json, sys, multiprocessing as mp
sys.path.insert(0, ".")
from proposals import work

if __name__ == "__main__":
    P = json.load(open("../data/proposals.json"))
    pcs = sorted(P["measurements"])
    with mp.Pool(4) as pool:
        res = {r["celex"]: r for r in pool.map(work, pcs)}
    P["measurements"] = res
    json.dump(P, open("../data/proposals.json", "w"), indent=1)
    print(len(res), "proposals; errors:", [k for k, v in res.items() if v.get("error")])
