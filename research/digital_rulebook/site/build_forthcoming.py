"""Builds Digital Acquis > Forthcoming (list of proposed and announced initiatives not yet adopted) and one page per
initiative. Writes to site/mockup/ and site/forthcoming.json (status blocks for pending laws that have a law page). Run from research/digital_rulebook/site."""
import html, json, os, re

esc = lambda s: html.escape(s, quote=True)
EUR = lambda c: f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{c}"
OEIL = lambda p: f"https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference={p}"
PAGES = json.load(open("instrument_pages.json"))  # row_id -> Act page
ACT = lambda rid: PAGES[str(rid)]
AS_OF = "November 2026"

STEPS = ["Proposal", "Parliament position", "Council position", "Trilogues", "Agreement"]
# track: list of dates (or "" if done without a date, None if not reached), one per step

F = [
 # --- agreed, awaiting formal adoption
 dict(id="psr", name="Payment Services Regulation (PSR)", stage="agreed", area="Finance", row=99, proc="2023/0210(COD)",
      what="Directly applicable rules for payment services: fraud prevention, IBAN checks, open banking access.",
      track=["Jun 2023", "Apr 2024", "Jun 2025", "2025", "Apr 2026"], target="—",
      latest="Agreed with Council in November 2025; Parliament's committee approved the text in May 2026; plenary vote indicatively 14 December 2026."),
 dict(id="psd3", name="Payment Services Directive 3 (PSD3)", stage="agreed", area="Finance", row=100, proc="2023/0209(COD)",
      what="Licensing and supervision of payment and e-money institutions.",
      track=["Jun 2023", "Apr 2024", "Jun 2025", "2025", "Apr 2026"], target="—",
      latest="Agreed together with the PSR; plenary vote indicatively 14 December 2026."),
 # --- proposed, in negotiation
 dict(id="digital-omnibus", name="Digital Omnibus (data, privacy, cybersecurity)", stage="proposed", area="Data & Privacy", proc="COM(2025) 837",
      what="Amends the GDPR, ePrivacy rules, the Data Act and incident reporting to cut compliance costs.",
      track=["Nov 2025", None, "Oct 2026", None, None], target="End 2026",
      latest="Council agreed its mandate in October 2026; Parliament committees are still voting on amendments. The AI part was adopted separately (Regulation (EU) 2026/1744, in force July 2026)."),
 dict(id="business-wallet", name="European Business Wallet", stage="proposed", area="Competition & Single Market", proc="Nov 2025",
      what="A digital wallet for companies to identify themselves, sign and exchange documents with authorities across the EU.",
      track=["Nov 2025", None, None, None, None], target="End 2026",
      latest="Parliament adopted its negotiating mandate on 7 October 2026; Council working party still negotiating."),
 dict(id="digital-networks-act", name="Digital Networks Act", stage="proposed", area="Connectivity", proc="2026/0013(COD)",
      what="Replaces the telecoms code with a single regulation: EU-wide spectrum coordination, copper switch-off, lighter authorisation.",
      track=["Jan 2026", None, None, None, None], target="Q4 2027",
      latest="Parliament: ITRE lead, rapporteur Michał Kobosko. Council: progress report to the June 2026 Telecoms Council."),
 dict(id="eu-kids-act", name="EU KIDS Act", stage="proposed", area="Trust & Safety", proc="2026/0286(COD)",
      what="No social media accounts under 13, supervised accounts at 13 and 14, independent accounts from 15; safety-by-design duties for services used by minors; certified age verification.",
      track=["Sep 2026", None, None, None, None], target="—",
      latest="Proposed 17 September 2026; referred to Parliament's Industry committee (ITRE) on 22 October 2026."),
 dict(id="cybersecurity-act-2", name="Cybersecurity Act 2", stage="proposed", area="Cybersecurity", proc="COM(2026) 11",
      what="Revises ENISA's mandate and EU certification, with targeted NIS2 amendments and ICT supply-chain security.",
      track=["Jan 2026", None, None, None, None], target="End 2026",
      latest="In committee in Parliament and in Council working party."),
 dict(id="eu-inc", name="EU Inc (28th regime)", stage="proposed", area="Competition & Single Market", proc="Q1 2026",
      what="An optional EU-wide company status, so firms can operate across all 27 member states under one rulebook.",
      track=["Mar 2026", None, None, None, None], target="End 2026",
      latest="Fast-tracked under the One Europe, One Market roadmap."),
 dict(id="cloud-ai-development-act", name="Cloud and AI Development Act", stage="proposed", area="Industrial Policy", proc="Jun 2026",
      what="Aims to triple EU data-centre capacity and sets EU-wide requirements for cloud providers.",
      track=["Jun 2026", None, None, None, None], target="Q4 2027",
      latest="Proposed in the tech sovereignty package with Chips Act 2."),
 dict(id="chips-act-2", name="Chips Act 2", stage="proposed", area="Industrial Policy", proc="Jun 2026",
      what="Further support for advanced chip production and design, and supply-chain monitoring.",
      track=["Jun 2026", None, None, None, None], target="Q2 2027",
      latest="Proposed in June 2026; amends the European Chips Act."),
 dict(id="european-innovation-act", name="European Innovation Act", stage="proposed", area="Industrial Policy", proc="Sep 2026",
      what="Regulatory sandboxes, access to research infrastructure, innovation-friendly procurement and IP-backed finance.",
      track=["Sep 2026", None, None, None, None], target="—",
      latest="Proposed September 2026 (planned for Q1 2026)."),
 dict(id="euccs", name="European Critical Communication System (EUCCS)", stage="proposed", area="Connectivity", proc="COM(2026) 1010",
      what="Interconnects member states' secure communications for police, civil protection and emergency services, with satellite back-up via IRIS².",
      track=["Sep 2026", None, None, None, None], target="—",
      latest="Proposed 30 September 2026."),
 dict(id="multimodal-digital-mobility", name="Multimodal Digital Mobility Services Regulation", stage="proposed", area="Competition & Single Market", proc="May 2026",
      what="Neutral display and ranking, data sharing and emissions information for platforms that sell journeys across transport modes; SMEs excluded.",
      track=["May 2026", None, None, None, None], target="—",
      latest="Proposed 13 May 2026; would repeal the code of conduct for computerised reservation systems."),
 dict(id="single-digital-booking", name="Single Digital Booking and Ticketing", stage="proposed", area="Competition & Single Market", proc="May 2026",
      what="Single tickets for cross-border rail journeys across operators, with open APIs for schedules, fares and reservations.",
      track=["May 2026", None, None, None, None], target="—",
      latest="Proposed 13 May 2026 with the multimodal booking regulation."),
 dict(id="digital-euro", name="Digital Euro Regulation", stage="proposed", area="Finance", row=101, proc="2023/0212(COD)",
      what="Legal framework for a digital euro issued by the ECB, with legal tender status and holding limits.",
      track=["Jun 2023", "Jul 2026", "Dec 2025", "Jul 2026", None], target="End 2026",
      latest="Trilogues opened in July 2026; political agreement targeted before the end of 2026."),
 dict(id="fida", name="Financial Data Access Regulation (FiDA)", stage="withdrawn", area="Finance", row=98, proc="2023/0205(COD)",
      what="Open finance: customers can share their financial data beyond payment accounts.",
      track=["Jun 2023", "Apr 2024", "Dec 2024", "2025", None], target="—",
      latest="The Commission's 2027 work programme (Annex III) lists it for withdrawal within six months: no trilogues since June 2025, and unlikely to find support in Council."),
 dict(id="csar", name="Child Sexual Abuse Regulation (CSAR)", stage="proposed", area="Data & Privacy", row=82, proc="2022/0155(COD)",
      what="Risk assessment and detection obligations for online services to fight child sexual abuse material.",
      track=["May 2022", "Nov 2023", "Nov 2025", "2026", None], target="—",
      latest="Trilogues ended June 2026 without agreement on detection; to resume under the Irish presidency. The interim derogation was extended to April 2028."),
 dict(id="digital-travel", name="EU Digital Travel Application Regulation", stage="proposed", area="Data & Privacy", row=106, proc="2024/0670(COD)",
      what="An EU app to submit travel documents before crossing the external border.",
      track=["Oct 2024", "2025", "Nov 2025", "2026", None], target="—",
      latest="Parliament (December 2025) and Council (November 2025) have mandates; trilogues continuing, with the age limit for digital travel credentials open."),
 dict(id="space-act", name="EU Space Act", stage="proposed", area="Industrial Policy", row=107, proc="COM(2025) 335",
      what="Common rules on safety, resilience and sustainability for space operators in the EU.",
      track=["Jun 2025", None, None, None, None], target="—",
      latest="Parliament committee vote moved to November 2026; no Council general approach yet."),
 dict(id="infosec", name="Information Security Regulation", stage="proposed", area="Cybersecurity", row=79, proc="2022/0084(COD)",
      what="Common information security rules for EU institutions, bodies and agencies.",
      track=["Mar 2022", None, None, None, None], target="—",
      latest="Stalled: Parliament's committee has not yet voted, more than four years after the proposal."),
 dict(id="late-payment", name="Late Payment Regulation", stage="withdrawn", area="Competition & Single Market", row=104, proc="2023/0323(COD)",
      what="A 30-day payment cap for commercial transactions, with enforcement authorities.",
      track=["Sep 2023", "Apr 2024", None, None, None], target="—",
      latest="The Commission's 2027 work programme (Annex III) lists it for withdrawal within six months: blocked in Council since Parliament's April 2024 position, with a sizeable number of member states opposed."),
 dict(id="csa-directive", name="Child Sexual Abuse Directive (recast)", stage="agreed", area="Data & Privacy", row=105, proc="2024/0035(COD)",
      what="Updates criminal-law definitions and penalties, including for AI-generated abuse material and livestreamed abuse.",
      track=["Feb 2024", "", "", "", "Jun 2026"], target="—",
      latest="Provisional agreement on 22 June 2026; plenary vote indicatively 14 December 2026."),
 dict(id="omnibus-iv", name="Omnibus IV (small mid-caps and digital product compliance)", stage="agreed", area="Competition & Single Market", proc="COM(2025) 501",
      what="Extends SME relief to small mid-caps, narrows the GDPR record-keeping duty and moves product compliance documents to digital.",
      track=["May 2025", "", "", "", "Jun 2026"], target="End 2026",
      latest="Provisional agreement in June 2026, approved by Parliament's committees in July; plenary vote indicatively 23 November 2026."),
 dict(id="digital-fairness-act", name="Digital Fairness Act", stage="announced", area="E-commerce & Consumer Protection", proc="CWP 2026",
      what="Consumer rules on dark patterns, addictive design, unfair personalisation and subscription traps.",
      expected="11 Nov 2026 (indicative)", target="—",
      latest="On the Commission's indicative agenda for 11 November 2026, in a consumer package with the consumer enforcement initiative."),
 dict(id="quantum-act", name="Quantum Act", stage="announced", area="Industrial Policy", proc="CWP 2026",
      what="Support for quantum research, pilot lines and industrial take-up.",
      expected="18 Nov 2026 (indicative; planned Q2)", target="Q3 2027",
      latest="On the Commission's indicative agenda for 18 November 2026."),
 dict(id="cpc-review", name="Review of the Consumer Protection Cooperation Regulation", stage="announced", area="E-commerce & Consumer Protection", row=None, proc="Roadmap",
      what="Stronger EU-level enforcement of consumer law in cross-border cases.",
      expected="11 Nov 2026 (indicative)", target="Q4 2027",
      latest="On the Commission's indicative agenda for 11 November 2026 as the consumer enforcement initiative, with the Digital Fairness Act."),
 dict(id="antitrust-procedure", name="Reform of the antitrust procedural rules (Regulation 1/2003)", stage="announced", area="Competition & Single Market", row=None, proc="Review",
      what="Faster, digital-ready enforcement of Articles 101 and 102: data-preservation orders, inspection of all business records, quicker interim measures.",
      expected="Q2 2027 (planned Q3 2026)", target="—",
      latest="Evaluation and consultation done; proposal pushed to 2027."),
 dict(id="european-product-act", name="European Product Act: Standardisation Regulation", stage="proposed", area="Competition & Single Market", proc="2026/0307(COD)",
      what="First part of the European Product Act: a faster European standardisation system, with common specifications where standards are late.",
      track=["Oct 2026", None, None, None, None], target="Q4 2027",
      latest="Standardisation Regulation proposed on 6 October 2026; the parts on the product framework and market surveillance are still to come."),
 dict(id="smbpa", name="Single Market Barriers Prevention Act", stage="announced", area="Competition & Single Market", proc="CWP 2027",
      what="Screens draft national rules to stop new single-market barriers before they are adopted.",
      expected="Q3 2027", target="—",
      latest="In the 2027 work programme for Q3 2027 (legislative or non-legislative), following the Single Market Strategy."),
 dict(id="avmsd-revision", name="Revision of the Audiovisual Media Services Directive", stage="announced", area="E-commerce & Consumer Protection", row=None, proc="Evaluation",
      what="Scope for influencers, protection of minors on video-sharing platforms, prominence of general-interest content.",
      expected="After the evaluation due 19 Dec 2026", target="—",
      latest="Ex-post evaluation under Article 33 under way; a proposal may follow."),
 dict(id="data-retention", name="EU framework for data retention", stage="announced", area="Data & Privacy", row=None, proc="Impact assessment",
      what="Common rules on which data communication providers must keep for criminal investigations.",
      expected="2027 (after further assessment)", target="—",
      latest="The 2027 work programme says the Commission will further assess the impact of data retention rules, with a view to following up next year."),
 dict(id="digital-transformation-package", name="Digital transformation package, simplification and copyright", stage="announced", area="Industrial Policy", row=None, proc="CWP 2027",
      what="Review of the Digital Decade targets, further simplification of digital rules, and copyright, including AI's use of protected works.",
      expected="Q2 2027", target="—",
      latest="In the 2027 work programme as legislation with an impact assessment; scope not yet published. Copyright consultation open until 10 November 2026."),
 dict(id="political-ads-review", name="Review of the Political Advertising Regulation", stage="announced", area="E-commerce & Consumer Protection", row=None, proc="CWP 2027",
      what="A legislative review, with an impact assessment, of the 2024 rules on the transparency and targeting of political advertising.",
      expected="Not set", target="—",
      latest="In the 2027 work programme as legislation with an impact assessment; no date given."),
]
# ---------- Parliament and Council data (OEIL procedure files + hand-entered Council steps)
from forthcoming_procs import PROC, COUNCIL, PREP, OMNIBUS
OE = json.load(open("forthcoming_oeil.json"))
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
mon = lambda d: f"{MON[int(d[3:5]) - 1]} {d[6:]}"
celex = lambda ref, kind: (lambda m: f"5{m.group(1)}{kind}{m.group(2)}" if m else "")(re.match(r"(?:COM|SWD)\((\d{4})\)(\d{4})", ref))
def oe_ev(ref, *keys):
    return [e for e in OE.get(ref, {}).get("events", []) if any(k in e[1] for k in keys)]
