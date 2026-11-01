"""Reporting obligations: which counted obligations require someone to pass on, publish, register or keep information.

Works on the instance dumps (scripts/addr_dump.py: instances_main.jsonl, instances_secondary.jsonl) and the final
addressee coding (scripts/addressee_v2.apply). An obligation is a reporting obligation when the action it requires
(the predicate after the marker, or the duty a "shall ensure that ..." clause imposes) is to report, notify, submit,
transmit, communicate or provide information, publish or disclose it, register, or keep records or documentation.
Clauses whose subject is the document itself ("The report shall include ...") only specify content: they are tagged
"content" and not counted as separate reporting obligations.

For each reporting obligation it records
  type       report_submission | notification | on_request | disclosure | registration | record_keeping
  recipient  commission | eu_body | ep_council | national_authority | public_users | business | unspecified
  cadence    periodic | one_off | event | on_request | ongoing | unspecified   (+ period / deadline when stated)
  review     True for EU institutions' review and evaluation reports on the act itself
Writes data/reporting/reporting_instances.jsonl and data/reporting/summary.json. See data/reporting/METHOD.md."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import addressee_v2

D = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(D, "reporting")

# ---------- lexicon ----------
V_REPORT = r"(report(?:s|ed|ing)?|submit(?:s|ted|ting)?|transmit(?:s|ted|ting)?|forward(?:s|ed)?|send(?:s)?|sent|send\s+back|lodge(?:s|d)?|file(?:s|d)?(?=\s+(?:a|an|the|with))|communicate(?:s|d)?)"
V_NOTIFY = r"(notif(?:y|ies|ied|ying)|alert(?:s|ed)?)"
V_INFORM = r"(inform(?:s|ed)?|provide(?:s|d)?|supply|supplies|supplied|make(?:s)?\s+available|made\s+available|share(?:s|d)?|give(?:s)?|given|furnish(?:es|ed)?|deliver(?:s|ed)?)"
V_PUBLISH = r"(publish(?:es|ed)?|make(?:s)?\s+public(?:ly\s+available)?|made\s+public(?:ly\s+available)?|disclose(?:s|d)?|display(?:s|ed)?|post(?:s|ed)?\s+on)"
V_REGISTER = r"(register(?:s|ed)?|enter(?:s|ed)?\s+(?:\w+\s+){0,4}in(?:to)?\s+the\s+(?:\w+\s+){0,3}(?:register|database|registry)|record(?:s|ed)?\s+in\s+the\s+(?:\w+\s+){0,3}(?:register|database))"
V_KEEP = r"((?:keep|keeps|kept|retain(?:s|ed)?|maintain(?:s|ed)?|store(?:s|d)?|preserve(?:s|d)?|archive(?:s|d)?)\b[^.;]{0,80}\b(?:records?|logs?|documentation|documents|register|registry|copies|copy|files?|data|information|evidence|accounts|minutes)|draw(?:s|n)?\s+up\s+(?:\w+\s+){0,3}(?:technical\s+)?documentation|(?:keep|keeps|kept)\s+(?:\w+\s+){0,6}at\s+the\s+disposal|record(?:s|ed)?\s+(?!in\s+the\s+(?:\w+\s+){0,3}(?:register|database))(?:the|all|any|each|every|details|information|data))"
INFO_OBJ = r"(information|data|details|documents?|documentation|reports?|statistics|notifications?|evidence|explanations?|copies|copy|records?|results|list|summary|figures|particulars|declarations?|statements?|reasons|justifications?|certificates?|instructions|observations|opinions|findings|decisions?|descriptions?|overviews?|updates?|stud(?:y|ies)|analys[ie]s|assessments?|plans?|datasets?)"

RECIP = [  # first match wins, searched in the predicate
    ("ep_council", r"european\s+parliament\s*(?:,|and)\s*(?:to\s+)?the\s+council|parliament\s+and\s+the\s+council"),
    ("eu_body", r"\b(european\s+data\s+protection\s+supervisor|esma|eba|eiopa|enisa|europol|eurojust|eu-lisa|ecb|european\s+central\s+bank|edpb|edps|board|agency|authority\s+for\s+anti-money|amla|ai\s+office|office|esas|joint\s+committee|berec|eccc|competence\s+centre|eppo|olaf|court\s+of\s+auditors)\b"),
    ("commission", r"\bcommission\b"),
    ("national_authority", r"\b(competent\s+authorit(?:y|ies)|supervisory\s+authorit(?:y|ies)|national\s+(?:\w+\s+){0,2}authorit(?:y|ies)|regulatory\s+authorit(?:y|ies)|market\s+surveillance\s+authorit(?:y|ies)|digital\s+services\s+coordinator|coordinators?|csirts?|single\s+points?\s+of\s+contact|notifying\s+authorit(?:y|ies)|notified\s+bod(?:y|ies)|tax\s+authorit(?:y|ies)|financial\s+intelligence\s+units?|fius?|authorit(?:y|ies)\s+of\s+the\s+member\s+state|member\s+states?|the\s+authorit(?:y|ies))\b"),
    ("public_users", r"\b(persons?\s+concerned|natural\s+or\s+legal\s+persons?|public|publicly|website|online\s+interface|recipients?\s+of\s+the\s+service|users?|end[- ]users?|consumers?|customers?|clients?|data\s+subjects?|natural\s+persons?|individuals?|investors?|holders?|passengers?|patients?|workers?|employees?|subscribers?|payers?|payees?|travellers?|citizens?|platform\s+workers?)\b"),
    ("business", r"\b(third\s+part(?:y|ies)|implementing\s+partners?|deployers?|distributors?|importers?|manufacturers?|providers?|operators?|downstream|business\s+users?|undertakings?|institutions?|entities|controllers?|processors?|traders?|suppliers?|counterpart(?:y|ies)|issuers?|offerors?|data\s+holders?|gatekeepers?|insurers?|banks?)\b"),
]

PERIOD = [  # (label, pattern) for periodic cadences
    ("monthly", r"\bmonthly\b|\bevery\s+month\b|\beach\s+month\b"),
    ("quarterly", r"\bquarterly\b|\bevery\s+(?:three|3)\s+months\b|\beach\s+quarter\b"),
    ("half-yearly", r"\bsemi-annual(?:ly)?\b|\bhalf-yearly\b|\bevery\s+(?:six|6)\s+months\b|\btwice\s+a\s+year\b"),
    ("annual", r"\bannual(?:ly)?\b|\bevery\s+year\b|\beach\s+(?:calendar\s+|financial\s+)?year\b|\byearly\b|\bonce\s+a\s+year\b|\bat\s+least\s+once\s+(?:a|per|every)\s+year\b|\bper\s+year\b"),
    ("every 2 years", r"\bevery\s+(?:two|2)\s+years\b|\bbiennial(?:ly)?\b|\bevery\s+second\s+year\b"),
    ("every 3 years", r"\bevery\s+(?:three|3)\s+years\b|\btriennial(?:ly)?\b"),
    ("every 4 years", r"\bevery\s+(?:four|4)\s+years\b"),
    ("every 5+ years", r"\bevery\s+(?:five|six|seven|eight|ten|5|6|7|8|10)\s+years\b"),
    ("regular", r"\bregular(?:ly)?\b|\bperiodic(?:al(?:ly)?)?\b|\bon\s+a\s+regular\s+basis\b"),
]
DEADLINE = re.compile(r"\bwithin\s+(\d+|one|two|three|four|five|six|seven|ten|fifteen|twenty|thirty)\s+(hours?|working\s+days?|business\s+days?|days?|weeks?|months?)\b", re.I)
WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "ten": 10, "fifteen": 15, "twenty": 20, "thirty": 30}
PROMPT = re.compile(r"\bwithout\s+(?:undue\s+)?delay\b|\bimmediately\b|\bpromptly\b|\bforthwith\b|\bas\s+soon\s+as\s+possible\b", re.I)
ONREQ = re.compile(r"\b(?:up)?on\s+(?:a\s+)?(?:reasoned\s+|duly\s+justified\s+|written\s+)?request\b|\bat\s+the\s+request\s+of\b|\bwhen\s+requested\b|\bwhere\s+requested\b|\bif\s+requested\b|\bupon\s+demand\b|\bon\s+demand\b|\bat\s+(?:its|their)\s+request\b|\brequest(?:ed)?\s+by\s+the\b", re.I)
EVENT = re.compile(r"\b(incident|breach|infringement|serious|malfunction|risk|change|changes|modif|amend|intends?\s+to|intention|planned|prior\s+to|before\s+(?:starting|placing|putting|launching|implementing|concluding|the\s+start)|suspicio|threat|attack|failure|withdrawal|recall|non-?complian|termination|occurr|event|discover|become[s]?\s+aware|becoming\s+aware|detect|where\s+an?\b|if\s+an?\b|in\s+the\s+event)\w*", re.I)
ONEOFF = re.compile(r"\b(?:by|no\s+later\s+than|not\s+later\s+than|before)\s+\d{1,2}\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b|\bby\s+\[|\bupon\s+(?:entry\s+into\s+force|adoption)\b|\bwhen\s+(?:submitting|applying)\b|\bapplication\s+for\b|\bbefore\s+(?:placing|putting)\b", re.I)
ONGOING = re.compile(r"\bup\s+to\s+date\b|\bat\s+all\s+times\b|\bcontinuous(?:ly)?\b|\bon\s+an\s+ongoing\s+basis\b|\bfor\s+(?:a\s+(?:period|minimum)\s+of\s+)?(?:at\s+least\s+)?(\d+|one|two|three|four|five|six|seven|ten)\s+years\b", re.I)
REVIEW = re.compile(r"\b(evaluat\w*|review\w*|application\s+of\s+this|functioning\s+of\s+this|implementation\s+of\s+this|operation\s+of\s+this|impact\s+of\s+this|progress)\b", re.I)
DOC_SUBJECT = re.compile(r"^\s*(?:\d+\.\s*)?(?:\([a-z0-9]+\)\s*)?(?:the|that|such|this|those|these|each|every|any|all|an?)\s+(?:[\w\-’' ]{0,40}\s)?(fields?|columns?|reports?|notifications?|information|summar(?:y|ies)|documentation|records?|statements?|declarations?|lists?|registers?|databases?|templates?|forms?|requests?|applications?|disclosures?|publications?|plans?)\b(?!\s+(?:shall\s+)?(?:be\s+)?(?:submitted|sent|transmitted|notified|published|made|communicated|forwarded|provided|kept|registered|entered|reported|lodged|filed|disclosed|stored|retained))", re.I)


def predicate(r):
    """The text the obligation governs: from the marker to the end of the clause (or the next 'shall'), plus the
    lead-in when the clause is a list item completing it."""
    c, a = r["clause"], int(r["pos"])
    tail = c[a:]
    nxt = re.search(r"\b(shall|must)\b", tail[len(r["marker"]):], re.I)
    if nxt:
        tail = tail[: len(r["marker"]) + nxt.start()]
    return tail


ADVERB = re.compile(r"^(?:\s*(?:,\s*)?(?:not|also|at\s+least|in\s+particular|in\s+any\s+event|immediately|promptly|forthwith|"
                    r"without\s+(?:undue\s+)?delay|where\s+(?:appropriate|necessary|relevant|applicable)|as\s+(?:appropriate|necessary|soon\s+as\s+possible)|"
                    r"if\s+(?:appropriate|necessary)|regularly|periodically|annually|every\s+year|each\s+year|jointly|electronically|take\s+(?:appropriate\s+|all\s+(?:necessary\s+|appropriate\s+)?|the\s+necessary\s+)?(?:measures|steps)\s+to|"
                    r"(?:up)?on\s+(?:a\s+)?(?:reasoned\s+)?request|be\s+able\s+to|be\s+required\s+to|be\s+obliged\s+to|be\s+in\s+a\s+position\s+to|have\s+to|endeavour\s+to|"
                    r"(?:by|no\s+later\s+than)\s+\d{1,2}\s+\w+\s+\d{4}|and|or)\b\s*,?)+", re.I)
INSERT = re.compile(r"^\s*,[^,]{0,140},")
VERBS = [  # (type, main-verb pattern at the start of the action, needs an information object)
    ("record_keeping", r"(?:keep|retain|maintain|store|preserve|archive)\b(?![^.;]{0,30}\bbackup)[^.;]{0,70}\b(?:records?|logs?|documentation|documents|register|registry|copies|copy|files?|accounts|minutes|evidence|information|data)\b|be\s+recorded\b|be\s+(?:kept|retained|stored|archived)\b|draw\s+up\s+(?:\w+\s+){0,3}(?:technical\s+)?documentation|keep\s+(?:\w+\s+){0,8}at\s+the\s+disposal|record\s+(?:the|all|any|each|every|details|information|data)\b|(?:indicate|record|note|state|document)\s+in\s+the\s+(?:case\s+)?(?:file|record|register|minutes)\b|document\s+(?:the|all|any|each|their|its)\b", False),
    ("registration", r"(?:be\s+)?recorded\s+in\s+the\s+(?:\w+\s+){0,3}(?:register|database|registry)|make\s+(?:\w+\s+){0,10}available\s+in\s+the\s+(?:\w+\s+){0,3}(?:register|database|registry)|enter\s+(?:\w+\s+){0,6}(?:information|data|details)\s+(?:\w+\s+){0,3}in(?:to)?\s+the\s+(?:\w+\s+){0,6}(?:system|platform|register|database|registry|portal)|register\b|be\s+registered\b|enter\s+(?:\w+\s+){0,5}in(?:to)?\s+the\s+(?:\w+\s+){0,3}(?:register|database|registry)|be\s+entered\s+(?:\w+\s+){0,3}in(?:to)?\s+the|apply\s+for\s+registration", False),
    ("notification", r"notify\b|be\s+notified\b|alert\b|(?:a\s+|the\s+)?notifications?\s+(?:is|are)\s+made\b|make\s+(?:a\s+|the\s+)?notifications?\b", False),
    ("disclosure", r"(?:be\s+)?made\s+(?:easily\s+|publicly\s+|directly\s+)?accessible\b|make\s+(?:\w+\s+){0,8}accessible\s+to\b|publish\b|be\s+published\b|make\s+(?:\w+\s+){0,8}public(?:ly\s+available)?\b|be\s+made\s+public(?:ly\s+available)?\b|disclose\b|be\s+disclosed\b|display\s+(?:\w+\s+){0,4}(?:information|details|notice|warning|statement|terms|price)", False),
    ("report", r"report\b(?=\s+(?:to|on|annually|every|each|regularly|without|any|all|the|their|its|such|in|immediately|at|serious|incidents?|suspicio))|be\s+reported\b|submit\b|be\s+submitted\b|transmit\b|be\s+transmitted\b|forward\b|be\s+forwarded\b|send\b|be\s+sent\b|lodge\b|be\s+lodged\b|file\b(?=\s+(?:a|an|the|with))|communicate\b|be\s+communicated\b", False),
    ("inform", r"inform\b|be\s+informed\b|keep\s+(?:\w+\s+){0,4}informed\b", False),
    ("provide", r"(?:provide|supply|make\s+(?:[\w\-’']+,?\s+){0,10}?available|be\s+made\s+available|share|give|furnish|deliver|be\s+provided|be\s+supplied|be\s+given)\b", True),
]
# third-person forms used after "ensure that <subject>"
def _finite(p):
    return (p.replace("keep|retain|maintain|store|preserve|archive", "keeps?|retains?|maintains?|stores?|preserves?|archives?|kept|retained|maintained|stored")
             .replace("register\\b", "registers?\\b|(?:is|are)\\s+registered\\b").replace("notify\\b", "notif(?:y|ies)\\b|(?:is|are)\\s+notified\\b")
             .replace("publish\\b", "publish(?:es)?\\b|(?:is|are)\\s+published\\b").replace("submit\\b", "submits?\\b|(?:is|are)\\s+submitted\\b")
             .replace("transmit\\b", "transmits?\\b|(?:is|are)\\s+(?:sent|transmitted|forwarded|communicated|reported)\\b").replace("inform\\b", "informs?\\b|(?:is|are)\\s+informed\\b")
             .replace("provide|supply|make\\s+available", "provides?|supplies|supply|makes?\\s+available|(?:is|are)\\s+(?:provided|made\\s+available)")
             .replace("communicate\\b", "communicates?\\b").replace("disclose\\b", "discloses?\\b").replace("report\\b(?=", "reports?\\b(?="))
FINITE = [(t, _finite(p), o) for t, p, o in VERBS]
OBJ = re.compile(r"^[^.;]{0,90}?\b" + INFO_OBJ + r"\b", re.I)
NOT_INFO = re.compile(r"^\s*(?:\w+\s+){0,3}(?:legislative\s+)?proposals?\b|^\s*(?:\w+\s+){0,3}draft\s+(?:regulatory|implementing)\s+technical\s+standards|^\s*(?:\w+\s+){0,6}(?:aid|help)\b|^\s*(?:\w+\s+){0,2}(?:funding|financial|support|assistance|access|training|services?|products?|goods|equipment|resources|staff|security|guarantees?|compensation|remed)", re.I)


def action(pred):
    """The start of the action the obligation requires: marker removed, leading adverbials and comma insertions skipped."""
    t = re.sub(r"^\s*(?:shall|must|is\s+required\s+to|are\s+required\s+to|is\s+obliged\s+to|are\s+obliged\s+to|may\s+only|shall\s+not|must\s+not)\b", "", pred, flags=re.I)
    for _ in range(4):
        t2 = ADVERB.sub("", INSERT.sub("", t))
        if t2 == t:
            break
        t = t2
    return t.strip()


EXCLUDE = re.compile(r"^(?:adopt\s+and\s+publish|adopt\s+and\s+communicate|bring\s+into\s+force|provide\s+for\b|be\s+entered\s+in\s+the\s+language|"
                     r"(?:\w+\s+){0,12}(?:the\s+)?(?:laws|regulations)\s+and\s+administrative\s+provisions\s+necessary)", re.I)
INTERNAL = re.compile(r"\b(?:to|inform)\s+(?:the\s+|its\s+|their\s+)?(?:management\s+body|board\s+of\s+directors|senior\s+management|compliance\s+function|"
                      r"supervisory\s+function|management\s+board|head\s+of\s+the\s+internal|internal\s+audit|general\s+meeting|shareholders)", re.I)


def match_verbs(act, table):
    if EXCLUDE.match(act):
        return None
    for t, p, needs_obj in table:
        m = re.match(r"(?:(?:(?!to\b|in\s+order\b)[\w\-]+,?\s+){1,7}?(?:and|or)\s+)?(?:" + p + r")", act, re.I)
        if m:
            rest = act[m.end():]
            if INTERNAL.search(act[:m.end() + 80]):
                return None
            if t in ("report", "provide") and NOT_INFO.match(rest):
                return None
            if needs_obj and not OBJ.match(rest):
                return None
            return t, m.group(0)[:40]
    return None


def detect(r):
    """Return (type, verb) when the obligation's action is a reporting action, else (None, reason)."""
    c = r["clause"]
    if DOC_SUBJECT.match(c[: int(r["pos"])] + " ") and r["category"] in ("obligation", "explicit_requirement"):
        if not re.match(r"\s*(?:shall|must)\s+be\s+(?:submitted|sent|transmitted|notified|published|made|communicated|forwarded|provided|kept|registered|entered|reported|lodged|filed|disclosed|stored|retained)", c[int(r["pos"]):], re.I):
            return None, "content"
    act = action(predicate(r))
    subj = c[: int(r["pos"])]
    # format and content instructions for a report or template are not separate reporting obligations
    if re.match(r"(?:be\s+)?reported\s*(?:as\b|in\s+(?:utc|the\s+format|accordance|euro|eur\b|thousands|units)|separately|either|using|with\b|for\s+each|:|[.;]?\s*$)|report\s+(?:the\s+|a\s+|any\s+)?(?:\w+\s+){0,3}(?:amount|value|date|figure|number|percentage)s?\s+as\b|be\s+entered\s+in\s+the\s+format|be\s+(?:made|given|submitted)\s+(?:electronically|in\s+(?:the|a|an)\s+(?:format|language|form))", act, re.I) \
            or re.search(r"\b(?:field|column|row|template|table|cell|data\s+point)s?\s*$", subj.strip(), re.I) and r["category"] != "prohibition":
        return None, "content"
    # a ban on disclosing is a confidentiality rule, not a reporting obligation
    if r["category"] == "prohibition" and re.match(r"(?:disclose|publish|make\s+public|transmit|communicate|share)\b", act, re.I):
        return None, "confidentiality"
    if INTERNAL.search(act[:300]):
        return None, "internal"
    if re.match(r"(?:ensure|guarantee)\s+that\s+(?:\w+\s+){0,3}(?:annual\s+|periodic\s+)?reports?\s+(?:include|contain|cover|set\s+out)", act, re.I):
        return None, "content"
    # internal reporting: to the company's own management or owners
    if re.search(r"\b(?:management\s+bod(?:y|ies)|board\s+of\s+directors|senior\s+management|general\s+meeting)\b", subj, re.I) and re.match(r"be\s+(?:informed|submitted|reported|notified)", act, re.I):
        return None, "internal"
    # passive keeping only for records and information, not plans or confidentiality
    if re.match(r"be\s+(?:kept|retained|stored|archived)\b", act, re.I):
        if re.match(r"be\s+kept\s+(?:confidential|secret|up[- ]to[- ]date|under|safe|separate)", act, re.I) or not re.search(
                r"\b(?:records?|data|information|documents?|documentation|logs?|copies|copy|registers?|files?|evidence|accounts|minutes|details|ledgers?|certificates?|declarations?)\b", subj, re.I):
            return None, "no_verb"
    if re.match(r"make\s+(?:[\w\-’']+,?\s+){0,10}?available\s+(?:in|on|through|via)\s+(?:a|the|its)\s+(?:\w+\s+){0,2}(?:public|publicly|website|online)", act, re.I):
        return "disclosure", "make available publicly"
    if re.match(r"(?:present|prepare|draw\s+up|produce|issue)\s+(?:and\s+(?:publish|submit|transmit)\s+)?(?:a|an|the|its|their)\s+(?:\w+\s+){0,3}reports?\b", act, re.I):
        return "report", act[:40]
    # information as the subject of a passive: "That information shall, on request, be supplied to ..."
    if re.match(r"be\s+(?:made\s+available|provided|supplied|given|shared)\b", act, re.I) and re.search(r"\b" + INFO_OBJ + r"\b", subj, re.I):
        return "provide", act[:40]
    m = re.search(r"\b(?:and|,)\s+(?:shall\s+)?(?:submit|present)\s+(?:a|an|the|its|their)\s+(?:\w+\s+){0,2}reports?\b", act[:260], re.I)
    if m and not re.match(r"(?:adopt|bring)", act, re.I):
        return "report", m.group(0)[:40]
    m = re.match(r"be\s+responsible\s+for\s+(submitting|reporting|notifying|providing|transmitting|publishing|registering|keeping|informing)\b", act, re.I)
    if m:
        return {"submitting": "report", "reporting": "report", "transmitting": "report", "providing": "report", "notifying": "notification",
                "publishing": "disclosure", "registering": "registration", "keeping": "record_keeping", "informing": "inform"}[m.group(1).lower()], m.group(0)[:40]
    hit = match_verbs(act, VERBS)
    if hit:
        return hit
    m = re.match(r"(?:ensure|guarantee|require)\s+(?:\w+\s+){0,3}?that\s+(.{0,260})", act, re.I)
    if m:
        emb = m.group(1)
        mm = re.search(r"\b(?:shall|must|will|is\s+required\s+to|are\s+required\s+to)\s+(.*)", emb, re.I)
        if mm and mm.start() < 160:
            hit = match_verbs(action(mm.group(1)), VERBS)
        else:
            for k in range(0, min(len(emb), 70)):
                if k == 0 or emb[k - 1] == " ":
                    hit = match_verbs(emb[k:], FINITE)
                    if hit:
                        break
        if hit:
            return hit
    return None, "no_verb"


