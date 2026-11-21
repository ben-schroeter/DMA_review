"""Company responses, step 2: find and code every passage that mentions a tracked law.

Inputs: data/company_responses/reports.json (from cr_fetch.py), law_patterns.json,
and the cached report texts. A passage is the paragraph that contains a mention.
One row per passage x law, coded with:
  categories  risk_factor / compliance_cost / fine_or_provision / product_change /
              revenue_impact / legal_proceedings / opportunity (rule-based cues; several allowed)
  amounts     money amounts in the sentence(s) around the mention
  repeated    passage near-identical (5-word-shingle Jaccard >= 0.8) to one in the
              company's previous report that mentions the same law
  list_only   the law is named only inside a list of several laws
  glossary    the mention is an entry in an abbreviations list
  boilerplate repeated, glossary, or list_only with no category other than risk_factor
  quote, link (PDFs link to the page)

Outputs in data/company_responses/: mentions.csv (EU laws), uk_mentions.csv (UK and
other non-EU laws, logged separately), company_year.csv (one row per company x year x EU law).
"""
import bisect, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "company_responses")
CACHE = os.path.join(os.environ.get("RULEBOOK_CACHE", os.path.expanduser("~/.cache/digital_rulebook")), "company_reports")

CUES = {
    "risk_factor": r"(?i)\b(could|may|might|would)\b[^.]{0,160}\b(adverse|adversely|harm|negative|negatively|materially|damage|impair|disrupt|reduce|limit)|\brisks?\b|\buncertain",
    "compliance_cost": r"(?i)\bcosts?\b|\bcostly\b|\bexpens|\binvest(ed|ment|ing)?\b|\bresources\b|\bburden|\bcompliance (programme|program|effort|project)s?\b|\bco[uû]ts?\b|\bKosten\b",
    "fine_or_provision": r"(?i)\bfines?\b|\bfined\b|\bpenalt|\bsanction|\bprovisions? (for|of|in respect|recogni)|\baccru|\bcharge of\b|\b\d+\s?% of (our |its |annual |global |worldwide )*(total |annual )*(worldwide |global )*(turnover|revenue)|\bamende|\bBußgeld",
    "product_change": r"(?i)\b(chang(e|ed|es|ing)|modif(y|ied|ies|ications?)|updat(e|ed|ing)|launch(ed)?|introduc(e|ed|ing)|roll(ed)? out|redesign|offer(ed)? (users|consumers|people|developers))\b[^.]{0,80}\b(products?|services?|features?|apps?|platforms?|practices|terms|experiences?|offerings?|policies|business model)\b|\bchoice screens?\b|\binteroperab|\bsideload|\balternative (app|browser|payment|distribution)|\bconsent (mechanism|flow|banner)|\bless personali[sz]ed\b|\bsubscription (for|without) (no )?ads\b|\bdata portability\b",
    "revenue_impact": r"(?i)\brevenues?\b|\bmonetiz|\bmonetis|\badvertis(ing|ers)\b[^.]{0,60}\b(revenue|demand|spend|effectiveness)|\bsales\b|\bchiffre d['’]affaires\b|\bUmsatz",
    "legal_proceedings": r"(?i)\binvestigat|\bproceedings?\b|\bnon-compliance (decision|proceeding)|\bappeal|\bcourt\b|\blawsuits?\b|\blitigation\b|\bcomplaints?\b|\binquir(y|ies)\b|\bData Protection Commission\b|\bDPC\b|\bCNIL\b|\bsupervisory authorit|\bopened (a|an) (formal )?(investigation|proceeding)|\bstatement of objections\b|\bdecision (against|finding)\b",
    "opportunity": r"(?i)\bopportunit|\bdemand for (our|its)\b|\bhelp(ing)? (our )?(clients|customers)\b[^.]{0,60}\b(comply|compliance|prepare|navigate)|\bcompetitive (advantage|edge)\b|\bdifferentiat|\bgrowth (driver|area)|\bnew (business|market)s?\b|\btrusted\b",
}
CUES = {k: re.compile(v) for k, v in CUES.items()}
AMOUNT = re.compile(r"(?:(?:€|EUR|US\$|USD|\$|£|GBP)\s?\d[\d,.]*(?:\s?(?:million|billion|bn|mn|m|k)\b)?"
                    r"|\b\d[\d,.]*\s?(?:million|billion|bn|Mio\.?|Mrd\.?)\s?(?:euros?|EUR|€|dollars|USD|\$|pounds|GBP|£))")
# names that make a sentence a list of laws
LAWISH = re.compile(r"\b(GDPR|CCPA|CPRA|LGPD|PIPL|PIPEDA|HIPAA|COPPA|DSA|DMA|NIS ?2|DORA|ePrivacy|Data Act|AI Act|"
                    r"[A-Z][A-Za-z-]+ (Act|Regulation|Directive|Law))\b")
