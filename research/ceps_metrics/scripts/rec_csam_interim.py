import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No impact assessment (the Commission judged none appropriate given urgency and lack of alternative options) and no LFS indicators; the memorandum says monitoring arrangements are 'not applicable'. The Regulation itself requires provider and Member State statistics (Articles 3 and 8) and Commission implementation reports (Article 9)"),
 ind("legal objective (Regulation)", "Continue voluntary detection and reporting of online child sexual abuse", "Reports of detected CSA; children identified; offenders convicted", "",
     "Member State data incomplete and fragmented; Commission says a comprehensive and reliable overview of reports, children identified and convictions is not possible. Available data show thousands of children identified and millions of images/videos removed.", "partially measured", "COM(2023) 797; COM(2025) 740"),
 ind("legal safeguard (Regulation)", "Accuracy / privacy", "Error ratios (false positives) of detection technologies", "",
     "Providers report aggregate error ratios using different methods: e.g. Google 1.14% (2023) and 0.54% (2024) of hash-matched flags not confirmed on human review; Meta 0.32% and 0.12% of actioned items restored; Microsoft could not calculate. Not comparable.", "partially measured", "COM(2025) 740"),
 ind("legal test (Article 9)", "Proportionality of the derogation", "Balance between child protection and users' privacy", "",
     "Commission: available data insufficient for a definitive answer, though no indications that the derogation is not proportionate; providers gave no information on data protection impact assessments. EDPS (2026) calls for safeguards against general and indiscriminate scanning.", "mixed evidence", "COM(2025) 740; EDPS Opinion 7/2026"),
]
literature = [
 lit("ec-2023-csam-interim-report", "European Commission", 2023, "Report on the implementation of Regulation (EU) 2021/1232 (temporary derogation from the ePrivacy Directive to combat online child sexual abuse)", "COM(2023) 797", EU + "52023DC0797",
     "Commission implementation report", "implementation report (provider and Member State statistics)", "reports; children identified; error rates; data quality", "mixed",
     "Member States reported for differing periods so EU-level totals of reports and identified child victims could not be calculated; large disparities between NCMEC and national figures", "The Commission's first report found national data too patchy to say how many abuse reports or rescued children the voluntary scanning produced.",
     "EU, 2021-2022", "descriptive; poor data", "full text read (key sections)"),
 lit("ec-2025-csam-interim-report", "European Commission", 2025, "Second report on the implementation of Regulation (EU) 2021/1232", "COM(2025) 740", EU + "52025DC0740",
     "Commission implementation report", "implementation report (provider and Member State statistics 2023-2024)", "reports; error rates; proportionality", "mixed",
     "Data still incomplete and not comparable; providers did not use the mandated reporting form; false-positive ratios reported between 0% and 1.14% with inconsistent methods; data insufficient to answer the proportionality question definitively, but thousands of children identified and millions of items removed", "The second Commission report still cannot measure the law's effect reliably, but concludes voluntary scanning helps identify thousands of abused children; error rates reported by platforms are low but calculated inconsistently.",
     "EU, 2023-2024", "descriptive; poor data", "full text read (key sections)"),
 lit("edps-2026-opinion-7", "European Data Protection Supervisor", 2026, "Opinion 7/2026 on the Proposal for a Regulation extending the application of Regulation (EU) 2021/1232", "EDPS Opinion, 16 February 2026", "https://www.edps.europa.eu/data-protection/our-work/publications/opinions/2026-02-16-edps-opinion-72026-regulation-extending-application-regulation-eu-20211232",
     "EU supervisory opinion", "legal opinion", "privacy; proportionality; safeguards", "negative (on safeguards)",
     "Recognises child protection as general-interest objective, but says the extension is the time to address key shortcomings of the interim regime and to ensure effective safeguards against general and indiscriminate scanning", "The EU's data protection watchdog accepts the aim but says the temporary scanning rules still lack safeguards against blanket monitoring of private messages.",
     "EU", "legal analysis", "page summary via search"),
]
write("32021R1232", "Temporary CSAM Derogation Regulation", "52020PC0568", "None (Commission judged an IA not appropriate)",
      "thin: Commission reports say data too incomplete to assess effectiveness or proportionality; no independent study",
      "This temporary law lets messaging services keep voluntarily scanning for child sexual abuse material despite EU privacy rules. Two Commission reports (2023, 2025) say national and platform data are too incomplete to measure its effect reliably, although thousands of children were identified and millions of images removed. Data protection authorities warn safeguards against blanket scanning remain weak.",
      indicators, literature)
