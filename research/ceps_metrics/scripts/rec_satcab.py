import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no indicators section; the memorandum promised baseline data collection at entry into force and monitoring of cross-border availability of TV and radio programmes every two to three years. Article 13 required a review report by 7 June 2025, which was not found published"),
 ind("monitoring promise (memorandum)", "Cross-border access", "Cross-border availability of TV and radio programmes (incl. broadcasters' ancillary online services)", "baseline at entry into force", "No baseline or monitoring data found.", "not measured", ""),
 ind("expected impact (impact assessment)", "Transaction costs", "Lower rights-clearance costs for broadcasters' cross-border online services and for retransmission over closed networks (e.g. IPTV)", "", "Not quantified ex ante or measured ex post.", "not measured", "SWD(2016) 301"),
 ind("review question (Directive recital 24)", "Consumers and creative sector", "Benefits for consumers, impact on creative industries and on investment in new content", "", "Review report not found.", "not measured", ""),
]
literature = [
 lit("ec-2016-copyright-ia", "European Commission", 2016, "Impact Assessment on the modernisation of EU copyright rules (executive summary SWD(2016) 302)", "SWD(2016) 301", EU + "52016SC0302",
     "Commission impact assessment", "ex-ante (qualitative)", "rights-clearance costs; cross-border availability of broadcasts", "positive (forecast, qualitative)",
     "Country-of-origin principle for broadcasters' ancillary online services and mandatory collective management for retransmission over closed networks would reduce transaction costs and enhance cross-border distribution of and access to TV and radio programmes; benefits not quantified",
     "The Commission expected simpler copyright clearance to make more TV and radio programmes available online across borders, but did not put a number on the gain.",
     "EU, forecast", "forecast; qualitative only; the adopted scope was narrowed to news, current affairs and fully financed own productions", "full text read (executive summary)"),
]
write("32019L0789", "Satellite and Cable II Directive", "52016PC0594", "SWD(2016) 301 (executive summary SWD(2016) 302)",
      "none: qualitative forecasts only; no baseline data, no review report found and no independent studies found",
      "The Directive aimed to make more TV and radio programmes available online across borders by simplifying copyright clearance for broadcasters' online services and for internet-based retransmission. The Commission promised to monitor cross-border availability but no data have been published, the review due in June 2025 has not been found, and no independent study has measured the effects.",
      indicators, literature)
