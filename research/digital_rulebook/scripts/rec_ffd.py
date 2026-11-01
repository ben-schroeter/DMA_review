import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement has no indicators section; the memorandum promised an evaluation five years on using indicators from the impact assessment, Eurostat and DESI data"),
 ind("evaluation question (memorandum)", "Data localisation", "Reduction in the number and range of data localisation restrictions", "", "Not quantified. The 2026 evaluation support study finds limited effectiveness in removing localisation requirements, hampered by the national-security exemption and uncertainty about mixed data sets.", "mixed evidence", "Open Evidence et al. 2026 study"),
 ind("evaluation question (memorandum)", "Regulatory access", "Member States can access data stored abroad for regulatory control", "", "No publicly reported cases under the Article 5 cooperation or penalty mechanisms; authorities report low demand.", "reported as activity (none)", "SWD(2025) 836"),
 ind("evaluation question (memorandum)", "Cloud switching", "Better transparency on conditions for data porting (self-regulatory codes)", "", "Codes of conduct had limited uptake and were superseded by binding switching rules in the Data Act (2023); Commission calls Article 6 practically obsolete.", "not achieved (superseded)", "SWD(2025) 836"),
 ind("evaluation question (memorandum)", "Trust", "Trust in free flow of non-personal data", "", "Consultation: fewer than 4 in 10 respondents see any objective fully met; weakest scores on trust/security and switching; about half have little or no familiarity with the Regulation.", "partially measured (opinion survey)", "SWD(2025) 836"),
 ind("expected impact (impact assessment)", "Growth", "GDP gain of up to EUR 8bn a year (0.06% of GDP) from removing localisation restrictions", "up to EUR 8bn/yr", "Never evaluated.", "not measured", "SWD(2017) 304; ECIPE 2016"),
]
literature = [
 lit("ec-2017-ffd-ia", "European Commission", 2017, "Impact Assessment accompanying the proposal on a framework for the free flow of non-personal data (executive summary SWD(2017) 305)", "SWD(2017) 304", EU + "52017SC0304",
     "Commission impact assessment", "ex-ante (relies on ECIPE and Deloitte modelling)", "GDP; cloud market competition", "positive (forecast)",
     "Removing localisation restrictions could raise GDP by up to EUR 8bn (0.06%) a year (ECIPE); Deloitte estimate of EUR 11.6bn net present value for cloud users and providers; moderate costs for cloud providers",
     "The Commission expected that banning unjustified national rules on where data must be stored would add up to EUR 8 billion a year to EU GDP.",
     "EU, forecast", "forecast", "full text partly read"),
 lit("bauer-et-al-2016-ecipe", "Bauer, Ferracane, Lee-Makiyama & van der Marel", 2016, "Unleashing Internal Data Flows in the EU: An Economic Assessment of Data Localisation Measures in the EU Member States", "ECIPE Policy Brief 3/2016", "https://ecipe.org/publications/unleashing-internal-data-flows-in-the-eu/",
     "think-tank study", "ex-ante (computable general equilibrium modelling)", "GDP", "positive (forecast)",
     "Identified 22 localisation measures in EU Member States; removing them would raise GDP by up to EUR 8bn a year (0.06%)",
     "A think-tank model found 22 national data localisation rules in the EU and estimated that scrapping them could add up to EUR 8 billion a year to GDP.",
     "EU, 2016", "model-based forecast, not an evaluation", "page summary via search"),
 lit("open-evidence-2026-ffd-eval-study", "Open Evidence et al. for the European Commission", 2026, "Study supporting the evaluation of the free flow of non-personal data regulation, open data directive and data governance act", "Publications Office of the EU", "https://op.europa.eu/en/publication-detail/-/publication/3a2a3e8b-edd1-11f0-8d3c-01aa75ed71a1/language-en",
     "evaluation support study (contractor for Commission)", "evaluation (consultation, desk research)", "data localisation; legal certainty", "limited effect",
     "Regulation has shown limited effectiveness in removing data localisation requirements, hampered by the national-security exemption and legal uncertainty about mixed data sets",
     "An evaluation study for the Commission concluded the Regulation did little to remove national data localisation rules.",
     "EU, 2019-2025", "qualitative evaluation; no quantified effect", "page summary via search (contractor's announcement)"),
 lit("ec-2025-digital-omnibus-swd", "European Commission", 2025, "Staff working document accompanying the Digital Omnibus proposals", "SWD(2025) 836", EU + "52025SC0836",
     "Commission staff working document", "review (public consultation, SME panel)", "uptake; enforcement; cloud switching", "limited effect",
     "Limited uptake and modest stakeholder interest; no publicly reported cases under cooperation or penalty mechanisms; switching codes superseded by the Data Act; fewer than 4 in 10 consultation respondents see any objective fully met; proposes repealing the Regulation and moving the free-flow principle into the Data Act",
     "The Commission found little use of the Regulation and proposes folding its core principle into the Data Act and repealing it.",
     "EU, 2019-2025", "consultation-based; no quantitative outcome data", "full text partly read"),
]
write("32018R1807", "Free Flow of Non-Personal Data Regulation", "52017PC0495", "SWD(2017) 304 (executive summary SWD(2017) 305)",
      "thin: no promised indicators measured; evaluation evidence qualitative and points to limited effect; no causal studies",
      "The Commission expected the Regulation to add up to EUR 8 billion a year to EU GDP by removing national rules on where data must be stored. That gain was never measured; an evaluation study and the Commission's own 2025 review found limited uptake, no recorded use of its enforcement mechanisms and little success in removing localisation rules. The Commission now proposes to repeal it and move its core principle into the Data Act.",
      indicators, literature)
