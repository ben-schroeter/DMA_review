import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no usable LFS indicators (1.4.4 in the extraction covers synergies); key indicators are in Part 1 of the Regulation's annex, with a Monitoring and Evaluation Framework published as SWD(2024) 276; interim evaluation was still under way in Sept 2025"),
 ind("programme objective (Regulation)", "Transport: complete TEN-T core network", "Cross-border and missing links, military mobility, alternative fuels infrastructure", "",
     "Calls oversubscribed up to almost 3x; whole transport budget committed by 2025; 600+ projects ongoing but only 23 small projects finished; remaining need EUR 845bn to complete the network.", "reported as activity", "COM(2025) 516"),
 ind("programme objective (Regulation)", "Energy: integrate internal energy market (PCIs, cross-border renewables)", "Interconnections built; cross-border renewables projects", "EUR 5.8bn budget",
     "EUR 3.5bn awarded 2021-2024 (e.g. 16 electricity projects >EUR 2bn incl. EuroAsia interconnector, Baltic synchronisation); some projects delayed by energy and materials price shocks; EUR 430m temporarily moved to transport.", "reported as activity", "COM(2025) 516"),
 ind("programme objective (Regulation)", "Digital: 5G corridors and backbone networks", "5G along transport corridors; Global Gateway backbones/submarine cables", "",
     "Start delayed; 117 projects worth over EUR 640m funded (51 backbone/submarine cable projects EUR 420m; 25 5G corridor projects EUR 93m); first results only from 2025; portfolio judged on track.", "reported as activity", "COM(2025) 516"),
 ind("expected impact (impact assessment)", "Growth, cohesion, decarbonisation", "Economic and environmental effects of completed networks", "",
     "Not measured; projects mostly not completed. No causal study of CEF grants found.", "not measured", ""),
]
literature = [
 lit("ec-2018-cef-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal for the Connecting Europe Facility 2021-2027 (executive summary SWD(2018) 313)", "SWD(2018) 312", EU + "52018SC0312",
     "Commission impact assessment", "ex-ante (MFF programme IA; draws on mid-term evaluation of CEF 2014-2020)", "programme design; delivery options", "positive (forecast)",
     "Focused on structure, priorities and delivery of a continued programme; Regulatory Scrutiny Board asked for stronger monitoring and evaluation arrangements; no quantified impact forecast", "The Commission's assessment argued for continuing the Connecting Europe Facility with a broader digital and energy scope, but did not forecast measurable economic effects.",
     "EU, 2021-2027", "forecast; qualitative", "full text read (executive summary)"),
 lit("ec-2025-cef-progress", "European Commission", 2025, "Progress report on the implementation of the 2021-2027 Connecting Europe Facility for the years 2021-2024", "COM(2025) 516", EU + "52025DC0516",
     "Commission implementation report", "progress report (monitoring data)", "commitments; projects; delays", "positive",
     "Transport calls oversubscribed up to ~3x and budget fully committed by 2025, but most projects in early stages (23 of 600+ finished); energy EUR 3.5bn awarded with some delays; digital 117 projects >EUR 640m, start delayed, judged on track; interim evaluation ongoing", "The Commission's first progress report shows the money is being committed quickly - transport calls were nearly three times oversubscribed - but few projects are finished, so no results on traffic, energy flows or growth are available yet.",
     "EU, 2021-2024", "self-assessment; descriptive", "full text read"),
]
write("32021R1153", "Connecting Europe Facility", "52018PC0438", "SWD(2018) 312 (executive summary SWD(2018) 313)",
      "thin: budget commitments and project counts only; interim evaluation pending; no causal study of CEF found",
      "The Connecting Europe Facility co-funds cross-border transport, energy and digital networks. By 2025 the transport money was fully committed and calls had been nearly three times oversubscribed, but only a handful of the 600+ funded transport projects were finished. There is no measured evidence yet of effects on trade, energy markets or growth, and the formal interim evaluation was still under way.",
      indicators, literature)
