"""Sketch-style hero illustration options for the mockup front page. Writes site/hero_options.json {key: svg}."""
import json, math

INK, CLAY, PAPER, SOFT = "#141413", "#D97757", "#F4F2EC", "#EDE6D8"


def star(cx, cy, r, pts=5):
    p = []
    for i in range(pts * 2):
        a = -math.pi / 2 + i * math.pi / pts
        rr = r if i % 2 == 0 else r * 0.42
        p.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return " ".join(p)


def wrap(key, body, w=480, h=420):
    f = f"rough-{key}"
    filt = (f'<defs><filter id="{f}" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7"></feTurbulence>'
            f'<feDisplacementMap in="SourceGraphic" scale="2.2"></feDisplacementMap></filter></defs>')
    # main stroke plus a faint offset second pass for a hand-drawn feel
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round">{filt}'
            f'<g filter="url(#{f})" stroke="{INK}" stroke-width="1.7">{body}</g>'
            f'<g filter="url(#{f})" stroke="{INK}" stroke-width="0.8" opacity="0.28" transform="translate(1.6 1.1)">{body}</g></svg>')


out = {}

# A. Star circuit: the EU ring of stars wired into a chip
cx, cy, R = 240, 210, 150
b = [f'<circle cx="{cx}" cy="{cy}" r="{R + 22}" fill="{PAPER}" stroke="none"></circle>']
for i in range(12):
    a = -math.pi / 2 + i * math.pi / 6
    sx, sy = cx + R * math.cos(a), cy + R * math.sin(a)
    # trace: radial in, then a right-angle bend onto a chip pin
    side = round(math.cos(a)) if abs(math.cos(a)) > abs(math.sin(a)) else 0
    ex = cx + 52 * max(-1, min(1, math.cos(a) * 1.6)); ey = cy + 52 * max(-1, min(1, math.sin(a) * 1.6))
    mx, my = sx + (ex - sx) * 0.55, sy + (ey - sy) * 0.55
    b.append(f'<path d="M{sx - 14 * math.cos(a):.1f},{sy - 14 * math.sin(a):.1f} L{mx:.1f},{my:.1f} L{ex if abs(math.cos(a)) > 0.7 else mx:.1f},{ey if abs(math.cos(a)) <= 0.7 else my:.1f} L{ex:.1f},{ey:.1f}"></path>')
    b.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3" fill="{INK}"></circle>')
    b.append(f'<polygon points="{star(sx, sy, 12)}" stroke="{CLAY}" fill="{CLAY}" fill-opacity="0.25"></polygon>')
