"""Company responses: per-law check sheet for the all-laws frequency run.

Reads frequency_all_mentions.csv and writes frequency_all_check.md: for each law, the number of
reports and companies that mention it, the most common matched strings, and up to 6 example
contexts drawn with a fixed seed (at most one per company), for a reader to judge whether the
matches really refer to the EU law. Laws judged unreliable are listed in law_exclusions.json
and dropped from the published figures.
"""
import collections, csv, json, os, random

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "company_responses")


def main():
    rows = list(csv.DictReader(open(os.path.join(DATA, "frequency_all_mentions.csv"), encoding="utf-8")))
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["law"], r["law_name"])].append(r)
    rnd = random.Random(20261121)
    L = ["# Check sheet: matches per law (all-laws frequency run)", ""]
    for (lid, name), xs in sorted(by.items(), key=lambda kv: -sum(int(x["mentions"]) for x in kv[1])):
        comps = {x["company"] for x in xs}
        top = collections.Counter(x["matched"] for x in xs).most_common(6)
        L += [f"## {name} ({lid})", f"{len(xs)} reports, {len(comps)} companies, {sum(int(x['mentions']) for x in xs)} mentions; "
              f"first years: {sorted({int(x['year']) for x in xs})[:3]}", "",
              "Matched: " + "; ".join(f"`{m}` ({n})" for m, n in top), ""]
        one = {}
        for x in rnd.sample(xs, len(xs)):
            one.setdefault(x["company"], x)
        for x in list(one.values())[:6]:
            L.append(f"- {x['company']} {x['year']}: …{x['context'][:300]}…")
        L.append("")
    open(os.path.join(DATA, "frequency_all_check.md"), "w", encoding="utf-8").write("\n".join(L))
    print(len(by), "laws with mentions")


if __name__ == "__main__":
    main()
