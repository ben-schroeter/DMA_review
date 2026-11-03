"""Generate one canvas page per instrument (115) from the workbook and the analysis data.
Sections: title, Commission and digital agenda, what it does / what we know, timeline, at a glance, how it compares,
the rules (who must act, by kind, reporting, rules or standards, who it applies to and size exemptions), objectives and
key results (with scorecard), evidence since adoption (scrollable, filter for causal studies), second layer and guidance,
amendments, related instruments. Writes site/mockup/Act-<slug>.dc.html (and Instrument.dc.html = Digital Markets Act),
plus site/instrument_pages.json (row_id -> file). Run from research/digital_rulebook."""
import os
import json, re, html, glob, hashlib, collections, statistics, datetime, openpyxl
esc = lambda s: html.escape(str(s if s is not None else ""), quote=True)
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
def sheet(n):
    rows = list(wb[n].values); h = rows[0]
    return [dict(zip(h, r)) for r in rows[1:] if r[0] is not None]
I = [r for r in sheet("instruments") if r.get("celex_measured")];  # initiatives without a measured text (not yet proposed, or newer proposals) have no law page

for _r in I:
    _st = json.load(open("site/forthcoming_status.json")).get(str(_r["row_id"])) if os.path.exists("site/forthcoming_status.json") else None
    if _st: _r["status"] = _st
SEC = sheet("secondary_acts"); AM = sheet("amendments"); GA = sheet("guidance_agencies"); GW = sheet("guidance_web")
PI = sheet("proposal_indicators"); LIT = sheet("impact_literature")
ERA = {o["row_id"]: o for o in json.load(open("data/policy_eras/instruments.json"))}
RS = {o["name"]: o for o in json.load(open("data/rules_standards/summary.json"))["instruments"]}
REP = [json.loads(l) for l in open("data/reporting/reporting_instances.jsonl")]
# company types and size rules (reuse the coding)
ct_src = open("scripts/company_types.py").read()
CT = {}; exec(compile(ct_src.split("wb = openpyxl")[0], "ct", "exec"), CT)
fs_src = open("scripts/firm_size.py").read()
FSR = re.findall(r"\((\d+), lambda r: .*?, (?:MICRO|SMALL|MEDIUM|SMC|LARGE|DESIG), \"([^\"]+)\"\)", fs_src)
SIZE = {
 20: "Organisations with fewer than 250 employees need not keep records of processing activities, unless the processing is risky, not occasional or involves sensitive or criminal-record data (Article 30(5)).",
 32: "Microenterprises offering only number-independent communications services (such as messaging apps) are exempt from most end-user rights rules in Title III, except Articles 99 and 100 (Article 98).",
 71: "Micro, small and medium-sized publishers are exempt from periodic reporting on political advertising revenue (Article 14(2)) and get longer deadlines and best-efforts duties when answering authorities and handling notifications (Articles 15 and 16).",
 115: "Micro and small platforms with a monthly average of fewer than 4,250 listings in the previous quarter may report activity data quarterly, and manually, instead of monthly by machine-to-machine transmission (Article 9(2)).",
 11: "Applies only to mergers above set turnover thresholds (EUR 5 billion worldwide and EUR 250 million in the EU, or lower alternative thresholds), so in practice to large firms.",
 44: "Small enterprises are exempt from the duties to run an internal complaint-handling system and to name mediators.",
 57: "Several obligations apply only to financial entities other than microenterprises.",
 59: "Only designated gatekeepers are bound: firms with at least EUR 7.5 billion annual EU turnover or EUR 75 billion market value, running a platform service with at least 45 million monthly users in the EU.",
 60: "Micro and small platforms are exempt from the extra duties for online platforms and marketplaces and from transparency reports. The strictest rules apply only to very large platforms and search engines, with more than 45 million users in the EU.",
 61: "Applies to medium-sized and larger entities in the listed sectors; some, such as telecoms providers, are covered whatever their size.",
 64: "The strictest rules for general-purpose AI apply only to models with systemic risk, designated by the Commission or trained with very large amounts of computing power. Other duties apply whatever the firm's size, with lighter documentation and lower fines for SMEs.",
 66: "Applies only to deals involving a target with at least EUR 500 million EU turnover, and to public tenders worth at least EUR 250 million.",
 76: "Micro and small manufacturers are exempt from the data-sharing duties for connected products, and some duties to provide data free of charge apply only to larger data holders.",
 80: "Micro and small enterprises are exempt from the duty to disclose unsold consumer products and from the ban on destroying them; medium-sized firms get a transition period.",
 81: "The duties of health data holders for secondary use do not apply to microenterprises.",
 92: "Risk-preparedness duties apply only to large companies (over 500 staff and EUR 150 million turnover) that use strategic raw materials."}
