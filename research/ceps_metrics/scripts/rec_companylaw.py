import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "Directive 2017/1132 is a codification (proposal COM(2015) 616) with no impact assessment or indicators. Substantive promises come from later amendments: digitalisation (2019/1151), cross-border mobility (2019/2121) and 'digitalisation 2.0' (2025/25)"),
 ind("expected impact (impact assessment, Directive 2019/1151)", "Online company registration and filing", "Savings from online registration for new companies", "EUR 42-84m (forecast)",
     "Online formation applies since 2021-2023 (with extensions); no ex-post measurement of savings found.", "not measured", "SWD(2018) 141/142"),
 ind("expected impact (impact assessment, Directive 2019/2121)", "Cross-border conversions, mergers and divisions", "Use of cross-border operations", "Baseline 2000-2019: 4,305 cross-border mergers, 553 conversions, 19 divisions (concentrated in DE, NL, LU)",
     "Independent counts exist up to 2023 (Biermeyer & Meyer series); no evaluation of the 2019 mobility rules yet.", "partially measured", "Biermeyer & Meyer 2019"),
 ind("expected impact (impact assessment, Directive 2025/25)", "Cross-border use of company data", "Recurrent administrative savings for companies", "about EUR 437m a year (forecast); one-off costs ~EUR 311m",
     "Transposition due 2027; forecast only.", "not measured", "SWD(2023) 178/179"),
]
literature = [
 lit("ec-2018-companylaw-package-ia", "European Commission", 2018, "Impact Assessment on the EU Company Law package (digital tools; cross-border conversions, mergers and divisions), executive summary", "SWD(2018) 142 (full IA SWD(2018) 141)", EU + "52018SC0142",
     "Commission impact assessment", "ex-ante", "registration costs; cross-border operations; SMEs", "positive (forecast)",
     "Online registration expected to save new companies EUR 42-84m; harmonised cross-border conversion and division rules expected to benefit especially SMEs",
     "For the 2019 amendments the Commission forecast EUR 42-84 million in savings from registering companies online and easier cross-border moves for small firms.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("ec-2023-companylaw-digital-ia", "European Commission", 2023, "Impact Assessment on further expanding and upgrading digital tools in company law, executive summary", "SWD(2023) 179 (full IA SWD(2023) 178)", EU + "52023SC0179",
     "Commission impact assessment", "ex-ante", "administrative burden; company data transparency", "positive (forecast)",
     "Recurrent savings of about EUR 437m a year for companies operating cross-border; one-off costs of about EUR 311m for companies newly filing data; EUR 5.4m one-off for registers",
     "For the 2025 amendment the Commission forecast about EUR 437 million a year in savings for firms doing business across borders.",
     "EU, forecast", "forecast", "full text read (executive summary)"),
 lit("biermeyer-meyer-2019-mobility", "Biermeyer & Meyer", 2019, "Cross-border Corporate Mobility in the EU: Empirical Findings 2019 (Vol. 1)", "Maastricht University / SSRN 3403791", "https://papers.ssrn.com/abstract=3403791",
     "working paper / data report", "descriptive (case counts from registers and official journals)", "cross-border mergers; conversions; seat transfers", "n/a",
     "2000-2019: 4,305 cross-border mergers, 553 conversions, 158 SE seat transfers, 19 divisions; heavily concentrated in Germany, the Netherlands and Luxembourg, suggesting incomplete integration",
     "Researchers counted about 8,400 cross-border company moves between 2000 and 2019, concentrated in a few countries, a baseline for judging the 2019 mobility rules.",
     "EU/EEA, 2000-2019", "descriptive baseline; pre-dates 2019 amendments", "page summary via search"),
]
write("32017L1132", "Company Law Directive", "52015PC0616", "None (codification); amendment IAs SWD(2018) 141 and SWD(2023) 178",
      "ex-ante only: codification with no promises of its own; amendment forecasts not yet evaluated; only descriptive mobility counts",
      "The 2017 Company Law Directive merely consolidated older rules, so it set no targets of its own. Later amendments promised EUR 42-84 million in savings from online company registration and about EUR 437 million a year from easier cross-border use of company data, but none has been evaluated. Independent counts show cross-border company moves remain concentrated in a few countries.",
      indicators, literature)
