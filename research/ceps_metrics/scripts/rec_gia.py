import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal has no LFS indicators; the memorandum foresees a report five years after entry into force, based on indicators and a data-collection mechanism to be drawn up by the Communications Committee"),
 ind("expected impact (impact assessment)", "Reduce deployment cost", "Reduction in cost of network deployment to 2030", "EUR 14.5bn; public subsidies EUR 2.4bn lower",
     "Main provisions applied from 12 Nov 2025; not evaluated.", "not measured", "SWD(2023) 47"),
 ind("expected impact (impact assessment)", "Re-use of infrastructure", "New network km deployed by re-using physical infrastructure or coordinating civil works", "470,000 km vs 250,000 km baseline",
     "No data yet.", "not measured", "SWD(2023) 47"),
 ind("expected impact (impact assessment)", "Faster permits", "Administrative cost savings for operators; digital permit procedures", "EUR 40m a year for operators; EUR 3-4m a year for local authorities",
     "About half of Member States had begun adopting implementing measures by March 2026, with divergent approaches to tacit approval of permits.", "reported as activity", "Cullen International 2026"),
 ind("expected impact (impact assessment)", "Contribute to Digital Decade gigabit targets", "Gigabit coverage of households", "100% gigabit by 2030 (Digital Decade)",
     "Coverage tracked in Digital Decade reports but not attributed to the GIA.", "not measured", ""),
]
literature = [
 lit("ec-2023-gia-ia", "European Commission", 2023, "Impact Assessment accompanying the Gigabit Infrastructure Act proposal (executive summary SWD(2023) 47)", "SWD(2023) 46", EU + "52023SC0047",
     "Commission impact assessment", "ex-ante", "deployment costs; subsidies; admin costs; emissions", "positive (forecast)",
     "Deployment costs EUR 14.5bn lower and public subsidies EUR 2.4bn lower; 470,000 km of network via re-use (vs 250,000 km); one-off costs EUR 70m; operator admin savings EUR 40m a year; 0.7 Mt GHG avoided to 2030",
     "The Commission expected the Act to cut the cost of rolling out fibre and 5G by EUR 14.5 billion and save EUR 2.4 billion of public subsidies.",
     "EU, to 2030", "forecast", "full text read"),
 lit("cullen-2026-gia-implementation", "Cullen International", 2026, "National implementation of the EU Gigabit Infrastructure Act", "Cullen International benchmark (March 2026)", "https://www.cullen-international.com/news/2026/03/National-implementation-of-the-EU-Gigabit-Infrastructure-Act.html",
     "consultancy benchmark", "legal benchmarking", "implementation", "n/a",
     "Main provisions applied from 12 Nov 2025; about half of Member States had begun adopting implementing legislation; approaches diverge on tacit approval, access to private buildings and fibre-ready labels",
     "A March 2026 survey found only about half of EU countries had started adapting national law, with different approaches to automatic permit approval.",
     "EU27, 2025-26", "descriptive; full detail paywalled", "page summary via search", access="abstract only",
     interested_party="Commercial regulatory-intelligence firm whose clients include telecom operators"),
]
write("32024R1309", "Gigabit Infrastructure Act", "52023PC0094", "SWD(2023) 46 (executive summary SWD(2023) 47)",
      "ex-ante only: applied from Nov 2025; only implementation tracking",
      "The Commission forecast that the Act would cut the cost of building fibre and 5G networks by EUR 14.5 billion and reduce the public subsidies needed by EUR 2.4 billion, mainly through re-using ducts and poles and faster permits. Its main rules have only applied since November 2025, and by March 2026 about half of EU countries had started adapting national law. No evidence yet shows whether costs have fallen.",
      indicators, literature)
