"""Build data/company_responses/law_patterns_all.json: text patterns for every adopted law in the database.

For each law (digital_rulebook.xlsx, sheet 'instruments', status 'adopted'):
  - its official number in the forms companies write it ('2016/679', 'Directive 2000/31/EC',
    'Regulation (EC) No 139/2004'); old-style numbers such as 1/2003 only after 'Regulation (EC)'
    so that dates are not matched;
  - its name in the database and the curated names and abbreviations in NAMES below
    (English, plus French/German/Italian/Spanish/Dutch names for the laws companies cite most);
  - abbreviations that also mean other things count only in reports that use one of the law's
    full names and do not define the abbreviation otherwise (CONFLICTS).
Mentions in reports for years before a law's proposal (min_year) are not counted, and official
numbers inside an 'amending ...' clause of another act's title are ignored (cr_code.match_law).
The three pilot laws (GDPR, DMA, AI Act) keep their validated patterns from law_patterns.json,
and the UK / non-EU entries are carried over (logged separately, never counted as EU).
"""
import json, os, re
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "data", "company_responses", "law_patterns_all.json")
PILOT = os.path.join(ROOT, "data", "company_responses", "law_patterns.json")
PILOT_ROWS = {20: "GDPR", 59: "DMA", 64: "AI_ACT"}
COUNTRY_BEFORE = r"(?i)(US|U\.S\.|United States|UK|U\.K\.|United Kingdom|British|Japan(ese)?|Korea(n)?|China|Chinese|India(n)?|Australia(n)?|Canada|Canadian|Singapore|California|Colorado|Texas|state|federal)['’]?s?\s*$"

