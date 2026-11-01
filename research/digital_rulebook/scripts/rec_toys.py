import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2008 proposal has no indicators section; the 2020 evaluation notes the Directive set no monitoring indicators, so data are incomplete and not comparable"),
 ind("objective (2008 IA)", "Child safety", "Stricter chemical and other safety requirements; fewer accidents", "",
     "No data on accidents or injuries; one in three toy samples inspected by market surveillance is non-compliant; chemical limits judged deficient (age limit 36 months, CMR derogations).", "not measured", "SWD(2020) 287"),
 ind("objective (2008 IA)", "Internal market", "Free movement of toys", "", "Intra-EU toy exports rose about 60% after full application in 2013; number of toy companies +10% in 5 years (not attributed causally).", "partially measured", "SWD(2020) 287"),
 ind("cost (evaluation)", "Proportionate costs", "", "", "One-off costs about 2% of annual turnover, recovered within about 3 years; recurring costs ~7% higher than predecessor; adaptations ~1% of turnover.", "measured", "SWD(2020) 287"),
 ind("expected impact (2023 IA)", "Replacement Toy Safety Regulation", "Generic bans on most harmful chemicals; digital product passport", "Health benefits EUR 240m-1.2bn/yr (endocrine disruptors alone); one-off costs EUR 23.5-397m",
     "Not yet applicable.", "not measured", "SWD(2023) 269"),
]
literature = [
 lit("ec-2008-toys-ia", "European Commission", 2008, "Executive summary of the impact assessment for the proposal on the safety of toys", "SEC(2008) 39", EU + "52008SC0039",
     "Commission impact assessment", "ex-ante (three external studies, consultation of 1,500+ respondents)", "child health; compliance costs", "positive (forecast)",
     "Revised directive preferred to repeal or 'old approach'; ban on CMR substances in accessible parts expected to raise manufacturing costs but bring considerable long-term health benefits (assessed in DALYs); warnings costs expected lower than industry claims; benefits not measurable in detail",
     "The Commission expected tighter toy rules to raise costs somewhat but deliver large, hard-to-measure health gains for children.",
     "EU, forecast", "forecast; largely qualitative", "full text read"),
 lit("ec-2020-toys-evaluation", "European Commission", 2020, "Evaluation of Directive 2009/48/EC on the safety of toys (executive summary SWD(2020) 288)", "SWD(2020) 287", EU + "52020SC0287",
     "Commission evaluation", "evaluation (2015 external study, JRC cost-benefit study, consultations, national reports)", "safety; trade; costs", "mixed",
     "More effective than the 1988 directive, but deficient on chemicals; one in three inspected samples non-compliant; intra-EU exports +60% since 2012/13; one-off costs ~2% of turnover recovered in 3 years or less; toy firms +10% in 5 years; benefits not quantifiable for lack of accident data; no monitoring indicators",
     "The 2020 evaluation found toy trade flourished and costs were modest, but a third of inspected toys broke the rules and there is no data on whether injuries fell.",
     "EU, 2009-2019", "self-evaluation; weak data acknowledged", "full text read (executive summary)"),
 lit("ec-2023-toys-ia", "European Commission", 2023, "Impact assessment for the proposal for a Toy Safety Regulation (executive summary SWD(2023) 270)", "SWD(2023) 269", EU + "52023SC0269",
     "Commission impact assessment", "ex-ante", "health benefits; industry costs", "positive (forecast)",
     "Generic bans on harmful chemicals: health benefits EUR 240m-1.2bn a year for endocrine disruptors alone; one-off redesign costs EUR 23.5-396.66m; testing +EUR 7.3-11.7m a year; EUR 249-367m of products could be affected; digital passport saves industry EUR 13-20m a year in inspections",
     "The Commission expected the new toy rules to avoid EUR 240 million to 1.2 billion a year of health damage from hormone-disrupting chemicals alone.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
]
write("32009L0048", "Toys Safety Directive", "52008PC0009", "SEC(2008) 38 (executive summary SEC(2008) 39)",
      "thin: Commission impact assessments and evaluation only; no data on injuries and no independent studies found",
      "The 2009 directive tightened safety and chemical rules for toys sold in the EU. The Commission's 2020 evaluation found intra-EU toy trade grew about 60% and compliance costs were modest (about 2% of turnover once), but one in three inspected toys broke the rules and there are no data on whether child injuries fell. A replacement regulation is forecast to avoid EUR 240 million to 1.2 billion a year in health damage.",
      indicators, literature)
