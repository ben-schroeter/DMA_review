import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2013 proposal (COM(2013) 813) has no financial-statement indicators; Article 18 requires an EUIPO litigation report (2021), a Commission intermediate report (2022) and an impact evaluation (2026)"),
 ind("expected impact (impact assessment)", "Better incentives for cross-border innovation and knowledge-sharing", "Willingness to share trade secrets; spending on protective measures", "Baseline (2012 survey): 40% of EU firms would refrain from sharing trade secrets for fear of misuse; 35% reported higher protection spending after misappropriation",
     "No follow-up survey or measurement found.", "not measured", "SWD(2013) 471/472"),
 ind("expected impact (impact assessment)", "Effective legal redress across the EU", "Litigation patterns and remedies", "",
     "EUIPO study of ~700 national judgments (2017-Oct 2022): litigation volumes and fora vary widely between Member States; cross-border disputes rare; most disputed secrets commercial (62%) rather than technical (33%).",
     "reported as activity", "Borghi, Cogo & Khan / EUIPO 2023"),
 ind("expected impact (impact assessment)", "Innovation, employee mobility, freedom of expression", "Effects on R&D, mobility and whistleblowing", "",
     "No Commission impact evaluation or independent empirical study of these effects found.", "not measured", ""),
]
literature = [
 lit("ec-2013-tradesecrets-ia", "European Commission", 2013, "Impact Assessment accompanying the proposal for a Directive on the protection of undisclosed know-how and business information (trade secrets)", "SWD(2013) 471 (executive summary SWD(2013) 472)", EU + "52013SC0472",
     "Commission impact assessment", "ex-ante (2012 business survey, studies)", "innovation; knowledge sharing; legal certainty", "positive (forecast)",
     "Fragmented national protection weakens incentives for cross-border innovation; 40% of firms would refrain from sharing trade secrets; misappropriation can cut turnover by up to 30%; harmonised redress expected to boost cross-border R&D cooperation",
     "The Commission argued that patchy national protection made firms afraid to share know-how, with 40% saying they held back, and that common rules would encourage innovation.",
     "EU, forecast", "forecast; survey-based problem definition", "full text read (executive summary)"),
 lit("borghi-cogo-khan-2023-euipo", "Borghi, Cogo & Khan (for EUIPO Observatory)", 2023, "Trade Secrets Litigation Trends in the EU", "EUIPO / European Observatory on Infringements of IP Rights", "https://iris.unito.it/handle/2318/1928879",
     "agency-commissioned study", "descriptive (quantitative and qualitative analysis of ~700 national judgments, 2017-2022)", "litigation; enforcement", "n/a",
     "Litigation highly uneven across Member States; cross-border cases uncommon; disputes mostly over commercial information (62%) such as customer lists; data gaps (party identity unknown in 45% of cases)",
     "A study of about 700 court cases found trade-secret litigation still differs a lot between EU countries and mostly concerns commercial data such as customer lists.",
     "EU, 2017-2022", "descriptive; required by Art. 18", "page summary via search; repository metadata checked",
     pdf_url="https://iris.unito.it/bitstream/2318/1928879/1/2023_Trade_Secrets_Litigation_Trends_Study_FullR_en.pdf"),
]
write("32016L0943", "Trade Secrets Directive", "52013PC0813", "SWD(2013) 471 (executive summary SWD(2013) 472)",
      "thin: one descriptive litigation study; the Commission's Article 18 impact evaluation (due June 2026) was not found; no causal evidence on innovation",
      "The Trade Secrets Directive aimed to encourage innovation by giving firms the same protection for confidential know-how across the EU; the Commission cited a survey in which 40% of firms said they held back from sharing secrets. An EU-commissioned study of about 700 court cases shows litigation still varies widely between countries and rarely crosses borders. No study has measured whether the directive changed innovation, knowledge-sharing or worker mobility.",
      indicators, literature)
