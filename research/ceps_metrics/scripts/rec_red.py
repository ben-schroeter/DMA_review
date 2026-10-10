import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Compliance", "Administrative and technical compliance ratios (periodic Member State reports)", "Baseline (IA): 28-56% compliance with essential requirements in market surveillance campaigns; of 6,168 R&TTE items inspected, 68% met essential requirements",
     "ADCO RED statistics: 11,491 inspections in 2022 with about 60% non-compliance, but inspections target problem sectors so not representative. 2018 report found no category with demonstrably low compliance; 2024 report says self-assessment 'has led to low levels of compliance' according to stakeholders.",
     "partially measured", "SWD(2012) 329; COM(2018) 740; COM(2024) 158"),
 ind("LFS indicator (1.4.4)", "Administrative simplification", "Induced administrative cost and burden; number of interpretation issues", "",
     "No quantified burden estimate in either operation report; interpretation issues handled via guidance and expert group.",
     "not measured", "COM(2018) 740; COM(2024) 158"),
 ind("LFS indicator (1.4.4)", "Regulatory barriers to innovation", "Perceived simplicity of introducing innovations", "",
     "Only stakeholder survey views in the 2024 report; no systematic measure.",
     "not measured", "COM(2024) 158"),
 ind("expected impact (impact assessment)", "Reduce harmful interference", "Prevention of harmful interference", "",
     "Not separately measured.", "not measured", "SWD(2012) 329"),
]
literature = [
 lit("ec-2012-red-ia", "European Commission", 2012, "Impact Assessment accompanying the proposal for a Directive on radio equipment", "SWD(2012) 329 (executive summary SWD(2012) 300)", EU + "52012SC0329",
     "Commission impact assessment", "ex-ante", "compliance; market surveillance; administrative costs", "positive (forecast)",
     "Baseline compliance with essential requirements of only 28-56% in surveillance campaigns; revision expected to raise compliance via traceability and registration with limited extra burden",
     "The Commission found that up to half of radio devices checked broke the rules and expected the revised directive to raise compliance at little extra cost.",
     "EU, forecast", "forecast", "full text read (executive summary; IA tables checked)"),
 lit("ec-2018-red-report", "European Commission", 2018, "Report on the operation of the Radio Equipment Directive 2014/53/EU", "COM(2018) 740", EU + "52018DC0740",
     "Commission implementation report", "monitoring report (Article 47)", "transposition; compliance; standards", "n/a",
     "Too early to judge effectiveness; manufacturers used the old directive during transition; no evidence of any category with low compliance",
     "The first review, a year after the transition, said it was too early to judge the directive's effects.",
     "EU, 2016-2018", "descriptive", "full text read"),
 lit("ec-2024-red-report", "European Commission", 2024, "Second Report on the operation of Radio Equipment Directive 2014/53/EU", "COM(2024) 158", EU + "52024DC0158",
     "Commission implementation report", "monitoring report (Article 47; ADCO statistics, stakeholder survey)", "compliance; market surveillance; common charger", "mixed",
     "11,491 inspections in 2022 with about 60% non-compliance (targeted, not representative); stakeholders say self-assessment has led to low compliance; common charger (USB-C) amendment adopted 2022",
     "The second review reports that about 60% of radio products inspected in 2022 failed checks, though inspectors target risky products, and stakeholders doubt self-certification works.",
     "EU, 2018-2023", "descriptive; non-representative sampling", "full text read"),
]
write("32014L0053", "Radio Equipment Directive", "52012PC0584", "SWD(2012) 329 (executive summary SWD(2012) 300)",
      "thin: compliance indicator partially tracked through targeted (non-representative) inspections; burden and innovation indicators not measured; no independent studies found",
      "The Radio Equipment Directive promised higher product compliance with little extra burden. Market surveillance data show around 60% of inspected products failing in 2022, but because inspectors target risky products this does not show whether compliance has improved since the 28-56% baseline. The promised indicators on red tape and innovation were never measured, and no independent study was found.",
      indicators, literature)
