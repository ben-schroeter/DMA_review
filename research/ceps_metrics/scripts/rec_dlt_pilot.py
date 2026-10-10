import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
ESMA = "https://www.consob.it/documents/d/asset-library-1912910/esma75-117376770-460"
indicators = [
 ind("note", "The proposal has no LFS indicators section (extraction empty). Article 14 requires an ESMA report and a Commission report after three years on whether to extend, amend or make the regime permanent"),
 ind("expected impact (impact assessment)", "Development of DLT market infrastructures", "Number of DLT market infrastructures authorised and operating", "",
     "By 31 May 2025 only three authorised (CSD Prague, 21X AG, 360X AG) with minimal live trading activity; growing applicant interest reported.", "measured", "ESMA 2025"),
 ind("expected impact (impact assessment)", "Competition with legacy infrastructures / EU competitiveness", "New entrants competing with incumbent trading and settlement venues", "",
     "Not measured; ESMA finds current thresholds restrict participation and cites lack of interoperability and access to central bank money. Commission proposed in Dec 2025 to make the regime permanent and lift the aggregate cap from EUR 6bn to EUR 100bn.", "not measured", "ESMA 2025; SWD(2025) 943"),
 ind("expected impact (impact assessment)", "Costs", "Small compliance costs for venues; NCA supervision EUR 150,000-250,000 per year", "",
     "Not evaluated.", "not measured", "SWD(2020) 202"),
]
literature = [
 lit("ec-2020-crypto-dlt-ia", "European Commission", 2020, "Impact Assessment accompanying the proposals on markets in crypto-assets and on a pilot regime for DLT market infrastructures (executive summary SWD(2020) 202)", "SWD(2020) 201", EU + "52020SC0202",
     "Commission impact assessment", "ex-ante (option comparison)", "security token trading and settlement; competition; supervisory costs", "positive (forecast)",
     "Pilot regime preferred for security tokens: enables new DLT-based infrastructures to compete with legacy ones in the medium to long term; small compliance costs for venues; NCA costs EUR 150,000-250,000 per year", "The Commission expected a three-year sandbox for blockchain-based trading and settlement to let new entrants compete with existing stock exchanges and depositories at little cost.",
     "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
 lit("esma-2025-dlt-review", "European Securities and Markets Authority", 2025, "ESMA Report on the Functioning and Review of the DLT Pilot Regime pursuant to Article 14 of Regulation (EU) 2022/858", "ESMA75-117376770-460, 25 June 2025", ESMA,
     "EU agency report", "review report (supervisory data to 31 May 2025)", "uptake; activity; thresholds; interoperability", "mixed",
     "Uptake limited: only three authorised DLT market infrastructures and minimal live trading; regime stimulated experimentation; frictions include interoperability and access to central bank money; thresholds restrict participation; recommends recalibrating thresholds and clarifying long-term status", "The EU securities regulator found that after two years only three blockchain market infrastructures had been licensed and trading was minimal, and recommended loosening the size caps.",
     "EU, Mar 2023-May 2025", "descriptive; supervisory data", "full text read (executive summary)", pdf_url=ESMA),
 lit("ec-2025-misp-dlt", "European Commission", 2025, "Market integration and supervision package: proposal amending Regulation (EU) 2022/858 and others, with impact assessment", "SWD(2025) 943 (procedure 2025/0381 COD), 4 December 2025", EU + "52025SC0943",
     "Commission impact assessment", "ex-ante (review of pilot regime)", "thresholds; scope; permanence", "positive (forecast)",
     "Proposes making the regime permanent, removing product-specific limits and raising the aggregate market value cap from EUR 6bn (EUR 9bn transition trigger) to EUR 100bn (EUR 150bn), with a simplified tier capped at EUR 10bn; Commission says current thresholds constrained the framework", "Responding to the low take-up, the Commission proposed in December 2025 to make the pilot permanent and raise its size cap from EUR 6bn to EUR 100bn.",
     "EU, forecast", "forecast", "page summary via search (figures checked against a Council working paper quoting the proposal)"),
]
write("32022R0858", "DLT Pilot Regime Regulation", "52020PC0594", "SWD(2020) 201 (executive summary SWD(2020) 202)",
      "thin: regulator's review documents very low uptake; no independent study of effects",
      "The DLT Pilot Regime lets trading venues and securities depositories test blockchain technology under relaxed rules. By mid-2025 only three had been licensed and live trading was minimal; the EU securities regulator blamed tight size caps and practical barriers. The Commission proposed in December 2025 to make the regime permanent with much higher caps; no study has measured effects on costs or competition.",
      indicators, literature)
