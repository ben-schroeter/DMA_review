import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No impact assessment: the Commission argued STEP creates no new instrument and relies on existing programmes' assessments"),
 ind("headline forecast (proposal)", "Investment mobilised", "Total new investment through STEP could reach up to EUR 160bn (proposal assumed EUR 10bn of fresh EU money)", "up to EUR 160bn",
     "Final regulation added only EUR 1.5bn new money (to the European Defence Fund). By March 2025: about EUR 6.3bn of cohesion funds reprogrammed and EUR 9.5bn of calls under Commission-managed programmes, EUR 5.1-5.2bn awarded.", "reported as activity", "COM(2023) 335; COM(2025) 421"),
 ind("LFS indicator (1.4.4)", "Critical technologies and skills", "Enterprises supported; participants in trainings; total investment mobilised; jobs created or maintained", "",
     "Interim evaluation reports funds and 190 STEP Seals awarded; about 15% of cohesion reallocations for skills; no figures yet on enterprises, trainees or jobs; Commission says too early for impact evaluation.", "reported as activity", "COM(2025) 421"),
 ind("expected impact (LFS 1.4.3)", "Industrial capability and competitiveness", "Substantial strengthening of EU industrial capabilities in clean, bio and deep tech", "",
     "Not measured. Seal projects had not yet received cohesion or RRF funding by March 2025; Seals concentrated in more developed regions.", "not measured", "COM(2025) 421"),
]
literature = [
 lit("ec-2023-step-proposal", "European Commission", 2023, "Proposal for a Regulation establishing the Strategic Technologies for Europe Platform (STEP)", "COM(2023) 335", EU + "52023PC0335",
     "Commission proposal (no impact assessment)", "ex-ante (explanatory memorandum)", "investment mobilised", "positive (forecast)",
     "Total estimated new investment through STEP could reach up to EUR 160bn; no impact assessment because STEP works through existing instruments",
     "The Commission claimed STEP could trigger up to EUR 160 billion of investment in critical technologies, without a dedicated impact assessment.",
     "EU, forecast", "forecast", "full text read (relevant sections)"),
 lit("ec-2025-step-interim-evaluation", "European Commission", 2025, "Interim evaluation of the Strategic Technologies for Europe Platform (STEP)", "COM(2025) 421 and SWD(2025) 194", EU + "52025DC0421",
     "Commission evaluation", "interim evaluation (implementation monitoring, first 13 months)", "funds mobilised; STEP Seals; regional distribution", "mixed",
     "About EUR 6.3bn of cohesion funds redirected (38 programme amendments, 11 Member States); EUR 9.5bn of STEP calls in centrally managed programmes with over EUR 5.1bn awarded; 190 STEP Seals but no Seal project yet funded from cohesion or RRF; complexity of 11 programmes limits impact; too early for full assessment",
     "The Commission's own interim review found about EUR 15 billion of existing EU money steered towards strategic technologies, but said the quality label has not yet unlocked new funding and it is too early to judge impact.",
     "EU, Mar 2024-Mar 2025", "self-assessment; activity data only", "full text read"),
]
write("32024R0795", "Strategic Technologies for Europe Platform (STEP)", "52023PC0335", "none (proposal relied on existing programmes' impact assessments)",
      "ex-ante only: no impact assessment; Commission activity figures; no independent impact study",
      "The Commission claimed STEP could trigger up to EUR 160 billion of investment in critical technologies, but the final law added only EUR 1.5 billion of new money and mostly redirects existing EU funds. Its own interim review counts about EUR 15 billion steered to strategic technologies in the first year but no data yet on jobs, firms or competitiveness.",
      indicators, literature)
