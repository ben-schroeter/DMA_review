"""Draft: timeline of EU digital policy, 1987-2028, with the 105 adopted laws of the CEPS list.
Layers: economic strategies and digital agendas (spans), Commission presidents and lead digital commissioners, events;
instruments by CEPS policy area as a line from proposal to adoption (dot at adoption sized by obligations; open line =
pending); cumulative obligations at the bottom. Era shading by proposal date. Writes site/policy_timeline.svg."""
import openpyxl, math, collections
wb = openpyxl.load_workbook("ceps_instruments_metrics.xlsx", read_only=True, data_only=True); r = list(wb["instruments"].values); h = r[0]
I = [dict(zip(h, x)) for x in r[1:] if x[0] and x[h.index("status_oct2026")] == "adopted"]  # pending proposals enter once adopted
import json
PAGES = {int(k): v for k, v in json.load(open("site/instrument_pages.json")).items()}
fy = lambda d: (lambda s: int(s[:4]) + (int(s[5:7]) - 1) / 12 + (int(s[8:10]) - 1) / 365)(str(d)) if d else None
INK, INK2, MUTED, LINE, BASE, BG = "#282424", "#3F3B3B", "#666666", "#E8E6E3", "#C9C6C3", "#FAF9F5"
GOLD, GOLD_D, GOLD_L, BLUE, SLATE = "#B8860B", "#8F6708", "#E3CF9C", "#004494", "#5C5858"
F = 'font-family="DM Sans, sans-serif"'
t = lambda x, y, s, size=12, fill=INK2, anchor="start", weight=None: (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {F} font-size="{size}" fill="{fill}"'
                                                                     + (f' font-weight="{weight}"' if weight else "") + f'>{s}</text>')
W, L, R, Y0, Y1 = 1100, 168, 1088, 1987, 2028.6
BRK = L + 0.13 * (R - L)          # 1987-2000 squeezed into 13% of the width
X = lambda v: L + (v - Y0) / (2000 - Y0) * (BRK - L) if v < 2000 else BRK + (v - 2000) / (Y1 - 2000) * (R - BRK)
g = []
ERAS = [(1987, 2000.2, "Market opening", "market-opening"), (2000.2, 2010.2, "Lisbon", "lisbon"), (2010.2, 2015.35, "Europe 2020", "europe-2020"),
        (2015.35, 2019.92, "Digital Single Market", "digital-single-market"), (2019.92, 2025.0, "Digital Decade", "digital-decade"), (2025.0, 2028.6, "Competitiveness", "competitiveness")]
ERA_FILL = ["#F3F1EC", "#FAF9F5"]
TOP = 4
AREAS = ["Connectivity", "Data & Privacy", "Trust & Safety", "E-commerce & Consumer Protection", "Competition & Single Market", "Cybersecurity",
         "Finance", "IPR", "Media", "Law Enforcement", "Industrial Policy", "Research & Innovation"]
