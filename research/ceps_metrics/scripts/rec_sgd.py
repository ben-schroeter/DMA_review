import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no indicators section; the memorandum mentions only transposition monitoring. Article 25 required a review report by 12 June 2024, which was not found published"),
 ind("expected impact (impact assessment, joint with Digital Content)", "Cross-border trade", "Share of businesses selling online cross-border up by more than 5 percentage points (about 122,000 firms)", "+5 pp", "Not evaluated.", "not measured", "SWD(2015) 274"),
 ind("expected impact (impact assessment, joint with Digital Content)", "Consumers", "Retail prices -0.25%; 8-13 million more cross-border online shoppers spending EUR 40 more each a year", "", "Not evaluated.", "not measured", "SWD(2015) 274"),
 ind("expected impact (impact assessment, joint with Digital Content)", "Growth", "EU GDP +0.03% (about EUR 4bn a year)", "EUR 4bn/yr", "Not evaluated.", "not measured", "SWD(2015) 274"),
 ind("expected cost (impact assessment)", "Business costs", "One-off contract adaptation cost of about EUR 7,000 per firm", "", "Not evaluated.", "not measured", "SWD(2015) 275"),
 ind("later amendment", "Sustainability", "Right to Repair Directive (EU) 2024/1799 amends the Directive (12-month extension of seller liability when consumers choose repair)", "", "The repair impact assessment reviewed how the remedies work but did not evaluate the Directive's market effects; several Member States said it was too early as the rules had only just applied.", "reported as activity", "SWD(2023) 59"),
]
literature = [
 lit("ec-2015-dcd-sgd-ia", "European Commission", 2015, "Impact Assessment accompanying the proposals for Directives on contracts for the supply of digital content and for online and other distance sales of goods (executive summary SWD(2015) 275)", "SWD(2015) 274", EU + "52015SC0275",
     "Commission impact assessment", "ex-ante (survey-based estimates and CGE macro model)", "cross-border trade; prices; consumption; GDP", "positive (forecast)",
     "Removing contract-law barriers would raise the share of firms selling cross-border online by more than 5 pp (122,000 firms), cut retail prices 0.25%, add 8-13m cross-border shoppers and raise GDP 0.03% (EUR 4bn a year); one-off cost about EUR 7,000 per firm",
     "The Commission expected common EU rules on faulty goods to cut prices slightly, bring more shops and shoppers online across borders and add about EUR 4 billion a year to GDP.",
     "EU, forecast", "forecast for the original online-only proposal; the adopted Directive covers all sales", "full text read (executive summary)"),
 lit("ec-2023-repair-ia", "European Commission", 2023, "Impact Assessment Report accompanying the proposal on common rules promoting the repair of goods", "SWD(2023) 59", EU + "52023SC0059",
     "Commission impact assessment", "ex-ante (with consultation on functioning of Sale of Goods remedies)", "repair; product lifetimes; remedies", "n/a",
     "Uses the Sale of Goods Directive as the vehicle for repair incentives; notes Member States' concern that it was too early to change rules that had only just applied; no ex-post measurement of the Directive's effect on trade or prices",
     "When proposing a right to repair, the Commission built on these rules but did not measure how they have affected trade or prices.",
     "EU, 2022-2023", "not an evaluation", "full text partly read"),
]
write("32019L0771", "Sale of Goods Directive", "52015PC0635", "SWD(2015) 274 (executive summary SWD(2015) 275), joint with the Digital Content Directive",
      "none ex-post: forecasts only; the review due June 2024 was not found and no independent impact studies were found",
      "The Directive harmonised consumers' rights when goods bought in shops or online are faulty, including a minimum two-year guarantee. The Commission forecast slightly lower prices, 122,000 more firms selling across borders online and about EUR 4 billion a year more GDP. None of this has been measured: the review due in June 2024 has not been found, and the rules have since been amended by the 2024 Right to Repair Directive without an evaluation.",
      indicators, literature)
