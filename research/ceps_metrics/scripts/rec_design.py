import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no indicators section; the memorandum says the Commission will monitor the spare-parts market to see whether the EU-wide repair clause yields the predicted savings, and refers to indicators in Section 9 of the impact assessment"),
 ind("expected impact (impact assessment)", "Open the spare-parts aftermarket to competition", "Consumer savings of EUR 340-544m a year once the 10-year transition for existing designs ends; benefits rising EUR 4-13m a year during the transition", "EUR 340-544m / year",
     "Not measured; transposition deadline December 2027. Ex-ante causal evidence (Herz & Mejer) finds design protection raises spare-part prices by about 5-8%.", "not measured", "SWD(2022) 368/369; Herz & Mejer 2020"),
 ind("expected impact (impact assessment)", "Accessible and affordable design protection", "Annual savings of EUR 6m from lower EU design fees and EUR 1.6m from simpler procedures", "EUR 7.6m / year",
     "Not evaluated (fee changes apply via the parallel EU Design Regulation 2024/2822).", "not measured", "SWD(2022) 369"),
 ind("expected impact (impact assessment)", "Align national design laws with the EU system", "Lower cost and more predictability for firms protecting designs across Member States", "", "Not measured.", "not measured", "SWD(2022) 369"),
]
literature = [
 lit("ec-2022-design-ia", "European Commission", 2022, "Impact Assessment accompanying the proposals to amend the Community Design Regulation and recast the Design Directive (executive summary SWD(2022) 369)", "SWD(2022) 368", EU + "52022SC0369",
     "Commission impact assessment", "ex-ante", "spare-part prices; consumer savings; registration costs", "positive (forecast)",
     "Liberalising must-match spare parts (option 1.2) would save consumers EUR 340-544m a year after a 10-year transition, matched by lost income for carmakers; lower fees save EUR 6m a year and simpler procedures EUR 1.6m",
     "The Commission expected that opening the market for visible car spare parts would save consumers EUR 340-544 million a year once fully in effect.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("herz-mejer-2020-design-spare-parts", "Herz & Mejer", 2020, "The effect of design protection on price and price dispersion: Evidence from automotive spare parts", "MPRA Paper 104137", "https://mpra.ub.uni-muenchen.de/104137/",
     "working paper", "difference-in-differences (cross-country variation in repair-clause coverage, detailed spare-part price data)", "spare-part prices; price dispersion", "negative effect of design protection on consumers (supports reform)",
     "Design protection raises spare-part prices by about 5-8%, with large differences across carmakers; lack of harmonisation plus pricing-to-market explains part of large cross-country price gaps for identical parts",
     "Comparing countries with and without a repair clause, the study finds design protection makes visible car spare parts about 5-8% more expensive - the kind of saving the Directive aims to unlock.",
     "EU car spare-parts markets", "causal (DiD); pre-reform evidence, not an evaluation of the Directive", "abstract read",
     pdf_url="https://mpra.ub.uni-muenchen.de/104137/", interested_party="Co-author Mejer is European Commission staff (ec.europa.eu affiliation); the study fed the Commission's analysis"),
 lit("ec-2020-design-evaluation", "European Commission", 2020, "Evaluation of EU legislation on design protection", "SWD(2020) 264", EU + "52020SC0264",
     "Commission evaluation", "ex-post evaluation (of Directive 98/71/EC and Regulation 6/2002)", "functioning of design protection system", "mixed",
     "Design protection system works well overall but has shortcomings: outdated procedures and fees, divergent national rules, and an unharmonised spare-parts aftermarket",
     "The Commission's 2020 review found EU design law worked well overall but was outdated and left the car spare-parts market split between countries.",
     "EU, 2003-2019", "evaluation of the predecessor law", "page summary (as summarised in SWD(2022) 369)"),
]
write("32024L2823", "Design Directive", "52022PC0667", "SWD(2022) 368 (executive summary SWD(2022) 369)",
      "ex-ante only, backed by one pre-reform causal price study; transposition due December 2027",
      "The Commission forecast that opening the market for visible car spare parts such as bumpers and lights would save consumers EUR 340-544 million a year once a 10-year transition ends. A pre-reform study comparing countries found design protection makes these parts about 5-8% more expensive, supporting the forecast, but the Directive has not yet been transposed and no savings have been measured.",
      indicators, literature)
