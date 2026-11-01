import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("indicator (LFS 1.4.4)", "Compliance", "Compliance rates by Member State/sector, for e-commerce and imports", "",
     "Partial: authorities report non-compliance in about 10% of checks (11% in 2019, 9% in 2022), 12% for products under Article 4; no EU-wide compliance-rate series. Commission reports 4.6bn low-value parcels imported in 2024, straining controls.", "partially measured", "COM(2025) 63; COM(2025) 37"),
 ind("indicator (LFS 1.4.4)", "Cooperation", "Number of coordinated control campaigns and results", "", "Joint actions run through the Union Product Compliance Network (e.g. 2023 online check of 215 offers); no aggregate count found.", "reported as activity", "COM(2025) 63"),
 ind("indicator (LFS 1.4.4)", "Cooperation", "Use of mutual assistance mechanisms and replicated measures", "", "Not reported in available documents; full evaluation (due July 2026) not found.", "not measured", ""),
 ind("indicator (LFS 1.4.4)", "Business awareness", "Awareness/understanding of product rules by businesses", "", "Very low economic operator response to the Article 4 study survey; no measure.", "not measured", "COM(2025) 63"),
 ind("specific provision (Article 4)", "Responsible operator in the EU", "Products sold in the EU must have an EU-based responsible economic operator", "",
     "Article 4 report: operator missing in 7% of checks and wrong in 5%; in a 2023 online joint action only 34% of indicated operators could be confirmed; half of authorities saw no change in compliance and none clearly attributable.", "measured (low compliance online)", "COM(2025) 63"),
 ind("expected cost (impact assessment)", "EU budget", "Union Product Compliance Network about EUR 18m a year", "", "Not evaluated.", "not measured", "SWD(2017) 467"),
]
literature = [
 lit("ec-2017-msr-ia", "European Commission", 2017, "Impact Assessment accompanying the proposal on compliance with and enforcement of Union harmonisation legislation on products (executive summary SWD(2017) 467)", "SWD(2017) 466", EU + "52017SC0467",
     "Commission impact assessment", "ex-ante (qualitative)", "product compliance; enforcement efficiency", "positive (forecast, qualitative)",
     "Products under EU harmonised rules worth over EUR 2,400bn a year (69% of manufactured output); expected fewer non-compliant products, more efficient import checks and a level playing field; EU Product Compliance Network costs about EUR 18m a year",
     "The Commission expected stronger, better coordinated market surveillance to reduce unsafe and non-compliant products, without quantifying the gain.",
     "EU, forecast", "forecast; benefits not quantified", "full text read (executive summary)"),
 lit("ec-2025-msr-art4-report", "European Commission", 2025, "Report on the implementation of Article 4 of Regulation (EU) 2019/1020", "COM(2025) 63", EU + "52025DC0063",
     "Commission implementation report", "review (survey of 108 market surveillance authorities, joint actions, evaluation study)", "compliance; cooperation with operators", "limited effect",
     "85% of authorities checked Article 4; operator absent in 7% and incorrect in 5% of checks; only 34% of indicated operators confirmed in a 2023 online joint action; non-compliance about 10% of checks with no clear change; half of authorities saw no change; not a full evaluation",
     "A Commission review found the rule requiring an EU-based contact for products has had no clear effect on compliance yet, and online sellers often give wrong details.",
     "EU, 2021-2023", "partial report; survey-based; low business response", "full text partly read"),
 lit("ec-2025-ecommerce-toolbox", "European Commission", 2025, "A comprehensive EU toolbox for safe and sustainable e-commerce", "COM(2025) 37", EU + "52025DC0037",
     "Commission communication", "policy document with customs statistics", "imports; product safety", "n/a",
     "4.6bn low-value consignments imported in 2024, nearly double 2023 (2.4bn) and more than triple 2022 (1.4bn); surge of non-compliant products strains authorities; calls for stronger enforcement",
     "The Commission says direct imports of cheap parcels tripled in two years to 4.6 billion in 2024, overwhelming product checks.",
     "EU, 2022-2024", "context, not an evaluation of the Regulation", "full text partly read"),
]
write("32019R1020", "Market Surveillance Regulation", "52017PC0795", "SWD(2017) 466 (executive summary SWD(2017) 467)",
      "thin: one partial Commission report on Article 4 based on authority surveys; full evaluation (due July 2026) not found; no independent studies",
      "The Regulation strengthened checks on products sold in the EU, including a rule that every product must have an EU-based responsible company. A 2025 Commission review found no clear improvement in compliance: about one in ten checked products still fails the rules, and in an online check only a third of the EU contacts given could be confirmed. Meanwhile direct imports of cheap parcels tripled to 4.6 billion in 2024, and the full evaluation is still awaited.",
      indicators, literature)