def auto_track(f):
    refs = PROC.get(f["id"])
    if not refs:
        return f.get("track")
    r = refs[0]; t = list(f.get("track") or [None] * 5)
    pr = oe_ev(r, "Legislative proposal published")
    if pr: t[0] = mon(pr[0][0])
    ep = oe_ev(r, "Decision by Parliament, 1st reading", "confirmed by plenary")
    t[1] = mon(ep[0][0]) if ep else None
    cm = [c for c in COUNCIL.get(f["id"], []) if c[4] == "mandate"]
    t[2] = (cm[0][0][-8:] if len(cm[0][0]) > 8 else cm[0][0]) if cm else None
    ag = [c for c in COUNCIL.get(f["id"], []) if c[4] == "agreement"] or [("" if not e else mon(e[0]),) for e in oe_ev(r, "Approval in committee of the text agreed")[:1]]
    t[4] = (ag[0][0][-8:] if len(ag[0][0]) > 8 else ag[0][0]) if ag else None
    t[3] = "" if (t[1] is not None and t[2] is not None) or t[4] is not None else None
    return t
for f in F:
    if f["stage"] != "announced":
        f["track"] = auto_track(f)
def parl_docs(fid):
    out = []
    for r in PROC.get(fid, []):
        d = OE.get(r, {})
        who = (f'{d["committee"]}, rapporteur {d["rapporteur"]}' if d.get("rapporteur") else (d["committee"] or "committee responsible not yet listed")) if d else ""
        out.append(("", f"{d.get('title') or r}: {who}", r, OEIL(r)))
        for e in d.get("events", []):
            ref = e[2]
            if re.match(r"A\d+-\d{4}/\d{4}", ref):
                m = re.match(r"A(\d+)-(\d{4})/(\d{4})", ref)
                out.append((mon(e[0]), "Committee report for plenary", ref, f"https://www.europarl.europa.eu/doceo/document/A-{m.group(1)}-{m.group(3)}-{m.group(2)}_EN.html"))
            elif re.match(r"T\d+-\d{4}/\d{4}", ref):
                m = re.match(r"T(\d+)-(\d{4})/(\d{4})", ref)
                out.append((mon(e[0]), "Parliament position, first reading", ref, f"https://www.europarl.europa.eu/doceo/document/TA-{m.group(1)}-{m.group(3)}-{m.group(2)}_EN.html"))
            elif "confirmed by plenary" in e[1]:
                out.append((mon(e[0]), "Plenary confirms the mandate to negotiate with Council", "", ""))
            elif "Approval in committee of the text agreed" in e[1]:
                out.append((mon(e[0]), "Committee approves the text agreed with Council", ref, ""))
            elif "Indicative plenary" in e[1]:
                out.append((mon(e[0]), "Indicative plenary vote", "", ""))
    return out
