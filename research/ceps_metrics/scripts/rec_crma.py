import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("benchmark (Regulation)", "Strengthen the strategic raw materials value chain", "EU capacity as share of annual EU consumption of strategic raw materials by 2030", "Extraction 10%, processing 40%, recycling 25%; no more than 65% from a single third country",
     "European Court of Auditors (Feb 2026) judges the EU unlikely to meet the 2030 benchmarks: targets are non-binding, unclear in basis, mining projects take up to two decades, and 10 of 26 energy-transition materials are not recycled at all.", "mixed evidence", "ECA SR 04/2026"),
 ind("LFS indicator", "Strengthen the value chain", "Number of Strategic Projects financed in the EU and abroad; investment volume", "",
     "47 EU Strategic Projects selected in March 2025 (expected capital investment EUR 22.5bn; 25 extraction, 24 processing, 10 recycling, 2 substitution), further third-country projects in June 2025 and a second call in Sept 2025. Investment actually made not reported.", "reported as activity", "Commission, March 2025"),
 ind("LFS indicator", "Diversify imports", "Monitoring data on trade flows in CRMs", "",
     "ECA found imports from the 14 strategic-partner countries fell between 2020 and 2024 for around half of materials examined.", "partially measured", "ECA SR 04/2026"),
 ind("LFS indicator", "Circularity", "Amount and share of recycled CRMs", "25% recycling benchmark", "ECA: recycling still in its infancy; no Commission measurement yet.", "partially measured", "ECA SR 04/2026"),
 ind("LFS indicator", "Monitoring", "Data and maps of EU mineral resources; strategic stocks at national level", "", "No consolidated figures found.", "not measured", ""),
]
literature = [
 lit("ec-2023-crma-ia", "European Commission", 2023, "Impact Assessment accompanying the Critical Raw Materials Act proposal (executive summary SWD(2023) 162)", "SWD(2023) 161", EU + "52023SC0162",
     "Commission impact assessment", "ex-ante", "supply security; value-chain capacity; costs", "positive (forecast, qualitative)",
     "Preferred option (Strategic Projects with streamlined permitting and finance) expected to help meet EU capacity targets and benefit downstream competitiveness; benefits and costs described qualitatively, IA notes the more ambitious option would have been more effective",
     "The Commission expected Strategic Projects and faster permits to raise EU capacity in critical raw materials, but gave no headline economic figures.",
     "EU, forecast", "forecast; largely qualitative", "full text read"),
 lit("ec-2025-crma-strategic-projects", "European Commission", 2025, "Commission selects 47 Strategic Projects to secure and diversify access to raw materials in the EU", "Press release, 25 March 2025 (as reported by Global Mining Review)", "https://www.globalminingreview.com/mining/27032025/commission-selects-47-strategic-projects-to-secure-and-diversify-access-to-raw-materials-in-the-eu/",
     "Commission implementation record (secondary report)", "administrative record", "investment; project pipeline", "n/a",
     "47 projects in 13 Member States, expected capital investment EUR 22.5bn, covering 14 of 17 strategic raw materials (22 lithium projects)",
     "In March 2025 the Commission designated 47 EU mining, processing and recycling projects with EUR 22.5 billion of planned investment.",
     "EU, 2025", "activity data; planned not realised investment", "page summary via search"),
 lit("eca-2026-crm", "European Court of Auditors", 2026, "Special report 04/2026: Critical raw materials for the energy transition - Not a rock-solid policy", "European Court of Auditors", "https://www.eca.europa.eu/en/publications/SR-2026-04",
     "audit report", "performance audit (document review, trade data, project analysis)", "import diversification; domestic production; recycling", "negative",
     "EU unlikely to secure sufficient strategic raw materials by 2030; CRMA targets non-binding with unclear methodology; imports from strategic partners fell for about half of materials 2020-2024; permitting delays and energy costs hold back domestic projects",
     "The EU's auditors concluded the EU is unlikely to hit its 2030 raw-materials goals: diversification has produced little and recycling is in its infancy.",
     "EU, 2020-2025", "independent audit", "page summary via search"),
]
write("32024R1252", "Critical Raw Materials Act", "52023PC0160", "SWD(2023) 161 (executive summary SWD(2023) 162)",
      "ex-ante plus early audit: Commission activity data and a critical ECA audit; no causal study",
      "The Act set 2030 goals for the EU to mine 10%, process 40% and recycle 25% of the strategic raw materials it uses, and to rely on no single country for more than 65%. The Commission has designated 47 EU Strategic Projects with EUR 22.5 billion of planned investment, but the European Court of Auditors concluded in 2026 that the goals are unlikely to be met. No study has yet measured the Act's effect on supply security or prices.",
      indicators, literature)
