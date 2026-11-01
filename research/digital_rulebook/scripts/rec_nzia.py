import sys; sys.path.insert(0, ".")
from impact_record import ind, lit, write
EU = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:"
indicators = [
 ind("note", "No formal impact assessment was prepared (urgency); the analysis was set out in staff working document SWD(2023) 68. The LFS gives no quantified indicators: the Commission will monitor via annual competitiveness reports on clean energy technologies and evaluate after three years"),
 ind("benchmark (Regulation)", "Manufacturing capacity", "EU net-zero technology manufacturing capacity as share of annual EU deployment needs", "At least 40% by 2030; 15% of world production by 2040",
     "No published assessment of progress against the benchmark found; Bruegel criticised the 40% benchmark as poorly defined.", "not measured", "Regulation (EU) 2024/1735; Tagliapietra et al. 2023"),
 ind("target (Regulation)", "CO2 storage", "Annual CO2 injection capacity", "50 Mt per year by 2030", "Commission to report annually; no figures verified.", "not measured", ""),
 ind("expected impact (Commission analysis)", "Investment", "Investment needed for EU net-zero manufacturing", "around EUR 92bn to 2030 (reported)",
     "Not tracked against the Act.", "not measured", "SWD(2023) 68 (figure as reported secondary)"),
]
literature = [
 lit("ec-2023-nzia-proposal", "European Commission", 2023, "Proposal for a Net-Zero Industry Act, explanatory memorandum", "COM(2023) 161", EU + "52023PC0161",
     "Commission proposal (no impact assessment)", "ex-ante (no IA)", "manufacturing capacity; market size", "positive (forecast)",
     "Proposal not accompanied by an impact assessment owing to urgency; global market for key mass-manufactured net-zero technologies expected to reach about EUR 600bn a year by 2030 (IEA)",
     "The Commission proposed the Act without an impact assessment, pointing to a global clean-tech market worth about EUR 600 billion a year by 2030.",
     "EU/global, forecast", "no impact assessment", "full text read"),
 lit("ec-2023-nzia-swd68", "European Commission", 2023, "Investment needs assessment and funding availabilities to strengthen EU's Net-Zero technology manufacturing capacity", "SWD(2023) 68", "https://data.consilium.europa.eu/doc/document/ST-7613-2023-ADD-2/en/pdf",
     "Commission staff working document", "ex-ante", "investment needs", "n/a (needs estimate)",
     "Estimates EU investment needed in net-zero manufacturing; secondary reports put it at around EUR 92bn by 2030",
     "The Commission's background analysis estimated the investment needed to build EU clean-tech factories, reported at around EUR 92 billion by 2030.",
     "EU, to 2030", "forecast", "page summary via search"),
 lit("tagliapietra-veugelers-zettelmeyer-2023", "Tagliapietra, Veugelers & Zettelmeyer", 2023, "Rebooting the European Union's Net Zero Industry Act", "Bruegel Policy Brief 15/2023", "https://hdl.handle.net/10419/274229",
     "think-tank policy brief", "policy analysis", "competitiveness; investment; governance", "negative (critique)",
     "Calls the proposal unconvincing: top-down technology picking, a poorly defined protectionist 40% self-sufficiency benchmark, reliance on permitting although it is not the main obstacle, ineffective procurement design and no governance structure",
     "Bruegel economists argued the Act picks technologies, sets a vague 40% self-sufficiency goal and targets permitting, which is not the main barrier to clean-tech investment.",
     "EU, 2023", "expert critique, not empirical", "abstract read"),
]
write("32024R1735", "Net-Zero Industry Act", "52023PC0161", "none (staff working document SWD(2023) 68 instead)",
      "ex-ante only, no impact assessment: one think-tank critique; no measurement of the 40% benchmark",
      "The Act aims for EU factories to supply at least 40% of the EU's needs for clean technologies such as solar panels, batteries and heat pumps by 2030. It was proposed without an impact assessment, and economists at Bruegel called the 40% goal vague and protectionist. No study or official report has yet measured progress towards the goal or the Act's effect on investment.",
      indicators, literature)
