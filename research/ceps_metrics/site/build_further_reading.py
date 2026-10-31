"""Builds the Studies > Further reading page (site/mockup/FurtherReading.dc.html) from the list below and adds the tab to the
other Studies pages. To add an entry, append it to READING. Run from research/ceps_metrics."""
import html, re

READING = {
    "Books": [
        {"title": "Digital Policy in the EU: Towards a Human-Centred Digital Transformation", "by": "Werner Stengg", "where": "Edward Elgar, 2024",
         "url": "https://www.e-elgar.com/shop/gbp/digital-policy-in-the-eu-9781035338634.html", "cover": "/_blob/74438afe7d7b4c65daf8d02a7e39f8bc",
         "note": "A guide to the EU's digital policy agenda and the thinking behind it."},
        {"title": "The Making of a Global Digital Rulebook: Digital Sovereignty and International Action in the EU", "by": "Edited by Thibaut Kleiner and Andrea G. Rodríguez",
         "where": "Palgrave Macmillan, 2026 · open access", "cover": "/_blob/c4d444b05b932e29af50ed0358d90e4f", "url": "https://link.springer.com/book/10.1007/978-981-95-9226-5",
         "note": "How the EU's digital rules are shaped by, and exported through, its international action."},
        {"title": "Big Tech and the Digital Economy: The Moligopoly Scenario", "by": "Nicolas Petit", "where": "Oxford University Press, 2020",
         "url": "https://global.oup.com/academic/product/big-tech-and-the-digital-economy-9780198837701", "cover": "/_blob/5b60159e45305c298e942c2ab6d8c309",
         "note": "Argues that the big tech firms are monopolists in their core markets but compete with each other, and draws the lessons for antitrust and regulation."},
        {"title": "Technology and the Rise of Great Powers: How Diffusion Shapes Economic Competition", "by": "Jeffrey Ding", "where": "Princeton University Press, 2024", "cover": "/_blob/090a2999ce3de181a48dccb6aeeb9075",
         "url": "https://press.princeton.edu/books/hardcover/9780691260334/technology-and-the-rise-of-great-powers",
         "note": "Shows that how widely an economy adopts general-purpose technologies matters more for its rise than who invents them first."},
        {"title": "Digital Empires: The Global Battle to Regulate Technology", "by": "Anu Bradford", "where": "Oxford University Press, 2023",
         "url": "https://global.oup.com/academic/product/digital-empires-9780197649268", "cover": "/_blob/ef320f6e9fafae364ace9556d5f18575",
         "note": "Compares the American market-driven, Chinese state-driven and European rights-driven models of regulating technology, and makes the case for Europe's."},
        {"title": "The Power of Creative Destruction: Economic Upheaval and the Wealth of Nations", "by": "Philippe Aghion, Céline Antonin and Simon Bunel",
         "where": "Harvard University Press, 2021", "url": "https://www.hup.harvard.edu/books/9780674292093", "cover": "/_blob/a47b02f3360f19175bb1233486b00c36",
         "note": "Innovation-led growth, why it needs competition, and what role the state should play in it."},
    ],
    "Blogs and newsletters": [
        {"title": "Silicon Continent", "by": "Pieter Garicano", "where": "Substack",
         "url": "https://www.siliconcontinent.com/", "cover": "/_blob/d19786e4191c6d1b032e6ff54a62cc0e",
         "note": "Essays on Europe, economics, innovation and growth, with a sharp eye on what regulation costs."},
        {"title": "Benedict's Newsletter", "by": "Benedict Evans", "where": "Weekly newsletter",
         "url": "https://www.ben-evans.com/newsletter",
         "note": "What mattered in tech this week: strategy, with a running commentary on regulation."},
        {"title": "Stratechery", "by": "Ben Thompson", "where": "Newsletter",
         "url": "https://stratechery.com/", "cover": "/_blob/380cc95385959a251848924e417b3539",
         "note": "On the business, strategy and impact of technology, including how platforms respond to regulation."},
        {"title": "Works in Progress", "by": "Works in Progress", "where": "Magazine",
         "url": "https://worksinprogress.co/", "cover": "/_blob/806f7e8089d9af85e9cf5ba2c79e8f08",
         "note": "New and underrated ideas to improve the world, from housing to science funding to regulation."},
        {"title": "MDM", "by": "Eric Seufert", "where": "Newsletter",
         "url": "https://mdm.co/", "cover": "/_blob/f9a85a4c11ffbe8d17acbd7212b2ee1f",
         "note": "Independent analysis of the digital economy, especially advertising, and what privacy and platform rules do to it."},
    ],
    "Studies and papers": [
        {"title": "The Constitution of Innovation", "by": "Luis Garicano, Bengt Holmström and Nicolas Petit", "where": "Academic paper",
         "url": "https://constitutionofinnovation.eu/", "cover": "/_blob/3e006eac1ba7fdad17c7d8bbb358a278",
         "note": "Why Europe struggles to innovate, and a proposal for a new constitutional framework for its economy."},
        {"title": "A dataset of EU legal and policy instruments for the digital world", "by": "Kai Zenner and J. Scott Marcus", "where": "CEPS, 2025", "short": "EU digital instruments",
         "url": "https://www.ceps.eu/ceps-publications/a-dataset-of-eu-legal-and-policy-instruments-for-the-digital-world/",
         "note": "The inventory of 115 EU digital instruments that this site's list of laws builds on."},
        {"title": "The Future of European Competitiveness", "by": "Mario Draghi", "where": "European Commission, 2024",
         "url": "https://commission.europa.eu/topics/eu-competitiveness/draghi-report_en", "cover": "/_blob/8df0da5f31f353995a258af2dfc25d16",
         "note": "The reference point for the productivity argument on the Why it matters page."},
        {"title": "Much More Than a Market", "by": "Enrico Letta", "where": "Report to the European Council, 2024",
         "url": "https://www.consilium.europa.eu/media/ny3j24sm/much-more-than-a-market-report-by-enrico-letta.pdf", "cover": "/_blob/ea1074e01fbb368df5b0d9198da9da75",
         "note": "The single-market companion to the Draghi report."},
        {"title": "Competition Policy for the Digital Era", "by": "Jacques Crémer, Yves-Alexandre de Montjoye and Heike Schweitzer", "where": "European Commission, 2019",
         "url": "https://op.europa.eu/en/publication-detail/-/publication/21dc175c-7b76-11e9-9f05-01aa75ed71a1/language-en", "cover": "/_blob/c3d04ff32479e81ed26b88d62116afb2",
         "note": "The expert report behind much of the Digital Markets Act's thinking."},
        {"title": "EU Innovation Policy: How to Escape the Middle Technology Trap", "by": "Clemens Fuest, Daniel Gros, Philipp-Leo Mengel, Giorgio Presidente and Jean Tirole",
         "where": "European Policy Analysis Group (EconPol, Bocconi, TSE), 2024", "url": "https://www.ifo.de/en/econpol/publications/2024/working-paper/eu-innovation-policy-how-escape-middle-technology-trap", "cover": "/_blob/b2896db0c60c259cfdc7048910b765dc",
         "note": "Why EU firms are stuck in mid-tech industries, and what innovation policy could do about it."},
    ],
}
esc = lambda s: html.escape(s, quote=True)
TABS = [("Studies.dc.html", "Library"), ("EvidenceMap.dc.html", "Evidence map"), ("FurtherReading.dc.html", "Further reading")]


