import re
us="site/mockup/UsComparison.dc.html"; s=open(us).read()
a=s.index('\n      <h2 class="h2" style="max-width: 26ch; padding-top: 48px">Rules or standards?')
b=s.index('</p>', s.index('<strong style="color: #282424; font-weight: 600">How we coded.</strong>'))+4
cap_old=s[s.index('<strong style="color: #282424; font-weight: 600">How we coded.</strong>'):b-4]
s=s[:a]+s[b:]
s=s.replace('"height":4800}','"height":2900}')
open(us,"w").write(s)
svg=open("site/rules_standards.svg").read()
cap=cap_old.replace("The lower chart shows laws with at least 60 obligations in their implementing and delegated acts and at least 50 in the main act.",
 "Obligations on companies: those whose addressee is a company, its officers or its staff, coded as elsewhere on this site. The lower chart shows laws with at least 60 obligations in their implementing and delegated acts and at least 50 in the main act; the line for companies is shown where both sides have at least 20.")
assert cap!=cap_old
block=f'''  <section style="padding-block: 80px; background: #F5F5F0; border-top: 1px solid #E8E6E3; border-bottom: 1px solid #E8E6E3">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 28px">
      <h2 class="h2" style="max-width: 26ch">Rules or standards? Three in four EU obligations are rules, and the second layer adds more</h2>
      <p class="body">Louis Kaplow distinguishes rules, whose content is fixed before people act ("notify within 72 hours"), from standards, whose content is decided afterwards by a regulator or court ("take appropriate measures"). Read obligation by obligation, 73% of those in the 105 EU digital laws are rules and 25% are standards. Obligations on companies look much the same: 72% rules. In the implementing and delegated acts that follow, 84% are rules, and 83% of those on companies: in 26 of the 30 laws with a sizeable second layer, the Commission's follow-up acts turn open terms into fixed ones. For companies the shift is largest in the Ecodesign Regulation (65% to 94%), the Cybersecurity Act (62% to 88%) and DORA (55% to 81%). NIS2 is the main exception: its implementing rules on security measures keep the "appropriate measures" style, and the share of rules for companies falls from 75% to 52%.</p>
      <div style="overflow-x: auto"><div style="min-width: 760px">{svg}</div></div>
      <p class="cap" style="margin: 0; max-width: 95ch">{cap}</p>
    </div>
  </section>

'''
r="site/mockup/Rules.dc.html"; t=open(r).read()
i=t.index('  <footer'); t=t[:i]+block+t[i:]
t=t.replace('"height":7760}','"height":9300}')
open(r,"w").write(t)
c=open("site/mockup/canvas.json").read()
for name,old,new in (("UsComparison.dc.html","4800","2900"),("Rules.dc.html","7760","9300")):
    i=c.index(f'"{name}": {{'); j=c.index(f'"h": {old}',i); c=c[:j]+f'"h": {new}'+c[j+len(old)+5:]
open("site/mockup/canvas.json","w").write(c)
import json; json.loads(c); print("ok")
