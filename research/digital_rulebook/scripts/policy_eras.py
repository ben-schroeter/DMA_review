"""Digital policy eras: assign each of the 115 instruments to the era in which it was proposed, and check whether its
Commission proposal (explanatory memorandum and recitals, EUR-Lex HTML) cites the era's strategy or agenda.
Writes data/policy_eras/instruments.json. Run from research/digital_rulebook."""
import json, re, os, sys, html, collections, openpyxl
sys.path.insert(0, "scripts")
from common import fetch
ERAS = [("market_opening", "Market opening", 0, 2000.2), ("lisbon", "Lisbon", 2000.2, 2010.2), ("europe2020", "Europe 2020", 2010.2, 2015.35),
        ("dsm", "Digital Single Market", 2015.35, 2019.92), ("digital_decade", "Digital Decade", 2019.92, 2025.0),
        ("competitiveness", "Competitiveness", 2025.0, 2100)]
PAT = {"lisbon": r"Lisbon ([Ss]trategy|[Aa]genda|European Council|objectives|[Pp]rocess|goals|[Pp]artnership)|\beEurope\b|\bi2010\b",
       "europe2020": r"Europe 2020|Digital Agenda for Europe",
       "dsm": r"Digital Single Market Strategy|Strategy for a Digital Single Market|Digital Single Market strategy",
       "digital_decade": r"Shaping Europe.s [Dd]igital [Ff]uture|Digital Decade|Digital Compass|European [Ss]trategy for [Dd]ata|European data strategy|White Paper on Artificial Intelligence|Europe fit for the digital age",
       "competitiveness": r"Competitiveness Compass|One Europe, One Market|Draghi"}
fy = lambda d: (lambda s: int(s[:4]) + (int(s[5:7]) - 1) / 12)(str(d))
wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True); r = list(wb["instruments"].values); h = r[0]
I = [dict(zip(h, x)) for x in r[1:] if x[0]]
links = json.load(open("data/proposals.json"))["links"]
out = []
for x in I:
    p = fy(x["proposal_date"]); era = next(e for e in ERAS if e[2] <= p < e[3])
    pc = (str(x["proposal_celex"]).split(";")[0] if x["proposal_celex"] else None) or (links.get(str(x["celex_measured"])) or {}).get("proposal_celex") or (str(x["celex_measured"]) if str(x["celex_measured"]).startswith("5") else None)
    cites, has_text = {}, False
    if pc and str(pc).startswith("5"):
        try:
            raw = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{pc}")
            txt = html.unescape(re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "ignore") if isinstance(raw, bytes) else raw))
            txt = re.sub(r"\s+", " ", txt)
            has_text = len(txt.split()) > 500
            if has_text:
                m_end = re.search(r"HA(VE|S) ADOPTED TH(IS|E PRESENT)", txt)
                body = txt[:m_end.start()] if m_end else txt      # memorandum, citations and recitals
                for k, pat in PAT.items():
                    m = re.search(pat, body)
                    if m:
                        cites[k] = m.group(0)
        except Exception as e:
            print("fail", pc, e)
    out.append({"row_id": x["row_id"], "name": x["name"], "celex": str(x["celex_measured"]), "proposal_celex": pc, "proposal_date": str(x["proposal_date"])[:10],
                "adoption_date": str(x["adoption_date"])[:10] if x["adoption_date"] else None, "status": x["status"], "area": x["policy_area"],
                "obligations": x["restrictions_total"], "era": era[0], "proposal_text": has_text, "cites": cites, "cites_own_era": era[0] in cites})
os.makedirs("data/policy_eras", exist_ok=True)
json.dump(out, open("data/policy_eras/instruments.json", "w"), indent=1)
c = collections.defaultdict(collections.Counter)
for o in out:
    c[o["era"]]["n"] += 1; c[o["era"]]["text"] += o["proposal_text"]; c[o["era"]]["cites"] += o["cites_own_era"]; c[o["era"]]["obl"] += o["obligations"] or 0
for e in ERAS:
    print(e[1], dict(c[e[0]]))
