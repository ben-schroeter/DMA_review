import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2003 proposal has no indicators section; Article 18 required a Commission report three years after transposition"),
 ind("objective", "Effective civil enforcement of IP rights", "Harmonised measures: evidence, right of information, injunctions, damages, legal costs", "",
     "2010 report: 'substantial and positive effect'. 2017 evaluation: improved enforcement conceptually, but econometric models found no statistically measurable effect on litigation indicators; application diverges across courts.", "mixed evidence", "COM(2010) 779; SWD(2017) 431"),
 ind("outcome", "Reduce infringement (piracy, counterfeiting)", "", "",
     "Sweden's 2009 implementation cut internet traffic 18% and raised music sales (physical +27%, digital +48%) over six months, with no effect on films; effects faded later. Commission notes counterfeiting still rising EU-wide.", "partially measured", "Adermon & Liang 2014; SWD(2017) 431"),
 ind("cost (evaluation)", "No undue burden", "", "", "Evaluation study found no incremental direct costs from the Directive; average firm spends about EUR 115,000 a year on IP enforcement overall.", "measured", "SWD(2017) 431"),
]
literature = [
 lit("ec-2010-ipred-report", "European Commission", 2010, "Report on the application of Directive 2004/48/EC on the enforcement of intellectual property rights (with SEC(2010) 1589)", "COM(2010) 779", EU + "52010DC0779",
     "Commission evaluation (implementation report)", "review (national reports)", "civil enforcement", "positive",
     "Directive had a 'substantial and positive effect' on civil protection of IP rights, but was not designed for the challenge of internet infringements; issues with right of information, damages and intermediaries",
     "The first review found the directive had strengthened IP enforcement in court but was not built for online piracy.",
     "EU, 2006-2009", "self-evaluation; based on national reports", "full text partly read"),
 lit("ec-2017-ipred-evaluation", "European Commission", 2017, "Evaluation of Directive 2004/48/EC (accompanying guidance communication)", "SWD(2017) 431", EU + "52017SC0431",
     "Commission evaluation", "evaluation study incl. econometric analysis of IP court cases 2005-2015, consultation", "litigation; costs; effectiveness", "mixed",
     "Directive improved civil enforcement at a conceptual level and imposed no incremental direct costs; but econometric models found no strong correlation, let alone causality, between the Directive and litigation indicators; benefits cannot be quantified; counterfeiting and piracy still rising",
     "The 2017 evaluation judged the directive useful and cheap, but could find no measurable effect on court enforcement, and counterfeiting kept growing.",
     "EU, 2005-2016", "self-evaluation; weak data acknowledged", "full text partly read"),
 lit("adermon-liang-2014-ipred", "Adermon & Liang", 2014, "Piracy and music sales: The effects of an anti-piracy law", "Journal of Economic Behavior & Organization 105", "https://doi.org/10.1016/j.jebo.2014.04.026",
     "peer-reviewed", "natural experiment (time-series around Sweden's IPRED implementation, 1 April 2009)", "piracy; music and film sales", "positive (short-run)",
     "Working-paper version: reform cut Swedish internet traffic by 18% over six months and raised physical music sales 27% and digital 48%; no significant effect on cinema tickets or DVDs; press coverage of the published version reports smaller figures (traffic -16%, music sales +36%) and fading effects",
     "When Sweden implemented the directive, file-sharing dropped and music sales jumped for several months, but film sales did not change and the effect faded.",
     "Sweden, 2008-2009", "credible causal design; single country, short-run", "abstract read (working paper)", pdf_url="https://swopec.hhs.se/iuiwop/abs/iuiwop0854.htm"),
]
write("32004L0048", "IPR Enforcement Directive", "52003PC0046", "none (2003)",
      "thin to moderate: one credible natural-experiment study (Sweden) plus Commission reviews that found no measurable effect on litigation",
      "The 2004 directive harmonised the court tools rights holders can use against IP infringers. A Swedish study found that when the rules came in, file-sharing fell and music sales rose sharply for some months before fading, with no effect on film sales. The Commission's 2017 evaluation judged the directive cheap and useful, but found no measurable effect on court enforcement across the EU, and counterfeiting kept rising.",
      indicators, literature)
