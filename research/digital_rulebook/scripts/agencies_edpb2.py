"""Classify EDPB guidelines/recommendations as final vs consultation draft; pick English PDF; map to parent act."""
import json, re, sys, html as H
sys.path.insert(0, ".")
from common import fetch
BASE = "https://www.edpb.europa.eu"
L = json.load(open("../data/edpb_all_links.json"))
out = []
for u, (typ, _) in L.items():
    if typ not in ("guideline", "recommendation"):
        continue
    h = fetch(BASE + u)
    title = H.unescape(re.search(r"<title>(.*?)\|", h, re.S).group(1)).strip() if "<title>" in h else u
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", h, flags=re.S)))
    pdfs = list(dict.fromkeys(x for x in re.findall(r'href="([^"]+\.pdf)"', h) if x.startswith("/")))
    main = [p for p in pdfs if re.search(r"_en\.pdf$|-en\.pdf$|_en_|en\.pdf$", p) and not re.search(r"summary|report|annex|statement|glance|consultation/", p, re.I)]
    v = max([int(x) for x in re.findall(r"_v(\d)", " ".join(pdfs))] or [1])
    consult = "public consultation" in txt.lower()
    has_report = any(re.search(r"report", p, re.I) for p in pdfs)
    # Reviewed by hand (last 13 Nov 2026): everything listed is a final/adopted (or EDPB-endorsed WP29) version except
    # these public-consultation drafts (v1 only) and old v1 pages of guidelines whose final version is listed separately
    DRAFTS = ("guidelines-042026", "guidelines-022026-on-anonymisation", "guidelines-032026-on-web-scraping",
              "guidelines-12026-on-processing-of-personal-data-for-scientific", "guidelines-012025-on-pseudonymisation",
              "recommendations-22025-on-the-legal-basis-for-requiring", "joint-guidelines-on-the-interplay-between-the-digital-markets",
              "guidelines-012021-on-examples-regarding-data-breach-notification_en", "guidelines-12020-on-processing-personal-data-in-the-context-of-connected",
              "article-29-working-party-guidelines-on-transparency-under-regulation")
    final = not any(d in u for d in DRAFTS)
    date = (re.search(r'datetime="(\d{4}-\d{2}-\d{2})', h) or [None, None])[1]
    s = (u + " " + title).lower()
    if "eprivacy" in s: parent = "32002L0058"
    elif "law-enforcement-directive" in s or "law enforcement directive" in s: parent = "32016L0680"
    elif "payment-services" in s or "payment services" in s: parent = "32015L2366"
    elif "dsa" in s or "digital services act" in s: parent = "32022R2065"
    elif "digital-markets" in s or "digital markets act" in s: parent = "32022R1925"
    else: parent = "32016R0679"
    also = "32016R0679" if parent in ("32015L2366", "32022R2065", "32022R1925") else ""
    out.append({"agency": "EDPB", "url": BASE + u, "title": title, "type": typ, "final": final,
                "endorsed_wp29": bool(re.search(r"wp\d{3}|article-29|29 working", s)), "date": date,
                "pdf": BASE + main[0] if main else (BASE + pdfs[0] if pdfs else None), "parent": parent, "also_relates_to": also})
seen = set(); ded = []
for o in out:
    if o["pdf"] and ("decision" in o["pdf"] or "pdps.ge" in o["pdf"]):
        o["pdf"] = None
    key = (o["pdf"] or o["url"]).rsplit("/", 1)[-1]
    if key in seen:
        continue
    seen.add(key); ded.append(o)
out = ded
json.dump(out, open("../data/agency_edpb.json", "w"), indent=1)
for o in out:
    print("F" if o["final"] else "D", o["parent"], o["date"], o["title"][:85], "|", (o["pdf"] or "NO PDF")[-45:])
