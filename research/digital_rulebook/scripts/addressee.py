"""Classify who a restriction binds: private parties, Member States, EU institutions, or unclear."""
import re
import spacy

NLP = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])

MS = re.compile(r"\bmember\s+states?\b|\b(national|competent|supervisory|regulatory|market\s+surveillance|notifying|designated|"
                r"judicial|tax|public|law\s+enforcement|requesting|requested|issuing|executing|enforcement|resolution|"
                r"customs|data\s+protection|audiovisual|media|statistical|screening)\s+(authorit|bod)|\bauthorit(y|ies)\b|"
                r"coordinators?\b|single\s+points?\s+of\s+contact|\bcsirts?\b|\bcourts?\b|\btribunals?\b|"
                r"\bnational\b|\bpublic\s+sector\s+bod|\bpublic\s+administrations?\b|\bcontracting\s+(authorit|entit)|"
                r"\bregulators?\b|\bnras?\b|\bthe\s+state\b|\bhost\s+member\s+state|\bhome\s+member\s+state", re.I)
EU = re.compile(r"\bcommission\b|\bcouncil\b|\beuropean\s+parliament\b|\bthe\s+board\b|\bboard\b|\bagency\b|\benisa\b|\besma\b|"
                r"\beba\b|\beiopa\b|\becb\b|\bamla\b|\bai\s+office\b|\bthe\s+office\b|\bedpb\b|\bedps\b|\beuropol\b|\beurojust\b|"
                r"\beu-lisa\b|\bfrontex\b|\bunion\s+(institutions?|bodies|body|agencies)|\bjoint\s+undertaking|\bthe\s+centre\b|"
                r"\bcommittee\b|\bcourt\s+of\s+justice|\bolaf\b|\beppo\b|\bthe\s+union\b|\beuropean\s+(supervisory|data|union)\b|"
                r"\bberec\b|\bbody\s+of\s+european|\bthe\s+authority\b|\bgoverning\s+board|\bexecutive\s+director|\bhadea\b|"
                r"\beuipo\b|\bcert-eu\b|\bsecretariat\b|\bthe\s+chair|\b(implementing|delegated)\s+acts?\b|"
                r"\bdelegation\s+of\s+power|\bthe\s+(executive\s+)?director\b|\biicb\b|\binterinstitutional|"
                r"\b(coordination|cooperation)\s+group|\bthe\s+Platform\b|\bUnion\s+entit", re.I)
PRIV = re.compile(r"provider|operator|manufacturer|importer|distributor|deployer|undertaking|controller|processor|"
                  r"gatekeeper|trader|platform|intermediar|issuer|offeror|institutions?\b|entit(y|ies)|data\s+holder|"
                  r"\busers?\b|\bhost|person|business|seller|supplier|holder|owner|employer|economic\s+operator|"
                  r"notified\s+bod|obliged|applicant|recipient|consumer|company|companies|firm|bank|insurer|"
                  r"service\s+providers?|publisher|broadcaster|licensee|rightholder|right\s+holder|organisations?|"
                  r"crypto-asset|investment|payment|merchant|marketplace|search\s+engine|developer|"
                  r"advertiser|sponsor|data\s+intermediation|beneficiar|participant|tenderer|party|parties|"
                  r"natural\s+or\s+legal|legal\s+person|natural\s+person|employee|worker|subscriber|authorised\s+representative|"
                  r"management\s+body|board\s+of\s+directors|auditor|custodian|trustee|manager|registr(y|ar)|\bcsds?\b|\bccps?\b|"
                  r"credit\s+institution|\bcasps?\b|bidder|space\s+operator|licensor|licensee", re.I)
PRONOUN = re.compile(r"^(it|they|he|she|which|who|that|this|these|those|such\s+\w+)$", re.I)


def classify_text(t):
    if not t:
        return None
    # priority: explicit EU body names, then Member State terms, then private actors
    if EU.search(t) and not re.search(r"\bcommission\s+(delegated|implementing)|\bunder\s+the\s+commission", t, re.I):
        if MS.search(t) and re.search(r"\bmember\s+states?\b", t, re.I) and not re.search(r"\bcommission\b", t, re.I):
            return "member_states"
        return "eu_institutions"
    if MS.search(t):
        return "member_states"
    if PRIV.search(t):
        return "private_parties"
    return None


def subject_text(doc, char_idx):
    tok = next((t for t in doc if t.idx <= char_idx < t.idx + len(t) + 1), None)
    if tok is None:
        return "", False
    verb = tok.head if tok.dep_ in ("aux", "auxpass", "neg") else tok
    passive = any(c.dep_ == "auxpass" for c in verb.children)
    for v in (verb, verb.head if verb.dep_ == "conj" else None):
        if v is None:
            continue
        subj = [c for c in v.children if c.dep_ in ("nsubj", "nsubjpass", "expl")]
        if subj:
            s = subj[0]
            span = doc[s.left_edge.i: s.right_edge.i + 1].text
            agent = ""
            if passive:
                for c in v.children:
                    if c.dep_ == "agent":
                        agent = doc[c.left_edge.i: c.right_edge.i + 1].text
            return (agent or span), passive and not agent
    return "", passive


_LAST = {"who": None}


def addressee(clause, start):
    doc = NLP(clause)
    subj, passive_no_agent = subject_text(doc, start)
    if PRONOUN.match(subj.strip()):
        cls_prev = classify_text(clause[:start][-120:])
        if cls_prev:
            return cls_prev, subj
        if _LAST["who"]:
            return _LAST["who"], subj
    res = _addressee(clause, start, subj, passive_no_agent)
    if res[0] != "unclear":
        _LAST["who"] = res[0]
    return res


def _addressee(clause, start, subj, passive_no_agent):
    cls = classify_text(subj)
    if cls and not passive_no_agent:
        return cls, subj
    if cls and passive_no_agent:
        # passive with no agent: the subject is what is acted upon, not who acts
        before = clause[:start]
        cls2 = classify_text(before[-120:])
        return (cls2 or "unclear"), subj
    cls2 = classify_text(clause[:start][-80:])
    return (cls2 or "unclear"), subj
