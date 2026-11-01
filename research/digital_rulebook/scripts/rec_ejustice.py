import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator (1.4.4)", "Efficient judicial cooperation between authorities", "Number of electronic exchanges via the decentralised IT system, against a baseline of traditional exchanges in a control group of authorities", "Monitored annually for at least 5 years from start of digital exchanges",
     "No published data found; obligations phase in from 2025 onwards as implementing acts and IT systems are rolled out.", "not measured", ""),
 ind("LFS indicator (1.4.4)", "Access to justice", "Number of electronic claims and submissions by citizens and businesses (e.g. European Small Claims) via the European electronic access point", "Baseline: paper submissions in control group",
     "No published data found.", "not measured", ""),
 ind("expected impact (impact assessment)", "Cost savings", "Yearly savings of about EUR 25.6m in postage and paper (EUR 4.5m for individuals and firms); procedures shortened by ~15.4m days in total per year", "",
     "Not measured.", "not measured", "SWD(2021) 392/393"),
 ind("expected impact (impact assessment)", "Costs", "One-off IT cost EUR 18.7m over 5 years; recurrent EUR 8.1m/yr at EU-27 level", "",
     "Not measured.", "not measured", "SWD(2021) 393"),
]
literature = [
 lit("ec-2021-ejustice-ia", "European Commission", 2021, "Impact Assessment accompanying the proposals on the digitalisation of judicial cooperation and access to justice in cross-border civil, commercial and criminal matters (executive summary SWD(2021) 393)", "SWD(2021) 392", EU + "52021SC0393",
     "Commission impact assessment", "ex-ante", "administrative costs; case duration; access to justice", "positive (forecast)",
     "Yearly savings EUR 25.59m in postage and paper at EU level (EUR 4.49m for individuals and legal entities); total case duration cut by ~15.4m days a year; one-off IT cost EUR 18.7m over 5 years; recurrent EUR 8.1m/yr; videoconferencing emits 7% of the carbon of physical meetings",
     "The Commission expected that moving cross-border court paperwork online would save about EUR 25 million a year in postage and paper and shorten proceedings.",
     "EU, forecast", "forecast", "full text read"),
]
write("32023R2844", "Digitalisation of judicial cooperation Regulation", "52021PC0759", "SWD(2021) 392 (executive summary SWD(2021) 393)",
      "ex-ante only: impact assessment forecasts; no monitoring data or independent studies found",
      "This regulation moves communication between courts and authorities in cross-border cases onto secure digital channels and lets people and firms file claims online and join hearings by video. The Commission forecast savings of about EUR 25 million a year in postage and paper and shorter proceedings. Its obligations are still being phased in, and no data or studies on its effects have been published yet.",
      indicators, literature)
