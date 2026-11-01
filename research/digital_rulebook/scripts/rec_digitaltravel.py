import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Common standard and app", "Adoption of implementing acts; start of operation of the EU Digital Travel application", "Start of operation by end 2030",
     "Not applicable: proposal not adopted; app not built.", "not measured", "COM(2024) 670 LFS"),
 ind("LFS indicator (1.4.4)", "Advance checks", "Share of Member States connected to the Traveller Router at go-live", "100%",
     "Not measured.", "not measured", "COM(2024) 670 LFS"),
 ind("LFS indicator (1.4.4)", "Uptake", "Share of passport/ID applicants also requesting a digital travel credential; share of border crossers using DTCs", "0 to 25% of applicants within 2 years; 30% of travellers within 5 years",
     "Not measured; only national DTC pilots (e.g. Finland, Croatia, Netherlands) exist.", "not measured", "COM(2024) 670 LFS; SWD(2024) 671"),
 ind("LFS indicator (1.4.4)", "Data quality", "Errors in creating/submitting DTCs from ICAO-compliant documents", "0%",
     "Not measured.", "not measured", "COM(2024) 670 LFS"),
 ind("expected impact (impact assessment)", "Smoother border crossing", "Shorter waiting times at external borders; 1-3 minutes for travellers to create a DTC", "",
     "Pilot evidence only (Finland, Croatia, Netherlands, cited in IA): processing time of pre-cleared DTC travellers fell from 30-90 seconds to under 9 seconds; monetary value of time savings not quantified.", "partially measured", "SWD(2024) 671"),
]
literature = [
 lit("ec-2024-digital-travel-ia", "European Commission", 2024, "Impact Assessment accompanying the proposal establishing an application for the electronic submission of travel data (EU Digital Travel application)", "SWD(2024) 671 (executive summary SWD(2024) 672)", EU + "52024SC0671",
     "Commission impact assessment", "ex-ante", "border security; waiting times; public costs", "positive (forecast)",
     "Preferred option (mandatory acceptance of DTCs) has highest expected uptake and allows advance checks; costs: about EUR 2m per Member State on average (pilots: EUR 300,000-700,000 plus up to EUR 250,000 servers), eu-LISA EUR 49.5m one-off to 2031 and ~20 FTE; time savings not monetised; EU-funded DTC pilots cut processing of pre-cleared travellers from 30-90 seconds to under 9 seconds",
     "The Commission expected a common EU travel app for digital passports to speed up border checks and improve security, at about EUR 2 million per country plus EUR 49.5 million for the EU agency that would build it.",
     "EU/Schengen, forecast", "forecast; benefits not quantified", "executive summary read; full text searched"),
]
write("52024PC0670", "EU Digital Travel Application Regulation", "52024PC0670", "SWD(2024) 671 (executive summary SWD(2024) 672)",
      "ex-ante only: detailed LFS uptake targets; small pilot evidence cited by the Commission; proposal pending",
      "The Commission wants an EU app that lets travellers send a digital copy of their passport before crossing Schengen's external borders, with targets of 30% of travellers using it within five years of launch (planned for end 2030). It expects faster, safer border checks at modest cost, about EUR 2 million per country and EUR 49.5 million for the EU app, Pilots in Finland and Croatia cut border processing of pre-cleared travellers from 30-90 seconds to under 9 seconds, but the EU-wide effect cannot be measured until the app exists.",
      indicators, literature)
