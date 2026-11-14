"""Impact records for the 16 laws added in the November 2026 scope decision (notes/scope_2026-11.md).
Sources are the Commission's own implementation and evaluation reports and impact assessments, read from the Publications
Office (Cellar) texts; no independent empirical study of the effect of these laws was found in the first search round.
Run from scripts/: python3 rec_scope_2026_11.py"""
import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
NOIND = "No monitoring indicators set in the proposal; assessed through the Commission's reports listed below"


def rec(celex, name, proposal, ia, rating, summary, inds, lits):
    write(celex, name, proposal, ia, rating, summary, inds, lits)


# 1. Radio Spectrum Policy Programme
rec("32012D0243", "Radio Spectrum Policy Programme", "52010PC0471", "SEC(2010) 1034 (summary SEC(2010) 1035)",
    "thin: one Commission implementation report and an audit of 5G roll-out; no study of the programme's own effect",
    "The programme set a target of at least 1200 MHz of spectrum for wireless broadband and a deadline for the 800 MHz band. The Commission's 2014 report found it had helped make harmonised spectrum available, but that its general principles were too vague and that delays in assigning the 800 MHz band showed the need for better-coordinated timing. No independent study of its effect was found.",
    [ind("note", NOIND),
     ind("target in the act", "Spectrum for wireless broadband", "MHz identified for wireless broadband", "at least 1200 MHz by 2015",
         "2014 report: the target promoted spectrum sharing and the spectrum inventory; delays in assigning the 800 MHz band (deadline 1 January 2013) in several Member States.", "partially measured", "COM(2014) 228")],
    [lit("ec-2014-rspp-report", "European Commission", 2014, "Report on the implementation of the Radio Spectrum Policy Programme", "COM(2014) 228", EU + "52014DC0228",
         "Commission implementation report", "implementation report (Member State information)", "spectrum availability; internal market", "mixed",
         "The programme helped make harmonised spectrum available and fostered spectrum sharing, but its general principles were too imprecise and delays in assigning the 800 MHz band fragmented the market",
         "The Commission found the programme useful for freeing spectrum but too general to stop national differences and delays in assigning frequencies.",
         "EU, 2012-2014", "Commission self-assessment", "full text read (conclusions)")])

