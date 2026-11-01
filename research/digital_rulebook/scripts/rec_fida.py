import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The FiDA proposal has no LFS indicators section; the memorandum only refers to a Commission review (Art. 31), with evaluation no earlier than 3 years after application"),
 ind("expected impact (impact assessment)", "Open finance uptake and innovation", "Customers share financial data beyond payment accounts; market entry of data-driven start-ups", "",
     "Not applicable: regulation not adopted (trilogues stalled in 2025-26, per secondary reports).", "not measured", "SWD(2023) 224"),
 ind("expected impact (impact assessment)", "Compliance costs", "One-off API cost for 17,745 data holders", "EUR 2.2-2.4bn one-off; EUR 147-465m a year recurring",
     "Forecast only.", "not measured", "SWD(2023) 224"),
 ind("expected impact (impact assessment)", "Economic value", "Potential boost from open financial data (external estimate cited by the IA)", "1-1.5% of EU GDP by 2030",
     "Third-party estimate cited in the IA; not a Commission forecast of this regulation's effect.", "not measured", "SWD(2023) 224"),
]
literature = [
 lit("ec-2023-fida-ia", "European Commission", 2023, "Impact Assessment accompanying the proposal for a framework for Financial Data Access", "SWD(2023) 224 (executive summary SWD(2023) 230)", EU + "52023SC0224",
     "Commission impact assessment", "ex-ante", "compliance costs; competition; innovation", "positive (forecast)",
     "Preferred option: one-off API costs of EUR 2.2-2.4bn for 17,745 data holders and EUR 147-465m recurring annual costs, recouped from 3,838 data users through compensation; licensing 350 FISPs about EUR 22m one-off. Benefits (competition, new services, SME access) described qualitatively; cites an outside estimate that open financial data could add 1-1.5% to EU GDP by 2030",
     "The Commission expected FiDA to cost financial firms about EUR 2.2-2.4 billion up front to build data interfaces, in return for more competition and new data-driven services, which it did not put a figure on.",
     "EU, forecast", "forecast", "executive summary read; full text searched"),
 lit("ec-2023-psd2-review", "European Commission", 2023, "Report on the review of Directive 2015/2366/EU on payment services (PSD2)", "COM(2023) 365", EU + "52023DC0365",
     "Commission review report", "evaluation (ex-post, of predecessor open banking rules)", "open banking; competition", "mixed",
     "PSD2 objectives only partly achieved; open banking grew but was hampered by poor-quality data interfaces - the experience FiDA builds on",
     "The Commission's review of the existing open banking rules found they helped new services grow but that banks' data interfaces were often poor, a lesson used in designing FiDA.",
     "EU, 2018-2022", "Commission self-assessment", "page summary via search"),
]
write("52023PC0360", "Financial Data Access Regulation (FiDA)", "52023PC0360", "SWD(2023) 224 (executive summary SWD(2023) 230)",
      "ex-ante only: impact assessment cost estimates; no indicators; regulation not adopted",
      "The Commission estimated that letting customers share their insurance, investment, pension and loan data would cost financial firms EUR 2.2-2.4 billion up front, in return for more competition and new services whose value it did not estimate. The proposal sets no monitoring indicators, and as it has not been adopted (talks stalled in 2025-26) there is no evidence on its effects.",
      indicators, literature)
