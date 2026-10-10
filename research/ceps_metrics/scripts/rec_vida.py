import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The ViDA proposal (a Council directive) has no LFS indicators section; the memorandum refers to the monitoring indicators in Section 4 of the impact assessment and an evaluation 5 years after entry into force"),
 ind("expected impact (impact assessment)", "Improve VAT collection and control", "Additional VAT revenue 2023-2032 (enhanced option)", "EUR 135-177bn over 10 years (about 0.1% of GDP a year)",
     "Not measurable yet: EU-level digital reporting and e-invoicing for intra-EU trade only applies from 1 July 2030 and the package phases in to 2035. Baseline: the EU VAT compliance gap was EUR 128bn in 2023 (Commission VAT Gap report 2025).", "not measured", "SWD(2022) 394; Commission VAT Gap report 2025"),
 ind("expected impact (impact assessment)", "Reduce compliance burden", "Business savings 2023-2032 (enhanced option)", "EUR 50.6bn savings (41.4bn reporting, 0.5bn platform economy, 8.7bn registration) against EUR 11.3bn new DRR costs",
     "Not measured. Commission still cites 'EUR 51 billion in savings for businesses' in its Sept 2025 implementation strategy.", "not measured", "SWD(2022) 394; DG TAXUD Sept 2025"),
 ind("expected impact (impact assessment)", "Minimise multiple VAT registrations", "SMEs benefiting from extended OSS/IOSS", "280,000 SMEs; up to EUR 7bn saved 2023-2032",
     "Not measured; single VAT registration measures apply from 2027-2028.", "not measured", "SWD(2022) 394"),
 ind("expected impact (impact assessment)", "Overall net impact", "Net impact against baseline 2023-2032", "EUR 172-214bn (enhanced option)",
     "Forecast only; the adopted text differs from the assessed option (some measures softened or delayed), so the figure is an upper reference rather than a forecast for the final law.", "not measured", "SWD(2022) 394"),
]
literature = [
 lit("ec-2022-vida-ia", "European Commission", 2022, "Impact assessment on VAT in the digital age (executive summary SWD(2022) 394)", "SWD(2022) 393", EU + "52022SC0394",
     "Commission impact assessment", "ex-ante", "VAT revenue; compliance costs; administrative burden", "positive (forecast)",
     "Enhanced option: EUR 172-214bn net impact 2023-2032; EUR 135-177bn extra VAT revenue; EUR 50.6bn business savings vs EUR 11.3bn new reporting costs; EUR 2.2bn implementation costs for tax administrations; 280,000 SMEs save up to EUR 7bn",
     "The Commission expected the package to bring in EUR 135-177 billion of extra VAT and save businesses about EUR 51 billion over ten years, with new digital reporting costing firms about EUR 11 billion.",
     "EU-27, 2023-2032 forecast", "forecast", "full text read"),
 lit("case-2022-vida-study", "Economisti Associati, Oxford Research, CASE, Wavestone et al.", 2022, "VAT in the digital age: final report (Vol. 1 Digital Reporting Requirements)", "Study for DG TAXUD, Publications Office of the EU", "https://case-research.eu/en/vat-in-the-digital-age-102154",
     "Commission-contracted study", "ex-ante / comparative review of national DRRs", "VAT revenue; compliance costs", "positive (forecast)",
     "12 Member States had digital reporting requirements by Sept 2021; these showed positive net impacts as extra VAT revenue exceeded set-up and compliance costs; fragmentation of national systems identified as core problem",
     "The study behind the impact assessment found that national digital VAT reporting schemes raised more revenue than they cost, but that their patchwork burdens cross-border firms.",
     "EU-27, to 2021", "contracted study; underpins IA", "page summary via search", interested_party="Commissioned by DG TAXUD"),
 lit("ec-2025-vat-gap", "European Commission (DG TAXUD)", 2025, "VAT Gap in the EU - 2025 report", "Commission report and data hub", "https://taxation-customs.ec.europa.eu/taxation/vat/fight-against-vat-fraud/vat-gap_en",
     "Commission statistics", "descriptive (top-down gap estimate)", "VAT compliance gap (baseline)", "n/a",
     "VAT compliance gap EUR 128bn in 2023 (+1.6 pp on 2022); actionable policy gap EUR 742bn",
     "Before ViDA takes effect, about EUR 128 billion of VAT due in 2023 went uncollected; this is the baseline ViDA aims to cut.",
     "EU-27, 2023", "official baseline", "full text read"),
 lit("ec-2025-vida-implementation", "European Commission (DG TAXUD)", 2025, "VAT in the Digital Age: implementation strategy to support businesses and Member States", "News item, 24 September 2025", "https://taxation-customs.ec.europa.eu/news/vat-digital-age-implementation-strategy-support-businesses-and-member-states-2025-09-24_en",
     "Commission implementation document", "roadmap", "implementation", "positive (forecast)",
     "Restates expected benefits of EUR 172-214bn over a decade including EUR 51bn savings for businesses; sets roadmap of action points to 2035",
     "The Commission's implementation plan restates the impact-assessment forecasts and sets out steps to 2035; no results yet.",
     "EU", "official claim", "full text read"),
]
write("32025L0516", "VAT in the Digital Age (ViDA)", "52022PC0701", "SWD(2022) 393 (executive summary SWD(2022) 394)",
      "ex-ante only: Commission IA and contracted study forecasts; key measures apply 2027-2035 so no outcome evidence yet",
      "The Commission forecast that ViDA would raise EUR 135-177 billion in extra VAT and save businesses about EUR 51 billion over ten years, mainly through EU-wide e-invoicing and digital reporting. These are forecasts for the option assessed in 2022; the main reporting rules only start in 2030, so nothing can be measured yet. The starting point is a VAT compliance gap of EUR 128 billion in 2023.",
      indicators, literature)
