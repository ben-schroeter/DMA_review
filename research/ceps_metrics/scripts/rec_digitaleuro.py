import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No LFS indicators section; the memorandum names monitoring indicators and requires a Commission review three years after application and every three years thereafter"),
 ind("monitoring indicator (memorandum)", "Use of central bank money in digital payments", "Amount of digital euro in circulation; number and value of retail payments in digital euro and share vs other means of payment", "",
     "Not applicable: regulation not adopted (Council position Dec 2025; Parliament mandate 2026; ECB targets issuance around 2029).", "not measured", "COM(2023) 369 memorandum"),
 ind("expected impact (impact assessment)", "Financial stability / bank intermediation", "Holding limits keep deposit substitution manageable", "ECB: a EUR 3,000 holding limit caps supply at max ~EUR 1tn",
     "Ex-ante simulations only: ECB (2025) estimates flight-to-safety outflows of EUR 156bn (EUR 500 limit) to EUR 699bn (EUR 3,000 limit; 8.2% of retail sight deposits); contained in business-as-usual.", "not measured", "SWD(2023) 233; ECB 2025; Adalid et al. 2022"),
 ind("expected impact (impact assessment)", "Costs", "One-off costs for PSPs and merchants", "PSPs up to EUR 3.6-6.8bn; merchants already accepting cards EUR 0.8-14bn",
     "Contested ex-ante: bank-commissioned PwC study puts bank costs at ~EUR 18bn over four years; ECB counters with ~EUR 4-5.8bn (per secondary reports).", "mixed evidence", "SWD(2023) 233; PwC 2025"),
]
literature = [
 lit("ec-2023-digital-euro-ia", "European Commission", 2023, "Impact Assessment accompanying the proposals on the establishment of the digital euro and on digital euro services", "SWD(2023) 233 (executive summary SWD(2023) 234)", EU + "52023SC0233",
     "Commission impact assessment", "ex-ante", "financial stability; payment choice; strategic autonomy; costs", "positive (forecast)",
     "Long-term benefits judged to outweigh costs; holding limits to protect financial stability (citing ECB: EUR 3,000 limit caps supply at max EUR 1tn; JRC bank-by-bank analysis). One-off costs: PSPs up to EUR 6.8bn (or EUR 3.6bn with size-differentiated method); merchants already accepting e-payments EUR 0.8-14bn; recurring costs not estimated",
     "The Commission judged that a digital euro's long-term benefits - payment choice, a public anchor for money and less reliance on foreign card schemes - outweigh set-up costs of several billion euros, provided holding limits protect banks.",
     "euro area, forecast", "forecast; benefits largely qualitative", "executive summary read; full text searched"),
 lit("adalid-et-al-2022-ecb-op293", "Adalid, Álvarez-Blázquez, Assenmacher et al.", 2022, "Central bank digital currency and bank intermediation", "ECB Occasional Paper No 293", "https://www.ecb.europa.eu/pub/pdf/scpops/ecb.op293~652cf2b1aa.en.pdf",
     "central bank research", "simulation (bank-level balance sheets, take-up scenarios)", "bank deposits; liquidity; bank runs", "mixed",
     "Illustrative take-up scenarios from just under EUR 500bn to just over EUR 7tn; effects on bank intermediation vary across banks in normal times and are potentially larger in stress; impact on bank-run dynamics depends on remuneration and usage limits",
     "ECB staff simulations found a digital euro's effect on bank funding would differ a lot between banks and could be bigger in a crisis, which is why holding limits matter.",
     "euro area, 2021 data", "ECB staff simulation; views of authors", "abstract and executive summary read", pdf_url="https://www.ecb.europa.eu/pub/pdf/scpops/ecb.op293~652cf2b1aa.en.pdf", interested_party="ECB is the prospective issuer of the digital euro"),
 lit("ecb-2025-holding-limits-technical", "European Central Bank", 2025, "Technical data on the financial stability impact of the digital euro", "ECB technical annex for co-legislators, 10 October 2025", "https://www.ecb.europa.eu/euro/digital_euro/timeline/profuse/shared/pdf/ecb.deprep251010_technical_annex_financial_stability_impact_digital_euro.en.pdf",
     "central bank analysis", "simulation (supervisory deposit data, business-as-usual and flight-to-safety scenarios)", "bank deposits; liquidity; profitability", "mixed",
     "Business-as-usual: deposit impact contained for all limits up to EUR 3,000; net interest income falls 9-18bp (without digitalisation trend). Flight-to-safety: outflows EUR 156bn (EUR 500 limit) to EUR 699bn (EUR 3,000; 2.2% of bank assets, 8.2% of retail sight deposits); at EUR 3,000, 13 banks (0.3% of assets) reach 100% LCR and 9 (0.1%) could fall below",
     "The ECB estimates that with a EUR 3,000 holding limit, a severe crisis could move up to EUR 699 billion of deposits into digital euros, but only a handful of small banks would run short of liquidity; in normal times the effect is small.",
     "euro area, 2025 data", "illustrative; ECB says not its full methodology", "full text read", pdf_url="https://www.ecb.europa.eu/euro/digital_euro/timeline/profuse/shared/pdf/ecb.deprep251010_technical_annex_financial_stability_impact_digital_euro.en.pdf", interested_party="ECB is the prospective issuer of the digital euro"),
 lit("pwc-2025-digital-euro-cost", "PwC (for EACB, EBF and ESBG)", 2025, "Digital Euro Cost Study", "Study commissioned by European bank associations, June 2025", "https://www.ebf.eu/digital-euro-cost-study/",
     "industry-commissioned study", "survey of 19 euro-area retail banks, extrapolated", "bank implementation costs", "negative",
     "Change costs of over EUR 2bn for 19 surveyed banks; extrapolated EUR 18-30bn across the euro area over the first four years (average ~EUR 110m per bank); ECB later put initial investment at roughly EUR 4-5.8bn",
     "A study paid for by bank associations estimated the digital euro would cost euro-area banks about EUR 18 billion or more to introduce, far above the ECB's own estimate.",
     "euro area, 2025", "industry survey extrapolation", "page summary via search", interested_party="Commissioned by bank associations (EACB, EBF, ESBG) opposed to current design"),
]
write("52023PC0369", "Digital Euro Regulation", "52023PC0369", "SWD(2023) 233 (executive summary SWD(2023) 234)",
      "ex-ante only: Commission IA and ECB simulations, contested industry cost study; regulation not adopted",
      "The Commission judged that a digital euro's benefits outweigh set-up costs of several billion euros if holding limits protect banks. ECB simulations suggest a EUR 3,000 limit would leave bank funding largely unaffected in normal times, though a severe crisis could shift up to EUR 699 billion of deposits; a bank-funded study puts banks' costs at EUR 18 billion or more, well above ECB estimates. The law is still being negotiated, so there is no evidence of actual effects.",
      indicators, literature)
