"""One database: brings the workbook's instruments sheet to the current schema and keeps it in step with the pending
initiatives. Renames legacy columns, drops columns that only described the initial inventory, appends every initiative not
yet adopted (from site/forthcoming_list.json, written by site/build_forthcoming.py) with stable ids kept in
data/initiative_ids.json, and keeps a 'reviews' sheet of guidance and rules under revision (data/reviews.json).
Idempotent: run after site/build_forthcoming.py. Run from research/digital_rulebook."""
import json, os, openpyxl
from openpyxl.styles import Font

WB = "digital_rulebook.xlsx"
wb = openpyxl.load_workbook(WB)
ws = wb["instruments"]
hdr = [c.value for c in ws[1]]
RENAME = {"policy_area_ceps": "policy_area", "status_oct2026": "status"}
for c in ws[1]:
    if c.value in RENAME: c.value = RENAME[c.value]
for name in ("ceps_table_status", "status_ceps_jul2025"):
    hdr = [c.value for c in ws[1]]
    if name in hdr: ws.delete_cols(hdr.index(name) + 1)
TRACK = ["stage_procedure", "parliament_position", "council_position", "trilogues", "agreement", "expected_proposal", "target_for_agreement", "latest_status", "page"]
hdr = [c.value for c in ws[1]]
for t in TRACK:
    if t not in hdr:
        ws.cell(1, len(hdr) + 1, t).font = Font(bold=True); hdr.append(t)
col = {h: i + 1 for i, h in enumerate(hdr)}
pend = json.load(open("site/forthcoming_list.json"))
ids = json.load(open("data/initiative_ids.json")) if os.path.exists("data/initiative_ids.json") else {}
rows = {ws.cell(r, 1).value: r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value is not None}
total_row = next((r for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value is None and ws.cell(r, 2).value), None)
nxt = max([k for k in rows if isinstance(k, int)] + list(ids.values()) + [0]) + 1
for p in pend:
    lid = p.get("law_id") or ids.get(p["id"])
    if not lid:
        lid = nxt; nxt += 1
    if not p.get("law_id"): ids[p["id"]] = lid
    if lid not in rows:
        if total_row:
            ws.insert_rows(total_row); r = total_row; total_row += 1
        else:
            r = ws.max_row + 1
        rows[lid] = r
        ws.cell(r, col["row_id"], lid); ws.cell(r, col["name"], p["name"]); ws.cell(r, col["identifier"], p["procedure"])
        ws.cell(r, col["policy_area"], p["policy_area"]); ws.cell(r, col["proposal_date"], p["proposal"] or None)
    r = rows[lid]
    ws.cell(r, col["status"], p["stage"])
    for k, v in (("stage_procedure", p["procedure"]), ("parliament_position", p["parliament_position"]), ("council_position", p["council_position"]),
                 ("trilogues", p["trilogues"]), ("agreement", p["agreement"]), ("expected_proposal", p["expected_proposal"]),
                 ("target_for_agreement", p["target_for_agreement"]), ("latest_status", p["latest"]), ("page", p["page"])):
        ws.cell(r, col[k], v if v not in (None, "—") else None)
json.dump(ids, open("data/initiative_ids.json", "w"), indent=1)
if "forthcoming" in wb.sheetnames: del wb["forthcoming"]
rev = json.load(open("data/reviews.json")) if os.path.exists("data/reviews.json") else []
if "reviews" in wb.sheetnames: del wb["reviews"]
wr = wb.create_sheet("reviews", 1)
cols = ["law_id", "law", "item", "kind", "status", "last_step", "next_step", "source_url", "checked"]
wr.append(cols)
for x in rev: wr.append([x.get(c) for c in cols])
for c in wr[1]: c.font = Font(bold=True)
wb.save(WB)
import collections
print(collections.Counter(ws.cell(r, col["status"]).value for r in rows.values()), "rows", len(rows), "reviews", len(rev))
