"""Rules vs standards (Kaplow 1992): word-list first pass. Codes an obligation S (standard) when it carries an open-ended term,
L when the provision says its content will be specified by a delegated or implementing act, technical standard or guidelines,
D when it leaves the content to member states, otherwise R (rule). M (mixed) is assigned when an open-ended term sits next to a
bright-line anchor (number, date, period, closed list). Imported by the pilot check and the full run."""
import re
OPEN = re.compile(r"\b(appropriate(ly)?|reasonabl[ey]|proportionate(ly)?|adequate(ly)?|sufficient(ly)?|effective(ly)?|necessary|"
                  r"diligen(ce|t)|due care|fair(ly|ness)?|non-discriminatory|objectively justified|justified|"
                  r"where (relevant|appropriate|applicable|necessary|possible)|as appropriate|to the extent possible|"
                  r"state of the art|risk-based|in good faith|best efforts|regular(ly)?|periodically|"
                  r"clear(ly)?,? (and )?(plain|intelligible|comprehensible)|easily accessible|user-friendly|"
                  r"coheren(t|ce)|in a timely manner|swift(ly)?|as soon as possible|significant(ly)?|"
                  r"high level of|legitimate interests?|take into (account|consideration)|having regard to|"
                  r"ensure (the )?(security|protection|coherence|consistency|effective)|all (relevant|necessary) (information|measures))\b", re.I)
LATER = re.compile(r"(delegated act|implementing act|regulatory technical standards?|implementing technical standards?|harmonised standards?|"
                   r"common specifications?|guidelines)[^.;]{0,80}(specif|lay(ing)? down|detail|adopted pursuant)|"
                   r"(as specified|specified|laid down|set out) in (the )?(applicable |relevant )?(delegated|implementing) act", re.I)
MSDISC = re.compile(r"\bMember States? (shall|may) (determine|lay down (the )?rules|decide|provide for (appropriate|effective)|choose)", re.I)
ANCHOR = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|ten|thirty|ninety)\s+(working |calendar )?(days?|hours?|months?|years?|weeks?)\b|"
                    r"\b(by|before|not later than|at the latest by) \d{1,2} [A-Z][a-z]+ \d{4}|\b\d+ ?%|\bannually|every \w+ (months|years)|"
                    r"the following|at least", re.I)
UNDUE = re.compile(r"without undue delay|immediately", re.I)


def code(clause, chapeau=""):
    t = f"{chapeau or ''} {clause}"
    if LATER.search(t):
        return "L"
    if MSDISC.search(clause):
        return "D"
    o = OPEN.search(clause)
    if o:
        return "M" if ANCHOR.search(clause) else "S"
    return "R"
