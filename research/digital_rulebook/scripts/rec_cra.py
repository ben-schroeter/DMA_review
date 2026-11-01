import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("LFS indicator", "Secure products throughout their life cycle", "Significant incidents caused by vulnerabilities; share of manufacturers with secure development life cycle; patch frequency and time-to-patch", "",
     "Reporting obligations apply from Sept 2026 and main requirements from Dec 2027; no measurement yet. A 2025 survey found most open-source respondents unfamiliar with the Act and few manufacturers producing SBOMs.", "not measured", "Lawson & Hendrick 2025"),
 ind("LFS indicator", "Coherent framework", "Absence of product-specific national cybersecurity legislation", "", "Not assessed.", "not measured", ""),
 ind("LFS indicator", "Transparency and secure use", "Share of products shipped with security information and secure-use instructions", "", "Not measured.", "not measured", ""),
 ind("expected impact (impact assessment)", "Fewer cyber incidents", "Reduction in incident costs for businesses", "EUR 180-290bn a year",
     "Not evaluated; Commission report due 36 months after application.", "not measured", "SWD(2022) 283"),
 ind("expected impact (impact assessment)", "Compliance costs", "Aggregate compliance costs for manufacturers", "up to ~EUR 29bn (market value up to EUR 1,485bn)", "Not measured.", "not measured", "SWD(2022) 283"),
]
literature = [
 lit("ec-2022-cra-ia", "European Commission", 2022, "Impact Assessment accompanying the Cyber Resilience Act proposal (executive summary SWD(2022) 283)", "SWD(2022) 282", EU + "52022SC0283",
     "Commission impact assessment", "ex-ante", "incident costs; compliance costs; prices", "positive (forecast)",
     "Incident costs for businesses reduced by roughly EUR 180-290bn a year; compliance costs up to about EUR 29bn; possible higher prices for users; SMEs more affected as manufacturers",
     "The Commission expected the Act to cut the cost of cyber incidents for firms by EUR 180-290 billion a year, against compliance costs of up to EUR 29 billion.",
     "EU, forecast", "forecast", "full text read"),
 lit("lawson-hendrick-2025-cra", "Lawson & Hendrick", 2025, "Unaware and Uncertain: The Stark Realities of Cyber Resilience Act Readiness in Open Source", "Linux Foundation Research (with OpenSSF and LF Europe)", "https://www.linuxfoundation.org/research/cra-readiness",
     "industry survey report", "survey (descriptive)", "awareness; readiness; SBOM use", "negative (readiness gaps)",
     "Most respondents unfamiliar with the CRA (62% not at all or only slightly familiar), uncertain about deadlines and penalties; manufacturers rely passively on upstream fixes and few produce SBOMs; calls for funding, legal support and clear guidance",
     "A 2025 survey of the open-source community found most people knew little about the Act and many manufacturers were not ready.",
     "global open-source community, 2024-25", "non-random survey", "abstract read",
     interested_party="Linux Foundation and OpenSSF represent open-source projects and member companies directly affected by the CRA"),
]
write("32024R2847", "Cyber Resilience Act", "52022PC0454", "SWD(2022) 282 (executive summary SWD(2022) 283)",
      "ex-ante only: obligations apply 2026-27; one readiness survey by an interested party",
      "The Commission forecast that mandatory security rules for connected products and software would cut the cost of cyber incidents for businesses by EUR 180-290 billion a year, against compliance costs of up to EUR 29 billion. The main requirements apply only from December 2027. An open-source industry survey in 2025 found low awareness and readiness, but no study has measured effects on security or costs.",
      indicators, literature)