GLOSS = re.compile(r"\b([A-Z]{2,7}) (?:[A-Z][a-z]+ ){1,6}")   # 'GLCM Global Liquidity and Cash ...' 
VERBISH = re.compile(r"\b(is|are|was|were|be|been|may|might|will|would|could|can|we|our|has|have|had|its)\b")
ZW = re.compile("[\u200b\u200c\u200d\u2060\ufeff\u00ad]")   # zero-width characters in some iXBRL filings
SENT = re.compile(r"(?<=[.!?;])\s+(?=[A-Z(“\"])")


def _combine(pats):
    """One alternation per law; a leading (?i) becomes a scoped (?i:...) group. Used only to test
    whether a report names a law at all (a single alternation is slower than separate patterns
    for finding every match, because Python's re loses its literal-prefix search)."""
    parts = ["(?i:" + p[4:] + ")" if p.startswith("(?i)") else "(?:" + p + ")" for p in pats]
    return re.compile("|".join(parts)) if parts else None


def load_laws(path=None):
    laws = json.load(open(path or os.path.join(DATA, "law_patterns.json")))["laws"]
    for l in laws:
        l["full_re"] = [re.compile(p) for p in l["full"]]
        l["abbrev_re"] = [re.compile(p) for p in l["abbrev"]]
        l["full_cre"], l["abbrev_cre"] = _combine(l["full"]), _combine(l["abbrev"])
        l["nb_re"] = re.compile(l["not_before"]) if l.get("not_before") else None
        l["na_re"] = re.compile(l["not_after"]) if l.get("not_after") else None
        l["conflict_re"] = [re.compile(p) for p in l.get("abbrev_conflicts", [])]
    return laws


def paragraphs(text):
    """Yield (page, paragraph) with soft line breaks joined."""
    page = 1
    for chunk in re.split(r"(\f|\n\s*\n)", text):
        if chunk == "\f":
            page += 1
            continue
        p = re.sub(r"-\n(?=[a-z])", "", chunk)
        p = re.sub(r"\s*\n\s*", " ", p).strip()
        if p:
            yield page, p


class Hit:
    """A match re-based onto its passage."""
    def __init__(self, text, start):
        self.text, self._start = text, start

    def start(self):
        return self._start

    def group(self, _=0):
        return self.text


def match_law(law, flat, doc_has_full):
    """Matches on the whole report (paragraphs joined by spaces), so names split
    across HTML blocks or PDF lines are still found."""
    hits = []
    for rx in law["full_re"] + (law["abbrev_re"] if doc_has_full else []):
        for m in rx.finditer(flat):
            if law["nb_re"] and law["nb_re"].search(flat[max(0, m.start() - 40):m.start()]):
                continue
            if law.get("na_re") and law["na_re"].search(flat[m.end():m.end() + 20]):
                continue
            hits.append(m)
    # drop matches contained in a longer match (e.g. 'GDPR' inside 'EU and UK GDPR')
    hits.sort(key=lambda m: (m.start(), -m.end()))
    out, last_end = [], -1
    for m in hits:
        if m.end() <= last_end:
            continue
        out.append(m)
        last_end = max(last_end, m.end())
    return out