TYPE_NAMES = CT["NAMES"]
CAUSAL = ("causal", "difference-in-difference", "event study", "event-study", "synthetic control", "regression discontinuity", "natural experiment", "instrumental variable", "randomi")
is_causal = lambda m: bool(m) and (bool(re.search(r"\bDiD\b|\bDID\b", m)) or any(k in m.lower() for k in CAUSAL)) and "non-causal" not in m.lower() and "not causal" not in m.lower()
TERMS = [("Delors", 1985.0, ""), ("Santer", 1995.04, "Martin Bangemann"), ("Prodi", 1999.7, "Erkki Liikanen"), ("Barroso I", 2004.9, "Viviane Reding"),
         ("Barroso II", 2010.1, "Neelie Kroes"), ("Juncker", 2014.84, "Andrus Ansip"), ("von der Leyen I", 2019.92, "Margrethe Vestager, Thierry Breton"),
         ("von der Leyen II", 2024.92, "Henna Virkkunen")]
COMNAME = {"Delors": "Delors Commission", "Santer": "Santer Commission", "Prodi": "Prodi Commission", "Barroso I": "first Barroso Commission",
           "Barroso II": "second Barroso Commission", "Juncker": "Juncker Commission", "von der Leyen I": "first von der Leyen Commission", "von der Leyen II": "second von der Leyen Commission"}
ERAN = {"market_opening": ("Market opening", "market-opening"), "lisbon": ("Lisbon", "lisbon"), "europe2020": ("Europe 2020", "europe-2020"),
        "dsm": ("Digital Single Market", "digital-single-market"), "digital_decade": ("Digital Decade", "digital-decade"), "competitiveness": ("Competitiveness · One Europe, One Market", "competitiveness")}
def fy(d):
    s = str(d); return int(s[:4]) + (int(s[5:7]) - 1) / 12 + (int(s[8:10]) - 1) / 365
def term(d):
    v = fy(d); t = [x for x in TERMS if x[1] <= v][-1]
    if t[0] == "Delors" and v < 1989: return t[0], ""
    return t[0], (t[2] if t[0] != "Delors" else "Martin Bangemann")
DATE = lambda d: datetime.date.fromisoformat(str(d)[:10]).strftime("%-d %b %Y") if d else ""
months = lambda a, b: round((fy(b) - fy(a)) * 12)
slug = lambda n: re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", n.lower())).strip("-")[:48].strip("-")
FILE = {r["row_id"]: ("Instrument.dc.html" if r["row_id"] == 59 else f"Act-{slug(r['name'])}.dc.html") for r in I}
adopted = [r for r in I if r["status"] == "adopted" and r["restrictions_total"] is not None]
med = statistics.median(r["restrictions_total"] for r in adopted)
TEMPLATE = open("site/mockup/Instrument.dc.html").read() if False else None

STATUS = {"measured": ("#8F6708", "#FFFFFF", "Measured"), "partially measured": ("#B8860B", "#FFFFFF", "Partly measured"),
          "mixed evidence": ("#E3CF9C", "#282424", "Mixed evidence"), "reported as activity": ("#FFFFFF", "#3F3B3B", "Activity only"),
          "not measured": ("#5C5858", "#FFFFFF", "Not measured"), None: ("#FFFFFF", "#666666", "Not assessed")}
chip = lambda bg, fg, lab, extra="": f'<span class="st" style="background: {bg}; color: {fg}{extra}">{esc(lab)}</span>'

def strip(r):
    W, H, L, R = 1000, 120, 20, 980
    mx = 1200
    X = lambda v: L + min(v, mx) / mx * (R - L)
    g = [f'<line x1="{L}" x2="{R}" y1="80" y2="80" stroke="#C9C6C3"></line>']
    for t in (0, 200, 400, 600, 800, 1000, 1200):
        g.append(f'<text x="{X(t):.1f}" y="104" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="12" fill="#666666">{t:,}{"+" if t == 1200 else ""}</text>')
    vals = sorted(a["restrictions_total"] for a in adopted)
    import random; random.seed(7)
    for v in vals:
        g.append(f'<circle cx="{X(v):.1f}" cy="{66 + random.uniform(-14, 14):.1f}" r="4" fill="#C9C6C3" fill-opacity="0.8"></circle>')
    g.append(f'<line x1="{X(med):.1f}" x2="{X(med):.1f}" y1="34" y2="86" stroke="#666666" stroke-dasharray="3 3"></line><text x="{X(med) + 5:.1f}" y="40" font-family="DM Sans, sans-serif" font-size="12" fill="#666666">median {med:.0f}</text>')
    v = r["restrictions_total"] or 0
    pend = r["status"] != "adopted"
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="18" y2="66" stroke="#B8860B" stroke-width="1.5"></line>'
             f'<circle cx="{X(v):.1f}" cy="66" r="7" fill="{"#FAF9F5" if pend else "#B8860B"}" stroke="#B8860B" stroke-width="2"></circle>'
             f'<text x="{min(max(X(v), 140), 860):.1f}" y="13" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="13" font-weight="600" fill="#282424">{esc(r["name"])}: {v:,}{" (proposal)" if pend else ""}</text>')
    return f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Obligations in this act compared with all 105 adopted acts">' + "".join(g) + "</svg>"

