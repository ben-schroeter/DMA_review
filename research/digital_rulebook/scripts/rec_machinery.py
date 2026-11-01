import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no indicators section (the raw extraction picked up Annex text); the memorandum only promises monitoring and a periodic Commission evaluation report. The Regulation applies from 20 January 2027, so no effects can yet be observed"),
 ind("expected impact (impact assessment)", "Burden reduction", "Savings in printing costs from digital instructions, up to EUR 16.6bn a year (EUR 201,000 per company)", "Up to EUR 16.6bn/yr (lower bound ~EUR 4bn per the IA's assumptions as summarised by tcworld)",
     "Not yet applicable (digital instructions allowed from 2027). The estimate rests on an assumption that printing costs are 1-4% of sector turnover, which a technical-communication trade article flags as untested.", "not measured", "SWD(2021) 82/83; tcworld 2024"),
 ind("expected impact (impact assessment)", "Costs", "One-off third-party conformity assessment costs of EUR 202m for high-risk machinery; server costs EUR 29m one-off and EUR 48m a year", "",
     "Not measured; Regulation not yet applicable.", "not measured", "SWD(2021) 83"),
 ind("expected impact (impact assessment)", "Health and safety", "Fewer accidents and occupational injuries (e.g. EUR 15m/yr saved on vibration-related sick leave)", "",
     "Not measured; Regulation not yet applicable.", "not measured", "SWD(2021) 83"),
]
literature = [
 lit("ec-2021-machinery-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Regulation on machinery products (executive summary SWD(2021) 83)", "SWD(2021) 82", EU + "52021SC0083",
     "Commission impact assessment", "ex-ante", "compliance costs; printing savings; safety", "positive (forecast)",
     "Printing savings of up to EUR 16.6bn (EUR 201,000 per company) from digital documentation; EUR 5,000-10,000 per instance saved on interpretation differences; EUR 202m one-off for third-party assessment of high-risk machines; EUR 29m one-off and EUR 48m/yr server costs; EUR 15m/yr saved on vibration-related sick leave. Sector: EUR 663bn turnover (2017), 98% SMEs",
     "The Commission expected the new machinery rules to save manufacturers billions in printing costs by allowing digital manuals, at modest extra cost for checking high-risk machines.",
     "EU, forecast", "forecast", "full text read"),
 lit("tcworld-2024-machinery-digital", "tcworld magazine (based on DIN Mitteilungen, May 2024)", 2024, "The European Machinery Regulation: New requirements for digital instructions for use", "tcworld, June 2024", "https://www.tcworld.info/news/the-european-machinery-regulation-1327",
     "trade press", "commentary on IA assumptions", "printing cost savings", "mixed",
     "IA assumed printing costs of 1-4% of turnover (EUR 6.63-26.5bn/yr), implying savings of about EUR 4bn to EUR 16.6bn (EUR 48,000-201,000 per company); no systematic comparison of usability of digital vs paper formats",
     "A trade article shows the headline savings rest on a broad assumption about printing costs and that the real figure could be a quarter of the top estimate.",
     "EU", "commentary", "full text read", interested_party="Technical-communication industry (tekom) lobbied for digital instructions"),
]
write("32023R1230", "Machinery Regulation", "52021PC0202", "SWD(2021) 82 (executive summary SWD(2021) 83)",
      "ex-ante only: rules apply from January 2027; only impact assessment forecasts and trade commentary",
      "The Machinery Regulation updates EU safety rules for machines, covering new risks from digital technologies and allowing digital instead of printed manuals. The Commission forecast printing savings of up to EUR 16.6 billion a year, but that rests on a broad assumption and the lower end is around EUR 4 billion. The rules only apply from January 2027, so no effects on safety or costs can be measured yet.",
      indicators, literature)
