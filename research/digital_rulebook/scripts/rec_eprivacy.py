import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "2000 proposal (COM(2000) 385) predates standard indicators sections; no quantified objectives or indicators were set"),
 ind("expected impact (evaluation criteria)", "Confidentiality of communications / user control (cookie rule)", "Effectiveness of consent rules", "",
     "Commission REFIT evaluation (2017): cookie rule 'not fully effective' - users accept tracking without understanding it, some cookies set without consent; rule also over-inclusive for non-privacy-intrusive cookies.", "measured (qualitative) - not achieved", "SWD(2017) 5/6"),
 ind("expected impact (evaluation criteria)", "Efficiency", "Compliance costs", "", "Supporting study estimates about EUR 658 per business; Commission notes robust cost data largely do not exist.", "partially measured", "SWD(2017) 6"),
]
literature = [
 lit("ec-2017-eprivacy-refit", "European Commission", 2017, "Ex-post REFIT evaluation of the ePrivacy Directive 2002/58/EC (executive summary SWD(2017) 6)", "SWD(2017) 5", EU + "52017SC0006",
     "Commission evaluation", "REFIT evaluation (studies, consultation)", "effectiveness; compliance costs", "mixed",
     "Directive broadly appropriate but enforcement fragmented; cookie rule not fully effective and over-inclusive; compliance costs around EUR 658 per business; robust cost data lacking", "The Commission found the cookie consent rule had not really given people control - they click 'accept' without understanding - while costing businesses a few hundred euros each.",
     "EU, 2002-2016", "self-evaluation; data gaps acknowledged", "full text read"),
 lit("goldfarb-tucker-2011", "Goldfarb & Tucker", 2011, "Privacy Regulation and Online Advertising", "Management Science 57(1)", "https://doi.org/10.1287/mnsc.1100.1246",
     "peer-reviewed", "causal: difference-in-differences (3.3m survey takers, 9,596 ad campaigns; EU vs other countries)", "advertising effectiveness; firm performance", "negative",
     "After the EU privacy rules (ePrivacy Directive) took effect, display advertising became far less effective at changing purchase intent relative to other countries; larger losses for general-content sites such as news and for plain, small ads", "Early EU privacy rules on tracking made online display ads much less effective, hitting news sites hardest.",
     "EU vs non-EU, early 2000s", "measures ad effectiveness (stated purchase intent), not revenue", "abstract read (Crossref)", "paywalled"),
]
write("32002L0058", "ePrivacy Directive", "52000PC0385", "none (2000 proposal); REFIT evaluation SWD(2017) 5",
      "moderate: one influential peer-reviewed causal study; Commission evaluation with acknowledged data gaps",
      "The ePrivacy Directive set no measurable targets. The Commission's own 2017 evaluation found its cookie-consent rule had not given users real control and was over-inclusive, at around EUR 658 compliance cost per business. Independent research found the EU tracking rules made online display advertising markedly less effective, especially for news sites. The proposed ePrivacy Regulation meant to fix this was withdrawn in 2025.",
      indicators, literature)
