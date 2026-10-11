"""Dump every counted restriction in the main acts with its context, for the addressee recheck.

For each instance: document, article number and heading, the list lead-in (chapeau) it sits under,
the clause, the marker, the category, and the current rule-based addressee and subject.
Writes data/addressee/instances_main.jsonl and checks that totals match data/measurements.json.
Usage: python3 addr_dump.py [kind]   (kind = main | secondary | consolidated; default main)"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import fetch
from textparse import html_to_lines, split_parts
from restrictions import strip_quoted, CLAUSE_SPLIT, find_instances
from addressee import addressee, _LAST

D = os.path.join(os.path.dirname(__file__), "..", "data")
ART = re.compile(r"^Article\s+(\d+[a-z]?)\s*$", re.I)
ANNEX = re.compile(r"^ANNEX(ES)?(\s+[IVXLC0-9]+[a-z]?)?\s*$", re.I)


def dump(celex, kind):
    raw = fetch(f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}")
    lines = html_to_lines(raw)
    parts = split_parts(lines, is_proposal=bool(re.match(r"5\d{4}PC", celex)))
    _LAST["who"] = None
    out, art, head, chapeau, expect_head, buf = [], "", "", "", False, ""
    for line in strip_quoted(parts["articles"] + parts["annexes"]):
        s = line.strip()
        m = ART.match(s)
        if m:
            art, head, chapeau, expect_head, buf = "Art. " + m.group(1), "", "", True, ""
            continue
        if ANNEX.match(s):
            art, head, chapeau, expect_head, buf = s.title(), "", "", True, ""
            continue
        if expect_head:
            expect_head = False
            if len(s) < 160 and not s.endswith((".", ";", ":")):
                head = s
                continue
        # a new numbered paragraph resets the lead-in; a line ending with ':' opens one
        if re.match(r"^\d+\.\s", s):
            chapeau = ""
        for c in CLAUSE_SPLIT.split(s):
            c = c.strip()
            if not c:
                continue
            inst, _ = find_instances(c)
            for cat, a, b in inst:
                who, subj = addressee(c[:600], min(a, 599))
                out.append({"doc": celex, "kind": kind, "article": art, "heading": head, "chapeau": chapeau,
                            "clause": c[:600], "marker": c[a:b], "pos": a, "category": cat,
                            "addressee": who, "subject": subj, "before": buf[-700:]})
            buf += " " + c
        if s.endswith(":"):
            chapeau = s[-400:]
    return out


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "main"
    meas = [m for m in json.load(open(os.path.join(D, "measurements.json"))) if m.get("kind") == kind]
    os.makedirs(os.path.join(D, "addressee"), exist_ok=True)
    path = os.path.join(D, "addressee", f"instances_{kind}.jsonl")
    tot, mism = collections.Counter(), []
    with open(path, "w") as f:
        for i, m in enumerate(meas):
            rows = dump(m["celex"], kind)
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
                tot[r["addressee"]] += 1
            if len(rows) != m["restrictions_total"]:
                mism.append((m["celex"], len(rows), m["restrictions_total"]))
            if i % 20 == 0:
                print(i, m["celex"], len(rows), flush=True)
    print("instances", sum(tot.values()), dict(tot))
    print("documents whose count differs from measurements.json:", len(mism), mism[:10])
