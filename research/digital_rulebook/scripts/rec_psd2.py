import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("specific objective", "Develop an EU-wide market for electronic payments"),
 ind("specific objective", "Address standardisation and interoperability gaps for card, internet and mobile payments"),
 ind("specific objective", "Eliminate hurdles for competition, in particular for card and internet payments"),
 ind("specific objective", "Align charging and steering practices across the EU"),
 ind("specific objective", "Cover emerging payment services and instruments"),
 ind("specific objective", "Ensure consistent application of licensing and supervision across Member States"),
 ind("specific objective", "Ensure adequate and consistent consumer protection"),
 ind("indicator (LFS 1.4.4)", "All objectives", "Commission assessment of implementation and impact, based on a conformity check and a market study (no quantified indicators set)", "",
     "Done: Commission review COM(2023) 365 and evaluation (with SWD(2023) 231). Finds 'varying degrees of success'.", "measured (qualitative review)", "COM(2023) 365"),
 ind("expected impact (LFS 1.4.3)", "Security", "Secure payment services (strong customer authentication)", "", "Clear success: SCA-authenticated remote card payments show 70-80% lower fraud than non-SCA ones.", "measured", "COM(2023) 365"),
 ind("expected impact (LFS 1.4.3)", "Competition and innovation", "Facilitate innovative payment services (open banking, new entrants)", "",
     "Mixed: hundreds of new non-bank providers with millions of clients, but open-banking uptake uneven and data-access interfaces of variable quality; banks report high API costs. Cross-country evidence: open-banking policies spur fintech investment (Babina et al.).", "mixed evidence", "COM(2023) 365; Babina et al. 2024"),
 ind("expected impact (LFS 1.4.3)", "Prices", "Downward convergence of costs and prices for payment users", "",
     "Not achieved yet: anticipated cost reductions for merchants from cheaper payment methods 'have not yet fully materialised'; card systems remain largely national; no pan-European solution yet.", "not achieved (per Commission)", "COM(2023) 365"),
 ind("expected impact (LFS 1.4.3)", "Charging practices", "Align surcharging and steering practices", "", "Surcharging ban covers 95% of EU payments; Commission sees no need for further alignment.", "measured", "COM(2023) 365"),
]
literature = [
 lit("ec-2013-psd2-ia", "European Commission", 2013, "Impact Assessment accompanying the proposals for PSD2 and the Interchange Fee Regulation (summary SWD(2013) 289)", "SWD(2013) 288", EU + "52013SC0289",
     "Commission impact assessment", "ex-ante", "costs and prices; standardisation", "positive (forecast)",
     "Package-level estimates: card standardisation benefits ~EUR 4bn/yr; interchange-fee caps EUR 3-6bn/yr operational savings for merchants (these relate mainly to the Interchange Fee Regulation, not PSD2)", "The Commission expected the payments package to save merchants and consumers billions a year, mostly through caps on card fees set in a separate regulation.",
     "EU, forecast", "forecast; most quantified benefits belong to the companion Interchange Fee Regulation", "full text partly read"),
 lit("ec-2023-psd2-review", "European Commission", 2023, "Report on the review of Directive (EU) 2015/2366 (PSD2)", "COM(2023) 365, with evaluation in SWD(2023) 231", EU + "52023DC0365",
     "Commission evaluation", "evaluation (market data, consultation)", "fraud; competition; open banking; prices", "mixed",
     "SCA highly successful against fraud (70-80% lower fraud on SCA remote card payments); new non-bank entrants and open-banking growth but uneven uptake and poor API performance; merchant cost reductions not yet materialised; card systems still national", "PSD2 sharply reduced card fraud and let many new payment firms enter, but open banking has taken off unevenly and promised savings for merchants have not yet appeared.",
     "EU, 2018-2022", "self-evaluation", "full text partly read"),
 lit("babina-et-al-2024", "Babina, Bahaj, Buchak, De Marco, Foulis, Gornall, Mazzola & Yu", 2024, "Customer Data Access and Fintech Entry: Early Evidence from Open Banking", "NBER Working Paper 32089 (also Bank of England staff working paper)", "https://www.nber.org/papers/w32089",
     "working paper", "causal: cross-country staggered adoption (49 countries) + UK microdata + calibrated model", "innovation (fintech investment); credit access; welfare", "positive (with distributional costs)",
     "Open-banking adoption spurs investment in fintechs; in the UK it gives consumers access to advice and credit and SMEs new fintech lending relationships; welfare gains from advice, mixed for credit (higher prices for costlier or privacy-conscious consumers)", "Across 49 countries, open-banking rules like those in PSD2 attracted more investment into fintech start-ups and widened access to credit, though some consumers end up paying more.",
     "49 countries; UK microdata", "not EU-specific; PSD2 is one of the policies studied", "abstract read", pdf_url="https://www.nber.org/system/files/working_papers/w32089/w32089.pdf"),
 lit("multisafepay-sca-conversion", "MultiSafepay", 2021, "How PSD2 & Strong Customer Authentication affect your payment success rates", "Industry blog (payment service provider)", "https://www.multisafepay.com/blog/how-psd2-strong-customer-authentication-affect-your-payment-success-rates",
     "industry", "descriptive (own transaction data)", "firm performance (online conversion)", "negative (friction)",
     "Average conversion for 3DS-authenticated card payments about 82%; gap vs non-authenticated flows about 7% in NL and about 13% in IT and ES", "Payment-industry data suggest the extra authentication step costs online shops some sales, with bigger losses in southern Europe.",
     "European markets", "vendor data; not independent; no counterfactual", "page summary via search", interested_party="Payment service provider"),
]
write("32015L2366", "Payment Services Directive 2 (PSD2)", "52013PC0547", "SWD(2013) 288 (summary SWD(2013) 289)",
      "moderate: Commission evaluation with market data; cross-country causal evidence on open banking; little independent evidence on prices or SCA trade-offs",
      "PSD2's strong customer authentication cut card fraud sharply (70-80% lower on authenticated remote payments) and open-banking rules helped new payment firms enter; cross-country research links open banking to more fintech investment. But open-banking uptake is uneven, banks report high API costs, card markets stay national and the promised fall in payment costs for merchants has not materialised. Industry data point to some lost online sales from authentication friction.",
      indicators, literature)
