import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No LFS indicators; the memorandum relies on transposition checks, periodic Commission reports, and new obligations for Member States to collect statistics and run a population-based victim survey every 3 years (Eurostat methodology)"),
 ind("monitoring obligation (memorandum)", "Measure the phenomenon", "Administrative statistics on offences (Arts 3-9) and 3-yearly prevalence survey", "Baseline cited in IA: at least one in five children falls victim to sexual violence",
     "Not yet applicable: provisional agreement reported June 2026; not adopted or transposed. Current data not comparable across Member States.", "not measured", "COM(2024) 60 memorandum; SWD(2024) 33"),
 ind("expected impact (impact assessment)", "Prevention, investigation and victim support", "Criminalise livestreamed abuse and online solicitation; longer limitation periods; national coordinating authorities", "",
     "Benefits described qualitatively; costs to Member States described as limited and not quantified.", "not measured", "SWD(2024) 33"),
]
literature = [
 lit("ec-2024-csa-directive-ia", "European Commission", 2024, "Impact Assessment accompanying the proposal for a Directive on combating the sexual abuse and sexual exploitation of children and child sexual abuse material (recast)", "SWD(2024) 33 (executive summary SWD(2024) 34)", EU + "52024SC0033",
     "Commission impact assessment", "ex-ante (includes 2022 evaluation of Directive 2011/93/EU)", "victim protection; investigations; prevention", "positive (forecast)",
     "Qualitative benefits: better identification and support of victims, more effective prevention and investigation, reduced impunity for live-streamed abuse; costs mainly on Member State administrations, described as limited; no direct SME or competitiveness impact. Evaluation found that even with full transposition of the 2011 Directive, abuse is not adequately addressed",
     "The Commission expected the updated rules to help find and support more victims and prosecute more offenders, including for live-streamed abuse, at limited cost to national governments; it gave no numerical forecasts.",
     "EU, forecast", "forecast; qualitative", "executive summary read; full text searched"),
]
write("52024PC0060", "Child Sexual Abuse Directive (recast)", "52024PC0060", "SWD(2024) 33 (executive summary SWD(2024) 34)",
      "ex-ante only: qualitative impact assessment; no quantified forecasts; not yet adopted",
      "The Commission expected the updated criminal-law rules to improve prevention, investigation and support for victims of child sexual abuse, but gave no figures. Its main monitoring tool is a new duty for countries to collect comparable statistics and survey victims every three years, which does not exist yet; a political agreement was reported in June 2026, so there is no evidence on effects.",
      indicators, literature)
