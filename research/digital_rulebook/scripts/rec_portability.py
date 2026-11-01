import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
NR = "https://ec.europa.eu/newsroom/dae/redirection/document/"
indicators = [
 ind("note", "The proposal has no financial statement indicators; the memorandum only promised two-phase monitoring with attention to SMEs and consumers. The Commission reported on application in SWD(2022) 173 (Article 10 review)"),
 ind("expected impact (impact assessment)", "Consumer demand for portability", "Potential users of portability of paid subscriptions: 29 million (5.7% of EU consumers) in 2015, rising to about 72 million (14%) by 2020", "29m (2015) -> ~72m (2020)",
     "Partially measured: Flash Eurobarometer (Feb 2019) found 32% of subscribers (49% of those who travelled) had tried to use their service in another Member State; providers report cross-border users are under 5% of their subscribers; COVID-19 travel restrictions reduced use. No headcount comparable to the forecast.", "partially measured", "SWD(2015) 270; Flash Eurobarometer 477a; SWD(2022) 173"),
 ind("monitoring (memorandum)", "Consumers", "Consumer awareness and satisfaction with portability", "",
     "Measured once: 52% of respondents aware of portability; 58% of users satisfied (2019). Over 80% of surveyed providers and 23 of 32 consumer bodies received no complaints.", "measured", "Flash Eurobarometer 477a; SWD(2022) 173"),
 ind("monitoring (memorandum)", "Service providers / SMEs", "Compliance and implementation costs for providers, in particular SMEs", "",
     "Survey-based: music, e-book and games providers already offered portability and faced no significant cost; audiovisual and sports providers had to adapt verification and infrastructure, costs reported as minor; SMEs found residence verification and data-protection compliance challenging. Some non-compliance: 10 providers limit portability to periods of 14 days to one year; some small providers unaware of the rules. No cost figures.", "reported as activity", "Visionary Analytics study (2022); SWD(2022) 173"),
 ind("expected impact (impact assessment)", "Rightholders", "No significant negative effect on licensing value / rightholder revenues", "",
     "Study found no significant impact on rightholders' overall revenues (self-reported; no quantitative analysis).", "partially measured", "Visionary Analytics study (2022)"),
]
literature = [
 lit("ec-2015-portability-ia", "European Commission", 2015, "Impact Assessment accompanying the proposal for a Regulation to ensure the cross-border portability of online content services in the internal market", "SWD(2015) 270", EU + "52015SC0270",
     "Commission impact assessment", "ex-ante (survey-based demand estimate)", "consumer access; demand for portability", "positive (forecast)",
     "Estimated 29 million potential users of portability of paid subscriptions (5.7% of EU consumers), forecast to reach about 72 million (14%) by 2020; costs for providers expected to be limited", "The Commission estimated that around 29 million Europeans could benefit from taking their paid streaming subscriptions abroad, rising to about 72 million by 2020.",
     "EU28, forecast", "forecast", "full text read", pdf_url=NR + "87793"),
 lit("ec-2022-portability-report", "European Commission", 2022, "Report on the application of Regulation (EU) 2017/1128 on cross-border portability of online content services in the internal market", "SWD(2022) 173", EU + "52022SC0173",
     "Commission review report", "review (synthesis of survey, Eurobarometer and stakeholder evidence)", "consumer use and satisfaction; provider compliance; rightholder revenues", "positive",
     "Regulation 'has proven to function well overall'; 32% of subscribers had used portability abroad, 58% of users satisfied; very few complaints; no significant revenue loss for rightholders reported; some non-compliance (time limits, too many verification means, small providers not offering portability)", "The Commission's 2022 review concluded the rules work well: about a third of subscribers had used their services abroad, few complained, and rightholders reported no significant revenue loss, though some providers still restrict portability.",
     "EU, 2018-2021", "descriptive; no counterfactual", "full text read", pdf_url=NR + "87791"),
 lit("visionary-analytics-2022-portability", "Visionary Analytics with Kantar Public (for DG CNECT)", 2022, "Study on the Portability Regulation - Final report (SMART 2019/0024)", "European Commission, DG CNECT", NR + "87794",
     "Commission-commissioned study", "surveys (62 providers, 40 consumer bodies), mystery shopping of 39 services, 63 interviews, case studies", "compliance; provider costs; rightholder impacts", "positive",
     "Overwhelming majority of providers apply the Regulation; music, e-book and games sectors faced no significant costs; audiovisual and sports providers made changes with mostly minor costs; 10 providers limit temporary presence to 14 days-1 year; cross-border users under 5% of each provider's subscribers", "An evaluation study for the Commission found most services comply at small cost, but ten limit how long subscribers can use them abroad and some small providers ignore the rules.",
     "EU/EEA, 2020-2021", "descriptive survey; self-reported costs", "full text read (abstract and summary sections)"),
 lit("eurobarometer-477a-2019", "European Commission (Kantar)", 2019, "Flash Eurobarometer 477a: Accessing content online and cross-border portability of online content services", "Flash Eurobarometer 477a", NR + "87795",
     "survey", "representative survey (fieldwork Feb 2019)", "awareness; use; satisfaction", "positive",
     "52% aware of portability; 32% of subscribers had tried to access services while in another Member State; 58% of users satisfied", "A 2019 EU-wide survey found half of Europeans knew about the portability right and most of those who used it were satisfied.",
     "EU28, Feb 2019", "representative survey; one wave only", "page summary via Commission report (figures as cited in SWD(2022) 173)"),
 lit("eao-2019-portability-free", "European Audiovisual Observatory", 2019, "First feedback from the implementation of the Portability Regulation by free online video services", "European Audiovisual Observatory (Council of Europe)", NR + "87790",
     "report (intergovernmental body)", "descriptive survey of free online video services", "voluntary uptake of portability by free services", "mixed",
     "Of 13 free online video services in the sample, 4 had implemented portability, 2 were implementing and 7 considering; uptake led by public broadcasters; mandatory login and verification costs deter others", "Few free streaming services (mostly public broadcasters) had chosen to offer portability by 2019, citing login and verification costs.",
     "Europe, 2019", "small sample; descriptive", "full text read (conclusions)"),
]
write("32017R1128", "Portability Regulation", "52015PC0627", "SWD(2015) 270",
      "thin: one Commission review backed by surveys and self-reported provider evidence; no independent or causal studies",
      "The Portability Regulation lets people use their paid streaming, music and gaming subscriptions when travelling in other EU countries. The Commission's 2022 review found it works well: about a third of subscribers had used their services abroad, few complained, and providers and rightholders reported only minor costs, though some services still cap how long you can use them abroad. No independent study has measured its economic effects.",
      indicators, literature)
