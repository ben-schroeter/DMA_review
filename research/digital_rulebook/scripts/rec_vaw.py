import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("specific objective (LFS 1.4.2-1.4.4)", "Comparable administrative data on violence against women", "Common disaggregations and methodology developed by EIGE; data collection tool and guidelines deployed; number of Member States able to report data on all forms of violence covered (availability) and in full compliance (comparability) each year", "",
     "Directive adopted May 2024; transposition deadline June 2027, so no Member State reporting under the Directive yet. Baseline exists from the joint Eurostat-FRA-EIGE EU gender-based violence survey (key results Nov 2024).", "not measured", "Directive 2024/1385; EU-GBV survey 2024"),
 ind("expected impact (impact assessment)", "Reduced prevalence of violence", "Economic benefits of reduced prevalence about EUR 53.1bn, potentially EUR 82.7bn in the long term (mostly lower physical and emotional harm to victims, EUR 32.2-64.5bn)", "EUR 53.1-82.7bn",
     "Not evaluated. Survey baseline: about 1 in 3 women in the EU (30.7%) report physical violence, threats and/or sexual violence in their lifetime.", "not measured", "SWD(2022) 62/63; EIGE 2024"),
 ind("expected cost (impact assessment)", "Compliance costs", "Total compliance costs EUR 5-6.6bn, mostly for Member States; about EUR 1.9bn for employers (manager training on sexual harassment)", "EUR 5-6.6bn",
     "Not measured.", "not measured", "SWD(2022) 63"),
 ind("monitoring (memorandum)", "Implementation reporting", "Member States report to the Commission 7 years after entry into force; regular EU-wide surveys transmitted to Eurostat", "", "Not yet due.", "not measured", "COM(2022) 105"),
]
literature = [
 lit("ec-2022-vaw-ia", "European Commission", 2022, "Impact Assessment accompanying the proposal for a Directive on combating violence against women and domestic violence (executive summary SWD(2022) 63)", "SWD(2022) 62", EU + "52022SC0063",
     "Commission impact assessment", "ex-ante", "prevalence of violence; economic cost of violence; compliance costs", "positive (forecast)",
     "Preferred option 2A: reduced prevalence could bring economic benefits of around EUR 53.1bn, up to EUR 82.7bn in the long term; compliance costs EUR 5-6.6bn, mostly borne by Member States, EUR 1.9bn by employers; no negative impacts noted",
     "The Commission estimated that the law could save around EUR 53 billion (up to EUR 83 billion in the long run) by reducing violence, against EUR 5-6.6 billion in costs, mostly for national authorities.",
     "EU-27, forecast", "forecast", "full text read (executive summary)"),
 lit("eige-fra-eurostat-2024-gbv-survey", "Eurostat, EU Agency for Fundamental Rights (FRA) & European Institute for Gender Equality (EIGE)", 2024, "EU gender-based violence survey - key results (2024 edition)", "Eurostat/FRA/EIGE joint publication, 25 November 2024", "https://eige.europa.eu/newsroom/news/one-three-women-eu-have-experienced-violence",
     "official statistics (survey)", "descriptive (survey of about 114,000 women aged 18-74, fieldwork Sept 2020-Mar 2024)", "prevalence of violence (baseline)", "n/a (baseline)",
     "About 1 in 3 women in the EU (30.7%) have experienced physical violence, threats and/or sexual violence; about 1 in 6 sexual violence including rape; 1 in 5 violence by a partner, relative or household member",
     "The EU's first joint survey since the Directive was proposed found about one in three women have experienced physical or sexual violence or threats - the baseline against which the Directive will be judged.",
     "EU-27, 2020-2024", "baseline only; not an impact study", "page summary via search"),
]
write("32024L1385", "Violence Against Women Directive", "52022PC0105", "SWD(2022) 62 (executive summary SWD(2022) 63)",
      "ex-ante only: Commission forecasts and a fresh survey baseline; transposition not due until 2027",
      "The Commission forecast that the Directive could save the EU economy around EUR 53 billion a year by reducing violence against women, against EUR 5-6.6 billion in compliance costs. Countries have until 2027 to apply it, so there is no evidence yet on its effect; a 2024 EU survey, finding that about one in three women have experienced physical or sexual violence or threats, provides the starting point for future evaluation.",
      indicators, literature)
