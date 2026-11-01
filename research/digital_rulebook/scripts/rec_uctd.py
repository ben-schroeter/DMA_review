import sys, json; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
ucpd = {l["id"]: l for l in json.load(open("../data/impact/32005L0029.json"))["literature"]}
def reuse(i, **kw):
    d = {k: v for k, v in ucpd[i].items() if k not in ("accessed", "archive_url")}; d.update(kw); return d
indicators = [
 ind("note", "The 1990 proposal has no indicators section; Article 9 required a Commission report five years after transposition"),
 ind("objective (recitals)", "Consumer protection", "Unfair standard terms not binding on consumers; plain, intelligible drafting", "",
     "2000 report: injunction actions in mobile, cable/satellite TV, car rental and timeshare mostly led traders to change terms, but traders rarely gave consumers terms in advance. 2017 fitness check: largely fit for purpose. 2024 fitness check: limited effectiveness online; legal analysis finds many big online service terms likely unfair.", "reported as activity", "COM(2000) 248; SWD(2017) 209; SWD(2024) 230; Loos & Luzak 2016"),
 ind("objective (recitals)", "Single market", "Common minimum rules to encourage cross-border purchases", "", "No measurement of cross-border effects attributable to the Directive found.", "not measured", ""),
 ind("cost (evaluation)", "Compliance costs", "Proportionate costs for traders", "", "2024 fitness check: combined compliance costs of UCPD, CRD and UCTD about EUR 511-737m a year; only 10-18% of traders report high costs.", "measured", "SWD(2024) 230"),
]
literature = [
 lit("ec-2000-uctd-report", "European Commission", 2000, "Report on the implementation of Council Directive 93/13/EEC on unfair terms in consumer contracts", "COM(2000) 248", EU + "52000DC0248",
     "Commission evaluation (implementation report)", "review (national reports, CLAB case-law database, 1999 conference)", "transposition; enforcement; contract practice", "mixed",
     "Injunction actions in new-technology sectors (mobile, cable and satellite TV), car rental, timeshare and holidays mostly led traders to change terms; but traders rarely give consumers the terms before contracting; sanctions and national control systems vary widely",
     "The first review found collective court actions got many companies to drop unfair terms, but consumers still seldom saw contract terms before signing.",
     "EU-15, 1995-1999", "self-evaluation; descriptive", "full text read"),
 reuse("ec-2017-consumer-fitness-check", headline="Consumer rules including the UCTD still largely fit for purpose if effectively enforced; compliance costs proportionate; low awareness and uneven enforcement; led to 2019 Omnibus adding fines for UCTD breaches",
       summary_plain="The 2017 review concluded EU consumer rules, including the unfair terms directive, were largely fit for purpose but poorly known and unevenly enforced."),
 reuse("ec-2024-digital-fairness-fitness-check"),
 lit("loos-luzak-2016-bigger-stick", "Loos & Luzak", 2016, "Wanted: a Bigger Stick. On Unfair Terms in Consumer Contracts with Online Service Providers", "Journal of Consumer Policy 39(1)", "https://doi.org/10.1007/s10603-015-9303-7",
     "peer-reviewed", "legal analysis of standard terms of major online service providers against CJEU case law", "contract terms; enforcement", "negative",
     "Several common terms of international online service providers (unilateral changes of terms or service, unilateral termination, liability exclusions, jurisdiction and choice-of-law clauses) are unlikely to pass the UCTD unfairness test; stronger sanctions needed",
     "A legal study of the terms used by big online services found many likely breach the unfair terms rules, suggesting the Directive is weakly enforced online.",
     "EU, c. 2015", "legal-doctrinal, not quantitative", "abstract read"),
]
write("31993L0013", "Unfair Contract Terms Directive", "51990PC0322", "none (pre-dates impact assessments)",
      "thin: Commission implementation reports and fitness checks plus legal studies; no causal studies of economic effects",
      "The 1993 directive makes unfair standard contract terms non-binding on consumers. Commission reviews found it largely fit for purpose and cheap to comply with, and court actions have forced companies to change terms, but legal studies and the 2024 review show many online terms still look unfair and enforcement is weak. No study measures its effect on prices, trade or consumer losses.",
      indicators, literature)
