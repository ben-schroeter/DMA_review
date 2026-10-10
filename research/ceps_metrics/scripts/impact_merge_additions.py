"""Merge data/impact/additions/found_*.json (new empirical studies from the 2026-10 broadened search) into data/impact/<CELEX>.json.
Skips duplicates by id, URL or normalised title; tags each added source with `added` = search round. Run impact_normalise.py afterwards."""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from impact_record import OUT, TODAY, wayback

KEYS = ["id", "authors", "year", "title", "venue", "url", "pdf_url", "source_type", "method", "outcomes", "direction",
        "headline", "summary_plain", "period_geography", "quality", "verified", "access", "interested_party"]
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
added, skipped, none = {}, [], []
for f in sorted(glob.glob(os.path.join(OUT, "additions", "found_*.json"))):
    for s in json.load(open(f)):
        if s.get("none_found"):
            none.append(s["celex"]); continue
        p = os.path.join(OUT, s["celex"] + ".json")
        rec = json.load(open(p))
        seen = {(l.get("id") or ""): 1 for l in rec["literature"]}
        urls = {(l.get("url") or "").rstrip("/") for l in rec["literature"]}
        titles = {norm(l.get("title")) for l in rec["literature"]}
        if s["id"] in seen or s["url"].rstrip("/") in urls or norm(s["title"]) in titles:
            skipped.append((s["celex"], s["title"])); continue
        l = {k: s.get(k, "") for k in KEYS}
        l["citation"] = f'{l["authors"]} ({l["year"]}), {l["title"]}, {l["venue"]}'
        l["accessed"] = TODAY
        l["archive_url"] = wayback(l["url"]) if "--wayback" in sys.argv else ""
        l["added"] = "2026-10 broadened search"
        rec["literature"].append(l)
        rec["last_reviewed"] = TODAY
        json.dump(rec, open(p, "w"), indent=1, ensure_ascii=False)
        added[s["celex"]] = added.get(s["celex"], 0) + 1
print("added", sum(added.values()), "sources to", len(added), "acts; skipped duplicates", len(skipped), "; none found for", len(set(none)))
for c, n in sorted(added.items(), key=lambda x: -x[1]):
    print(" ", c, n)
for c, t in skipped:
    print("  dup:", c, t[:80])
