"""Build the single-file placeholder page (site/placeholder/index.html) from template.html,
embedding the fonts and the hero illustration as base64. Run from research/ceps_metrics/site/placeholder.
Font files: DM Sans and Source Serif 4 (SIL Open Font License), latin subset, in ./fonts."""
import base64
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
s = open("template.html").read()
for key, path in {"DMSANS400": "fonts/DMSans-400.woff", "DMSANS500": "fonts/DMSans-500.woff",
                  "SERIF400": "fonts/SourceSerif4-400.woff", "HERO": "../assets/hero3_960.webp"}.items():
    s = s.replace("{{" + key + "}}", b64(path))
assert "{{" not in s
open("index.html", "w").write(s)
print(len(s) // 1024, "KB")
