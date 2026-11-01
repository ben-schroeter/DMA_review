import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 1991 proposal has no indicators section; the Directive required a Commission report on its application"),
 ind("objective (recitals)", "Cross-border broadcasting", "Country-of-origin rule for satellite broadcasts to ease rights clearance and cross-border reception", "",
     "2002 report: correctly transposed, but rightholders still license territorially (encryption), so practice is not in line with the country-of-origin principle. 2016 evaluation: mechanisms helped clear rights for satellite broadcasts, but are technology-specific and do not reach online transmission.", "reported as activity", "COM(2002) 430; SWD(2016) 308"),
 ind("objective (recitals)", "Cable retransmission", "Mandatory collective management to clear retransmission rights", "",
     "Reported as contributing to cross-border retransmission; some rightholders say they lose income; long mediation disputes.", "reported as activity", "COM(2002) 430"),
 ind("baseline (2016 IA)", "Online availability", "Cross-border availability of broadcasters' online services", "82% of public and 62% of commercial broadcasters geo-block at least one online service (sector inquiry)",
     "Led to Directive (EU) 2019/789; its review was due June 2025 (not found).", "not measured", "SWD(2016) 301"),
]
literature = [
 lit("ec-2002-satcab-report", "European Commission", 2002, "Report on the application of Council Directive 93/83/EEC (satellite broadcasting and cable retransmission)", "COM(2002) 430", EU + "52002DC0430",
     "Commission evaluation (implementation report)", "review (transposition, stakeholder input)", "rights clearance; cross-border broadcasting", "mixed",
     "Correct transposition everywhere, and the mechanisms contribute to cross-border TV broadcasting; but rightholders' practice (territorial licensing, encryption) is not in line with the country-of-origin principle; cable mediation slow; no extension of mandatory collective management proposed",
     "The first review found the directive's rules worked on paper and helped cross-border TV, but broadcasters still sold rights country by country and scrambled signals.",
     "EU-15, to 2002", "self-evaluation; descriptive", "full text read"),
 lit("ec-2016-satcab-evaluation", "European Commission", 2016, "Ex-post (REFIT) evaluation of the Satellite and Cable Directive (93/83/EEC)", "SWD(2016) 308", "https://data.consilium.europa.eu/doc/document/ST-12281-2016-INIT/en/pdf",
     "Commission evaluation", "REFIT evaluation (SatCab study, public consultation 2015)", "rights clearance; relevance", "mixed",
     "Mechanisms helped clear rights for cross-border satellite broadcasts and simultaneous cable retransmission, but technology-specific provisions do not cover newer digital and online transmission; study data limited",
     "The 2016 evaluation found the directive eased rights clearing for satellite and cable, but its rules do not cover online TV.",
     "EU, to 2015", "self-evaluation; data gaps acknowledged", "page summary via search"),
 lit("ec-2016-copyright-ia-satcab", "European Commission", 2016, "Impact assessment on the modernisation of EU copyright rules (online transmissions of broadcasters)", "SWD(2016) 301", EU + "52016SC0301",
     "Commission impact assessment", "ex-ante", "online availability of broadcasts; licensing", "positive (forecast)",
     "Country-of-origin approach not applied online; 82% of public and 62% of commercial broadcasters geo-block at least one online service (e-commerce sector inquiry); extending the principle to ancillary online services expected to widen cross-border access; commercial TV broadcasters warned of weaker territorial licensing",
     "The Commission found most broadcasters block their online services abroad and proposed extending the satellite rule online; commercial TV feared it would undermine exclusive licensing.",
     "EU, forecast", "forecast; qualitative", "full text partly read"),
]
write("31993L0083", "Satellite and Cable Directive", "51991PC0276", "none (pre-dates impact assessments); later SWD(2016) 301",
      "thin: Commission reviews only; no independent quantitative studies found",
      "The 1993 directive let satellite broadcasters clear rights only in their home country and made cable retransmission rights go through collecting societies. Commission reviews in 2002 and 2016 found these mechanisms eased cross-border TV, but rightholders kept licensing country by country and the rules did not reach online TV, where most broadcasters still geo-block. No independent study measures the effect on access, prices or revenues.",
      indicators, literature)
