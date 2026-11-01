import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("specific objective", "Ensure AI systems placed on the market and used are safe and respect fundamental rights and Union values"),
 ind("specific objective", "Ensure legal certainty to facilitate investment and innovation in AI"),
 ind("specific objective", "Enhance governance and effective enforcement of existing law on fundamental rights and safety"),
 ind("specific objective", "Facilitate a single market for lawful, safe and trustworthy AI and prevent fragmentation"),
 ind("indicator (LFS 1.4.4)", "Safety and fundamental rights", "Number of serious incidents or breaches of fundamental-rights obligations (semi-annual), by field, absolute and relative", "",
     "Not yet reportable: high-risk obligations not yet applicable; the 2026 AI omnibus postponed them to 2 Dec 2027 (Annex III) and 2 Aug 2028 (Annex I).", "not yet measurable", "AI omnibus (2026)"),
 ind("indicator (LFS 1.4.4)", "Investment and innovation", "Total AI investment in the EU and by Member State (annual)", "", "No Commission series linked to the Act found yet.", "not measured", ""),
 ind("indicator (LFS 1.4.4)", "Uptake", "Share of companies using AI (annual) / share of SMEs using AI", "",
     "Measurable via Eurostat: 7.7% (2021), 8.1% (2023), 13.5% (2024), about 20% (2025) of EU enterprises with 10+ staff; 55% of large firms in 2025. Rise cannot be attributed to the Act (main obligations not yet applicable; generative-AI boom).", "measured (not attributable)", "Eurostat"),
 ind("expected impact (impact assessment)", "Compliance costs", "Aggregate compliance cost EUR 100-500m by 2025 (up to 4-5% of high-risk AI investment) plus verification 2-5%; high-risk = 5-15% of AI applications", "",
     "Not evaluated. Start-up surveys put the high-risk share at 33-50% of their systems, far above the 5-15% assumed; obligations later postponed and simplified.", "not measured (contested assumptions)", "SWD(2021) 85; appliedAI/Digital Poland survey"),
]
literature = [
 lit("ec-2021-aiact-ia", "European Commission", 2021, "Impact Assessment accompanying the AI Act proposal (executive summary SWD(2021) 85)", "SWD(2021) 84", EU + "52021SC0085",
     "Commission impact assessment", "ex-ante", "compliance costs; SMEs; trust", "positive (forecast)",
     "Aggregate compliance cost EUR 100-500m by 2025 (up to 4-5% of investment in high-risk AI, assumed 5-15% of applications), plus 2-5% verification costs; SMEs expected to benefit from higher trust", "The Commission expected compliance to cost EUR 100-500 million in total by 2025, because only 5-15% of AI systems would count as high-risk.",
     "EU, forecast", "forecast", "full text read"),
 lit("eurostat-ai-use-2025", "Eurostat", 2025, "Use of artificial intelligence in enterprises", "Statistics Explained (data extracted December 2025)", "https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises",
     "official statistics", "descriptive", "AI uptake", "n/a (monitoring indicator)",
     "AI use by EU enterprises (10+ employees): 7.7% (2021), 8.1% (2023), 13.5% (2024), 19.95% (2025); large enterprises 55%; Denmark 42%, Romania 5%", "One in five EU firms used AI in 2025, up from one in thirteen in 2023 - one of the Act's own success indicators, though the rise reflects the generative-AI boom rather than the Act.",
     "EU-27, 2021-2025", "descriptive; not causal", "search summary of official release"),
 lit("ai-omnibus-2026", "Council of the EU / European Parliament", 2026, "Digital Omnibus on AI (amending the AI Act): postponement of high-risk obligations", "Political agreement 7 May 2026; Parliament 16 June, Council 29 June 2026", "https://www.addleshawgoddard.com/en/insights/insights-briefings/2026/technology/ai-omnibus-provisional-agreement-changes-eu-ai-act-delayed-deadlines/",
     "legislative record (secondary summary)", "legislative record", "implementation", "n/a",
     "High-risk obligations postponed from 2 Aug 2026 to 2 Dec 2027 (Annex III) and from 2 Aug 2027 to 2 Aug 2028 (Annex I)", "Two years after adoption, EU lawmakers postponed the AI Act's main high-risk rules by more than a year to give firms and standard-setters more time.",
     "EU", "law-firm summary; check Official Journal text", "search summary"),
 lit("appliedai-2022-startups", "appliedAI Institute / Digital Poland et al.", 2022, "AI Act Impact Survey: Exploring the impact of the AI Act on startups in Europe", "Survey of 113 AI start-ups and VC firms", "https://www.digitalpoland.org/en/blog/2022/12/artificial-intelligence-act-will-reduce-the-competitiveness-of-the-european-ai-ecosystem",
     "industry/advocacy survey", "survey (ex-ante, draft Act)", "innovation; investment; compliance burden", "negative (expected)",
     "33-50% of start-ups expected their systems to be high-risk (vs 5-15% assumed by the Commission); about 16% considered stopping AI development or relocating outside the EU; 73% of surveyed VCs expected reduced competitiveness", "Before adoption, many AI start-ups expected far more of their products to be classed as high-risk than the Commission assumed, and some considered leaving the EU.",
     "EU start-ups, 2022", "small, self-selected sample; expectations not outcomes", "search summary", interested_party="Start-up and digital-industry associations"),
]
write("32024R1689", "Artificial Intelligence Act", "52021PC0206", "SWD(2021) 84 (executive summary SWD(2021) 85)",
      "forecasts only: main obligations not yet applicable (postponed to 2027-28); no ex-post evidence; ex-ante cost assumptions contested",
      "The AI Act's main high-risk obligations do not yet apply and were postponed in 2026 to December 2027 and August 2028, so its effects cannot yet be measured. One of its own success indicators - the share of firms using AI - rose from 8% (2023) to 20% (2025), but this reflects the generative-AI boom rather than the Act. The Commission's forecast of EUR 100-500m compliance costs assumed only 5-15% of AI systems would be high-risk; start-up surveys put that share at 33-50%.",
      indicators, literature)
