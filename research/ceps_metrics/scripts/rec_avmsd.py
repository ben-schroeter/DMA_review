import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2009 proposal was a codification with no indicators; monitoring is through biennial Member State reports on European works (Arts 13, 16, 17). The 2016 evaluation found no effective monitoring system"),
 ind("objective", "Promote European works (linear TV)", "Majority of transmission time for European works; 10% for independent works", "majority share",
     "Member States report 68-69% European works on TV (2020-21), down from 72.6% (2019); an independent sample study found only 38%, and under 3% independent European works vs 40-41% reported.", "mixed evidence", "COM(2024) 261"),
 ind("objective (2018 amendment)", "Promote European works (on demand)", "At least 30% European works in VOD catalogues, with prominence", "30%",
     "Member States report 63-64% (2020-21); independent snapshot of 1,062 services (2023) found 35%; methods differ and data incomplete.", "mixed evidence", "COM(2024) 261"),
 ind("objective", "Single market (country of origin)", "Providers regulated only where established", "",
     "2016 evaluation: perceived as effective, brought legal certainty and economies of scale; robust economic data lacking.", "reported as activity", "SWD(2016) 170"),
 ind("expected impact (2016 IA)", "Protection of minors on video-sharing platforms", "", "", "Costs and benefits not quantified; no outcome measurement found.", "not measured", "SWD(2016) 168"),
]
literature = [
 lit("ec-2016-avmsd-evaluation", "European Commission", 2016, "Ex-post REFIT evaluation of the Audiovisual Media Services Directive 2010/13/EU (executive summary SWD(2016) 171)", "SWD(2016) 170", EU + "52016SC0170",
     "Commission evaluation", "REFIT evaluation (three public consultations, studies, monitoring reports)", "single market; cultural diversity; pluralism; costs", "mixed",
     "Country-of-origin principle effective; Directive enhanced cultural diversity on TV but less so on demand; partly effective on media freedom; robust economic data and compliance-cost data lacking; no effective monitoring system",
     "The 2016 evaluation found the rules let broadcasters operate EU-wide under one country's law, but admitted there was little hard data on their effects.",
     "EU, 2007-2015", "self-evaluation; data gaps acknowledged", "full text read (executive summary)"),
 lit("ec-2016-avmsd-ia", "European Commission", 2016, "Impact assessment for the amendment of Directive 2010/13/EU (executive summary SWD(2016) 169)", "SWD(2016) 168", EU + "52016SC0168",
     "Commission impact assessment", "ex-ante", "minors' protection; level playing field", "positive (forecast)",
     "Preferred options: obligations on video-sharing platforms for minors and hate speech, stronger European-works rules for on-demand services, independent regulators; costs mainly on on-demand and video-sharing services, mitigated by existing practice; not quantified",
     "The Commission proposed extending the rules to video-sharing platforms and on-demand services, without putting numbers on costs or benefits.",
     "EU, forecast", "forecast; qualitative", "full text read (executive summary)"),
 lit("ec-2024-avmsd-european-works-report", "European Commission", 2024, "Report on the application of Articles 13, 16 and 17 of Directive 2010/13/EU for 2020-2021 (with SWD(2024) 149)", "COM(2024) 261", EU + "52024DC0261",
     "Commission monitoring report", "Member State reports plus independent sample study", "share of European works", "mixed",
     "VOD: Member States report 63-64% European works, independent study of 1,062 services finds 35%; TV: reported 68-69% vs 38% in the study, independent productions reported 40-41% vs under 3% in the study; SVOD revenues EUR 6.7bn (2019) to EUR 11.7bn (2021)",
     "Countries report that European works make up about two-thirds of TV and streaming content, but an independent check found only about 35-38%.",
     "EU/EEA, 2020-2023", "official data inconsistent with independent sample", "full text read"),
]
write("32010L0013", "Audiovisual Media Services Directive", "52009PC0185", "none for the 2010 codification; SWD(2016) 168 for the 2018 amendment",
      "thin: Commission evaluation and monitoring reports with conflicting figures; no independent causal studies of quotas or other rules found",
      "The AVMS Directive lets TV and streaming services operate EU-wide under one country's rules and requires them to promote European works. The Commission's 2016 evaluation found the single-country rule effective but admitted little hard data. Member States report European works at about two-thirds of TV and streaming content, yet an independent check found only 35-38%, and no study measures whether the quotas boosted European production.",
      indicators, literature)
