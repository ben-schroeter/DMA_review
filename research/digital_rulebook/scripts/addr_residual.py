"""Collect restrictions still unclear after the v2 rules and logged decisions, for secondary acts, consolidated texts
and proposals. Writes data/addressee/residual_<kind>.jsonl (with context) for the second readers."""
import json, os, re, sys, collections, multiprocessing as mp
sys.path.insert(0, os.path.dirname(__file__))
D = os.path.join(os.path.dirname(__file__), "..", "data")


def lines_for(celex, kind):
    from common import fetch
    from textparse import html_to_lines, split_parts
    from measure import pdf_text_lines
    html = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}")
    if kind == "proposal":
        p = split_parts(html_to_lines(html), is_proposal=True)
        if len(" ".join(p["articles"]).split()) < 300 or "TABLE POSITION" in html or "Having regard" not in html:
            paras = pdf_text_lines(celex)
            start = next((i for i, x in enumerate(paras) if re.match(r"^Proposal for an?\b", x, re.I)
                          and any(q.startswith("Having regard") or q.startswith("THE COUNCIL") for q in paras[i:i + 12])), 0)
            p = split_parts(paras[start:], is_proposal=False)
    else:
        p = split_parts(html_to_lines(html))
    return p["articles"] + p["annexes"]


def work(arg):
    celex, kind = arg
    from addr_dump import walk
    from addressee_v2 import apply
    try:
        rows = walk(lines_for(celex, kind), celex, kind)
        res = apply(rows) if rows else []
        return [dict(r, how=x["how"]) for r, x in zip(rows, res) if x["formal"] == "unclear"], len(rows)
    except Exception as e:
        print("error", celex, e, flush=True)
        return [], 0


if __name__ == "__main__":
    kinds = sys.argv[1:] or ["secondary", "consolidated", "proposal"]
    meas = json.load(open(os.path.join(D, "measurements.json")))
    for kind in kinds:
        if kind == "proposal":
            jobs = [(c, kind) for c in json.load(open(os.path.join(D, "proposals.json")))["measurements"]]
        else:
            jobs = [(m["celex"], kind) for m in meas if m.get("kind") == kind and not m.get("error")]
        tot = 0; out = []
        with mp.Pool(4) as pool:
            for rows, n in pool.imap_unordered(work, jobs, chunksize=4):
                out += rows; tot += n
        with open(os.path.join(D, "addressee", f"residual_{kind}.jsonl"), "w") as f:
            for r in out:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(kind, "documents", len(jobs), "restrictions", tot, "still unclear", len(out), flush=True)
