import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no indicators section; Article 18 required a monitoring programme (set out in SWD(2023) 23) and Article 21 a transposition report (2023) and an impact evaluation by 31 May 2026"),
 ind("specific objective (impact assessment)", "Legal framework", "Clear, robust, technology-neutral criminal law framework (incl. virtual currencies, stolen credentials)", "",
     "Transposition report: 9 Member States on time; infringement cases opened against 16 in July 2021; most provisions transposed, with gaps notably on virtual currency coverage.", "partially measured", "COM(2023) 363"),
 ind("specific objective (impact assessment)", "Investigation and prosecution", "Eliminate operational obstacles to cross-border investigation and prosecution", "", "No outcome data published; the impact evaluation due May 2026 was not found.", "not measured", ""),
 ind("general objective (impact assessment)", "Fraud losses", "Reduce direct losses from non-cash payment fraud and raise trust", "",
     "Fraud is tracked by the ECB/EBA under PSD2 reporting (EUR 4.3bn in 2022, EUR 2.0bn in H1 2023 across instruments), but these figures cannot be attributed to the Directive.", "measured (not attributable)", "EBA/ECB 2024"),
 ind("expected cost (impact assessment)", "Member State costs", "One-off EUR 561,000 and about EUR 2.3m a year across Member States", "", "Not evaluated.", "not measured", "SWD(2017) 298"),
]
literature = [
 lit("ec-2017-ncpfraud-ia", "European Commission", 2017, "Impact Assessment accompanying the proposal on combating fraud and counterfeiting of non-cash means of payment (executive summary SWD(2017) 299)", "SWD(2017) 298", EU + "52017SC0299",
     "Commission impact assessment", "ex-ante", "law enforcement effectiveness; costs to Member States", "positive (forecast, qualitative)",
     "Expected more effective law enforcement, better cross-border and public-private cooperation and more trust in the digital single market; costs EUR 561,000 one-off and about EUR 2.3m a year for Member States; no impact on SMEs",
     "The Commission expected the update of criminal law on payment fraud to make police work more effective at a modest cost to national authorities, but gave no forecast of reduced fraud.",
     "EU, forecast", "forecast; benefits not quantified", "full text read (executive summary)"),
 lit("ec-2023-ncpfraud-transposition", "European Commission", 2023, "Report assessing the extent to which Member States have taken the necessary measures to comply with Directive (EU) 2019/713", "COM(2023) 363", EU + "52023DC0363",
     "Commission implementation report", "legal transposition review", "transposition", "n/a",
     "Only 9 Member States transposed on time; infringement procedures against 16 in July 2021; transposition largely complete by 2023 but gaps remain, notably on coverage of virtual currencies",
     "The Commission's check found most countries transposed the payment-fraud rules late but largely correctly, with gaps on virtual currencies.",
     "EU, 2021-2023", "legal compliance only; no impact data", "full text partly read"),
 lit("eba-ecb-2024-payment-fraud", "European Banking Authority & European Central Bank", 2024, "2024 Report on Payment Fraud", "EBA/ECB joint report (1 August 2024)", "https://www.ecb.europa.eu/press/pr/date/2024/html/ecb.pr240801~f21cc4a009.en.html",
     "supervisory statistics", "descriptive (PSD2 fraud reporting data)", "fraud losses", "n/a (not attributable)",
     "Payment fraud in the EEA totalled EUR 4.3bn in 2022 and EUR 2.0bn in H1 2023; card fraud about 0.031% of card payment value, mostly in remote transactions",
     "European regulators' statistics show payment fraud of about EUR 4 billion a year, mostly online, but they do not show whether this Directive made a difference.",
     "EEA, 2022-H1 2023", "descriptive; no link to the Directive", "page summary via search", pdf_url="https://eba.europa.eu/sites/default/files/2024-08/465e3044-4773-4e9d-8ca8-b1cd031295fc/EBA_ECB%202024%20Report%20on%20Payment%20Fraud.pdf"),
]
write("32019L0713", "Non-cash payment fraud Directive", "52017PC0489", "SWD(2017) 298 (executive summary SWD(2017) 299)",
      "thin: only a legal transposition report; fraud statistics exist but no study links them to the Directive; impact evaluation (due May 2026) not found",
      "The Directive updated criminal law on payment card and online payment fraud. The Commission's only review so far checked legal transposition, finding most countries late and some gaps on virtual currencies. Payment fraud in Europe still runs at about EUR 4 billion a year, but no study has assessed whether the Directive helped reduce it.",
      indicators, literature)
