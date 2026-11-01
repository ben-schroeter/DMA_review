"""Builds site/mockup/DigitalPolicy.dc.html: intro, timeline (site/policy_timeline.svg), one block per era with overview,
numbers, flagship instruments and linked key documents, and a method note. Numbers from data/policy_eras/instruments.json."""
import json, re, html
D_ALL = json.load(open("data/policy_eras/instruments.json"))
D = [o for o in D_ALL if o["status"] == "adopted"]   # counts cover adopted laws; pending proposals enter once adopted
PEND = {}
for o in D_ALL:
    if o["status"] != "adopted": PEND[o["era"]] = PEND.get(o["era"], 0) + 1
FC = json.load(open("site/forthcoming_list.json"))   # exported by site/build_forthcoming.py
PAGES = {int(k): v for k, v in json.load(open("site/instrument_pages.json")).items()}
OBJ = json.load(open("data/policy_eras/objectives.json"))
CHIP = {"met": ("#8F6708", "#FFFFFF"), "met late": ("#B8860B", "#FFFFFF"), "on track": ("#B8860B", "#FFFFFF"), "near miss": ("#E3CF9C", "#282424"),
        "not met": ("#5C5858", "#FFFFFF"), "off track": ("#5C5858", "#FFFFFF"), "too early": ("#FFFFFF", "#3F3B3B"), "not measurable": ("#FFFFFF", "#3F3B3B")}
