"""Company responses: trend in attention to EU laws, controlling for changes in the sample and sources.

Inputs: frequency_all_reports.csv and frequency_all_mentions.csv (cr_frequency.py --out-prefix).
Outcomes per report: number of EU laws named; mentions of all EU laws per 100,000 words (log(1+x));
whether at least one EU law other than the GDPR is named.

Three ways of holding composition constant:
  raw         plain yearly means (as before)
  balanced    only companies with a report in every year of the window
  fe          OLS with company fixed effects, year dummies, source/document-type dummies
              (SEC 10-K, SEC 20-F, ESEF, company website, AMF, annualreports.com, financialreports.eu)
              and report-language dummies; year coefficients relative to the base year, with
              standard errors clustered by company. The FE model also runs on SEC filings only.

  python3 cr_trend.py [--from 2010] [--to 2025] [--exclude R127,R129] [--out trend_controls.csv] [--by-type]
  --by-type also writes trend_by_type.csv (raw means and FE per main company type).
"""
import collections, csv, json, math, os, sys
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "company_responses")


def load(exclude):
    laws = {l["id"]: l for l in json.load(open(os.path.join(DATA, "law_patterns_all.json")))["laws"] if l["scope"] == "eu"}
    reps = [r for r in csv.DictReader(open(os.path.join(DATA, "frequency_all_reports.csv"), encoding="utf-8")) if r["words"]]
    by = collections.defaultdict(list)
    for m in csv.DictReader(open(os.path.join(DATA, "frequency_all_mentions.csv"), encoding="utf-8")):
        if m["law"] in exclude or m["law"] not in laws or int(m["year"]) < laws[m["law"]].get("min_year", 0):
            continue
        by[(m["company"], m["year"])].append(m)
    out = []
    for r in reps:
        ms = by.get((r["company"], r["year"]), [])
        words = int(r["words"])
        src = r["source"] if r["source"] != "SEC EDGAR" else "SEC " + ("20-F" if r["form"] == "20-F" else "10-K")
        out.append({"company": r["company"], "region": r["region"], "year": int(r["year"]), "source": src,
                    "language": r["language"] or "en", "laws": len(ms),
                    "rate": sum(int(x["mentions"]) for x in ms) / words * 1e5 if words else 0.0,
                    "non_gdpr": int(any(x["law"] != "GDPR" for x in ms))})
    return out


def fe_years(rows, y, years, base):
    """Within-company OLS of y on year, source and language dummies; clustered SEs by company."""
    rows = [r for r in rows if r["year"] in years]
    comps = sorted({r["company"] for r in rows})
    srcs = sorted({r["source"] for r in rows})[1:]
    langs = sorted({r["language"] for r in rows})[1:]
    yrs = [t for t in years if t != base]
    cols = [("year", t) for t in yrs] + [("source", s) for s in srcs] + [("language", l) for l in langs]
    X = np.array([[1.0 if r[k] == v else 0.0 for k, v in cols] for r in rows])
    Y = np.array([y(r) for r in rows], dtype=float)
    g = np.array([comps.index(r["company"]) for r in rows])
    # demean within company (absorbs company fixed effects)
    for c in range(len(comps)):
        idx = g == c
        X[idx] -= X[idx].mean(0)
        Y[idx] -= Y[idx].mean()
    keep = X.std(0) > 0
    X, cols = X[:, keep], [c for c, k in zip(cols, keep) if k]
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ X.T @ Y
    e = Y - X @ b
    meat = np.zeros((X.shape[1], X.shape[1]))
    for c in range(len(comps)):
        s = X[g == c].T @ e[g == c]
        meat += np.outer(s, s)
    G, N, K = len(comps), len(Y), X.shape[1] + len(comps)
    V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((N - 1) / max(N - K, 1))
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    return {t: (b[cols.index(("year", t))], se[cols.index(("year", t))]) for t in yrs if ("year", t) in cols}, len(comps), N


