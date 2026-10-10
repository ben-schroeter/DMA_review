import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2012 LED proposal (COM(2012) 10) has no financial-statement indicators; monitoring relies on four-yearly Commission reports under Article 62 (first 2022, second due 2026)"),
 ind("evaluation question", "Harmonised, high level of protection in policing and criminal justice", "Transposition and conformity of national laws", "Deadline 6 May 2018",
     "Two-thirds of Member States missed the deadline; infringement cases against 19 Member States (2018), later one against Germany (2022). Transposition complete by 2019-2022 but gaps on storage limits, legal basis and supervisory powers.",
     "measured", "COM(2022) 364"),
 ind("evaluation question", "Effective rights for individuals", "Complaints and supervisory activity", "",
     "More than a third of supervisory authorities reported more complaints; most inadmissible, some led to erasure/rectification orders; representative complaints rarely used. Council (2025) finds DPOs improved awareness but access requests and DPIAs burdensome.",
     "reported as activity", "COM(2022) 364; Council ST 15616/25"),
 ind("evaluation question", "Facilitate exchange of data between law-enforcement authorities", "Volume/ease of cross-border data exchange", "",
     "Not measured; Council reports international transfer rules (Art. 37) hard to use in practice.", "not measured", "Council ST 15616/25"),
]
literature = [
 lit("ec-2012-dp-reform-ia", "European Commission", 2012, "Impact Assessment for the data protection reform package (GDPR and Law Enforcement Directive), executive summary", "SEC(2012) 73 (full IA SEC(2012) 72)", EU + "52012SC0073",
     "Commission impact assessment", "ex-ante", "legal certainty; protection of individuals; police cooperation", "positive (forecast)",
     "Shared IA with the GDPR; for policing it identified fragmented rules under the 2008 Framework Decision and legal uncertainty for individuals and authorities; no quantified forecast for the LED",
     "The Commission's joint impact assessment argued that a single directive would end patchy data protection rules for police and courts, but gave no figures for this part.",
     "EU, forecast", "forecast; qualitative for LED", "full text read (executive summary)"),
 lit("ec-2022-led-report", "European Commission", 2022, "First report on application and functioning of the Data Protection Law Enforcement Directive (EU) 2016/680", "COM(2022) 364", EU + "52022DC0364",
     "Commission review report", "transposition analysis, Member State and supervisory authority input, external study", "transposition; complaints; supervisory resources", "mixed",
     "Two-thirds of Member States late; 19 infringement procedures; transposition satisfactory overall with gaps; complaints rising; limited experience to judge effects",
     "The first review found most countries implemented the rules late and with gaps, and it was too early to judge their real effect.",
     "EU, 2018-2022", "descriptive; early", "full text read (relevant sections)"),
 lit("council-2025-led-findings", "Council of the European Union", 2025, "Council position and findings on the evaluation and review of the Law Enforcement Directive (LED)", "Council document ST 15616/25", "https://data.consilium.europa.eu/doc/document/ST-15616-2025-INIT/en/pdf",
     "Member State position paper", "Member State observations (input to 2026 Commission review)", "administrative burden; international transfers; DPOs", "mixed",
     "Harmonised framework welcomed; DPOs improved awareness and compliance; DPIAs, broad access requests and international-transfer rules perceived as burdensome",
     "Member States say the directive brought consistent rules and better data-protection awareness in police forces, but some obligations are burdensome in practice.",
     "EU, 2022-2025", "views of the regulated authorities", "full text read (parts)", interested_party="Member State governments (whose police and justice authorities are the regulated parties)"),
]
write("32016L0680", "Law Enforcement Directive", "52012PC0010", "SEC(2012) 72 (executive summary SEC(2012) 73), shared with GDPR",
      "thin: transposition and complaint statistics only; no independent or causal evidence on protection outcomes or law-enforcement effectiveness found",
      "The Law Enforcement Directive, which sets data protection rules for police and criminal courts, came with no monitoring indicators. The Commission's 2022 review found two-thirds of countries implemented it late and with gaps, and that complaints are rising; Member States say it improved awareness but some duties are burdensome. No study measures whether it actually changed how police handle personal data; a second Commission review is due in 2026.",
      indicators, literature)
