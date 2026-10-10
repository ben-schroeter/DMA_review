import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator", "Product sustainability", "Number of product groups covered by delegated acts", "",
     "First ESPR working plan (April 2025) prioritises steel, aluminium, textiles, furniture, tyres and others, with indicative adoption 2026-2028; ban on destroying unsold apparel and footwear applies to large firms from 19 July 2026. No product-specific ESPR requirements yet in force.", "reported as activity", "Commission working plan 2025-2030 (secondary reports)"),
 ind("LFS indicator", "Product sustainability", "Change in GHG and pollutant emissions; energy, water and material efficiency of regulated products", "",
     "Not measured; depends on future delegated acts.", "not measured", ""),
 ind("LFS indicator", "Circularity", "Product lifetime; recycled content; circular material use rate", "",
     "Eurostat publishes the circular material use rate, but no attribution to ESPR.", "not measured", ""),
 ind("LFS indicator", "Sustainable business models", "Value added, investment and jobs in recycling, repair and re-use; green public procurement share; consumer cost impacts", "",
     "Not tracked against ESPR.", "not measured", ""),
 ind("expected impact (Commission)", "Energy savings", "Primary energy savings by 2030 (ecodesign scope)", "132 Mtoe, ~150 bcm gas (reported)",
     "Not evaluated; evaluation due eight years after application.", "not measured", "Commission 2022 announcement as reported by INFORSE-Europe"),
]
literature = [
 lit("ec-2022-espr-ia", "European Commission", 2022, "Impact Assessment accompanying the proposal for an Ecodesign for Sustainable Products Regulation (executive summary SWD(2022) 83)", "SWD(2022) 82", EU + "52022SC0083",
     "Commission impact assessment", "ex-ante", "environment; consumer costs; business costs", "positive (forecast, qualitative)",
     "Framework design means costs and benefits cannot be identified precisely; expects significant GHG reductions and market greening, some costs passed to consumers but offset by long-run savings; each delegated act to have its own IA (RSB first gave a negative opinion)",
     "The Commission expected greener, longer-lasting products and lower emissions, but said overall costs and benefits could only be estimated when rules for each product are set.",
     "EU, forecast", "forecast; largely unquantified", "full text read", pdf_url="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52022SC0083"),
 lit("inforse-2022-espr", "INFORSE-Europe", 2022, "EU Ecodesign for Sustainable Products proposal (summary page)", "INFORSE-Europe", "https://inforse.org/europe/eu_ecodesign_sust_products.htm",
     "NGO summary of Commission figures", "secondary report", "energy savings", "positive (forecast)",
     "Reports Commission estimate that the framework could deliver 132 Mtoe primary energy savings by 2030, about 150 bcm of gas, nearly equal to EU imports of Russian gas",
     "The Commission said the ecodesign framework could save energy by 2030 roughly equal to the EU's imports of Russian gas.",
     "EU, to 2030", "secondary report of Commission forecast", "page summary via search",
     interested_party="Environmental NGO network advocating energy-efficiency policy"),
]
write("32024R1781", "Ecodesign for Sustainable Products Regulation", "52022PC0142", "SWD(2022) 82 (executive summary SWD(2022) 83)",
      "ex-ante only: framework law, product rules not yet adopted; forecasts largely unquantified",
      "This framework law lets the EU set durability, repairability, recycled-content and digital-passport rules for almost any product. The Commission said it could save energy by 2030 roughly equal to EU imports of Russian gas, but its impact assessment did not quantify overall costs and benefits. Apart from a ban on destroying unsold clothes (from July 2026), product rules are still being prepared, so there is no evidence of impact yet.",
      indicators, literature)
