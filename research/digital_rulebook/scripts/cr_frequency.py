"""Company responses, frequency study: how often each annual report names each EU law.

A firm-level attention measure in the spirit of Hassan, Hollander, van Lent and Tahoun
(2019, QJE): mentions of a law per 100,000 words of the report. Unlike Hassan et al.
it has no risk-word component (see METHOD.md for why).

  python3 cr_frequency.py [--config FILE] [--manifest FILE] [--out FILE]

Defaults to the universe (universe/universe.json, reports_universe.json,
frequency.csv). For each report:
  - text with zero-width characters removed; paragraphs that occur more than once
    (e.g. a 20-F and its annual-report exhibit) are counted once;
  - words = Unicode word tokens; language = most frequent stop-word set;
  - for each EU law in law_patterns.json: mentions (every match of the law's
    patterns; abbreviations only where the full name is used), paragraphs with a
    mention, and mentions per 100,000 words.
Also writes <out>_summary.csv: by region x year x law, the number of reports, the
share that mention the law, and the mean and median rate.
"""
import bisect, csv, json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cr_code as cc  # noqa: E402

DATA = os.path.join(HERE, "..", "data", "company_responses")
EU27 = set("AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE".split())
STOP = {
    "en": "the and of to in that is for with are".split(), "fr": "le la les des et du dans est pour une".split(),
    "de": "der die und das den des ist mit für nicht".split(), "it": "il di che la per del della sono gli nel".split(),
    "es": "el los las del que por para una con es".split(), "nl": "de het een van en dat voor zijn met niet".split(),
    "fi": "ja on että ei se myös ovat oli tai kuin".split(), "sv": "och att det som för med är på av inte".split(),
    "pt": "os das que não para uma com dos pelo mais".split(),
}
WORD = re.compile(r"\w+", re.UNICODE)


def language(sample):
    toks = [t.lower() for t in WORD.findall(sample)]
    cnt = {}
    for t in toks:
        cnt[t] = cnt.get(t, 0) + 1
    score = {k: sum(cnt.get(w, 0) for w in v) for k, v in STOP.items()}
    return max(score, key=score.get)


def region(hq):
    return "US" if hq == "US" else "UK" if hq == "GB" else "EU" if hq in EU27 else hq


def main():
    args = sys.argv[1:]
    opt = {"--config": os.path.join(DATA, "universe", "universe.json"),
           "--manifest": os.path.join(DATA, "reports_universe.json"),
           "--out": os.path.join(DATA, "frequency.csv")}
    for k in list(opt):
        if k in args:
            opt[k] = args[args.index(k) + 1]
    cfg = {c["id"]: c for c in json.load(open(opt["--config"]))["companies"]}
    laws = [l for l in cc.load_laws() if l["scope"] == "eu"]
    rows = []
    for r in json.load(open(opt["--manifest"])):
        c = cfg.get(r["company"], {})
        hq = c.get("hq", "")
        base = {"company": r["company"], "name": c.get("name", r["company"]), "hq": hq, "region": region(hq),
                "groups": "; ".join(c.get("groups", [])), "year": r["year"], "form": r.get("form", ""),
                "source": r.get("source", ""), "report_status": r.get("status", "")}
        if r.get("status") != "ok":
            for l in laws:
                rows.append(dict(base, law=l["id"]))
            continue
        text = cc.ZW.sub("", open(os.path.join(cc.CACHE, r["text_file"]), encoding="utf-8").read())
        seen, paras = set(), []
        for _, p in cc.paragraphs(text):
            if len(p) >= 80:
                if p in seen:
                    continue
                seen.add(p)
            paras.append(p)
        flat = " ".join(paras)
        nwords = len(WORD.findall(flat))
        lang = language(flat[: min(len(flat), 400_000)])
        offs, pos = [], 0
        for p in paras:
            offs.append(pos)
            pos += len(p) + 1
        for l in laws:
            full = any(rx.search(flat) for rx in l["full_re"]) and not any(rx.search(flat) for rx in l["conflict_re"])
            ms = cc.match_law(l, flat, full)
            npara = len({bisect.bisect_right(offs, m.start()) for m in ms})
            rows.append(dict(base, language=lang, words=nwords, law=l["id"], mentions=len(ms), paragraphs=npara,
                             per_100k=round(1e5 * len(ms) / nwords, 3) if nwords else ""))
        print(r["company"], r["year"], lang, nwords, [x["mentions"] for x in rows[-len(laws):]], flush=True)
    cols = ["company", "name", "hq", "region", "groups", "year", "form", "source", "report_status", "language", "words",
            "law", "mentions", "paragraphs", "per_100k"]
    with open(opt["--out"], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    # summary by region x year x law
    groups = {}
    for x in rows:
        if x.get("per_100k", "") == "":
            continue
        groups.setdefault((x["region"], x["year"], x["law"]), []).append(x)
    summ = []
    for (g, y, l), xs in sorted(groups.items()):
        rates = [x["per_100k"] for x in xs]
        summ.append({"region": g, "year": y, "law": l, "reports": len(xs),
                     "share_mentioning": round(sum(x["mentions"] > 0 for x in xs) / len(xs), 3),
                     "mean_per_100k": round(statistics.mean(rates), 3), "median_per_100k": round(statistics.median(rates), 3)})
    with open(opt["--out"].replace(".csv", "_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summ[0].keys()))
        w.writeheader()
        w.writerows(summ)


if __name__ == "__main__":
    main()
