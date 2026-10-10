"""Assemble research/ceps_metrics/ceps_instruments_metrics.xlsx from data/*.json|csv."""
import csv, json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

D = "../data/"
rows = list(csv.DictReader(open(D + "ceps_instruments.csv")))
imap = list(csv.DictReader(open(D + "instrument_map.csv")))
meas = {(m["celex"], m["kind"]): m for m in json.load(open(D + "measurements.json"))}
mainm = {m["celex"]: m for m in json.load(open(D + "measurements.json")) if m["kind"] in ("main", "secondary")}
cons = json.load(open(D + "consolidated.json"))
nim = json.load(open(D + "national_measures.json"))
sec = json.load(open(D + "secondary_acts.json"))
web = list(csv.DictReader(open(D + "guidance_web_supplement.csv")))
val = json.load(open(D + "validation_results.json"))

URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{}"
METRICS = ["pages", "words_legal_text", "words_preamble", "words_recitals", "words_articles", "words_annexes",
           "words_memorandum", "words_financial_statement", "restrictions_total", "r_obligation", "r_prohibition",
           "r_restricted_permission", "r_explicit_requirement", "r_duty_of_result", "addr_private_parties",
           "addr_member_states", "addr_eu_institutions", "addr_unclear"]
HDR = Font(name="Arial", bold=True, color="FFFFFF"); FILL = PatternFill("solid", fgColor="1F4E78")
BODY = Font(name="Arial", size=10)


def style(ws, widths):
    for c in ws[1]:
        c.font = HDR; c.fill = FILL; c.alignment = Alignment(wrap_text=True, vertical="top")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = Font(name="Arial", size=10, color=c.font.color.rgb if c.font and c.font.color and c.font.color.type == "rgb" else None)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "C2"; ws.auto_filter.ref = ws.dimensions
    ws.row_dimensions[1].height = 45


def summed(celexes, kind="main"):
    out, notes = {}, []
    for c in celexes:
        m = meas.get((c, kind)) or mainm.get(c)
        if not m or "error" in m:
            notes.append(f"{c}: not measured ({(m or {}).get('error', 'missing')})"); continue
        if m.get("parse_warning"):
            notes.append(f"{c}: {m['parse_warning']}")
        for k in METRICS:
            v = m.get(k)
            if v is not None:
                out[k] = out.get(k, 0) + v
    return out, notes


wb = Workbook()
# ---------------- secondary sheet first (instrument formulas reference it) ----------------
ws2 = wb.active; ws2.title = "secondary_acts"
row_of = {}
for r in imap:
    for c in r["celex_measured"].split(";"):
        row_of.setdefault(c, (r["row_id"], r["name"]))
sh = ["parent_row_id", "parent_name", "parent_celex", "celex", "kind", "eurlex_type", "date", "title",
      "addressed_to_specific_member_state", "source_url"] + METRICS + ["note"]
ws2.append(sh)
for s in sorted(sec, key=lambda s: (int(row_of.get(s["parent"], ("999",))[0]), s["date"], s["celex"])):
    rid, nm = row_of.get(s["parent"], ("", ""))
    m, notes = summed([s["celex"]], "secondary")
    note = "; ".join(notes)
    if s["kind"] == "guidance":
        note = (note + "; " if note else "") + "Guidance is non-binding: restriction counts mostly reflect obligations it restates"
    ws2.append([int(rid) if rid else None, nm, s["parent"], s["celex"], s["kind"], s["type"], s["date"], s["title"],
                "yes" if s["addressed_to_specific_state_or_party"] else "no", URL.format(s["celex"])]
               + [m.get(k) for k in METRICS] + [note])
n2 = ws2.max_row
style(ws2, [8, 30, 13, 16, 14, 12, 11, 60, 12, 30] + [10] * len(METRICS) + [40])

# ---------------- web guidance ----------------
ws3 = wb.create_sheet("guidance_web")
ws3.append(["parent_row_id", "parent_name", "parent_celex", "reference", "date", "title", "source_url", "note"])
for g in web:
    rid, nm = row_of.get(g["parent_celex"], ("", ""))
    ws3.append([int(rid) if rid else None, nm, g["parent_celex"], g["reference"], g["date"], g["title"], g["source_url"],
                g["note"] + "; found by web search, not linked in EUR-Lex; not measured"])
n3 = ws3.max_row
style(ws3, [8, 30, 13, 14, 11, 70, 50, 50])

# ---------------- instruments ----------------
ws = wb.create_sheet("instruments", 0)
cols = ["row_id", "name", "identifier", "proposal_date", "confidence_proposal_date", "status_ceps_jul2025", "status_oct2026",
        "celex_measured", "text_measured", "source_url"] + METRICS + \
       ["consolidated_celex", "consolidated_restrictions_total", "consolidated_addr_private_parties",
        "n_implementing_acts", "n_delegated_acts", "n_other_commission_council_acts", "n_guidance_eurlex", "n_guidance_web",
        "restrictions_in_implementing_and_delegated_acts", "national_transposition_measures", "member_states_with_measures", "note"]
