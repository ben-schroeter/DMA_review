"""Builds Digital Acquis > Forthcoming (list of proposed and announced initiatives not yet adopted) and one page per
initiative. Writes to site/mockup/ and site/forthcoming.json (status blocks for pending acts in the CEPS list). Run from research/ceps_metrics/site."""
import html, json, os, re

esc = lambda s: html.escape(s, quote=True)
EUR = lambda c: f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{c}"
OEIL = lambda p: f"https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference={p}"
PAGES = json.load(open("instrument_pages.json"))  # row_id -> Act page
ACT = lambda rid: PAGES[str(rid)]
AS_OF = "October 2026"

STEPS = ["Proposal", "Parliament position", "Council position", "Trilogues", "Agreement"]
# track: list of dates (or "" if done without a date, None if not reached), one per step

F = [
 # --- agreed, awaiting formal adoption
 dict(id="psr", name="Payment Services Regulation (PSR)", stage="agreed", area="Finance", row=99, proc="2023/0210(COD)",
      what="Directly applicable rules for payment services: fraud prevention, IBAN checks, open banking access.",
      track=["Jun 2023", "Apr 2024", "Jun 2025", "2025", "Apr 2026"], target="—",
      latest="Provisional agreement reached; awaiting formal adoption by Parliament and Council."),
 dict(id="psd3", name="Payment Services Directive 3 (PSD3)", stage="agreed", area="Finance", row=100, proc="2023/0209(COD)",
      what="Licensing and supervision of payment and e-money institutions.",
      track=["Jun 2023", "Apr 2024", "Jun 2025", "2025", "Apr 2026"], target="—",
      latest="Agreed together with the PSR; awaiting formal adoption."),
 # --- proposed, in negotiation
 dict(id="digital-omnibus", name="Digital Omnibus (data, privacy, cybersecurity)", stage="proposed", area="Data & Privacy", proc="COM(2025) 837",
      what="Amends the GDPR, ePrivacy rules, the Data Act and incident reporting to cut compliance costs.",
      track=["Nov 2025", None, "Oct 2026", None, None], target="End 2026",
      latest="Council agreed its mandate in October 2026; Parliament committees are still voting on amendments. The AI part was adopted separately (Regulation (EU) 2026/1744, in force July 2026)."),
 dict(id="business-wallet", name="European Business Wallet", stage="proposed", area="Competition & Single Market", proc="Nov 2025",
      what="A digital wallet for companies to identify themselves, sign and exchange documents with authorities across the EU.",
      track=["Nov 2025", None, None, None, None], target="End 2026",
      latest="Council working party is negotiating a compromise text (June 2026)."),
 dict(id="digital-networks-act", name="Digital Networks Act", stage="proposed", area="Connectivity", proc="2026/0013(COD)",
      what="Replaces the telecoms code with a single regulation: EU-wide spectrum coordination, copper switch-off, lighter authorisation.",
      track=["Jan 2026", None, None, None, None], target="Q4 2027",
      latest="Parliament: ITRE lead, rapporteur Michał Kobosko. Council: progress report to the June 2026 Telecoms Council."),
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
 dict(id="fida", name="Financial Data Access Regulation (FiDA)", stage="proposed", area="Finance", row=98, proc="2023/0205(COD)",
      what="Open finance: customers can share their financial data beyond payment accounts.",
      track=["Jun 2023", "Apr 2024", "Dec 2024", "2025", None], target="—",
      latest="Trilogues stalled since October 2025; kept on the 2026 work programme as pending."),
 dict(id="csar", name="Child Sexual Abuse Regulation (CSAR)", stage="proposed", area="Data & Privacy", row=82, proc="2022/0155(COD)",
      what="Risk assessment and detection obligations for online services to fight child sexual abuse material.",
      track=["May 2022", "Nov 2023", "Nov 2025", "2026", None], target="—",
      latest="Trilogues ended June 2026 without agreement on detection; to resume under the Irish presidency. The interim derogation was extended to April 2028."),
 dict(id="digital-travel", name="EU Digital Travel Application Regulation", stage="proposed", area="Data & Privacy", row=106, proc="2024/0670(COD)",
      what="An EU app to submit travel documents before crossing the external border.",
      track=["Oct 2024", "2025", "Nov 2025", "2026", None], target="—",
      latest="Trilogues continuing (second round May 2026); age limit for digital travel credentials open."),
 dict(id="space-act", name="EU Space Act", stage="proposed", area="Industrial Policy", row=107, proc="COM(2025) 335",
      what="Common rules on safety, resilience and sustainability for space operators in the EU.",
      track=["Jun 2025", None, None, None, None], target="—",
      latest="Parliament committee vote moved to November 2026; no Council general approach yet."),
 dict(id="infosec", name="Information Security Regulation", stage="proposed", area="Cybersecurity", row=79, proc="2022/0084(COD)",
      what="Common information security rules for EU institutions, bodies and agencies.",
      track=["Mar 2022", None, None, None, None], target="—",
      latest="Stalled: Parliament's committee has not yet voted, more than four years after the proposal."),
 dict(id="late-payment", name="Late Payment Regulation", stage="proposed", area="Competition & Single Market", row=104, proc="2023/0323(COD)",
      what="A 30-day payment cap for commercial transactions, with enforcement authorities.",
      track=["Sep 2023", "Apr 2024", None, None, None], target="—",
      latest="Blocked in Council since Parliament's April 2024 position; 2026 reports say the Commission intends to withdraw it."),
 dict(id="csa-directive", name="Child Sexual Abuse Directive (recast)", stage="agreed", area="Data & Privacy", row=105, proc="2024/0035(COD)",
      what="Updates criminal-law definitions and penalties, including for AI-generated abuse material and livestreamed abuse.",
      track=["Feb 2024", "", "", "", "Jun 2026"], target="—",
      latest="Provisional agreement on 22 June 2026; awaiting formal adoption."),
 dict(id="omnibus-iv", name="Omnibus IV (small mid-caps and digital product compliance)", stage="agreed", area="Competition & Single Market", proc="COM(2025) 501",
      what="Extends SME relief to small mid-caps, narrows the GDPR record-keeping duty and moves product compliance documents to digital.",
      track=["May 2025", "", "", "", "Jun 2026"], target="End 2026",
      latest="Provisional agreement reported on 9 June 2026; Parliament plenary vote indicatively 23 November 2026."),
 dict(id="digital-fairness-act", name="Digital Fairness Act", stage="announced", area="E-commerce & Consumer Protection", proc="CWP 2026",
      what="Consumer rules on dark patterns, addictive design, unfair personalisation and subscription traps.",
      expected="Q4 2026", target="—",
      latest="Consultation closed October 2025 (over 4,000 replies); proposal expected Q4 2026."),
 dict(id="quantum-act", name="Quantum Act", stage="announced", area="Industrial Policy", proc="CWP 2026",
      what="Support for quantum research, pilot lines and industrial take-up.",
      expected="Q4 2026 (planned Q2)", target="Q3 2027",
      latest="Consultation held in 2025; proposal not yet adopted."),
 dict(id="cpc-review", name="Review of the Consumer Protection Cooperation Regulation", stage="announced", area="E-commerce & Consumer Protection", row=None, proc="Roadmap",
      what="Stronger EU-level enforcement of consumer law in cross-border cases.",
      expected="By Q4 2026", target="Q4 2027",
      latest="Listed in the One Europe, One Market roadmap."),
 dict(id="antitrust-procedure", name="Reform of the antitrust procedural rules (Regulation 1/2003)", stage="announced", area="Competition & Single Market", row=None, proc="Review",
      what="Faster, digital-ready enforcement of Articles 101 and 102: data-preservation orders, inspection of all business records, quicker interim measures.",
      expected="Q2 2027 (planned Q3 2026)", target="—",
      latest="Evaluation and consultation done; proposal pushed to 2027."),
 dict(id="european-product-act", name="European Product Act", stage="announced", area="Competition & Single Market", proc="CWP 2026",
      what="Overhauls the framework for EU product laws, market surveillance and standardisation.",
      expected="Q3 2026, delayed", target="Q4 2027",
      latest="Scheduled for Q3 2026; not yet proposed."),
 dict(id="smbpa", name="Single Market Barriers Prevention Act", stage="announced", area="Competition & Single Market", proc="Single Market Strategy",
      what="Screens draft national rules to stop new single-market barriers before they are adopted.",
      expected="Q3 2027", target="—",
      latest="Announced in the Single Market Strategy."),
 dict(id="avmsd-revision", name="Revision of the Audiovisual Media Services Directive", stage="announced", area="E-commerce & Consumer Protection", row=None, proc="Evaluation",
      what="Scope for influencers, protection of minors on video-sharing platforms, prominence of general-interest content.",
      expected="After the evaluation due 19 Dec 2026", target="—",
      latest="Ex-post evaluation under Article 33 under way; a proposal may follow."),
 dict(id="data-retention", name="EU framework for data retention", stage="announced", area="Data & Privacy", row=None, proc="Impact assessment",
      what="Common rules on which data communication providers must keep for criminal investigations.",
      expected="Q4 2026", target="—",
      latest="Commission preparing an impact assessment; consultation held."),
]
STAGE = {"agreed": ("Agreed, awaiting adoption", "#2E7D5B"), "proposed": ("In negotiation", "#B8860B"), "announced": ("Announced", "#6B6B6B")}


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