# row_id: (names [regex, case-sensitive unless (?i)], abbreviations [only with a full name in the report], conflicts)
NAMES = {
    1: (["GSM Directive", "Frequency Bands Directive"], [], []),
    2: (["Unfair (Contract )?Terms Directive", "Directive on [Uu]nfair [Tt]erms in [Cc]onsumer [Cc]ontracts"], [], []),
    3: (["Satellite and Cable Directive", "Cable and Satellite Directive"], [], []),
    4: (["Database Directive", "Directive on the legal protection of databases"], [], []),
    5: (["Community Designs? Regulation", "Community Design Regulation"], [], []),
    6: (["Price Indication Directive"], [], []),
    7: (["InfoSoc Directive", "Information Society Directive", "Copyright and Related Rights in the Information Society"], [r"\bInfoSoc\b"], []),
    8: (["(?i)e-?commerce directive", "Electronic Commerce Directive", "(?i)directive (on|sur le) (electronic commerce|commerce électronique)"], [], []),
    9: (["(?i)e-?privacy directive", "Privacy and Electronic Communications Directive", "Cookie Directive", "(?i)directive vie privée et communications électroniques"], [], []),
    10: (["Radio Spectrum Decision"], [], []),
    11: (["(EC|EU) Merger Regulation", "European Merger Regulation", "Merger Regulation"], [r"\bEUMR\b", r"\bECMR\b"], []),
    12: (["(IPR?|Intellectual Property( Rights)?) Enforcement Directive"], [r"\bIPRED\b"], []),
    13: (["Unfair Commercial Practices Directive", "(?i)directive (sur les|relative aux) pratiques commerciales déloyales"], [r"\bUCPD\b"], []),
    14: (["(EU |Common |Principal )?VAT Directive", "Common (System of )?VAT (System )?Directive", "Directive on the common system of value added tax"], [], []),
    15: (["Audiovisual Media Services Directive", "AVMS Directive", "(?i)directive (sur les )?services de médias audiovisuels"], [r"\bAVMSD\b"], []),
    17: (["Toys? Safety Directive"], [], []),
    18: (["Consumer Rights Directive", "(?i)directive (relative aux|sur les) droits des consommateurs"], [], []),
    19: (["DAC ?[5-9]\\b", "Directive on Administrative Cooperation", "Administrative Cooperation Directive"], [r"\bDAC\b"], [r"(?i)\bDAC\b\W{0,5}(design|digital[- ]to[- ]analog|converter)"]),
    21: (["Law Enforcement Directive", "Police (and Criminal Justice )?Directive"], [], []),
    22: (["eIDAS( 2(\\.0)?)?( Regulation)?", "Regulation on electronic identification and trust services", "European Digital Identity (Framework|Regulation|Wallet)"], [], []),
    23: (["PSD ?2\\b", "(Second|Revised) Payment Services Directive", "Payment Services Directive(?! ?3| \\(PSD3\\))", "(?i)deuxième directive (sur|concernant) les services de paiement", "(?i)directive sur les services de paiement"], [], []),
    24: (["Open Internet (Access )?Regulation", "(EU )?Net Neutrality Regulation", "Telecoms Single Market Regulation"], [], []),
    25: (["Technology Transfer Block Exemption( Regulation)?"], [r"\bTTBER\b"], []),
    26: (["Trade Secrets? Directive"], [], []),
    27: (["Digital Content (and Digital Services )?Directive"], [], []),
    28: (["Sale of Goods Directive"], [], []),
    29: (["Company Law Directive", "Directive relating to certain aspects of company law"], [], []),
    30: (["Geo-?blocking Regulation", "(?i)geo-?blocking regulation"], [], []),
    31: (["Consumer Protection Cooperation Regulation", "CPC Regulation"], [], []),
    32: (["European Electronic Communications Code", "(?i)code des communications électroniques européen", "(?i)Europäische[nr]? Kodex für die elektronische Kommunikation", "(?i)codice europeo delle comunicazioni elettroniche"], [r"\bEECC\b"], []),
    33: (["Copyright (in the )?Digital Single Market Directive", "Directive on [Cc]opyright (and related rights )?in the Digital Single Market", "DSM (Copyright )?Directive", "(EU |European )?Copyright Directive"], [], []),
    34: (["Satellite and Cable II Directive", "Online Broadcasting Directive"], [], []),
    35: (["Data protection by EU institutions", "EU ?DPR\\b"], [], []),
    36: (["Single Digital Gateway"], [], []),
    37: (["(EU |European )?Cybersecurity Act(?! of)"], [], []),
    38: (["Free Flow of Non-Personal Data", "Non-Personal Data Regulation"], [], []),
    39: (["FDI Screening Regulation", "(EU |European )?Foreign Direct Investment Screening Regulation", "(EU|European) FDI (screening )?(Regulation|framework)"], [], []),
    40: (["Non-cash payment fraud Directive", "Directive on combating fraud and counterfeiting of non-cash means of payment"], [], []),
    41: (["Market Surveillance Regulation"], [], []),
    42: (["E-[Ee]vidence (Regulation|package)", "e-Evidence Regulation"], [], []),
    43: (["Open Data Directive", "PSI Directive", "Public Sector Information Directive"], [], []),
    44: (["P2B Regulation", "Platform[- ]to[- ]Business Regulation", "Platform-to-Business \\(P2B\\)", "(?i)règlement platform to business"], [r"\bP2B\b"], []),
    51: (["Terrorist Content Online Regulation", "TCO Regulation", "Regulation on addressing the dissemination of terrorist content online"], [r"\bTERREG\b"], []),
    53: (["Interim (ePrivacy )?Derogation", "Temporary (CSAM )?Derogation"], [], []),
    55: (["DLT Pilot Regime", "DLT Pilot Regulation"], [], []),
    56: (["Markets in Crypto-?[Aa]ssets( Regulation)?", "MiCA ?R?\\b", "(?i)règlement sur les marchés de crypto-actifs"], [], []),
    57: (["Digital Operational Resilience Act", "(?i)règlement sur la résilience opérationnelle numérique", "(?i)Verordnung über die digitale operationale Resilienz"], [r"\bDORA\b"], [r"(?i)DevOps|DORA metrics|DevOps Research"]),
    58: (["Data Governance Act"], [r"\bDGA\b"], []),
    60: (["Digital Services Act", "(?i)règlement sur les services numériques", "(?i)législation sur les services numériques", "Gesetz über digitale Dienste", "(?i)regolamento sui servizi digitali", "(?i)reglamento de servicios digitales", "(?i)ley de servicios digitales"], [r"\bDSA\b"], [r"(?i)digital signature algorithm|data sharing agreement|\bDSA\b\W{0,5}(defen[cs]e|security assistance)"]),
    61: (["NIS ?2\\b", "NIS2 Directive", "(Second|Revised) NIS Directive", "Directive on measures for a high common level of cybersecurity", "NIS-2"], [], []),
    63: (["(EU |European )?Roaming Regulation", "Roam[- ]like[- ](at[- ])?[Hh]ome"], [], []),
    65: (["Machinery Regulation", "(EU |European )?Machinery Products Regulation"], [], []),
    66: (["Foreign Subsidies Regulation", "(?i)règlement (sur les|relatif aux) subventions étrangères"], [r"\bFSR\b"], [r"(?i)\bFSR\b\W{0,5}(funding|federal|financial strength)"]),
    67: (["General Product Safety Regulation"], [r"\bGPSR\b"], []),
    68: (["(EU |European )?Anti-Money Laundering Regulation(?! ?s| 20)", "AMLR\\b", "Single Rulebook Regulation"], [], []),
    69: (["Vertical Block Exemption Regulation", "VBER\\b", "Verticals? Block Exemption"], [], []),
    70: (["Digital Decade Policy Programme", "Path to the Digital Decade"], [], []),
    71: (["Political Advertising Regulation", "Regulation on the transparency and targeting of political advertising", "TTPA\\b"], [], []),
    73: (["Platform Work Directive", "Directive on improving working conditions in platform work"], [], []),
    74: (["(European|EU) Chips Act", "Chips Act \\(EU\\)", "(?i)européen sur les semi-conducteurs"], [], []),
    76: (["(?:EU|European Union|EU['’]s|European|[Tt]he) Data Act(?! [0-9]{4})(?! of)", "Data Act \\((?:EU|Regulation)", "(?i)règlement (européen )?sur les données", "Datenverordnung", "(?i)regolamento (europeo )?sui dati"], [], []),
    77: (["Directive on combating violence against women"], [], []),
    80: (["Ecodesign for Sustainable Products Regulation", "ESPR\\b", "(EU )?Digital Product Passport"], [], []),
    81: (["European Health Data Space", "EHDS\\b"], [], []),
    83: (["Cyber Resilience Act", "(?i)règlement sur la cyber-?résilience", "Cyberresilienzgesetz", "Cyber-Resilienz-Verordnung"], [r"\bCRA\b"], [r"(?i)Community Reinvestment Act|Canada Revenue Agency|\bCRA\b\W{0,5}(rating|exam)"]),
    84: (["European Media Freedom Act", "EMFA\\b"], [], []),
    86: (["(New |Revised |EU |European )?Product Liability Directive"], [], []),
    87: (["Horizontal Block Exemption Regulations?", "HBERs?\\b", "R&D Block Exemption", "Specialisation Block Exemption"], [], []),
    89: (["Design Directive", "(EU )?Design (Legislation|Reform) Package"], [], []),
    90: (["VAT in the Digital Age", "ViDA\\b"], [], []),
    91: (["Gigabit Infrastructure Act", "Broadband Cost Reduction Directive"], [r"\bGIA\b"], []),
    94: (["Right to Repair Directive", "(EU |European )?Right to Repair"], [], []),
    102: (["GDPR Procedural Regulation", "GDPR Enforcement Procedur(e|al) Regulation"], [], []),
    103: (["Toys? Safety Regulation"], [], []),
    108: (["(European )?Standardi[sz]ation Regulation"], [], []),
    109: (["Electromagnetic Compatibility Directive", "EMC Directive"], [], []),
    110: (["Radio Equipment Directive", "\\bRED Directive", "Radio Equipment Directive \\(RED\\)"], [], []),
    111: (["E-?[Ii]nvoicing Directive", "Directive on electronic invoicing in public procurement"], [], []),
    112: (["Portability Regulation", "Cross-[Bb]order Portability Regulation"], [], []),
    113: ([r"\.eu Top[- ]Level Domain", r"\.eu Regulation"], [], []),
    115: (["Short-[Tt]erm [Rr]ental (Data )?Regulation", "STR Regulation"], [], []),
    116: (["Radio Spectrum Policy Programme", "RSPP\\b"], [], []),
    117: (["700 MHz Decision"], [], []),
    118: (["TRIS Directive", "Single Market Transparency Directive", "Technical Regulations Information System"], [], []),
    119: (["European Accessibility Act", "(?i)acte européen sur l['’]accessibilité", "Barrierefreiheitsstärkungsgesetz", "(?i)European Accessibility Directive"], [], []),
    120: (["Software Directive", "Computer Programs Directive", "Directive on the legal protection of computer programs"], [], []),
    121: (["Collective Rights Management Directive", "Collective Management Directive"], [], []),
    122: (["Conditional Access Directive"], [], []),
    123: (["ADR Directive", "Alternative Dispute Resolution Directive", "Directive on consumer ADR"], [], []),
    124: (["Representative Actions Directive", "(EU )?Collective Redress Directive", "Directive on representative actions"], [], []),
    125: (["E-?[Mm]oney Directive", "Electronic Money Directive", "EMD ?2\\b", "Second E-?[Mm]oney Directive"], [], []),
    126: (["SEPA Regulation", "SEPA End-?[Dd]ate Regulation", "Instant Payments Regulation"], [], []),
    127: (["(Revised |EU )?Transfer of Funds Regulation", "Funds Transfer Regulation", "Wire Transfer Regulation"], [], []),   # 'TFR' = Italian severance pay
    128: (["Consumer Credit Directive", "CCD ?2\\b"], [], []),
    129: (["European Single Access Point"], [r"\bESAP\b"], [r"(?i)Executive Separation"]),
    130: (["Cybercrime Directive", "Directive on attacks against information systems"], [], []),
    131: (["Child Sexual Abuse Directive", "Directive on combating the sexual abuse and sexual exploitation of children"], [], []),
    132: (["Regulation 1/2003", "Modernisation Regulation", "Antitrust Procedure Regulation"], [], []),
    133: (["(EU|European|Single Market) Services Directive", "Bolkestein Directive", "Directive on services in the internal market"], [], []),
    134: (["(EU |European )?Medical Devices? Regulation", "EU MDR\\b", "MDR \\(EU\\)"], [], []),
    135: (["In[- ][Vv]itro Diagnostic( Medical Devices)? Regulation", "IVDR\\b"], [], []),
    136: (["(Vehicle )?General Safety Regulation", "GSR ?2\\b"], [], []),
    137: (["(EU |European )?Dual-[Uu]se Regulation", "(EU|European) [Dd]ual-[Uu]se (export )?(controls?|regime)"], [], []),
    138: (["Low Voltage Directive"], [], []),   # 'LVD' is also a company name
    139: (["RoHS( ?[23])?( Directive)?"], [], []),
    140: (["WEEE( 2)? Directive", "EU WEEE", "Directive (on )?(WEEE|[Ww]aste (from |of )?[Ee]lectrical and [Ee]lectronic [Ee]quipment)", "[Ww]aste (from |of )?[Ee]lectrical and [Ee]lectronic [Ee]quipment \\(WEEE\\) Directive", "(?i)directive DEEE"], [], []),   # bare 'WEEE' is also the waste category
    141: (["(Fourth|Fifth|4th|5th) Anti-?[Mm]oney[- ][Ll]aundering Directive", "(4|5|6)AMLD\\b", "AMLD ?[456]\\b", "(EU |European )?Anti-Money Laundering Directive"], [], []),
}
# names that also match narrower or broader things: reject if the preceding text matches
NOT_BEFORE = {
    133: r"(?i)(Payment|Media|Audiovisual|Digital|Financial|Investment|Markets in Financial Instruments|Insurance|Postal|Payment Services|Mortgage Credit|Credit|Information Society)\s*$",
    136: r"(?i)(Product|Consumer|Vehicle General)\s*$",
    37: COUNTRY_BEFORE, 76: COUNTRY_BEFORE + r"|(Use and Access|Protection|Personal|Privacy)\)?\s*$",
    86: COUNTRY_BEFORE, 74: COUNTRY_BEFORE, 139: r"(?i)(China|Chinese|Korea|India|UAE)\s*$", 140: r"(?i)(UK|China|Chinese)\s*$",
    11: r"(?i)(UK|national)\s*$", 14: r"(?i)(UK|national)\s*$",
}
NOT_AFTER = {37: r"^\s*(of|20\d\d)", 76: r"^\s*(\(|of|20\d\d)", 68: r"^s?\s*(20\d\d)"}


