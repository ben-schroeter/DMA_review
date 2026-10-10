import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
ECA = "https://www.eca.europa.eu/ECAPublications/SAR-JUS-2024/SAR-JUS-2024_EN.pdf"
indicators = [
 ind("note", "The proposal's LFS has no indicators (1.4.4 lists synergies only) and no new impact assessment: the Commission relied on the January 2018 IA for the first EuroHPC Regulation (SWD(2018) 6). Monitoring is via Horizon Europe evaluations and JU annual activity reports"),
 ind("expected impact (impact assessment)", "World-class supercomputing", "Exascale supercomputers ranking among the world's top three", "Around 2022 (2017 HPC strategy, cited in IA)",
     "Delayed: JUPITER, the first EU exascale system, ranked 4th on TOP500 (2025) and its JEDI module 1st on Green500; 19 of 30 planned procurements done by end-2024.", "measured", "SWD(2025) 420; COM(2025) 771"),
 ind("expected impact (impact assessment)", "Access for science and industry / AI", "Use of EuroHPC systems by researchers, industry, SMEs", "",
     "19 AI Factories being deployed; JUPITER made available to first users end-2024; usage statistics for industry not reported in sources reviewed.", "reported as activity", "COM(2025) 771"),
 ind("legal target (Regulation)", "Private co-investment", "Private members' contributions", "EUR 900m under Horizon Europe; EUR 420m minimum under Horizon 2020",
     "ECA: private members contributed only about EUR 19.8m against the EUR 420m Horizon 2020 minimum; risk to the much larger 2021-2027 target rated medium.", "measured", "ECA 2025"),
 ind("expected impact (impact assessment)", "EU HPC supply chain / technological sovereignty", "Share of European technology in EU systems; EU vendors' global share", "",
     "JUPITER installed by European companies; no systematic market-share data found.", "not measured", ""),
]
literature = [
 lit("ec-2018-eurohpc-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal for a Council Regulation on establishing the European High Performance Computing Joint Undertaking", "SWD(2018) 6", EU + "52018SC0006",
     "Commission impact assessment", "ex-ante (qualitative option comparison)", "HPC capacity; European supply; access", "positive (forecast)",
     "EU consumes about a third of world HPC resources but lags US, China and Japan; joint undertaking to pool EU and national money; cites goal of exascale systems around 2022 ranking among the world's top three; reused for the 2021 Regulation", "The Commission argued that only pooled EU and national money could buy world-class supercomputers, aiming for European exascale machines among the world's top three around 2022.",
     "EU, forecast", "forecast; qualitative", "full text skimmed"),
 lit("ec-2025-dep-interim-hpc", "European Commission", 2025, "Interim Evaluation of the Digital Europe Programme (HPC objective implemented by EuroHPC)", "SWD(2025) 420; COM(2025) 771", EU + "52025SC0420",
     "Commission evaluation", "interim evaluation (monitoring data)", "procurements; rankings; AI Factories", "positive",
     "19 of 30 planned HPC procurements done (milestone met); JUPITER first EU exascale system, 4th on TOP500 and top of Green500; 19 AI Factories", "The Commission reports that EuroHPC has delivered Europe's first exascale supercomputer, ranked fourth in the world, a few years later than first hoped.",
     "EU, 2021-2025", "self-evaluation; outputs", "full text read (relevant sections)"),
 lit("eca-2025-ju-annual-2024-eurohpc", "European Court of Auditors", 2025, "Annual report on EU joint undertakings for the 2024 financial year", "ECA annual report", ECA,
     "audit report", "financial and compliance audit", "private contributions; budget implementation; staffing", "negative",
     "EuroHPC private members contributed about EUR 19.8m against a EUR 420m minimum target (Horizon 2020/CEF1 period); risk of missing the significantly higher new target rated medium; low implementation of Digital Europe budget; recruitment objective not met", "EU auditors found industry partners have put in only about EUR 20m of the EUR 420m they were meant to contribute, and doubt the higher new target will be met.",
     "EU, 2024", "audit", "full text read (relevant sections)", pdf_url=ECA),
]
write("32021R1173", "EuroHPC Joint Undertaking Regulation", "52020PC0569", "None new; relies on SWD(2018) 6 for Regulation (EU) 2018/1488",
      "thin: output evidence (rankings, procurements) and audit findings; no study of effects on research or industry",
      "EuroHPC pools EU and national money to buy supercomputers. It has delivered Europe's first exascale machine, JUPITER, ranked fourth in the world in 2025 - later than the original aim of a top-three system around 2022. EU auditors found private partners have contributed only about EUR 20m of the EUR 420m expected, and no study yet measures the benefits for science or industry.",
      indicators, literature)
