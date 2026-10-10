import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Findable information", "Share of users who found the information they were looking for", "",
     "Your Europe user survey: 77% of businesses and 76% of citizens found what they were looking for (2023 report).", "measured", "COM(2023) 534"),
 ind("LFS indicator (1.4.4)", "Awareness and use", "Trend in average monthly users", "",
     "Your Europe ~43 million visits in 2022 (third most visited Commission site); national SDG pages >100 million visits a year in 2021-2022.", "measured", "COM(2023) 534"),
 ind("LFS indicator (1.4.4)", "Quality", "Share satisfied with quality", "",
     "92.5% of citizens and 90.3% of businesses rated the portal satisfactory or better; assistance services 4.3/5 average from ~3,200 feedbacks (self-selected respondents).", "measured", "COM(2023) 534"),
 ind("LFS indicator (1.4.4)", "Core procedures online for cross-border users", "Share of (cross-border) users able to complete procedures fully online", "21 procedures fully online by end-2023",
     "eGovernment Benchmark (preliminary, 2023): SDG procedures 84% completable online by nationals but only 47% by cross-border users; Once-Only Technical System still being rolled out.", "partially measured", "COM(2023) 534"),
 ind("expected impact (impact assessment)", "Reduce costs for businesses", "Annual cost savings for businesses expanding cross-border", "EUR 11-55bn a year (indicative)",
     "Not measured; the Commission's only ex-post figure is about EUR 2.5m a year in avoided legal-advice costs for Your Europe business users.", "not measured", "SWD(2017) 213/214; COM(2023) 534"),
]
literature = [
 lit("ec-2017-sdg-ia", "European Commission", 2017, "Impact Assessment accompanying the proposal for a Regulation on establishing a single digital gateway (executive summary)", "SWD(2017) 214 (full IA SWD(2017) 213)", EU + "52017SC0214",
     "Commission impact assessment", "ex-ante", "administrative burden; cross-border trade; public costs", "positive (forecast)",
     "Could reduce business costs by EUR 11-55bn a year (based on 9 procedures and 9 information topics); set-up cost about EUR 5.8m per Member State, EUR 4.3-4.8m for the Commission",
     "The Commission estimated that a single EU portal for information and online procedures could save businesses EUR 11-55 billion a year.",
     "EU, forecast", "forecast; wide range", "full text read (executive summary)"),
 lit("ec-2023-sdg-report", "European Commission", 2023, "First Implementation Report on the Single Digital Gateway", "COM(2023) 534", EU + "52023DC0534",
     "Commission implementation report", "monitoring report (usage statistics, user surveys, eGovernment Benchmark)", "usage; satisfaction; online procedures; obstacles", "positive (partial)",
     "43m Your Europe visits in 2022; 90%+ satisfaction; 76-77% found information; 6.5m assistance cases 2021-22; SDG procedures 84% online for nationals vs 47% for cross-border users; ~EUR 2.5m/yr saved in legal advice",
     "The first implementation report shows heavy use and high satisfaction with the Your Europe portal, but fewer than half of key procedures could yet be completed online by people from other EU countries.",
     "EU, 2020-2023", "Commission self-assessment; usage data robust, savings minimal", "full text read (relevant sections)"),
 lit("graux-2021-sdg-once-only", "Graux", 2021, "The Single Digital Gateway Regulation as an Enabler and Constraint of Once-Only in Europe", "in The Once-Only Principle, Lecture Notes in Computer Science 12621, Springer", "https://doi.org/10.1007/978-3-030-79851-2_5",
     "peer-reviewed (book chapter)", "legal analysis", "once-only principle; cross-border evidence exchange", "mixed",
     "Analyses how the Regulation enables the once-only principle for cross-border procedures while its design constrains its scope",
     "A legal analysis argues the Regulation both pushes forward and limits the 'tell us once' idea for cross-border paperwork.",
     "EU", "qualitative; no impact data", "page summary via search (Crossref metadata)", access="open"),
]
write("32018R1724", "Single Digital Gateway Regulation", "52017PC0256", "SWD(2017) 213 (executive summary SWD(2017) 214)",
      "moderate on usage, thin on impact: usage and satisfaction indicators measured by the Commission; forecast cost savings unmeasured; no independent impact studies found",
      "The Single Digital Gateway promised to save businesses EUR 11-55 billion a year by putting EU and national information and procedures online. The Commission's 2023 report shows the Your Europe portal is heavily used (43 million visits in 2022) with over 90% satisfaction, but only about half of key procedures could be completed online by users from other EU countries. The promised savings have not been measured, and the 2025 evaluation was not found.",
      indicators, literature)