b.append(f'<rect x="{cx - 52}" y="{cy - 52}" width="104" height="104" rx="8" fill="#FAF9F5"></rect>')
b.append(f'<rect x="{cx - 36}" y="{cy - 36}" width="72" height="72" rx="4" fill="{SOFT}"></rect>')
b.append(f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-family="Source Serif 4, Georgia, serif" font-size="46" fill="{INK}" stroke="none">§</text>')
out["A"] = wrap("A", "".join(b))

# B. The rulebook goes digital: an open book whose right page dissolves into circuits, an arc of stars above
b = [f'<path d="M60,300 Q150,270 238,300 L238,140 Q150,112 60,140 Z" fill="{PAPER}"></path>',
     f'<path d="M420,300 Q330,270 242,300 L242,140 Q330,112 420,140 Z" fill="{PAPER}"></path>',
     '<path d="M52,312 Q150,284 240,314 Q330,284 428,312"></path>']
for k in range(7):
    y = 160 + k * 18; w = 140 if k % 3 else 100
    b.append(f'<path d="M80,{y + 4} Q{80 + w / 2},{y - 4} {80 + w},{y + 2}" stroke-width="1.3"></path>')
b.append(f'<text x="86" y="150" font-family="Source Serif 4, Georgia, serif" font-size="18" fill="{INK}" stroke="none">Art. 1</text>')
for k in range(4):
    y = 168 + k * 18
    b.append(f'<path d="M262,{y} H{300 + k * 8}" stroke-width="1.3"></path>')
    for j in range(3):
        b.append(f'<rect x="{310 + k * 8 + j * 14}" y="{y - 4}" width="8" height="8" fill="{CLAY if (j + k) % 2 else INK}" fill-opacity="{0.8 - j * 0.2:.1f}" stroke="none"></rect>')
for (x0, y0, x1, y1) in ((300, 236, 360, 176), (330, 252, 404, 210), (280, 262, 340, 120)):
    b.append(f'<path d="M{x0},{y0} V{(y0 + y1) / 2:.0f} H{x1} V{y1}"></path><circle cx="{x1}" cy="{y1}" r="4" fill="#FAF9F5"></circle>')
for i in range(12):
    a = math.pi + i * math.pi / 11
    b.append(f'<polygon points="{star(240 + 175 * math.cos(a), 118 + 70 * math.sin(a) * 0.9, 9)}" stroke="{CLAY}" fill="{CLAY}" fill-opacity="0.25"></polygon>')
out["B"] = wrap("B", "".join(b))

# C. Temple of servers: a classical facade whose columns are server racks, stars in the pediment
b = [f'<path d="M90,150 L240,72 L390,150 Z" fill="{PAPER}"></path>', '<path d="M80,160 H400"></path>', '<path d="M80,150 H400"></path>']
for i in range(12):
    a = -math.pi / 2 + i * math.pi / 6
    b.append(f'<polygon points="{star(240 + 30 * math.cos(a), 118 + 20 * math.sin(a), 4.5)}" stroke="{CLAY}" fill="{CLAY}"></polygon>')
for c in range(4):
    x = 104 + c * 76
    b.append(f'<rect x="{x}" y="170" width="44" height="150" rx="3" fill="#FAF9F5"></rect>')
    for s in range(6):
        y = 182 + s * 23
        b.append(f'<path d="M{x + 8},{y + 6} H{x + 28}" stroke-width="1.3"></path><circle cx="{x + 35}" cy="{y + 6}" r="2.6" fill="{CLAY if (s + c) % 3 == 0 else INK}" stroke="none"></circle>')
b += ['<path d="M78,330 H402"></path>', '<path d="M66,344 H414"></path>', '<path d="M54,358 H426"></path>']
b.append('<path d="M148,320 C150,340 190,352 200,344" stroke-width="1.2"></path><path d="M300,320 C300,346 344,352 352,344" stroke-width="1.2"></path>')
out["C"] = wrap("C", "".join(b))

# D. Paper and network: a growing stack of legal pages, with a network of nodes rising from it and a star seal
b = []
for k in range(6):
    dx, dy = k * 6, -k * 9
    b.append(f'<path d="M{110 + dx},{330 + dy} L{290 + dx},{330 + dy} L{330 + dx},{280 + dy} L{150 + dx},{280 + dy} Z" fill="{PAPER if k % 2 else "#FAF9F5"}"></path>')
top_y = 330 - 5 * 9
for j in range(4):
    b.append(f'<path d="M{180 + j * 6},{top_y - 12 - j * 9} H{290 + j * 6}" stroke-width="1.2"></path>')
nodes = [(200, 200), (262, 168), (330, 196), (232, 120), (310, 110), (380, 140), (270, 66), (360, 62)]
edges = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (3, 6), (4, 7), (6, 7), (2, 5)]
b.append('<path d="M225,250 L200,200 M262,250 L262,168 M300,250 L330,196" stroke-dasharray="3 5"></path>')
for a_, b_ in edges:
    b.append(f'<path d="M{nodes[a_][0]},{nodes[a_][1]} L{nodes[b_][0]},{nodes[b_][1]}"></path>')
for i, (x, y) in enumerate(nodes):
    b.append(f'<circle cx="{x}" cy="{y}" r="{7 if i % 3 else 9}" fill="{CLAY if i in (1, 4, 7) else "#FAF9F5"}"></circle>')
sx, sy = 110, 120
b.append(f'<circle cx="{sx}" cy="{sy}" r="46" fill="{PAPER}"></circle><circle cx="{sx}" cy="{sy}" r="38" stroke-width="1.1"></circle>')
for i in range(12):
    a = -math.pi / 2 + i * math.pi / 6
    b.append(f'<polygon points="{star(sx + 26 * math.cos(a), sy + 26 * math.sin(a), 5)}" stroke="{CLAY}" fill="{CLAY}"></polygon>')
out["D"] = wrap("D", "".join(b))

json.dump(out, open("site/hero_options.json", "w"))
print({k: len(v) for k, v in out.items()})
