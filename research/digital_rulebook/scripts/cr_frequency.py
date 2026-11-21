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


_LAWS = None


def _init(path):
    global _LAWS
    _LAWS = [l for l in cc.load_laws(path) if l["scope"] == "eu"]


def measure(r):
    """Words, language and per-law mentions for one report (runs in a worker process)."""
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
    res = {}
    for l in _LAWS:
        full = any(rx.search(flat) for rx in l["full_re"]) and not any(rx.search(flat) for rx in l["conflict_re"])
        ms = cc.match_law(l, flat, full)
        if ms:
            m = ms[0]
            res[l["id"]] = {"mentions": len(ms), "paragraphs": len({bisect.bisect_right(offs, x.start()) for x in ms}),
                            "matched": m.group(0), "context": re.sub(r"\s+", " ", flat[max(0, m.start() - 150):m.end() + 150])}
    return nwords, lang, res


def main():
    """Default: the three pilot laws, long format (frequency.csv: one row per report x law).
    With --patterns FILE (e.g. law_patterns_all.json) and --out-prefix P: compact output for many laws,
    P_reports.csv (one row per report), P_mentions.csv (report x law with at least one mention, with the
    first match and its context for checking) and P_summary.csv (region x year x law, zeros included)."""
    from multiprocessing import Pool
    args = sys.argv[1:]
    opt = {"--config": os.path.join(DATA, "universe", "universe.json"),
           "--manifest": os.path.join(DATA, "reports_universe.json"),
           "--out": os.path.join(DATA, "frequency.csv"), "--patterns": None, "--out-prefix": None, "--procs": "4"}
    for k in list(opt):
        if k in args:
            opt[k] = args[args.index(k) + 1]
    cfg = {c["id"]: c for c in json.load(open(opt["--config"]))["companies"]}
    _init(opt["--patterns"])
    laws = _LAWS
    reps = json.load(open(opt["--manifest"]))
    ok = [r for r in reps if r.get("status") == "ok"]
    results = []
    with Pool(int(opt["--procs"]), initializer=_init, initargs=(opt["--patterns"],)) as pool:
        for i, res in enumerate(pool.imap(measure, ok, chunksize=4), 1):
            results.append(res)
            if i % 100 == 0:
                print(f"{i}/{len(ok)} reports", flush=True)
    meas = {(r["company"], r["year"]): x for r, x in zip(ok, results)}

    def base(r):
        c = cfg.get(r["company"], {})
        hq = c.get("hq", "")
        return {"company": r["company"], "name": c.get("name", r["company"]), "hq": hq, "region": region(hq),
                "groups": "; ".join(c.get("groups", [])), "year": r["year"], "form": r.get("form", ""),
                "source": r.get("source", ""), "report_status": r.get("status", "")}

    rows = []      # long rows, used for the summary
    for r in reps:
        b = base(r)
        if (r["company"], r["year"]) not in meas:
            continue
        nwords, lang, res = meas[(r["company"], r["year"])]
        for l in laws:
            x = res.get(l["id"], {}) if r["year"] >= l.get("min_year", 0) else {}
            n = x.get("mentions", 0)
            rows.append(dict(b, language=lang, words=nwords, law=l["id"], mentions=n, paragraphs=x.get("paragraphs", 0),
                             per_100k=round(1e5 * n / nwords, 3) if nwords else "", matched=x.get("matched", ""),
                             context=x.get("context", "")))
    if opt["--out-prefix"]:
        P = opt["--out-prefix"]
        rep_cols = ["company", "name", "hq", "region", "groups", "year", "form", "source", "report_status", "language", "words"]
        with open(P + "_reports.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rep_cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(dict(base(r), **({"language": meas[(r["company"], r["year"])][1], "words": meas[(r["company"], r["year"])][0]}
                                          if (r["company"], r["year"]) in meas else {})) for r in reps)
        names = {l["id"]: l["name"] for l in laws}
        with open(P + "_mentions.csv", "w", newline="", encoding="utf-8") as f:
            cols = ["company", "region", "year", "law", "law_name", "mentions", "paragraphs", "per_100k", "words", "matched", "context"]
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(dict(x, law_name=names[x["law"]]) for x in rows if x["mentions"])
        out_summary = P + "_summary.csv"
    else:
        cols = ["company", "name", "hq", "region", "groups", "year", "form", "source", "report_status", "language", "words",
                "law", "mentions", "paragraphs", "per_100k"]
        with open(opt["--out"], "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
            w.writerows(dict(base(r), law=l["id"]) for r in reps if (r["company"], r["year"]) not in meas for l in laws)
        out_summary = opt["--out"].replace(".csv", "_summary.csv")
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
    with open(out_summary, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summ[0].keys()))
        w.writeheader()
        w.writerows(summ)
    print(len(ok), "reports measured;", len(laws), "laws")


if __name__ == "__main__":
    main()