TABS = [("Instruments.dc.html", "Legal instruments"), ("DigitalPolicy.dc.html", "Digital policy"), ("Forthcoming.dc.html", "Forthcoming")]


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
            + (" · in the CEPS list" if f.get("row") else "") + f'</span></div>'
            f'<div style="padding-top: 8px">{tr}</div><div class="cap" style="padding-top: 4px">{esc(prop)}</div><div class="cap" style="padding-top: 4px">{esc(f["target"])}</div>'
            f'<div class="cap" style="padding-top: 4px; color: #3F3B3B">{esc(f["latest"])}</div></div>')


groups = [("proposed", "In negotiation", "Proposed by the Commission and being negotiated by Parliament and Council."),
          ("agreed", "Agreed, awaiting formal adoption", "Parliament and Council have reached a provisional agreement."),
          ("announced", "Announced", "In the Commission work programme or the One Europe, One Market roadmap, but not yet proposed.")]
cnt = {k: sum(f["stage"] == k for f in F) for k, _, _ in groups}
stat = "".join(f'<div style="display: flex; flex-direction: column; gap: 4px; padding: 18px 20px; border: 1px solid #E8E6E3; border-radius: 12px; background: #FFFFFF; min-width: 180px">'
               f'<span class="num">{cnt[k]}</span><span class="cap">{t.lower() if k != "agreed" else "agreed, awaiting adoption"}</span></div>' for k, t, _ in groups)
