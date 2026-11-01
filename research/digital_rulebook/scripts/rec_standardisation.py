import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
CNL = "https://data.consilium.europa.eu/doc/document/ST-10804-2025-INIT/en/pdf"
indicators = [
 ind("LFS indicator (1.4.4)", "Faster delivery of standards", "Time between ESO acceptance of a standardisation request and adoption of the standard", "",
     "2025 evaluation: 'moderately effective' in reducing development time, but harmonised standards still take on average six years (three for drafting and consensus). 2022 report: median 100 days from ESO adoption to delivery to the Commission; formal objections take on average 1,084 days.",
     "measured", "SWD(2025) 171; COM(2022) 30"),
 ind("LFS indicator (1.4.4)", "Responsiveness to Commission requests", "Number of European standards adopted following a Commission request", "",
     "2015-2020: 44 standardisation requests issued, 6 rejected by the ESOs (13.6%); only 27.6% of HAS consultant assessments of draft harmonised standards were positive. No outcome-based count of standards linked to effects.",
     "reported as activity", "COM(2022) 30"),
 ind("LFS indicator (1.4.4)", "Inclusiveness", "Participation of SME, consumer, environmental and trade-union organisations (Annex III)", "",
     "Annex III organisations funded (EUR 20m 2015-2019); CEN-CENELEC gave them a formal right of opinion in 2017; ETSI criticised as less inclusive. 2025 evaluation: 'moderately effective' but real influence limited by lack of resources.",
     "reported as activity", "COM(2022) 30; SWD(2025) 171"),
 ind("LFS indicator (1.4.4)", "Governance", "Effect of governance changes on number, speed and participation", "",
     "Evaluation found new CJEU-driven procedures made the process more burdensome; cost-benefit analysis suggests benefits exceed costs but data described as lacking.",
     "mixed evidence", "SWD(2025) 171"),
]
literature = [
 lit("ec-2011-standardisation-ia", "European Commission", 2011, "Impact Assessment accompanying the proposal for a Regulation on European standardisation (executive summary)", "SEC(2011) 672", EU + "52011SC0672",
     "Commission impact assessment", "ex-ante", "speed of standard-setting; inclusiveness; EU budget", "positive (forecast)",
     "Problem defined as slow standard-setting and weak SME/societal participation; options costed qualitatively (e.g. extra EUR 150,000-200,000 per standard for some options); no headline economic forecast",
     "The Commission aimed to speed up European standard-setting and give small firms and civil society more voice, without a quantified economic forecast.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("ec-2022-standardisation-report", "European Commission", 2022, "Report on the implementation of Regulation (EU) No 1025/2012 from 2016 to 2020", "COM(2022) 30", EU + "52022DC0030",
     "Commission implementation report", "monitoring report (Article 24 reporting, contractor study)", "delivery times; inclusiveness; funding", "mixed",
     "Median 100 days from ESO adoption to delivery for citation; formal objections take on average 1,084 days; 6 of 44 requests rejected; EUR 105m grants 2015-2019; ETSI inclusiveness criticised",
     "The Commission's second implementation report found improvements in IT tools but persistent delays and weak inclusion of small firms and civil society.",
     "EU, 2016-2020", "descriptive monitoring", "full text read"),
 lit("ec-2025-standardisation-evaluation", "European Commission", 2025, "Evaluation of Regulation (EU) No 1025/2012 on European standardisation (executive summary)", "SWD(2025) 171 (full evaluation SWD(2025) 170; supporting study by Intellera, Fraunhofer ISI and Trinomics)", CNL,
     "Commission evaluation", "ex-post evaluation (contractor study, surveys, consultation)", "speed; inclusiveness; costs; EU added value", "mixed",
     "Moderately effective in speeding up harmonised standards, but average duration still six years; moderately effective on SME/civil society participation; benefits judged to outweigh costs despite poor data; new procedures after CJEU case law made the process slower",
     "The 2025 evaluation found the Regulation removed conflicting national standards and modestly sped things up, but harmonised standards still take about six years to produce.",
     "EU, 2013-2024", "Commission self-assessment; cost data weak", "full text read (executive summary, via Council register)"),
]
write("32012R1025", "European Standardisation Regulation", "52011PC0315", "SEC(2011) 671 (executive summary SEC(2011) 672)",
      "thin: Commission monitoring reports and one evaluation track speed and participation; no independent causal study of economic effects found",
      "The Regulation promised faster European standards with more input from small firms and civil society. The Commission's 2025 evaluation found it removed conflicting national standards and made modest progress, but harmonised standards still take about six years to produce and smaller stakeholders have little real influence. No independent study measuring its economic effects was found.",
      indicators, literature)
