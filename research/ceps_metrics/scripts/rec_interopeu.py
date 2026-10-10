import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no performance indicators (the 1.4.x sections cover added value and MFF compatibility); monitoring is to rely on existing data and an Interoperable Europe monitoring mechanism"),
 ind("expected impact (impact assessment)", "Administrative savings from interoperability", "JRC estimate of savings potential: citizens up to 24 million hours (EUR 543m) and businesses EUR 568bn a year; cross-border share EUR 5.5-6.3m for citizens and EUR 5.7-19.2bn for businesses", "",
     "Not measured; the IA itself says direct impact is difficult to quantify. First annual report (Dec 2025) says comprehensive monitoring data not yet available.", "not measured", "SWD(2022) 721/722; Commission annual report 2025"),
 ind("objective (proposal)", "Structured cooperation and interoperability by design", "Interoperable Europe Board; mandatory interoperability assessments for trans-European digital public services", "",
     "Board and working group operating since Q4 2024; interoperability assessments mandatory from January 2025; regulatory sandbox implementing act adopted; over 12,000 Academy enrolments.", "reported as activity", "Commission annual report 2025"),
]
literature = [
 lit("ec-2022-iea-ia", "European Commission", 2022, "Impact Assessment accompanying the proposal for an Interoperable Europe Act (executive summary SWD(2022) 722)", "SWD(2022) 721", EU + "52022SC0722",
     "Commission impact assessment", "ex-ante", "administrative time and cost savings", "positive (forecast)",
     "Direct impact hard to quantify; cites JRC estimate (Ulrich et al. 2022, doi:10.2760/72064) of savings potential of up to 24 million hours (EUR 543m) a year for citizens and EUR 568bn a year for businesses, of which cross-border EUR 5.5-6.3m (citizens) and EUR 5.7-19.2bn (businesses)",
     "The Commission, citing its Joint Research Centre, put the potential savings from better-connected public services at up to EUR 543 million a year for citizens and far more for businesses, while admitting the law's own effect is hard to quantify.",
     "EU, forecast", "forecast; savings potential of interoperability in general, not attributable to the Act", "full text read (executive summary)"),
 lit("ec-2022-eif-evaluation", "European Commission", 2022, "Final evaluation of the European Interoperability Framework (EIF)", "SWD(2022) 720", EU + "52022SC0720",
     "Commission evaluation", "ex-post evaluation (supported by CEPS study)", "interoperability cooperation", "mixed",
     "Voluntary EU interoperability cooperation was beneficial but limited by weak incentives, lack of shared ownership and common resources, motivating a binding framework",
     "The Commission's review of the earlier voluntary approach found it useful but too weak, which led to the Act.",
     "EU, 2017-2021", "evaluation of the predecessor framework", "page summary (as summarised in SWD(2022) 722)"),
 lit("ec-2025-interop-annual-report", "European Commission", 2025, "First Annual Report on Interoperability in the Union", "Commission news, 16 December 2025", "https://commission.europa.eu/news-and-media/news/state-interoperability-union-2025-12-16_en",
     "Commission monitoring report", "implementation monitoring", "governance; assessments; take-up", "n/a (activity)",
     "Board and portal established; interoperability assessments mandatory since January 2025; sandbox implementing act adopted; 12,000+ Academy enrolments; Council version notes comprehensive monitoring data not yet available",
     "In its first annual report the Commission says the new governance and mandatory interoperability checks are up and running, but has no data yet on savings.",
     "EU, Apr 2024-2025", "self-reported activity", "full text read (news summary)"),
]
write("32024R0903", "Interoperable Europe Act", "52022PC0720", "SWD(2022) 721 (executive summary SWD(2022) 722)",
      "ex-ante only: savings potential not attributable to the Act; Commission activity reporting",
      "The Commission pointed to large potential savings from better-connected public services - up to EUR 543 million a year for citizens according to its research centre - while admitting the Act's own effect is hard to quantify. The first annual report (December 2025) shows the new governance bodies and mandatory interoperability checks are running, but there is no data yet on savings or service quality.",
      indicators, literature)
