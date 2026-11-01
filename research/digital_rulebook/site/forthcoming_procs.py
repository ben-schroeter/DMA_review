"""Procedure data for the Forthcoming pages. Parliament data come from the Legislative Observatory (OEIL) procedure files,
saved in site/forthcoming_oeil.json (refresh with /tmp/oeil_parse.py or by re-fetching the procedure files). Council data
are entered by hand from Council press releases and documents (OEIL carries none). Status as of October 2026."""

PROC = {
 "digital-omnibus": ["2025/0360(COD)"], "business-wallet": ["2025/0358(COD)"], "digital-networks-act": ["2026/0013(COD)"],
 "cybersecurity-act-2": ["2026/0011(COD)", "2026/0012(COD)"], "eu-inc": ["2026/0074(COD)"], "cloud-ai-development-act": ["2026/0138(COD)"],
 "chips-act-2": ["2026/0139(COD)"], "european-innovation-act": ["2026/0264(COD)"], "euccs": ["2026/0301(COD)"],
 "multimodal-digital-mobility": ["2026/0113(COD)"], "single-digital-booking": ["2026/0115(COD)", "2026/0114(COD)"],
 "european-product-act": ["2026/0307(COD)"], "eu-kids-act": ["2026/0286(COD)"], "omnibus-iv": ["2025/0130(COD)", "2025/0131(COD)", "2025/0133(COD)", "2025/0134(COD)"],
 "digital-euro": ["2023/0212(COD)"], "fida": ["2023/0205(COD)"], "csar": ["2022/0155(COD)"], "digital-travel": ["2024/0670(COD)"],
 "space-act": ["2025/0335(COD)"], "infosec": ["2022/0084(COD)"], "late-payment": ["2023/0323(COD)"], "psr": ["2023/0210(COD)"],
 "psd3": ["2023/0209(COD)"], "csa-directive": ["2024/0035(COD)"],
}
# Council: (date, what, reference, url, kind) with kind "mandate" (Council position), "agreement", or "note"
COUNCIL = {
 "digital-euro": [("19 Dec 2025", "Council negotiating position on the digital euro and the legal tender of cash", "Press release",
                   "https://www.consilium.europa.eu/en/press/press-releases/2025/12/19/single-currency-council-agrees-position-on-the-digital-euro-and-on-strengthening-the-role-of-cash/", "mandate")],
 "digital-omnibus": [("21 Oct 2026", "Council negotiating mandate agreed in Coreper (reported)", "ST 14756/26", "", "mandate")],
 "digital-networks-act": [("21 May 2026", "Presidency progress report", "ST 8523/26", "https://data.consilium.europa.eu/doc/document/ST-8523-2026-INIT/en/pdf", "note"),
                          ("9 Jun 2026", "Policy debate at the Telecoms Council", "ST 9685/26", "https://data.consilium.europa.eu/doc/document/ST-9685-2026-INIT/en/pdf", "note")],
 "psr": [("18 Jun 2025", "Council negotiating mandate", "", "", "mandate"),
         ("Nov 2025", "Provisional agreement with Parliament", "EP press release", "https://www.europarl.europa.eu/news/en/press-room/20251121IPR31540/payment-services-deal-more-protection-from-online-fraud-and-hidden-fees", "agreement")],
 "psd3": [("18 Jun 2025", "Council negotiating mandate", "", "", "mandate"),
          ("Nov 2025", "Provisional agreement with Parliament", "EP press release", "https://www.europarl.europa.eu/news/en/press-room/20251121IPR31540/payment-services-deal-more-protection-from-online-fraud-and-hidden-fees", "agreement")],
 "digital-travel": [("19 Nov 2025", "Council negotiating mandate", "", "", "mandate")],
 "csar": [("26 Nov 2025", "Council position, without mandatory detection orders", "", "", "mandate")],
 "csa-directive": [("", "Council general approach", "", "", "mandate"), ("22 Jun 2026", "Provisional agreement with Parliament", "", "", "agreement")],
 "omnibus-iv": [("", "Council mandates", "", "", "mandate"), ("Jun 2026", "Provisional agreement with Parliament", "", "", "agreement")],
 "fida": [("", "Council position agreed; trilogues stalled since October 2025", "", "", "mandate")],
 "late-payment": [("", "No Council position: the file is blocked in Council", "", "", "note")],
}
# extra preparatory documents for announced initiatives: (date, title, ref, url)
PREP = {
 "quantum-act": [("Jul 2025", "Quantum Europe Strategy", "COM(2025) 363", "https://digital-strategy.ec.europa.eu/en/library/quantum-europe-strategy"),
                 ("Oct 2025", "Call for evidence for the impact assessment (closed 15 Dec 2025)", "Have your say", "https://digital-strategy.ec.europa.eu/en/news/commission-invites-contributions-shape-future-eu-quantum-act")],
 "avmsd-revision": [("Nov 2025", "Call for evidence for the evaluation (closed 21 Dec 2025)", "Have your say", ""),
                    ("Feb 2026", "Public consultation on the evaluation and review options", "Have your say", "")],
 "smbpa": [("May 2025", "Single Market Strategy: our European home market in an uncertain world", "COM(2025) 500", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025DC0500")],
}
# Omnibus proposals: provisions changed in laws on our list, counted from the amending instructions of the Commission proposals
OMNIBUS = {
 "digital-omnibus": dict(source="COM(2025) 837, Articles 1 to 10", changes=[
     (76, "Data Act", 23, 6, 17), (20, "General Data Protection Regulation", 4, 3, 11), (35, "Data protection by EU institutions Regulation", 5, 1, 7),
     (9, "ePrivacy Directive", 0, 1, 1), (61, "NIS 2 Directive", 2, 0, 2), (22, "eIDAS Regulation", 0, 0, 3), (57, "Digital Operational Resilience Act (DORA)", 2, 0, 0),
     (36, "Single Digital Gateway Regulation", 1, 0, 0)],
     repeals=[(44, "Platform-to-Business (P2B) Regulation", "repealed; Articles 2(1), 2(2), 2(5), 4, 11 and 15 apply until 31 December 2032"),
              (58, "Data Governance Act", "repealed; its rules move into the Data Act"), (38, "Free Flow of Non-Personal Data Regulation", "repealed; its rules move into the Data Act"),
              (43, "Open Data Directive (PSI)", "repealed; its rules move into the Data Act")],
     other="It also amends the Critical Entities Resilience Directive, which is not on our list."),
 "omnibus-iv": dict(source="COM(2025) 501 to 504 (the Commission proposals; the agreed texts may differ)", changes=[
     (20, "General Data Protection Regulation", 3, 0, 1), (65, "Machinery Regulation", 12, 0, 4), (80, "Ecodesign for Sustainable Products Regulation", 6, 0, 1),
     (109, "Electromagnetic Compatibility Directive", 10, 0, 5), (110, "Radio Equipment Directive", 11, 2, 5)],
     repeals=[], other="It also amends about 20 other product, financial and trade laws that are not on our list."),
}
