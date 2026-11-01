import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal was prepared without an impact assessment (noted by the European Court of Auditors); the extracted financial statement sections 1.4.2-1.4.4 contain headings only. The headline benchmark is the Digital Decade target of a 20% EU share of global semiconductor production value by 2030"),
 ind("policy target (Digital Decade)", "Production capacity", "20% of global production value of cutting-edge and sustainable chips by 2030", "20% by 2030 (baseline ~10%)",
     "Off track: Commission July 2024 forecast had the EU's value-chain share rising only from 9.8% (2022) to 11.7% (2030); the 2026 Chips Act 2.0 impact assessment puts EU production share at 8.1% in 2030 despite a 30% capacity rise. ECA: 20% target very unlikely.", "measured", "ECA SR 12/2025; SWD(2026) 504"),
 ind("expected impact", "Investment", "Mobilise public and private investment in EU chip manufacturing", "",
     "About EUR 80bn in announced or planned manufacturing investments; 11 first-of-a-kind facilities approved by end-2025 worth over EUR 31.6bn; capacity expected to rise from 1.07m to 1.39m wafers per month by 2030. Some projects cancelled or suspended (e.g. Intel Magdeburg, per press reports). EU budget provides only EUR 4.5bn of an estimated EUR 86bn.", "partially measured", "SWD(2026) 504; ECA SR 12/2025"),
 ind("expected impact", "Research and innovation (Pillar I)", "Pilot lines, competence centres, design platform, Chips Fund", "",
     "Over 85% of the Pillar I budget committed to five pilot lines, competence centres in all Member States, a design platform and six quantum chip pilot lines; outcomes not yet measurable.", "reported as activity", "SWD(2026) 504"),
 ind("expected impact", "Crisis preparedness (Pillar III)", "Monitoring and crisis response via the European Semiconductor Board", "",
     "Commission evaluation: coordination improved but voluntary information collection insufficient; limited visibility of supply chains weakens crisis preparedness.", "mixed evidence", "SWD(2026) 504 Annex I"),
]
literature = [
 lit("ec-2026-chips-evaluation", "European Commission", 2026, "Impact Assessment report accompanying the Chips Act 2.0 proposal, including the evaluation of the Chips Act (Annex I)", "SWD(2026) 504", EU + "52026SC0504",
     "Commission evaluation", "evaluation (Sept 2023-Nov 2025; consultation, workshops, interviews, IDC data)", "investment; capacity; market share; crisis preparedness", "mixed",
     "Chips Act created a framework quickly and mobilised substantial investment (~EUR 80bn announced; 11 FOAK projects >EUR 31.6bn; capacity +30% by 2030) but EU production share still only 8.1% by 2030 and value-chain share ~11.6%; weak demand aggregation and supply-chain monitoring; long State aid procedures",
     "The Commission's own evaluation says the Chips Act triggered big investment announcements but will leave the EU's share of world chip production roughly unchanged, prompting a 'Chips Act 2.0'.",
     "EU, 2023-2025", "self-assessment; projections", "full text read"),
 lit("eca-2025-chips", "European Court of Auditors", 2025, "The EU's strategy for microchips: Reasonable progress in its implementation, but the Chips Act is very unlikely to be sufficient to reach the overly ambitious Digital Decade target", "ECA Special Report 12/2025", "https://www.eca.europa.eu/en/publications/SR-2025-12",
     "audit report", "performance audit", "market share target; funding; monitoring", "negative",
     "20% target very unlikely; Commission's July 2024 forecast: share from 9.8% (2022) to 11.7% (2030); meeting target would need ~4x capacity; Commission manages only EUR 4.5bn (5%) of EUR 86bn; targets and monitoring unclear; no impact assessment or prior evaluation",
     "The EU's auditors concluded the Chips Act will not get Europe near its goal of 20% of world chip production by 2030 and lacks clear targets and monitoring.",
     "EU, 2022-2024", "independent audit", "ECA press release read in full"),
 lit("garcia-herrero-poitiers-2022", "García-Herrero & Poitiers (Bruegel)", 2022, "Europe's promised semiconductor subsidies need to be better targeted", "Bruegel Blog, 17 October 2022", "https://www.bruegel.org/blog-post/europes-promised-semiconductor-subsidies-need-be-better-targeted",
     "think tank analysis", "ex-ante policy analysis", "subsidy design", "negative (forecast)",
     "The proposed Chips Act over-emphasises production subsidies and focuses too little on raising value added in research",
     "Bruegel economists warned before adoption that the Act bet too heavily on factory subsidies rather than research where Europe adds most value.",
     "EU, 2022", "ex-ante commentary", "abstract read"),
]
write("32023R1781", "European Chips Act", "52022PC0046", "None (proposal prepared without an impact assessment); evaluation in SWD(2026) 504 Annex I",
      "thin but consistent: Commission evaluation and EU auditors agree investment rose but the 20% market-share goal is far out of reach; no causal study",
      "The European Chips Act aimed to double the EU's share of world chip production to 20% by 2030. It has triggered about EUR 80 billion in announced factory investments and a 30% rise in planned capacity, but both the EU's auditors and the Commission's own 2026 evaluation find the EU's share will stay around 8-12%, because other regions are expanding just as fast. No independent study has yet measured its effect on prices, jobs or supply security.",
      indicators, literature)
