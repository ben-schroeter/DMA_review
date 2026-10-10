import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
ECA = "https://www.eca.europa.eu/ECAPublications/SAR-JUS-2024/SAR-JUS-2024_EN.pdf"
indicators = [
 ind("LFS indicator (1.4.4)", "Cybersecurity infrastructure", "Number of cybersecurity infrastructure/tools jointly procured", "",
     "26 cybersecurity infrastructures (CyberHubs, incl. two cross-border) procured and first 12 tools deployed under Digital Europe, in line with targets.", "measured (outputs)", "COM(2025) 771"),
 ind("LFS indicator (1.4.4)", "Competitiveness of EU suppliers", "Global market share of European cybersecurity suppliers", "25% by 2027",
     "No data on market share found in Commission or ECCC reporting.", "not measured", ""),
 ind("LFS indicator (1.4.4)", "Innovation", "Patents, publications, commercial products from next-generation cybersecurity technologies", "", "Not reported.", "not measured", ""),
 ind("LFS indicator (1.4.4)", "Network and skills", "National coordination centres; people trained; curricula aligned", "",
     "Network of 27 national coordination centres set up; stakeholders cite standardised practices and cross-border cooperation as main benefits. ECCC reached financial autonomy only in September 2024.", "reported as activity", "COM(2025) 771; ECA 2025"),
 ind("evaluation clause (Article 38)", "Evaluation", "Independent Commission evaluation of the Centre", "", "No published Commission evaluation found (Oct 2026).", "not measured", ""),
]
literature = [
 lit("ec-2018-eccc-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal establishing the European Cybersecurity Industrial, Technology and Research Competence Centre and the Network of National Coordination Centres (executive summary SWD(2018) 404)", "SWD(2018) 403", EU + "52018SC0403",
     "Commission impact assessment", "ex-ante (qualitative option comparison)", "industrial competitiveness; market share; R&D uptake", "positive (forecast)",
     "Fragmented EU cybersecurity market dominated by non-EU firms; preferred option (Competence Centre plus network, Art. 173/187 TFEU) expected to help EU industry raise market share; target 25% global market share by 2027", "The Commission expected a new competence centre pooling EU and national money to strengthen Europe's cybersecurity industry, aiming for a 25% global market share by 2027.",
     "EU, forecast", "forecast; qualitative", "full text skimmed"),
 lit("ec-2025-dep-interim-cyber", "European Commission", 2025, "The Digital Europe Programme: Main findings of the interim evaluation (cybersecurity objective)", "COM(2025) 771 (SWD(2025) 420)", EU + "52025DC0771",
     "Commission evaluation", "interim evaluation of the funding programme the ECCC implements", "outputs; infrastructure; network", "positive",
     "26 CyberHubs procured in line with targets; 27 national coordination centres; first 12 cybersecurity tools deployed with first users in health", "The Commission's review of Digital Europe reports that the cybersecurity infrastructure the Centre oversees has been bought on schedule, but says nothing yet about effects on Europe's cybersecurity industry.",
     "EU, 2021-2024", "self-evaluation; outputs only", "full text read"),
 lit("eca-2025-ju-annual-2024", "European Court of Auditors", 2025, "Annual report on EU joint undertakings for the 2024 financial year", "ECA annual report", ECA,
     "audit report", "financial and compliance audit", "governance; contributions; internal control", "mixed",
     "ECCC achieved financial autonomy only on 24 Sept 2024; did not disclose members' cumulative contributions or compare them with targets; internal control framework only partly implemented", "EU auditors found the Centre became independent from the Commission only in 2024 and cannot yet show how much Member States have contributed.",
     "EU, 2024", "audit", "full text read (relevant sections)", pdf_url=ECA),
]
write("32021R0887", "European Cybersecurity Competence Centre", "52018PC0630", "SWD(2018) 403 (executive summary SWD(2018) 404)",
      "thin: output counts and audit findings only; headline 25% market-share target not tracked; no independent study",
      "The Centre in Bucharest channels EU cybersecurity funding with Member States. The infrastructure it oversees (26 CyberHubs, 27 national centres) is in place, but the Centre only became operationally independent in late 2024, auditors found gaps in its reporting, and its headline aim of a 25% global market share for EU cybersecurity firms by 2027 is not being tracked.",
      indicators, literature)
