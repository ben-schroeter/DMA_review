import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2011 proposal (part of the New Legislative Framework alignment package) has no financial-statement indicators; it relied on the impact assessment for the NLF alignment package and later REFIT evaluation"),
 ind("evaluation question", "Avoid electromagnetic disturbance between equipment", "Interference problems and product compliance", "",
     "2023 REFIT evaluation: Directive 'successfully reduced interference', but market surveillance authorities report too many cheap non-compliant products, especially bought online from third countries. No EU-wide compliance rate reported.",
     "reported as activity", "SWD(2023) 7/8"),
 ind("evaluation question", "Free movement / efficiency", "Compliance costs vs benefits", "",
     "Evaluation concludes benefits outweigh costs for each stakeholder group; industry estimates compliance costs at 5-10% of total production costs, relatively higher for SMEs. Based on stakeholder input, not measured outcomes.",
     "partially measured", "SWD(2023) 7/8"),
]
literature = [
 lit("ec-2023-emcd-evaluation", "European Commission", 2023, "Evaluation of Electromagnetic Compatibility Directive 2014/30/EU (executive summary)", "SWD(2023) 8 (full evaluation SWD(2023) 7)", EU + "52023SC0008",
     "Commission evaluation", "ex-post REFIT evaluation (14 product groups; stakeholder consultation, supporting study)", "interference; compliance costs; market surveillance", "positive",
     "Directive reduced interference and supported the internal market; benefits outweigh costs; compliance costs estimated by industry at 5-10% of production costs; persistent non-compliant low-cost online imports",
     "The Commission's evaluation judged the EMC rules effective and worth their cost, but noted many cheap non-compliant gadgets still reach EU buyers online.",
     "EU, 2016-2021", "Commission self-assessment; largely qualitative", "full text read (executive summary)"),
]
write("32014L0030", "Electromagnetic Compatibility Directive", "52011PC0765", "Shared impact assessment for the 2011 NLF alignment package (not separately reviewed)",
      "thin: one Commission evaluation based on stakeholder views; no measured compliance trend and no independent studies found",
      "The EMC Directive, which keeps electrical products from interfering with each other, set no monitoring indicators. The Commission's 2023 evaluation found it effective and worth its cost, with industry putting compliance at 5-10% of production costs, but warned that cheap non-compliant products bought online remain a problem. No independent study of its effects was found.",
      indicators, literature)
