import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no indicators section; the memorandum promised a monitoring and evaluation exercise feeding a review (Article 25 set the review for 12 June 2024), which was not found published"),
 ind("expected impact (impact assessment, joint with Sale of Goods)", "Cross-border trade", "122,000 more businesses selling online across borders; intra-EU exports +0.04% (about EUR 1bn)", "+122,000 firms", "Not evaluated.", "not measured", "SWD(2015) 274"),
 ind("expected impact (impact assessment, joint with Sale of Goods)", "Consumers", "8-13 million more consumers buying online cross-border; retail prices -0.25%; household consumption +0.23% (about EUR 18bn)", "", "Not evaluated; cross-border e-commerce has grown, but no study attributes any change to the Directive.", "not measured", "SWD(2015) 274"),
 ind("expected impact (impact assessment, joint with Sale of Goods)", "Growth", "EU GDP +0.03% (about EUR 4bn a year, permanent)", "EUR 4bn/yr", "Not evaluated.", "not measured", "SWD(2015) 274"),
 ind("problem baseline (impact assessment)", "Consumer detriment", "Detriment from faulty digital content of EUR 9-11bn a year (four content types)", "baseline EUR 9-11bn", "No follow-up measurement.", "not measured", "SWD(2015) 275"),
]
literature = [
 lit("ec-2015-dcd-sgd-ia", "European Commission", 2015, "Impact Assessment accompanying the proposals for Directives on contracts for the supply of digital content and for online and other distance sales of goods (executive summary SWD(2015) 275)", "SWD(2015) 274", EU + "52015SC0275",
     "Commission impact assessment", "ex-ante (survey-based estimates and CGE macro model)", "cross-border trade; prices; consumption; GDP", "positive (forecast)",
     "Joint package forecast: 122,000 more firms selling cross-border online, 8-13m more cross-border online shoppers, retail prices -0.25%, household consumption +0.23% (EUR 18bn), GDP +0.03% (EUR 4bn a year); one-off contract adaptation cost about EUR 7,000 per firm; consumer detriment from faulty digital content EUR 9-11bn a year",
     "The Commission expected the digital content and sale of goods rules together to add about EUR 4 billion a year to EU GDP and bring millions more people to shop online across borders.",
     "EU, forecast", "forecast for the original (fully harmonised, online-only) proposals, later changed in negotiation", "full text read (executive summary)"),
 lit("eli-2016-dcd-statement", "European Law Institute", 2016, "Statement of the European Law Institute on the European Commission's Proposed Directive on the Supply of Digital Content to Consumers", "ELI statement", "https://www.europeanlawinstitute.eu/fileadmin/user_upload/p_eli/Publications/ELI_Statement_on_DCD.pdf",
     "expert legal commentary", "legal analysis (ex-ante)", "consumer protection level", "mixed",
     "Supports EU rules on digital content but argues some provisions give insufficient protection and could lower protection existing under national laws",
     "Europe's leading law reform body backed the idea of EU rules on digital content but warned some provisions could reduce consumer protection in some countries.",
     "EU, 2016", "legal opinion on the proposal; not an impact study", "page summary via search", pdf_url="https://www.europeanlawinstitute.eu/fileadmin/user_upload/p_eli/Publications/ELI_Statement_on_DCD.pdf"),
]
write("32019L0770", "Digital Content Directive", "52015PC0634", "SWD(2015) 274 (executive summary SWD(2015) 275), joint with the Sale of Goods Directive",
      "none ex-post: forecasts only; the review due June 2024 was not found and no independent impact studies were found",
      "The Directive gave consumers EU-wide rights when apps, streaming, software and other digital content or services are faulty. The Commission forecast that, with the sister Sale of Goods Directive, it would add about EUR 4 billion a year to EU GDP and bring 8-13 million more people to shop online across borders. None of this has been measured: the Commission's review was due in June 2024 but has not been found, and no independent study has assessed the effects.",
      indicators, literature)
