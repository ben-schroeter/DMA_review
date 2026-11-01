import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No LFS indicators extracted; memorandum says specific objectives would be monitored annually and the act evaluated five years after entry into force (IA executive summary says three years), focusing on market and SME impact"),
 ind("expected impact (impact assessment)", "Single market for space", "One set of EU licensing requirements instead of 13+ national regimes; lower administrative burden; cross-border recognition", "",
     "Not applicable: proposal pending (June 2025).", "not measured", "SWD(2025) 335"),
 ind("expected impact (impact assessment)", "Compliance costs", "Satellite manufacturing cost increase from binding safety, resilience and environmental requirements", "+3-10% vs baseline; risk management up to EUR 240,000 initial then ~1% of turnover",
     "Forecast only; US government and some industry argue costs and burdens are underestimated and discriminatory (qualitative, no published cost estimate).", "not measured", "SWD(2025) 335; US Government comments 2025"),
 ind("expected impact (impact assessment)", "Safety and sustainability", "Less space debris; trackable space objects; cybersecurity risk framework; common environmental footprint method", "",
     "Not measured.", "not measured", "SWD(2025) 335"),
]
literature = [
 lit("ec-2025-space-act-ia", "European Commission", 2025, "Impact Assessment accompanying the proposal for a Regulation on the safety, resilience and sustainability of space activities in the Union (EU Space Act)", "SWD(2025) 335 (executive summary SWD(2025) 336)", EU + "52025SC0335",
     "Commission impact assessment", "ex-ante", "compliance costs; single market; competitiveness; space debris", "positive (forecast)",
     "Preferred option (binding EU framework plus support measures): satellite manufacturing costs +3-10% vs baseline; risk management up to EUR 240,000 initially then 1% of turnover; benefits (less debris and cyber risk, business continuity, single market, attracting investment) described qualitatively",
     "The Commission expected a single EU licensing regime to cut red tape and make space safer and greener, while raising satellite manufacturing costs by 3-10%.",
     "EU, forecast", "forecast; benefits not quantified", "executive summary read; full text searched"),
 lit("usg-2025-space-act-comments", "US Departments of State and Commerce", 2025, "U.S. Government feedback on the draft EU Space Act", "Comments released 4 November 2025", "https://space.commerce.gov/wp-content/uploads/2025/11/090166e52487d15d.pdf",
     "government position", "qualitative (drawing on input from 70+ companies and trade associations)", "compliance costs; market access", "negative",
     "Argues the act would impose unacceptable regulatory burdens and drive up costs, especially via environmental requirements, and that some provisions (e.g. on large constellations) unfairly target non-EU operators; no quantified cost estimate",
     "The US government said the EU Space Act would raise costs and unfairly burden American satellite operators, but gave no cost figures.",
     "EU/US, 2025", "stakeholder position", "page summary via search", interested_party="Government representing affected non-EU (US) operators"),
]
write("52025PC0335", "EU Space Act", "52025PC0335", "SWD(2025) 335 (executive summary SWD(2025) 336)",
      "ex-ante only: impact assessment with cost estimates; qualitative critiques; proposal pending",
      "The Commission expects one EU-wide licensing regime for space activities to replace 13 or more national systems, reduce space debris and cyber risks, and help European start-ups grow, at the price of satellites costing 3-10% more to build. The United States and some companies argue the burden is higher and unfairly hits non-EU operators. The proposal is still under negotiation, so there is no evidence of effects yet.",
      indicators, literature)
