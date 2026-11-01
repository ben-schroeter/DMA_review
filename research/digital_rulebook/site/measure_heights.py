"""Measures each canvas page at 1440 px wide and writes the height into the page ($preview) and into canvas.json.
Needs node with playwright (site/tools/measure.js). Run from research/digital_rulebook."""
import json, re, os, subprocess, glob
KEEP = {"Instruments.dc.html", "Studies.dc.html", "EvidenceMap.dc.html", "HeroOptions.dc.html", "Infographics.dc.html"}   # interactive pages sized by hand
pages = [p for p in sorted(glob.glob("site/mockup/*.dc.html")) if os.path.basename(p) not in KEEP and not os.path.basename(p).startswith("Infographic")]
root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
H = {}
for i in range(0, len(pages), 40):
    out = subprocess.run(["node", "site/tools/measure.js", *pages[i:i + 40]], capture_output=True, text=True, env={**os.environ, "NODE_PATH": root}, cwd=".")
    H.update({os.path.basename(k): v + 20 for k, v in json.loads(out.stdout).items()})
c = json.load(open("site/mockup/canvas.json")); B = c["boards"]; over = []
for f, h in H.items():
    if h > 8000: over.append((f, h)); h = 8000
    p = f"site/mockup/{f}"; s = open(p).read()
    s2 = re.sub(r'("\$preview":\{"width":1440,"height":)\d+', lambda m: m.group(1) + str(h), s)
    if s2 != s: open(p, "w").write(s2)
    if f in B: B[f]["h"] = h
json.dump(c, open("site/mockup/canvas.json", "w"), indent=2)
print(f"measured {len(H)} pages" + (f"; capped at 8000: {over}" if over else ""))