def council_docs(fid):
    c = COUNCIL.get(fid)
    return [(d, t, r, u) for d, t, r, u, _ in c] if c else [("", "Council position", "not yet adopted", "")]
def com_docs(fid):
    out = []
    for r in PROC.get(fid, []):
        d = OE.get(r, {})
        for c in d.get("com", [])[:1]:
            pr = oe_ev(r, "Legislative proposal published")
            out.append((mon(pr[0][0]) if pr else "", f"Commission proposal: {d.get('title', '')}", re.sub(r"\)0*", ") ", c), EUR(celex(c, "PC"))))
        sw = d.get("swd", [])
        if sw:
            out.append(("", "Staff working documents: impact assessment or supporting analysis", ", ".join(re.sub(r"\)0*", ") ", x) for x in sw), EUR(celex(sw[0], "SC"))))
    return out
def omnibus_html(fid):
    o = OMNIBUS.get(fid)
    if not o:
        return ""
    rows = "".join(f'<tr><td><a href="{ACT(r)}">{esc(n)}</a></td><td class="n">{a}</td><td class="n">{b}</td><td class="n">{c}</td></tr>' for r, n, a, b, c in o["changes"])
    tot = [sum(x[i] for x in o["changes"]) for i in (2, 3, 4)]
    rep = "".join(f'<li><a href="{ACT(r)}">{esc(n)}</a> <span class="cap">· {esc(how)}</span></li>' for r, n, how in o["repeals"])
    return f'''  <section style="padding-block: 8px 40px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 14px">
      <h2 class="h2">What the omnibus would change, law by law</h2>
      <p class="body">Provisions the proposal replaces, deletes or inserts in each law on our list: {tot[0]} replaced, {tot[1]} deleted, {tot[2]} inserted.{" It also repeals " + str(len(o["repeals"])) + " laws." if o["repeals"] else ""} Counted from the amending instructions of {esc(o["source"])}.</p>
      <table class="tbl" style="max-width: 760px"><thead><tr><th>Law</th><th style="text-align: right">Replaced</th><th style="text-align: right">Deleted</th><th style="text-align: right">Inserted</th></tr></thead><tbody>{rows}</tbody></table>
      {f'<ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px">{rep}</ul>' if rep else ""}
      <p class="cap">{esc(o["other"])} A provision is an article, paragraph or point. How many obligations are removed, eased or added will be counted once the text is adopted.</p>
    </div>
  </section>
'''

