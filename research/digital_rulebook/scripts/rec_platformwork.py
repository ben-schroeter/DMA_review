import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no indicators section; the memorandum refers to core indicators listed in the impact assessment and a review 5 years after entry into force"),
 ind("expected impact (impact assessment)", "Correct employment status", "1.7-4.1 million people reclassified as workers (of about 5.5 million at risk of misclassification among 28 million platform workers)", "1.7-4.1 million",
     "Not measured; transposition deadline 2 December 2026. The adopted text dropped the proposal's list of criteria for the presumption, leaving them to Member States, so the forecast may not hold. Model-based evidence from Spain's 2021 Riders' Law suggests reclassification raised the employee share but reduced riders' total work and wages.", "not measured", "SWD(2021) 396/397; Dolado et al. 2025"),
 ind("expected impact (impact assessment)", "Earnings and public finances", "Platform workers' earnings up to EUR 484m a year; up to EUR 4bn a year more tax and social contributions; platform costs EUR 1.9-4.5bn a year", "",
     "Not measured.", "not measured", "SWD(2021) 397"),
 ind("expected impact (impact assessment)", "Algorithmic management", "Improved working conditions for 28 million people through transparency, human oversight and redress rights", "28 million", "Not measured.", "not measured", "SWD(2021) 397"),
]
literature = [
 lit("ec-2021-platformwork-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Directive on improving working conditions in platform work (executive summary SWD(2021) 397)", "SWD(2021) 396", EU + "52021SC0397",
     "Commission impact assessment", "ex-ante", "employment status; earnings; platform costs; public revenue", "positive (forecast)",
     "1.7-4.1 million people reclassified as workers; earnings up to +EUR 484m a year; platform costs EUR 1.9-4.5bn a year, partly passed on; up to EUR 4bn a year extra public revenue",
     "The Commission expected 1.7-4.1 million people working through apps to be reclassified as employees, gaining up to EUR 484 million a year, at a cost to platforms of EUR 1.9-4.5 billion a year.",
     "EU-27, forecast", "forecast; based on the proposal's criteria, later dropped", "full text read (executive summary)"),
 lit("dolado-janez-wellschmied-2025-riders", "Dolado, Jáñez & Wellschmied", 2025, "Riders on the Storm", "IZA Discussion Paper 17740 (also CEPR DP19974)", "https://www.iza.org/publications/dp/17740",
     "working paper", "structural search-and-matching model calibrated to Spain's 2021 Riders' Law (presumption of employment)", "employment; wages; welfare of delivery riders", "mixed",
     "Spain's presumption of employment for riders raised the share of employees but did not absorb the large outflow from self-employment and lowered riders' wages, causing welfare losses; adding a payroll tax cut for platforms hiring employees would preserve employment and raise welfare",
     "Spain's 2021 law presuming delivery riders are employees - a model for the EU Directive - increased the share of riders on employment contracts but, according to this model, cut overall rider jobs and wages.",
     "Spain, 2021 reform (national precursor)", "model-based, not quasi-experimental; analogous national law", "abstract read", pdf_url="https://docs.iza.org/dp17740.pdf"),
]
write("32024L2831", "Platform Work Directive", "52021PC0762", "SWD(2021) 396 (executive summary SWD(2021) 397)",
      "ex-ante only: Commission forecasts plus model-based evidence from a similar Spanish law; transposition due December 2026",
      "The Commission expected 1.7-4.1 million people working through apps to be reclassified as employees and to earn up to EUR 484 million a year more. The final law left the test for employment status to national rules and applies only from late 2026, so nothing has been measured; a study of a similar Spanish law suggests more riders got contracts but overall rider work and pay fell.",
      indicators, literature)
