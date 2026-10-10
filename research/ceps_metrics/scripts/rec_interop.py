import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("indicator (LFS 1.4.4)", "Delivery", "Components ready for operations by target dates (search portal T0+36 months; common identity repository and multiple-identity detector end-2022/2023; shared biometric matching end-2023)", "complete by end-2023",
     "Far behind schedule: shared biometric matching service launched May 2025; European search portal and common identity repository due June 2026; multiple-identity detector in testing; reporting repository expected Q4 2026.", "measured (delayed)", "COM(2026) 446"),
 ind("indicator (LFS 1.4.4)", "Fast access to data", "Number of searches handled by the European search portal vs total searches", "", "Not yet operational in the reporting period.", "not measured", "COM(2026) 446"),
 ind("indicator (LFS 1.4.4)", "Identity fraud", "Identities linked to the same biometrics; detected identity fraud cases", "", "Multiple-identity detector not yet operational.", "not measured", "COM(2026) 446"),
 ind("indicator (LFS 1.4.4)", "Law enforcement access", "Number of step-1 (hit/no-hit) and step-2 accesses for law enforcement", "", "Not yet operational.", "not measured", ""),
 ind("expected impact (impact assessment)", "Cost savings", "Direct savings of EUR 77.5m a year, mostly for Member State administrations", "EUR 77.5m/yr", "Not measured; components not yet operating.", "not measured", "SWD(2017) 474"),
 ind("expected cost (impact assessment)", "Costs", "One-off cost EUR 169.8m (about half EU, half Member States); EUR 28.5m a year running costs", "EUR 169.8m one-off",
     "By 1 Dec 2025 eu-LISA alone had signed contracts worth EUR 170.8m for interoperability (EUR 133.2m paid), already above the whole one-off estimate for the EU and Member States combined.", "partially measured (cost overrun likely)", "COM(2026) 446"),
]
literature = [
 lit("ec-2017-interop-ia", "European Commission", 2017, "Impact Assessment accompanying the proposals on interoperability between EU information systems (executive summary SWD(2017) 474)", "SWD(2017) 473", EU + "52017SC0474",
     "Commission impact assessment", "ex-ante", "border management; identity fraud; costs", "positive (forecast)",
     "Direct savings EUR 77.5m a year (training, resolving multiple identities); one-off costs EUR 169.8m, running costs EUR 28.5m a year; positive for border control and law enforcement",
     "The Commission expected linking the EU's border and security databases to save national administrations about EUR 77.5 million a year for a one-off cost of about EUR 170 million.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("ec-2026-interop-state-of-play", "European Commission", 2026, "Sixth report on the state of play of preparations for the full implementation of the Interoperability Regulations (covering 2025)", "COM(2026) 446", EU + "52026DC0446",
     "Commission implementation report", "monitoring report", "delivery timeline; costs", "n/a (implementation delayed)",
     "Shared biometric matching service launched 19 May 2025; Entry/Exit System rolled out 12 Oct 2025; search portal and common identity repository to start 12 June 2026; reporting repository Q4 2026; eu-LISA contracts EUR 170.8m signed, EUR 133.2m paid by Dec 2025",
     "Six years on, the first building block went live in 2025 and the rest is due in 2026, about three years later than planned, with spending already above the original estimate.",
     "EU, 2025", "self-reported progress; no outcome data", "full text partly read"),
 lit("ec-2026-eulisa-eval", "European Commission", 2026, "Report on the evaluation of eu-LISA under Article 39 of Regulation (EU) 2018/1726", "COM(2026) 32 (SWD(2026) 980)", EU + "52026DC0032",
     "Commission evaluation", "agency evaluation", "delivery of large-scale IT systems", "mixed",
     "Operational management of existing systems effective, but development of new systems less so: contractor management, internal coordination and resource problems caused significant delays to EES, ETIAS, ECRIS-TCN and revised VIS; warns new tasks would raise the risk of further delays to the interoperability project",
     "The Commission's evaluation of the EU IT agency found it runs existing systems well but has struggled to deliver new ones on time, which has held up the interoperability project.",
     "EU, agency mandate period", "agency evaluation, not of the Regulation's effects", "full text partly read"),
]
write("32019R0817", "Interoperability of EU information systems (borders and visa) Regulation", "52017PC0793", "SWD(2017) 473 (executive summary SWD(2017) 474)",
      "thin: implementation monitoring only; components not yet operating, so none of the outcome indicators can be measured; no independent studies",
      "The Regulation links the EU's border, visa and security databases so officials can check identities in one search and detect people using multiple identities. Delivery is about three years behind plan: the first component went live in May 2025 and the main search tools are due in June 2026, while spending by the EU IT agency alone (EUR 171 million) already exceeds the original one-off cost estimate. The promised savings and anti-fraud benefits cannot yet be measured.",
      indicators, literature)