# 2. 700 MHz Decision
rec("32017D0899", "700 MHz Decision", "52016PC0043", "SWD(2016) 20 (executive summary SWD(2016) 19)",
    "thin: no Commission evaluation yet; an EU audit of 5G roll-out found delays in the Member States",
    "The Decision required Member States to allow wireless broadband in the 700 MHz band by mid-2020 (with up to two years' delay allowed). The impact assessment expected it to support EU-wide connectivity and economies of scale in equipment; it gave no quantified forecast. No Commission evaluation has been published; the European Court of Auditors found considerable delays in 5G roll-out across Member States in 2022.",
    [ind("note", NOIND),
     ind("deadline in the act", "Make the 700 MHz band available for wireless broadband", "Member States allowing use of the band", "by 30 June 2020 (delay up to 2 years for listed reasons)",
         "No Commission compliance report found; the ECA audit (2022) reports delays in 5G deployment generally, not band by band.", "not measured", "ECA Special Report 03/2022")],
    [lit("ec-2016-700mhz-ia", "European Commission", 2016, "Impact Assessment on the use of the 470-790 MHz frequency band in the Union (executive summary)", "SWD(2016) 19 (full IA SWD(2016) 20)", EU + "52016SC0019",
         "Commission impact assessment", "ex-ante", "connectivity; spectrum use; broadcasting", "positive (forecast)",
         "Coordinated release of the 700 MHz band expected to support EU-wide connectivity, avoid interference with broadcasting and gain economies of scale in equipment; preferred option keeps the sub-700 MHz band for broadcasting",
         "The Commission expected a coordinated release of the band to speed up mobile broadband while protecting free-to-air television; it gave no figures.",
         "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
     lit("eca-2022-5g", "European Court of Auditors", 2022, "5G roll-out in the EU: delays in deployment of networks with security issues remaining unresolved", "Special Report 03/2022",
         "https://op.europa.eu/webpub/eca/special-reports/security-5g-networks-03-2022/en",
         "EU audit", "performance audit", "5G deployment; spectrum assignment", "negative",
         "Member States experienced considerable delays in deploying 5G networks; most unlikely to meet the 2025 coverage goal",
         "EU auditors found that 5G networks, for which the 700 MHz band is a key frequency, were being rolled out with considerable delays.",
         "EU, 2016-2021", "audit; not specific to the Decision", "page summary via search")])

# 3. TRIS Directive
rec("32015L1535", "TRIS Directive", "52013PC0932", "codification of Directive 98/34/EC; no impact assessment of its own",
    "thin: Commission operation reports count notifications and reactions; no independent study of the effect on trade barriers",
    "Member States must notify draft technical rules and online-service rules before adopting them. In 2016-2020 the Commission received 3,553 notifications and issued 212 detailed opinions and 816 comments; it considers the procedure effective at preventing barriers, but this rests on activity counts, not on a measure of barriers avoided.",
    [ind("note", NOIND),
     ind("activity (operation report)", "Prevent new technical barriers", "Notifications, detailed opinions and comments", "",
         "2016-2020: 3,553 notifications; 212 detailed opinions and 816 comments by the Commission; access to notifications rose from about 1.2 million (2015) to 7.4 million (2020).",
         "reported as activity", "COM(2022) 481; SWD(2022) 297")],
    [lit("ec-2022-tris-report", "European Commission", 2022, "Report on the operation of the Single Market Transparency Directive from 2016 to 2020", "COM(2022) 481 (with SWD(2022) 297)", EU + "52022DC0481",
         "Commission implementation report", "operation report (notification statistics)", "technical barriers; administrative cooperation", "positive",
         "3,553 notifications in 2016-2020; 212 detailed opinions and 816 comments; procedure judged effective in preventing technical barriers and useful during COVID-19",
         "The Commission reports that the notification procedure keeps working and helps stop new national barriers, based on counts of notifications and its own reactions.",
         "EU, 2016-2020", "Commission self-assessment; activity data", "full text read (conclusions and statistics)")])

# 4. European Accessibility Act
rec("32019L0882", "European Accessibility Act", "52015PC0615", "SWD(2015) 264 (executive summary SWD(2015) 265)",
    "ex-ante only: applies since June 2025; impact assessment forecasts",
    "The accessibility requirements apply to new products and services since 28 June 2025, so no evaluation exists yet (the Commission reports by 2030). The impact assessment estimated that common requirements would cut the cost of meeting divergent national accessibility rules by up to about half, from a baseline of around EUR 20 billion a year in 2020.",
    [ind("note", "Applies since 28 June 2025; first Commission report due in 2030"),
     ind("expected impact (impact assessment)", "Lower costs of divergent national accessibility rules", "Annual cost to business of accessibility requirements", "baseline about EUR 20 billion (2020); savings up to 45-50% (forecast)",
         "Forecast only.", "not measured", "SWD(2015) 264")],
    [lit("ec-2015-eaa-ia", "European Commission", 2015, "Impact Assessment accompanying the proposal for a European Accessibility Act", "SWD(2015) 264", EU + "52015SC0264",
         "Commission impact assessment", "ex-ante", "compliance costs; accessibility; cross-border trade", "positive (forecast)",
         "Baseline annual cost of around EUR 20 billion in 2020; the options considered would save 20-50% of it; firms surveyed put extra accessibility costs below 5% of production costs",
         "The Commission expected one set of EU accessibility rules to cost firms much less than many national ones, and to widen the market for accessible products.",
         "EU, forecast", "forecast", "full text searched")])

# 5. Software Directive
rec("32009L0024", "Software Directive", "52008PC0023", "codification of Directive 91/250/EEC; no impact assessment of its own",
    "thin: one Commission implementation report (2000); no later evaluation",
    "The Directive codified the 1991 rules protecting computer programs by copyright. The Commission's only report (2000) found implementation satisfactory, the effects beneficial and no reason to reopen the rules, including the decompilation exception. No later evaluation or empirical study of its effects was found.",
    [ind("note", NOIND)],
    [lit("ec-2000-software-report", "European Commission", 2000, "Report on the implementation and effects of Directive 91/250/EEC on the legal protection of computer programs", "COM(2000) 199", EU + "52000DC0199",
         "Commission implementation report", "implementation report (Member State laws, stakeholder views)", "copyright protection; interoperability; piracy", "positive",
         "Implementation overall satisfactory; effects beneficial; the balance struck on decompilation still valid; no new initiative needed",
         "The Commission found that the rules protecting software by copyright worked and saw no reason to change them.",
         "EU-15, 1991-1999", "Commission self-assessment", "full text read (conclusions)")])

# 6. Collective Rights Management Directive
rec("32014L0026", "Collective Rights Management Directive", "52012PC0372", "SWD(2012) 204 (executive summary SWD(2012) 205)",
    "thin: one Commission application report based mainly on stakeholder views, with two supporting studies",
    "The Commission's 2021 report found the Directive had a positive effect on rightholders and on licensing, including multi-territorial licensing of music online, and saw no need to revise it; stakeholders still reported problems with user reporting and timely distribution of royalties. The assessment rests on consultation and two commissioned studies, not on measured outcomes.",
    [ind("note", NOIND)],
    [lit("ec-2021-crm-report", "European Commission", 2021, "Report on the application of Directive 2014/26/EU on collective management of copyright and related rights and multi-territorial licensing of rights in musical works for online use", "SWD(2021) 338",
         "https://digital-strategy.ec.europa.eu/en/library/reports-collective-management-and-extended-licensing",
         "Commission implementation report", "application report (stakeholder consultation, two external studies)", "governance and transparency of collecting societies; licensing", "positive",
         "Positive effect on rightholders and the licensing market; no need for review; remaining problems with users' reporting and timely distribution of royalties",
         "The Commission concluded the rules on collecting societies were working and did not need changes, though some payment and reporting problems persisted.",
         "EU, 2016-2021", "Commission self-assessment based on stakeholder views", "page summary via search")])

# 7. Conditional Access Directive
rec("31998L0084", "Conditional Access Directive", "51997PC0356", "none (proposed before impact assessments were introduced)",
    "thin: two Commission implementation reports (2003, 2008)",
    "The Directive bans commercial dealing in devices that give unauthorised access to pay-TV and online subscription services. The Commission's second report (2008) found that piracy adapted to new technology and that the hoped-for growth of cross-border pay services had largely not happened. No later evaluation or empirical study was found.",
    [ind("note", NOIND)],
    [lit("ec-2008-ca-report", "European Commission", 2008, "Second report on the implementation of Directive 98/84/EC on the legal protection of services based on, or consisting of, conditional access", "COM(2008) 593 (with SEC(2008) 2506)", EU + "52008DC0593",
         "Commission implementation report", "implementation report (public consultation, 54 contributions)", "piracy; cross-border pay-TV services", "mixed",
         "Piracy adapts well to technological progress; little cross-border growth of conditional-access services, though some pay-TV services are offered across borders",
         "Ten years on, the Commission found the ban on pirate decoders in place but piracy still adapting, and little cross-border pay-TV market.",
         "EU, 1998-2008", "Commission self-assessment", "full text read")])

# 8. ADR Directive
rec("32013L0011", "ADR Directive", "52011PC0793", "SEC(2011) 1408 (joint with the ODR Regulation; executive summary SEC(2011) 1409)",
    "thin: Commission application report (2019) and evaluation (2023) based on administrative data, surveys and consultation",
    "By 2019 consumers had access to certified dispute-resolution bodies in virtually all retail sectors, but the Commission found the system under-used: low awareness among consumers and low participation by traders. Its 2023 evaluation, annexed to the impact assessment for the amending proposal, confirmed this and led to targeted amendments.",
    [ind("note", NOIND),
     ind("evaluation question", "Consumers can use ADR for disputes with traders", "ADR coverage, awareness and trader participation", "",
         "2019: full sector coverage reached; framework 'underused'; ODR platform led to direct settlement in up to 42% of cases. 2023: low trader participation remains the main obstacle.",
         "partially measured", "COM(2019) 425; SWD(2023) 335")],
    [lit("ec-2019-adr-report", "European Commission", 2019, "Report on the application of Directive 2013/11/EU on alternative dispute resolution for consumer disputes and Regulation (EU) No 524/2013 on online dispute resolution", "COM(2019) 425", EU + "52019DC0425",
         "Commission implementation report", "application report (administrative data, surveys)", "access to redress; ADR use", "mixed",
         "High-quality ADR available in virtually all retail sectors; the framework is underused because of low awareness, complex national landscapes and low trader uptake",
         "Out-of-court dispute bodies now exist for almost every kind of purchase, but few consumers and traders use them.",
         "EU, 2015-2019", "Commission self-assessment", "full text read (conclusions)"),
     lit("ec-2023-adr-ia", "European Commission", 2023, "Impact Assessment accompanying the proposal amending Directive 2013/11/EU on alternative dispute resolution (evaluation of the ADR Directive annexed)", "SWD(2023) 335", EU + "52023SC0335",
         "Commission evaluation", "ex-post evaluation (annexed to impact assessment)", "ADR participation; consumer redress", "mixed",
         "Evaluation confirms low participation by traders as the main obstacle; disparities between Member States in ADR use persist",
         "The Commission's evaluation confirmed that the rules work where traders take part, but that many traders do not.",
         "EU, 2015-2023", "Commission self-assessment", "full text searched")])

# 9. Representative Actions Directive
rec("32020L1828", "Representative Actions Directive", "52018PC0184", "SWD(2018) 96 (joint impact assessment for the New Deal for Consumers)",
    "ex-ante only: applies since June 2023; no evaluation yet",
    "National rules transposing the Directive apply to representative actions brought since 25 June 2023, and several Member States transposed late. No Commission evaluation exists yet and no study measuring how many collective actions it has enabled was found.",
    [ind("note", "Applies since 25 June 2023; Commission evaluation due no earlier than 2028")],
    [lit("ec-2018-newdeal-ia", "European Commission", 2018, "Impact Assessment accompanying the New Deal for Consumers proposals", "SWD(2018) 96", EU + "52018SC0096",
         "Commission impact assessment", "ex-ante", "collective redress; consumer law enforcement", "positive (forecast)",
         "Joint impact assessment for the Omnibus Directive and the Representative Actions Directive; collective redress expected to improve consumers' access to justice in mass-harm cases",
         "The Commission expected EU-wide collective actions to make it easier for consumers to get redress when many are harmed at once.",
         "EU, forecast", "forecast", "title and scope checked")])

# 10. E-money Directive
rec("32009L0110", "E-money Directive", "52008PC0627", "SEC(2008) 2572",
    "thin: one Commission report (2018) drawing on two external studies",
    "The Commission's 2018 report judged the Directive largely successful in lowering barriers to entry: interest in e-money licences and cross-border passporting grew after 2011, though e-money remained a niche market. It suggested guidance on product classification and limited networks rather than legislative change.",
    [ind("note", NOIND),
     ind("evaluation question", "Lower barriers to market entry", "E-money licences and passporting", "",
         "Interest in e-money licences and cross-border passporting increased since 2011; number of institutions unevenly distributed across Member States.", "partially measured", "COM(2018) 41")],
    [lit("ec-2018-emd2-report", "European Commission", 2018, "Report on the implementation and impact of Directive 2009/110/EC, in particular on the application of prudential requirements for electronic money institutions", "COM(2018) 41", EU + "52018DC0041",
         "Commission implementation report", "implementation report (two external studies)", "market entry; competition; cross-border activity", "positive",
         "Overall assessment positive: the Directive largely removed barriers to entry; licences and passporting increased; e-money remains a niche market",
         "The Commission found the rules made it easier for new firms to issue e-money, although the market stayed small.",
         "EU, 2009-2014", "Commission self-assessment", "full text read (conclusions)")])

# 11. SEPA Regulation
rec("32012R0260", "SEPA Regulation", "52010PC0775", "SEC(2010) 1584 (summary SEC(2010) 1583)",
    "thin: Commission application report based on Member State questionnaires; earlier benefit figures are forecasts",
    "The Regulation forced the switch to common euro credit transfers and direct debits by 2014 (2016 outside the euro area). The Commission's 2017 report found it correctly applied across the EU and saw no need for new legislation, while monitoring 'IBAN discrimination'. No ex-post study quantifying the savings was found; the large benefit figures in circulation are forecasts.",
    [ind("note", NOIND),
     ind("deadline in the act", "Migration to SEPA credit transfers and direct debits", "Share of transactions in SEPA formats", "1 February 2014 (euro area); 31 October 2016 (other Member States)",
         "2017 report: migration achieved; correctly applied; IBAN discrimination still monitored.", "measured", "COM(2017) 683")],
    [lit("ec-2017-sepa-report", "European Commission", 2017, "Report on the application of Regulation (EU) No 260/2012 establishing technical and business requirements for credit transfers and direct debits in euro", "COM(2017) 683", EU + "52017DC0683",
         "Commission implementation report", "application report (Member State questionnaire)", "payment migration; compliance", "positive",
         "Correctly applied and implemented across the EU; no need for follow-up legislation; IBAN discrimination to be monitored",
         "The Commission found the switch to common euro payment formats complete and the rules working.",
         "EU, 2012-2016", "Commission self-assessment", "full text read (conclusions)"),
     lit("ec-2010-sepa-ia", "European Commission", 2010, "Impact Assessment accompanying the proposal for a Regulation establishing technical requirements for credit transfers and direct debits in euros", "SEC(2010) 1584", EU + "52010SC1584",
         "Commission impact assessment", "ex-ante", "payment costs; competition", "positive (forecast)",
         "Benefits of SEPA for the wider economy estimated at over EUR 300 billion over six years",
         "The Commission forecast very large savings from common euro payment formats; these were never measured afterwards.",
         "EU, forecast", "forecast", "summary via search")])

# 12. Transfer of Funds Regulation
rec("32023R1113", "Transfer of Funds Regulation", "52021PC0422", "SWD(2021) 190 (joint impact assessment for the 2021 AML package; executive summary SWD(2021) 191)",
    "ex-ante only: applies since December 2024; no evaluation yet",
    "The Regulation extends the 'travel rule' (information on sender and recipient) to crypto-asset transfers from 30 December 2024; EBA guidelines apply from the same date. No evaluation or study of its effect on money laundering exists yet; the impact assessment covered the whole anti-money-laundering package and did not quantify the effect of this Regulation.",
    [ind("note", "Applies since 30 December 2024")],
    [lit("ec-2021-aml-ia", "European Commission", 2021, "Impact Assessment accompanying the anti-money laundering package (executive summary)", "SWD(2021) 191 (full IA SWD(2021) 190)", EU + "52021SC0191",
         "Commission impact assessment", "ex-ante", "money laundering; supervision; compliance costs", "positive (forecast)",
         "Package-level assessment: harmonised rules, an EU supervisor and a EUR 10,000 cash limit; 99% of 202 consultation replies saw a need for further action; no separate quantification for transfers of funds",
         "The Commission's assessment of the anti-money-laundering package expected stronger, more uniform rules, but did not estimate the effect of the transfer-information rules on their own.",
         "EU, forecast", "forecast; package-level", "full text read (executive summary)")])

# 13. Consumer Credit Directive II
rec("32023L2225", "Consumer Credit Directive II", "52021PC0347", "SWD(2021) 170 (executive summary SWD(2021) 171)",
    "ex-ante only: applies from November 2026; evaluation of the 2008 Directive",
    "The new Directive applies from 20 November 2026. The evaluation of the 2008 Directive it replaces found that consumer protection and a single credit market had been only partially achieved, and that digital lending raised new risks. The impact assessment forecast a reduction in consumer detriment of around EUR 2 billion in 2021-2030.",
    [ind("note", "Applies from 20 November 2026"),
     ind("expected impact (impact assessment)", "Reduce consumer detriment", "Consumer detriment from credit problems", "about EUR 2 billion less in 2021-2030 (forecast)",
         "Forecast only.", "not measured", "SWD(2021) 170/171")],
    [lit("ec-2020-ccd-evaluation", "European Commission", 2020, "Evaluation of Directive 2008/48/EC on credit agreements for consumers", "SWD(2020) 254 (with report COM(2020) 963)", EU + "52020DC0963",
         "Commission evaluation", "ex-post evaluation (stakeholder consultation, external study)", "consumer protection; cross-border credit", "mixed",
         "Objectives only partially achieved; withdrawal and early repayment rights and standard information reduced detriment; digitalisation and new products created risks the Directive did not cover",
         "The Commission found the 2008 rules had raised consumer protection but had not created a single credit market and were outdated for online lending.",
         "EU, 2010-2019", "Commission self-assessment", "full text read (conclusions)"),
     lit("ec-2021-ccd-ia", "European Commission", 2021, "Impact Assessment accompanying the proposal for a Directive on consumer credits (executive summary)", "SWD(2021) 171 (full IA SWD(2021) 170)", EU + "52021SC0171",
         "Commission impact assessment", "ex-ante", "consumer detriment; compliance costs", "positive (forecast)",
         "Up to 46 million people affected by problems with the old rules; preferred option to cut consumer detriment by about EUR 2 billion in 2021-2030",
         "The Commission expected the new rules to save consumers about EUR 2 billion over ten years.",
         "EU, forecast", "forecast", "full text read (executive summary)")])

# 14. European Single Access Point
rec("32023R2859", "European Single Access Point (ESAP)", "52021PC0723", "SWD(2021) 344 (executive summary SWD(2021) 345)",
    "ex-ante only: ESAP starts operating in July 2027",
    "ESMA must open the single access point by 10 July 2027, so there is no evidence on use yet. The impact assessment put ESMA's set-up and running costs at up to EUR 16 million over 2022-2027 and companies' recurring filing costs at around EUR 121 million a year EU-wide; benefits for investors were described but not quantified.",
    [ind("note", "ESAP to be established by 10 July 2027"),
     ind("expected impact (impact assessment)", "Central access to company disclosures", "Costs of ESAP and of filing", "ESMA up to EUR 16 million (2022-2027); filers about EUR 121 million a year (forecast)",
         "Forecast only.", "not measured", "SWD(2021) 344/345")],
    [lit("ec-2021-esap-ia", "European Commission", 2021, "Impact Assessment accompanying the proposals establishing a European single access point (executive summary)", "SWD(2021) 345 (full IA SWD(2021) 344)", EU + "52021SC0345",
         "Commission impact assessment", "ex-ante", "costs; investor access to information", "positive (forecast)",
         "ESMA's costs up to EUR 16 million in 2022-2027; one-off interconnection about EUR 50,800 per collection body; recurring filing costs up to EUR 800 per entity, about EUR 121 million a year EU-wide",
         "The Commission expected a central portal for company disclosures to help investors, at modest cost per company.",
         "EU, forecast", "forecast", "full text read (executive summary)")])

# 15. Cybercrime Directive
rec("32013L0040", "Cybercrime Directive", "52010PC0517", "SEC(2010) 1122 (summary SEC(2010) 1123)",
    "thin: one Commission transposition report (2017)",
    "The Commission's 2017 report found that the Directive had led to comparable criminal offences for cyberattacks across Member States, but that definitions, penalties and statistics were not fully implemented; it saw no need to amend the Directive. The Directive's own statistics requirement is the weakest point, so its effect on cybercrime cannot be measured.",
    [ind("note", NOIND),
     ind("obligation in the act", "Monitoring and statistics", "Member State statistics on offences (Art. 14)", "",
         "2017 report: statistics and reporting channels among the provisions least implemented.", "not measured", "COM(2017) 474")],
    [lit("ec-2017-cybercrime-report", "European Commission", 2017, "Report assessing the extent to which the Member States have taken the necessary measures to comply with Directive 2013/40/EU on attacks against information systems", "COM(2017) 474", EU + "52017DC0474",
         "Commission implementation report", "transposition report", "criminalisation; cross-border cooperation", "mixed",
         "Substantive progress in criminalising cyberattacks on a comparable level; gaps on definitions, penalties, reporting channels and statistics; no need to amend",
         "The Commission found that countries had made cyberattacks crimes on similar terms, but had not fully applied the rules on penalties and statistics.",
         "EU, 2013-2017", "Commission self-assessment; legal analysis", "full text read (conclusions)")])

# 16. Child Sexual Abuse Directive
rec("32011L0093", "Child Sexual Abuse Directive", "52010PC0094", "SEC(2009) 355 (prepared for the 2009 Framework Decision proposal)",
    "thin: Commission transposition reports (2016) and a 2022 evaluation annexed to the recast impact assessment",
    "The Commission's 2016 reports found substantive progress in national criminal law but gaps in prevention programmes, victim support and the removal of abuse material online. Its 2022 evaluation, supported by an external study (RAND Europe and EY), concluded that even full transposition would not address the problem adequately, leading to the 2024 recast proposal. Comparable data on offences do not exist.",
    [ind("note", NOIND),
     ind("evaluation question", "Prevent abuse, protect victims, prosecute offenders", "Transposition of the Directive's provisions", "",
         "2016: main gaps in offender programmes (Arts 22-24), substantive criminal law (Arts 3-5) and victim support (Arts 18-20); removal of online material (Art. 25) still incomplete.",
         "reported as activity", "COM(2016) 871; COM(2016) 872")],
    [lit("ec-2016-csa-transposition", "European Commission", 2016, "Report assessing the extent to which the Member States have taken the necessary measures to comply with Directive 2011/93/EU", "COM(2016) 871", EU + "52016DC0871",
         "Commission implementation report", "transposition report", "criminal law; victim support; prevention", "mixed",
         "Substantive progress in criminal codes and cooperation; main gaps in offender programmes, substantive criminal law and victim assistance; no plan to amend",
         "The Commission found that countries had changed their criminal laws but lagged on prevention programmes and support for child victims.",
         "EU, 2011-2016", "Commission self-assessment; legal analysis", "full text read (conclusions)"),
     lit("ec-2016-csa-art25", "European Commission", 2016, "Report assessing the implementation of the measures referred to in Article 25 of Directive 2011/93/EU (websites containing child sexual abuse material)", "COM(2016) 872", EU + "52016DC0872",
         "Commission implementation report", "implementation report", "removal and blocking of abuse material online", "mixed",
         "Significant efforts by Member States; prompt removal of material hosted in their territory and safeguards for blocking still to be ensured",
         "The Commission found that removing child abuse material from websites was still not prompt enough everywhere.",
         "EU, 2011-2016", "Commission self-assessment", "full text read (conclusions)"),
     lit("ec-2024-csa-recast-ia", "European Commission", 2024, "Impact Assessment accompanying the proposal for a Directive on combating the sexual abuse and sexual exploitation of children (recast), with the evaluation of Directive 2011/93/EU", "SWD(2024) 33", EU + "52024SC0033",
         "Commission evaluation", "ex-post evaluation (external study by RAND Europe and EY) within impact assessment", "prevention; victim support; prosecution", "negative",
         "Evaluation found that even with full transposition, child sexual abuse is not adequately addressed; prevention and victim-assistance programmes rarely evaluated by Member States",
         "The Commission's evaluation concluded that the 2011 rules, even if fully applied, were not enough to tackle child sexual abuse, especially online.",
         "EU, 2011-2022", "Commission self-assessment with external study", "full text searched")])