def recipient(pred, t):
    low = pred.lower()
    if t == "record_keeping":
        return "unspecified"
    if t == "disclosure" and re.search(r"\bpublish|\bpublic|\bwebsite|\bdisclose", low):
        if not re.search(r"\bto\s+the\s+(?:commission|competent|supervisory|authorit)", low):
            return "public_users"
    m = re.search(r"\b(?:to|with|inform(?:s|ed)?|notif(?:y|ies|ied)|alert)\s+(?:the\s+|its\s+|their\s+|all\s+|any\s+|each\s+|relevant\s+)?(.{0,120})", low)
    seg = m.group(1) if m else low
    for lab, p in RECIP:
        if re.search(p, seg, re.I):
            return lab
    for lab, p in RECIP:
        if re.search(p, low, re.I):
            return lab
    return "unspecified"


def cadence(text, t):
    low = text.lower()
    for lab, p in PERIOD:
        if re.search(p, low):
            if lab == "regular" and t in ("record_keeping",):
                break
            return "periodic", lab, None
    d = DEADLINE.search(low)
    if d:
        n = d.group(1); n = int(n) if n.isdigit() else WORDNUM[n]
        unit = d.group(2).split()[0][:3]
        hours = n * {"hou": 1, "wor": 24, "bus": 24, "day": 24, "wee": 168, "mon": 720}[unit]
        if ONREQ.search(low):
            return "on_request", None, hours
        return "event", f"within {n} {d.group(2)}", hours
    if ONREQ.search(low):
        return "on_request", None, None
    if PROMPT.search(low):
        return "event", "without delay", None
    if ONEOFF.search(low):
        return "one_off", None, None
    if t == "record_keeping" or ONGOING.search(low):
        return "ongoing", None, None
    if t == "notification" or EVENT.search(low):
        return "event", None, None
    return "unspecified", None, None


