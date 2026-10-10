import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2004 proposal was a recast of the Sixth VAT Directive with no indicators; evidence concerns later digital amendments (e-services 2015, e-commerce package 2021, VAT in the Digital Age 2025)"),
 ind("expected impact (2016 IA)", "E-commerce VAT: revenue and compliance", "Extend one-stop shop, abolish EUR 22 import exemption", "Status quo losses EUR 7bn/yr by 2020; preferred option cuts business VAT admin burden 42% (EUR 1.8bn)",
     "OSS/IOSS VAT declared rose from EUR 26.3bn (2023) to EUR 33.1bn (2024), about EUR 88bn in 2021-2024; MOSS for e-services collected about EUR 3bn in 2015 and saved firms ~EUR 500m. Revenue is gross collection through the schemes, not a net causal effect.", "partially measured", "SWD(2016) 379; Commission OSS report 2025"),
 ind("expected impact (2022 IA)", "VAT in the Digital Age", "Digital reporting, platform deemed supplier, single registration", "Net impact EUR 172-214bn 2023-2032; extra VAT EUR 135-177bn; business savings EUR 50.6bn",
     "Adopted 2025; phased in to 2035; not yet measured.", "not measured", "SWD(2022) 393"),
 ind("outcome (independent research)", "Pass-through of VAT to consumer prices", "", "", "Using EU VAT changes 1996-2015, prices respond about twice as much to VAT increases as to decreases.", "measured", "Benzarti et al. 2020"),
]
literature = [
 lit("ec-2016-vat-ecommerce-ia", "European Commission", 2016, "Impact assessment on modernising VAT for cross-border B2C e-commerce", "SWD(2016) 379", EU + "52016SC0379",
     "Commission impact assessment", "ex-ante (external study)", "VAT revenue; compliance costs", "positive (forecast)",
     "MOSS (2015): ~EUR 3bn VAT paid, ~70% of e-service supplies, saved businesses ~EUR 500m; status quo: cross-border compliance costs EUR 4.2bn a year, VAT losses EUR 7bn a year by 2020; preferred option cuts admin burden 42% (EUR 1.8bn)",
     "The Commission expected its e-commerce VAT reform to cut business paperwork by 42% and close a EUR 7 billion a year revenue gap.",
     "EU, forecast", "forecast", "full text partly read"),
 lit("ec-2025-oss-report", "European Commission", 2025, "Report on the application of the VAT e-commerce package for 2024", "VAT One Stop Shop portal, 14 July 2025", "https://vat-one-stop-shop.ec.europa.eu/report-application-vat-e-commerce-package-2024-2025-07-14_en",
     "Commission monitoring report", "administrative data", "VAT collected through OSS/IOSS", "positive",
     "VAT declared via the three OSS schemes rose from EUR 26.3bn in 2023 to EUR 33.1bn in 2024 (+26%); about EUR 88bn declared 2021-2024",
     "VAT collected through the EU's one-stop-shop for online sales reached EUR 33 billion in 2024, up 26% on 2023.",
     "EU, 2021-2024", "gross collections; not a causal estimate", "page summary via search"),
 lit("ec-2022-vida-ia", "European Commission", 2022, "Impact assessment on VAT in the digital age (executive summary SWD(2022) 394)", "SWD(2022) 393", EU + "52022SC0393",
     "Commission impact assessment", "ex-ante", "VAT revenue; compliance costs", "positive (forecast)",
     "Preferred approach: EUR 172-214bn net impact 2023-2032; EUR 50.6bn savings; EUR 135-177bn additional VAT revenue; EUR 11.3bn new reporting costs for business; 280,000 SMEs benefit from extended OSS",
     "The Commission expected digitising VAT to raise EUR 135-177 billion of extra VAT and save firms about EUR 50 billion over ten years.",
     "EU, forecast 2023-2032", "forecast", "full text read (executive summary)"),
 lit("benzarti-et-al-2020-vat", "Benzarti, Carloni, Harju & Kosonen", 2020, "What Goes Up May Not Come Down: Asymmetric Incidence of Value-Added Taxes", "Journal of Political Economy 128(12) (NBER WP 23849)", "https://www.nber.org/papers/w23849",
     "peer-reviewed", "quasi-experimental (two exogenous VAT changes) plus panel of all EU VAT changes 1996-2015", "consumer prices; markups", "mixed",
     "Prices respond twice as much to VAT increases as to decreases; asymmetry raises profits and markups and persists for years; similar asymmetry across all EU VAT changes 1996-2015",
     "Studying VAT changes across the EU, economists found shops pass on VAT rises about twice as fully as VAT cuts.",
     "EU, 1996-2015", "strong causal design; about VAT rates, not the Directive itself", "abstract read"),
]
write("32006L0112", "Common VAT system Directive", "52004PC0246", "none for the 2006 recast; SWD(2016) 379 (e-commerce); SWD(2022) 393 (digital age)",
      "moderate for VAT in general, thin for the Directive's digital rules: Commission forecasts and collection data, one strong causal study on VAT incidence",
      "The VAT Directive sets the EU's common VAT rules, which have been updated for online sales. Since the 2021 e-commerce reform, VAT collected through the EU's one-stop-shop rose to EUR 33 billion in 2024, though this is gross collection rather than a measured net gain. Independent research using EU VAT changes shows price rises from VAT increases are passed on about twice as fully as VAT cuts; the 2025 digital VAT reform is forecast to raise EUR 135-177 billion over ten years.",
      indicators, literature)