STAGE = {"agreed": ("Agreed, awaiting adoption", "#2E7D5B"), "proposed": ("In negotiation", "#B8860B"), "announced": ("Announced", "#6B6B6B"), "withdrawn": ("Withdrawn", "#9B3B3B")}


def track(t, big=False):
    """Five-step horizontal track; filled dots for reached steps."""
    n = sum(x is not None for x in t)
    cells = []
    for i, (s, d) in enumerate(zip(STEPS, t)):
        on = d is not None
        dot = (f'<span style="width: {14 if big else 10}px; height: {14 if big else 10}px; border-radius: 50%; flex: none; '
               + ("background: #B8860B; border: 2px solid #B8860B" if on else "background: #FFFFFF; border: 2px solid #C9C6C3") + '"></span>')
        line = "" if i == len(STEPS) - 1 else (f'<span style="flex: 1; height: 2px; background: {"#B8860B" if on and t[i + 1] is not None else "#E0DED9"}"></span>')
        lab = (f'<span style="position: absolute; top: {20 if big else 14}px; left: 0; transform: translateX(-40%); font-size: {13 if big else 11}px; '
               f'color: {"#282424" if on else "#8A8580"}; white-space: nowrap; line-height: 1.3">{s if big else ""}'
               + (f'<br><span style="color: #666666">{esc(d)}</span>' if big and d else "") + "</span>") if big else ""
        cells.append(f'<span style="position: relative; display: flex; align-items: center; flex: {"1" if line else "none"}">{dot}{line}{lab}</span>')
    return f'<span role="img" aria-label="Reached: {esc(", ".join(s for s, d in zip(STEPS, t) if d is not None) or "none")}" style="display: flex; align-items: center; width: 100%; max-width: {640 if big else 150}px; padding-bottom: {54 if big else 0}px">{"".join(cells)}</span>'


