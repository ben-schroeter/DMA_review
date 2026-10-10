import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No LFS indicators were extracted from the proposal's financial statement; the memorandum refers to a monitoring programme in Article 83 and the impact assessment (indicators collected by public authorities, providers and the EU Centre), with evaluation five years after entry into force. The proposal was still in trilogue in mid-2026 (fifth trilogue 29 June 2026); voluntary detection continues under the interim Regulation (EU) 2021/1232, which the Commission proposed to extend to April 2028."),
 ind("expected impact (impact assessment)", "More effective detection, reporting and removal of child sexual abuse online; better victim support", "Reports of child sexual abuse; removal; victims identified", "Qualitative: number of reports expected to increase; reduced fragmentation",
     "Not measurable: Regulation not adopted. EPRS complementary IA found tools to detect new material and grooming substantially less accurate than for known material.", "not measured", "SWD(2022) 210; EPRS 2023"),
 ind("expected impact (impact assessment)", "Costs", "Costs to providers, public authorities and EU Centre", "Providers EUR 1.6bn one-off + EUR 1.5bn/yr; public authorities EUR 5.4m one-off + EUR 825.6m/yr; EU Centre EUR 5m one-off + EUR 25.7m/yr",
     "Not measured.", "not measured", "SWD(2022) 210"),
 ind("expected impact (impact assessment)", "Respect for fundamental rights (privacy, data protection)", "", "Safeguards to ensure fair balance and respect prohibition of general monitoring",
     "Contested ex ante: EDPB-EDPS and EPRS concluded detection orders risk generalised scanning and would likely fail the proportionality test for new material and grooming.", "mixed evidence", "EDPB-EDPS 2022; EPRS 2023"),
]
literature = [
 lit("ec-2022-csar-ia", "European Commission", 2022, "Impact assessment accompanying the proposal laying down rules to prevent and combat child sexual abuse (executive summary SWD(2022) 210)", "SWD(2022) 209", EU + "52022SC0210",
     "Commission impact assessment", "ex-ante", "detection and reporting; costs; fundamental rights", "positive (forecast)",
     "Costs: providers EUR 1.6bn one-off and EUR 1.5bn/yr; public authorities EUR 5.4m one-off and EUR 825.6m/yr; EU Centre EUR 5m one-off and EUR 25.7m/yr; benefits described qualitatively (more reports, less fragmentation, better victim support)",
     "The Commission estimated the rules would cost online services about EUR 1.5 billion a year and public authorities about EUR 0.8 billion a year, in return for more detection and reporting of abuse.",
     "EU, forecast", "forecast; benefits not monetised in summary", "full text read"),
 lit("eprs-2023-csar-complementary-ia", "Ecorys, Queen Mary University London et al. for EPRS", 2023, "Proposal for a regulation laying down rules to prevent and combat child sexual abuse: Complementary impact assessment", "EPRS study PE 740.248 (requested by LIBE)", "https://www.europarl.europa.eu/thinktank/en/document/EPRS_STU(2023)740248",
     "Parliament complementary impact assessment", "ex-ante review (legal, technical and cost-benefit analysis)", "detection accuracy; fundamental rights; EU Centre cost-efficiency", "critical",
     "Weaknesses in Commission problem definition (limited treatment of end-to-end encryption); tools for known material accurate, for new material and grooming substantially less accurate; detection orders for new material and grooming would likely fail proportionality test; most cost-efficient EU Centre option is a hybrid with Europol",
     "An independent study for the European Parliament found that scanning for previously unknown abuse images and grooming is too inaccurate and intrusive to be proportionate, and that the Commission underplayed encryption.",
     "EU, 2023", "independent expert review", "full text read", pdf_url="https://edri.org/wp-content/uploads/2023/07/EPRS_STU2023740248_EN.pdf"),
 lit("edpb-edps-2022-csam-opinion", "EDPB & EDPS", 2022, "Joint Opinion 04/2022 on the Proposal for a Regulation laying down rules to prevent and combat child sexual abuse", "EDPB-EDPS Joint Opinion, 28 July 2022", "https://edps.europa.eu/system/files/2022-07/22-07-28_edpb-edps-joint-opinion-csam_en.pdf",
     "regulator opinion", "legal analysis (ex-ante)", "privacy; data protection; confidentiality of communications", "negative (forecast)",
     "Vague conditions for detection orders risk generalised and indiscriminate scanning; substantial degradation of confidentiality of communications; proposal may present more risks to individuals and society than to criminals pursued",
     "Europe's data protection authorities warned the proposal could lead to indiscriminate scanning of private messages and weaken confidentiality for everyone, children included.",
     "EU, 2022", "expert opinion", "page summary via search"),
]
write("52022PC0209", "Child Sexual Abuse Regulation (CSAR, proposal)", "52022PC0209", "SWD(2022) 209 (executive summary SWD(2022) 210)",
      "ex-ante only and contested: Commission IA cost forecasts versus critical Parliament complementary IA and regulators' opinion; proposal still in trilogue",
      "The Commission estimated its child sexual abuse proposal would cost online services about EUR 1.5 billion a year and public authorities about EUR 0.8 billion, in exchange for more detection and reporting of abuse. A study for the European Parliament and Europe's data protection authorities found that scanning for new abuse material and grooming is too inaccurate and intrusive to be proportionate. The law was still being negotiated in 2026, so there is no evidence of its effects.",
      indicators, literature)
