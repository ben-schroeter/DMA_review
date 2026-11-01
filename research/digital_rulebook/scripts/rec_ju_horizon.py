import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
ECA = "https://www.eca.europa.eu/ECAPublications/SAR-JUS-2024/SAR-JUS-2024_EN.pdf"
indicators = [
 ind("note", "The proposal's LFS has no indicators (1.4.4 lists synergies); partnerships are monitored under Articles 45 and 47 and Annex III of the Horizon Europe Regulation and feed into Horizon Europe interim and ex-post evaluations"),
 ind("expected impact (impact assessment)", "Leverage of private and national funding", "Non-EU contributions mobilised per EU euro (e.g. KDT/Chips 1:3 leverage)", "EU EUR 17.2bn to leverage EUR 21.3bn (123%) in 2021-2027",
     "ECA: planned leverage lower than 2014-2020 (158%); shortfalls for some JUs - Global Health EDCTP3 partners' cash only EUR 15.6m (4% of EUR 400m target) by end-2024; SESAR 3/Eurocontrol and IHI also short. HE interim evaluation: JU projects have highest direct leverage factor (0.8) among HE actions.", "partially measured", "ECA 2025; SWD(2025) 110"),
 ind("expected impact (impact assessment)", "Knowledge, innovation and value-chain resilience", "Scientific, economic and technological impacts of partnerships", "",
     "HE interim evaluation: partnerships contributed to new knowledge and EU leadership in key technologies; only a smaller number of JUs had an impact on accelerating uptake of innovative solutions. Based on partnership evaluations, not counterfactual.", "partially measured", "SWD(2025) 110"),
 ind("partnership criterion (Horizon Europe Regulation)", "Openness and SME participation", "New members; SME and widening-country participation", "",
     "308 new organisations joined partnerships 2022-2024, mostly EIT KICs; few newcomers in JUs; only three JUs have SMEs as members; about 15% of JU funding went to SMEs.", "measured", "SWD(2025) 110"),
 ind("expected impact (impact assessment)", "Sector targets (e.g. aviation emissions, rail, hydrogen, health)", "Sector-specific technology and climate targets", "",
     "Too early; no ex-post measures of sector outcomes found. Predecessor (Horizon 2020) JUs covered in SWD(2024) 29.", "not measured", ""),
]
literature = [
 lit("ec-2021-ju-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Council Regulation establishing the Joint Undertakings under Horizon Europe (executive summary SWD(2021) 38)", "SWD(2021) 37", EU + "52021SC0038",
     "Commission impact assessment", "ex-ante (coordinated IA of 9 partnerships; option comparison)", "leverage; sector R&I targets", "positive (forecast)",
     "Institutionalised partnerships preferred for each area; e.g. Key Digital Technologies expected leverage of 1:3 (EUR 1 EU, EUR 1 states, EUR 2 private) with SMEs at least one-third of participants; aviation and rail options with over 60% of costs covered by private partners", "The Commission argued that public-private joint undertakings would multiply EU research money with industry and national funds, e.g. three extra euros for every EU euro in chips research.",
     "EU, 2021-2031", "forecast; qualitative plus cost estimates", "full text read (executive summary)"),
 lit("ec-2025-horizon-interim-jus", "European Commission", 2025, "Interim Evaluation of the Horizon Europe Framework Programme 2021-2024 (incl. annexes on 19 institutionalised partnerships)", "SWD(2025) 110", EU + "52025SC0110",
     "Commission evaluation", "interim evaluation (partnership evaluations, monitoring data)", "leverage; openness; innovation", "mixed",
     "JUs have highest direct leverage (0.8; EU covers 55% of eligible costs); older partnerships leverage much more than newer ones; impacts on knowledge and value-chain resilience, but only some JUs accelerated uptake of innovations; few newcomers; SMEs members in only three JUs", "The Commission's mid-term review finds the joint undertakings bring in co-funding and help strategic technologies, but few newcomers join and only some speed up market uptake.",
     "EU, 2021-2024", "self-evaluation; no counterfactual", "full text read (relevant sections)"),
 lit("eca-2025-ju-annual-2024-jus", "European Court of Auditors", 2025, "Annual report on EU joint undertakings for the 2024 financial year", "ECA annual report", ECA,
     "audit report", "financial and compliance audit", "leverage targets; contributions", "mixed",
     "Planned 2021-2027 leverage (123%) lower than 2014-2020 (158%); by end of Horizon 2020 period members met 96% of contribution targets on average but with shortfalls (SESAR 3, IHI, EuroHPC); Global Health EDCTP3 at 4% of contributing-partner target", "EU auditors find the joint undertakings' finances sound overall, but several are well short of the private or partner money they promised.",
     "EU, 2024", "audit", "full text read (relevant sections)", pdf_url=ECA),
]
write("32021R2085", "Joint Undertakings under Horizon Europe", "52021PC0087", "SWD(2021) 37 (executive summary SWD(2021) 38)",
      "thin: Commission self-evaluation and audit evidence on co-funding; no counterfactual study of impact for the Horizon Europe JUs",
      "This regulation set up nine public-private research partnerships (aviation, rail, hydrogen, chips, health and others) meant to multiply EU research money with industry funds. The Commission's 2025 mid-term review finds they attract co-funding and support strategic technologies, but few newcomers join and only some speed up market uptake. EU auditors report sizeable shortfalls in promised partner contributions for several of them.",
      indicators, literature)