def page_of(f):
    return ACT(f["row"]) if f.get("row") else f"Fc-{f['id']}.dc.html"


TPL = open("instrument_template.dc.html").read()
HEAD, FOOT = TPL.split("<!--BODY-->")
FOOT = re.sub(r"<script type=\"text/x-dc\".*?</script>", '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":HEIGHT}}\'>\nclass Component extends DCLogic {}\n</script>', FOOT, flags=re.S)
EXTRA_CSS = (".h1{font-family:'Source Serif 4',Georgia,serif;font-weight:400;font-size:52px;line-height:1.1;margin:0}"
             ".tab{display:inline-flex;align-items:center;padding:8px 16px;border:1px solid #D4D2CE;border-radius:999px;text-decoration:none;font-size:15px;color:#282424;min-height:40px;box-sizing:border-box}"
             ".frow{display:grid;grid-template-columns:minmax(0,2.2fr) 170px 96px 96px minmax(0,2fr);gap:20px;align-items:start;padding:16px 0;border-top:1px solid #E8E6E3}"
             "@media (max-width:900px){.frow{grid-template-columns:1fr}}")


def shell(title, body, h):
    head = HEAD.replace("<title>Digital Markets Act</title>", f"<title>{esc(title)}</title>").replace("</style>", EXTRA_CSS + "</style>")
    return head + body + FOOT.replace("HEIGHT", str(h))


TABS = [("Instruments.dc.html", "Legal instruments"), ("Forthcoming.dc.html", "Forthcoming"), ("DigitalPolicy.dc.html", "Digital policy")]


def tabs(cur):
    return ('<nav aria-label="Digital Acquis" style="display: flex; flex-wrap: wrap; gap: 10px">' + "".join(
        f'<a class="tab" href="{f}"' + (' style="background: #282424; color: #FAF9F5; border-color: #282424" aria-current="page"' if f == cur else "") + f">{n}</a>"
        for f, n in TABS) + "</nav>")


# ---------- list page
def row(f):
    lab, col = STAGE[f["stage"]]
    tr = track(f["track"]) if f["stage"] != "announced" else f'<span class="cap">Proposal expected:<br><strong style="font-weight: 600; color: #282424">{esc(f["expected"])}</strong></span>'
    prop = f["track"][0] if f.get("track") else "—"
    chk = ' <span class="st" style="border-color: #C0392B; color: #C0392B">to verify</span>' if f.get("check") else ""
    return (f'<div class="frow"><div><a href="{page_of(f)}" style="font-family: \'Source Serif 4\', Georgia, serif; font-size: 20px; line-height: 1.25; text-decoration: none">{esc(f["name"])} →</a>{chk}'
            f'<span class="small" style="font-size: 14px; color: #3F3B3B">{esc(f["what"])}</span><span class="small">{esc(f["area"])}'
            + f'</span></div>'
            f'<div style="padding-top: 8px">{tr}</div><div class="cap" style="padding-top: 4px">{esc(prop)}</div><div class="cap" style="padding-top: 4px">{esc(f["target"])}</div>'
            f'<div class="cap" style="padding-top: 4px; color: #3F3B3B">{esc(f["latest"])}</div></div>')


groups = [("agreed", "Agreed, awaiting formal adoption", "Parliament and Council have reached a provisional agreement; the text still needs formal adoption by both.", "agreed", "#F3F1EC", "#2E7D5B"),
          ("proposed", "In negotiation", "Proposed by the Commission and being negotiated by Parliament and Council.", "negotiation", "#FFFFFF", "#B8860B"),
          ("announced", "Announced", "In the Commission work programme or the One Europe, One Market roadmap, but not yet proposed.", "announced", "#F3F1EC", "#6B6B6B"),
          ("withdrawn", "Withdrawn", "Proposals the Commission has withdrawn or listed for withdrawal. Not counted among the initiatives above.", "withdrawn", "#FFFFFF", "#9B3B3B")]
cnt = {k: sum(f["stage"] == k for f in F) for k, *_ in groups}
stat = "".join(f'<a href="#{anc}" style="display: flex; flex-direction: column; gap: 4px; padding: 18px 20px; border: 1px solid #E8E6E3; border-top: 4px solid {col}; border-radius: 12px; background: #FFFFFF; min-width: 200px; text-decoration: none; color: #282424">'
               f'<span class="num">{cnt[k]}</span><span class="cap">{t.lower()}</span><span class="cap" style="color: #8F6708; font-weight: 500">See the list ↓</span></a>' for k, t, _, anc, _, col in groups)