def shingles(s, n=5):
    w = re.findall(r"\w+", s.lower())
    return {" ".join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def quote_around(p, m, width=320):
    sents, pos = SENT.split(p), 0
    for s in sents:
        start = p.find(s, pos)
        if start <= m.start() < start + len(s) + 1:
            q = s
            break
        pos = start + len(s)
    else:
        q = p
    if len(q) > width:
        c = m.start() - p.find(q)
        a = max(0, c - width // 2)
        q = ("…" if a else "") + q[a:a + width] + "…"
    return q.strip()


def context_sentences(p, m):
    """The sentence containing the mention plus its neighbours."""
    sents = SENT.split(p)
    pos = 0
    for i, s in enumerate(sents):
        start = p.find(s, pos)
        if start <= m.start() < start + len(s) + 1:
            return " ".join(sents[max(0, i - 1):i + 2]), s
        pos = start + len(s)
    return p, p


def main():
    laws = load_laws()
    reports = [r for r in json.load(open(os.path.join(DATA, "reports.json"))) if r.get("status") == "ok"]
    reports.sort(key=lambda r: (r["company"], r["year"]))
    eu_rows, other_rows = [], []
    prev = {}  # (company, law) -> list of shingle sets from the previous report
    for r in reports:
        text = ZW.sub("", open(os.path.join(CACHE, r["text_file"]), encoding="utf-8").read())
        cur = {}
        seen = set()
        paras = list(paragraphs(text))
        offs, pos = [], 0
        for _, p in paras:
            offs.append(pos)
            pos += len(p) + 1
        flat = " ".join(p for _, p in paras)
        # abbreviations count only where the report also uses the full name and
        # does not define the abbreviation as something else
        doc_full = {l["id"]: any(rx.search(flat) for rx in l["full_re"])
                    and not any(rx.search(flat) for rx in l["conflict_re"]) for l in laws}
        for law in laws:
            groups = {}
            for m in match_law(law, flat, doc_full[law["id"]]):
                i = bisect.bisect_right(offs, m.start()) - 1
                j = bisect.bisect_right(offs, m.end() - 1) - 1
                groups.setdefault((i, j), []).append(m)
            covered = -1
            for (i, j), ms in sorted(groups.items()):
                if i <= covered:     # already inside the previous passage for this law
                    continue
                page = paras[i][0]
                # short paragraphs (headings, broken table cells) take in what follows
                while sum(len(q) for _, q in paras[i:j + 1]) < 200 and j + 1 < len(paras):
                    j += 1
                covered = j
                p = " ".join(q for _, q in paras[i:j + 1])
                cut = 0
                if len(p) > 2500:   # page-long blocks: keep the sentences around the mentions
                    a, b = ms[0].start() - offs[i], ms[-1].end() - offs[i]
                    lo = max(0, a - 900)
                    lo = max([lo] + [k.end() for k in SENT.finditer(p, lo, a)][:1])
                    hi = min(len(p), b + 900)
                    ends = [k.start() + 1 for k in SENT.finditer(p, b, hi)]
                    hi = ends[-1] if ends else hi
                    p, cut = p[lo:hi], lo
                key = (law["id"], p[:200])
                if key in seen:      # same paragraph repeated (e.g. report and exhibit both filed)
                    continue
                seen.add(key)
                hits = [Hit(m.group(0), m.start() - offs[i] - cut) for m in ms]
                m = hits[0]
                ctx, sent = context_sentences(p, m)
                sh = shingles(p)
                cur.setdefault(law["id"], []).append(sh)
                row = {"company": r["company"], "year": r["year"], "law": law["id"], "scope": law["scope"],
                       "form": r["form"], "source": r["source"], "language": r.get("language", "en"),
                       "page": page if r["kind"] == "pdf" else "",
                       "n_hits": len(hits), "matched": m.group(0),
                       "quote": quote_around(p, m),
                       "link": r["url"] + (f"#page={page}" if r["kind"] == "pdf" else ""),
                       "passage_chars": len(p)}
                if law["scope"] != "eu":
                    other_rows.append(row)
                    continue
                cats = [k for k, rx in CUES.items() if rx.search(ctx)]
                amounts = sorted(set(a.strip() for a in AMOUNT.findall(ctx)))
                repeated = max((jaccard(sh, o) for o in prev.get((r["company"], law["id"]), [])), default=0.0)
                list_only = len({x.group(0) for x in LAWISH.finditer(sent)}) >= 3 and len(sent) < 600
                # glossary / abbreviation-list entries ("GDPR General Data Protection Regulation GLCM ...")
                glossary = (len(set(GLOSS.findall(sent))) >= 3 and not VERBISH.search(sent))
                row.update({"categories": ";".join(cats), "amounts": "; ".join(amounts),
                            "similarity_prev": round(repeated, 2), "repeated": repeated >= 0.8,
                            "list_only": list_only, "glossary": glossary,
                            "boilerplate": repeated >= 0.8 or glossary or (list_only and set(cats) <= {"risk_factor"})})
                for k in CUES:
                    row[k] = int(k in cats)
                row["passage"] = p[:4000]
                eu_rows.append(row)
        # "previous report" = the company's last report that mentioned the law
        for lid, shs in cur.items():
            prev[(r["company"], lid)] = shs
    # write passage files
    cols = ["company", "year", "law", "form", "source", "language", "page", "matched", "n_hits", "categories",
            *CUES.keys(), "amounts", "similarity_prev", "repeated", "list_only", "glossary", "boilerplate", "quote", "link",
            "passage_chars", "passage"]
    with open(os.path.join(DATA, "mentions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(eu_rows)
    with open(os.path.join(DATA, "uk_mentions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "year", "law", "scope", "form", "page", "matched", "quote", "link"],
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(other_rows)
    # company x year x law panel
    allrep = json.load(open(os.path.join(DATA, "reports.json")))
    eu_laws = [l["id"] for l in laws if l["scope"] == "eu"]
    out = []
    for r in allrep:
        for lid in eu_laws:
            rows = [x for x in eu_rows if x["company"] == r["company"] and x["year"] == r["year"] and x["law"] == lid]
            sub = [x for x in rows if not x["boilerplate"]]
            o = {"company": r["company"], "year": r["year"], "law": lid,
                 "report": r.get("form", "") if r.get("status") == "ok" else "",
                 "report_status": r.get("status"),
                 "mentioned": (1 if rows else 0) if r.get("status") == "ok" else "",
                 "n_passages": len(rows), "n_substantive": len(sub)}
            for k in CUES:
                o[k] = sum(x[k] for x in rows)
            o["amounts"] = " | ".join(x["amounts"] for x in rows if x["amounts"] and x["fine_or_provision"])
            best = sorted(sub or rows, key=lambda x: -(len(x["categories"].split(";")) if x["categories"] else 0))
            o["example_quote"] = best[0]["quote"] if best else ""
            o["example_link"] = best[0]["link"] if best else ""
            out.append(o)
    with open(os.path.join(DATA, "company_year.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(len(reports), "reports;", len(eu_rows), "EU-law passages;", len(other_rows), "UK/other passages")


if __name__ == "__main__":
    main()
