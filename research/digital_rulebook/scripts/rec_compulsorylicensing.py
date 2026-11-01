import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No LFS indicators. Monitoring relies on basic descriptive data (Member States notifying national crisis compulsory licences); the Commission expects use to be rare. Evaluation is due after the first Union compulsory licence is activated (3 years in the proposal; 5 years after first licence in the IA)."),
 ind("expected impact (impact assessment)", "Effective, EU-wide compulsory licensing in cross-border crises", "Union compulsory licences granted; time to supply of crisis-critical products", "Qualitative only: 'significantly lower risk of delays or unavailability of critical products during crisis'",
     "No Union compulsory licence was found in searches since the Regulation entered into force (January 2026). Final text narrowed the scope compared with the proposal (EPRS).", "not measured", "SWD(2023) 122; EPRS 2024/2025"),
 ind("expected impact (impact assessment)", "Lower costs and legal certainty for patent holders, licensees and Member States", "", "Qualitative scores only (+/++/+++); no monetised estimates",
     "Not measured.", "not measured", "SWD(2023) 122"),
]
literature = [
 lit("ec-2023-compulsory-licensing-ia", "European Commission", 2023, "Impact assessment accompanying the proposal on compulsory licensing for crisis management (executive summary SWD(2023) 122)", "SWD(2023) 121", EU + "52023SC0122",
     "Commission impact assessment", "ex-ante (qualitative scoring)", "crisis supply; negotiation costs; legal certainty; patent owners' control", "positive (forecast)",
     "Single EU-level licence expected to cut negotiation and procedure costs and give significantly lower risk of delays or unavailability of critical products in crises; patent owners face some loss of control; compulsory licensing described as an 'extremely low probability event'; impacts scored qualitatively, not monetised",
     "The Commission expected an EU-wide compulsory licence to get critical products to people faster in a crisis, but gave no monetary estimates and expected the tool to be used rarely.",
     "EU, forecast", "qualitative forecast", "full text read"),
 lit("eprs-2025-compulsory-licensing", "European Parliamentary Research Service", 2025, "Union compulsory licensing of patents for crisis management (EU Legislation in Progress briefing, 4th edition)", "EPRS_BRI(2024)757634", "https://www.europarl.europa.eu/thinktank/en/document/EPRS_BRI(2024)757634",
     "Parliament research briefing", "legislative analysis", "scope; stakeholder positions", "n/a",
     "Civil society backed broad application, industry a narrow scope; the 21 May 2025 provisional agreement largely amended the proposal in favour of rights-holders, excluding semiconductor, gas supply and defence crises and dropping the proposed cap on licence fees",
     "The Parliament's researchers report that the final deal narrowed the tool in rights-holders' favour, excluding some crises and dropping a cap on royalties.",
     "EU, 2023-2025", "descriptive", "page summary via search"),
]
write("32025R2645", "Compulsory licensing of patents Regulation", "52023PC0224", "SWD(2023) 121 (executive summary SWD(2023) 122)",
      "ex-ante only: qualitative IA, no indicators; no licence granted so nothing to measure",
      "The Commission expected an EU-wide compulsory patent licence to speed up access to critical products in a crisis, but gave only qualitative estimates and expected it to be used rarely. No EU licence appears to have been granted since the law took effect in January 2026, so there is no evidence on its impact. The final text was narrowed in patent holders' favour.",
      indicators, literature)
