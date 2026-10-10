import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no indicators section; the memorandum only promises a review of application and transposition 6 years after entry into force"),
 ind("expected impact (impact assessment)", "Compensation for injured people", "Annual compensation up EUR 0.15-22.13m (wider scope incl. software) and EUR 0.20-43.54m (easier burden of proof) compared with baseline", "up to about EUR 66m / year",
     "Not measured; Member States must apply the new rules to products placed on the market from 9 December 2026.", "not measured", "SWD(2022) 316/317"),
 ind("expected cost (impact assessment)", "Insurance and legal costs for producers", "Insurance premiums up EUR 4.35-8.69m (scope) and EUR 14.35-28.71m (burden of proof) a year; legal costs up EUR 1.12-2.75m a year", "",
     "Not measured. Insurers argued the reform would make some risks (psychological harm, data loss, cyber) hard to price and raise litigation and consumer costs.", "not measured", "SWD(2022) 317; Insurance Europe 2022"),
 ind("expected impact (impact assessment)", "Product safety and legal certainty", "Producers, including non-EU ones, encouraged to place only safe products; clear coverage of software and digital products", "", "Not measured.", "not measured", "SWD(2022) 317"),
]
literature = [
 lit("ec-2022-pld-ia", "European Commission", 2022, "Impact Assessment accompanying the proposal for a Directive on liability for defective products (executive summary SWD(2022) 317)", "SWD(2022) 316", EU + "52022SC0317",
     "Commission impact assessment", "ex-ante", "compensation to victims; insurance premiums; legal costs", "positive (forecast)",
     "Extending no-fault liability to software and other actors raises annual compensation by EUR 0.15-22.13m and easing the burden of proof by EUR 0.20-43.54m; premiums rise EUR 4.35-8.69m and EUR 14.35-28.71m a year; small unquantified price rises for non-EU products",
     "The Commission expected modest effects: tens of millions of euros a year more compensation for people harmed by defective products, including software, and a small rise in producers' insurance premiums.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("ec-2018-pld-evaluation", "European Commission", 2018, "Evaluation of Council Directive 85/374/EEC on liability for defective products", "SWD(2018) 157", EU + "52018SC0157",
     "Commission evaluation", "ex-post evaluation (qualitative; cost-benefit analysis not possible for lack of data)", "consumer protection; single market; burden of proof", "mixed",
     "The 1985 Directive contributes to consumer protection and a level playing field at reasonable cost, but the burden of proof, the EUR 500 threshold and unclear coverage of software and digital products limit its effectiveness",
     "The Commission's review of the 1985 law found it broadly worked but was hard for victims to use, especially for complex and digital products - the problems the new Directive targets.",
     "EU, 1985-2017", "evaluation of the predecessor law", "full text read (conclusions)"),
 lit("insurance-europe-2022-pld", "Insurance Europe", 2022, "Key messages on the European Commission's proposal for a revision of the Product Liability Directive (PLD)", "Position paper, December 2022", "https://insuranceeurope.eu/publications/2788/key-messages-on-the-ec-proposal-for-a-revision-of-the-pld",
     "stakeholder position paper", "qualitative argument", "insurability; litigation; innovation", "negative (critique)",
     "Proposal would compromise insurers' ability to price risk (psychological harm, data loss, cyber), increase litigation and ultimately consumer costs, and could harm innovation",
     "The insurance industry warned that the reform would make some risks hard to insure and lead to more lawsuits and higher costs.",
     "EU", "advocacy; no data", "full text read", interested_party="Insurance industry federation; members underwrite product liability risk"),
]
write("32024L2853", "Product Liability Directive", "52022PC0495", "SWD(2022) 316 (executive summary SWD(2022) 317)",
      "ex-ante only: Commission forecasts, an evaluation of the old law and industry critique; applies from December 2026",
      "The Commission expected the new rules, which extend no-fault liability to software and make claims easier, to raise compensation for victims by up to tens of millions of euros a year, with a small rise in producers' insurance costs. The rules apply only to products placed on the market from December 2026, so there is no evidence yet; insurers warned of more litigation and harder-to-insure risks.",
      indicators, literature)
