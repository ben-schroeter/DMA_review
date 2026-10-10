import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2000 proposal has no indicators section; Article 9 required annual Commission reports on spectrum developments"),
 ind("objective", "Harmonised spectrum availability", "Technical harmonisation decisions via the Radio Spectrum Committee", "",
     "14 harmonisation decisions for wireless broadband 2007-2015; 990 MHz harmonised by 2014 and up to 1,268 MHz by 2015, more than other world regions; all measures put to the committee received a positive opinion.", "reported as activity", "COM(2014) 228; SWD(2016) 313"),
 ind("target (RSPP 2012, built on the RSD)", "Wireless broadband spectrum", "At least 1,200 MHz for wireless broadband by 2015", "1,200 MHz",
     "Harmonised: about 1,268 MHz; but Member States had on average assigned only 708 MHz in 2015 (+77% since 2010).", "partially measured", "SWD(2016) 313"),
 ind("outcome (2026 IA)", "Timely assignment", "Coordinated availability of harmonised bands across Member States", "5G pioneer bands deadline 31 Dec 2020",
     "Assignment of 5G pioneer bands spanned over a decade; about half of Member States missed the 2020 deadline; Commission links late assignment to slower 5G coverage.", "measured", "SWD(2026) 13"),
]
literature = [
 lit("ec-2014-rspp-report", "European Commission", 2014, "Report on the implementation of the Radio Spectrum Policy Programme (incl. Art. 9 Radio Spectrum Decision)", "COM(2014) 228", EU + "52014DC0228",
     "Commission evaluation (implementation report)", "implementation review", "spectrum harmonisation", "positive",
     "Radio Spectrum Decision 'has proven successful' in making harmonised spectrum available; 990 MHz harmonised for wireless broadband, Member States had assigned on average about 600 MHz; stronger coordination of authorisations needed",
     "The Commission judged its spectrum-harmonisation machinery a success, while noting countries had put only part of the harmonised spectrum to use.",
     "EU, 2002-2013", "self-evaluation; descriptive", "full text partly read"),
 lit("ec-2016-ecomms-evaluation", "European Commission", 2016, "Evaluation of the regulatory framework for electronic communications", "SWD(2016) 313", EU + "52016SC0313",
     "Commission evaluation", "REFIT evaluation (study, consultation)", "spectrum assignment; internal market", "mixed",
     "Framework identified more spectrum for wireless broadband (up to 1,268 MHz) than Australia, South Korea, Japan or the US, but Member States had assigned only 708 MHz on average in 2015; multi-year lags between first and last Member State (e.g. 800 MHz) delayed services",
     "The 2016 evaluation found the EU harmonised plenty of mobile spectrum, but national governments were slow and uneven in handing it out.",
     "EU, 2009-2015", "self-evaluation", "full text partly read"),
 lit("ec-2026-dna-ia", "European Commission", 2026, "Impact assessment accompanying the proposal for a Digital Networks Act (amending Decision 676/2002/EC)", "SWD(2026) 13", EU + "52026SC0013",
     "Commission impact assessment", "ex-ante, with evaluation annex", "5G spectrum assignment; investment", "negative (baseline)",
     "5G pioneer band (700 MHz, 3.6 GHz, 26 GHz) assignment spanned more than ten years; about half of Member States missed the end-2020 deadline; correlation between assignment timing and 5G coverage; spectrum about 7% of mobile revenues",
     "The Commission's 2026 assessment found Europe's 5G spectrum was handed out late and unevenly, which it links to slower 5G roll-out.",
     "EU, 2016-2025", "self-assessment; correlational", "full text partly read"),
]
write("32002D0676", "Radio Spectrum Decision", "52000PC0407", "none (2000); evaluated in SWD(2016) 313; amendments assessed in SWD(2026) 13",
      "thin: Commission implementation reports and evaluations only; no independent causal studies found",
      "The 2002 decision set up the EU process for harmonising technical rules on radio spectrum. The Commission credits it with making more mobile broadband spectrum available than other world regions, but countries were slow to put that spectrum to use: by 2015 they had assigned only about 708 MHz of a 1,200 MHz target, and 5G bands took over a decade to assign. No independent study isolates its economic effects.",
      indicators, literature)