secs = ""
for k, t, d in groups:
    xs = [f for f in F if f["stage"] == k]
    hdr = ('<div class="frow" style="border-top: 0; padding-bottom: 6px"><span class="eyebrow" style="font-size: 12px">Initiative</span>'
           f'<span class="eyebrow" style="font-size: 12px">{"Stage" if k != "announced" else "Timing"}</span><span class="eyebrow" style="font-size: 12px">{"Proposed" if k != "announced" else ""}</span>'
           '<span class="eyebrow" style="font-size: 12px">Target for agreement</span><span class="eyebrow" style="font-size: 12px">Latest</span></div>')
    secs += (f'<section style="padding-block: 0 48px"><div class="wrap" style="display: flex; flex-direction: column; gap: 8px">'
             f'<h2 class="h2">{t} <span class="cap" style="font-size: 18px">· {len(xs)}</span></h2><p class="cap">{d}</p>'
             f'<div style="margin-top: 8px">{hdr}{"".join(row(f) for f in xs)}</div></div></section>')
legend = ('<div style="display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: center" class="cap"><span>Stage dots:</span>'
          + "".join(f'<span>{i + 1}. {s}</span>' for i, s in enumerate(STEPS)) + "</div>")
body = f'''
  <section style="padding-block: 64px 32px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      {tabs("Forthcoming.dc.html")}
      <p class="eyebrow">Digital Acquis · Forthcoming</p>
      <h1 class="h1">{len(F)} digital initiatives not yet adopted</h1>
      <p class="body">Proposals still being negotiated and initiatives the Commission has announced but not yet proposed, with where each stands and the documents behind it. Targets for agreement are from the One Europe, One Market roadmap (April 2026). Status as of {AS_OF}.</p>
      <div style="display: flex; flex-wrap: wrap; gap: 14px">{stat}</div>
      {legend}
    </div>
  </section>
{secs}
  <section style="padding-block: 0 72px"><div class="wrap"><p class="cap">Recently adopted, so no longer listed: Digital Omnibus on AI (Regulation (EU) 2026/1744, in force 27 July 2026) and the EuroHPC amendment for AI Gigafactories and quantum (Council, 16 January 2026). Both postdate the CEPS list.</p></div></section>
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
      [("Commission", [("Feb 2024", "White Paper: How to master Europe's digital infrastructure needs?", "COM(2024) 81", EUR("52024DC0081")),
                       ("Jan 2026", "Proposal for a Digital Networks Act", "COM(2026) 16", EUR("52026PC0016")),
                       ("Jan 2026", "Impact assessment and Regulatory Scrutiny Board opinion", "SWD", "https://www.parlament.gv.at/gegenstand/XXVIII/EU/54732")]),
       ("European Parliament", [("2026", "Procedure file 2026/0013(COD): ITRE, rapporteur Michał Kobosko", "Legislative Observatory", OEIL("2026/0013(COD)")),
                                ("", "Draft report", "not yet published", "")]),
       ("Council", [("May 2026", "Progress report", "ST 8523/26", "https://data.consilium.europa.eu/doc/document/ST-8523-2026-INIT/en/pdf"),
                    ("Jun 2026", "Note to the Telecoms Council of 8–9 June", "ST 9685/26", "https://data.consilium.europa.eu/doc/document/ST-9685-2026-INIT/en/pdf")]),
       ("Other opinions", [("Mar 2026", "European Data Protection Supervisor opinion", "EDPS", ""), ("Jun 2026", "European Economic and Social Committee opinion", "TEN/879", "")])],
      "Key documents", "Commission proposal and impact assessment, then the reports and positions of Parliament and Council as they appear.")

dfa = next(f for f in F if f["id"] == "digital-fairness-act")
dfa["chips"] = ["Likely a regulation or amending directive"]
dfa["latest_long"] = ("The Commission's public consultation and call for evidence ran from 17 July to 24 October 2025 and drew over 4,000 replies; a factual summary was published in December 2025. "
                      "The proposal is in the 2026 work programme for the fourth quarter of 2026. No impact assessment has been published yet.")
fpage(dfa, [("Announced in", "Work programme 2026"), ("Consultation", "Jul – Oct 2025"), ("Proposal expected", "Q4 2026")],
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
       ("Planning", [("Oct 2025", "Commission work programme 2026", "COM(2025) 870", EUR("52025DC0870"))])],
      "Preparatory studies and consultations", "Until the proposal is published there is no impact assessment; these are the studies and consultations it will build on.")

# ---------- all other initiative pages, from forthcoming_details.py
from forthcoming_details import D
SRC = json.load(open("forthcoming_sources.json"))
CWP26 = ("Oct 2025", "Commission work programme 2026", "COM(2025) 870", EUR("52025DC0870"))
ROADMAP = ("Apr 2026", "One Europe, One Market roadmap", "Parliament, Council and Commission", "https://commission.europa.eu/topics/competitiveness/one-europe-one-market-roadmap_en")
OEIL_OK = lambda pr: bool(re.match(r"\d{4}/\d{4}\(COD\)", pr or ""))
for f in F:
    if f.get("row") or f["id"] in ("digital-networks-act", "digital-fairness-act"):
        continue
    d = D[f["id"]]
    src = SRC.get(f["id"], {})
    links = src.get("sources", [])
    f["latest_long"] = d["latest"]
    chg = [(n, how, ACT(r)) for n, how, r in d["changes"]] or [("No law in the current Digital Acquis", "a new instrument", "Instruments.dc.html")]
    tracker = [("", "Digital Acquis tracker entry", "digital-acquis.eu (Kai Zenner, Digital Policy Alert, TUM Think Tank)", src["tracker"])] if src.get("tracker") else []
    if f["stage"] == "announced":
        prep = [("", t if t != "Official source" else "Commission page on the initiative", "Commission", u) for t, u in links]
        docs = [("Preparatory work and consultations", prep or [("", "No preparatory documents published yet", "", "")]), ("Planning", [CWP26, ROADMAP] + tracker)]
        sub = [("Announced in", "Work programme 2026" if f["proc"] == "CWP 2026" else f["proc"]), ("Proposal expected", f["expected"]), ("Target for agreement", f["target"] if f["target"] != "—" else "not set")]
        fpage(f, sub, d["intro"], d["does"], chg, docs, "Preparatory studies and consultations",
              "Until the proposal is published there is no impact assessment; these are the documents it will build on.")
    else:
        url = EUR(d["eurlex"]) if d.get("eurlex") else (links[0][1] if links else "")
        com = [(d["date"], "Commission proposal", d["ref"], url)] + [("", t, "Commission", u) for t, u in links[1:]]
        pc = []
        if OEIL_OK(f["proc"]):
            pc.append(("", f"Procedure file {f['proc']}", "Legislative Observatory", OEIL(f["proc"])))
        if f["id"] == "digital-omnibus":
            pc.append(("Oct 2026", "Council negotiating mandate", "agreed 21 October 2026", ""))
            pc.append(("", "Parliament report", "in committee", ""))
        elif f["stage"] == "agreed":
            pc.append(("Jun 2026", "Provisional agreement", "awaiting formal adoption", ""))
        else:
            pc.append(("", "Parliament report and Council position", "not yet adopted", ""))
        docs = [("Commission", com), ("Parliament and Council", pc), ("Planning", [ROADMAP] + tracker)]
        fpage(f, None, d["intro"], d["does"], chg, docs, "Key documents",
              "The Commission proposal, then the reports and positions of Parliament and Council as they appear.")

# ---------- status blocks for pending acts that already have an instrument page
def eurproc(pr):
    m = re.match(r"(\d{4})/(\d{4})\(COD\)", pr or "")
    return f"https://eur-lex.europa.eu/procedure/EN/{m.group(1)}_{int(m.group(2))}" if m else ""
STAND = {}
for f in F:
    if not f.get("row"):
        continue
    lab, col = STAGE[f["stage"]]
    docs = [(f"Procedure file {f['proc']}", "Legislative Observatory: Parliament reports and votes", OEIL(f["proc"]))] if OEIL_OK(f["proc"]) else []
    if eurproc(f["proc"]):
        docs.append(("EUR-Lex procedure", "Commission proposal and Council documents", eurproc(f["proc"])))
    dl = "".join(f'<li style="display: block"><a href="{u}">{esc(t)}</a> <span class="cap">· {esc(n)}</span></li>' for t, n, u in docs)
    STAND[f["row"]] = f'''  <section style="padding-block: 40px 8px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 16px">
      <div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 12px"><h2 class="h2">Where it stands</h2><span class="chip" style="border-color: {col}; color: {col}; font-weight: 600">{lab}</span><a class="cap" href="Forthcoming.dc.html">All forthcoming initiatives →</a></div>
      {track(f["track"], big=True)}
      <div style="padding: 16px 20px; border-left: 3px solid #B8860B; background: #FFFFFF; border-radius: 0 12px 12px 0"><p class="eyebrow" style="font-size: 12px">Latest · {AS_OF}</p><p class="body" style="margin-top: 6px">{esc(f["latest"])}</p></div>
      <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px">{dl}</ul>
    </div>
  </section>
'''
json.dump(STAND, open("forthcoming.json", "w"), indent=1)
json.dump({str(f["row"]): f["stage"] if f["stage"] == "agreed" else "proposed" for f in F if f.get("row")}, open("forthcoming_status.json", "w"), indent=1)
print("ok", len(F), "Fc pages:", sum(1 for f in F if not f.get("row")), "status blocks:", len(STAND))