chip = lambda st: f'<span class="chip" style="background: {CHIP[st][0]}; color: {CHIP[st][1]}">{st}</span>'
svg = open("site/policy_timeline.svg").read()
EUR = lambda c: f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{c}"
ERAS = [
 {"id": "market_opening", "anc": "market-opening", "name": "Market opening", "years": "1987–2000",
  "who": "Delors and Santer Commissions · Martin Bangemann (industry, information and telecommunications technologies)",
  "text": "The 1987 Green Paper on telecommunications set the course: open national telecoms monopolies to competition and build one market for equipment and services, a process completed with full liberalisation in 1998. The 1994 Bangemann report framed the “information society” as a project for markets and private investment. The first digital rules were single-market rules: databases, satellite and cable broadcasting, unfair contract terms and, at the end of the decade, electronic commerce and copyright in the information society.",
  "cite": None, "flag": ["E-commerce Directive", "Database Directive", "Information Society (InfoSoc) Directive", "Satellite and Cable Directive"],
  "docs": [("Jun 1987", "Green Paper on the development of the common market for telecommunications services and equipment", "COM(87) 290", EUR("51987DC0290"), "Opening of national telecoms markets; led to full liberalisation by 1998."),
           ("Jun 1994", "Europe and the global information society (Bangemann report)", "Recommendations to the European Council, Bulletin of the EU, Supplement 2/94", "https://aei.pitt.edu/1199/1/info_society_bangeman_report.pdf", "An information society driven by private investment, with liberalisation and common rules.")]},
 {"id": "lisbon", "anc": "lisbon", "name": "Lisbon", "years": "2000–2010",
  "who": "Prodi and first Barroso Commissions · Erkki Liikanen (enterprise and information society), Viviane Reding (information society and media)",
  "text": "The Lisbon European Council set the goal of making the EU “the most competitive and dynamic knowledge-based economy in the world” by 2010. The internet was treated as an enabler for research, education and business, and the eEurope (2000–2005) and i2010 (2005–2010) programmes focused on getting schools, administrations and firms online and on cheaper, faster access. Legislation in this period was mostly sectoral and aimed at consumers: privacy in electronic communications, unfair commercial practices, audiovisual media services, toy safety and consumer rights.",
  "cite": "Lisbon, eEurope or i2010", "flag": ["ePrivacy Directive", "Unfair Commercial Practices Directive", "Audiovisual Media Services Directive", "Consumer Rights Directive"],
  "docs": [("Dec 1999", "eEurope – An Information Society for All", "COM(1999) 687", "https://eur-lex.europa.eu/legal-content/EN/HIS/?uri=COM:1999:687:FIN", "Commission initiative prepared for the Lisbon summit."),
           ("Mar 2000", "Lisbon European Council, Presidency conclusions", "23–24 March 2000", "https://www.europarl.europa.eu/summits/lis1_en.htm", "The 2010 goal of a competitive, knowledge-based economy."),
           ("May 2002", "eEurope 2005: An information society for all", "COM(2002) 263", EUR("52002DC0263"), "Action plan for broadband access and online public services."),
           ("Jun 2005", "i2010 – A European Information Society for growth and employment", "COM(2005) 229", EUR("52005DC0229"), "Single information space, research and an inclusive information society.")]},
 {"id": "europe2020", "anc": "europe-2020", "name": "Europe 2020", "years": "2010–2015",
  "who": "Second Barroso Commission · Neelie Kroes (Vice-President, Digital Agenda)",
  "text": "After the financial crisis, Europe 2020 made “smart growth” one of three priorities, and the Digital Agenda for Europe was one of its seven flagship initiatives. Targets moved from access to speed: basic broadband for all by 2013, and by 2020 30 Mbps for all and 100 Mbps subscriptions for half of households. The Commission proposed the General Data Protection Regulation in 2012 (adopted 2016), rules on electronic identification and trust services, the second Payment Services Directive and the net-neutrality rules of the Open Internet Regulation.",
  "cite": "Europe 2020 or the Digital Agenda", "flag": ["General Data Protection Regulation", "eIDAS Regulation", "Payment Services Directive 2 (PSD2)", "Open Internet Access Regulation"],
  "docs": [("Mar 2010", "Europe 2020: A strategy for smart, sustainable and inclusive growth", "COM(2010) 2020", EUR("52010DC2020"), "Ten-year growth strategy with seven flagship initiatives."),
           ("May 2010", "A Digital Agenda for Europe", "COM(2010) 245", EUR("52010DC0245"), "Seven pillars, from a digital single market to fast internet; broadband speed targets for 2020.")]},
 {"id": "dsm", "anc": "digital-single-market", "name": "Digital Single Market", "years": "2015–2019",
  "who": "Juncker Commission · Andrus Ansip (Vice-President, Digital Single Market), Günther Oettinger, Mariya Gabriel",
  "text": "Goods moved freely across the EU, but digital services ran into 28 national rulebooks. The Digital Single Market strategy set out 16 actions to remove those barriers so that firms could scale across borders. Policy turned to targeted digital legislation: contract rules for digital content and online sales, a ban on unjustified geo-blocking, cross-border portability of online content, copyright for online use, the free flow of non-personal data and a new European Electronic Communications Code. Retail roaming charges ended in 2017, and the GDPR, proposed in the previous era, applied from 2018.",
  "cite": "the Digital Single Market strategy", "flag": ["European Electronic Communications Code", "Geo-blocking Regulation", "Copyright in the Digital Single Market Directive", "Digital Content Directive"],
  "docs": [("May 2015", "A Digital Single Market Strategy for Europe", "COM(2015) 192", EUR("52015DC0192"), "16 actions in three pillars: access, environment, and the economy and society."),
           ("May 2017", "Mid-term review of the Digital Single Market Strategy", "COM(2017) 228", EUR("52017DC0228"), "Progress review; new focus on data, cybersecurity and online platforms.")]},
 {"id": "digital_decade", "anc": "digital-decade", "name": "Digital Decade", "years": "2019–2024",
  "who": "First von der Leyen Commission · Margrethe Vestager (Executive Vice-President, A Europe Fit for the Digital Age), Thierry Breton (internal market)",
  "text": "The EU came to see its reliance on foreign software, cloud services and chips as a strategic risk. “Shaping Europe’s digital future”, the data strategy and the AI White Paper (all February 2020) launched a wave of horizontal rules; the 2030 Digital Compass and the Digital Decade policy programme added targets for skills, infrastructure, business uptake and public services. This is by far the busiest period: about half of all instruments in the list were proposed in these five years, among them the Digital Markets Act and Digital Services Act for large platforms, the Data Act, the AI Act, the Cyber Resilience Act and the crypto-assets regulation MiCA.",
  "cite": "these strategies", "flag": ["Digital Services Act", "Digital Markets Act", "Artificial Intelligence Act", "Data Act", "Markets in Crypto-Assets (MiCA)"],
  "docs": [("Feb 2020", "Shaping Europe’s digital future", "COM(2020) 67", EUR("52020DC0067"), "Technology that works for people, a fair digital economy, an open and democratic society."),
           ("Feb 2020", "A European strategy for data", "COM(2020) 66", EUR("52020DC0066"), "A single market for data; led to the Data Governance Act and the Data Act."),
           ("Feb 2020", "White Paper on Artificial Intelligence", "COM(2020) 65", EUR("52020DC0065"), "Options for AI rules; led to the AI Act."),
           ("Mar 2021", "2030 Digital Compass: the European way for the Digital Decade", "COM(2021) 118", EUR("52021DC0118"), "Targets for 2030 in skills, infrastructure, business and public services."),
           ("Dec 2022", "Digital Decade Policy Programme 2030", "Decision (EU) 2022/2481", EUR("32022D2481"), "Makes the 2030 targets binding and sets up yearly monitoring.")]},
 {"id": "competitiveness", "anc": "competitiveness", "name": "Competitiveness · One Europe, One Market", "years": "2025–2027",
  "who": "Second von der Leyen Commission · Henna Virkkunen (Executive Vice-President, Tech Sovereignty, Security and Democracy)",
  "text": "The Draghi report (2024) tied Europe’s lagging productivity to weak digital industries, fragmented markets and high energy costs. The Competitiveness Compass made simplification a priority, with a target to cut businesses’ recurring administrative costs by €37.5 billion by 2029. In April 2026 Parliament, Council and Commission signed the One Europe, One Market roadmap: 42 initiatives in five blocks, among them digital and AI, to be agreed by the end of 2027. So far the era has produced proposals rather than laws: the Digital Omnibus (November 2025) to streamline the data, privacy and cybersecurity rules, the Digital Networks Act and Cybersecurity Act 2 (January 2026), EU Inc (March 2026), the Cloud and AI Development Act and Chips Act 2 (June 2026), and the European Innovation Act (September 2026). The AI part of the Digital Omnibus was adopted in July 2026 as an amendment to the AI Act. The Digital Fairness Act, the Quantum Act and the European Product Act are announced. None of this era’s proposals is law yet, so none is in the counts.",
  "cite": "the Competitiveness Compass", "flag": [],
  "docs": [("Sep 2024", "The future of European competitiveness (Draghi report)", "Report to the Commission", "https://commission.europa.eu/topics/competitiveness/draghi-report_en", "Diagnosis of Europe’s productivity gap and an investment need of about €800 billion a year."),
           ("Jan 2025", "A Competitiveness Compass for the EU", "COM(2025) 30", EUR("52025DC0030"), "Innovation, decarbonisation and security, with simplification as a cross-cutting priority."),
           ("Nov 2025", "Digital Omnibus and Digital Omnibus on AI", "COM(2025) 837 and COM(2025) 836", EUR("52025PC0837"), "Proposals to simplify the data, privacy, cybersecurity and AI rules."),
           ("Apr 2026", "One Europe, One Market: joint roadmap", "Parliament, Council and Commission, 24 April 2026", "https://commission.europa.eu/topics/competitiveness/one-europe-one-market-roadmap_en", "42 initiatives in five blocks, to be agreed by the end of 2027.")]},
]
esc = html.escape
blocks = []
for i, e in enumerate(ERAS):
    xs = [o for o in D if o["era"] == e["id"]]
    n, obl = len(xs), sum(o["obligations"] or 0 for o in xs)
    pend = sum(o["status"] != "adopted" for o in xs)
    withtext = sum(o["proposal_text"] for o in xs); cites = sum(o["cites_own_era"] for o in xs)
    pend = PEND.get(e["id"], 0)
    stats = f'<strong style="font-weight: 600">{n} law{"s" if n != 1 else ""} adopted</strong> · {obl:,} obligations' + (f' · <a href="Forthcoming.dc.html">{pend} more proposal{"s" if pend != 1 else ""} still pending</a>' if pend else "")
    if e["cite"] and withtext:
        stats += f" · {cites} of {withtext} proposals cite {e['cite']}"
    by = {o["name"]: o for o in xs}
    fl = []
    for f in e["flag"]:
        o = by[f]
        when = f'{o["proposal_date"][:4]}→{o["adoption_date"][:4]}' if o["adoption_date"] else f'proposed {o["proposal_date"][:4]}'
        fl.append(f'<a href="{PAGES[o["row_id"]]}">{esc(f)}</a> <span class="cap">({when})</span>')
    flags = f'<p class="body" style="font-size: 15px">Flagships: {" · ".join(fl)} · <a href="Instruments.dc.html">See all {n} →</a></p>' if fl else ""
    if e["id"] == "competitiveness":
        mine = [f for f in FC if f["stage"] == "announced" or int(f["proposal"][-4:]) >= 2025]
        page = lambda f: f["page"]
        grp = [("agreed", "Agreed, awaiting adoption"), ("proposed", "In negotiation"), ("announced", "Announced")]
        stats = ("<strong style=\"font-weight: 600\">No law proposed in this era has been adopted yet</strong> · "
                 + " · ".join(f'{sum(f["stage"] == k for f in mine)} {lab.lower()}' for k, lab in grp))
        flags = ('<p class="body" style="font-size: 14px; line-height: 1.5">' + "<br>".join(f'<strong style="font-weight: 600">{lab}:</strong> '
                        + ", ".join(f'<a href="{page(f)}">{esc(f["name"].split(" (")[0])}</a>' for f in mine if f["stage"] == k) for k, lab in grp)
                 + ' · <a href="Forthcoming.dc.html">Where each stands →</a></p>')
    docs = "".join(f'<li style="display: grid; grid-template-columns: 76px minmax(0, 1fr); gap: 12px; padding-block: 10px; border-top: 1px solid #E8E6E3">'
                   f'<span class="cap" style="padding-top: 2px">{d}</span><span><a href="{u}">{esc(t)}</a> <span class="cap">· {esc(ref)}</span><br><span class="cap">{esc(s)}</span></span></li>'
                   for d, t, ref, u, s in e["docs"])
    rows = [o for o in OBJ["items"] if o["era"] == e["id"]]
    trs = "".join(f'<tr><td>{esc(o["objective"])}</td><td>{esc(o["target"])}' + (f' <span class="cap">· {esc(o["deadline"])}</span>' if o["deadline"] else "") + '</td>'
                  f'<td>{esc(o["result"])}' + (f' <a class="cap" href="{OBJ["sources"][o["src"]][1]}">{esc(OBJ["sources"][o["src"]][0])}</a>' if o["src"] else "") + f'</td><td>{chip(o["status"])}</td></tr>' for o in rows)
    score = (f'<div style="grid-column: 1 / -1; overflow-x: auto"><p class="eyebrow" style="margin: 0 0 6px">Objectives and targets</p>'
             f'<table class="okr"><thead><tr><th style="width: 18%">Objective</th><th style="width: 32%">Target</th><th>Result</th><th style="width: 110px">Status</th></tr></thead><tbody>{trs}</tbody></table></div>')
    bg = "background: #F3F1EC; border-top: 1px solid #E8E6E3; border-bottom: 1px solid #E8E6E3; " if i % 2 == 0 else ""
    blocks.append(f'''  <section id="era-{e["anc"]}" style="{bg}padding-block: 36px">
    <div class="wrap era">
      <div style="display: flex; flex-direction: column; gap: 10px">
        <p class="eyebrow">{e["years"]}</p>
        <h2 class="h2">{esc(e["name"])}</h2>
        <p class="cap" style="margin: 0">{esc(e["who"])}</p>
        <p class="body" style="font-size: 16px; line-height: 1.6">{esc(e["text"])}</p>
        <p class="body" style="font-size: 15px">{stats}</p>
        {flags}
      </div>
      <div>
        <p class="eyebrow" style="margin-bottom: 4px">Key documents</p>
        <ul style="list-style: none; margin: 0; padding: 0; font-size: 15px; line-height: 1.45">{docs}</ul>
      </div>
      {score}
    </div>
  </section>
''')
src = open("site/digital_policy_template.dc.html").read()
a = src.index('  <section style="padding-block: 64px 120px">'); b = src.index("  <footer") if "  <footer" in src else src.index("</div>\n</x-dc>")
tabs = re.search(r'      <nav aria-label="Digital Acquis".*?</nav>\n', src, re.S).group(0)
ORD = ["met", "met late", "on track", "near miss", "not met", "off track", "too early", "not measurable"]
ov = []
for k, e in enumerate(ERAS):
    rows = [o for o in OBJ["items"] if o["era"] == e["id"]]
    y = 30 + k * 30; x = 230
    ov.append(f'<text x="220" y="{y + 15}" text-anchor="end" font-family="DM Sans, sans-serif" font-size="13" fill="#282424">{esc(e["name"].split(" · ")[0])}</text>')
    for st in ORD:
        for o in [o for o in rows if o["status"] == st]:
            ov.append(f'<rect x="{x}" y="{y}" width="36" height="20" rx="3" fill="{CHIP[st][0]}" stroke="#C9C6C3"><title>{esc(o["target"])}: {st}</title></rect>'); x += 39
