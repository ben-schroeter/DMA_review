import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("specific objective", "Increase capabilities and preparedness of Member States and businesses; improve cooperation; raise awareness; strengthen trust through certification of ICT products and services"),
 ind("indicator (LFS 1.4.4)", "ENISA outputs", "Trainings, good practices, threat landscape reports, exercises (e.g. Cyber Europe), support requests handled", "",
     "Evaluation: ENISA delivered nearly all planned outputs and stakeholders value its work, but 'with no sufficient indicators in place' the assessment relies mainly on interviews and surveys; insufficient resources and hiring problems caused delays.", "reported as activity", "COM(2026) 9"),
 ind("indicator (LFS 1.4.4)", "Certification", "Number of certification schemes adopted under the framework", "",
     "One scheme (EUCC, common criteria) adopted in early 2024, 57 months after initiation; cloud scheme (EUCS) stalled over data-sovereignty disputes; 5G scheme not adopted. Framework judged unable to reduce fragmentation.", "measured (low)", "COM(2026) 9"),
 ind("indicator (LFS 1.4.4)", "Certification", "Reduced cost of obtaining an ICT security certificate", "", "Not measured.", "not measured", "COM(2026) 9"),
 ind("indicator (LFS 1.4.4)", "Awareness", "Increase in cyber awareness among EU citizens (e.g. awareness quiz scores)", "", "No time series reported in the evaluation.", "not measured", "COM(2026) 9"),
 ind("expected impact (LFS 1.4.3)", "Economy", "Help reduce the cost of cyber incidents, estimated at 0.41% of EU GDP (about EUR 55bn)", "baseline EUR 55bn", "Not measured or attributed.", "not measured", "COM(2017) 477"),
]
literature = [
 lit("ec-2017-csa-ia", "European Commission", 2017, "Impact Assessment accompanying the Cybersecurity Act proposal (executive summary SWD(2017) 501)", "SWD(2017) 500", EU + "52017SC0501",
     "Commission impact assessment", "ex-ante (qualitative)", "cyber resilience; certification market fragmentation", "positive (forecast, qualitative)",
     "Preferred option: permanent, reinforced ENISA plus an EU ICT security certification framework enabling mutual recognition; moderate extra EU budget cost; benefits not quantified (context: cyber incidents cost about 0.41% of EU GDP)",
     "The Commission expected a stronger EU cyber agency and EU-wide certification to reduce fragmentation and raise trust, without quantifying the benefits.",
     "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
 lit("ec-2026-csa-evaluation", "European Commission", 2026, "Report on the evaluation of ENISA and the European Cybersecurity Certification Framework", "COM(2026) 9 (SWD(2026) 2)", EU + "52026DC0009",
     "Commission evaluation", "evaluation (interviews, surveys, document review; external study completed Dec 2024)", "ENISA effectiveness; certification", "mixed",
     "ENISA delivered nearly all planned outputs but lacked indicators and resources; the certification framework failed to reduce fragmentation: first scheme (EUCC) took 57 months and was adopted only in early 2024, cloud scheme stalled over data-sovereignty debates",
     "The Commission's evaluation found the EU cyber agency does useful work but is stretched, while the certification system has been slow and has not reduced fragmentation: only one scheme was adopted in five years.",
     "EU, 2017-2023", "self-evaluation; no outcome indicators", "full text partly read"),
 lit("ec-2026-csa2-ia", "European Commission", 2026, "Impact Assessment accompanying the proposal for a Cybersecurity Act 2 (executive summary SWD(2026) 12)", "SWD(2026) 11", EU + "52026SC0012",
     "Commission impact assessment", "ex-ante", "costs; compliance burden; certification reform", "positive (forecast)",
     "Proposes repealing and replacing Regulation 2019/881: reformed certification framework with scheme maintenance; ENISA costs up to EUR 161.3m over five years; compliance savings for businesses of up to EUR 14.6bn",
     "Building on the evaluation, the Commission proposed in 2026 to replace the Cybersecurity Act and fix its certification process.",
     "EU, forecast", "forecast", "full text read (executive summary, partly)"),
]
write("32019R0881", "Cybersecurity Act", "52017PC0477", "SWD(2017) 500 (executive summary SWD(2017) 501)",
      "thin: one Commission evaluation based on interviews and surveys (no outcome indicators); no independent impact studies",
      "The Cybersecurity Act made the EU cyber agency ENISA permanent and created an EU-wide certification system for ICT products. The Commission's 2026 evaluation found ENISA delivered nearly all its planned work but lacked resources and indicators, while certification badly underperformed: the first scheme took almost five years and the cloud scheme stalled. The Commission has proposed replacing the Act; no independent study measures its effect on cyber resilience.",
      indicators, literature)
