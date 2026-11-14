"""Impact records for the second round of additions (November 2026; notes/scope_2026-11.md): rows 132-141.
Sources: Commission evaluations, implementation reports and impact assessments read from the Publications Office (Cellar)
where available, otherwise from the Commission's pages and summaries found by search (marked in `verified`).
Run from scripts/: python3 rec_scope_2026_11b.py"""
import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
NOIND = "No monitoring indicators set in the proposal; assessed through the Commission's reports listed below"

write("32003R0001", "Antitrust Procedure Regulation", "52000PC0582", "none (proposed in 2000, before impact assessments)",
      "thin: Commission evaluations based on enforcement records, consultation and a support study; no independent study of the Regulation's effect on enforcement outcomes",
      "Regulation 1/2003 ended the notification of agreements to the Commission and shared enforcement with national authorities and courts. The Commission's 2024 evaluation judged the framework broadly effective, citing 225 Commission enforcement decisions and more than EUR 42 billion in fines over 20 years, but found procedures slow and less suited to digital markets; a revision is under way.",
      [ind("note", NOIND),
       ind("activity (evaluation)", "Effective and uniform enforcement of Articles 101 and 102", "Commission enforcement decisions and fines", "",
           "2004-2024: 225 Commission enforcement decisions; fines above EUR 42 billion (about EUR 37 billion upheld by the EU Courts).", "reported as activity", "SWD(2024) 217")],
      [lit("ec-2024-reg1-evaluation", "European Commission", 2024, "Evaluation of Regulations 1/2003 and 773/2004 (antitrust enforcement framework)", "SWD(2024) 217",
           "https://competition-policy.ec.europa.eu/antitrust-and-cartels/legislation/regulation-12003_en",
           "Commission evaluation", "ex-post evaluation (public consultation, workshop, external support study)", "enforcement effectiveness; procedures", "positive with gaps",
           "Framework broadly met its goal of effective, efficient and uniform application of EU competition rules; 225 enforcement decisions and over EUR 42 billion in fines in 20 years; procedures seen as slow, notably for digital markets",
           "The Commission found the decentralised antitrust system it created in 2004 works, but that cases take long, which led to a planned revision.",
           "EU, 2004-2024", "Commission self-assessment", "page summary via search"),
       lit("ec-2009-reg1-report", "European Commission", 2009, "Report on the functioning of Regulation 1/2003", "COM(2009) 206", EU + "52009DC0206",
           "Commission implementation report", "implementation report", "enforcement; cooperation in the competition network", "positive",
           "Five years on, the Regulation had transformed enforcement: more cases by national authorities, cooperation through the European Competition Network, and an end to notifications",
           "The Commission's first review found the 2004 reform had made antitrust enforcement across the EU more active and better coordinated.",
           "EU, 2004-2008", "Commission self-assessment", "summary via search")])

write("32006L0123", "Services Directive", "52004PC0002", "extended impact assessment SEC(2004) 21",
      "thin: model-based estimates of the effect of the barriers removed; no causal ex-post study found",
      "The Directive required Member States to remove unjustified barriers to establishing and providing services and to set up points of single contact. A Commission economists' assessment (2012) estimated gains in trade, investment and GDP from the barriers actually removed, but its authors describe it as an extrapolation rather than a full ex-post evaluation; a 2015 review by Sweden's National Board of Trade found no ex-post analysis of the Directive's effects.",
      [ind("note", NOIND)],
      [lit("monteagudo-2012-services", "Monteagudo, J., Rutkowski, A. and Lorenzani, D.", 2012, "The economic impact of the Services Directive: a first assessment following implementation", "European Economy Economic Papers 456, European Commission (DG ECFIN)",
           "https://econpapers.repec.org/RePEc:euf:ecopap:0456",
           "Commission working paper", "quantitative assessment (barrier indicators before and after implementation, gravity-model estimates)", "trade in services; FDI; GDP", "positive (estimate)",
           "Estimates gains in intra-EU services trade, FDI and GDP from the barriers removed by implementation; authors describe it as an updated prediction rather than an assessment of full effects",
           "Commission economists estimated that the barriers removed by the Directive raise trade and investment in services, but stressed that this is an estimate, not a measurement of what happened.",
           "EU, 2006-2011", "model-based; not causal", "abstract read"),
       lit("kommerskollegium-2015-single-market", "National Board of Trade Sweden (Kommerskollegium)", 2015, "Economic effects of the European Single Market: review of the empirical literature", "National Board of Trade report",
           "https://www.kommerskollegium.se/globalassets/publikationer/rapporter/2016-och-aldre/publ-economic-effects-of-the-european-single-market.pdf",
           "Government agency review", "literature review", "single market for services", "no evidence",
           "No ex-post analysis of the effects of the Services Directive available at the time of the review",
           "A Swedish government review of the evidence found no study that had measured the Directive's actual effects.",
           "EU", "literature review", "summary via search")])

