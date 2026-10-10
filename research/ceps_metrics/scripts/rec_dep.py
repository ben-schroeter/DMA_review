import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no usable LFS indicators (1.4.4 in the extraction covers synergies); performance indicators per specific objective are set in Annex II of the Regulation, and the IA said indicators would also draw on the Digital Economy and Society Index"),
 ind("performance indicator (Regulation annex)", "High performance computing", "Joint procurements of HPC infrastructure; use of exascale systems", "30 procurements by 2029",
     "19 of 30 planned procurements done; JUPITER, the EU's first exascale computer, ranked 4th on TOP500 and 1st on Green500 (its JEDI module); 19 AI Factories being deployed.", "measured (outputs)", "SWD(2025) 420; COM(2025) 771"),
 ind("performance indicator (Regulation annex)", "Adoption of digital technologies (EDIHs)", "Number of European Digital Innovation Hubs and businesses served", "",
     "Over 150 EDIHs covering 90% of regions by end-2024; 29,000 services to 54,600 companies; users value services at EUR 8,000-15,300 per organisation (perceived value, not measured effect).", "reported as activity", "COM(2025) 771"),
 ind("performance indicator (Regulation annex)", "Advanced digital skills", "People trained; master's programmes and courses", "",
     "By end-2024: 50+ master's programmes, 530 short courses, 20,700+ people trained in AI, cybersecurity, semiconductors etc.", "reported as activity", "COM(2025) 771"),
 ind("performance indicator (Regulation annex)", "Cybersecurity", "Cybersecurity infrastructures procured", "",
     "26 CyberHubs procured (in line with targets); network of 27 national coordination centres; first 12 cybersecurity tools deployed.", "measured (outputs)", "COM(2025) 771"),
 ind("expected impact (impact assessment)", "Closing digital investment gap / competitiveness", "Higher EU digital capacity and uptake (e.g. SMEs highly digitised 20% in 2018)", "",
     "Interim evaluation: programme on track or ahead on activities and outputs, first outcome-level benefits only now emerging; no measured effect on productivity, uptake or competitiveness.", "not measured", "SWD(2025) 420"),
]
literature = [
 lit("ec-2018-dep-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal establishing the Digital Europe programme (executive summary SWD(2018) 306)", "SWD(2018) 305", EU + "52018SC0305",
     "Commission impact assessment", "ex-ante (problem analysis; qualitative)", "digital investment gap; HPC; AI; cybersecurity; skills", "positive (forecast)",
     "Identifies an upstream investment gap: EU consumes one third of world HPC resources but provides about 5%; HPC investment at 60% of US level; only 20% of SMEs highly digitised; no quantified impact forecast", "The Commission said Europe was under-investing in supercomputers, AI, cybersecurity and digital skills and proposed a dedicated deployment programme, without forecasting measurable economic gains.",
     "EU, 2021-2027", "forecast; qualitative", "full text skimmed"),
 lit("ec-2025-dep-interim", "European Commission", 2025, "Interim Evaluation of the Digital Europe Programme (Staff Working Document) and report COM(2025) 771", "SWD(2025) 420; COM(2025) 771", EU + "52025SC0420",
     "Commission evaluation", "interim evaluation (monitoring data, surveys, perceived-value study)", "outputs; HPC; EDIHs; skills; cybersecurity", "positive",
     "Implementation initially delayed by late legal basis but accelerated; on track or ahead on outputs; JUPITER exascale system; 150+ EDIHs serving 54,600 companies; 20,700 people trained; 26 CyberHubs; administrative costs 4.9%; outcome-level benefits only emerging", "The Commission's mid-term review finds the EUR 8.2bn programme has delivered its planned supercomputers, innovation hubs and training places, but evidence on effects for firms or the economy is still limited to user ratings.",
     "EU, 2021-2024", "self-evaluation; no counterfactual", "full text read (report; SWD key sections)", pdf_url=""),
]
write("32021R0694", "Digital Europe Programme", "52018PC0434", "SWD(2018) 305 (executive summary SWD(2018) 306)",
      "thin: Commission interim evaluation reports outputs and user ratings; no counterfactual or independent study of impact found",
      "Digital Europe (EUR 8.2bn, 2021-2027) funds supercomputers, AI and cybersecurity infrastructure, innovation hubs and advanced skills. The Commission's 2025 mid-term review shows outputs largely on track - the JUPITER exascale computer, over 150 innovation hubs serving 54,600 firms and 20,700 people trained - but effects on firms' productivity or digital uptake have not been measured, and no independent evaluation was found.",
      indicators, literature)
