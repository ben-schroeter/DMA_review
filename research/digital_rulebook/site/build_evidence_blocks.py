"""'Do the rules work?' page: the objectives bar with its legend, and the strength-of-evidence bars, built from the
workbook so no count is typed into the page. Same definitions as site/facts.py (objectives: key results in the
proposal_indicators sheet for adopted laws; strength: impact_evidence_level of each adopted law).
Writes site/evidence_objectives_table.html and site/evidence_levels_table.html, filled in by site/assemble.py.
Run from research/digital_rulebook."""
import collections, openpyxl

wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
def sheet(n):
    r = list(wb[n].iter_rows(values_only=True)); return [dict(zip(r[0], x)) for x in r[1:] if any(v is not None for v in x)]
A = [x for x in sheet("instruments") if x["row_id"] and x["status"] == "adopted"]; Aid = {x["row_id"] for x in A}
sg = collections.Counter(p["status_group"] for p in sheet("proposal_indicators") if p["indicator / promised impact"] and p["parent_row_id"] in Aid)

OBJ = [("measured", "Measured", "#282424"), ("partially measured", "Partly measured", "#666262"), ("mixed evidence", "Mixed evidence", "#A6A3A0"),
       ("reported as activity", "Activity only", "#D4D2CE"), ("not measured", "Never measured", "#B8860B")]
aria = ", ".join(f"{lab.lower()} {sg[k]}" for k, lab, _ in OBJ)
bar = "".join(f'<div style="flex: {sg[k]}; background: {c}"></div>' for k, _, c in OBJ)
leg = "".join(f'<span style="display: inline-flex; align-items: center; gap: 8px' + ('; color: #282424; font-weight: 500' if k == "not measured" else "")
              + f'"><span style="width: 10px; height: 10px; border-radius: 2px; background: {c}"></span>{lab} {sg[k]}</span>' for k, lab, c in OBJ)
open("site/evidence_objectives_table.html", "w").write(
    f'<div style="display: flex; flex-direction: column; gap: 14px"><div style="display: flex; height: 40px; border-radius: 6px; overflow: hidden; gap: 2px" role="img" aria-label="{aria[0].upper() + aria[1:]}">{bar}</div>'
    f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px 20px" class="cap">{leg}</div></div>')

lv = collections.Counter(x["impact_evidence_level"] for x in A)
LV = [("strong", "Strong", "#B8860B"), ("moderate", "Moderate", "#B8860B"), ("thin", "Thin", "#A6A3A0"), ("ex-ante only", "Too early to tell", "#D4D2CE"), ("none", "None", "#D4D2CE")]
mx = max(lv[k] for k, _, _ in LV) or 1
rows = "".join(f'<div class="lv"><span>{lab}</span><div style="height: 14px; width: {100 * lv[k] / mx:.1f}%; background: {c}; border-radius: 0 4px 4px 0"></div>'
               f'<span style="text-align: right">{lv[k]}</span></div>' for k, lab, c in LV)
open("site/evidence_levels_table.html", "w").write(f'<div style="display: flex; flex-direction: column; gap: 14px">{rows}</div>')
print("objectives", dict(sg), "levels", {k: lv[k] for k, _, _ in LV})