secs = ""
for k, t, d, anc, bg, col in groups:
    xs = [f for f in F if f["stage"] == k]
    hdr = ('<div class="frow" style="border-top: 0; padding-bottom: 6px"><span class="eyebrow" style="font-size: 12px">Initiative</span>'
           f'<span class="eyebrow" style="font-size: 12px">{"Stage" if k != "announced" else "Timing"}</span><span class="eyebrow" style="font-size: 12px">{"Proposed" if k != "announced" else ""}</span>'
           '<span class="eyebrow" style="font-size: 12px">Target for agreement</span><span class="eyebrow" style="font-size: 12px">Latest</span></div>')
    secs += (f'<section id="{anc}" style="background: {bg}; border-top: 1px solid #E8E6E3; padding-block: 44px 48px; scroll-margin-top: 16px"><div class="wrap" style="display: flex; flex-direction: column; gap: 8px">'
             f'<h2 class="h2" style="--bar: {col}">{t} <span class="cap" style="font-size: 18px">· {len(xs)}</span></h2><p class="cap">{d}</p>'
             f'<div style="margin-top: 8px">{hdr}{"".join(row(f) for f in xs)}</div></div></section>')
legend = ('<div style="display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: center" class="cap"><span>Stage dots:</span>'
          + "".join(f'<span>{i + 1}. {s}</span>' for i, s in enumerate(STEPS)) + "</div>")
body = f'''
  <section style="padding-block: 64px 32px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      {tabs("Forthcoming.dc.html")}
      <p class="eyebrow">Digital Acquis · Forthcoming</p>
      <h1 class="h1">{sum(f["stage"] != "withdrawn" for f in F)} digital initiatives not yet adopted</h1>
      <p class="body">Proposals still being negotiated and initiatives the Commission has announced but not yet proposed, with where each stands and the documents behind it. Targets for agreement are from the One Europe, One Market roadmap (April 2026). Status as of {AS_OF}.</p>
      <div style="display: flex; flex-wrap: wrap; gap: 14px">{stat}</div>
      {legend}
    </div>
  </section>
{secs}
'''
OUT = "mockup"
open(f"{OUT}/Forthcoming.dc.html", "w").write(shell("Forthcoming", body, 6000))


# ---------- initiative pages (two prototypes)
def doc_list(groups):
    out = ""
    for g, items in groups:
        out += (f'<div style="display: flex; flex-direction: column; gap: 4px"><p class="eyebrow" style="font-size: 12px">{esc(g)}</p><ul class="lst" style="padding: 0">'
                + "".join(f'<li><span class="cap">{esc(d)}</span><span>' + (f'<a href="{u}">{esc(t)}</a>' if u else esc(t)) + (f' <span class="cap">· {esc(r)}</span>' if r else "") + "</span></li>" for d, t, r, u in items)
                + "</ul></div>")
    return out


def fpage(f, sub, intro, does, changes, docs, docs_title, docs_note, extra=""):
    lab, col = STAGE[f["stage"]]
    if f["stage"] == "announced":
        where = (f'<div style="display: flex; flex-wrap: wrap; gap: 14px">'
                 + "".join(f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 16px 18px; border: 1px solid #E8E6E3; border-radius: 12px; background: #FFFFFF; min-width: 200px"><span class="cap">{a}</span><span style="font-family: \'Source Serif 4\', Georgia, serif; font-size: 22px">{b}</span></div>'
                          for a, b in sub) + "</div>")
    else:
        where = track(f["track"], big=True)
    chg = "".join(f'<li style="display: block"><a href="{u}">{esc(t)}</a> <span class="cap">· {esc(how)}</span></li>' for t, how, u in changes)
    body = f'''
  <section style="padding-block: 48px 24px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 16px">
      <p class="cap"><a href="Instruments.dc.html">Digital Acquis</a> / <a href="Forthcoming.dc.html">Forthcoming</a></p>
      <h1 class="h1" style="font-size: 46px">{esc(f["name"])}</h1>
      <div style="display: flex; flex-wrap: wrap; gap: 8px"><span class="chip" style="border-color: {col}; color: {col}; font-weight: 600">{lab}</span><span class="chip">{esc(f["area"])}</span><span class="chip">{esc(f["proc"])}</span>{"".join(f'<span class="chip">{esc(c)}</span>' for c in f.get("chips", []))}</div>
      <p class="body" style="font-size: 19px">{intro}</p>
      <p class="cap">Von der Leyen II Commission · part of the <a href="DigitalPolicy.dc.html#era-competitiveness">Competitiveness · One Europe, One Market</a> agenda</p>
    </div>
  </section>
  <section style="padding-block: 24px 40px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 18px">
      <h2 class="h2">Where it stands</h2>
      {where}
      <div style="padding: 16px 20px; border-left: 3px solid #B8860B; background: #FFFFFF; border-radius: 0 12px 12px 0"><p class="eyebrow" style="font-size: 12px">Latest · {AS_OF}</p><p class="body" style="margin-top: 6px">{f["latest_long"]}</p></div>
    </div>
  </section>
  <section style="padding-block: 24px 40px">
    <div class="wrap" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 40px">
      <div style="display: flex; flex-direction: column; gap: 12px"><h2 class="h3">What it would do</h2><ul class="body" style="padding-left: 20px; margin: 0; display: flex; flex-direction: column; gap: 6px">{"".join(f"<li>{d}</li>" for d in does)}</ul></div>
      <div style="display: flex; flex-direction: column; gap: 12px"><h2 class="h3">What it would change in the Digital Acquis</h2><ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px">{chg}</ul></div>
    </div>
  </section>
  {extra}
  <section style="padding-block: 24px 72px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 16px">
      <h2 class="h2">{docs_title}</h2>
      <p class="cap">{docs_note}</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 28px">{doc_list(docs)}</div>
    </div>
  </section>
'''
    open(f"{OUT}/Fc-{f['id']}.dc.html", "w").write(shell(f["name"], body, 2600))


