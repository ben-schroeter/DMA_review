"""Backfill empty archive_url fields (read-only Wayback availability API) and rebuild the Done list in PROGRESS.md from data/impact/*.json."""
import glob, json, os, re, time
from impact_record import wayback, OUT

files = sorted(glob.glob(os.path.join(OUT, "[35]*.json")))
filled = 0
for f in files:
    rec = json.load(open(f)); changed = False
    for l in rec["literature"]:
        if not l.get("archive_url") and l.get("url"):
            u = wayback(l["url"]); time.sleep(1)
            if u:
                l["archive_url"] = u; changed = True; filled += 1
    if changed:
        json.dump(rec, open(f, "w"), indent=1, ensure_ascii=False)
p = os.path.join(OUT, "PROGRESS.md")
txt = open(p).read().split("## Done")[0]
done = [f"- [x] {json.load(open(f))['celex']} {json.load(open(f))['name']}" for f in files]
open(p, "w").write(txt + "## Done\n" + "\n".join(done) + "\n")
print("records", len(files), "archive urls filled", filled)
