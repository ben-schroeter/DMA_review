import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No impact assessment: the Commission judged one unnecessary because the rules apply only to EU institutions, bodies and agencies. Indicators below are from the proposal's financial statement (1.4.4); progress is reported annually by the Interinstitutional Cybersecurity Board (IICB)"),
 ind("LFS indicator (1.4.4)", "Risk management frameworks", "Frameworks and baselines in place; regular maturity assessments and cybersecurity plans in all Union entities", "",
     "IICB 2025 report: Union entities set up risk-management frameworks and completed maturity and risk assessments; all milestones foreseen for 2025 completed on time. Aggregate maturity scores not published.", "reported as activity", "IICB annual report 2025"),
 ind("LFS indicator (1.4.4)", "Incident handling", "Improved handling of incidents", "Baseline: significant incidents rose more than tenfold 2018-2021",
     "8 significant incidents confirmed for 2025 as of early November, fewer than in 2024; CERT-EU analysed over 800 malicious activities in depth; threat level 'very high'.", "partially measured", "IICB annual report 2025; ECA SR 05/2022"),
 ind("LFS indicator (1.4.4)", "Resources", "Levelling ICT security spending as a share of overall ICT spending", "",
     "No spending share reported; IICB notes an internal assessment that cybersecurity staff would need to rise by about 75% by 2027, which may be hard to achieve.", "not measured", "IICB annual report 2025"),
 ind("LFS indicator (1.4.4)", "Cooperation", "Information sharing and cooperation with ENISA and Member State bodies", "",
     "CERT-EU notified all significant incidents to national counterparts as required; participates in CSIRTs Network.", "reported as activity", "IICB annual report 2025"),
]
literature = [
 lit("eca-2022-euiba-cyber", "European Court of Auditors", 2022, "Cybersecurity of EU institutions, bodies and agencies: Level of preparedness overall not commensurate with the threats", "ECA Special Report 05/2022", "https://op.europa.eu/webpub/eca/special-reports/hack-proofing-eu-institutions-05-2022/en",
     "audit report", "performance audit (baseline)", "cyber preparedness", "negative (baseline)",
     "Preparedness not commensurate with threats; very different maturity levels across bodies; significant incidents up more than tenfold 2018-2021; recommended binding rules and more resources for CERT-EU",
     "Before the regulation, the EU's auditors found EU bodies poorly and unevenly prepared for cyberattacks and called for binding rules - which this regulation introduced.",
     "EU institutions, 2018-2021", "independent audit; pre-regulation baseline", "page summary via search"),
 lit("iicb-2025-annual-report", "Interinstitutional Cybersecurity Board (IICB)", 2025, "IICB Annual Report 2025 on the implementation of Regulation (EU, Euratom) 2023/2841", "IICB, adopted 16 December 2025", "https://www.cert.europa.eu/iicb/annual-report-2025/",
     "official implementation report", "self-reported implementation monitoring", "frameworks; incidents; resources", "positive (activity)",
     "2025 milestones met on time; entities completed maturity and risk assessments; 8 significant incidents to early November 2025 (down from 2024); >800 malicious activities analysed; staffing would need to rise ~75% by 2027",
     "The board overseeing the rules reports that EU bodies met their 2025 deadlines and suffered fewer serious incidents, but warns that threats remain very high and staff are short.",
     "EU institutions, 2025", "self-assessment by the governing body", "full text read"),
]
write("32023R2841", "Cybersecurity Regulation (EU institutions)", "52022PC0122", "None (proposal states an impact assessment was not necessary)",
      "thin: self-reported implementation monitoring plus a pre-regulation audit baseline; no independent assessment of outcomes",
      "This regulation sets common cybersecurity rules for the EU's own institutions and agencies and strengthens their response team, CERT-EU. The board overseeing it reports that all 2025 milestones were met and serious incidents fell to 8 in 2025, though threats remain very high and staff numbers fall short. There is no independent assessment yet of whether EU bodies are actually more secure than when auditors found them poorly prepared in 2022.",
      indicators, literature)