def tabs(cur):
    return ('<nav aria-label="Studies" style="display: flex; flex-wrap: wrap; gap: 10px">\n'
            + "\n".join(f'        <a class="tab" href="{f}"' + (' style="background: #282424; color: #FAF9F5; border-color: #282424" aria-current="page"' if f == cur else "")
                        + f'>{n}</a>' for f, n in TABS) + "\n      </nav>")


def cover(e):
    if e.get("cover"):
        return f'<img class="rd-cover" src="{e["cover"]}" alt="" loading="lazy">'
    words = e.get("short") or e["title"].split(":")[0]
    return f'<span class="rd-cover rd-ph" aria-hidden="true"><span>{esc(words)}</span><span class="rd-ph-by">{esc(e["by"].split(",")[0].split(" and ")[0])}</span></span>'


def card(e, book=False):
    if book:
        return (f'<a class="rd rd-book" href="{esc(e["url"])}" target="_blank" rel="noopener">{cover(e)}<span class="rd-body">'
                f'<span class="rd-where">{esc(e["where"])}</span><span class="rd-title">{esc(e["title"])}</span>'
                f'<span class="rd-by">{esc(e["by"])}</span><span class="rd-note">{esc(e["note"])}</span><span class="rd-go">Open ↗</span></span></a>')
    return (f'<a class="rd" href="{esc(e["url"])}" target="_blank" rel="noopener">'
            f'<span class="rd-where">{esc(e["where"])}</span>'
            f'<span class="rd-title">{esc(e["title"])}</span>'
            f'<span class="rd-by">{esc(e["by"])}</span>'
            f'<span class="rd-note">{esc(e["note"])}</span>'
            f'<span class="rd-go">Open ↗</span></a>')


sections = "\n".join(
    f'''  <section style="padding-block: 8px 48px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 18px">
      <h2 class="h2">{esc(name)}</h2>
      <div class="rds rds-books{' rds-sq' if name.startswith('Blogs') else ''}">{"".join(card(e, True) for e in items)}</div>
    </div>
  </section>''' for name, items in READING.items())

