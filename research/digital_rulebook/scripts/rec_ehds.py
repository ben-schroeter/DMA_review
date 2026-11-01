import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator", "SO1: empower people through digital access to and control of their health data, incl. across borders", "Healthcare providers connected to MyHealth@EU; volume of data shared cross-border; share of people with access to their EHR; satisfaction with MyHealth@EU", "Patient summaries and ePrescriptions to be exchangeable in all Member States by 2029; images, lab results and discharge reports by 2031",
     "Commission (early 2025): 15 Member States support sharing patient summaries and ePrescriptions via MyHealth@EU; only a few countries can send or receive data digitally across borders; 10 countries still use paper prescriptions. No provider-level, volume or satisfaction figures published yet.", "partially measured", "Commission health data rights page (2025)"),
 ind("LFS indicator", "SO2: interoperable, secure EHR systems", "Certified EHR systems and labelled wellness apps in the EU database; non-compliance cases", "",
     "Not measured: EHR requirements apply only from 2029 onward.", "not measured", ""),
 ind("LFS indicator", "SO3: efficient framework for secondary use of health data", "Datasets in the European data catalogue; data access requests processed/accepted/rejected by health data access bodies", "",
     "Not measured: secondary-use rules apply from 2029; health data access bodies being set up.", "not measured", ""),
 ind("expected impact (impact assessment)", "Economic benefit", "Total economic benefits over 10 years", "Above EUR 11bn benefits vs EUR 0.7-2.5bn costs over 10 years",
     "Forecast only. Independent commentators (EIT Health Think Tank 2024) argue implementation funding is 'significantly misaligned' with the ambition, which could delay benefits.", "not measured", "SWD(2022) 132; EIT Health 2024"),
]
literature = [
 lit("ec-2022-ehds-ia", "European Commission", 2022, "Impact assessment accompanying the proposal on the European Health Data Space (executive summary SWD(2022) 132)", "SWD(2022) 131", EU + "52022SC0132",
     "Commission impact assessment", "ex-ante", "economic benefits; costs; SMEs; access to health data", "positive (forecast)",
     "Preferred option: total economic benefits above EUR 11bn over 10 years; costs EUR 0.7-2.5bn above baseline over 10 years, mainly digital infrastructure (MyHealth@EU, health data access bodies) and certification",
     "The Commission expected the health data space to bring more than EUR 11 billion in benefits over ten years for EUR 0.7-2.5 billion of costs.",
     "EU-27, 10-year forecast", "forecast", "full text read"),
 lit("marcus-et-al-2022-ehds", "Marcus, Martens, Carugati, Bucher & Godlovitch", 2022, "The European Health Data Space", "Study for the European Parliament ITRE committee (Policy Department for Economic, Scientific and Quality of Life Policies); SSRN 4300393", "https://doi.org/10.2139/ssrn.4300393",
     "Parliament-commissioned study", "legal and economic analysis (ex-ante)", "implementation costs; incentives for healthcare providers; governance", "mixed",
     "Examines legal and economic challenges to implementing the proposed EHDS, including costs and incentives for health care providers and EU/Member State institutional interaction; recommends design improvements",
     "A study for the European Parliament found that providers' costs and weak incentives, and the split between EU and national bodies, could hold back the health data space, and proposed design changes.",
     "EU, 2022", "qualitative ex-ante analysis", "abstract read"),
 lit("eit-health-2024-ehds-funding", "EIT Health Think Tank", 2024, "Report on implementing the European Health Data Space (released at EIT Health Summit, May 2024)", "EIT Health (as reported by Pulse IT and Research Professional News)", "https://www.researchprofessionalnews.com/rr-news-europe-innovation-2024-4-more-commitment-needed-for-european-health-data-space/",
     "think tank report (secondary report)", "expert consultation", "implementation funding", "critical",
     "Commission implementation budget 'significantly misaligned with the ambition level' of the regulation; Member States must increase their commitment to funding",
     "A health-innovation think tank warned that the money set aside to implement the health data space falls short of its ambitions and called on national governments to contribute more.",
     "EU, 2024", "expert opinion; report not read directly", "page summary via search", interested_party="EIT Health network includes industry partners that would use health data"),
 lit("ec-2025-myhealth-status", "European Commission (DG SANTE)", 2025, "My rights over my health data", "Commission web page", "https://health.ec.europa.eu/ehealth-digital-health-and-care/my-rights-over-my-health-data_en",
     "Commission statistics", "descriptive", "cross-border exchange of health data (baseline)", "n/a",
     "15 Member States support sharing patient summaries and ePrescriptions via MyHealth@EU; only a few countries can send or receive data digitally across borders in early 2025; 10 countries still use paper prescriptions",
     "In early 2025, 15 EU countries could share patient summaries and e-prescriptions across borders; the EHDS requires all to do so by 2029.",
     "EU, early 2025", "official baseline", "full text read"),
]
write("32025R0327", "European Health Data Space", "52022PC0197", "SWD(2022) 131 (executive summary SWD(2022) 132)",
      "ex-ante only: Commission IA forecast and baseline counts; obligations apply from 2027-2031 so no outcome evidence",
      "The Commission expected the European Health Data Space to bring more than EUR 11 billion in benefits over ten years, by letting patients access and share their records and researchers reuse health data. Most obligations start between 2027 and 2031, so effects cannot be measured yet; in early 2025, 15 countries could exchange patient summaries and e-prescriptions across borders. Independent reviews warn that funding and incentives for healthcare providers may fall short.",
      indicators, literature)
