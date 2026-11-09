"""Rules/standards codes (Kaplow) for every obligation, on the same base as the regulatory design grid (Coglianese):
an obligation the grid reader coded N (not a duty) is N here too, so both measures count the same duties.
Kaplow codes: data/rules_standards/batches/*_coded.json; grid codes: data/rules_standards/grid/*_coded.json."""
import glob, json


def load(harmonise=True):
    codes = {}
    for f in sorted(glob.glob("data/rules_standards/batches/*_coded.json")):
        for o in json.load(open(f)):
            codes[o["k"]] = o["c"]
    if harmonise:
        for f in sorted(glob.glob("data/rules_standards/grid/*_coded.json")):
            if "pilot" in f:
                continue
            for o in json.load(open(f)):
                if o["c"] == "N" and o["k"] in codes:
                    codes[o["k"]] = "N"
    return codes
