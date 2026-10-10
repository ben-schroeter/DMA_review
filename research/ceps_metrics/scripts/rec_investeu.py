import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2020 amended proposal's financial statement has no indicators section (1.4.4 is about synergies); monitoring relies on the key performance indicators annexed to the Regulation and guarantee agreements"),
 ind("headline target (Regulation / Commission)", "Investment mobilised", "More than EUR 372bn additional public and private investment by 2028 from a EUR 26.2bn EU guarantee (2018 proposal: EUR 650bn from EUR 38bn)", "EUR 372bn",
     "Interim evaluation: about EUR 218bn expected to be mobilised by end-2023 (65% private), anticipated multiplier 14.76; 90% of the guarantee allocated, almost 80% of that approved. Figures are expected/approved, not disbursed.", "partially measured (self-reported)", "SWD(2024) 228/229"),
 ind("objective", "Additionality", "Support only investment that would not otherwise happen (market gaps, higher risk)", "",
     "Interim evaluation reports high additionality based on implementing partners' assessments; the Court of Auditors found additionality of the predecessor EFSI insufficiently demonstrated and its mobilised investment overstated by EUR 131bn (26%).", "mixed evidence", "SWD(2024) 228; ECA SR 07/2025"),
 ind("outcome", "Firm investment and growth", "Effects on recipient firms' investment, jobs, innovation", "", "No causal study of InvestEU yet; a causal study of predecessor EFSI direct loans finds about 12 percentage points extra fixed-asset growth.", "not measured (predecessor evidence only)", "Frayman 2026"),
]
literature = [
 lit("ec-2018-investeu-ia", "European Commission", 2018, "Impact Assessment accompanying the proposal establishing the InvestEU Programme", "SWD(2018) 314", EU + "52018SC0314",
     "Commission impact assessment", "ex-ante (builds on EFSI and financial instrument evaluations)", "investment mobilised", "positive (forecast)",
     "Single EU guarantee of EUR 38bn expected to mobilise EUR 650bn of investment, with a more cautious multiplier than EFSI because of riskier, policy-targeted products; EFSI multiplier 13.5 at end-2017 against a target of 15",
     "The Commission expected merging EU investment instruments into one guarantee programme to unlock EUR 650 billion of investment; the final, smaller programme targets EUR 372 billion.",
     "EU, forecast", "forecast for original 2018 proposal; budget later reduced", "full text partly read"),
 lit("ec-2024-investeu-interim-eval", "European Commission (based on ICF study)", 2024, "Interim evaluation of the InvestEU Programme", "SWD(2024) 228 (executive summary SWD(2024) 229)", "https://investeu.europa.eu/interim-evaluation-investeu-programme_en",
     "Commission evaluation", "interim evaluation (portfolio data to end-2023, interviews, surveys)", "investment mobilised; additionality", "positive (self-assessment)",
     "About EUR 218bn expected to be mobilised by end-2023 (65% private), anticipated multiplier 14.76; 90% of the EUR 26.2bn guarantee allocated; meaningful crowding-in and high additionality; budget insufficient relative to demand",
     "The Commission's mid-term review says InvestEU was on track to unlock EUR 218 billion of investment by end-2023, most of it private, and that demand exceeds its budget.",
     "EU, 2021-2023", "self-evaluation; mobilisation figures are expected, not realised; no counterfactual", "page summary (Commission page and press report)"),
 lit("eca-2025-efsi-sr07", "European Court of Auditors", 2025, "The European Fund for Strategic Investments: contributed substantially to addressing the investment gap, but had not fully reached the EUR 500 billion target in the real economy by the end of 2022", "ECA Special Report 07/2025", "https://www.eca.europa.eu/ECAPublications/SR-2025-07/SR-2025-07_EN.pdf",
     "independent audit", "audit of reported results", "investment mobilised; additionality", "negative (for predecessor's reporting)",
     "EFSI contributed substantially to closing the investment gap, but its reported EUR 503bn of mobilised investment was overstated by EUR 131bn (26%) against the EUR 500bn target (undisbursed financing counted, double counting with other EU instruments, cancellations not deducted); additionality not sufficiently demonstrated; no ex-post check of additionality",
     "The EU's auditors found that InvestEU's predecessor overstated the investment it unlocked by about a quarter and could not prove it funded projects that would not have happened anyway, a warning for how InvestEU's figures are read.",
     "EU, 2015-2022 (EFSI)", "audit of predecessor programme, same methodology lineage", "abstract read (ECA press release and report contents)", pdf_url="https://www.eca.europa.eu/ECAPublications/SR-2025-07/SR-2025-07_EN.pdf"),
 lit("frayman-2026-efsi", "Frayman", 2026, "The European Fund for Strategic Investments (EFSI): causal effects of a state lending policy", "Journal of Economic Policy Reform", "https://doi.org/10.1080/17487870.2026.2613781",
     "peer-reviewed", "causal: difference-in-differences with matched controls", "firm investment (fixed assets)", "positive",
     "EFSI-backed direct EIB loans raised recipients' fixed-asset growth by about 12 percentage points on average after treatment",
     "A causal study of InvestEU's predecessor finds firms receiving its loans grew their fixed assets about 12 percentage points faster than similar firms.",
     "EU firms, EFSI period", "predecessor programme; direct loans, not guarantees", "page summary via search (Crossref metadata confirmed)", "paywalled"),
]
write("32021R0523", "InvestEU Programme", "52020PC0403", "SWD(2018) 314 (for the original 2018 proposal COM(2018) 439)",
      "moderate-thin: Commission interim evaluation with self-reported mobilisation figures; auditors' critique and one causal study concern the predecessor EFSI, not InvestEU itself",
      "InvestEU uses a EUR 26.2 billion EU budget guarantee to unlock more than EUR 372 billion of investment by 2028. The Commission's 2024 mid-term review reported EUR 218 billion expected by end-2023, mostly private, but these are expected rather than realised figures. EU auditors found the predecessor fund overstated its results by 26% and could not prove additionality, although an independent causal study finds its loans did boost firms' investment.",
      indicators, literature)
