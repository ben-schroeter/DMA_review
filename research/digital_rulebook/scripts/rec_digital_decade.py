import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No impact assessment (the Commission judged one unnecessary and issued a staff working document instead) and no LFS indicators. The Decision itself sets the 2030 digital targets (Article 4) with KPIs tracked in the annual State of the Digital Decade report"),
 ind("2030 target (Article 4)", "Connectivity", "Gigabit coverage for all households; 5G in all populated areas", "100% by 2030",
     "Basic 5G covers 96.8% of households (2026); fibre-to-the-premises 69% and very-high-capacity networks 82% (2025 report) - FTTP 'not enough to reach 100% by 2030'; stand-alone 5G lagging.", "measured", "COM(2025) 290; Commission news 17 June 2026"),
 ind("2030 target (Article 4)", "Digital transformation of businesses", "75% of enterprises using cloud, big data or AI", "75% by 2030",
     "2026: 46.7% of firms use cloud, 39.9% data analytics, nearly 20% AI; AI, cloud and data analytics progress rated 'deeply unsatisfactory' in 2025.", "measured", "COM(2025) 290; Commission news 17 June 2026"),
 ind("2030 target (Article 4)", "Skills", "80% of adults with basic digital skills; 20 million ICT specialists", "80%; 20m by 2030",
     "More than 60% have at least basic skills (2026); ICT specialist shortages and gender gap persist; both rated deeply unsatisfactory in 2025.", "measured", "COM(2025) 290; Commission news 17 June 2026"),
 ind("2030 target (Article 4)", "Semiconductors", "EU share of global semiconductor production", "20% by 2030",
     "About 10% of the global market at the programme's launch; secondary summaries of the 2026 report put it at 9%, far below target; the Commission says semiconductors still lag.", "measured", "COM(2025) 771; Commission news 17 June 2026"),
 ind("2030 target (Article 4)", "Digital public services", "100% key public services online", "100% by 2030",
     "82% for citizens and 86% for businesses (2025 report).", "measured", "COM(2025) 290"),
 ind("governance mechanism (Articles 7-9)", "Member State action", "National roadmaps and follow-up of recommendations", "",
     "All Member States adopted roadmaps: 1,910 measures worth EUR 288.6bn (EUR 205.1bn public, 1.14% of EU GDP); 57% of 306 country recommendations from 2024 addressed, mostly only partly (12% significant changes).", "measured", "COM(2025) 290"),
]
literature = [
 lit("ec-2025-state-digital-decade", "European Commission", 2025, "State of the Digital Decade 2025: Keep building the EU's sovereignty and digital future", "COM(2025) 290", EU + "52025DC0290",
     "Commission monitoring report", "annual KPI monitoring against 2030 targets", "connectivity; skills; business digitalisation; public services", "mixed",
     "Uneven progress: edge nodes, e-health and basic 5G near targets; AI, cloud, data analytics, ICT specialists and basic skills 'deeply unsatisfactory'; FTTP 69%, VHCN 82%; national roadmaps worth EUR 288.6bn; 57% of 2024 recommendations addressed", "The Commission's own scorecard shows the EU on track for basic 5G and online services but far off its 2030 goals for AI use by firms, digital skills, fibre and chips.",
     "EU-27, 2024 data", "monitoring; descriptive", "full text read (main report)", pdf_url="https://ec.europa.eu/newsroom/dae/redirection/document/116741"),
 lit("ec-2026-state-digital-decade", "European Commission", 2026, "State of the Digital Decade 2026 report (news summary)", "Commission news, 17 June 2026", "https://commission.europa.eu/news-and-media/news/state-digital-decade-report-progress-made-gaps-remain-2026-06-17_en",
     "Commission monitoring report", "annual KPI monitoring against 2030 targets", "connectivity; skills; business digitalisation", "mixed",
     "96.8% of households have basic 5G; fibre, semiconductors and computing capacity lag; more than 60% have basic digital skills; ICT specialist shortages persist; targets to be reviewed in 2027", "The 2026 scorecard shows more progress on mobile coverage and skills, but fibre, chips and business use of advanced technology still trail the 2030 goals; the targets will be reviewed in 2027.",
     "EU-27, 2025 data", "monitoring; descriptive", "full text read (news page)"),
]
write("32022D2481", "Digital Decade Policy Programme Decision", "52021PC0574", "None (staff working document instead of an IA)",
      "monitoring only: annual Commission KPI tracking against 2030 targets; no assessment of whether the governance mechanism itself changed outcomes",
      "The Digital Decade programme sets EU targets for 2030 on connectivity, skills, business digitalisation and public services, and makes the Commission report progress every year. Its own reports show basic 5G at 96.8% of households and online public services above 80%, but the EU is far off target on AI use by firms (about 20% vs 75%), basic digital skills (just over 60% vs 80%), fibre and chips. No study has assessed whether the programme's governance changed what Member States do.",
      indicators, literature)
