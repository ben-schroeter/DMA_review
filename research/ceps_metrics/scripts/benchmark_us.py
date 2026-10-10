"""Measure a US public law (e.g. Sarbanes-Oxley) with the same restriction counter, as an external benchmark.
Usage: python3 benchmark_us.py <pdf> <label>
Reports two variants: all enacted text, and excluding text inserted into other statutes (‘‘ … ’’ quotes)."""
import json, re, subprocess, sys
sys.path.insert(0, ".")
import addressee as A
from textparse import words
import restrictions as Rm
from restrictions import clauses, find_instances

# US drafting patterns that use 'shall' without imposing a duty (benchmark only; mirrors the EU constitutive exclusions)
Rm.EXCLUDE_SHALL = re.compile(Rm.EXCLUDE_SHALL.pattern[:-len(")\\b")] + r"|remain\s+(?:in\s+effect|effective|in\s+force)|"
    r"(?:not\s+)?be\s+subject\s+to|be\s+available|be\s+treated\s+as|be\s+fined|be\s+imprisoned|have\s+(?:been\s+)?[a-z]+ed\b|"
    r"determine|deem|be\s+in\s+addition\s+to|not\s+supersede|not\s+preempt|not\s+be\s+an?\s+agency|"
    r"not\s+by\s+itself|be\s+\d+\s+years|serve\s+(?:for\s+)?a\s+term|be\s+effective)\b", re.I)
from measure import _pages

# US actor terms, added for this run only (EU lexicons are not changed on disk)
A.EU = re.compile(A.EU.pattern + r"|\bthe\s+commission\b|\bcomptroller\s+general|\battorney\s+general|\bsecretary\s+of\b|"
                  r"\bfederal\b|\bthe\s+board\b|\bpcaob\b|\bsec\b|\bcongress\b|\bthe\s+president\b|\bdepartment\s+of\b", re.I)
A.MS = re.compile(r"\bstates?\b(?!\s+of\s+america)|\bstate\s+(regulatory\s+)?authorit|\bstate\s+boards?\b", re.I)
A.PRIV = re.compile(A.PRIV.pattern + r"|\bofficers?\b|\bdirectors?\b|\battorneys?\b|\baccountants?\b|audit\s+committee|"
                    r"\bmanagement\b|chief\s+(executive|financial)|principal\s+(executive|financial)|\bemployees?\b|"
                    r"accounting\s+firm|\bbroker|\bdealer|\banalyst|\bassociated\s+person|\bfirm\b", re.I)
LAB = {"private_parties": "private parties", "member_states": "US States", "eu_institutions": "federal government / regulators (SEC, PCAOB)",
       "unclear": "unclear / none"}

pdf, label = sys.argv[1], sys.argv[2]
raw = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
drop = re.compile(r"^\s*(\d+\s+STAT\.\s+\d+|PUBLIC LAW \d+–\d+—[A-Z]+\.? \d+, \d{4}|VerDate.*|\d+ USC \d+.*|"
                  r"Deadlines?\.|Reports?\.|Effective dates?\.|Regulations\.|Applicability\.|Termination date\.)\s*$")
lines = [l for l in raw.replace("\f", "\n").split("\n") if not drop.match(l)]
text = re.sub(r"-\n(?=[a-z])", "", "\n".join(lines))
body = text[text.find("SEC. 2."):] if "SEC. 2." in text else text
paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
# drop margin notes: very short fragments without a verb-like marker
paras = [p for p in paras if len(p.split()) > 3 or re.search(r"\b(shall|must|may)\b", p)]

INS = re.compile(r"‘‘.*?’’", re.S)


def run(ps):
    A._LAST["who"] = None
    res, addr, sample = {}, {}, []
    for cl in clauses(ps):
        inst, _ = find_instances(cl)
        for cat, a, b in inst:
            if cat == "obligation" and re.match(r"shall\s+be\s+unlawful", cl[a:a + 30], re.I):
                cat = "prohibition"            # US drafting: 'it shall be unlawful for ... to ...'
            res[cat] = res.get(cat, 0) + 1
            who, subj = A.addressee(re.sub(r"board\s+of\s+directors", "company directors", cl[:600], flags=re.I), min(a, 599))
            addr[who] = addr.get(who, 0) + 1
            sample.append({"clause": cl[:500], "marker": cl[a:b], "category": cat, "addressee": who})
    return res, addr, sample


joined = "\n\n".join(paras)
without = INS.sub(" ", joined)
out = {"label": label, "pages": _pages(open(pdf, "rb").read())}
for name, t in (("all_text", joined), ("excluding_inserted_text", without)):
    ps = [p for p in t.split("\n\n") if p.strip()]
    r, a, s = run(ps)
    out[name] = {"words": words(t), "restrictions_total": sum(r.values()), "by_category": r,
                 "by_addressee": {LAB[k]: v for k, v in a.items()}, "per_1000_words": round(1000 * sum(r.values()) / max(1, words(t)), 1)}
    json.dump(s, open(f"../data/benchmark_{label}_{name}_instances.json", "w"), indent=1)
out["inserted_text_words"] = out["all_text"]["words"] - out["excluding_inserted_text"]["words"]
json.dump(out, open(f"../data/benchmark_{label}.json", "w"), indent=1)
print(json.dumps(out, indent=1))
