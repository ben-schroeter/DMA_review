"""Insert the evidence map SVGs into the Evidence and Studies pages (between EVIDENCE-MAP markers; idempotent).
Usage: python3 site/insert_evidence_map.py <dir with Evidence.dc.html and Studies.dc.html>"""
import re, sys, json
D = sys.argv[1]
s = json.load(open("data/evidence_map/summary.json"))
compact, full = open("site/evidence_map_compact.svg").read(), open("site/evidence_map_full.svg").read()
CAVEAT = ("An empty cell means our searches found nothing, not that nothing exists. Counts are not quality, and one source can count "
          "for several effects. We sorted sources into effects by keywords on the outcomes recorded for each; a hand check of 150 "
          "found 86% tagged correctly before we fixed the commonest errors. Enforcement decisions and court rulings are not counted.")
EV = f'''<!-- EVIDENCE-MAP -->
  <section style="padding-block: 80px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      <h2 class="h2">Most effects of most laws have never been measured</h2>
      <p class="body">We sorted every study and forecast by the kind of effect it looks at. Of {s["pairs"]} pairs of law and effect, {s["pairs_evidence"]} have any evidence from after adoption and {s["pairs_causal"]} have a causal study. For the five economic effects (costs, prices, competition, innovation and growth), {s["core_evidence"]} of {s["core_pairs"]} pairs have been looked at after adoption, {s["core_causal"]} with a causal design. What gets checked most is whether a law was implemented, not what it did.</p>
      <div style="padding-top: 8px; overflow-x: auto"><div style="min-width: 760px">{compact}</div></div>
      <p class="cap" style="margin: 0; max-width: 90ch">Each bar shows the laws in a policy area that are now in force: dark gold, at least one causal study on that effect; light gold, other evaluations, audits, statistics or studies; hatched, only the Commission's forecast; white, nothing found. Hover over a bar to see the laws. {CAVEAT}</p>
      <a href="EvidenceMap.dc.html" style="align-self: flex-start; font-size: 15px; font-weight: 500; text-decoration: none; border-bottom: 1px solid #B8860B; padding-bottom: 2px">See the map for every law</a>
    </div>
  </section>
<!-- /EVIDENCE-MAP -->
'''
TABS = lambda cur: ('<nav aria-label="Studies" style="display: flex; flex-wrap: wrap; gap: 10px">\n        '
    + "\n        ".join(f'<a class="tab" href="{f}"' + (' style="background: #282424; color: #FAF9F5; border-color: #282424" aria-current="page"' if f == cur else "") + f'>{n}</a>'
                       for f, n in [("Studies.dc.html", "Library"), ("EvidenceMap.dc.html", "Evidence map")]) + "\n      </nav>\n      ")
TAB_CSS = ".tab{text-decoration:none;font-size:15px;padding:8px 14px;border-radius:999px;border:1px solid #D4D2CE;color:#3F3B3B;min-height:44px;box-sizing:border-box;display:inline-flex;align-items:center}"
PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Evidence map: The EU Digital Rulebook</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&amp;family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&amp;display=swap">
<style>
body{{margin:0;background:#FAF9F5;color:#282424;font-family:'DM Sans',ui-sans-serif,system-ui,sans-serif;font-size:17px;line-height:1.6;font-variant-numeric:tabular-nums}}
a{{color:#282424}}a:hover{{color:#8F6708}}
.wrap{{max-width:1120px;margin:0 auto;padding-inline:32px}}
.eyebrow{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#666666;margin:0}}
.h1{{font-family:'Source Serif 4',Georgia,serif;font-weight:400;font-size:56px;line-height:1.05;letter-spacing:-.02em;margin:0;text-wrap:balance}}
.body{{color:#3F3B3B;margin:0;max-width:68ch}}
.cap{{font-size:14px;color:#666666;line-height:1.45}}
.nav a{{text-decoration:none;font-size:15px;color:#3F3B3B}}
.nav a:hover{{color:#282424}}
{TAB_CSS}
@media (max-width:640px){{.wrap{{padding-inline:20px}}.h1{{font-size:40px}}}}
@media (max-width:640px){{.nav{{width:100%;justify-content:space-between;gap:10px !important}}.nav a{{font-size:14px}}}}
</style>
</helmet>
<div style="width: 100%; background: #FAF9F5">
HEADER
  <section style="padding-block: 64px 32px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      {TABS("EvidenceMap.dc.html")}<p class="eyebrow">Studies · Evidence map</p>
      <h1 class="h1">What has been studied for each law</h1>
      <p class="body" style="font-size: 19px">The {s["instruments"]} laws in force, grouped by policy area and ordered by the size of their rulebook, against eight kinds of effect. Of {s["pairs"]} pairs of law and effect, {s["pairs_evidence"]} have any evidence from after adoption and {s["pairs_causal"]} have a causal study.</p>
      <p class="body">Each cell gives the number of sources and is coloured by the strongest one: dark gold, a causal study; light gold, another evaluation, audit, statistic or study; hatched, only the Commission's forecast; white, nothing found. Hover over a cell to see the sources, and find them in the <a href="Studies.dc.html">library</a>.</p>
    </div>
  </section>

  <section style="padding-block: 8px 80px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      <div style="overflow-x: auto"><div style="min-width: 760px">{full}</div></div>
      <p class="cap" style="margin: 0; max-width: 90ch">{CAVEAT}</p>
    </div>
  </section>

  <footer style="border-top: 1px solid #E8E6E3">
    <div class="wrap" style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 24px; padding-block: 40px">
      <span class="cap"><a href="https://eutechlaws.org" style="color: #8F6708; font-weight: 500; text-decoration: none">eutechlaws.org</a> · Data as of October 2026.</span>
      <a href="Data.dc.html" style="font-size: 15px">Download all sources →</a>
    </div>
  </footer>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":3800}}}}'>
class Component extends DCLogic {{ renderVals() {{ return {{}}; }} }}
</script>
</body>
</html>
"""
def put(path, block, anchor):
    h = open(path).read()
    h = re.sub(r"<!-- EVIDENCE-MAP -->.*?<!-- /EVIDENCE-MAP -->\n", "", h, flags=re.S)
    i = h.index(anchor)
    h = h[:i] + block + h[i:]
    open(path, "w").write(h)


put(f"{D}/Evidence.dc.html", EV, '  <section style="padding-block: 80px">\n    <div class="wrap" style="display: flex; flex-direction: column; gap: 24px">\n      <h2 class="h2">Where the evidence')
st = open(f"{D}/Studies.dc.html").read()
st = re.sub(r"<!-- EVIDENCE-MAP -->.*?<!-- /EVIDENCE-MAP -->\n", "", st, flags=re.S)
st = st.replace(' <a href="#evidence-map"', ' <a href="EvidenceMap.dc.html"')
if 'href="EvidenceMap.dc.html">Evidence map</a>' not in st:
    st = st.replace('<p class="eyebrow">Studies</p>', TABS("Studies.dc.html") + '<p class="eyebrow">Studies · Library</p>', 1)
    st = st.replace(".seg{", TAB_CSS + "\n.seg{", 1)
open(f"{D}/Studies.dc.html", "w").write(st)
header = re.search(r"  <header.*?</header>\n", st, re.S).group(0)
open(f"{D}/EvidenceMap.dc.html", "w").write(PAGE.replace("HEADER\n", header))
