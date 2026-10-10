"""Map each row to its CEPS Table 1 column (policy area) and colour status, from extracted cell positions."""
import csv, json, re
AREAS = {33: "Research & Innovation", 240: "Industrial Policy", 447: "Connectivity", 654: "Data & Privacy", 861: "IPR",
         1069: "Cybersecurity", 1276: "Law Enforcement", 1483: "Trust & Safety", 1690: "E-commerce & Consumer Protection",
         1897: "Competition & Single Market", 2104: "Media", 2311: "Finance"}
cells = []
for line in open("../data/ceps_table1_cells.txt"):
    m = re.match(r"\s*(\d+)\s+\d+\s+(ENACTED|PROPOSAL|PLANNED) \| (.*)", line)
    if m:
        cells.append((AREAS[int(m.group(1))], m.group(2).lower(), m.group(3)))


def keys(s):
    out = set()
    for a, b in re.findall(r"(?<![\d(])(\d{1,4})/(\d{1,4})(?!\d)", re.sub(r"\d{4}/\d{4}\((COD|CNS|NLE)\)", "", s)):
        a, b = int(a), int(b)
        if a < 100 and not 1950 <= b <= 2030: a += 1900
        out.add(frozenset((a, b)))
    return out

res = {}
for r in csv.DictReader(open("../data/ceps_instruments.csv")):
    ident = r["identifier"]
    hit = None
    proc = re.match(r"\d{4}/\d{4}\((COD|CNS)\)", ident)
    for area, st, text in cells:
        if proc and ident in text.replace(" ", ""):
            hit = (area, st); break
        if not proc and keys(ident) & keys(text):
            hit = (area, st); break
    if hit is None and "Space Act" in r["name"]:
        hit = next((a, s) for a, s, t in cells if t.startswith("EU Space Act"))
    st = hit[1] if hit else None
    if st == "enacted" and r["status"] == "proposed":
        st = "proposal (listed in the cell of its enacted predecessor)"
    res[r["name"]] = {"policy_area": hit[0] if hit else None, "ceps_colour_status": st}
json.dump(res, open("../data/policy_area.json", "w"), indent=1)
miss = [k for k, v in res.items() if not v["policy_area"]]
print(len(res), "missing:", miss)
import collections; print(collections.Counter(v["policy_area"] for v in res.values()))
