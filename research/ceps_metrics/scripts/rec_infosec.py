import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator", "SO1: harmonised categories of information and common handling rules", "Guidelines adopted; new markings implemented; handling instructions published; common systems for sensitive non-classified information and EUCI", "",
     "Not applicable yet: proposal still pending (Council Security Committee still revising the text in March 2026; no trilogue agreement found).", "not measured", ""),
 ind("LFS indicator", "SO2: identify and close security gaps", "Recommendations made/implemented; number of information leaks across institutions", "",
     "Not measured. Baseline: Court of Auditors found preparedness 'not commensurate with the threats' and significant incidents up more than tenfold 2018-2021.", "not measured", "ECA SR 05/2022"),
 ind("LFS indicator", "SO3-4: lean cooperation and modernised policies (teleworking)", "Centralised vs local procurement; inspection reports; Coordination Group queries; staff trained; awareness; share of staff with secure teleworking equipment", "",
     "Not measured: proposal pending.", "not measured", ""),
 ind("expected impact (impact analysis)", "Efficiency", "Costs for institutions", "Implementation costs offset by efficiency gains; 2 Commission posts (1 AD, 1 AST) for the Coordination Group secretariat; no impact on Member States or private sector",
     "Not measured.", "not measured", "SWD(2022) 65"),
]
literature = [
 lit("ec-2022-infosec-ia", "European Commission", 2022, "Executive summary of the impact analysis report accompanying the proposal for a Regulation on information security in the institutions, bodies, offices and agencies of the Union", "SWD(2022) 65", EU + "52022SC0065",
     "Commission impact assessment", "ex-ante (qualitative)", "information security level; administrative efficiency", "positive (forecast)",
     "Baseline rules expected to raise overall information security and remove weak links; implementation effort compensated by efficiency gains from common tasks (clearances, accreditation); 1 AD + 1 AST for secretariat; no economic impact on Member States or private sector",
     "The Commission expected common security rules to close weak links between EU bodies at little net cost, but gave no measurable targets.",
     "EU institutions", "qualitative forecast", "full text read"),
 lit("eca-2022-cybersecurity-euibas", "European Court of Auditors", 2022, "Cybersecurity of EU institutions, bodies and agencies: Level of preparedness overall not commensurate with the threats", "Special report 05/2022", "https://op.europa.eu/webpub/eca/special-reports/hack-proofing-eu-institutions-05-2022/en",
     "audit report", "performance audit", "cybersecurity preparedness (baseline)", "n/a",
     "EU bodies' preparedness not commensurate with threats and maturity varies widely; significant incidents rose more than tenfold 2018-2021; recommends binding common rules and more resources for CERT-EU",
     "EU auditors found that many EU bodies were poorly prepared for cyberattacks, which had increased more than tenfold, and called for binding common rules.",
     "EU institutions, 2018-2021", "official audit", "page summary via search"),
]
write("52022PC0119", "Information Security Regulation (proposal)", "52022PC0119", "SWD(2022) 65 (executive summary of impact analysis)",
      "ex-ante only: proposal still pending; qualitative impact analysis and audit baseline",
      "This 2022 proposal would set common information security rules for all EU institutions and agencies; it was still being negotiated in 2026. The Commission expected better protection at little net cost but set no measurable targets. The baseline is an EU audit finding that many EU bodies were poorly prepared as serious cyber incidents rose more than tenfold between 2018 and 2021.",
      indicators, literature)