MD_EVAL = lit("ec-2025-mdr-ivdr-evaluation", "European Commission", 2025, "Targeted evaluation of Regulation (EU) 2017/745 on medical devices and Regulation (EU) 2017/746 on in vitro diagnostic medical devices", "SWD(2025) 1051", EU + "52025SC1051",
              "Commission evaluation", "ex-post evaluation (targeted; surveys, consultation, studies)", "safety; compliance costs; device availability; innovation", "mixed",
              "Benefits for patients materialising through stronger safety, performance and transparency, but at high and often disproportionate cost; implementation delays, longer and costlier market access, limited notified-body capacity; decrease in availability of some, particularly innovative and niche, devices",
              "The Commission's own evaluation found the stricter rules make devices safer and more transparent, but are costly and slow enough that some devices, especially new and niche ones, have left or not reached the EU market.",
              "EU, 2017-2025", "Commission self-assessment; data on costs limited", "full text read (conclusions)")
MD_SAVE = lit("ec-2025-mdr-ivdr-savings", "European Commission", 2025, "Cost-savings accompanying the proposal amending Regulations (EU) 2017/745 and 2017/746", "SWD(2025) 1050", EU + "52025SC1050",
              "Commission proposal (cost-savings document)", "ex-ante (targeted revision)", "compliance costs", "positive (forecast)",
              "Simplification measures in the December 2025 proposal estimated to save around EUR 3.3 billion a year (EUR 0.9 billion adjustment and EUR 2.4 billion administrative costs)",
              "For its proposed simplification, the Commission estimates savings for industry of about EUR 3.3 billion a year.",
              "EU, forecast", "forecast", "full text searched")
MD_IND = lit("medtecheurope-2024-survey", "MedTech Europe", 2024, "MDR/IVDR survey report (highlights)", "MedTech Europe",
             "https://medtecheurope.org/wp-content/uploads/2025/01/mte-ivdr-mdr-survey-report-highlights-final.pdf",
             "industry survey", "survey of manufacturers", "market access; device availability; innovation", "negative",
             "About half of respondents deprioritise the EU as the first market for new devices; SMEs obtain certificates more slowly",
             "An industry survey reports that many manufacturers now launch new devices outside the EU first.",
             "EU, 2022 data", "industry survey; interested party", "summary via search", interested_party="medical technology industry association")
write("32017R0745", "Medical Devices Regulation", "52012PC0542", "joint impact assessment SWD(2012) 273 (executive summary SWD(2012) 274)",
      "thin: one Commission targeted evaluation and industry surveys; no causal study of effects on safety or availability",
      "The Regulation has applied since May 2021, with transition periods extended several times. The Commission's 2025 targeted evaluation found safety and transparency improving but compliance costs high and often disproportionate, with fewer innovative and niche devices available; a targeted revision proposed in December 2025 is estimated to save about EUR 3.3 billion a year.",
      [ind("note", NOIND),
       ind("evaluation question", "High level of safety while supporting innovation", "Availability of devices; certification times and costs", "",
           "2025: safety and transparency benefits materialising; longer and costlier market access; decrease in availability of some devices.", "partially measured", "SWD(2025) 1051")],
      [MD_EVAL, MD_SAVE, MD_IND])
write("32017R0746", "In Vitro Diagnostic Medical Devices Regulation", "52012PC0541", "joint impact assessment SWD(2012) 273 (executive summary SWD(2012) 274)",
      "thin: one Commission targeted evaluation (with the Medical Devices Regulation) and industry surveys",
      "The Regulation has applied since May 2022, with long transition periods because most tests now need a notified body. The Commission's 2025 targeted evaluation, covering both device regulations, found safety and transparency benefits but high and often disproportionate costs and reduced availability of some devices; the December 2025 proposal would simplify both.",
      [ind("note", NOIND)], [MD_EVAL, MD_SAVE, MD_IND])

