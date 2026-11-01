import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Resilient Union communication services", "Governments and EU institutions access initial governmental services in 2025, full capacity in 2027", "Initial services 2025; full capacity 2027",
     "Missed: concession signed Dec 2024 foresaw initial capacity in 2030; after the 2026 review the first satellites are expected to launch in 2029. Interim services rely on pooled GOVSATCOM capacity.", "measured", "European Spaceflight 2026; Payload 2026"),
 ind("expected impact (impact assessment)", "Cost", "Total infrastructure cost about EUR 6bn (EUR 4bn public, EUR 2bn private)", "EUR 6bn",
     "Concession (Dec 2024): EUR 10.55bn for 290 satellites; after the Aug 2026 review over EUR 15.6bn for about 348 satellites, with about EUR 11.6bn public and up to EUR 4bn from the SpaceRISE partners (figures from company releases; Commission did not disclose the revised total).", "measured", "European Spaceflight 2026; Payload 2026"),
 ind("LFS indicator (1.4.4)", "Innovation / New Space", "Number of start-ups, SMEs and midcaps participating in building the infrastructure", "",
     "Not reported; Commission lists large subcontractors (Airbus, Thales Alenia Space, OHB) plus some newer firms (e.g. Aerospacelab).", "not measured", "Payload 2026"),
 ind("LFS indicator (1.4.4)", "Cyber resilience / security accreditation", "System accredited to carry EU classified information; EuroQCI integrated", "",
     "Not yet applicable: system not deployed.", "not measured", ""),
 ind("LFS indicator (1.4.4)", "Broadband and cohesion", "Speed of commercial satellite broadband; new commercial users in rural and strategic areas", "",
     "Not yet applicable: no commercial service before the constellation is deployed.", "not measured", ""),
]
literature = [
 lit("ec-2022-iris2-ia", "European Commission", 2022, "Impact Assessment accompanying the proposal establishing the Union Secure Connectivity Programme 2023-2027 (executive summary SWD(2022) 31)", "SWD(2022) 30", EU + "52022SC0031",
     "Commission impact assessment", "ex-ante", "cost; security of supply; space industry competitiveness", "positive (forecast)",
     "Public-private concession preferred; rough total infrastructure cost EUR 6bn (EUR 4bn public, EUR 2bn private); initial services 2024-25, full operational capability 2027; jobs and value added in the space industry (not quantified in summary)",
     "The Commission expected a EUR 6 billion public-private satellite network giving governments secure links by 2027 and boosting Europe's space industry.",
     "EU, forecast", "forecast", "full text read"),
 lit("parsonson-2026-iris2-review", "Parsonson (European Spaceflight)", 2026, "IRIS2 Gets Green Light With More Money and More Satellites", "European Spaceflight, 8 August 2026", "https://europeanspaceflight.com/iris2-gets-green-light-with-more-money-and-more-satellites/",
     "trade press", "news report of Commission/ESA/SpaceRISE review and company releases", "cost; schedule", "negative (cost and delay)",
     "Concession signed Dec 2024 at EUR 10.55bn for 290 satellites with initial capacity in 2030; Aug 2026 review: total investment over EUR 15.6bn (Hispasat), EUR 11.6bn public, partners up to EUR 4bn; 348 satellites (Commission) vs 342 (Hispasat); first launches 2029",
     "Europe's secure satellite network now looks set to cost over EUR 15.6 billion - more than double the original EUR 6 billion estimate - with first launches only in 2029.",
     "EU, 2024-2026", "journalistic; figures from official and company releases", "full text read"),
 lit("gorman-2026-iris2-build", "Gorman (Payload)", 2026, "Europe's IRIS2 Constellation Enters the Build Phase", "Payload, 10 August 2026", "https://payloadspace.com/europes-iris2-constellation-enters-the-build-phase/",
     "trade press", "news report", "cost; industrial participation", "negative (cost)",
     "About 50% budget increase to ~EUR 15.6bn; at least 348 satellites; ~EUR 11.6bn from EU and member states; national commitments from Spain (up to EUR 2bn), Poland, Hungary; first launch on European launcher targeted 2029",
     "Trade press reports the network's budget rose by about half in the 2026 renegotiation, with most of the extra money coming from public sources.",
     "EU, 2026", "journalistic", "full text read"),
]
write("32023R0588", "Union Secure Connectivity Programme (IRIS²)", "52022PC0057", "SWD(2022) 30 (executive summary SWD(2022) 31)",
      "thin: no outcomes yet; cost and schedule tracking via press reports shows large overruns against the impact assessment",
      "IRIS² is the EU's planned secure satellite communications network. The impact assessment promised initial government services by 2025 and full capacity by 2027 for about EUR 6 billion; by August 2026 the expected cost had risen to over EUR 15.6 billion and first launches had slipped to 2029. No services exist yet, so none of the promised security, broadband or innovation results can be measured.",
      indicators, literature)
