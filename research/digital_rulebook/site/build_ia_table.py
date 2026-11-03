"""Impact assessments behind the adopted laws and pending proposals, by period (Evaluation page table).
Reads data/ia/ia_laws.json (scripts/ia_lookup.py), the workbook and site/forthcoming_list.json. Writes site/ia_table.html
and data/ia/summary.json (used by site/facts.py). Run from research/digital_rulebook."""
import json, collections, openpyxl
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
r = list(wb["instruments"].iter_rows(values_only=True)); h = r[0]
A = {x[h.index("celex_measured")].split(";")[0]: dict(zip(h, x)) for x in r[1:] if x[0] and x[h.index("status")] == "adopted"}
I = json.load(open("data/ia/ia_laws.json"))
P = [f for f in json.load(open("site/forthcoming_list.json")) if f.get("impact_assessment")]
PER = [("2003–2014", 2003, 2014), ("2015–2019", 2015, 2019), ("2020 onwards", 2020, 2100)]
rows, summ = [], {}
for lab, a, b in PER:
    xs = [I[c] for c, l in A.items() if a <= (I[c]["proposal_year"] or int(str(l["adoption_date"])[:4])) <= b and I[c]["status"] in ("full", "none", "swd")]
    n = len(xs); full = sum(x["status"] == "full" for x in xs)
    rows.append((lab + " (adopted laws)", n, full, n - full)); summ[lab] = (n, full)
pf = sum(f["impact_assessment"] == "full" for f in P)
rows.append(("Pending proposals, November 2026", len(P), pf, len(P) - pf))
B = [v["board"] for c, v in I.items() if c in A and v["board"]]
summ.update(board_known=len(B), board_neg_first=sum(b["first"] in ("negative", "revisions requested") for b in B),
            board_neg_twice=sum(b["first"] == "negative" and b["final"] == "negative" for b in B),
            status=collections.Counter(I[c]["status"] for c in A))
json.dump(summ, open("data/ia/summary.json", "w"), indent=1)
TH = 'style="text-align: {a}; font-weight: 600; font-size: 13px; letter-spacing: .04em; text-transform: uppercase; color: #3F3B3B; padding: 8px 12px; border-bottom: 1px solid #D4D2CE; vertical-align: bottom"'
TD = 'style="text-align: {a}; padding: 8px 12px; border-bottom: 1px solid #EFEDE9; font-variant-numeric: tabular-nums"'
html = ('<table style="width: 100%; max-width: 820px; border-collapse: collapse; font-size: 15px; color: #282424"><thead><tr>'
        + "".join(f'<th {TH.format(a="left" if i == 0 else "right")}>{h}</th>' for i, h in enumerate(["Proposed", "Laws", "With a full impact assessment", "Without", "Share without"]))
        + "</tr></thead><tbody>"
        + "".join("<tr>" + "".join(f'<td {TD.format(a="left" if i == 0 else "right")}>{v}</td>' for i, v in enumerate([l, n, f, w, f"{round(100 * w / n) if n else 0}%"])) + "</tr>" for l, n, f, w in rows)
        + "</tbody></table>")
open("site/ia_table.html", "w").write(html)
print("ia table:", rows, summ["board_known"], summ["board_neg_first"], summ["board_neg_twice"])