lx = 230
for st in ORD:
    ov.append(f'<rect x="{lx}" y="4" width="12" height="12" rx="2" fill="{CHIP[st][0]}" stroke="#C9C6C3"></rect><text x="{lx + 17}" y="14" font-family="DM Sans, sans-serif" font-size="12" fill="#3F3B3B">{st}</text>'); lx += 30 + len(st) * 6.6
overview = f'<svg viewBox="0 0 1000 {30 + len(ERAS) * 30}" width="100%" role="img" aria-label="Targets by era and result">' + "".join(ov) + '</svg>'
intro = f'''  <section style="padding-block: 64px 32px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
{tabs}      <p class="eyebrow">Digital Acquis · Digital policy</p>
      <h1 class="h1" style="max-width: 20ch">From market liberalization to digital sovereignty</h1>
      <p class="body" style="font-size: 19px">In 2000 the internet was a niche infrastructure project; by 2010 it was a driver of growth; today it is treated as a question of sovereignty and industrial scale. This page follows that path through six eras of EU policy and places each of the 105 adopted laws in the era in which the Commission proposed it.</p>
    </div>
  </section>
  <section style="padding-block: 8px 40px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 12px">
      <div style="overflow-x: auto"><div style="min-width: 1000px">{svg}</div></div>
      <span class="cap">Each line is one instrument, from the Commission proposal to adoption; the dot is sized by the number of obligations in the adopted text. Shading marks the eras, by date of proposal; click an era for its summary. Commission terms and portfolios are simplified to the lead commissioner(s) for digital policy.</span>
      <figure style="margin: 24px 0 0; display: flex; flex-direction: column; gap: 10px"><figcaption style="font-weight: 500">How the targets turned out, by era</figcaption>{overview}</figure>
    </div>
  </section>
'''
note = '''  <section style="padding-block: 48px 72px">
    <div class="wrap">
      <p class="cap" style="margin: 0; max-width: 95ch"><strong style="color: #282424; font-weight: 600">How we assigned the instruments.</strong> Each instrument belongs to the era in which the Commission proposed it, whatever the date of adoption; Commission regulations without a legislative proposal (the block exemptions) are placed by date of adoption. To check the link to each era’s strategy we searched the explanatory memorandum, citations and recitals of every Commission proposal available on EUR-Lex for the strategy’s name (for example “Digital Single Market Strategy” or “Shaping Europe’s digital future”). Older proposals rarely name the strategy behind them, so low counts for the early eras say more about drafting habits than about policy. Obligations are counted in the adopted text; proposals still pending are on the Forthcoming page and enter the counts once adopted.</p>
    </div>
  </section>
'''
out = src[:a] + intro + "".join(blocks) + note + src[b:]
out = out.replace(".ph{color:#8F6708}", ".ph{color:#8F6708}\n.era{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:20px 48px;align-items:start}\n@media (max-width:860px){.era{grid-template-columns:minmax(0,1fr);gap:24px}}\n.okr{width:100%;min-width:640px;border-collapse:collapse;font-size:14px;line-height:1.4}\n.okr th{text-align:left;font-weight:500;font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:#666666;padding:6px 10px;border-bottom:1px solid #D4D2CE}\n.okr td{padding:5px 10px;border-bottom:1px solid #E8E6E3;vertical-align:top}\n.chip{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:600;border:1px solid #C9C6C3;white-space:nowrap}")
open("site/mockup/DigitalPolicy.dc.html", "w").write(out)
print(len(out))
