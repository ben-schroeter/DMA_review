import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("monitoring target (memorandum)", "Fewer late payments", "Share of companies reporting late payments as a problem (ECB/Commission SAFE survey)", "Target 28% from 2022 baseline 43% (-35%)",
     "Not applicable: regulation not adopted (Parliament position 2024; blocking minority reported in Council).", "not measured", "COM(2023) 533 memorandum"),
 ind("monitoring target (memorandum)", "Fewer late payments, by firm size", "Same SAFE indicator per size class", "Target 26-31% from baselines 40-47% (-35%)",
     "Not applicable: regulation not adopted.", "not measured", "COM(2023) 533 memorandum"),
 ind("expected impact (impact assessment)", "Cash flow and admin burden", "Payment times cut ~35%; hassle costs of chasing debtors (340.2m hours, EUR 8.74bn) significantly reduced; EUR 27m/yr court savings from mediation", "Costs: EUR 243m one-off (invoices); EUR 70-105m/yr public enforcement and mediation",
     "Forecast only; industry (trade credit insurers) claims a strict 30-day cap creates up to EUR 2tn new financing need.", "not measured", "SWD(2023) 314; ICISA"),
]
literature = [
 lit("ec-2023-late-payment-ia", "European Commission", 2023, "Impact Assessment accompanying the proposal for a Regulation on combating late payment in commercial transactions", "SWD(2023) 314 (executive summary SWD(2023) 313)", EU + "52023SC0314",
     "Commission impact assessment", "ex-ante", "payment times; administrative burden; SME cash flow", "positive (forecast)",
     "Payment times reduced by an estimated 35%; hassle costs of chasing debtors (340.2m hours, EUR 8.74bn) significantly reduced; mediation saves EUR 27m a year in court cases; one-off costs EUR 243m; public enforcement and mediation EUR 70-105m a year; ~41% of SMEs benefit from 30-day cap",
     "The Commission expected a hard 30-day payment limit to shorten payment times by about 35% and save firms much of the EUR 8.7 billion a year they spend chasing late payers, at one-off costs of about EUR 243 million.",
     "EU, forecast", "forecast", "executive summary read"),
 lit("eesc-2024-late-payment-opinion", "European Economic and Social Committee", 2024, "Opinion on the revision of the Late Payments Directive", "EESC opinion INT/1041, adopted 17 January 2024", "https://www.eesc.europa.eu/en/our-work/opinions-information-reports/opinions/revision-late-payments-directive",
     "advisory body opinion", "qualitative", "contractual freedom; business impact", "mixed",
     "Strong concerns that the 30-day cap for business-to-business payments eliminates contractual freedom; welcomes 30 days for public authorities paying businesses; sees potential benefit in national enforcement bodies",
     "The EU's advisory committee of employers, unions and civil society backed a 30-day limit for public bodies but found a strict 30-day cap between businesses too rigid.",
     "EU", "stakeholder opinion", "opinion summary page read"),
 lit("icisa-2024-late-payment", "International Credit Insurance & Surety Association (ICISA)", 2024, "EU Late Payment Regulation: Blocking majority forms in European Council", "ICISA news, 6 June 2024", "https://icisa.org/news/update-on-eu-late-payment-regulation-blocking-majority-forms-in-european-council/",
     "industry position", "industry estimate (method not published)", "trade credit; financing needs", "negative",
     "Claims a strict 30-day term for B2B transactions would create a new financing requirement of up to EUR 2tn; reports a blocking majority forming in Council",
     "Trade credit insurers argue the 30-day cap would force firms to find up to EUR 2 trillion in extra financing; the figure is the industry's own and unverified.",
     "EU", "advocacy; unverified estimate", "page read", interested_party="Trade credit insurers' association whose business depends on payment terms"),
]
write("52023PC0533", "Late Payment Regulation", "52023PC0533", "SWD(2023) 314 (executive summary SWD(2023) 313)",
      "ex-ante only: impact assessment forecasts with clear targets; contested by stakeholders; not adopted",
      "The Commission set a clear target - cutting the share of firms reporting late payment as a problem from 43% to 28% - and expected a strict 30-day payment limit to shorten payment times by about 35%. Business groups and trade credit insurers dispute the costs, and the proposal has stalled in the Council, so none of these promises can yet be tested.",
      indicators, literature)
