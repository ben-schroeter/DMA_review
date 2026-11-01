import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The DSA proposal's financial statement contains no indicators section; monitoring was left to the Commission's evaluation under Article 91"),
 ind("expected impact (impact assessment)", "Single market", "Cross-border digital trade +1-1.8%", "+1-1.8%", "Not evaluated.", "not measured", "SWD(2020) 349"),
 ind("expected impact (impact assessment)", "Safety and fundamental rights", "Better protection of users and fundamental rights online; effective supervision", "",
     "Enforcement under way: first non-compliance decision fined X EUR 120m (5 Dec 2025) for misleading verification, deficient ad repository and blocking researcher data access; other investigations ongoing. Transparency database operational but platform self-reports inconsistent.", "reported as activity", "Commission decision Dec 2025; Kaushal et al.; Trujillo et al."),
 ind("expected impact (impact assessment)", "Competition", "Asymmetric rules boost smaller competitors", "", "No evidence found.", "not measured", ""),
]
literature = [
 lit("ec-2020-dsa-ia", "European Commission", 2020, "Impact Assessment accompanying the DSA proposal (executive summary SWD(2020) 349)", "SWD(2020) 348", EU + "52020SC0349",
     "Commission impact assessment", "ex-ante", "cross-border trade; compliance costs", "positive (forecast)",
     "Cross-border digital trade expected to rise 1-1.8%; direct costs proportionate to size and reach; less legal fragmentation", "The Commission expected the DSA to raise cross-border digital trade by 1-1.8% by replacing diverging national rules.",
     "EU, forecast", "forecast", "full text read"),
 lit("ec-2025-x-dsa-fine", "European Commission", 2025, "First DSA non-compliance decision: X fined EUR 120 million", "Decision of 5 December 2025 (as reported by eucrim)", "https://eucrim.eu/news/eu-fines-x-120-million-in-first-dsa-non-compliance-decision/",
     "Commission enforcement (secondary report)", "enforcement record", "sanctions", "n/a",
     "EUR 120m for deceptive 'blue checkmark' verification, inadequate advertising repository and refusing researchers access to public data", "The first DSA fine: EUR 120 million against X for misleading verification badges, an incomplete ad library and blocking researchers.",
     "EU", "secondary report of Commission decision", "page summary via search"),
 lit("kaushal-et-al-2024", "Kaushal, van de Kerkhof, Goanta, Spanakis & Iamnitchi", 2024, "Automated Transparency: A Legal and Empirical Analysis of the Digital Services Act Transparency Database", "ACM FAccT 2024 (arXiv 2404.02894)", "https://arxiv.org/abs/2404.02894",
     "peer-reviewed (conference)", "descriptive (sample of 131m statements of reasons, Nov 2023)", "transparency; content moderation", "mixed",
     "Some transparency gains, but compliance problematic because the database lets platforms exercise wide discretion; terms-of-service grounds dominate over illegal content", "The DSA's public database of moderation decisions adds some transparency, but platforms report so inconsistently that it is hard to rely on.",
     "EU, Nov 2023", "descriptive; early period", "abstract read", pdf_url="https://arxiv.org/pdf/2404.02894"),
 lit("trujillo-fagni-cresci-2023", "Trujillo, Fagni & Cresci", 2023, "The DSA Transparency Database: Auditing Self-reported Moderation Actions by Social Media", "arXiv 2312.10269", "https://arxiv.org/abs/2312.10269",
     "working paper", "descriptive (all 353m records from 8 largest platforms, first 100 days)", "transparency; content moderation", "mixed",
     "Platforms adhered only in part to the database's structure; structure partly inadequate; large cross-platform differences; database contents inconsistent with platforms' own transparency reports", "An audit of 353 million moderation records found the big platforms only partly comply with the DSA database and that their submissions contradict their own reports.",
     "EU, Sept-Dec 2023", "descriptive", "abstract read", pdf_url="https://arxiv.org/pdf/2312.10269"),
]
write("32022R2065", "Digital Services Act", "52020PC0825", "SWD(2020) 348 (executive summary SWD(2020) 349)",
      "thin: no promised indicators; enforcement record and descriptive transparency studies only; no causal evidence on economic or safety outcomes",
      "The DSA set no monitoring indicators, and its forecast 1-1.8% boost to cross-border digital trade has not been evaluated. Enforcement has begun - X was fined EUR 120m in December 2025 - and the new transparency database has made moderation more visible, but audits of hundreds of millions of records show platforms report inconsistently. No study yet measures the DSA's effect on illegal content, users' safety or the platform economy.",
      indicators, literature)