studies = open("site/mockup/Studies.dc.html").read()
header = re.search(r"  <header.*?</header>\n", studies, re.S).group(0)
footer = re.search(r"  <footer.*?</footer>\n", studies, re.S).group(0)
footer = footer.replace("Mockup: collection switches are illustrative; the causal set is shown.", "Data as of October 2026.").replace('<a href="Data.dc.html" style="font-size: 15px">Download all sources →</a>', '<a href="Studies.dc.html" style="font-size: 15px">Browse the evidence library →</a>')
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Further reading: The EU Digital Rulebook</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&amp;family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&amp;display=swap">
<style>
body{{margin:0;background:#FAF9F5;color:#282424;font-family:'DM Sans',ui-sans-serif,system-ui,sans-serif;font-size:17px;line-height:1.6}}
a{{color:#282424}}a:hover{{color:#8F6708}}
.wrap{{max-width:1120px;margin:0 auto;padding-inline:32px}}
.eyebrow{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#666666;margin:0}}
.h1{{font-family:'Source Serif 4',Georgia,serif;font-weight:400;font-size:56px;line-height:1.05;letter-spacing:-.02em;margin:0}}
.h2{{font-family:'Source Serif 4',Georgia,serif;font-weight:400;font-size:28px;line-height:1.2;margin:0}}
.body{{color:#3F3B3B;margin:0;max-width:68ch}}
.cap{{font-size:14px;color:#666666;line-height:1.45}}
.nav a{{text-decoration:none;font-size:15px;color:#3F3B3B}}
.nav a:hover{{color:#282424}}
.tab{{text-decoration:none;font-size:15px;padding:8px 14px;border-radius:999px;border:1px solid #D4D2CE;color:#3F3B3B;min-height:44px;box-sizing:border-box;display:inline-flex;align-items:center}}
.rds{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}
.rd{{display:flex;flex-direction:column;gap:8px;padding:22px 24px;border:1px solid #E8E6E3;border-radius:12px;background:#FFFFFF;text-decoration:none;color:#282424;transition:border-color .15s ease,box-shadow .15s ease}}
.rd:hover,.rd:focus-visible{{border-color:#B8860B;box-shadow:0 6px 20px rgba(40,36,36,.08);color:#282424}}
.rd:focus-visible{{outline:2px solid #B8860B;outline-offset:3px}}
.rd-where{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#666666}}
.rd-title{{font-family:'Source Serif 4',Georgia,serif;font-size:21px;line-height:1.25}}
.rd-by{{font-size:14.5px;font-weight:500;color:#3F3B3B}}
.rd-note{{font-size:15px;line-height:1.5;color:#3F3B3B}}
.rd-go{{margin-top:auto;padding-top:6px;font-size:14px;font-weight:500;color:#8F6708}}
.rds-books{{grid-template-columns:repeat(auto-fill,minmax(420px,1fr))}}
.rd-book{{flex-direction:row;gap:20px;align-items:flex-start}}
.rd-body{{display:flex;flex-direction:column;gap:8px;min-width:0;align-self:stretch}}
.rd-cover{{flex:none;width:84px;height:126px;object-fit:cover;border-radius:3px;box-shadow:0 2px 8px rgba(40,36,36,.18);background:#E8E6E3}}
.rd-ph{{display:flex;flex-direction:column;justify-content:space-between;box-sizing:border-box;padding:10px 8px;background:#282424;color:#FAF9F5;font-family:'Source Serif 4',Georgia,serif;font-size:12.5px;line-height:1.2;border-top:4px solid #B8860B;overflow:hidden}}
.rds-sq .rd-cover{{height:84px}}
.rds-sq .rd-ph{{font-size:12px}}
.rd-ph-by{{font-family:'DM Sans',sans-serif;font-size:10px;color:#E3CF9C;letter-spacing:.02em}}
@media (max-width:520px){{.rds-books{{grid-template-columns:1fr}}.rd-cover{{width:64px;height:96px}}.rds-sq .rd-cover{{height:64px}}}}
@media (max-width:640px){{.wrap{{padding-inline:20px}}.h1{{font-size:40px}}}}
@media (max-width:640px){{.nav{{width:100%;justify-content:space-between;gap:10px !important}}.nav a{{font-size:14px}}}}
</style>
</helmet>
<div style="width: 100%; background: #FAF9F5">
{header}
  <section style="padding-block: 64px 32px">
    <div class="wrap" style="display: flex; flex-direction: column; gap: 20px">
      {tabs("FurtherReading.dc.html")}
      <p class="eyebrow">Studies · Further reading</p>
      <h1 class="h1">Further reading</h1>
      <p class="body" style="font-size: 19px">Blogs, studies and books we recommend on EU digital policy, regulation and Europe's innovation gap. They span different views; inclusion is not endorsement of every argument.</p>
    </div>
  </section>

{sections}

{footer}</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":3300}}}}'>
class Component extends DCLogic {{ renderVals() {{ return {{}}; }} }}
</script>
</body>
</html>
"""
open("site/mockup/FurtherReading.dc.html", "w").write(page)
# add the tab to the other Studies pages
for f in ("Studies.dc.html", "EvidenceMap.dc.html"):
    p = f"site/mockup/{f}"; h = open(p).read()
    h2 = re.sub(r'<nav aria-label="Studies".*?</nav>', tabs(f), h, count=1, flags=re.S)
    if h2 != h:
        open(p, "w").write(h2)
print("ok", sum(len(v) for v in READING.values()), "entries")