LANE = 38
lane_top = TOP + 214
lanes_bottom = lane_top + len(AREAS) * LANE
cum_top, cum_h = lanes_bottom + 40, 120
H = cum_top + cum_h + 50
# era shading over everything
for i, (a, b, lab, anc) in enumerate(ERAS):
    g.append(f'<rect x="{X(a):.1f}" y="{TOP}" width="{X(b) - X(a):.1f}" height="{H - TOP - 30}" fill="{ERA_FILL[i % 2]}"></rect>')
    words = lab.split(" ") if X(b) - X(a) < len(lab) * 7 else [lab]
    lines = [" ".join(words[:len(words) // 2 + len(words) % 2]), " ".join(words[len(words) // 2 + len(words) % 2:])] if len(words) > 1 else words
    g.append(f'<a href="#era-{anc}">' + "".join(t((X(a) + X(b)) / 2, TOP + 12 + k * 13, ln, 12, INK, "middle", 600) for k, ln in enumerate(lines)) + '</a>')
# years axis
for y in (1990, 2000, 2005, 2010, 2015, 2020, 2025):
    g.append(f'<line x1="{X(y):.1f}" x2="{X(y):.1f}" y1="{TOP + 22}" y2="{H - 40}" stroke="{LINE}" stroke-dasharray="2 3"></line>')
    g.append(t(X(y), H - 24, y, 12, MUTED, "middle"))
# span rows
def spans(y, label, items, fill, tc="#FFFFFF"):
    g.append(t(L - 12, y + 15, label, 12.5, INK, "end", 600))
    for a, b, lab in items:
        w = X(b) - X(a)
        g.append(f'<rect x="{X(a):.1f}" y="{y}" width="{w - 2:.1f}" height="22" rx="3" fill="{fill}"><title>{lab}</title></rect>')
        SH = {"Digital Agenda for Europe": "Digital Agenda", "Shaping Europe's digital future · Digital Decade": "Digital Decade",
              "One Europe, One Market": "One Europe, One Market", "Competitiveness Compass": "Compass", "Telecoms liberalisation (Green Paper 1987)": "Telecoms", "Lisbon Strategy": "Lisbon"}
        for cand in (lab, SH.get(lab, lab)):
            if w > len(cand) * 6.3 + 6:
                g.append(t(X(a) + 5, y + 15, cand, 11.5, tc)); break
        else:
            parts = SH.get(lab, lab).split(", ") if ", " in SH.get(lab, lab) else SH.get(lab, lab).rsplit(" ", 1)
            if len(parts) == 2 and w > max(len(p) for p in parts) * 5.0 + 4:
                g.append(t(X(a) + 4, y + 9.5, parts[0] + ("," if ", " in SH.get(lab, lab) else ""), 9.5, tc) + t(X(a) + 4, y + 19.5, parts[1], 9.5, tc))
y = TOP + 38
spans(y, "Economic strategy", [(2000.2, 2010.2, "Lisbon Strategy"), (2010.2, 2020.0, "Europe 2020"), (2025.05, 2028.6, "Competitiveness Compass")], SLATE)
y += 30
spans(y, "Digital agenda", [(1987.5, 1998.0, "Telecoms liberalisation (Green Paper 1987)"), (1999.9, 2005.4, "eEurope"), (2005.4, 2010.4, "i2010"),
                            (2010.4, 2015.35, "Digital Agenda for Europe"), (2015.35, 2019.92, "Digital Single Market"), (2020.1, 2025.0, "Shaping Europe's digital future · Digital Decade"),
                            (2026.1, 2028.6, "One Europe, One Market")], BLUE)
y += 30
spans(y, "Commission", [(1987, 1995.0, "Delors"), (1995.0, 1999.7, "Santer"), (1999.7, 2004.9, "Prodi"), (2004.9, 2014.85, "Barroso"),
                        (2014.85, 2019.92, "Juncker"), (2019.92, 2028.6, "von der Leyen")], "#D4D2CE", INK)
y += 30
spans(y, "Digital commissioner", [(1989.0, 1999.7, "Bangemann"), (1999.7, 2004.9, "Liikanen"), (2004.9, 2010.1, "Reding"), (2010.1, 2014.85, "Kroes"),
                                  (2014.85, 2019.92, "Ansip"), (2019.92, 2024.9, "Vestager, Breton"), (2024.9, 2028.6, "Virkkunen")], "#E9E7E3", INK)
# events
y += 40
EV = [(1993.0, "Single market"), (2008.7, "Financial crisis"), (2013.45, "Snowden"), (2018.2, "Cambridge Analytica"),
      (2020.2, "COVID-19"), (2022.9, "ChatGPT"), (2024.7, "Draghi report")]
for j, (v, lab) in enumerate(EV):
    yy = y + (j % 2) * 14
    g.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{yy - 4}" y2="{lanes_bottom}" stroke="{GOLD}" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"></line>')
    g.append(f'<circle cx="{X(v):.1f}" cy="{yy - 4}" r="3" fill="{GOLD}"></circle>' + t(X(v) + 5, yy, lab, 11, GOLD_D))
g.append(t(L - 12, y, "Events", 12.5, INK, "end", 600))
# instruments
rad = lambda n: 2.5 + math.sqrt(max(n or 0, 1)) / 3.2
for i, a in enumerate(AREAS):
    yy = lane_top + i * LANE + LANE / 2
    g.append(f'<line x1="{L}" x2="{R}" y1="{yy + LANE / 2:.1f}" y2="{yy + LANE / 2:.1f}" stroke="{LINE}"></line>')
    g.append(t(L - 12, yy + 4, a.replace("E-commerce & Consumer Protection", "E-commerce, consumers").replace("Competition & Single Market", "Competition, single mkt").replace("Research & Innovation", "Research, innovation"), 12.5, INK, "end"))
    acts = sorted([x for x in I if x["policy_area_ceps"] == a], key=lambda x: fy(x["proposal_date"]))
    for k, x in enumerate(acts):
        p, d = fy(x["proposal_date"]), fy(x["adoption_date"])
        off = (k % 4 - 1.5) * 7
        end = d if d else 2026.83
        g.append(f'<line x1="{X(p):.1f}" x2="{X(end):.1f}" y1="{yy + off:.1f}" y2="{yy + off:.1f}" stroke="{GOLD}" stroke-width="1.6" opacity="0.55"'
                 + ('' if d else ' stroke-dasharray="3 2"') + '></line>')
        g.append(f'<circle cx="{X(p):.1f}" cy="{yy + off:.1f}" r="1.8" fill="{GOLD_D}"></circle>')
        if d:
            g.append(f'<a href="{PAGES[x['row_id']]}"><circle cx="{X(d):.1f}" cy="{yy + off:.1f}" r="{rad(x["restrictions_total"]):.1f}" fill="{GOLD}" fill-opacity="0.85" stroke="{BG}" stroke-width="1">'
                     f'<title>{x["name"]}: proposed {str(x["proposal_date"])[:7]}, adopted {str(x["adoption_date"])[:7]}, {x["restrictions_total"]} obligations</title></circle></a>')
        else:
            g.append(f'<a href="{PAGES[x['row_id']]}"><circle cx="{X(end):.1f}" cy="{yy + off:.1f}" r="4" fill="{BG}" stroke="{GOLD}" stroke-width="1.5"><title>{x["name"]}: proposed {str(x["proposal_date"])[:7]}, pending</title></circle></a>')
# cumulative obligations (adopted acts, original texts)
pts = sorted((fy(x["adoption_date"]), x["restrictions_total"] or 0) for x in I if x["adoption_date"] and x["status_oct2026"] == "adopted")
tot = sum(n for _, n in pts); cum = 0; path = [f"{X(Y0):.1f},{cum_top + cum_h:.1f}"]
ycum = lambda c: cum_top + cum_h - c / tot * cum_h
for v, n in pts:
    path.append(f"{X(v):.1f},{ycum(cum):.1f}"); cum += n; path.append(f"{X(v):.1f},{ycum(cum):.1f}")
path.append(f"{X(2026.83):.1f},{ycum(cum):.1f}"); path.append(f"{X(2026.83):.1f},{cum_top + cum_h:.1f}")
g.append(f'<polygon points="{" ".join(path)}" fill="{GOLD_L}" opacity="0.8"></polygon>')
g.append(t(L - 12, cum_top + 40, "Obligations", 12.5, INK, "end", 600) + t(L - 12, cum_top + 56, "in adopted acts,", 11.5, MUTED, "end") + t(L - 12, cum_top + 70, "cumulative", 11.5, MUTED, "end"))
g.append(t(X(2026.83) + 6, ycum(cum) + 4, f"{cum:,}", 12.5, INK, "start", 600))
for v in (2000, 2010, 2020):
    c = sum(n for d, n in pts if d < v)
    g.append(f'<circle cx="{X(v):.1f}" cy="{ycum(c):.1f}" r="3" fill="{GOLD_D}"></circle>' + t(X(v) - 6, ycum(c) - 6, f"{c:,}", 11.5, INK2, "end"))
# legend
ly = H - 6
g.append(f'<line x1="{L}" x2="{L + 30}" y1="{ly - 4}" y2="{ly - 4}" stroke="{GOLD}" stroke-width="1.6" opacity="0.6"></line><circle cx="{L}" cy="{ly - 4}" r="1.8" fill="{GOLD_D}"></circle>'
         f'<circle cx="{L + 30}" cy="{ly - 4}" r="6" fill="{GOLD}"></circle>' + t(L + 42, ly, "Instrument: proposed → adopted (dot size = obligations)", 12))
open("site/policy_timeline.svg", "w").write(f'<svg viewBox="0 0 {W} {H + 4}" width="100%" role="img" aria-label="Timeline of EU digital policy, 1987 to 2028, with the 105 adopted laws">' + "".join(g) + "</svg>")
print(H, cum)