def number_patterns(ident):
    pats = []
    for m in re.finditer(r"(Regulation|Regulations|Directive|Decision)?\s*(?:\((?:EU|EC|EEC)\)\s*)?(?:No\.?\s*)?(\d{1,4})/(\d{1,4})(/(?:EU|EC|EEC))?", ident or ""):
        kind, a, b, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
        if len(a) == 4:                       # new style 2016/679
            pats.append(rf"(?<![\d/]){a}/{b}(?![\d/])")
        elif suffix:                          # 2000/31/EC, 96/9/EC
            pats.append(rf"(?<![\d/]){a}/{b}{suffix}")
        else:                                 # old style 139/2004, 1/2003: only after the act type
            pats.append(rf"(?:Regulation|Decision)\s*(?:\((?:EU|EC)\)\s*)?(?:No\.?\s*)?{a}/{b}(?![\d/])")
    return pats


def min_year(proposal_date):
    """Mentions count from the report year before the Commission proposal (a report for year t is
    published in t+1 and may discuss a proposal made then); earlier matches are predecessors or noise."""
    m = re.search(r"(19|20)\d\d", str(proposal_date or ""))
    return int(m.group(0)) - 1 if m else 0


def main():
    wb = openpyxl.load_workbook(os.path.join(ROOT, "digital_rulebook.xlsx"), read_only=True)
    rows = list(wb["instruments"].iter_rows(values_only=True))
    ix = {k: i for i, k in enumerate(rows[0])}
    pilot = {l["id"]: l for l in json.load(open(PILOT))["laws"]}
    laws, missing = [], []
    for r in rows[1:]:
        if r[ix["status"]] != "adopted":
            continue
        rid, name, ident = r[ix["row_id"]], r[ix["name"]], r[ix["identifier"]]
        if rid in PILOT_ROWS:
            l = dict(pilot[PILOT_ROWS[rid]], row_id=rid, policy_area=r[ix["policy_area"]], min_year=min_year(r[ix["proposal_date"]]))
            laws.append(l)
            continue
        if rid not in NAMES:
            missing.append((rid, name))
        names, abbrev, conflicts = NAMES.get(rid, ([], [], []))
        base = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()          # 'Payment Services Directive 2 (PSD2)' -> name
        full = [re.escape(base)] + list(names) + number_patterns(ident)
        laws.append({"id": f"R{rid}", "row_id": rid, "scope": "eu", "name": name, "identifier": ident, "min_year": min_year(r[ix["proposal_date"]]),
                     "policy_area": r[ix["policy_area"]], "full": list(dict.fromkeys(full)), "abbrev": abbrev,
                     "abbrev_conflicts": conflicts, "not_before": NOT_BEFORE.get(rid, ""), "not_after": NOT_AFTER.get(rid, "")})
    laws += [l for l in pilot.values() if l["scope"] != "eu"]
    json.dump({"_note": "Generated by scripts/cr_law_patterns.py from the database and curated names; see its docstring. "
               "GDPR, DMA and AI Act keep the validated pilot patterns.", "laws": laws},
              open(OUT, "w"), indent=1, ensure_ascii=False)
    print(len([l for l in laws if l["scope"] == "eu"]), "EU laws;", "no curated names for:", missing)


if __name__ == "__main__":
    main()
