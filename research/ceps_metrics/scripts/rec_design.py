import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 1993 proposal has no indicators section"),
 ind("objective", "Simple, affordable EU-wide design protection", "Unitary registered and unregistered Community design administered by EUIPO", "",
     "Steady growth in filings (nearly 1.5m registered Community designs 2003-2019); 2020 evaluation: registration cheaper, simpler and faster than national routes, but system underused and partly outdated for digital designs.", "reported as activity", "SWD(2020) 264; Filitz et al. 2015"),
 ind("objective", "Single market for products embodying designs", "Undistorted competition", "",
     "Broadly achieved except spare parts: 12 Member States liberalised, others keep manufacturers' monopoly; market fragmented.", "reported as activity", "SWD(2020) 264; SWD(2022) 368"),
 ind("expected impact (2022 IA)", "Spare parts liberalisation and fee cuts", "Consumer savings from opening must-match spare parts market; fee savings", "EUR 340-544m consumer savings after 10 years; EUR 6m/yr fee savings",
     "Reform adopted 2024; not yet evaluated.", "not measured", "SWD(2022) 368"),
]
literature = [
 lit("ec-2020-design-evaluation", "European Commission", 2020, "Evaluation of EU legislation on design protection (executive summary SWD(2020) 265)", "SWD(2020) 264", EU + "52020SC0264",
     "Commission evaluation", "evaluation (external studies, consultation)", "access to protection; single market; costs", "positive overall, shortcomings",
     "Broadly fit for purpose; unitary registration lowered costs, complexity and delays; benefits outweigh costs; but system underused (lack of awareness), not adapted to digital designs, spare parts market fragmented, fees and procedures create unnecessary burden",
     "The Commission's 2020 review found the EU design right works well and is cheaper than national routes, but is underused and out of date for digital designs.",
     "EU, 2003-2019", "self-evaluation", "full text read (executive summary)"),
 lit("ec-2022-design-ia", "European Commission", 2022, "Impact assessment on the revision of EU design legislation (executive summary SWD(2022) 369)", "SWD(2022) 368", EU + "52022SC0368",
     "Commission impact assessment", "ex-ante", "consumer savings; fees", "positive (forecast)",
     "Design-intensive industries almost 16% of EU GDP and 14% of jobs (2014-2016); liberalising spare parts to save consumers EUR 340-544m once fully phased in; lower fees save EUR 6m a year; simpler procedures EUR 1.6m a year",
     "The Commission expected its design-law reform to save consumers EUR 340-544 million by opening up the car spare-parts market.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("filitz-henkel-tether-2015", "Filitz, Henkel & Tether", 2015, "Protecting aesthetic innovations? An exploration of the use of registered community designs", "Research Policy 44(6)", "https://doi.org/10.1016/j.respol.2015.02.004",
     "peer-reviewed", "exploratory qualitative (German firms in footwear, cars, tool-making) plus filing statistics", "use of design rights", "neutral",
     "About three-quarters of a million RCDs filed in the first decade; firms use RCDs in very different ways across industries; little prior empirical research on design rights",
     "A study of German firms found registered Community designs are widely used but in very different ways across industries, and that their economic effects are barely studied.",
     "EU/Germany, 2003-2013", "qualitative; no effect estimate", "abstract read"),
]
write("32002R0006", "Community Design Regulation", "51993PC0342", "none (1993); evaluation SWD(2020) 264; revision IA SWD(2022) 368",
      "thin: Commission evaluation and impact assessment; independent research mostly descriptive; no causal studies",
      "The 2002 regulation created a single EU-wide design right run by the EU IP office. The Commission's 2020 evaluation found it cheaper and simpler than national routes and widely used (about 1.5 million registrations by 2019), but underused by small firms and outdated for digital designs. Its 2024 reform is forecast to save consumers EUR 340-544 million by opening up car spare parts; no independent study measures effects on innovation or prices.",
      indicators, literature)
