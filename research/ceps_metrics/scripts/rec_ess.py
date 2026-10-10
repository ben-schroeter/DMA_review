import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2007 proposal has no indicators section; monitoring relies on the Code of Practice peer reviews and statistical programme evaluations"),
 ind("objective", "Reliable, independent European statistics", "Compliance with the European Statistics Code of Practice", "",
     "ECA 2012: Code not yet fully implemented, weak verification and enforcement. 2013-15 peer reviews: 707 recommendations (65 to achieve compliance), professional independence a recurring issue.", "partially measured", "ECA SR 12/2012; COM(2016) 114"),
 ind("expected impact (2023 IA, amendment)", "Timely statistics using new data sources", "Access to privately held and administrative data; crisis response", "Benefits EUR 1.5bn/yr (EUR 577m to business) vs costs EUR 757m/yr",
     "Amendment adopted as Regulation (EU) 2024/3018; evaluation due five years after implementation.", "not measured", "SWD(2023) 240"),
]
literature = [
 lit("eca-2012-statistics", "European Court of Auditors", 2012, "Did the Commission and Eurostat improve the process for producing reliable and credible European statistics?", "Special Report No 12/2012", "https://www.eca.europa.eu/Lists/ECADocuments/SR12_12/SR12_12_EN.PDF",
     "independent audit", "performance audit", "governance; Code of Practice compliance", "negative",
     "Commission and Eurostat had not yet achieved full implementation of the Code of Practice; Code demanding but lacks strong verification and enforcement tools; ambiguity over which elements are binding; statistical programme not an effective planning and accountability tool",
     "The EU's auditors found in 2012 that the rules meant to guarantee trustworthy EU statistics were not fully applied or enforced.",
     "EU, to 2011", "independent audit", "page summary via search"),
 lit("ec-2016-cop-report", "European Commission", 2016, "Report on the implementation of the European Statistics Code of Practice and coordination within the ESS", "COM(2016) 114", EU + "52016DC0114",
     "Commission evaluation (peer review synthesis)", "peer reviews of all Member States, EFTA countries and Eurostat (2013-2015)", "independence; quality; coordination", "mixed",
     "707 peer-review recommendations (avg 21 per country), 65 needed to achieve compliance; professional independence (88 recommendations) and the need to revise statistical laws on appointment and dismissal of chief statisticians were main issues",
     "Independent peer reviews in 2013-2015 made over 700 recommendations, often about protecting statistical offices' independence.",
     "EU/EFTA, 2013-2015", "peer review; descriptive", "full text partly read"),
 lit("ec-2023-ess-ia", "European Commission", 2023, "Impact assessment for the amendment of Regulation (EC) No 223/2009 (executive summary SWD(2023) 241)", "SWD(2023) 240", EU + "52023SC0241",
     "Commission impact assessment", "ex-ante", "timeliness; response burden; costs", "positive (forecast)",
     "Statistics not timely, frequent, detailed or cost-efficient enough; preferred targeted revision: direct benefits EUR 1.5bn a year (EUR 577m for business) vs direct costs EUR 757m a year (EUR 196m for business); micro and small firms exempt from mandatory data sharing",
     "The Commission expected giving statisticians access to private and administrative data to bring EUR 1.5 billion a year of benefits for EUR 757 million of costs.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
]
write("32009R0223", "European Statistics Regulation", "52007PC0625", "none (2007); SWD(2023) 240 for the 2024 amendment",
      "thin: audit and peer-review evidence on governance; no studies of economic effects",
      "The 2009 regulation is the legal basis for EU official statistics and the independence of statistical offices. The EU's auditors (2012) and peer reviews (2013-2015) found the quality code only partly applied, with over 700 recommendations, many on independence. A 2024 amendment giving statisticians access to private data is forecast to bring EUR 1.5 billion a year of benefits for EUR 757 million of costs; it has not yet been evaluated.",
      indicators, literature)
