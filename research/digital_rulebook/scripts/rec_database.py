import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 1992 proposal (COM(92) 24) predates impact assessments and set no indicators. Article 16(3) required periodic Commission reviews of whether the sui generis right led to abuse of a dominant position or other interference with free competition"),
 ind("objective (proposal / recitals)", "Stimulate investment in and production of databases in Europe", "Growth in EU database production and competitiveness vs the US", "",
     "Measured and negative/flat: the 2005 evaluation found EU-based entries in the Gale Directory of Databases back at pre-Directive levels by 2004 (3,095 vs 3,092 in 1998, after a 4,085 peak in 2001) and the EU/US production ratio worsening from about 1:2 (1996) to 1:3 (2004). The 2018 evaluation again found 'no proven impact on the overall production of databases in Europe, nor on the competitiveness of the EU database industry'.",
     "measured", "DG MARKT 2005; SWD(2018) 146/147"),
 ind("objective (proposal / recitals)", "Harmonise national protection regimes", "Reduced fragmentation of database protection", "",
     "Commission's 2018 evaluation judges harmonisation effective, helped by CJEU case law; based on qualitative assessment and stakeholder input.",
     "reported as activity", "SWD(2018) 146/147"),
 ind("objective (Art. 16(3))", "Balance between makers and users; no significant interference with competition", "", "",
     "2018 evaluation found costs and benefits 'moderate', benefits 'seem to be higher', no significant regulatory burdens; after the 2004 CJEU rulings the right does not cover by-product data, limiting effects on the data economy. Not quantified.",
     "partially measured", "SWD(2018) 146/147; Technopolis/JIIP 2018"),
]
literature = [
 lit("ec-2005-database-evaluation", "European Commission, DG Internal Market and Services", 2005, "First evaluation of Directive 96/9/EC on the legal protection of databases", "DG MARKT working paper, 12 December 2005", "https://ec.europa.eu/internal_market/copyright/docs/databases/evaluation_report_en.pdf",
     "Commission evaluation", "descriptive (Gale Directory of Databases counts; online industry survey)", "database production; EU vs US competitiveness", "no effect / negative",
     "'The economic impact of the sui generis right on database production is unproven'; EU database entries fell back to pre-Directive level (3,095 in 2004 vs 3,092 in 1998; peak 4,085 in 2001); EU/US production ratio worsened from ~1:2 (1996) to ~1:3 (2004); publishers nevertheless argued the right was crucial",
     "The Commission's first evaluation found that EU database production was no higher in 2004 than before the Directive, while the US - with no such right - pulled further ahead.",
     "EU vs US, 1996-2004", "descriptive counts; no control for other factors", "page summary via search (report quoted verbatim by EDRi and Harvard Berkman blog; original URL now offline)"),
 lit("ec-2018-database-evaluation", "European Commission", 2018, "Evaluation of Directive 96/9/EC on the legal protection of databases (executive summary SWD(2018) 147)", "SWD(2018) 146", "https://digital-strategy.ec.europa.eu/en/library/staff-working-document-and-executive-summary-evaluation-directive-969ec-legal-protection-databases",
     "Commission evaluation", "review (supporting study, stakeholder survey, legal analysis)", "database production; competitiveness; costs and benefits", "no proven effect",
     "The sui generis right 'continues to have no proven impact on the overall production of databases in Europe, nor on the competitiveness of the EU database industry'; harmonisation effective; costs and benefits moderate with benefits seeming higher; reform judged disproportionate",
     "The Commission's second evaluation repeated that the special database right has not been shown to increase database production in Europe, but kept it because costs appear modest and many stakeholders value it.",
     "EU, 2005-2017", "self-evaluation; largely qualitative", "executive summary full text read", pdf_url="https://data.consilium.europa.eu/doc/document/ST-8467-2018-INIT/en/pdf"),
 lit("technopolis-jiip-2018-database-study", "JIIP, Technopolis Group, University of Cambridge & University of Nottingham", 2018, "Study in support of the evaluation of Directive 96/9/EC on the legal protection of databases", "Study for the European Commission (DG CONNECT)", "https://www.technopolis-group.com/?p=8227",
     "Commission-commissioned evaluation study", "legal literature review, stakeholder survey, expert interviews", "data economy; access to data; scope", "mixed",
     "Views divided on extending protection to machine-generated data; academic researchers feared more data locked in closed databases or costly access models",
     "The study behind the 2018 evaluation found stakeholders split on the right, with researchers worried it could lock up data.",
     "EU, 2017", "qualitative", "page summary via search"),
 lit("boyle-2004-database-experiment", "Boyle", 2004, "A natural experiment: Do we want 'faith-based' IP policy?", "Financial Times online, 22 November 2004", "https://law.duke.edu/boylesite/experiment.html",
     "commentary", "descriptive comparison (EU with database right vs US without, Gale Directory data)", "database production", "negative",
     "Argues the EU-US divergence after 1996 is a natural experiment showing the right did not boost EU database production; calls for evidence-based IP policy",
     "A leading copyright scholar argued that comparing Europe, which created a database right, with the US, which did not, shows the right failed to boost European databases.",
     "EU vs US, 1990s-2004", "opinion piece; descriptive", "full text read"),
]
write("31996L0009", "Database Directive", "51992PC0024", "none (1992 proposal predates impact assessments)",
      "thin but consistent: two Commission evaluations (2005, 2018) with descriptive data find no proven effect on database production; no causal academic study",
      "The Database Directive created a special 'sui generis' right to encourage investment in European databases. Two Commission evaluations, in 2005 and 2018, found no proven effect on database production or the industry's competitiveness: EU database entries in 2004 were back at their 1998 level (about 3,100) while the US, which has no such right, pulled further ahead. The Commission kept the right because its costs appear modest and publishers value it.",
      indicators, literature)