write("32019R2144", "Vehicle General Safety Regulation", "52018PC0286", "SWD(2018) 190 (executive summary SWD(2018) 191)",
      "ex-ante only: applies to all new vehicles since July 2024; first Commission evaluation due July 2027",
      "The mandatory safety systems apply to new vehicle types since July 2022 and to all new vehicles since July 2024; the Commission must report on their effect, including real-world performance of intelligent speed assistance, by 7 July 2027. No evaluation exists yet.",
      [ind("note", "Evaluation report due by 7 July 2027 (Art. 14)")],
      [lit("ec-2018-gsr-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal on type-approval requirements for motor vehicles as regards their general safety", "SWD(2018) 190 (executive summary SWD(2018) 191)", EU + "52018SC0190",
           "Commission impact assessment", "ex-ante", "road safety; vehicle costs", "positive (forecast)",
           "Mandatory advanced safety systems expected to reduce road deaths and serious injuries; costs passed on in vehicle prices",
           "The Commission expected the new mandatory safety systems to save lives on EU roads.",
           "EU, forecast", "forecast", "title and scope checked")])

write("32021R0821", "Dual-Use Regulation", "52016PC0616", "SWD(2016) 315 (executive summary SWD(2016) 314)",
      "thin: annual Commission implementation reports with licensing and trade statistics; no evaluation of effects",
      "The recast export-control regime applies since September 2021. The Commission's annual implementation reports put dual-use exports at about 2.7% of EU exports (EUR 128 billion in 2020) and describe licensing activity, but licensing decisions are not public and no evaluation of the Regulation's effects exists.",
      [ind("note", NOIND),
       ind("activity (implementation report)", "Effective and consistent export controls", "Licences, denials, controlled trade", "",
           "Dual-use exports about 2.7% of EU exports (EUR 128 billion, 2020); latest report covers 2024.", "reported as activity", "COM(2022) 434; COM(2026) 296")],
      [lit("ec-2026-dualuse-report", "European Commission", 2026, "Report on the implementation of Regulation (EU) 2021/821 (export control data for 2024)", "COM(2026) 296 (with SWD(2026) 162)", EU + "52026DC0296",
           "Commission implementation report", "implementation report (Member State licensing data)", "export controls; transparency", "reported as activity",
           "Aggregated EU and Member State export control data for 2024; aims to increase transparency of licensing",
           "The Commission publishes yearly figures on dual-use export licensing, but they describe activity, not effects.",
           "EU, 2024", "activity data", "summary via search"),
       lit("ec-2022-dualuse-report", "European Commission", 2022, "Report on the implementation of Regulation (EU) 2021/821 (2021)", "COM(2022) 434", EU + "52022DC0434",
           "Commission implementation report", "implementation report", "export controls", "reported as activity",
           "Dual-use exports about 2.7% of EU exports, EUR 128 billion in 2020",
           "Dual-use items make up a small but significant share of EU exports.",
           "EU, 2020-2021", "activity data", "summary via search")])

write("32014L0035", "Low Voltage Directive", "52011PC0773", "joint impact assessment SEC(2011) 1376 for the New Legislative Framework alignment package",
      "thin: one Commission evaluation based mainly on stakeholder views; little quantitative data",
      "The Commission's 2021 evaluation found the Directive fairly effective in creating a single market for electrical equipment and protecting safety, with no major differences in interpretation between Member States; market surveillance, especially of online sales, was the weak point. Stakeholders supplied little quantitative cost data.",
      [ind("note", NOIND)],
      [lit("ec-2021-lvd-evaluation", "European Commission", 2021, "Evaluation of the Low Voltage Directive 2014/35/EU", "SWD(2021) 202", EU + "52021SC0202",
           "Commission evaluation", "ex-post evaluation (stakeholder survey, external study)", "internal market; product safety", "positive with gaps",
           "Fairly effective for the internal market and health and safety; harmonised standards keep it up to date; market surveillance, notably of e-commerce, ineffective; benefits judged to outweigh costs but little quantitative data",
           "The Commission found the safety rules for electrical equipment work, but that unsafe products sold online often slip through.",
           "EU, 2016-2020", "Commission self-assessment based on stakeholder views", "full text read (conclusions)")])