def timeline(r):
    pts = [("Proposal", r["proposal_date"]), ("Adopted", r["adoption_date"]), ("Published", r["oj_publication_date"]), ("In force", r["entry_into_force"])]
    pts = [(l, d) for l, d in pts if d]
    today = "2026-10-31"
    pend = r["status"] != "adopted"
    end = today if pend else max(d for _, d in pts)
    a, b = fy(pts[0][1]), max(fy(end), fy(pts[0][1]) + 0.5)
    W, L, R = 1000, 30, 970
    X = lambda d: L + (fy(d) - a) / (b - a) * (R - L)
    g = [f'<line x1="{L}" x2="{X(end):.1f}" y1="40" y2="40" stroke="#B8860B" stroke-width="3"' + (' stroke-dasharray="6 4"' if pend else "") + "></line>"]
    clusters = []
    for lab, d in pts:
        if clusters and X(d) - X(clusters[-1][-1][1]) < 150:
            clusters[-1].append((lab, d))
        else:
            clusters.append([(lab, d)])
    for k, cl in enumerate(clusters):
        for lab, d in cl:
            g.append(f'<circle cx="{X(d):.1f}" cy="40" r="7" fill="#B8860B" stroke="#FAF9F5" stroke-width="2"></circle>')
        x = X(cl[0][1]); ty = 18 if k % 2 == 0 else 72
        anchor = "start" if x < 160 else ("end" if x > 840 else "middle")
        if anchor == "end": x = X(cl[-1][1])
        txt = " · ".join(f'<tspan font-weight="600">{lab}</tspan> {DATE(d)}' for lab, d in cl)
        g.append(f'<text x="{x:.1f}" y="{ty}" text-anchor="{anchor}" font-family="DM Sans, sans-serif" font-size="13" fill="#282424">{txt}</text>')
    if pend:
        g.append(f'<circle cx="{X(today):.1f}" cy="40" r="6" fill="#FAF9F5" stroke="#B8860B" stroke-width="2"></circle><text x="{X(today):.1f}" y="72" text-anchor="end" font-family="DM Sans, sans-serif" font-size="13" fill="#666666">pending, October 2026</text>')
    return f'<svg viewBox="0 0 {W} 86" width="100%" role="img" aria-label="Timeline from proposal to entry into force">' + "".join(g) + "</svg>"

def ctbl(title, total, rows, note=""):
    tr = "".join(f'<tr><td>{esc(l)}</td><td class="n">{esc(v)}</td></tr>' for l, v in rows)
    if note:
        tr += f'<tr><td class="cap" colspan="2" style="padding-top: 6px">{note}</td></tr>'
    return f'<table class="ctbl"><thead><tr><th>{esc(title)}</th><th class="n">{esc(total)}</th></tr></thead><tbody>{tr}</tbody></table>'

