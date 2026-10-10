import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The proposal's financial statement contains no indicators section; the Commission will evaluate within two years after each European Parliament election, using contractor data collection"),
 ind("expected impact (impact assessment)", "Transparency of political advertising", "Labelled political ads with sponsor, cost and targeting information; common ad repository; better oversight", "",
     "Regulation applies from 10 October 2025. Google (Nov 2024 announcement) and Meta (from 6 Oct 2025) stopped selling political, electoral and social-issue ads in the EU rather than comply, so the main online channels and their ad libraries for such ads have largely disappeared. Pre-application audit found Meta met 9 and Google 7 of 19 transparency criteria in the 2024 EU elections.", "mixed evidence", "Meta 2025; EDMO 2025"),
 ind("expected impact (impact assessment)", "Single market for political advertising services", "Less fragmentation, lower costs for cross-border campaigns and SMEs scaling up", "",
     "Not measured; the exit of the largest platforms points the other way for online services.", "not measured", "SWD(2021) 356"),
 ind("expected impact (impact assessment)", "Protection against manipulation via targeting", "Restrictions on targeting using personal data", "", "Not measured.", "not measured", "SWD(2021) 356"),
]
literature = [
 lit("ec-2021-polads-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Regulation on the transparency and targeting of political advertising (executive summary SWD(2021) 356)", "SWD(2021) 355", EU + "52021SC0356",
     "Commission impact assessment", "ex-ante (qualitative)", "legal certainty; transparency; compliance costs", "positive (forecast)",
     "Expected more legal certainty and lower fragmentation costs, transparency of targeting, better oversight and public trust; compliance costs offset by efficiency gains; no quantified headline",
     "The Commission expected clearer, EU-wide rules to make political ads more transparent and cheaper to run across borders, but gave no figures.",
     "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
 lit("edmo-2025-eu-election-ads", "Meyer et al. (European Digital Media Observatory)", 2025, "A Cross-Country Analysis of Electoral Advertising on Meta and Google during the EU 2024 Elections: Compliance, Transparency, and Targeting", "EDMO report, September 2025", "https://edmo.eu/wp-content/uploads/2025/09/EDMO-Analysis-of-Electoral-Advertising.pdf",
     "research report (EU-funded observatory)", "descriptive audit of ad libraries across 15 Member States (before the Regulation applied)", "platform transparency; ad spend; targeting", "n/a (baseline)",
     "Meta and Google definitions not fully aligned with Regulation 2024/900; Meta met 9 and Google 7 of 19 transparency criteria; about 30,000 ads and EUR 8.7m spent by parties in 15 countries; targeting common but mostly broad; Meta targeting details disappearing by Aug 2025",
     "Before the rules applied, an audit of the 2024 EU election found Meta and Google only partly met the new transparency standards, with parties spending about EUR 8.7 million on 30,000 ads in 15 countries.",
     "15 EU countries, 2024 EP elections", "descriptive baseline", "full text read (conclusions)", pdf_url="https://edmo.eu/wp-content/uploads/2025/09/EDMO-Analysis-of-Electoral-Advertising.pdf",
     interested_party="Funded by the European Union"),
 lit("meta-2025-ttpa-exit", "Meta", 2025, "Ending Political, Electoral and Social Issue Advertising in the EU in Response to Incoming European Regulation", "Meta Newsroom, 25 July 2025 (updated 6 October 2025)", "https://about.fb.com/news/2025/07/ending-political-electoral-and-social-issue-advertising-in-the-eu/",
     "company statement", "announcement", "availability of political advertising", "negative",
     "From 6 October 2025 Meta no longer delivers political, electoral and social-issue ads in the EU, citing 'unworkable requirements and legal uncertainties' of the Regulation; notes other platforms have done the same",
     "Meta stopped all political and social-issue ads in the EU in October 2025, blaming the new rules; Google had already announced the same in 2024.",
     "EU, Oct 2025", "self-reported; company position", "full text read", interested_party="Regulated company; statement explains its own commercial decision"),
]
write("32024R0900", "Political Advertising Regulation", "52021PC0731", "SWD(2021) 355 (executive summary SWD(2021) 356)",
      "ex-ante only, with an early unintended effect: largest platforms withdrew from political ads",
      "The Commission expected EU-wide rules to make political ads more transparent and easier to run across borders, but put no numbers on it. When the rules took effect in October 2025, Google and Meta stopped selling political and social-issue ads in the EU altogether rather than comply, so the regulation's main early effect has been to shrink online political advertising rather than make it more transparent; no study yet measures effects on campaigns or voters.",
      indicators, literature)