dna = next(f for f in F if f["id"] == "digital-networks-act")
dna["chips"] = ["Regulation", "Target for agreement: Q4 2027"]
dna["latest_long"] = ("Parliament has referred the proposal to its Industry committee (ITRE), with Michał Kobosko (Renew) as rapporteur; IMCO and LIBE give opinions. "
                      "In Council, the Cyprus presidency presented a progress report to the Telecoms Council of 8–9 June 2026: delegations back the aims but several question the shift to EU-level spectrum coordination and the reliance on implementing acts. "
                      "Neither institution has adopted a position yet.")
fpage(dna, None,
      "Turns the European Electronic Communications Code into a directly applicable regulation and adds EU-level coordination of spectrum, a timetable for switching off copper networks and a lighter single authorisation for operators.",
      ["One regulation in place of the telecoms code and the BEREC Regulation.", "EU-wide coordination of spectrum assignment and longer licence durations.",
       "A planned switch-off of copper networks by 2030–35.", "A single EU authorisation for operators active in several member states.", "Keeps the open internet rules."],
      [("European Electronic Communications Code", "repealed and replaced", ACT(32)),
       ("Open Internet Access Regulation", "amended", "Act-open-internet-access-regulation.dc.html"),
       ("Radio Spectrum Decision", "amended", "Act-radio-spectrum-decision.dc.html"),
       ("ePrivacy Directive", "amended", "Act-eprivacy-directive.dc.html")],
      [("Commission", [("Feb 2024", "White Paper: How to master Europe's digital infrastructure needs?", "COM(2024) 81", EUR("52024DC0081"))] + com_docs("digital-networks-act")),
       ("European Parliament", parl_docs("digital-networks-act")), ("Council", council_docs("digital-networks-act")),
       ("Other opinions", [("Mar 2026", "European Data Protection Supervisor opinion", "EDPS", ""), ("Jun 2026", "European Economic and Social Committee opinion", "TEN/879", "")])],
      "Key documents", "Commission proposal and impact assessment, then the reports and positions of Parliament and Council as they appear.")

dfa = next(f for f in F if f["id"] == "digital-fairness-act")
dfa["chips"] = ["Likely a regulation or amending directive"]
dfa["latest_long"] = ("The Commission's public consultation and call for evidence ran from 17 July to 24 October 2025 and drew over 4,000 replies; a factual summary was published in December 2025. "
                      "The proposal is in the 2026 work programme for the fourth quarter of 2026, and the Commission's indicative agenda of 20 October 2026 schedules it for 11 November 2026, in a consumer package with a consumer enforcement initiative. No impact assessment has been published yet.")
fpage(dfa, [("Announced in", "Work programme 2026"), ("Consultation", "Jul – Oct 2025"), ("Proposal expected", "11 Nov 2026 (indicative)")],
      "Planned consumer rules for online practices the current law handles poorly: dark patterns, addictive design, unfair personalisation, influencer marketing and subscription traps.",
      ["Ban or restrict dark patterns and addictive design features.", "Rules on personalised pricing and advertising based on vulnerabilities.",
       "Easier cancellation of subscriptions and limits on auto-renewal traps.", "Clearer duties for influencer marketing.", "Possibly a shift of the burden of proof in digital cases."],
      [("Unfair Commercial Practices Directive", "likely amended", "Act-unfair-commercial-practices-directive.dc.html"),
       ("Consumer Rights Directive", "likely amended", "Act-consumer-rights-directive.dc.html"),
       ("Unfair Contract Terms Directive", "likely amended", "Act-unfair-contract-terms-directive.dc.html"),
       ("Digital Services Act", "overlaps on dark patterns", "Act-digital-services-act.dc.html")],
      [("Preparatory work", [("Oct 2024", "Fitness check of EU consumer law on digital fairness", "SWD(2024) 230", "https://commission.europa.eu/law/law-topic/consumer-protection-law/review-eu-consumer-law_en"),
                             ("Oct 2026", "Towards a digital fairness act", "EPRS briefing", "https://eprs.europarl.europa.eu/contents/publications/EPRS/2026/10/EPRS_BRI(2026)791529.html")]),
       ("Consultation", [("Jul 2025", "Public consultation and call for evidence", "closed 24 Oct 2025", "https://digital-strategy.ec.europa.eu/en/consultations/commission-launches-open-consultation-forthcoming-digital-fairness-act"),
                         ("Dec 2025", "Factual summary report of the consultation", "Commission", "")]),
       ("Planning", [("Oct 2025", "Commission work programme 2026", "COM(2025) 870", EUR("52025DC0870")),
                     ("Oct 2026", "Indicative Commission agenda, 27 October to 24 November 2026", "SEC(2026) 2581", "https://ec.europa.eu/transparency/documents-register/detail?ref=SEC(2026)2581&lang=en")])],
      "Preparatory studies and consultations", "Until the proposal is published there is no impact assessment; these are the studies and consultations it will build on.")

