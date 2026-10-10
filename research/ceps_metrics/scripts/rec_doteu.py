import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no indicators section (1.4.4 is about synergies); the Commission must assess the .eu domain five years after application (i.e. by October 2027) and every three years after"),
 ind("specific objective (impact assessment)", "Attractiveness of .eu", "Promote the attractiveness and uptake of .eu (incl. opening eligibility to EU citizens living outside the EU)", "",
     "Registrations broadly flat: 3.7m in April 2021 and about 3.79m at end-2025 (EURid figures); Brexit losses offset by pandemic demand; Q3 2025 was the strongest growth quarter.", "measured (registry statistics)", "COM(2022) 1; EURid quarterly reports"),
 ind("specific objective (impact assessment)", "Governance", "Governance reflecting best practice and EU public interest (multistakeholder council)", "", "Multistakeholder Council and new registry selection set up under the Regulation (applies since 13 Oct 2022); no assessment of effects yet.", "reported as activity", "COM(2023) 485"),
 ind("specific objective (impact assessment)", "Trust and security", "Future-proof, secure namespace", "", "Registry reports 100% availability, abuse-prevention early warning system and know-your-customer checks (2019-2021).", "reported as activity", "COM(2022) 1"),
]
literature = [
 lit("ec-2018-doteu-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal on the implementation and functioning of the .eu top-level domain (executive summary SWD(2018) 121)", "SWD(2018) 120", EU + "52018SC0121",
     "Commission impact assessment", "ex-ante (qualitative)", "governance; flexibility; attractiveness of .eu", "positive (forecast, qualitative)",
     "Preferred option: principles-based framework, separate multistakeholder advisory body, relaxed eligibility (EU citizenship criterion) and direct registration; no quantified targets",
     "The Commission expected simpler, more flexible rules and wider eligibility to make the .eu domain more attractive, without setting numerical targets.",
     "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
 lit("ec-2018-doteu-refit-eval", "European Commission", 2018, "REFIT evaluation of Regulations 733/2002 and 874/2004 on the .eu top-level domain (executive summary)", "SWD(2018) 122", EU + "52018SC0122",
     "Commission evaluation", "REFIT evaluation of predecessor rules", "effectiveness; efficiency", "mixed",
     "Old framework still delivered its benefits but was outdated and rigid, with governance and accountability deficiencies and poor fit with a fast-changing domain market",
     "The Commission's evaluation of the old .eu rules found them still useful but outdated and too rigid.",
     "EU, 2002-2017", "self-evaluation of predecessor", "full text read (executive summary)"),
 lit("ec-2022-doteu-report", "European Commission", 2022, "Report on the implementation, functioning and effectiveness of the .eu Top-Level Domain from April 2019 to April 2021", "COM(2022) 1", EU + "52022DC0001",
     "Commission implementation report", "monitoring report (registry data)", "registrations; security", "n/a",
     "3.7 million .eu domains in April 2021 (8th largest ccTLD); growth flattened as Brexit losses were offset by pandemic demand; citizens abroad allowed to register; 100% availability",
     "In 2021 the .eu domain had 3.7 million registrations and growth had flattened.",
     "EU, 2019-2021 (mostly before the new Regulation applied)", "descriptive", "full text partly read"),
 lit("eurid-2025-q4", "EURid (registry)", 2026, "Q4 2025 quarterly update", "EURid quarterly report", "https://cdn.eurid.eu/assets/q4-2025.pdf",
     "registry statistics", "descriptive", "registrations", "n/a",
     "3,790,453 .eu registrations at end-2025; 193,047 new registrations in Q4 2025",
     "By end-2025 the .eu domain had about 3.79 million registrations, roughly the same as in 2021.",
     "EU, 2025", "descriptive; registry operator data", "page summary via search", interested_party="EURid is the registry operator under contract with the Commission"),
]
write("32019R0517", ".eu Top-Level Domain Regulation", "52018PC0231", "SWD(2018) 120 (executive summary SWD(2018) 121); evaluation SWD(2018) 122",
      "thin: registry statistics only; no evaluation of the new Regulation yet (due 2027); no independent studies",
      "The Regulation modernised the rules for the .eu internet domain and opened it to EU citizens living anywhere. Registrations have been broadly flat since it was proposed, at about 3.7-3.8 million (end-2025). The new framework has applied only since October 2022 and its first evaluation is due by 2027; no independent study exists.",
      indicators, literature)
