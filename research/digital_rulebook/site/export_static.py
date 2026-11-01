"""Export the site as plain static files for an ordinary web server (HTML/PHP hosting, no build step on the server).

Reads the pages in site/mockup (the .dc.html sources), keeps only those reachable from the front page, and writes
site_export/ (and site_export.zip next to it):
  index.html (front page) and <Page>.html for every other page; links rewritten from X.dc.html to X.html
  assets/      images, copied from site/assets_blob (downloaded from the canvas; named <id>.<ext>)
  dc-lite.js   small renderer for the interactive pages (filters, toggles, infographic viewer)
Static pages become plain HTML; pages with holes ({{...}}) or logic keep their template and run dc-lite.js.
Run from research/digital_rulebook:  python3 site/export_static.py [--assets DIR] [--out DIR]"""
import argparse, json, os, re, shutil, zipfile

ap = argparse.ArgumentParser()
ap.add_argument("--assets", default="site/assets_blob")
ap.add_argument("--out", default="site_export")
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
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{title}</title>\n{helmet}\n</head>\n<body>\n')
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
open(os.path.join(OUT, "README.txt"), "w").write(
    "eutechlaws.org: static export of The EU Digital Rulebook\n\n"
    "Upload the contents of this folder to the web root of the server (for example public_html/), keeping the\n"
    "folder structure. index.html is the front page. No PHP, database or build step is needed; any web server works.\n"
    "Interactive pages (Digital Acquis list, Studies library, law pages, Infographics) use dc-lite.js.\n"
    "Fonts load from Google Fonts. Regenerate with: python3 site/export_static.py (from research/digital_rulebook).\n")

zpath = OUT.rstrip("/") + ".zip"
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, _, fs in os.walk(OUT):
        for fn in fs:
            p = os.path.join(dp, fn); z.write(p, os.path.relpath(p, OUT))
print(json.dumps({"pages": len(seen), "dynamic": len(dynamic_pages), "assets": len(used), "missing_assets": sorted(missing),
                  "zip": zpath, "zip_mb": round(os.path.getsize(zpath) / 1e6, 1)}))