ws.append(cols)
ci = {c: i + 1 for i, c in enumerate(cols)}
for i, (r, m0) in enumerate(zip(rows, imap), start=2):
    cel = m0["celex_measured"].split(";")
    if cel[0].startswith("COUNCIL"):
        text, url = "Council final compromise text, 23 Apr 2026", ""
        met, notes = {}, ["Not measured: Council document register (data.consilium.europa.eu) is blocked by this environment's network policy"]
    else:
        text = "Commission proposal (COM)" if cel[0].startswith("5") else "Original act as published in the OJ"
        url = " ; ".join(URL.format(c) for c in cel)
        met, notes = summed(cel)
    cc = [cons[c]["latest"] for c in cel if c in cons]
    cmet, cnotes = summed(cc, "consolidated") if cc else ({}, [])
    dirs = [c for c in cel if c[5:6] == "L"]
    note = "; ".join(x for x in [m0["note"]] + notes + cnotes if x)
    vals = [int(m0["row_id"]), r["name"], r["identifier"], r["proposal_date"], r["confidence"], m0["status_ceps_jul2025"],
            m0["status_oct2026"], ";".join(cel), text, url] + [met.get(k) for k in METRICS] + \
           [";".join(cc) or None, cmet.get("restrictions_total"), cmet.get("addr_private_parties")]
    ws.append(vals + [None] * 6 + [sum(nim[c]["n_measures"] for c in dirs if c in nim) if dirs else None,
                                   max((nim[c]["n_member_states"] for c in dirs if c in nim), default=None) if dirs else None,
                                   note])
    R = f"secondary_acts!$A$2:$A${n2}"; K = f"secondary_acts!$E$2:$E${n2}"
    RT = f"secondary_acts!${get_column_letter(10 + METRICS.index('restrictions_total') + 1)}$2:${get_column_letter(10 + METRICS.index('restrictions_total') + 1)}${n2}"
    f = {"n_implementing_acts": f'=COUNTIFS({R},$A{i},{K},"implementing")',
         "n_delegated_acts": f'=COUNTIFS({R},$A{i},{K},"delegated")',
         "n_other_commission_council_acts": f'=COUNTIFS({R},$A{i},{K},"other Commission/Council act")',
         "n_guidance_eurlex": f'=COUNTIFS({R},$A{i},{K},"guidance")',
         "n_guidance_web": f'=COUNTIF(guidance_web!$A$2:$A${max(n3, 2)},$A{i})',
         "restrictions_in_implementing_and_delegated_acts":
             f'=SUMIFS({RT},{R},$A{i},{K},"implementing")+SUMIFS({RT},{R},$A{i},{K},"delegated")'}
    for k, v in f.items():
        ws.cell(row=i, column=ci[k], value=v)
# totals row
tr = ws.max_row + 1
ws.cell(row=tr, column=2, value="TOTAL (all rows)").font = Font(name="Arial", bold=True)
for k in METRICS + ["consolidated_restrictions_total", "consolidated_addr_private_parties", "n_implementing_acts",
                    "n_delegated_acts", "n_other_commission_council_acts", "n_guidance_eurlex", "n_guidance_web",
                    "restrictions_in_implementing_and_delegated_acts", "national_transposition_measures"]:
    L = get_column_letter(ci[k]); ws.cell(row=tr, column=ci[k], value=f"=SUM({L}2:{L}{tr - 1})")
style(ws, [6, 34, 22, 11, 9, 10, 10, 16, 18, 30] + [10] * len(METRICS) + [20, 11, 11, 9, 9, 9, 9, 9, 12, 11, 10, 60])
for c in ws[tr]:
    c.font = Font(name="Arial", bold=True, size=10)
for k in METRICS + ["consolidated_restrictions_total", "restrictions_in_implementing_and_delegated_acts", "national_transposition_measures"]:
    for row in ws.iter_rows(min_row=2, min_col=ci[k], max_col=ci[k]):
        row[0].number_format = "#,##0"

# ---------------- method + validation ----------------
wm = wb.create_sheet("method")
for line in open(D + "../METHOD.md").read().splitlines():
    wm.append([line])
wm.column_dimensions["A"].width = 140
for row in wm.iter_rows():
    row[0].font = Font(name="Arial", size=10, bold=row[0].value is not None and str(row[0].value).startswith("#"))
    row[0].alignment = Alignment(wrap_text=True)
wv = wb.create_sheet("validation")
wv.append(["sample", "counted_true", "counted_false", "missed_true", "correctly_dropped", "precision", "recall_within_sample",
           "addressee_accuracy", "addressee_n"])
for k, v in val.items():
    if isinstance(v, dict) and "precision" in v:
        wv.append([k] + [v[x] for x in ["counted_true", "counted_false", "missed_true", "correctly_dropped", "precision",
                                         "recall_within_sample", "addressee_accuracy", "addressee_n"]])
    elif isinstance(v, dict):
        wv.append([k] + [json.dumps(v)])
style(wv, [28, 12, 12, 12, 14, 10, 14, 14, 12])
wv.freeze_panes = None
wb.save("../ceps_instruments_metrics.xlsx")
print("saved", ws.max_row, n2, n3)
