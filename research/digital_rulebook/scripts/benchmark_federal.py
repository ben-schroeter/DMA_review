"""Candidate federal US comparators for the 'Obligations per act' chart, measured with the same US-adapted counter as SOX and the
matched pairs (reuses load/paragraphs/run from us_measure.py). Writes ../data/benchmark_federal.json. Usage (from scripts/)."""
import json, re, sys
src = open("us_measure.py").read().split("out = []")[0]
exec(compile(src, "us_measure_head", "exec"))
CANDS = [
    ("telecom96", "Telecommunications Act of 1996", "PLAW-104publ104", None, None),
    ("glba", "Gramm-Leach-Bliley Act (1999)", "PLAW-106publ102", None, None),
    ("glba_v", "Gramm-Leach-Bliley Act, title V privacy (1999)", "PLAW-106publ102", (r"TITLE V--PRIVACY", 2), r"TITLE VI--"),
    ("hipaa_as", "HIPAA administrative simplification (1996, title II subtitle F)", "PLAW-104publ191", (r"Subtitle F--Administrative Simplification", 2), r"Subtitle G--"),
    ("takeitdown", "TAKE IT DOWN Act (2025)", "PLAW-119publ12", None, None),
    ("dodd_frank", "Dodd-Frank Act (2010)", "PLAW-111publ203", None, None),
]
out = []
for sid, label, source, start, end in CANDS:
    try:
        t, pages = load("plaw", source, start, end)
    except Exception as e:
        print(sid, "FAILED", e); continue
    ps = paragraphs(t); joined = "\n\n".join(ps)
    rec = {"id": sid, "label": label, "source": source, "pages": pages}
    for name, txt in (("all_text", joined), ("excluding_inserted_text", re.sub(r"(``|‘‘|\").*?(''|’’|\")", " ", joined, flags=re.S))):
        r, a, s = run([p for p in txt.split("\n\n") if p.strip()])
        n = sum(r.values())
        rec[name] = {"words": words(txt), "restrictions_total": n, "by_addressee": a, "per_1000_words": round(1000 * n / max(1, words(txt)), 1)}
        if name == "all_text":
            json.dump(s, open(f"../data/us_map/instances_{sid}_all_text.json", "w"), indent=1)
    out.append(rec)
    v = rec["all_text"]
    print(f"{sid:11} pages={pages:>4} words={v['words']:>7} restr={v['restrictions_total']:>5} per1000={v['per_1000_words']:>5} addr={v['by_addressee']}")
json.dump(out, open("../data/benchmark_federal.json", "w"), indent=1)
