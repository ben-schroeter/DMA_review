import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No impact assessment and no LFS indicators: the memorandum says only that the Commission will monitor the Regulation together with the GDPR. The Regulation applies to cross-border cases opened after 2 April 2027."),
 ind("objective (memorandum)", "Faster cross-border GDPR enforcement and quicker remedies for individuals", "Duration of cross-border investigations; number of disputes sent to the EDPB", "",
     "Baseline only (Commission 2nd GDPR report, data to Nov 2023): ~2,400 cross-border case entries; ~1,500 lead-authority draft decisions, 990 final infringement decisions; median complaint handling 1-12 months across authorities. No post-application data.", "not measured", "COM(2024) 357"),
 ind("objective (memorandum)", "Harmonised complaint admissibility and procedural rights for complainants and parties", "", "",
     "Not measured. Critics (noyb) argued the trilogue text created many procedure types and could lengthen cases; no evidence either way yet.", "not measured", "Euronews Apr 2025; EDPB-EDPS Joint Opinion 01/2023"),
]
literature = [
 lit("ec-2024-gdpr-second-report", "European Commission", 2024, "Second Report on the application of the General Data Protection Regulation", "COM(2024) 357", EU + "52024DC0357",
     "Commission evaluation/review report", "review (DPA and stakeholder input)", "cross-border enforcement (baseline)", "n/a",
     "Almost 2,400 cross-border case entries; ~1,500 draft decisions, 990 final infringement decisions (Nov 2023); DPAs receive 100,000+ complaints a year; calls for swift adoption of the procedural rules proposal to deliver quick remedies",
     "The Commission's 2024 GDPR review described slow, uneven cross-border enforcement and urged adoption of the procedural rules to speed it up.",
     "EU, 2018-2023", "official review", "full text read"),
 lit("edpb-edps-2023-joint-opinion-procedural", "EDPB & EDPS", 2023, "Joint Opinion 01/2023 on the Proposal for a Regulation laying down additional procedural rules relating to the enforcement of Regulation (EU) 2016/679", "EDPB-EDPS Joint Opinion, September 2023", "https://edps.europa.eu/system/files/2023-09/EDPS-EDPB-2023-10-Joint-Opinion-Procedural-Rules-GDPR_EN.pdf",
     "regulator opinion", "legal analysis (ex-ante)", "procedural efficiency; complainants' rights", "positive (forecast)",
     "Welcomes harmonised complaint admissibility and streamlining of cooperation; calls for swift adoption; stresses complainants' procedural rights",
     "Europe's data protection regulators backed the proposal as a way to speed up cross-border cases, while asking for stronger rights for complainants.",
     "EU", "expert opinion", "page summary via search", interested_party="The regulators who apply the rules (the proposal followed the EDPB's own 2022 wish list)"),
 lit("euronews-2025-noyb-procedural", "Euronews (reporting noyb)", 2025, "EU plans to reform data protection rules are 'tangled mess', privacy advocates warn", "Euronews, 18 April 2025", "https://www.euronews.com/next/2025/04/18/eu-plans-to-reform-data-protection-rules-are-tangled-mess-privacy-advocates-warn",
     "NGO critique (press report)", "commentary", "procedural complexity; enforcement speed", "negative (forecast)",
     "noyb argued the trilogue draft would create around ten types of GDPR procedure and could lengthen investigations; Max Schrems called it 'the biggest legislative mess I have seen in a long time'",
     "Privacy group noyb warned that the negotiated text was so complex it could slow, rather than speed up, cross-border GDPR enforcement.",
     "EU, 2025 (pre-final text)", "advocacy view on draft text", "page summary via search", interested_party="noyb files many cross-border GDPR complaints"),
]
write("32025R2518", "GDPR Procedural Regulation", "52023PC0348", "None (no impact assessment carried out)",
      "ex-ante only: no IA or indicators; baseline figures and opposing expert opinions; applies from 2027",
      "The GDPR Procedural Regulation was adopted without an impact assessment or monitoring indicators, aiming to speed up cross-border data protection cases that often take years. It only applies to cases opened from April 2027, so there is no evidence yet on whether it works. Regulators backed it, while privacy campaigners warned the final text may be too complex to deliver faster decisions.",
      indicators, literature)
