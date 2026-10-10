import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2013 proposal (COM(2013) 449) has no financial-statement indicators; Article 12 required a Commission report on effects on the internal market and uptake"),
 ind("expected impact (impact assessment)", "Savings in public procurement", "Annual savings if all public procurement invoices were electronic", "EUR 1.5-2.3bn a year (potential, full uptake)",
     "2024 evaluation does not quantify EU-wide savings; 17 of 23 surveyed Member States say benefits outweigh costs.", "not measured", "SWD(2013) 222; SWD(2024) 39/40"),
 ind("expected impact (impact assessment)", "Interoperability", "Adoption of a European e-invoicing standard and its acceptance by public authorities", "",
     "European standard (EN 16931) published 2017; accepted at central level in all Member States except Cyprus and Slovakia, but only partly at sub-central level; transmission-level interoperability still lacking.",
     "partially measured", "SWD(2024) 39/40"),
 ind("expected impact (impact assessment)", "Uptake", "Uptake of e-invoicing in public procurement (B2G)", "",
     "High uptake only where governments mandate e-invoices or are digitally mature (e.g. Estonia, Finland, Sweden); no EU-wide uptake rate in executive summary.",
     "partially measured", "SWD(2024) 39/40"),
]
literature = [
 lit("ec-2013-einvoicing-ia", "European Commission", 2013, "Impact Assessment accompanying the proposal for a Directive on electronic invoicing in public procurement", "SWD(2013) 222 (executive summary SWD(2013) 223)", EU + "52013SC0222",
     "Commission impact assessment", "ex-ante", "procurement costs; administrative burden; environment", "positive (forecast)",
     "Savings of about EUR 1.5-2.3bn a year potentially achievable if all public procurement invoices were electronic; actual impact of the initiative explicitly said to possibly differ",
     "The Commission estimated that switching all public procurement invoices to electronic form could save EUR 1.5-2.3 billion a year.",
     "EU, forecast", "forecast; extrapolated from national estimates", "full text read (relevant sections)"),
 lit("ec-2024-einvoicing-evaluation", "European Commission", 2024, "Evaluation of Directive 2014/55/EU on electronic invoicing in public procurement (executive summary)", "SWD(2024) 40 (full evaluation SWD(2024) 39)", EU + "52024SC0040",
     "Commission evaluation", "ex-post evaluation (Member State survey, stakeholder consultation)", "interoperability; uptake; costs", "positive but incomplete",
     "European standard established and widely accepted by central governments; adoption high only where mandated; 17 of 23 Member States report benefits exceed costs; transmission-level interoperability and divergent national implementations remain problems",
     "The evaluation found the directive created a common e-invoice standard used across Europe, but uptake is high only where governments make e-invoices compulsory.",
     "EU, 2014-2023", "Commission self-assessment; savings not quantified", "full text read (executive summary)"),
]
write("32014L0055", "E-invoicing Directive", "52013PC0449", "SWD(2013) 222 (executive summary SWD(2013) 223)",
      "thin: Commission evaluation confirms standard and partial uptake; forecast savings never measured; no independent studies of this Directive found",
      "The Commission forecast that full e-invoicing in public procurement could save EUR 1.5-2.3 billion a year. Its 2024 evaluation found the directive did create a common European e-invoice standard accepted by almost all central governments, but uptake is high only where it is mandatory and the promised savings were never measured. No independent study of the directive's effects was found.",
      indicators, literature)
