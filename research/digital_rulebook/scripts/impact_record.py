"""Helper to write data/impact/<CELEX>.json records in the agreed schema (adds accessed date and archive_url)."""
import json, os, urllib.request, urllib.parse
TODAY = "2026-10-10"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "impact")


def wayback(u):
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(
            "https://archive.org/wayback/available?url=" + urllib.parse.quote(u, safe=""), headers={"User-Agent": "research"}), timeout=30))
        s = r.get("archived_snapshots", {}).get("closest")
        return s["url"] if s and s.get("available") else ""
    except Exception:
        return ""


def ind(type_, objective, indicator="", target="", evidence="", status="", sources=""):
    return {"type": type_, "objective": objective, "indicator": indicator, "target_or_baseline": target,
            "evidence": evidence, "status": status, "sources": sources}


def lit(id, authors, year, title, venue, url, source_type, method, outcomes, direction, headline, summary_plain,
        period_geography="", quality="", verified="abstract read", access="open", pdf_url="", interested_party=""):
    return {"id": id, "citation": f"{authors} ({year}), {title}, {venue}", "authors": authors, "year": year, "title": title,
            "venue": venue, "url": url, "pdf_url": pdf_url, "source_type": source_type, "method": method, "outcomes": outcomes,
            "direction": direction, "headline": headline, "summary_plain": summary_plain, "period_geography": period_geography,
            "quality": quality, "verified": verified, "access": access, "interested_party": interested_party}


def write(celex, name, proposal, impact_assessment, evidence_rating, summary, indicators, literature):
    for l in literature:
        l.setdefault("accessed", TODAY)
        l["archive_url"] = wayback(l["url"])
    rec = {"celex": celex, "name": name, "proposal": proposal, "impact_assessment": impact_assessment,
           "evidence_rating": evidence_rating, "summary": summary, "last_reviewed": TODAY,
           "indicators": indicators, "literature": literature}
    json.dump(rec, open(os.path.join(OUT, celex + ".json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, "PROGRESS.md"), "a") as f:
        f.write(f"- [x] {celex} {name}\n")
    print("wrote", celex, len(indicators), "indicators,", len(literature), "sources")
