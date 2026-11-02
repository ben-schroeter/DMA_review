"""Export the site as plain static files for an ordinary web server (HTML/PHP hosting, no build step on the server).

Reads the pages in site/mockup (the .dc.html sources), keeps only those reachable from the front page, and writes
site_export/ (and site_export.zip next to it):
  index.html (front page) and <Page>.html for every other page; links rewritten from X.dc.html to X.html
  assets/      images, copied from site/assets_blob (downloaded from the canvas; named <id>.<ext>)
  dc-lite.js   small renderer for the interactive pages (filters, toggles, infographic viewer)
  sitemap.xml, robots.txt   for search engines (base URL set with --base)
  favicon.ico/.svg, apple-touch-icon.png, icon-192/512.png, site.webmanifest   site icon (sources in site/static/icons)
Static pages become plain HTML; pages with holes ({{...}}) or logic keep their template and run dc-lite.js.
Run from research/digital_rulebook:  python3 site/export_static.py [--assets DIR] [--out DIR]"""
import argparse, datetime, json, os, re, shutil, zipfile

ap = argparse.ArgumentParser()
ap.add_argument("--assets", default="site/assets_blob")
ap.add_argument("--out", default="site_export")
ap.add_argument("--base", default="https://eutechlaws.org/")
args = ap.parse_args()

SRC = "site/mockup"
OUT = args.out

# pages reachable from the front page
seen, todo = set(), ["Main.dc.html"]
while todo:
    f = todo.pop()
    if f in seen or not os.path.exists(os.path.join(SRC, f)):
        continue
    seen.add(f)
    todo += re.findall(r"""["'(]([A-Za-z0-9_-]+\.dc\.html)""", open(os.path.join(SRC, f)).read())

out_name = lambda f: "index.html" if f == "Main.dc.html" else f.replace(".dc.html", ".html")
LINK = re.compile(r"\b([A-Za-z0-9_-]+)\.dc\.html")
fix_links = lambda s: LINK.sub(lambda m: out_name(m.group(1) + ".dc.html"), s)

assets = {os.path.splitext(a)[0]: a for a in os.listdir(args.assets)} if os.path.isdir(args.assets) else {}
missing = set()
def fix_blobs(s):
    def rep(m):
        a = assets.get(m.group(1))
        if not a:
            missing.add(m.group(1)); return m.group(0)
        return "assets/" + a
    return re.sub(r"/_blob/([0-9a-f]{32})", rep, s)

def sc_to_template(s):
    """<sc-if>/<sc-for> become <template data-sc-…> so they survive HTML parsing inside tables."""
    s = re.sub(r'<sc-if\s+value="([^"]*)"[^>]*>', r'<template data-sc-if="\1">', s)
    s = re.sub(r'<sc-for\s+list="([^"]*)"\s+as="([^"]*)"[^>]*>', r'<template data-sc-for="\1" data-as="\2">', s)
    return re.sub(r"</sc-(?:if|for)>", "</template>", s)

if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "assets"))
ICONS = ('<link rel="icon" href="favicon.ico" sizes="any">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
         '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<link rel="manifest" href="site.webmanifest">\n<meta name="theme-color" content="#FAF9F5">')
used = set()
dynamic_pages = []
for f in sorted(seen):
    s = open(os.path.join(SRC, f)).read()
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    xdc = re.search(r"<x-dc>(.*)</x-dc>", s, re.S).group(1)
    hm = re.search(r"<helmet>(.*?)</helmet>", xdc, re.S)
    helmet = hm.group(1).strip() if hm else ""
    body = xdc.replace(hm.group(0), "") if hm else xdc
    sm = re.search(r"""<script type="text/x-dc" data-dc-script data-props='([^']*)'>(.*?)</script>""", s, re.S)
    props, code = (sm.group(1), sm.group(2).strip()) if sm else ("{}", "")
    body = re.sub(r'\s+hint-[a-z-]+="[^"]*"', "", body)
    dynamic = "{{" in body or "setState" in code or "renderVals() { return {" not in code and "renderVals" in code
    body, helmet, code = (fix_blobs(fix_links(x)) for x in (body, helmet, code))
    used |= set(re.findall(r"assets/([0-9a-f]{32}\.\w+)", body + code + helmet))
    head = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n{ICONS}\n{helmet}\n</head>\n<body>\n')
    if dynamic:
        assert "</script" not in code.lower(), f
        dynamic_pages.append(out_name(f))
        page = (head + '<div id="dc-root"></div>\n<template id="dc-tpl">' + sc_to_template(body) + "</template>\n"
                + f"<script id=\"dc-logic\" type=\"text/plain\" data-props='{props}'>\n{code}\n</script>\n"
                + '<script src="dc-lite.js"></script>\n</body>\n</html>\n')
    else:
        page = head + body.strip() + "\n</body>\n</html>\n"
    open(os.path.join(OUT, out_name(f)), "w").write(page)

for a in used:
    shutil.copy(os.path.join(args.assets, a), os.path.join(OUT, "assets", a))
shutil.copy("site/static/dc-lite.js", os.path.join(OUT, "dc-lite.js"))
for ic in os.listdir("site/static/icons"):
    shutil.copy(os.path.join("site/static/icons", ic), os.path.join(OUT, ic))
open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({"name": "The EU Digital Rulebook", "short_name": "EU Rulebook",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
    "theme_color": "#FAF9F5", "background_color": "#FAF9F5", "display": "browser", "start_url": "/"}, indent=1))
open(os.path.join(OUT, "README.txt"), "w").write(
    "eutechlaws.org: static export of The EU Digital Rulebook\n\n"
    "Upload the contents of this folder to the web root of the server (for example public_html/), keeping the\n"
    "folder structure. index.html is the front page. No PHP, database or build step is needed; any web server works.\n"
    "Interactive pages (Digital Acquis list, Studies library, law pages, Infographics) use dc-lite.js.\n"
    "Fonts load from Google Fonts. Regenerate with: python3 site/export_static.py (from research/digital_rulebook).\n")

# sitemap.xml and robots.txt; lastmod = the page's "Last update" date, else today
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}
def lastmod(txt):
    m = re.search(r"Last update:\s*(\d{1,2}) (\w+) (\d{4})", txt)
    return datetime.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1))).isoformat() if m and m.group(2) in MONTHS else datetime.date.today().isoformat()
def priority(n):
    if n == "index.html": return "1.0"
    if n.startswith(("Act-", "Fc-")) or n == "Instrument.html": return "0.6"
    return "0.8"
base = args.base.rstrip("/") + "/"
urls = []
for n in sorted(os.listdir(OUT), key=lambda n: (n != "index.html", n.startswith(("Act-", "Fc-")), n)):
    if not n.endswith(".html"): continue
    loc = base if n == "index.html" else base + n
    urls.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod(open(os.path.join(OUT, n)).read())}</lastmod><priority>{priority(n)}</priority></url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                                 + "\n".join(urls) + "\n</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {base}sitemap.xml\n")

zpath = OUT.rstrip("/") + ".zip"
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, _, fs in os.walk(OUT):
        for fn in fs:
            p = os.path.join(dp, fn); z.write(p, os.path.relpath(p, OUT))
print(json.dumps({"pages": len(seen), "dynamic": len(dynamic_pages), "assets": len(used), "missing_assets": sorted(missing),
                  "sitemap_urls": len(urls), "zip": zpath, "zip_mb": round(os.path.getsize(zpath) / 1e6, 1)}))