def page(r):
    rid = r["row_id"]; name = r["name"]; pend = r["status"] != "adopted"
    era = ERA.get(rid); en, ea = ERAN[era["era"]]
    pt, pc = term(r["proposal_date"])
    who = f'Proposed {DATE(r["proposal_date"])}'
    pcs = f' ({esc(pc)})' if pc else ""
    if r["adoption_date"] and not pend:
        at, ac = term(r["adoption_date"])
        acs = f' ({esc(ac)})' if ac else ""
        who += (f' and adopted {DATE(r["adoption_date"])} under the <strong>{COMNAME[pt]}</strong>{pcs}' if at == pt
                else f' under the <strong>{COMNAME[pt]}</strong>{pcs} and adopted {DATE(r["adoption_date"])} under the <strong>{COMNAME[at]}</strong>{acs}')
    else:
        who += f' by the <strong>{COMNAME[pt]}</strong>{pcs}; {"agreed, awaiting adoption" if r["status"] == "agreed" else ("listed for withdrawal in the Commission's 2027 work programme" if r["status"] == "withdrawn" else "still pending")}{"" if r["status"] == "withdrawn" else " in October 2026"}'
    cite = era["cites"].get(era["era"]) if era else None
    who += f' · Part of the <a href="DigitalPolicy.dc.html#era-{ea}" style="color: #8F6708; font-weight: 500">{esc(en)} agenda</a>'
    LBL = {"strong": "strong", "moderate": "moderate", "thin": "thin", "ex-ante only": "too early to tell", "not adopted": "not yet adopted", "none": "none"}
    lvl = LBL.get(r["impact_evidence_level"] or ("not adopted" if pend else "none"), r["impact_evidence_level"])
    chips = [f'<a class="chip" href="{esc(r["source_url"] or "")}" style="text-decoration: none">{esc(r["identifier"] or r["celex_measured"])} ↗</a>',
             f'<span class="chip">{"Adopted " + DATE(r["adoption_date"]) if not pend else ("Agreed" if r["status"] == "agreed" else ("Withdrawn" if r["status"] == "withdrawn" else "Proposal"))}</span>',
             f'<span class="chip" style="border-color: #B8860B; color: #8F6708">Evidence: {esc(lvl)}</span>']
    # at a glance
    n = r["restrictions_total"] or 0
    secs = [s for s in SEC if s["parent_row_id"] == rid]
    impl = [s for s in secs if s["kind"] in ("implementing", "delegated")]
    ev = [l for l in LIT if l["parent_row_id"] == rid and (l["category"] or "evidence") == "evidence"]
    causal = [l for l in ev if is_causal(l["method"] or "")]
    kpi = [(f"{n:,}", "obligations in the " + ("proposal" if pend else "adopted text"))]
    if not pend and r["proposal_restrictions_total"]:
        kpi.append((f'{(n - r["proposal_restrictions_total"]) / r["proposal_restrictions_total"] * 100:+.0f}%', f'obligations vs the proposal ({r["proposal_restrictions_total"]:,})'))
    kpi.append((f'{r["words_legal_text"] or 0:,}', f'words, {r["pages"] or "?"} pages'))
    kpi.append((f'{len(impl)}', f'implementing and delegated acts ({sum(s["restrictions_total"] or 0 for s in impl):,} obligations)'))
    kpi.append((f'{len(causal)}', f'causal studies among {len(ev)} sources'))
    kpis = "".join(f'<div style="display: flex; flex-direction: column; gap: 8px"><span class="num">{a}</span><span class="cap">{esc(b)}</span></div>' for a, b in kpi)
    rank = sum(1 for a in adopted if a["restrictions_total"] < n)
    cmp_text = (f"With {n:,} obligations, the {esc(name)} has more than {rank} of the 105 adopted EU digital acts. The median act has {med:.0f}."
                if not pend else f"The proposal contains {n:,} obligations; the median adopted act has {med:.0f}.")
    # rules
    ap, ams, aei, aun, ano = (r[k] or 0 for k in ("addr_private_parties", "addr_member_states", "addr_eu_institutions", "addr_unclear", "addr_no_actor"))
    tot = max(1, ap + ams + aei + aun + ano)
    bar = "".join(f'<div style="flex: {v}; background: {c}"></div>' for v, c in ((ap, "#B8860B"), (aei, "#A6A3A0"), (ams, "#666262"), (aun + ano, "#E8E6E3")) if v)
    leg = "".join(f'<span style="display: inline-flex; align-items: center; gap: 8px"><span style="width: 10px; height: 10px; border-radius: 2px; background: {c}"></span>{l} {v}</span>'
                  for l, v, c in (("Companies", ap, "#B8860B"), ("Commission and EU bodies", aei, "#A6A3A0"), ("Member states", ams, "#666262"), ("No specific actor", aun + ano, "#E8E6E3")) if v)
    kinds = [("Positive obligations", r["r_obligation"] or 0), ("Prohibitions", r["r_prohibition"] or 0), ("Duties of result", r["r_duty_of_result"] or 0),
             ("Other", (r["r_restricted_permission"] or 0) + (r["r_explicit_requirement"] or 0))]
    tables = [ctbl("By kind", f"{n:,}", [(k, f"{v:,}") for k, v in kinds if v])]
    rep_main = [x for x in REP if x["doc"] == str(r["celex_measured"]) and x["kind"] == "main" and x["reporting"]]
    rep_sec = [x for x in REP if x["kind"] == "secondary" and x["reporting"] and x["doc"] in {s["celex"] for s in impl}]
    if rep_main or rep_sec:
        TL = {"report_submission": "Reports to authorities", "disclosure": "Public disclosures", "notification": "Notifications", "on_request": "On request", "record_keeping": "Record keeping", "registration": "Registration"}
        tc = collections.Counter(x["type"] for x in rep_main)
        ac = collections.Counter(x["addressee"] for x in rep_main)
        owed = " · ".join(f"{l} {ac[k]}" for k, l in (("private_parties", "companies"), ("eu_institutions", "Commission and EU bodies"), ("member_states", "member states")) if ac[k])
        tables.append(ctbl("Reporting obligations", len(rep_main), [(TL.get(k, k.replace("_", " ")), v) for k, v in tc.most_common()],
                           (f"Owed by {owed}. " if owed else "") + (f"Implementing and delegated acts add {len(rep_sec)} more. " if rep_sec else "") + '<a href="CompanyTypes.dc.html">Reporting across all laws</a>'))
    rs = RS.get(name)
    if rs and rs["main"]["n"]:
        rows = [(f'Main act ({rs["main"]["n"]:,} obligations)', f'{rs["main"]["R"]:.0%}')]
        if rs.get("secondary") and rs["secondary"]["n"] >= 10:
            rows.append((f'Implementing and delegated acts ({rs["secondary"]["n"]:,})', f'{rs["secondary"]["R"]:.0%}'))
        tables.append(ctbl("Rules or standards", "rules", rows, 'Rules fix the required conduct in advance; standards (“appropriate”, “proportionate”) leave it to be judged later. <a href="UsComparison.dc.html">How we code this</a>'))
    types = [TYPE_NAMES[k] for k in (["B"] + CT["TYPES"]) if k in CT["M"].get(rid, {})]
    applies = ("Applies to: " + "; ".join(types) + ".") if types else ("No company type assigned: its obligations fall mainly on public bodies, or on companies only as grant conditions." if ap else "Its obligations fall on public bodies, not companies.")
    size = SIZE.get(rid)
    applies_html = ''
    applies_html += (f'<p class="body" style="font-size: 15px"><strong style="font-weight: 600">Size thresholds and exemptions:</strong> {esc(size)}</p>') if size else '<p class="body" style="font-size: 15px"><strong style="font-weight: 600">Size thresholds and exemptions:</strong> none found in the binding text; the rules apply to firms of every size.</p>'
    applies_html += '<p class="cap" style="margin: 0"><a href="CompanyTypes.dc.html">See how the Digital Acquis applies by type of company</a></p>'
    # objectives and key results
    pis = [p for p in PI if p["parent_row_id"] == rid]
    krs = [p for p in pis if p["indicator / promised impact"]]
    objs = []
    for p in pis:
        if not p["indicator / promised impact"] and p["objective"] and "objective" in (p["type"] or ""):
            objs.append(p["objective"])
    if not objs:
        objs = list(dict.fromkeys((p["objective"] or "").split(" / ")[0] for p in krs if p["objective"]))
    objs = list(dict.fromkeys(objs))[:8]
    sc = collections.Counter(p["status_group"] for p in krs)
    score = (f'{sc["measured"]} of {len(krs)} key results measured, {sc["partially measured"]} partly, {sc["mixed evidence"]} with mixed evidence, '
             f'{sc["reported as activity"]} reported only as activity, {sc["not measured"]} not measured' + (f', {sc[None]} not assessed' if sc[None] else "") + ".") if krs else ""
    kr_rows = "".join(f'<tr><td>{esc(p["indicator / promised impact"])}<span class="small">{esc((p["type"] or "").split(" (")[0].capitalize())}</span></td><td>{esc(p["objective"] or "")}</td>'
                      f'<td>{esc(p["evidence found"] or "")}</td><td>{chip(*STATUS.get(p["status_group"], STATUS[None]))}</td></tr>' for p in krs)
    okr = ""
    if objs or krs:
        okr = f'''  <section style="padding-block: 40px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      <h2 class="h2">Objectives and key results</h2>
      <p class="body">Objectives are the aims the Commission set for the law. Key results are how it said it would measure them: indicators in the proposal and forecasts in the impact assessment, checked against the evidence available in October 2026.</p>
      {"<div style='display: flex; flex-direction: column; gap: 10px; padding: 20px 24px; border-radius: 12px; background: #F3F1EC'><span class='eyebrow' style='font-size: 12px'>Objectives</span><ul style='margin: 0; padding-left: 20px; color: #3F3B3B'>" + "".join(f"<li>{esc(o)}</li>" for o in objs) + "</ul></div>" if objs else ""}
      {f'<p class="body" style="font-size: 15px"><strong style="font-weight: 600">Scorecard:</strong> {score} <a href="Evidence.dc.html">All laws</a></p>' if score else ""}
      {f'<div class="scroll" style="max-height: 460px"><table class="tbl"><thead><tr><th scope="col">Key result</th><th scope="col">Objective</th><th scope="col">Evidence found</th><th scope="col">Status</th></tr></thead><tbody>{kr_rows}</tbody></table></div>' + (f'<p class="hint">Scroll the table to see all {len(krs)} key results ↓</p>' if len(krs) > 5 else "") if krs else '<p class="cap">No measurable key results were set in the proposal.</p>'}
    </div>
  </section>
'''
    # evidence
    ev_sorted = sorted(ev, key=lambda l: (not is_causal(l["method"] or ""), -(l["year"] or 0)))
    def evrow(l):
        u = l["url"] or l["pdf_url"] or l["archive_url"] or ""
        title = (l["citation"] or "")
        tchip = '<span class="chip" style="margin-top: 6px; border-color: #B8860B; color: #8F6708">Causal</span>' if is_causal(l["method"] or "") else ""
        return (f'<tr><td style="min-width: 260px">' + (f'<a href="{esc(u)}">{esc(title)}</a>' if u else esc(title)) + f'<span class="small">{esc(l["source_type"] or "")} · {esc(l["year"] or "")}</span>{tchip}</td>'
                f'<td>{esc(l["method"] or "")}</td><td>{esc(l["plain-language summary"] or l["headline finding"] or "")}</td></tr>')
    ev_c = "".join(evrow(l) for l in ev_sorted if is_causal(l["method"] or ""))
    ev_o = "".join(evrow(l) for l in ev_sorted if not is_causal(l["method"] or ""))
    evidence = f'''  <section style="padding-block: 40px; background: #F3F1EC; border-top: 1px solid #E8E6E3; border-bottom: 1px solid #E8E6E3">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 16px">
        <div style="display: flex; flex-direction: column; gap: 10px">
          <h2 class="h2">{"Evidence so far" if pend else "Evidence since adoption"}</h2>
          <p class="body">Evaluations and research. Causal studies first, then the rest by year. Enforcement decisions and court rulings are not counted as evidence.</p>
        </div>
        <label for="causal-only" style="display: inline-flex; align-items: center; gap: 10px; font-size: 15px; min-height: 44px; cursor: pointer"><input id="causal-only" type="checkbox" checked="{{{{causalOnly}}}}" onChange="{{{{toggle}}}}" style="width: 18px; height: 18px; accent-color: #B8860B">Causal studies only</label>
      </div>
      {f'<div class="scroll" style="max-height: 560px; background: #FAF9F5"><table class="tbl"><thead><tr><th scope="col">Source</th><th scope="col">Method</th><th scope="col">Finding</th></tr></thead><tbody>{ev_c}<sc-if value="{{{{showAll}}}}" hint-placeholder-val="{{{{ true }}}}">{ev_o}</sc-if></tbody></table></div>' + (f'<p class="hint">Scroll the list to see all {len(ev)} sources ↓</p>' if len(ev) > 4 else "") if ev else '<p class="cap">No evaluations or studies found yet.</p>'}
      <span class="cap">{len(ev)} sources, {len(causal)} causal. Each source links to the paper or official page.</span>
    </div>
  </section>
'''
    # second layer and guidance
    def lst(items, empty):
        if not items:
            return f'<p class="cap" style="margin: 0">{empty}</p>'
        hint = f'<p class="hint">Scroll the box to see all {len(items)} ↓</p>' if len(items) > 5 else ""
        return '<div class="scroll" style="max-height: 300px"><ul class="lst">' + "".join(items) + "</ul></div>" + hint
    sec_items = [f'<li><span class="cap">{DATE(s["date"])}</span><span><a href="{esc(s["source_url"] or "")}">{esc((s["title"] or s["celex"])[:180])}</a> <span class="cap">· {esc(s["kind"])}{", " + format(s["restrictions_total"], ",") + " obligations" if s["restrictions_total"] else ""}</span></span></li>'
                 for s in sorted([x for x in secs if x["kind"] != "guidance"], key=lambda s: str(s["date"] or ""), reverse=True)]
    sec_guid = [x for x in secs if x["kind"] == "guidance"]
    gd_items = [f'<li><span class="cap">{DATE(g["date"]) if g["date"] and re.match(r"\d{4}-\d\d-\d\d", str(g["date"])) else esc(g["date"] or "")}</span><span><a href="{esc(g["pdf_url"] or "")}">{esc((g["title"] or "")[:180])}</a> <span class="cap">· {esc(g["agency"] or "")}</span></span></li>' for g in GA if g["parent_row_id"] == rid]
    gd_items += [f'<li><span class="cap">{esc(g["date"] or "")}</span><span><a href="{esc(g["source_url"] or "")}">{esc((g["title"] or "")[:180])}</a> <span class="cap">· Commission</span></span></li>' for g in GW if g["parent_row_id"] == rid]
    gd_items = [f'<li><span class="cap">{DATE(x["date"])}</span><span><a href="{esc(x["source_url"] or "")}">{esc((x["title"] or x["celex"])[:180])}</a> <span class="cap">· Commission</span></span></li>'
                for x in sorted(sec_guid, key=lambda x: str(x["date"] or ""), reverse=True)] + gd_items
    ng = max(0, (r["n_guidance_eurlex"] or 0) - len(sec_guid))
    revs = [x for x in REVIEWS if x["law_id"] == rid]
    rev_html = "".join(f'<div style="padding: 12px 16px; border-left: 3px solid #B8860B; background: #FFFFFF; border-radius: 0 10px 10px 0; font-size: 14px; line-height: 1.45">'
                       f'<strong style="font-weight: 600">Under review: {esc(x["item"])}.</strong> {esc(x["last_step"])}. Next: {esc(x["next_step"])}. '
                       f'<a href="{esc(x["source_url"])}">Review page</a> <span class="cap">· checked {esc(x["checked"])}</span></div>' for x in revs)
    second = f'''  <section style="padding-block: 40px">
    <div class="wrap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 40px; align-items: start">
      <div style="display: flex; flex-direction: column; gap: 12px">
        <h2 class="h3">Implementation: {len(sec_items)} implementing, delegated and other acts</h2>
        {lst(sec_items, "No implementing or delegated acts found.")}
      </div>
      <div style="display: flex; flex-direction: column; gap: 12px">
        <h2 class="h3">Guidance</h2>
        {rev_html}
        {lst(gd_items, "No guidance in our dataset.")}
        {f'<p class="cap" style="margin: 0">Plus {ng} Commission guidance documents and notices listed on EUR-Lex.</p>' if ng else ""}
      </div>
    </div>
  </section>
'''
    ams_ = [a for a in AM if a["parent_row_id"] == rid and a["kind"] == "amendment"]
    am_items = [f'<li><span class="cap">{DATE(a["date"])}</span><span><a href="{esc(a["source_url"] or "")}">{esc((a["title"] or a["celex"])[:200])}</a></span></li>' for a in sorted(ams_, key=lambda a: str(a["date"] or ""), reverse=True)]
    pa = [x for x in PENDING if x["law_id"] == rid]
    pa_html = ("".join(f'<div style="padding: 12px 16px; border-left: 3px solid #B8860B; background: #FFFFFF; border-radius: 0 10px 10px 0; font-size: 14px; line-height: 1.45">'
                       f'<strong style="font-weight: 600">Amendment pending: <a href="{esc(x["url"])}">{esc(x["proposal"])}</a></strong> <span class="cap">· {esc(x["ref"])}, proposed {DATE(x["proposed"])}</span><br>'
                       f'{esc(x["what"])} <a href="{esc(x["oeil"])}">Procedure {esc(x["procedure"])}</a></div>' for x in sorted(pa, key=lambda x: x["proposed"], reverse=True)))
    pa_note = (" Pending amending proposals are those on the Commission's priority list in its 2027 work programme." if pa else " Pending amending proposals, such as the Digital Omnibus, are not yet tracked for this law.")
    amend = f'''  <section style="padding-block: 8px 40px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 12px">
      <h2 class="h3">Amendments: {len(ams_)}{f" adopted, {len(pa)} pending" if pa else ""}</h2>
      {pa_html}
      {lst(am_items, "Not amended since adoption." if not pend else "Not yet adopted.")}
      <p class="cap" style="margin: 0">Adopted amending acts, latest first{(", plus " + str(r["n_corrigenda"]) + " corrigenda") if r["n_corrigenda"] else ""}.{pa_note}</p>
    </div>
  </section>
'''
    rel = sorted([x for x in I if x["policy_area"] == r["policy_area"] and x["row_id"] != rid], key=lambda x: -(x["restrictions_total"] or 0))[:3]
    related = "".join(f'<a href="{FILE[x["row_id"]]}" style="display: flex; flex-direction: column; gap: 6px; padding: 18px; border: 1px solid #E8E6E3; border-radius: 12px; text-decoration: none; background: #FFFFFF"><span style="font-family: \'Source Serif 4\', Georgia, serif; font-size: 20px">{esc(x["name"])}</span><span class="cap">{str(x["adoption_date"] or x["proposal_date"])[:4]} · {(x["restrictions_total"] or 0):,} obligations</span></a>' for x in rel)
    body = f'''  <section style="padding-block: 40px 28px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 18px">
      <nav aria-label="Breadcrumb" class="cap"><a href="Instruments.dc.html" style="color: #666666">Legal instruments</a> / <span>{esc(r["policy_area"])}</span></nav>
      <h1 style="font-family: 'Source Serif 4', Georgia, serif; font-weight: 400; font-size: 52px; line-height: 1.05; letter-spacing: -0.02em; margin: 0">{esc(name)}</h1>
      <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center">{"".join(chips)}</div>
      <p class="cap" style="margin: 0">{who}</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; padding-top: 4px">
        <div style="display: flex; flex-direction: column; gap: 8px"><p class="eyebrow">What it does</p><p class="body" style="font-size: 17px; color: #282424">{esc(r["objectives"] or "")}</p></div>
        <div style="display: flex; flex-direction: column; gap: 8px"><p class="eyebrow">What we know so far</p><p class="body" style="font-size: 17px">{esc(r["impact_summary"] or ("Not yet adopted; no evidence on effects." if pend else "No summary yet."))}</p></div>
      </div>
      <figure style="margin: 8px 0 0; display: flex; flex-direction: column; gap: 4px"><figcaption class="eyebrow">Timeline</figcaption>{timeline(r)}
        <span class="cap">{f'{months(r["proposal_date"], r["adoption_date"])} months from proposal to adoption.' if r["adoption_date"] and not pend else f'In negotiation for {months(r["proposal_date"], "2026-10-31")} months.'} Dates when rules start to apply may be set in the text and can come later.</span></figure>
    </div>
  </section>
  <section style="border-top: 1px solid #E8E6E3; border-bottom: 1px solid #E8E6E3; background: #F3F1EC">
    <div class="wrap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 28px; padding-block: 30px">{kpis}</div>
  </section>
{STAND.get(str(rid), "")}  <section style="padding-block: 40px 0">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 12px">
      <h2 class="h2">How it compares</h2>
      <p class="body">{cmp_text}</p>
      <figure style="margin: 0">{strip(r)}<span class="cap">Each dot is one adopted act; gold marks this one. <a href="Instruments.dc.html">Compare all instruments</a></span></figure>
    </div>
  </section>
  <section style="padding-block: 40px">
    <div class="wrap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 48px">
      <div style="display: flex; flex-direction: column; gap: 16px">
        <h2 class="h2">The rules</h2>
        <div style="display: flex; height: 28px; border-radius: 6px; overflow: hidden; gap: 2px" role="img" aria-label="Who must act">{bar}</div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px 18px" class="cap">{leg}</div>
        <span class="cap">Who the text tells to act, for each of the {n:,} obligations. <a href="Methodology.dc.html#obligations">How we code this</a></span>
        <h3 class="h3" style="padding-top: 8px">Who it applies to</h3>
        {applies_html}
      </div>
      <div style="display: flex; flex-direction: column; gap: 18px">{"".join(tables)}</div>
    </div>
  </section>
  <hr style="border: 0; border-top: 1px solid #E8E6E3; margin: 0">
{okr}{evidence}{second}{amend}  <section style="padding-block: 8px 48px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 16px">
      <h2 class="h3">Related instruments in {esc(r["policy_area"])}</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px">{related}</div>
    </div>
  </section>
'''
    return body

REVIEWS = json.load(open("data/reviews.json")) if os.path.exists("data/reviews.json") else []
PENDING = json.load(open("data/pending_amendments.json")) if os.path.exists("data/pending_amendments.json") else []
STAND = json.load(open("site/forthcoming.json")) if os.path.exists("site/forthcoming.json") else {}
TPL = open("site/instrument_template.dc.html").read()
H0, H1 = TPL.split("<!--BODY-->")
out = {}
for r in I:
    src = H0.replace("<title>Digital Markets Act</title>", f"<title>{esc(r['name'])}</title>") + page(r) + H1
    open(f"site/mockup/{FILE[r['row_id']]}", "w").write(src)
    out[r["row_id"]] = FILE[r["row_id"]]
json.dump(out, open("site/instrument_pages.json", "w"), indent=1)
print(len(out))