def main():
    a = sys.argv[1:]
    get = lambda k, d: a[a.index(k) + 1] if k in a else d
    y0, y1 = int(get("--from", "2010")), int(get("--to", "2025"))
    exclude = set(filter(None, get("--exclude", "").split(",")))
    rows = load(exclude)
    years = list(range(y0, y1 + 1))
    outcomes = {"laws": lambda r: r["laws"], "log_rate": lambda r: math.log1p(r["rate"]), "non_gdpr": lambda r: r["non_gdpr"]}
    res = []
    # raw
    for t in years:
        xs = [r for r in rows if r["year"] == t]
        if xs:
            res.append({"method": "raw", "year": t, "n_reports": len(xs), "n_companies": len({r['company'] for r in xs}),
                        **{k: round(sum(f(r) for r in xs) / len(xs), 3) for k, f in outcomes.items()}})
    # balanced panel (window ending in the last complete year)
    have = collections.defaultdict(set)
    for r in rows:
        have[r["company"]].add(r["year"])
    for w0, w1 in ((y0, y1 - 1), (2016, y1 - 1)):
        bal = {c for c, ys in have.items() if set(range(w0, w1 + 1)) <= ys}
        for t in range(w0, w1 + 1):
            xs = [r for r in rows if r["year"] == t and r["company"] in bal]
            if xs:
                res.append({"method": f"balanced {w0}-{w1}", "year": t, "n_reports": len(xs), "n_companies": len(bal),
                            **{k: round(sum(f(r) for r in xs) / len(xs), 3) for k, f in outcomes.items()}})
    # fixed effects, all sources and SEC only
    for label, sub in (("fe", rows), ("fe SEC only", [r for r in rows if r["source"].startswith("SEC")])):
        for k, f in outcomes.items():
            est, nc, n = fe_years(sub, f, years, y0)
            for t in years:
                b, s = est.get(t, (0.0, 0.0)) if t != y0 else (0.0, 0.0)
                res.append({"method": f"{label}: {k}", "year": t, "n_reports": n, "n_companies": nc,
                            "coef": round(float(b), 3), "se": round(float(s), 3)})
    # by company type (main type, as in universe/company_list.md): raw means and FE per type
    if "--by-type" in a:
        u = json.load(open(os.path.join(DATA, "universe", "universe.json")))["companies"]
        main = {c["id"]: (c.get("company_types") or "").split(";")[0] for c in u}
        res2 = []
        for ty in ("GK", "PL", "CL", "TC", "FI", "PR"):
            sub = [r for r in rows if main.get(r["company"]) == ty]
            for t in years:
                xs = [r for r in sub if r["year"] == t]
                if xs:
                    res2.append({"type": ty, "method": "raw", "year": t, "n_reports": len(xs),
                                 **{k: round(sum(f(r) for r in xs) / len(xs), 3) for k, f in outcomes.items()}})
            for k, f in outcomes.items():
                est, nc, n = fe_years(sub, f, years, y0)
                for t in years:
                    b, s = est.get(t, (0.0, 0.0)) if t != y0 else (0.0, 0.0)
                    res2.append({"type": ty, "method": f"fe: {k}", "year": t, "n_reports": n, "n_companies": nc,
                                 "coef": round(float(b), 3), "se": round(float(s), 3)})
        with open(os.path.join(DATA, "trend_by_type.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["type", "method", "year", "n_reports", "n_companies", "laws", "log_rate",
                                               "non_gdpr", "coef", "se"])
            w.writeheader()
            w.writerows(res2)
        print("wrote trend_by_type.csv")
    out = os.path.join(DATA, get("--out", "trend_controls.csv"))
    cols = ["method", "year", "n_reports", "n_companies", "laws", "log_rate", "non_gdpr", "coef", "se"]
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(res)
    print("wrote", out)


if __name__ == "__main__":
    main()
