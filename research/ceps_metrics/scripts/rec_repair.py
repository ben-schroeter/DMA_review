import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no indicators section; the memorandum promises an evaluation 5 years after application based on a set of indicators covering the sustainable-consumption package"),
 ind("expected impact (impact assessment)", "Environment", "CO2 savings of 18.4 million tonnes over 15 years (alongside ESPR 471 Mt and ECGT 0.33-0.47 Mt)", "18.4 Mt CO2 / 15 years",
     "Not measured; rules apply only from 31 July 2026.", "not measured", "SWD(2023) 59/60"),
 ind("expected impact (impact assessment)", "Consumers", "Consumer savings of EUR 176.5bn over 15 years from less replacement and more repair", "EUR 176.5bn / 15 years",
     "Not measured.", "not measured", "SWD(2023) 60"),
 ind("expected impact (impact assessment)", "Business / repair sector", "Lost sales and GVA for producers and retailers (treated as a transfer to consumers); repair-sector SMEs gain", "",
     "Not measured. Academic critique argues the Directive leaves the main barriers to repair (obsolescence, spare parts, repair information, price incentives) unaddressed.", "not measured", "SWD(2023) 60; López-Bermúdez & Vence 2025"),
]
literature = [
 lit("ec-2023-repair-ia", "European Commission", 2023, "Impact Assessment accompanying the proposal for a Directive on common rules promoting the repair of goods (executive summary SWD(2023) 60)", "SWD(2023) 59", EU + "52023SC0060",
     "Commission impact assessment", "ex-ante", "CO2 emissions; consumer savings; business turnover", "positive (forecast)",
     "In 15 years the initiative saves 18.4 Mt CO2 and EUR 176.5bn for consumers; producers and retailers lose sales; overall slightly beneficial for SMEs as a whole",
     "The Commission expected the right to repair to save consumers EUR 176.5 billion and 18.4 million tonnes of CO2 over 15 years, with manufacturers and retailers selling fewer new goods.",
     "EU, forecast over 15 years", "forecast", "full text read (executive summary)"),
 lit("lopez-bermudez-vence-2025-repair", "López-Bermúdez & Vence", 2025, "A critical assessment of the European Directive proposal on the common rules promoting the repair of goods", "Resources, Conservation and Recycling 212, 107996", "https://doi.org/10.1016/j.resconrec.2024.107996",
     "peer-reviewed", "legal-economic policy analysis (qualitative)", "barriers to repair; repair market structure", "negative (critique)",
     "The Directive fails to address the most important barriers to repair (planned obsolescence, repair instructions and spare parts, economic incentives), may add administrative burdens for independent repairers, relies mainly on information tools and gives manufacturers power over the repair market",
     "Researchers argue the Directive mostly adds information duties and leaves untouched the biggest obstacles to repair, such as spare-part availability and cost, while strengthening manufacturers' grip on repair.",
     "EU", "qualitative assessment; no outcome data", "abstract read", access="paywalled"),
]
write("32024L1799", "Right to Repair Directive", "52023PC0155", "SWD(2023) 59 (executive summary SWD(2023) 60)",
      "ex-ante only: Commission forecasts plus academic critique; rules apply from July 2026",
      "The Commission forecast that the right to repair would save consumers EUR 176.5 billion and cut 18.4 million tonnes of CO2 over 15 years. The rules only started applying in July 2026, so nothing has been measured yet, and academic critics argue the law does too little about the main barriers to repair, such as the price and availability of spare parts.",
      indicators, literature)
