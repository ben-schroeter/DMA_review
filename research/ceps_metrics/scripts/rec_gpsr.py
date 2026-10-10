import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement lists no concrete indicators; it refers to the impact assessment's section 9 and to enforcement indicators still to be defined by a study"),
 ind("expected impact (impact assessment)", "Consumer protection", "Consumer detriment from unsafe products (EUR 19.3bn/yr) cut by about EUR 1.0bn in year one and EUR 5.5bn over a decade; recall-related detriment cut by over EUR 400m/yr", "Baseline EUR 19.3bn/yr",
     "Not evaluated (GPSR applies only since 13 Dec 2024; evaluation due 5 years after application).", "not measured", "SWD(2021) 168/169"),
 ind("expected impact (impact assessment)", "Consumer protection", "Fewer product-related injuries (baseline detriment EUR 11.5bn/yr; health-care cost EUR 6.7bn/yr)", "",
     "No EU injury data series to track it; the IA itself could not quantify this for lack of injury data.", "not measured", "SWD(2021) 169"),
 ind("expected impact (impact assessment)", "Business costs", "Business costs EUR 196.6m in year one, EUR 177.8m/yr after; savings of EUR 59m/yr from less fragmentation", "",
     "No ex-post cost measurement found.", "not measured", "SWD(2021) 169"),
 ind("LFS objective (1.4.2)", "Enforcement and information exchange", "Safety Gate alerts and follow-up actions; online marketplace registration", "",
     "2025: record 4,671 Safety Gate alerts (+13%), 5,794 follow-up actions (+35%); over 1,200 online marketplaces registered. Activity rise, not proof of safer markets. Consumer-group tests in 2025 still found about two-thirds of Temu and 73% of Shein products non-compliant.", "reported as activity", "Commission Safety Gate report 2025; Euroconsumers 2025"),
]
literature = [
 lit("ec-2021-gpsr-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Regulation on general product safety (executive summary SWD(2021) 169)", "SWD(2021) 168", EU + "52021SC0169",
     "Commission impact assessment", "ex-ante", "consumer detriment; business costs; enforcement costs", "positive (forecast)",
     "Consumer detriment from unsafe products EUR 19.3bn/yr expected to fall by ~EUR 1.0bn in year one and ~EUR 5.5bn over a decade; recall detriment down >EUR 400m/yr; business costs EUR 196.6m in year one (0.02% of turnover), EUR 177.8m/yr recurrent; fragmentation savings EUR 59m/yr",
     "The Commission expected the new rules to cut the harm from unsafe products by about EUR 5.5 billion over ten years, at a cost to business of under EUR 200 million a year.",
     "EU, forecast", "forecast", "full text read"),
 lit("ec-2026-safety-gate-2025", "European Commission", 2026, "Increased action against dangerous products in the EU in 2025 (Safety Gate annual report 2025)", "Commission news, 9 March 2026", "https://commission.europa.eu/news-and-media/news/increased-action-against-dangerous-products-eu-2025-2026-03-09_en",
     "Commission monitoring report", "administrative statistics", "enforcement activity", "positive (activity)",
     "Record 4,671 alerts in 2025 (+13%); follow-up actions +35%; cosmetics and toys over half of cases; more than 1,200 online marketplaces registered in the Safety Gate Portal under the GPSR",
     "Alerts about dangerous products hit a record in 2025 and more than 1,200 online marketplaces registered with the EU's safety system, as the new rules require.",
     "EU/EEA, 2025", "activity counts; no outcome measure", "full text read"),
 lit("euroconsumers-2025-temu-shein", "Euroconsumers / Testachats-Testaankoop", 2025, "Systemic failures in product compliance on TEMU and Shein", "Euroconsumers", "https://euroconsumers.org/systemic-failures-in-product-compliance-on-temu-and-shein",
     "consumer organisation report", "mystery shopping and accredited lab tests (81 products per platform)", "product compliance on online marketplaces", "negative",
     "Almost two-thirds of Temu products and 73% of Shein products failed at least one requirement; 26/27 Temu and 27/27 Shein children's products non-compliant; serious electrical risks in chargers",
     "Lab tests of 162 products bought on Temu and Shein in 2025 found most failed EU safety or labelling rules, showing unsafe imports still reach consumers.",
     "Belgium/EU, 2025", "small sample; not causal; date from search summary", "full text read", interested_party="Consumer organisation (advocacy for stronger enforcement)"),
]
write("32023R0988", "General Product Safety Regulation", "52021PC0346", "SWD(2021) 168 (executive summary SWD(2021) 169)",
      "thin: forecasts plus enforcement activity counts and consumer-group tests; no evaluation of effects on injuries or consumer detriment",
      "The General Product Safety Regulation, applied since December 2024, updated EU rules on unsafe consumer goods, especially those sold online. The Commission forecast it would cut harm from unsafe products by about EUR 5.5 billion over ten years. So far there are only activity figures - a record 4,671 safety alerts in 2025 and over 1,200 marketplaces registered - while consumer-group tests still find most products bought on Temu and Shein non-compliant; no study measures effects on injuries or costs.",
      indicators, literature)
