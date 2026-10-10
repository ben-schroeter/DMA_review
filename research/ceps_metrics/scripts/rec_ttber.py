import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "Commission Regulation adopted without a legislative proposal or financial statement; no monitoring indicators. Assessed through the 2022-2024 evaluation and the 2026 impact assessment for its replacement"),
 ind("evaluation question", "Legal certainty and lower compliance costs for licensing", "Stakeholder-reported legal certainty and compliance costs", "",
     "2024 evaluation: rules 'largely meet their objectives', providing legal certainty and lower compliance costs, but market-share thresholds hard to apply (especially early-stage licensing) and data licensing/licensing negotiation groups not covered. Based on consultation, not measured outcomes.",
     "reported as activity", "SWD(2024) 268"),
 ind("expected impact (impact assessment, successor TTBER)", "Simplify threshold assessment", "Cost of applying market-share thresholds per licensing agreement", "-15 to -40% (forecast)",
     "Forecast only; new TTBER applies from May 2026.", "not measured", "SWD(2026) 114/116"),
 ind("expected impact (impact assessment, successor TTBER)", "Facilitate data licensing", "Compliance assessment costs for covered data licensing agreements", "up to -33% (forecast)",
     "Forecast only.", "not measured", "SWD(2026) 114/116"),
]
literature = [
 lit("ec-2024-ttber-evaluation", "European Commission", 2024, "Evaluation of the Technology Transfer Block Exemption Regulation and Technology Transfer Guidelines", "SWD(2024) 268 (with SWD(2024) 269)", "https://competition-policy.ec.europa.eu/public-consultations/2023-technology-transfer_en",
     "Commission evaluation", "ex-post evaluation (stakeholder consultation, targeted survey)", "legal certainty; compliance costs; licensing", "positive with gaps",
     "Rules largely meet objectives, providing legal certainty and lower compliance costs; problems applying market-share thresholds, the '4+' test and technology pools; data licensing not addressed",
     "The Commission's evaluation found the licensing safe harbour still useful, but out of date for early-stage technologies and data licensing.",
     "EU, 2014-2023", "Commission self-assessment based on stakeholder views", "page summary via search"),
 lit("ec-2026-ttber-ia", "European Commission", 2026, "Impact Assessment accompanying the revised Technology Transfer Block Exemption Regulation and Guidelines (executive summary)", "SWD(2026) 116 (full IA SWD(2026) 114)", EU + "52026SC0116",
     "Commission impact assessment", "ex-ante", "compliance costs; licensing; SMEs", "positive (forecast)",
     "Preferred options to cut cost of applying market-share thresholds by 15-40% per agreement and data-licensing assessment costs by up to 33%; no new obligations on business",
     "For the replacement rules, the Commission expects firms' legal-assessment costs for licensing deals to fall by 15-40%.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
]
write("32014R0316", "Technology Transfer Block Exemption", None, "No IA for the 2014 Regulation reviewed; evaluation SWD(2024) 268; successor IA SWD(2026) 114",
      "thin: Commission evaluation based on stakeholder views; no independent empirical study of the Regulation's effect on licensing or innovation found",
      "This competition-law safe harbour for technology licensing had no monitoring indicators. The Commission's 2024 evaluation, based mostly on stakeholder views, found it largely did its job of giving firms legal certainty, but had gaps on early-stage technologies and data licensing; its 2026 replacement is forecast to cut legal-assessment costs by 15-40%. No independent study measuring its effect on licensing or innovation was found.",
      indicators, literature)
