import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Reduce cross-border consumer detriment", "Non-compliance rate", "Baseline (IA): average 37% non-compliance in website screenings; detriment ~EUR 770m in five cross-border online markets",
     "Sweeps keep finding high non-compliance (e.g. 2022 sweep: 37% of 399 websites used dark patterns); no consistent trend series against the baseline and no updated detriment estimate.",
     "partially measured", "SWD(2016) 164; COM(2024) 311"),
 ind("LFS indicator (1.4.4)", "Efficient cooperation", "Mutual assistance requests where binding time limits were not respected", "",
     "2024 report describes coordinated-action procedures as 'long and cumbersome' but gives no systematic time-limit compliance figure in the sections reviewed.",
     "not measured", "COM(2024) 311"),
 ind("LFS indicator (1.4.4)", "Tackle widespread infringements", "Number of coordinated and common actions; number of alerts", "",
     "Coordinated actions and alerts counted in the 2024 application report; alerts used unevenly across Member States; outcomes (commitments by major traders) reported qualitatively.",
     "reported as activity", "COM(2024) 311"),
 ind("LFS indicator (1.4.4)", "Enforcement capacity", "National enforcement plans; benchmarking of CPC resources", "",
     "Report finds large differences in national resources are a main impediment; limited evidence on use of the new minimum investigation powers.",
     "reported as activity", "COM(2024) 311"),
]
literature = [
 lit("ec-2016-cpc-ia", "European Commission", 2016, "Impact Assessment accompanying the proposal for a Regulation on cooperation between national authorities responsible for the enforcement of consumer protection laws", "SWD(2016) 164", EU + "52016SC0164",
     "Commission impact assessment", "ex-ante", "consumer detriment; non-compliance; enforcement efficiency", "positive (forecast)",
     "Average non-compliance of 37% in website screenings; consumer detriment of about EUR 770m in five cross-border online sectors; reform expected to reduce non-compliance and detriment",
     "The Commission found more than a third of websites checked broke consumer law, costing consumers about EUR 770 million in five online markets, and expected stronger joint enforcement to cut this.",
     "EU, forecast", "forecast", "full text read (relevant sections)"),
 lit("ec-2024-cpc-report", "European Commission", 2024, "Report on the application of Regulation (EU) 2017/2394 on consumer protection cooperation", "COM(2024) 311", EU + "52024DC0311",
     "Commission evaluation", "application report (supporting study: surveys of authorities, alert entities and targeted traders)", "enforcement; coordinated actions; sweeps", "mixed",
     "Stakeholders consider objectives generally met and coordinated actions efficient; but procedures long and cumbersome, resources uneven across Member States, consumer groups say harm not significantly reduced; sweeps still find widespread non-compliance (37% of sites using dark patterns in 2022)",
     "The Commission's review says joint enforcement against big traders works better than 27 separate actions, but procedures are slow, national resources uneven, and rule-breaking online remains widespread.",
     "EU, 2020-2023", "Commission self-assessment; stakeholder-based", "full text read (relevant sections)"),
]
write("32017R2394", "Consumer Protection Cooperation Regulation", "52016PC0283", "SWD(2016) 164",
      "thin: activity counts and stakeholder views; headline non-compliance indicator not tracked consistently; no independent studies found",
      "The CPC Regulation promised to cut widespread breaches of consumer law, which the Commission put at 37% of websites checked and about EUR 770 million in consumer losses in five online markets. Its 2024 review found joint actions against big traders work, but procedures are slow and national resources uneven, and recent checks still find more than a third of websites using manipulative designs. No study has measured whether consumer harm actually fell.",
      indicators, literature)
