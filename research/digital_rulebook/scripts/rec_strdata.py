import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no LFS indicators; the memorandum says effectiveness will be judged mainly on a set of key performance indicators, with a first evaluation no earlier than five years after application (i.e. after 2031)"),
 ind("expected impact (impact assessment)", "Lower compliance costs for platforms", "Savings for online platforms from replacing uncoordinated data requests", "EUR 54-115m over 5 years",
     "Regulation applies only from 20 May 2026; no data yet.", "not measured", "SWD(2022) 349"),
 ind("expected impact (impact assessment)", "Simpler host registration", "Time saved by new hosts registering (monetised)", "> EUR 1 480m over first 5 years",
     "No data yet.", "not measured", "SWD(2022) 349"),
 ind("expected impact (impact assessment)", "Better public-authority data on short-term rentals", "Regular data flow from platforms via national Single Digital Entry Points", "",
     "Registration and data-sharing obligations applicable since 20 May 2026; no published figures on data flows or compliance found.", "not measured", ""),
]
literature = [
 lit("ec-2022-str-ia", "European Commission", 2022, "Impact Assessment accompanying the proposal on data collection and sharing relating to short-term accommodation rental services (executive summary SWD(2022) 349)", "SWD(2022) 350", EU + "52022SC0349",
     "Commission impact assessment", "ex-ante", "compliance costs; administrative savings", "positive (forecast)",
     "Platform savings EUR 54-115m over 5 years; host time savings above EUR 1.48bn over 5 years; one-off costs ~EUR 8.2m for platforms (~EUR 30,000 each) and ~EUR 3m for national authorities",
     "The Commission expected the rules to save platforms EUR 54-115 million and new hosts more than EUR 1.4 billion in registration time over five years, at small set-up costs.",
     "EU, forecast", "forecast", "full text read"),
]
write("32024R1028", "Short-Term Rental Data Regulation", "52022PC0571", "SWD(2022) 350 (executive summary SWD(2022) 349)",
      "ex-ante only: rules applied from May 2026; no evaluation or independent study yet",
      "The regulation requires hosts to register and platforms such as Airbnb to share activity data with public authorities. The Commission forecast savings of EUR 54-115 million for platforms and over EUR 1.4 billion in time saved for hosts over five years. The rules only started to apply in May 2026, so there is no evidence yet on whether these savings, or better local regulation of short-term rentals, have materialised.",
      indicators, literature)