def classify(r, addr):
    t, why = detect(r)
    if t is None:
        return {"reporting": False, "why": why}
    ctx = (r.get("chapeau") or "") + " " + r["clause"]
    pred = predicate(r)
    cad, period, hours = cadence(ctx, t)
    typ = {"report": "report_submission", "provide": "report_submission", "inform": "notification"}.get(t, t)
    if cad == "on_request" and typ in ("report_submission", "notification"):
        typ = "on_request"
    rec = recipient(pred, typ)
    if rec == "unspecified" and typ != "record_keeping" and r.get("chapeau"):
        rec = recipient(r["chapeau"], typ)
    if typ in ("report_submission", "notification") and rec == "public_users":
        typ = "disclosure"
    review = (addr in ("eu_institutions",) and rec in ("ep_council",) and bool(REVIEW.search(ctx))) or \
             (addr == "eu_institutions" and bool(re.search(r"\b(evaluat|review)\w*\s+(?:of\s+)?this\s+(regulation|directive|decision)", ctx, re.I)))
    return {"reporting": True, "verb": why, "type": typ, "recipient": rec, "cadence": cad, "period": period,
            "deadline_hours": hours, "review": review}


def load(kind):
    rows = [json.loads(l) for l in open(os.path.join(D, "addressee", f"instances_{kind}.jsonl"))]
    res = addressee_v2.apply(rows)
    out = []
    for r, x in zip(rows, res):
        if x.get("model_not_a_restriction"):
            continue          # read as not an obligation at all; excluded from the published counts too
        r["addr"] = x["ultimately_bound"]
        r["formal_addr"] = x["formal"]
        out.append(r)
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    out, stats = [], collections.Counter()
    for kind in ("main", "secondary"):
        for r in load(kind):
            x = classify(r, r["addr"])
            stats[(kind, x["reporting"], x.get("why") if not x["reporting"] else x["type"])] += 1
            out.append({"doc": r["doc"], "kind": kind, "article": r["article"], "heading": r["heading"], "pos": r["pos"],
                        "marker": r["marker"], "category": r["category"], "addressee": r["addr"],
                        "chapeau": r["chapeau"][-300:], "clause": r["clause"], **x})
    with open(os.path.join(OUT, "reporting_instances.jsonl"), "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    for k, v in sorted(stats.items(), key=lambda kv: (kv[0][0], not kv[0][1], -kv[1])):
        print(k, v)
