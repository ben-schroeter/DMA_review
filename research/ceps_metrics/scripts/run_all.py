"""Measure all main, consolidated and secondary texts. Writes data/measurements.json."""
import csv, json, sys, traceback, multiprocessing as mp
sys.path.insert(0, ".")


def work(arg):
    celex, kind = arg
    from measure import measure
    try:
        if kind == "consolidated":
            r = measure(celex, want_pages=False)
        else:
            r = measure(celex)
        r["kind"] = kind
        return r
    except Exception as e:
        return {"celex": celex, "kind": kind, "error": f"{type(e).__name__}: {str(e)[:150]}"}


if __name__ == "__main__":
    jobs = {}
    for r in csv.DictReader(open("../data/instrument_map.csv")):
        for c in r["celex_measured"].split(";"):
            if c[:1] in "35":
                jobs[(c, "main")] = 1
    for c, v in json.load(open("../data/consolidated.json")).items():
        jobs[(v["latest"], "consolidated")] = 1
    for s in json.load(open("../data/secondary_acts.json")):
        if (s["celex"], "main") not in jobs:
            jobs[(s["celex"], "secondary")] = 1
    todo = list(jobs)
    print(len(todo), "documents", flush=True)
    out = []
    with mp.Pool(4) as pool:
        for i, r in enumerate(pool.imap_unordered(work, todo, chunksize=4)):
            out.append(r)
            if i % 100 == 0:
                print(i, r.get("celex"), r.get("error", ""), flush=True)
    json.dump(out, open("../data/measurements.json", "w"), indent=1)
    print("errors:", sum("error" in r for r in out))
