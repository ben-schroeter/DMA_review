import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The LFS lists no quantified indicators: it promises a Commission evaluation five years after application and regular monitoring of the effect of free-movement measures, information requests and strategic reserves"),
 ind("LFS objective", "Minimise obstacles to free movement in crises", "Fewer and better-coordinated national crisis restrictions", "",
     "Regulation applies from 29 May 2026; no vigilance or emergency mode activated and no data found.", "not measured", ""),
 ind("LFS objective", "Safeguard availability of crisis-relevant goods and services", "Availability of crisis-relevant products during emergencies", "",
     "No crisis activation yet; not measured.", "not measured", ""),
]
literature = [
 lit("ec-2022-smei-ia", "European Commission", 2022, "Impact Assessment accompanying the Single Market Emergency Instrument proposal (executive summary SWD(2022) 290)", "SWD(2022) 289", EU + "52022SC0290",
     "Commission impact assessment", "ex-ante", "free movement in crises; supply of crisis-relevant goods; business costs", "positive (forecast, qualitative)",
     "Benefits described qualitatively (fewer obstacles to free movement, better availability of crisis goods); costs for firms from information requests, ramp-up obligations and priority-rated orders; SMEs could be hit by mandatory information requests; no headline monetised figures",
     "The Commission expected better crisis coordination and supply of essential goods but did not put a figure on the benefits, and warned that information requests and priority orders could burden firms.",
     "EU, forecast", "forecast; unquantified", "full text read"),
]
write("32024R2747", "Single Market Emergency Instrument (IMERA)", "52022PC0459", "SWD(2022) 289 (executive summary SWD(2022) 290)",
      "ex-ante only: unquantified forecasts; applies from May 2026 and never yet activated",
      "The instrument gives the EU powers to keep goods, services and people moving in a crisis and, as a last resort, to request information from firms or prioritise orders for crisis goods. The Commission's impact assessment described the benefits only in general terms and flagged costs for businesses. It has applied only since May 2026 and has not been activated, so there is no evidence on its effects.",
      indicators, literature)
