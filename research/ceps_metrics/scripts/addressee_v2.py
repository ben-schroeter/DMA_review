"""Addressee classifier, version 2 (October 2026). See data/addressee/CODEBOOK.md.

Works on the instance dump (scripts/addr_dump.py), which carries each restriction's article heading,
list lead-in and the preceding text of the same article. For every restriction it returns
  formal            private_parties | member_states | eu_institutions | no_actor | unclear
  ultimately_bound  same codes; differs for duties on states/EU bodies that govern another actor's conduct
  how               which rule set the code (subject, agent, lead_in, previous, heading, article, product, act_rule, no_actor, v1)

Order: the v1 reading of the grammatical subject is kept when it found an actor (with a few corrections);
otherwise the actor is looked for in context, nearest first."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from addressee import NLP, subject_text, classify_text as v1_classify, PRONOUN

P, M, E, N, U = "private_parties", "member_states", "eu_institutions", "no_actor", "unclear"

# ---- extra terms found in the diagnosis sample (classify before the v1 lists) ----
EU_X = re.compile(r"\bcompetence\s+centre\b|\beccc\b|\blead\s+overseers?\b|\besas\b|\bjoint\s+committee\b|"
                  r"\binvesteu\s+(fund|advisory\s+hub|portal|guarantee)\b|\bthe\s+eic\b|\beic\s+(board|fund)\b|\beit\b|"
                  r"\bhigh-level\s+group\b|\bsub-groups?\b|\beu\s+centre\b|\b(advisory|scientific|expert)\s+(group|panel|forum)s?\b|"
                  r"\beurostat\b|\bexecutive\s+agenc|\bombudsman\b|\bedib\b|\b(ehds|data\s+innovation)\s+board\b|"
                  r"\bprogramme\s+committee\b|\beuropean\s+(health|data)\s+[a-z ]*board\b|\bunion\s+guarantee\b", re.I)
MS_X = re.compile(r"\bhealth\s+data\s+access\s+bod|\bsingle\s+liaison\s+offices?\b|\bliaison\s+offices?\b|"
                  r"\b(judges?|prosecutors?|investigating\s+judges?)\b|\bnational\s+statistical\b|\bstatistical\s+authorit|"
                  r"\bcentral\s+offices?\b|\bintellectual\s+property\s+offices?\b|\bpolice\b|\bpublic\s+prosecutor", re.I)
P_X = re.compile(r"\bconformity\s+assessment\s+bod|\bcertification\s+bod|\bcontractors?\b|\bprivate\s+members?\b|"
                 r"\bdlt\s+market\s+infrastructure|\bdata\s+sharing\s+schemes?\b|\bcourier|\btaxable\s+persons?\b|"
                 r"\bchurches\b|\breligious\s+associations\b|\bspace\s+operators?\b|\bspacecraft\s+operators?\b|"
                 r"\bwhite\s+paper\s+offeror|\bpersons?\s+seeking\s+admission|\bmanufacturers?\b|\bimporters?\b", re.I)

# subjects that are documents, products or abstract things: someone else must act
THING = re.compile(r"^(the\s+|such\s+|that\s+|those\s+|this\s+|these\s+|each\s+|any\s+|all\s+|an?\s+)?([\w\-’' ]+\s)?"
                   r"(documentation|documents?|reports?|notifications?|applications?|requests?|information|registers?|lists?|plans?|"
                   r"statements?|records?|certificates?|declarations?|labels?|notices?|decisions?|measures?|procedures?|agreements?|"
                   r"contracts?|orders?|data|polic(y|ies)|summar(y|ies)|assessments?|descriptions?|templates?|forms?|database|systems?|"
                   r"terms|conditions|codes?|instructions|logs?|white\s+papers?|invoices?|returns?|programmes?|strategy|strategies|"
                   r"machinery|products?|toys?|equipment|devices?|components?|parts?|spacecraft|vehicles?|machines?|guards?|"
                   r"controls?|software|models?|warnings?|markings?|evidence|copies|copy|translations?|fees?|charges?|"
                   r"contributions?|financing|support|operations?|actions?|work\s+programme|mechanism|network|tests?|checks?|audits?)\b", re.I)
PRODUCT = re.compile(r"\b(machinery|machines?|products?|toys?|equipment|devices?|components?|spacecraft|vehicles?|guards?|"
                     r"control\s+systems?|batteries|packaging|substances?|mixtures?|appliances?|tractors?|trailers?|cabs?|"
                     r"seats?|software|hardware|ai\s+systems?|high-risk\s+ai\s+systems?)\b", re.I)
# legal effect, status or time rules with no actor
NOACT = re.compile(r"\bshall\s+(re)?start\b|\bshall\s+(begin|start)\s+to\s+run\b|\blimitation\s+period\b|\bshall\s+be\s+valid\b|"
                   r"\bshall\s+have\s+legal\s+personality\b|\bshall\s+enjoy\s+the\s+most\s+extensive\s+legal\s+capacity\b|"
                   r"\bshall\s+be\s+(an?\s+)?(body|office)\s+of\s+the\s+union\b|\bshall\s+be\s+dealt\s+with\b|"
                   r"\bshall\s+be\s+expressed\s+in\b|\bshall\s+be\s+rounded\b|\bshall\s+correspond\s+to\b|\bshall\s+be\s+equal\s+to\b", re.I)
AGENT = re.compile(r"\b(?:shall|must)\s+(?:not\s+)?be\s+\w+(?:ed|en|ne|wn|de)\b[^.;:]{0,60}?\bby\s+((?:the|a|an|each|any|all|its)\s+[^,.;:()]{3,80})", re.I)

# act-specific readings (CELEX -> {term regex: class})
ACT_RULES = {
    "32018R1725": [(re.compile(r"\bcontrollers?\b|\bprocessors?\b|\bunion\s+institution|\bdata\s+protection\s+officer", re.I), E)],
    "32023R2841": [(re.compile(r"\bunion\s+entit|\blocal\s+cybersecurity\s+officer|\bhighest\s+level\s+of\s+management", re.I), E)],
    "32022R0858": [(re.compile(r"\boperators?\s+of\s+(a\s+)?dlt", re.I), P)],
}


def classify(t, doc=""):
    """Class of a text naming an actor, or None. Extra terms first, then act rules, then the v1 lists."""
    if not t:
        return None
    for rx, cls in ACT_RULES.get(doc, []):
        if rx.search(t):
            return cls
    if EU_X.search(t) and not re.search(r"\bmember\s+states?\b", t, re.I):
        return E
    if MS_X.search(t):
        return M
    if P_X.search(t) and not re.search(r"\bcommission\b|\bmember\s+states?\b|\bauthorit", t, re.I):
        return P
    return v1_classify(t)


def subj_of(text, doc):
    """Class of the subject of the main verb of `text` (falls back to other subjects in order)."""
    text = text.strip()
    if not text:
        return None
    d = NLP(text[:400])
    roots = [t for t in d if t.dep_ == "ROOT"]
    toks = [c for r in roots for c in r.children if c.dep_ in ("nsubj", "nsubjpass")] + \
           [t for t in d if t.dep_ in ("nsubj", "nsubjpass")]
    for tok in toks:
        if True:
            span = d[tok.left_edge.i: tok.right_edge.i + 1].text
            if PRONOUN.match(span.strip()) or THING.match(span.strip()):
                continue
            c = classify(span, doc)
            if c:
                return c
    return None


SENT = re.compile(r"(?<=[.;])\s+(?=[A-Z(])")


def last_sentences(before, k=2):
    s = [x for x in SENT.split(before.strip()) if len(x) > 15 and not re.match(r"^\(?\d+\.?\)?$", x)]
    return s[-k:][::-1]


def formal(r, art_major):
    doc, cl, pos, subj = r["doc"], r["clause"], r["pos"], (r["subject"] or "").strip()
    s_cls = classify(subj, doc)
    thing = bool(THING.match(subj)) or PRONOUN.match(subj) or not subj
    # act-specific rules override v1 where they name the subject
    if r["addressee"] != U:
        if s_cls and s_cls != r["addressee"] and any(rx.search(subj) for rx, _ in ACT_RULES.get(doc, [])):
            return s_cls, "act_rule"
        return r["addressee"], "v1"
    if s_cls and not thing:
        return s_cls, "subject"
    # an actor named directly before the marker ("... all Member States shall take ...")
    near = re.search(r"([\w\-’' ]{3,60})\s*$", cl[:pos])
    if near:
        c = classify(near.group(1), doc)
        if c and not re.search(r"\b(of|to|by|with|from|for|in|on|that|which|whom)\s+[\w\-’' ]*$", near.group(1), re.I):
            return c, "near"
    m = AGENT.search(cl[max(0, pos - 5):])
    if m and classify(m.group(1), doc):
        return classify(m.group(1), doc), "agent"
    if NOACT.search(cl):
        return N, "no_actor"
    if r["chapeau"]:
        c = subj_of(r["chapeau"], doc) or classify(r["chapeau"][:160], doc)
        if c:
            return c, "lead_in"
    for s in last_sentences(r["before"]):
        c = subj_of(s, doc)
        if c:
            return c, "previous"
    c = classify(r["heading"], doc)
    if c:
        return c, "heading"
    if r["article"].lower().startswith("annex") and PRODUCT.search(subj + " " + cl[:200]):
        return P, "product"
    if PRODUCT.search(subj) and not re.search(r"\bauthorit|\bcommission\b|\bmember\s+state", cl, re.I):
        return P, "product"
    c = art_major.get((doc, r["article"]))
    if c:
        return c, "article"
    return U, "unclear"


ULT = re.compile(r"\b(?:shall\s+ensure|shall\s+require|shall\s+oblige|shall\s+impose|shall\s+(?:take|adopt)\s+(?:the\s+)?(?:necessary\s+)?measures"
                 r"|shall\s+lay\s+down\s+rules)\b(.{0,160})", re.I)


def ultimately(r, f):
    if f not in (M, E):
        return f
    m = ULT.search(r["clause"][max(0, r["pos"] - 2):])
    if not m:
        return f
    tail = m.group(1)
    m2 = re.search(r"\b(?:that|whereby|requiring|to\s+require|so\s+that)\s+(.{0,90})", tail, re.I) or re.match(r"\s*(.{0,90})", tail)
    if not m2:
        return f
    t = m2.group(1)
    if re.search(r"\bpenalt|\bsanction", tail[:60], re.I):
        return f
    c = classify(t, r["doc"])
    return P if c == P else f


def run(rows):
    # article majority among v1-classified restrictions (used only as a last resort)
    cnt = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["addressee"] != U:
            cnt[(r["doc"], r["article"])][r["addressee"]] += 1
    art_major = {}
    for k, c in cnt.items():
        top, n = c.most_common(1)[0]
        if n >= 3 and n / sum(c.values()) >= 0.75:
            art_major[k] = top
    out = []
    for r in rows:
        f, how = formal(r, art_major)
        out.append({"formal": f, "ultimately_bound": ultimately(r, f), "how": how})
    return out


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "main"
    D = os.path.join(os.path.dirname(__file__), "..", "data", "addressee")
    rows = [json.loads(l) for l in open(os.path.join(D, f"instances_{kind}.jsonl"))]
    res = run(rows)
    with open(os.path.join(D, f"v2_{kind}.jsonl"), "w") as f:
        for r, x in zip(rows, res):
            f.write(json.dumps({"doc": r["doc"], "article": r["article"], "pos": r["pos"], "v1": r["addressee"], **x}) + "\n")
    print("formal", collections.Counter(x["formal"] for x in res))
    print("ultimately bound", collections.Counter(x["ultimately_bound"] for x in res))
    print("how", collections.Counter(x["how"] for x in res))
