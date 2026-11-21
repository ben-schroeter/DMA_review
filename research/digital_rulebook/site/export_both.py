"""Static export with both kinds of page names: the lower-case pages (site_export, the main set, in the sitemap) plus a full
copy of every page under its original capitalised name (site_export_capitalised; Rules.html, About.html, Act-...html), each
set linking within itself. The capitalised copies carry a canonical link to their lower-case page, so search engines treat
the lower-case page as the original. Five names differ only in letter case (About/about, Forthcoming, Infographics,
Methodology, Studies): both files are kept, which is fine on a web server, but on a Mac or Windows disk one overwrites the other.
Writes site_export_both/ and site_export_both.zip. Run from research/digital_rulebook: python3 site/export_both.py"""
import json, os, re, shutil, subprocess, sys, zipfile
run = lambda *a: subprocess.run([sys.executable, "site/export_static.py", *a], check=True, capture_output=True)
run(); run("--original-names", "--out", "site_export_capitalised")
low = json.load(open("site_export_names.json")); cap = json.load(open("site_export_capitalised_names.json"))
OUT = "site_export_both"
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree("site_export", OUT)
for f in os.listdir(OUT):   # drop the small redirect pages and .htaccess rules: the full capitalised pages replace them
    p = os.path.join(OUT, f)
    if f.endswith(".html") and f not in set(low.values()) and "This page has moved to" in open(p).read():
        os.remove(p)
if os.path.exists(os.path.join(OUT, ".htaccess")): os.remove(os.path.join(OUT, ".htaccess"))
base = "https://eutechlaws.org/"
n = 0
for src, cname in cap.items():
    if cname == "index.html":
        continue
    lname = low[src]
    h = open(os.path.join("site_export_capitalised", cname)).read()
    canon = base + ("" if lname == "index.html" else lname)
    h = h.replace("</head>", f'<link rel="canonical" href="{canon}">\n</head>', 1)
    open(os.path.join(OUT, cname), "w").write(h); n += 1
open(os.path.join(OUT, "README.txt"), "a").write(
    "\nThis export also holds every page under its original capitalised name (Rules.html, About.html, Act-...html), with links\n"
    "between those copies; they point search engines to the lower-case page (canonical link). Five names differ from the\n"
    "lower-case ones only in letter case (About, Forthcoming, Infographics, Methodology, Studies): upload from a Linux machine\n"
    "or straight from the zip, as unzipping on a Mac or Windows keeps only one of each pair.\n")
z = OUT + ".zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk(OUT):
        for f in files:
            zf.write(os.path.join(root, f), os.path.relpath(os.path.join(root, f), OUT))
print(json.dumps({"lower_case_pages": len(low), "capitalised_copies": n, "zip": z, "zip_mb": round(os.path.getsize(z) / 1e6, 1)}))
