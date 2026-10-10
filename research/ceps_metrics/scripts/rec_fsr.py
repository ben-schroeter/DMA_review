import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Identify the most distortive subsidies", "Yearly number of cases of alleged distortive foreign subsidies dealt with", "IA projected 30-40 merger notifications a year",
     "By 31 May 2026: 273 merger notifications (about 100 a year, well above the 30-40 projected), 5,150 submissions across 863 public procurement procedures; 3 in-depth merger and 4 in-depth procurement investigations; ex officio cases opened (e.g. Nuctech, Goldwind).", "reported as activity", "COM(2026) 368"),
 ind("LFS indicator (1.4.4)", "Identify the most distortive subsidies", "Share of cases found distortive vs total cases", "",
     "About 97% of notified mergers cleared after preliminary review; two merger cases (e&/PPF Telecom, ADNOC/Covestro) and one procurement case ended with commitments; three procurement probes closed after the Chinese bidders withdrew.", "partially measured", "COM(2026) 368"),
 ind("LFS indicator (1.4.4)", "Identify the most distortive subsidies", "Share of cases cleared thanks to the balancing test", "",
     "No case has yet applied the balancing test in practice, according to the review.", "not measured", "COM(2026) 368"),
 ind("LFS indicator (1.4.4)", "Remove distortions caused by foreign subsidies", "Stakeholder perceptions of the impact of redressive measures", "",
     "Review consultation: stakeholders support the objective but say compliance costs are disproportionate, especially for notifications; Commission plans simplification (higher thresholds, shorter forms). Procurement filing compliance reportedly fell from about 70% to 45% by late 2025.", "reported as activity", "COM(2026) 368"),
 ind("expected impact (impact assessment)", "Investment", "Possible short-term drop in foreign direct investment, offset in the medium term by a level playing field", "",
     "No study measures the FSR's effect on FDI, M&A or tender participation.", "not measured", "SWD(2021) 99/100"),
]
literature = [
 lit("ec-2021-fsr-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Regulation on foreign subsidies distorting the internal market (executive summary SWD(2021) 100)", "SWD(2021) 99", EU + "52021SC0100",
     "Commission impact assessment", "ex-ante", "level playing field; compliance costs; FDI", "positive (forecast)",
     "New instrument with notification for large mergers and tenders; low burden for SMEs; possible short-term drop in FDI offset by fairer competition", "The Commission expected the new tool to restore fair competition with foreign-subsidised firms at modest cost, while warning that foreign investment might dip at first.",
     "EU, forecast", "forecast; few quantified impacts", "full text read"),
 lit("ec-2026-fsr-review", "European Commission", 2026, "Report on the implementation and enforcement of Regulation (EU) 2022/2560 (first review, with SWD(2026) 183)", "COM(2026) 368", EU + "52026DC0368",
     "Commission review report", "implementation review (case statistics, consultation, call for evidence)", "enforcement activity; administrative burden", "positive (self-assessment)",
     "Fit for purpose; 273 merger notifications to 31 May 2026 (about 100 a year vs 30-40 projected), 97% cleared in preliminary review; 5,150 procurement submissions in 863 procedures; commitments in e&/PPF and ADNOC/Covestro; deterrence via bidder withdrawals; stakeholders report disproportionate costs; targeted simplification planned",
     "The Commission's first review says the regime works and has deterred some subsidised bidders, but handles far more filings than expected and firms complain of heavy paperwork.",
     "EU, Oct 2023-May 2026", "self-assessment; no counterfactual", "full text read"),
]
write("32022R2560", "Foreign Subsidies Regulation", "52021PC0223", "SWD(2021) 99 (executive summary SWD(2021) 100)",
      "thin: Commission enforcement statistics and self-assessed review only; no independent or causal study of effects on competition, investment or prices",
      "The Foreign Subsidies Regulation lets the Commission check whether subsidies from non-EU governments distort EU takeovers and public tenders. Its first review (July 2026) counted about 100 merger notifications a year, far above the 30-40 expected, a handful of in-depth cases ending in commitments, and several Chinese bidders withdrawing from tenders. No independent study yet measures its effect on competition, investment or prices, and businesses say the filing burden is heavy.",
      indicators, literature)
