import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator", "Fostering cross-border activity and investment", "Number and value of cross-border investments in EU media markets (annual)", "Baseline 2013-2021: 478 EU and 389 non-EU investor transactions; gradual increase expected",
     "No post-EMFA tracking found.", "not measured", "COM(2022) 457 LFS 1.4.4"),
 ind("LFS indicator", "Regulatory cooperation and convergence", "Board opinions taken into account; share of cases solved by the Board; number of guidance documents", "n/a",
     "European Board for Media Services set up in 2025 and adopted its first reports and deliverables (Dec 2025 plenary); no data on uptake of opinions found.", "reported as activity", "Media Board news"),
 ind("LFS indicator", "Quality media services / editorial independence", "Media Pluralism Monitor risk scores on political independence, PSM governance, owner influence, source protection, ownership transparency", "2021 MPM scores 16-60%; gradual reduction expected",
     "MPM2025 (2024 data) published, but switched to a six-tier scale so results are not strictly comparable with earlier editions; it covers the period before EMFA fully applied (Aug 2025).", "partially measured", "Blagojev et al. 2025"),
 ind("LFS indicator", "Quality media services", "Citizens' trust in media; number of Member States with media self-regulatory bodies", "16 Member States with self-regulatory bodies",
     "Not tracked against the EMFA.", "not measured", ""),
 ind("expected impact (impact assessment)", "Economic", "Net economic benefit (higher media company revenues)", "EUR 2.9bn per year",
     "Not evaluated; first evaluation due four years after entry into force.", "not measured", "SWD(2022) 287"),
]
literature = [
 lit("ec-2022-emfa-ia", "European Commission", 2022, "Impact Assessment accompanying the European Media Freedom Act proposal (executive summary SWD(2022) 287)", "SWD(2022) 286", EU + "52022SC0287",
     "Commission impact assessment", "ex-ante", "media revenues; compliance costs; regulator costs", "positive (forecast)",
     "Annual net economic benefits EUR 2.9bn in higher media revenues; one-off business costs EUR 9.4-14m and recurrent EUR 5.6-14.5m; public authority costs EUR 6.1m a year",
     "The Commission expected the Act to raise media companies' revenues by about EUR 2.9 billion a year, at negligible cost to businesses.",
     "EU, forecast", "forecast", "full text read"),
 lit("blagojev-et-al-2025-mpm", "Blagojev, Bleyer-Simon, Brogi, Carlini, Da Costa Leite Borges, Kermer, Nenadic, Palmer, Parcu, Reviglio, Trevisan & Verza", 2025, "Monitoring media pluralism in the European Union: results of the MPM2025", "EUI Centre for Media Pluralism and Media Freedom, RSC Research Report (doi:10.2870/2415644)", "https://cadmus.eui.eu/handle/1814/92916",
     "independent monitoring report (EU co-financed)", "expert risk assessment (indicator-based)", "media pluralism; editorial independence; ownership transparency", "n/a (baseline)",
     "Risk assessment for 2024 across 32 countries, with insights on EMFA-related themes before the Act fully applied; new six-tier scale not strictly comparable with earlier years",
     "The EU-funded Media Pluralism Monitor gives a pre-EMFA baseline of risks to media freedom; commentary on it describes uneven readiness to apply the Act.",
     "EU27 + 5 candidates, 2024", "descriptive baseline; methodology break", "abstract read", pdf_url="",
     interested_party="Centre is co-financed by the EU and its MPM is the Act's own monitoring indicator source"),
]
write("32024R1083", "European Media Freedom Act", "52022PC0457", "SWD(2022) 286 (executive summary SWD(2022) 287)",
      "ex-ante only: Act fully applicable since Aug 2025; only baseline monitoring data",
      "The Commission forecast that the Media Freedom Act would lift media companies' revenues by about EUR 2.9 billion a year and reduce risks to editorial independence. The Act has only applied in full since August 2025; the new EU media board is operating, but the Media Pluralism Monitor's latest results describe the situation before the Act and use a new scale. No study has yet measured its effects.",
      indicators, literature)
