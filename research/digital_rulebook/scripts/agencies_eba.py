"""EBA final guidelines (document type 'Guidelines'), mapped to parent acts via legal-basis citations in the PDF."""
import json, re, sys, html as H, subprocess, tempfile, urllib.parse
sys.path.insert(0, ".")
from common import fetch
BASE = "https://www.eba.europa.eu"
items = []
TOPICS = {"All": None, "219": "32015L2366", "209": "32023R1114", "210": "32022R2554", "5219": None, "237": "32024R1624"}
for topic, hint in TOPICS.items():
  for p in range(0, 30):
    h = fetch(f"{BASE}/publications-and-media/publications?text=&document_type=250&media_topics={topic}&page={p}")
    cards = re.findall(r'calendar">([^<]+)</div>.*?teaser__title"><a href="([^"]+)">([^<]+)</a>', h, re.S)
    if not cards:
        break
    for d, u, t in cards:
        items.append({"date_text": d.strip(), "pdf": BASE + u if u.startswith("/") else u, "title": H.unescape(t).strip(),
                      "topic": topic, "topic_parent_hint": hint})
by = {}
for i in items:                       # keep the topic hint if the item appears under a specific topic
    if i["pdf"] not in by or (by[i["pdf"]]["topic_parent_hint"] is None and i["topic_parent_hint"]):
        by[i["pdf"]] = i
items = list(by.values())
items = [i for i in items if i["pdf"].lower().endswith(".pdf")]
print(len(items), "EBA guideline items; oldest:", items[-1]["date_text"] if items else None)
json.dump(items, open("../data/eba_items_raw.json", "w"), indent=1)
