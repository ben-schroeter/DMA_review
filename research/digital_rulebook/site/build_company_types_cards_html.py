"""Company types page: the six type cards (headline count, growth since 2018, laws, reporting, share in implementing and
delegated acts, share adopted since 2020, top laws, and the small chart), from data/company_types/summary.json and
site/company_types_cards.json. Writes site/company_types_cards.html. Run from research/digital_rulebook."""
import json, re
S = json.load(open("data/company_types/summary.json")); SVG = json.load(open("site/company_types_cards.json"))
ORDER = ["PR", "FI", "GK", "CL", "TC", "PL"]
TEXT = {
 "PR": [
  "Makers of connected products",
  "Philips, Bosch, Siemens, phone and toy makers, importers",
  "Manufacturers, importers and distributors of machinery, radio equipment, toys and other products with digital elements."
 ],
 "FI": [
  "Finance, payments and crypto",
  "Banks, Adyen, Klarna, Revolut, Trade Republic, crypto exchanges",
  "Payment and e-money firms, crypto-asset issuers and service providers, and financial entities under DORA and anti-money-laundering rules."
 ],
 "GK": [
  "Gatekeepers and very large platforms",
  "Amazon, Google, Meta, Apple, Booking, Zalando",
  "Designated gatekeepers under the Digital Markets Act and very large platforms under the Digital Services Act. Most of what applies to online platforms applies to them too, plus their own tier."
 ],
 "CL": [
  "Cloud, data and AI",
  "AWS, Microsoft Azure, OVHcloud, Mistral, data intermediaries",
  "Cloud and data processing services, data intermediaries, providers of AI models and systems, and ICT suppliers to financial firms."
 ],
 "TC": [
  "Telecoms",
  "Deutsche Telekom, Orange, Telefónica, Vodafone, KPN",
  "Mobile and fixed network operators and internet access providers."
 ],
 "PL": [
  "Online platforms and digital services",
  "Uber, Bolt, Vinted, Airbnb, Deliveroo, app developers",
  "Marketplaces, gig and booking platforms, hosting and other online services below the very-large thresholds."
 ]
}
EXTRA = {"GK": '. Of the 1,452, 1,033 are the rules for all online platforms and 419 apply only to gatekeepers and very large platforms.'}   # split of the gatekeeper count, from data/company_types/matrix.csv
B = S["types"]["B"]["obligations"] if "B" in S["types"] else S["baseline"]["obligations"]
out = []
for k in ORDER:
    t = S["types"][k]; title, ex, desc = TEXT[k]; n = t["obligations"]
    SHORT = {"Digital Services Act": "DSA", "Digital Markets Act": "DMA", "Artificial Intelligence Act": "AI Act", "NIS 2 Directive": "NIS 2", "European Electronic Communications Code": "Electronic Communications Code"}
    short = lambda a: SHORT.get(a) or (re.search(r"\(([A-Za-z0-9]+)\)$", a).group(1) if re.search(r"\(([A-Za-z0-9]+)\)$", a) else a)
    top = ", ".join(f"{short(a)} ({b:,})" for a, b in list(t["top_laws"].items())[:4])
    out.append(f'''<div style="border: 1px solid #E8E6E3; border-radius: 12px; padding: 24px; background: #FFFFFF; display: flex; flex-direction: column; gap: 10px">
          <h3 style="font-family: 'Source Serif 4', Georgia, serif; font-weight: 400; font-size: 22px; line-height: 1.25; margin: 0">{title}</h3>
          <p class="cap" style="margin: 0">{ex}</p>
          <div style="display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap"><span class="num" style="font-size: 34px">{n:,}</span><span style="font-size: 14px; font-weight: 600; color: #8F6708">{(("×" + (f"{n / t['start_2018']:.0f}" if n / t['start_2018'] >= 10 else f"{n / t['start_2018']:.1f}") + " since 2018") if t["start_2018"] else "new since 2018")}</span></div>
          <p class="cap" style="margin: 0">obligations specific to this type, from {t["laws"]} laws, plus {B:,} that apply to every company{EXTRA.get(k, "")}</p>
          <p style="margin: 0; font-size: 15px; color: #3F3B3B; line-height: 1.5">{desc}</p>
          <dl style="margin: 0; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 6px 12px; font-size: 14px; border-top: 1px solid #E8E6E3; padding-top: 12px">
            <dt style="color: #666666">Reporting obligations</dt><dd style="margin: 0; font-weight: 600">{t["reporting"]:,}</dd>
            <dt style="color: #666666">In implementing and delegated acts</dt><dd style="margin: 0; font-weight: 600">{t["in_implementing_delegated"] / n:.0%}</dd>
            <dt style="color: #666666">Adopted since 2020</dt><dd style="margin: 0; font-weight: 600">{t["since_2020"] / n:.0%}</dd>
          </dl>
          <p class="cap" style="margin: 0"><strong style="color: #282424; font-weight: 500">Most obligations from:</strong> {top}</p>
          <div style="margin-top: auto; padding-top: 10px; border-top: 1px solid #E8E6E3">{SVG[k]}</div>
        </div>''')
open("site/company_types_cards.html", "w").write("".join(out))
print(len(out))