write("32011L0065", "RoHS Directive", "52008PC0809", "SEC(2008) 2930 (summary SEC(2008) 2931)",
      "thin: one Commission evaluation with two supporting studies",
      "The Commission's 2023 evaluation found that the Directive has reduced hazardous substances in electrical and electronic equipment and works well overall, including as a global benchmark, but that the processes for exemptions and new restrictions lack transparency and efficiency; it proposed moving the technical assessment to the European Chemicals Agency.",
      [ind("note", NOIND)],
      [lit("ec-2023-rohs-evaluation", "European Commission", 2023, "Evaluation of Directive 2011/65/EU on the restriction of the use of certain hazardous substances in electrical and electronic equipment", "SWD(2023) 760 (with report COM(2023) 760)", EU + "52023SC0760",
           "Commission evaluation", "ex-post evaluation (two external studies, consultation)", "hazardous substances; internal market", "positive with gaps",
           "Helped reduce hazardous substances in EEE and harmonise the market; a global benchmark; exemption and restriction procedures lack transparency, efficiency and scientific robustness",
           "The Commission found the ban on hazardous substances in electronics effective, but its exemption procedures slow and opaque.",
           "EU, 2011-2021", "Commission self-assessment", "full text read (conclusions of the report)")])

write("32012L0019", "WEEE Directive", "52008PC0810", "SEC(2008) 2933 (summary SEC(2008) 2934)",
      "thin: one Commission evaluation with a supporting study; collection data reported by Member States",
      "The Commission's 2025 evaluation found that collection of waste electronics rose by about 65% between 2012 and 2021, but that nearly half of all e-waste generated in the EU is still not collected, only three Member States met the 65% collection target in 2022, and the recycling targets do little to recover critical raw materials.",
      [ind("note", NOIND),
       ind("target in the act", "Separate collection of WEEE", "Collection rate", "65% of EEE placed on the market (or 85% of WEEE generated) from 2019",
           "Collection up about 65% (2012-2021); nearly half of WEEE generated not collected; three Member States met the target in 2022.", "measured", "Commission evaluation 2025")],
      [lit("ec-2025-weee-evaluation", "European Commission", 2025, "Evaluation of Directive 2012/19/EU on waste electrical and electronic equipment (WEEE)", "Commission staff working document (July 2025)",
           "https://environment.ec.europa.eu/publications/staff-working-document-evaluation-directive-201219eu-waste-electrical-and-electronic-equipment-weee_en",
           "Commission evaluation", "ex-post evaluation (Member State data, supporting study by Ramboll, Umweltbundesamt and Oeko-Institut, consultation)", "collection; recycling; raw materials", "mixed",
           "Collection up about 65% between 2012 and 2021, but nearly half of WEEE not collected; only three Member States met the 65% target in 2022; recycling targets do not drive recovery of critical raw materials",
           "The Commission found more e-waste is collected than before, but most countries miss the target and valuable materials are still lost.",
           "EU, 2012-2022", "Commission self-assessment; official statistics", "summary via search")])

write("32015L0849", "Fourth Anti-Money Laundering Directive", "52013PC0045", "SWD(2013) 21 (executive summary SWD(2013) 22)",
      "thin: Commission assessments and an EU audit of implementation; no study measuring effects on money laundering",
      "The Commission's 2019 assessment found major divergences in how Member States apply the anti-money laundering rules, a structural weakness that led to the 2024 package replacing this Directive with a directly applicable Regulation from July 2027. The European Court of Auditors (2021) found EU action in the banking sector fragmented and implementation insufficient.",
      [ind("note", NOIND)],
      [lit("ec-2019-aml-implementation", "European Commission", 2019, "Towards better implementation of the EU's anti-money laundering and countering the financing of terrorism framework", "COM(2019) 360", EU + "52019DC0360",
           "Commission implementation report", "assessment (recent cases, supranational risk assessment, FIU cooperation)", "implementation; supervision", "negative",
           "Major divergences in the application of the framework; a structural problem for preventing misuse of the financial system; options include turning the Directive into a Regulation and an EU supervisor",
           "The Commission concluded that countries applied the anti-money laundering rules so differently that the system had structural gaps.",
           "EU, 2015-2019", "Commission self-assessment", "full text read (conclusions)"),
       lit("eca-2021-aml", "European Court of Auditors", 2021, "EU efforts to fight money laundering in the banking sector are fragmented and implementation is insufficient", "Special Report 13/2021",
           "https://op.europa.eu/webpub/eca/special-reports/fight-money-laundering-13-2021/en/index.html",
           "EU audit", "performance audit", "transposition; supervision", "negative",
           "Incomplete transposition of the AML directives; fragmented and poorly coordinated institutional response; EU oversight insufficient for a level playing field",
           "EU auditors found the rules were not fully put into national law and that supervision was fragmented.",
           "EU, 2015-2020", "audit", "page summary via search")])
