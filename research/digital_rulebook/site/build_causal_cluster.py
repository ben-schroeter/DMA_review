"""'Do the rules work?' page: the laws with the most causal studies (bars), from site/studies_data.json (built by
site/build_studies_data.py). Writes site/causal_cluster_table.html, filled into the page by site/assemble.py
(<!--@chart file:causal_cluster_table.html-->). Run from research/digital_rulebook."""
import collections, json, html

L = json.load(open("site/studies_data.json"))["L"]
PAGES = json.load(open("site/instrument_pages.json"))   # row_id -> page
import openpyxl
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
rows = list(wb["instruments"].values); h = rows[0]
by_name = {r[h.index("name")]: r[0] for r in rows[1:] if r[0] and r[h.index("status")] == "adopted"}
SHORT = {"General Data Protection Regulation": "GDPR", "Digital Markets Act": "Digital Markets Act", "Vertical Block Exemption Regulation": "Vertical Block Exemption",
         "Copyright in the Digital Single Market Directive": "Copyright DSM Directive", "Markets in Crypto-Assets (MiCA)": "MiCA"}
cnt = collections.Counter(x[0] for x in L if x[10] == "ev causal" and x[0] in by_name)
TOP = 10
top = cnt.most_common()
# keep ties at the cut-off together
cut = top[TOP - 1][1] if len(top) >= TOP else 0
shown = [t for t in top if t[1] >= cut][:TOP + 3]
rest = top[len(shown):]
mx = shown[0][1]
out = []
for name, n in shown:
    page = PAGES.get(str(by_name[name]), "Instruments.dc.html")
    col = "#B8860B" if n >= 4 else "#A6A3A0"
    out.append(f'<div class="lv" style="grid-template-columns: 240px minmax(0,1fr) 28px"><a href="{page}">{html.escape(SHORT.get(name, name))}</a>'
               f'<div style="height: 12px; width: {round(100 * n / mx)}%; background: {col}; border-radius: 0 4px 4px 0"></div><span style="text-align: right">{n}</span></div>')
if rest:
    lo, hi = min(n for _, n in rest), max(n for _, n in rest)
    out.append(f'<div class="lv" style="grid-template-columns: 240px minmax(0,1fr) 28px"><span>{len(rest)} other instruments</span><div></div>'
               f'<span style="text-align: right">{lo if lo == hi else f"{lo}–{hi}"}</span></div>')
open("site/causal_cluster_table.html", "w").write('<div style="display: flex; flex-direction: column; gap: 10px">' + "".join(out) + "</div>")
print("causal cluster:", shown, "other", len(rest), "total", sum(cnt.values()))
