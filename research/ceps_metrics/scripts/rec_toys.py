import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal has no LFS indicators section; the Commission will evaluate the Regulation five years after entry into force and every five years thereafter. The Regulation entered into force in January 2026 and fully applies from 1 August 2030."),
 ind("expected impact (impact assessment)", "Protect children from harmful chemicals", "Avoided health damage from banning endocrine disruptors in toys", "EUR 240m-1.2bn per year",
     "Not measured; chemical bans apply from 2030.", "not measured", "SWD(2023) 270"),
 ind("expected impact (impact assessment)", "Fewer unsafe and non-compliant toys on the market (digital product passport, enforcement)", "Non-compliant/unsafe toys; market surveillance efficiency", "Industry savings EUR 13-20m/yr on inspections and EUR 2.6-3.9m/yr from digital information; costs EUR 18m one-off + EUR 10.5m/yr for the passport",
     "Baseline only. Toys were 15% of the record 4,137 Safety Gate alerts in 2024 (second after cosmetics). Industry test purchases found 80% of 100+ toys from third-party sellers on 10 marketplaces failed EU rules (2024).", "not measured", "Safety Gate 2024; TIE 2024"),
 ind("expected impact (impact assessment)", "Compliance costs", "One-off redesign costs; products withdrawn", "EUR 23.5-397m one-off; EUR 249-367m of products affected (of EUR 6.56bn industry turnover)",
     "Not measured.", "not measured", "SWD(2023) 270"),
]
literature = [
 lit("ec-2023-toys-ia", "European Commission", 2023, "Impact assessment accompanying the proposal for a Regulation on the safety of toys (executive summary SWD(2023) 270)", "SWD(2023) 269", EU + "52023SC0270",
     "Commission impact assessment", "ex-ante", "child health; compliance costs; market surveillance", "positive (forecast)",
     "Health benefits EUR 240m-1.2bn/yr from endocrine-disruptor ban alone; one-off redesign costs EUR 23.5-397m; EUR 249-367m worth of products affected; product passport EUR 18m one-off + EUR 10.5m/yr, offset by EUR 13-20m/yr inspection savings and EUR 2.6-3.9m/yr digital information savings",
     "The Commission expected the new chemical bans to avoid EUR 240 million to 1.2 billion a year in health damage, at one-off costs to industry of up to about EUR 400 million.",
     "EU-27, forecast", "forecast", "full text read"),
 lit("ec-2025-safety-gate-2024", "European Commission", 2025, "Safety Gate: 2024 results", "Commission annual report (as summarised by UL and SGS)", "https://www.ul.com/news/consumer-products-eu-commission-publishes-2024-safety-gate-report",
     "Commission statistics (secondary report)", "descriptive", "dangerous product alerts (baseline)", "n/a",
     "Record 4,137 alerts in 2024; toys 15% of alerts, second after cosmetics (36%); chemical risks 49% of all alerts",
     "Toys made up 15% of the EU's record 4,137 alerts on dangerous products in 2024, a baseline the new rules aim to reduce.",
     "EU, 2024", "official statistics, secondary summary", "page summary via search"),
 lit("tie-2024-marketplace-toys", "Toy Industries of Europe", 2024, "80% of toys bought from third-party traders on online marketplaces fail EU safety standards", "TIE press release (October 2024)", "https://toyindustries.eu/80-of-toys-bought-from-third-party-traders-on-online-marketplaces-fail-eu-safety-standards-and-could-be-a-danger-to-children",
     "industry study", "test purchases (100+ toys, 10 marketplaces)", "non-compliance of toys sold online (baseline)", "n/a",
     "80% of toys bought from third-party traders on 10 online marketplaces failed EU safety standards; no well-known brands tested; 2025 follow-up reported 86% of 70 toys posed direct safety risks",
     "An industry test of more than 100 toys bought from third-party sellers online found 80% broke EU safety rules, the problem the passport and marketplace duties are meant to address.",
     "EU marketplaces, 2024", "small non-random sample", "page summary via search", interested_party="EU toy manufacturers' association; competes with non-EU online sellers"),
]
write("32025R2509", "Toys Safety Regulation", "52023PC0462", "SWD(2023) 269 (executive summary SWD(2023) 270)",
      "ex-ante only: Commission IA forecasts plus baseline data on unsafe toys; rules apply from 2030",
      "The Commission expected the new toy rules to avoid EUR 240 million to 1.2 billion a year in health damage by banning harmful chemicals, and to cut unsafe imports through a digital product passport. The rules only fully apply from August 2030, so no effects can be measured yet. As a baseline, toys made up 15% of EU dangerous-product alerts in 2024, and industry tests found most toys from third-party online sellers broke EU rules.",
      indicators, literature)
