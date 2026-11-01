import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("specific objective", "Ensure consistent application of data protection rules throughout the Union (alignment of EU institutions' rules with the GDPR)"),
 ind("specific objective", "Rationalise the governance model and strengthen compliance and enforcement in EU institutions and bodies"),
 ind("indicator (LFS 1.4.4)", "Governance", "Number of opinions issued by the EDPB and the EDPS", "", "Reported qualitatively: EDPS replies to legislative consultations with opinions and comments; EDPB output growing. No time series tied to the Regulation.", "reported as activity", "COM(2022) 530"),
 ind("indicator (LFS 1.4.4)", "Accountability", "Breakdown of activities of data protection officers", "", "Survey of 56 EU bodies: 54% gave more resources to DPOs; 84% adapted processes so staff consult DPOs. No breakdown of DPO activities.", "partially measured", "COM(2022) 530"),
 ind("indicator (LFS 1.4.4)", "Accountability", "Use made of data protection impact assessments", "", "Annex table of DPIAs by institution 2019-2021 (most by ECB, EIB and Commission); cases sent to the EDPS fell sharply compared with the old prior-checking system, as intended; 94% of bodies find DPIA criteria adequate.", "measured", "COM(2022) 530"),
 ind("indicator (LFS 1.4.4)", "Enforcement", "Number of complaints made by data subjects", "", "Report notes inadmissible complaints to the EDPS rose 2019-2021 (mostly aimed at national controllers); no clear trend in requests from individuals because institutions record them differently.", "partially measured", "COM(2022) 530"),
 ind("indicator (LFS 1.4.4)", "Enforcement", "Fines imposed on data controllers responsible for breaches", "", "None: by 2022 the EDPS had used most powers (e.g. temporary processing bans) but had never issued a fine.", "measured (zero)", "COM(2022) 530"),
 ind("note", "No dedicated impact assessment: the proposal (COM(2017) 8) relied on the GDPR impact assessment and gave no quantified forecasts"),
]
literature = [
 lit("ec-2022-eudpr-report", "European Commission", 2022, "First report on the application of the Data Protection Regulation for EU institutions, bodies, offices and agencies (Regulation 2018/1725)", "COM(2022) 530", EU + "52022DC0530",
     "Commission evaluation", "review (survey of 56 EU bodies, EDPS contribution)", "compliance; enforcement; resources", "positive (self-assessment)",
     "Regulation 'working well and fit for purpose'; 54% of bodies gave more resources to DPOs; DPIAs replaced prior checking and cut routine consultations of the EDPS; EDPS had not used its power to fine; proposes aligning rules for Europol/Eurojust/EPPO",
     "The Commission found the rules for EU institutions work well: bodies invested more in data protection officers and risk assessments, and the supervisor used bans but never fines.",
     "EU institutions, 2018-2021", "self-evaluation based on self-reported survey; no outcome measures", "full text partly read"),
 lit("ec-2025-digital-omnibus-swd", "European Commission", 2025, "Staff working document accompanying the Digital Omnibus proposals", "SWD(2025) 836", EU + "52025SC0836",
     "Commission staff working document", "review (simplification analysis)", "compliance burden", "n/a",
     "Proposes mirroring the Omnibus GDPR amendments in Regulation 2018/1725 to keep EU-institution rules aligned with the GDPR; no new evidence on the Regulation's effects",
     "The Commission's 2025 simplification package would change these rules in step with planned GDPR changes, but presents no new evidence on how they have worked.",
     "EU", "policy document; no ex-post data on EUDPR", "full text partly read"),
]
write("32018R1725", "Data protection by EU institutions Regulation", "52017PC0008", "none (relied on the GDPR impact assessment SEC(2012) 72)",
      "thin: one Commission self-assessment based on a survey of EU bodies; no independent studies found",
      "These rules bring data protection in the EU institutions in line with the GDPR. The Commission's 2022 review, based on a survey of 56 EU bodies, judged them to be working well: over half gave their data protection officers more resources and routine checks by the supervisor fell as intended, but the supervisor had not issued any fines. No independent study has assessed the rules' effects.",
      indicators, literature)
