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
      <a href="Studies.dc.html#evidence-map" style="align-self: flex-start; font-size: 15px; font-weight: 500; text-decoration: none; border-bottom: 1px solid #B8860B; padding-bottom: 2px">See the map for every law</a>
    </div>
  </section>
<!-- /EVIDENCE-MAP -->
'''
ST = f'''<!-- EVIDENCE-MAP -->
  <section id="evidence-map" style="padding-block: 80px; background: #F5F5F0; border-top: 1px solid #E8E6E3">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      <p class="eyebrow">Evidence map</p>
      <h2 style="font-family: 'Source Serif 4', Georgia, serif; font-weight: 400; font-size: 34px; line-height: 1.2; margin: 0">What has been studied for each law</h2>
      <p class="body">The {s["instruments"]} laws in force, by policy area and size of the rulebook, against eight kinds of effect. Each cell gives the number of sources and is coloured by the strongest one: dark gold, a causal study; light gold, another evaluation, audit, statistic or study; hatched, only the Commission's forecast; white, nothing found. Hover over a cell to see the sources.</p>
      <div style="padding-top: 8px; overflow-x: auto"><div style="min-width: 760px">{full}</div></div>
      <p class="cap" style="margin: 0; max-width: 90ch">{CAVEAT}</p>
    </div>
  </section>
<!-- /EVIDENCE-MAP -->
'''


def put(path, block, anchor):
    h = open(path).read()
    h = re.sub(r"<!-- EVIDENCE-MAP -->.*?<!-- /EVIDENCE-MAP -->\n", "", h, flags=re.S)
    i = h.index(anchor)
    h = h[:i] + block + h[i:]
    open(path, "w").write(h)


put(f"{D}/Evidence.dc.html", EV, '  <section style="padding-block: 80px">\n    <div class="wrap" style="display: flex; flex-direction: column; gap: 24px">\n      <h2 class="h2">Where the evidence')
put(f"{D}/Studies.dc.html", ST, "  <footer")
h = open(f"{D}/Studies.dc.html").read()
if "#evidence-map" not in h:
    h = h.replace("</p>\n      <div style=\"display: flex; flex-wrap: wrap; gap: 10px\" role=\"group\" aria-label=\"Collection\">",
                  ' <a href="#evidence-map" style="color: #282424; text-decoration: none; border-bottom: 1px solid #B8860B">See the evidence map</a>.</p>\n      <div style="display: flex; flex-wrap: wrap; gap: 10px" role="group" aria-label="Collection">', 1)
    open(f"{D}/Studies.dc.html", "w").write(h)
