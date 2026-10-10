import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
# Covers both horizontal block exemptions: 2023/1066 (R&D agreements) and 2023/1067 (specialisation agreements)
indicators = [
 ind("note", "Commission regulations adopted without a legislative proposal or financial statement, so there are no LFS indicators; the 2023 rules replaced Regulations 1217/2010 and 1218/2010 after an evaluation (SWD(2021) 103) and an impact assessment phase with five support studies whose report was not found on EUR-Lex"),
 ind("evaluation objective", "Legal certainty for cooperating firms", "Firms and authorities find the block exemptions clear and usable", "",
     "2021 evaluation: rules still relevant and made economically desirable cooperation easier, but some conditions seen as too strict or unclear; need to reflect digitalisation and sustainability. The 2023 revision responds to this; no ex-post check of the new rules yet (they expire in 2035).", "partially measured", "SWD(2021) 103"),
 ind("evaluation objective", "Lower compliance costs", "Self-assessment costs saved compared with no block exemption", "",
     "Evaluation could not quantify savings: most stakeholders did not know whether costs had changed; few gave estimates.", "not measured", "SWD(2021) 103"),
 ind("expected impact", "Innovation", "More pro-competitive R&D cooperation and innovation", "",
     "No empirical study found of the block exemption's effect on R&D cooperation or innovation; theory suggests the 25% market-share safe harbour is not clearly justified.", "not measured", "Ruble & Versaevel 2014"),
]
literature = [
 lit("ec-2021-hber-evaluation", "European Commission", 2021, "Evaluation of the Horizontal Block Exemption Regulations (R&D and Specialisation) and the Horizontal Guidelines", "SWD(2021) 103", EU + "52021SC0103",
     "Commission evaluation", "evaluation (public consultation 2019-20, external evaluation study, NCA survey)", "legal certainty; compliance costs; relevance", "mixed",
     "HBERs and Guidelines made economically desirable cooperation easier and gave legal certainty, but some rules unduly strict or unclear and outdated for digitalisation and sustainability; compliance-cost savings could not be quantified",
     "The Commission's evaluation found the old rules useful for firms that cooperate on research or production, but in need of updating and unable to put a number on the money saved.",
     "EU, 2011-2020", "self-assessment; largely qualitative", "full text read"),
 lit("ec-2023-hber-note", "European Commission (DG Competition)", 2023, "Explanatory note on the 2023 Horizontal Block Exemption Regulations", "DG Competition", "https://competition-policy.ec.europa.eu/system/files/2023-06/2023_HBERs_explanatory_note_en.pdf",
     "Commission explanatory note", "descriptive", "rule changes", "n/a",
     "Revision addresses issues found in the evaluation, informed by an impact assessment phase with stakeholder workshops and five support studies; changes to market-share calculation, innovation competition and SME usability",
     "The Commission explains that the 2023 rules fix problems found in the evaluation, but publishes no forecast of their economic effect.",
     "EU", "descriptive", "full text read", pdf_url="https://competition-policy.ec.europa.eu/system/files/2023-06/2023_HBERs_explanatory_note_en.pdf"),
 lit("ruble-versaevel-2014", "Ruble & Versaevel", 2014, "Market shares, R&D agreements, and the EU block exemption", "International Review of Law and Economics 37: 15-25", "https://doi.org/10.1016/j.irle.2013.04.008",
     "peer-reviewed", "theoretical model", "R&D incentives; welfare", "mixed",
     "Incentives to innovate under cooperation depend on several effects; an 'outsider effect' can raise R&D when combined market share is high, so theory does not support limiting the exemption to low market shares",
     "A theory paper argues that the market-share cap in the R&D block exemption may exclude cooperation that would actually boost innovation.",
     "theory (Regulation 1217/2010)", "theory only; no data", "page summary via search", access="paywalled"),
]
write("32023R1066", "Horizontal Block Exemption Regulations (R&D 2023/1066 and specialisation 2023/1067)", "", "No published impact assessment report; evaluation SWD(2021) 103",
      "very thin: Commission evaluation of the predecessor rules (qualitative) and theory; no empirical study of effects on R&D cooperation or innovation",
      "These two Commission regulations let competitors cooperate on research and on specialised production without breaching EU competition law if they stay below market-share limits. The Commission's 2021 evaluation of the previous rules found them useful but outdated, and could not measure how much they saved companies. No study has measured whether the block exemptions increase research cooperation or innovation.",
      indicators, literature)
