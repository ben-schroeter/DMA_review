import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "Commission regulation adopted under Article 101(3) TFEU - no legislative proposal or LFS indicators. The accompanying 2022 impact assessment and the 2020 evaluation of the 2010 VBER set the objectives; the Regulation expires 31 May 2034 and no ex-post evaluation exists yet"),
 ind("objective (impact assessment)", "Legal certainty and lower compliance costs", "Clearer safe harbour, reduced self-assessment costs for businesses", "",
     "Not measured. The 2020 evaluation itself found too little quantitative data to assess compliance costs robustly.", "not measured", "SWD(2020) 172"),
 ind("objective (impact assessment)", "Adapt rules to online sales and platforms", "Treatment of wide retail parity clauses (no longer block-exempted), online sales restrictions, dual distribution", "",
     "No study of the 2022 rules' effects found. Earlier causal studies of national bans on hotel-booking parity clauses (Germany, France) found more room availability and direct-channel price competition and some short-run price falls - background evidence for the change.", "not measured (background evidence only)", "Hunold et al. 2018; Mantovani et al. 2021"),
 ind("objective (impact assessment)", "Prevent consumer harm from vertical restraints", "Fewer harmful restrictions (e.g. resale price maintenance, territorial restrictions)", "",
     "Enforcement continues case by case; no aggregate measure.", "not measured", ""),
]
literature = [
 lit("ec-2020-vber-evaluation", "European Commission", 2020, "Evaluation of the Vertical Block Exemption Regulation and Vertical Guidelines (Staff Working Document)", "SWD(2020) 172", EU + "52020SC0172",
     "Commission evaluation", "ex-post evaluation (external study, public consultation, case studies)", "legal certainty; compliance costs; online sales", "mixed",
     "2010 VBER useful and still relevant but not adapted to growth of online sales and platforms; some definitions unclear; diverging national interpretation; costs could not be quantified robustly due to lack of data", "The Commission's review of the 2010 rules found them still useful but outdated for e-commerce and online platforms, and could not put numbers on their costs or benefits.",
     "EU, 2010-2019", "self-evaluation; mostly qualitative", "full text read (conclusions)"),
 lit("ec-2022-vber-ia", "European Commission", 2022, "Impact assessment report accompanying the revised Vertical Block Exemption Regulation and Vertical Guidelines", "Commission staff working document (May 2022)", "https://competition-policy.ec.europa.eu/public-consultations/2018-vber_en",
     "Commission impact assessment", "ex-ante", "legal certainty; online sales; parity clauses; dual distribution", "positive (forecast)",
     "Published with the revised rules (VBER adopted 10 May 2022, in force 1 June 2022; Guidelines 30 June 2022); SWD reference not confirmed", "The Commission's assessment underpinned changes to how the competition rules treat online sales, platforms and price-parity clauses.",
     "EU", "forecast", "page summary via search"),
 lit("hunold-et-al-2018", "Hunold, Kesler, Laitenberger & Schlutter", 2018, "Evaluation of best price clauses in online hotel bookings", "International Journal of Industrial Organization 61: 542-571", "https://doi.org/10.1016/j.ijindorg.2018.03.008",
     "peer-reviewed", "difference-in-differences (meta-search price data, ~30,000 hotels, several countries)", "availability; prices; channel competition", "positive (of banning parity clauses)",
     "After Booking.com's narrow parity clause was abolished in Germany, hotels offered rooms more often on Booking.com and more often promoted their direct channel; chain hotels' direct channel more often had the strictly lowest price", "A study of nearly 30,000 hotels found that when price-parity clauses were removed, hotels listed more rooms and more often undercut booking platforms on their own websites.",
     "Germany and other European countries, mid-2010s", "causal; predates 2022 VBER (background)", "abstract read", access="paywalled"),
 lit("mantovani-piga-reggiani-2021", "Mantovani, Piga & Reggiani", 2021, "Online platform price parity clauses: Evidence from the EU Booking.com case", "European Economic Review 131: 103625", "https://doi.org/10.1016/j.euroecorev.2020.103625",
     "peer-reviewed", "difference-in-differences (posted Booking.com prices, France vs controls)", "prices", "mixed",
     "Removal of price parity clauses in France in 2015 led to significant price decreases in the short run but a more limited effect in the medium run; hotels with more complex structures cut prices more", "Hotel prices on Booking.com fell after France banned price-parity clauses, though the effect faded over time.",
     "France (2015 ban) vs comparison countries", "causal; predates 2022 VBER (background)", "page summary via search", access="paywalled"),
]
write("32022R0720", "Vertical Block Exemption Regulation", "None (Commission regulation)", "Impact assessment report, May 2022 (SWD number not confirmed); evaluation SWD(2020) 172",
      "thin: no evaluation of the 2022 rules yet; causal evidence exists only for related national bans on hotel price-parity clauses",
      "The 2022 rules define which supply and distribution agreements are automatically allowed under EU competition law, with changes for online sales and platform price-parity clauses. No study has yet measured their effect. Earlier research on national bans of hotel-booking parity clauses found more price competition and some short-run price falls, which helped motivate the change.",
      indicators, literature)