# ---------- all other initiative pages, from forthcoming_details.py
from forthcoming_details import D
SRC = json.load(open("forthcoming_sources.json"))
CWP26 = ("Oct 2025", "Commission work programme 2026", "COM(2025) 870", EUR("52025DC0870"))
ROADMAP = ("Apr 2026", "One Europe, One Market roadmap", "Parliament, Council and Commission", "https://commission.europa.eu/topics/competitiveness/one-europe-one-market-roadmap_en")
# indicative list of items for Commission meetings (Secretariat-General); ids listed are scheduled in it
AGENDA = ("Oct 2026", "Indicative Commission agenda, 27 October to 24 November 2026", "SEC(2026) 2581", "https://ec.europa.eu/transparency/documents-register/detail?ref=SEC(2026)2581&lang=en")
ON_AGENDA = {"digital-fairness-act", "cpc-review", "quantum-act"}
# Commission work programme 2027: adoption due 4 November 2026. Check the reference and link against the adopted text.
CWP27 = ("Nov 2026", "Commission work programme 2027", "COM(2026) 710", EUR("52026DC0710"))
PLAN = {"smbpa": [CWP27, ROADMAP], "data-retention": [CWP27]}
OEIL_OK = lambda pr: bool(re.match(r"\d{4}/\d{4}\(COD\)", pr or ""))
for f in F:
    if f.get("row") or f["id"] in ("digital-networks-act", "digital-fairness-act"):
        continue
    d = D[f["id"]]
    src = SRC.get(f["id"], {})
    links = src.get("sources", [])
    f["latest_long"] = d["latest"]
    chg = [(n, how, ACT(r)) for n, how, r in d["changes"]] or [("No law in the current Digital Acquis", "a new instrument", "Instruments.dc.html")]
    if f["stage"] == "announced":
        prep = [("", t if t != "Official source" else "Commission page on the initiative", "Commission", u) for t, u in links] + PREP.get(f["id"], [])
        docs = [("Preparatory work and consultations", prep or [("", "No preparatory documents published yet", "", "")]), ("Planning", PLAN.get(f["id"]) or ([CWP27] if f["proc"] == "CWP 2027" else [CWP26, ROADMAP] + ([AGENDA] if f["id"] in ON_AGENDA else [])))]
        sub = [("Announced in", {"CWP 2026": "Work programme 2026", "CWP 2027": "Work programme 2027"}.get(f["proc"], f["proc"])), ("Proposal expected", f["expected"]), ("Target for agreement", f["target"] if f["target"] != "—" else "not set")]
        fpage(f, sub, d["intro"], d["does"], chg, docs, "Preparatory studies and consultations",
              "Until the proposal is published there is no impact assessment; these are the documents it will build on.")
    else:
        com = com_docs(f["id"]) or [(d.get("date", ""), "Commission proposal", d.get("ref", ""), EUR(d["eurlex"]) if d.get("eurlex") else (links[0][1] if links else ""))]
        com += [("", t, "Commission", u) for t, u in links[1:]]
        docs = [("Commission", com), ("European Parliament", parl_docs(f["id"]) or [("", "Not yet referred to a committee", "", "")]), ("Council", council_docs(f["id"])), ("Planning", [ROADMAP])]
        fpage(f, None, d["intro"], d["does"], chg, docs, "Key documents",
              "The Commission proposal and impact assessment, then the reports and positions of Parliament and Council as they appear. Parliament steps from the Legislative Observatory.", extra=omnibus_html(f["id"]))

# ---------- status blocks for pending acts that already have an instrument page
def eurproc(pr):
    m = re.match(r"(\d{4})/(\d{4})\(COD\)", pr or "")
    return f"https://eur-lex.europa.eu/procedure/EN/{m.group(1)}_{int(m.group(2))}" if m else ""
STAND = {}
for f in F:
    if not f.get("row"):
        continue
    lab, col = STAGE[f["stage"]]
    dl = ""
    grp = [("Commission", com_docs(f["id"])), ("European Parliament", parl_docs(f["id"])), ("Council", council_docs(f["id"]))]
    dl = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 24px">' + doc_list(grp) + "</div>"
    STAND[f["row"]] = f'''  <section style="padding-block: 40px 8px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 16px">
      <div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 12px"><h2 class="h2">Where it stands</h2><span class="chip" style="border-color: {col}; color: {col}; font-weight: 600">{lab}</span><a class="cap" href="Forthcoming.dc.html">All forthcoming initiatives →</a></div>
      {track(f["track"], big=True)}
      <div style="padding: 16px 20px; border-left: 3px solid #B8860B; background: #FFFFFF; border-radius: 0 12px 12px 0"><p class="eyebrow" style="font-size: 12px">Latest · {AS_OF}</p><p class="body" style="margin-top: 6px">{esc(f["latest"])}</p></div>
      {dl}
    </div>
  </section>
'''
json.dump(STAND, open("forthcoming.json", "w"), indent=1)
STEP_KEYS = ["proposal", "parliament_position", "council_position", "trilogues", "agreement"]
json.dump([dict(id=f["id"], name=f["name"], stage=f["stage"], law_id=f.get("row"), policy_area=f["area"], procedure=", ".join(PROC.get(f["id"], [])) or f["proc"],
                **({k: (v if v is not None else "") for k, v in zip(STEP_KEYS, f["track"])} if f.get("track") else {k: "" for k in STEP_KEYS}),
                expected_proposal=f.get("expected", ""), target_for_agreement=f["target"], latest=f["latest"], page=page_of(f)) for f in F],
          open("forthcoming_list.json", "w"), indent=1, ensure_ascii=False)
json.dump({str(f["row"]): f["stage"] if f["stage"] in ("agreed", "withdrawn") else "proposed" for f in F if f.get("row")}, open("forthcoming_status.json", "w"), indent=1)
print("ok", len(F), "Fc pages:", sum(1 for f in F if not f.get("row")), "status blocks:", len(STAND))
