import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "The 2018 proposal's financial statement has no indicators section; the memorandum says Member States will collect yearly monitoring data and the Commission will report within 5 years. The Regulation applies only from 18 August 2026"),
 ind("expected impact (impact assessment)", "Effective investigations", "Faster, more effective cross-border access to electronic evidence; fewer gaps in investigations", "",
     "No data yet; Regulation applicable only since 18 Aug 2026. Industry reports the decentralised IT system (e-CODEX) was still under development in mid-2026 and 22 Member States received formal notices (27 Mar 2026) for not transposing the companion Directive 2023/1544.", "not measured", "SWD(2018) 118/119; EuroISPA 2026"),
 ind("expected impact (impact assessment)", "Costs and savings", "One-off costs EUR 3.3m for Member States and EUR 1.7m for service providers; recurrent savings over EUR 7.1m/yr (Member States) and EUR 4.3m/yr (providers)", "",
     "Not measured.", "not measured", "SWD(2018) 119"),
]
literature = [
 lit("ec-2018-eevidence-ia", "European Commission", 2018, "Impact Assessment accompanying the proposals on European Production and Preservation Orders for electronic evidence and on legal representatives (executive summary SWD(2018) 119)", "SWD(2018) 118", EU + "52018SC0119",
     "Commission impact assessment", "ex-ante", "investigation effectiveness; administrative costs", "positive (forecast)",
     "More effective and efficient investigations and prosecutions; one-off costs EUR 3.3m (Member States) and EUR 1.7m (providers); no recurrent costs; recurrent savings >EUR 7.1m/yr for Member States and >EUR 4.3m/yr for providers; possible crime reduction through deterrence",
     "The Commission expected the new orders to speed up police access to online evidence across borders and to save authorities and providers more than EUR 11 million a year.",
     "EU, forecast", "forecast", "full text read"),
 lit("euroispa-2026-eevidence", "EuroISPA", 2026, "e-Evidence Regulation: Closing the implementation gap before August 2026", "EuroISPA position paper, June 2026", "https://www.euroispa.org/wp-content/uploads/2026/06/final_e-Evidence-implementation-paper.pdf",
     "industry position paper", "descriptive (member survey and national engagement)", "implementation readiness", "negative",
     "Systemic readiness gap: Directive transposition deadline (18 Feb 2026) met by few states; Commission formal notices to 22 Member States on 27 Mar 2026; decentralised e-CODEX system still under development; providers need at least 18 months after technical specifications; asks for a grace period",
     "Internet providers warned in mid-2026 that neither governments nor the IT system were ready for the new e-evidence rules.",
     "EU, 2026", "advocacy document", "full text read", pdf_url="https://www.euroispa.org/wp-content/uploads/2026/06/final_e-Evidence-implementation-paper.pdf",
     interested_party="Association of internet service providers subject to the obligations"),
]
write("32023R1543", "E-evidence Regulation", "52018PC0225", "SWD(2018) 118 (executive summary SWD(2018) 119)",
      "ex-ante only: rules applied from August 2026; impact assessment forecasts and an industry readiness paper",
      "The E-evidence Regulation lets prosecutors order online service providers in other EU countries to hand over or preserve electronic data. The Commission expected faster investigations and savings of over EUR 11 million a year, but the rules only applied from August 2026 and industry warned that the IT system and national laws were not ready. There is no evidence yet on how well it works.",
      indicators, literature)
