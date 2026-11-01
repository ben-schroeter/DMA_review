import sys, json; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
ucpd = {l["id"]: l for l in json.load(open("../data/impact/32005L0029.json"))["literature"]}
def reuse(i, **kw):
    d = {k: v for k, v in ucpd[i].items() if k not in ("accessed", "archive_url")}; d.update(kw); return d
indicators = [
 ind("note", "The 1995 proposal has no indicators section; the Directive required a Commission report on its application, particularly by small retailers"),
 ind("objective (recitals)", "Price transparency", "Selling price and unit price shown for all products to ease comparison", "",
     "2006 communication: transposed in all Member States without major problems, but exemptions diverge widely. 2017 fitness check: rules largely fit for purpose.", "reported as activity", "COM(2006) 325; SWD(2017) 209"),
 ind("objective (2019 amendment, Art. 6a)", "Genuine price reductions", "Announced reductions must show the lowest price of the previous 30 days", "",
     "Nov 2022 CPC sweep: 23% of 16,000 price-reduction announcements on 176 websites breached Art. 6a, on at least 43% of sites; Swedish 2023 check: 70% of firms with reductions infringed.", "partially measured", "COM(2024) 258"),
]
literature = [
 lit("ec-2006-pid-communication", "European Commission", 2006, "Communication on the implementation of Directive 98/6/EC on consumer protection in the indication of prices", "COM(2006) 325", EU + "52006DC0325",
     "Commission evaluation (implementation report)", "review (transposition check, study of EU-15 small retailers)", "transposition; exemptions", "neutral",
     "All Member States transposed without major problems; national exemptions from unit pricing (small shops, product lists, quantity thresholds from 5g to 100g) diverge widely; consultation launched on simplification",
     "The 2006 review found every country had adopted the price-display rules, but with very different exemptions.",
     "EU, to 2005", "self-evaluation; descriptive", "full text partly read"),
 reuse("ec-2017-consumer-fitness-check", headline="Consumer and marketing rules, including the Price Indication Directive, still largely fit for purpose if effectively enforced; compliance costs proportionate; led to the 2019 Omnibus, which added the 30-day prior-price rule for price reductions",
       summary_plain="The 2017 review found EU consumer rules, including price-display rules, largely fit for purpose but unevenly enforced; it led to a new rule on genuine price reductions."),
 reuse("ec-2024-omnibus-report", headline="Article 6a (30-day prior price) transposed everywhere but with divergent exemptions; Nov 2022 CPC sweep of 16,000 products on 176 websites found 23% of price-reduction announcements breached it, on at least 43% of sites; Swedish 2023 check found 70% of firms with reductions infringed; use of comparisons with recommended retail prices increased",
       summary_plain="The new rule that discounts must be measured against the lowest price of the past 30 days was widely breached in early checks: about a quarter of discounts in an EU-wide sweep did not comply.",
       outcomes="price-reduction compliance; transposition", direction="mixed (early)"),
]
write("31998L0006", "Price Indication Directive", "51995PC0276", "none (pre-dates impact assessments)",
      "thin: Commission implementation reports and enforcement sweeps; no independent studies of effects on prices or competition found",
      "The 1998 directive requires shops to show both the price and the price per kilo or litre. Commission reviews found it in place everywhere and largely fit for purpose, but with differing national exemptions. A 2022 rule requiring discounts to be measured against the lowest price of the previous 30 days was breached in about a quarter of discounts checked in an EU-wide sweep; no study measures effects on prices or competition.",
      indicators, literature)
