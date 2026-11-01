import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no usable LFS indicators (section 1.4.4 in the extraction is about synergies); performance is tracked through the indicators in the Regulation's annex, continuous monitoring and mid-term/final evaluations"),
 ind("programme objective (proposal)", "Internal market and enforcement (Pillar 1)", "Better digital tools for enforcement and administrative cooperation (e.g. IMI, Your Europe, competition case tools)", "",
     "Interim evaluation: tools improved enforcement and cooperation, but CASE@EC rollout only partly done and broader impact of tools not measured because user feedback is not collected regularly.", "reported as activity", "COM(2025) 347"),
 ind("programme objective (proposal)", "SME competitiveness (Pillar 2)", "SMEs supported through Enterprise Europe Network, Erasmus for Young Entrepreneurs, Euroclusters", "",
     "Interim evaluation reports very high client satisfaction and 'tangible effects on business performance' but recommends systematic tracking of all SMEs supported and a harmonised survey of effects on growth, digitalisation and internationalisation - i.e. impact on firms is not yet measured.", "reported as activity", "COM(2025) 347"),
 ind("programme objective (proposal)", "Consumer protection, standardisation, food safety, statistics (Pillars 3-6)", "Effective consumer enforcement (CPC, Safety Gate), standards adoption, animal disease eradication, trusted statistics", "",
     "Interim evaluation finds all pillars effective; e.g. reduced brucellosis, rabies and Salmonella cases; 95% of surveyed users confident in European statistics (2024). Mostly output and satisfaction evidence.", "partially measured", "COM(2025) 347"),
 ind("budget execution", "Implementation", "Budget committed", "EUR 4,353m total 2021-2027",
     "EUR 1,909m (44%) allocated in the first three years; inflation reduced the number and scope of actions.", "measured", "COM(2025) 347"),
]
literature = [
 lit("ec-2018-smp-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal establishing the Single Market Programme", "SWD(2018) 320", EU + "52018SC0320",
     "Commission impact assessment", "ex-ante (programme design; qualitative)", "programme design; single market functioning", "positive (forecast)",
     "Merges six predecessor programmes (COSME, consumer, standardisation, food chain, statistics, internal market tools) into one; justification largely qualitative, citing evaluations of predecessors; no macro forecast of programme impact", "The Commission argued that combining six existing funding lines into one Single Market Programme would make support for SMEs, consumers and enforcement simpler and more flexible, but did not forecast measurable economic effects.",
     "EU, 2021-2027", "forecast; qualitative", "full text skimmed"),
 lit("ec-2025-smp-interim", "European Commission", 2025, "Report on the interim evaluation of the Single Market Programme 2021-2027 (with SWD(2025) 172)", "COM(2025) 347", EU + "52025DC0347",
     "Commission evaluation", "interim evaluation (external study by Prognos consortium; surveys, monitoring data, case studies)", "outputs; user satisfaction; SME support", "positive",
     "Positive conclusions for 2021-2023 across all pillars; EUR 1.9bn (44%) of EUR 4.35bn allocated; flagship SME services highly rated; but data collection weak, indicators need refining, and impact on SME growth should be measured with a harmonised survey", "The Commission's mid-term review rates the programme as effective, but most evidence is satisfaction surveys and activity counts; it admits impact on firms' growth is not yet measured.",
     "EU, 2021-2023", "self-evaluation; no counterfactual", "full text read"),
]
write("32021R0690", "Single Market Programme", "52018PC0441", "SWD(2018) 320",
      "thin: Commission interim evaluation based on outputs and satisfaction surveys; no counterfactual or independent study found",
      "The EUR 4.4bn Single Market Programme funds SME support networks, consumer enforcement, standards, food safety and statistics. The Commission's 2025 mid-term review calls it effective, citing satisfied users and disease control results, but admits it does not yet measure effects on firms' growth. No independent study of its impact was found.",
      indicators, literature)
