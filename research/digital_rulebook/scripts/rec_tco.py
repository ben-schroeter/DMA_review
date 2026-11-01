import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal has no LFS indicators; the memorandum committed the Commission to a monitoring programme within one year, an implementation report after two years and an evaluation (Article 23)"),
 ind("expected impact (impact assessment)", "Limit availability of terrorist content", "Faster removal: removal orders executed within one hour", "1 hour",
     "At least 349 removal orders issued by six Member States by end-2023 (to Telegram, Meta, X, TikTok, Archive.org and others), mostly with swift follow-up; Commission judges impact 'positive'. No measure of overall prevalence of terrorist content.", "reported as activity", "COM(2024) 64"),
 ind("expected impact (impact assessment)", "Authority capacity and cooperation", "Competent authorities designated; cooperation via Europol (PERCI)", "",
     "23 Member States had designated authorities by end-2023 after infringement procedures against 22; 14,615 referrals processed in PERCI July-Dec 2023.", "measured (outputs)", "COM(2024) 64"),
 ind("expected impact (impact assessment)", "Safeguards against erroneous removal / fundamental rights", "Complaints, reinstatements and court challenges; no over-removal", "",
     "No removal order scrutinised, reinstated or challenged in court by end-2023. FRA (2026) interviews flag risk of over-removal and disproportionate effects on Muslims and Arabic speakers. No quantitative evidence.", "mixed evidence", "COM(2024) 64; FRA 2026"),
 ind("expected impact (impact assessment)", "Single market", "Less fragmentation and lower compliance costs for hosting providers", "", "Not evaluated.", "not measured", ""),
]
literature = [
 lit("ec-2018-tco-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal on preventing the dissemination of terrorist content online (executive summary SWD(2018) 409)", "SWD(2018) 408", EU + "52018SC0409",
     "Commission impact assessment", "ex-ante (qualitative option comparison)", "removal speed; transparency; fundamental rights; compliance costs", "positive (forecast)",
     "Preferred option (one-hour removal orders, referrals, proactive measures for exposed providers, safeguards, transparency) judged most effective, with highest costs and highest benefits; no quantified headline", "The Commission expected binding one-hour removal orders and transparency duties to cut the spread of terrorist propaganda online, and accepted higher costs for platforms.",
     "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
 lit("ec-2024-tco-implementation", "European Commission", 2024, "Report on the implementation of Regulation (EU) 2021/784 on addressing the dissemination of terrorist content online (with SWD(2024) 36)", "COM(2024) 64", EU + "52024DC0064",
     "Commission implementation report", "implementation report (Member State, Europol and provider data)", "removal orders; authority designation; safeguards", "positive",
     "By 31 Dec 2023: 349+ removal orders from six Member States, mostly executed quickly; 23 Member States designated authorities; 14,615 referrals via PERCI; no orders challenged; Commission concludes a positive impact in limiting spread of terrorist content", "The Commission's first report counts about 350 removal orders in 2023, mostly acted on quickly, and calls the law a success - but the evidence is activity counts, not a measured drop in terrorist content.",
     "EU, June 2022-Dec 2023", "self-assessment; descriptive", "full text read"),
 lit("fra-2026-terrorist-content", "EU Agency for Fundamental Rights (FRA)", 2026, "Regulating online terrorist content - Balancing public safety and fundamental rights", "FRA report, 22 January 2026", "https://fra.europa.eu/en/publication/2025/regulating-online-terrorist-content",
     "EU agency report", "qualitative (fieldwork interviews with 62 practitioners and experts)", "fundamental rights; over-removal; discrimination", "mixed",
     "Moderation by authorities and platforms may disproportionately affect Muslims and Arabic speakers while far-right content gets less scrutiny; risks of over-removal and chilling of free expression; recommends clearer definitions, transparency and avoiding incentives to over-remove", "The EU's rights agency warns that the terrorist content rules may lead platforms to over-remove legal posts and hit Muslim and Arabic-speaking users hardest, based on interviews with experts.",
     "EU, 2024-2025", "qualitative; interviews", "page summary via search"),
]
write("32021R0784", "Terrorist Content Online Regulation", "52018PC0640", "SWD(2018) 408 (executive summary SWD(2018) 409)",
      "thin: Commission activity counts and a qualitative rights assessment; no measure of effect on terrorist content or on platforms",
      "Since June 2022 national authorities can order platforms to remove terrorist content within one hour. The Commission counted about 350 such orders by end-2023, mostly acted on quickly, and judged the law a success, but no study measures whether terrorist content online actually fell. The EU's rights agency (2026) warns of over-removal and uneven effects on Muslim and Arabic-speaking users.",
      indicators, literature)
