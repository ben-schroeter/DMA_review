"""EDPB guidelines and recommendations: final versions only (no public-consultation drafts)."""
import json, re, sys, html as H
sys.path.insert(0, ".")
from common import fetch
BASE = "https://www.edpb.europa.eu"
links = {}
for p in range(0, 60):
    h = fetch(f"{BASE}/our-work-tools/our-documents_en?page={p}")
    found = re.findall(r'href="(/documents/([a-z0-9\-]+)/[^"]+)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{5,300})', h)
    if not found:
        break
    for url, typ, title in found:
        links[url] = (typ, H.unescape(title).strip())
import collections
print(len(links), collections.Counter(t for t, _ in links.values()).most_common(25))
json.dump(links, open("../data/edpb_all_links.json", "w"), indent=1)
