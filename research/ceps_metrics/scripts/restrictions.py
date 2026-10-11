"""Count restrictions in the enacting terms + annexes of an EU act (English text).

Categories and exclusions follow the method agreed for this project (see method sheet):
  prohibition            shall not / may not / must not / (shall be|is|are) prohibited / prohibited
  restricted_permission  may only / shall only / may ... only if|where|when|to the extent|after|for
  duty_of_result         shall ensure
  obligation             shall (remaining) / must
  explicit_requirement   'is/are required (to)', 'mandatory', 'obliged to', 'an obligation to', 'requirement to'
                         (bare nouns such as 'the obligations laid down in Article 5' are cross-references, not counted)
                         (counted only in clauses with no other counted marker, to avoid double counting)
Excluded uses of 'shall': entry into force / application / binding-ness, definitions and legal
fictions, amendment instructions, saving clauses, rights and entitlements. Quoted amending text is skipped.
"""
import re

EXCLUDE_SHALL = re.compile(
    r"\bshall\s+(?:(?:also|therefore|nevertheless|however|thereafter|only|then|not)\s+)?(?:"
    r"enter\s+into\s+force|apply|continue\s+to\s+apply|cease\s+to\s+(?:apply|have\s+effect|be\s+in\s+force)|"
    r"be\s+binding|have\s+effect|take\s+effect|expire|"
    r"mean|be\s+deemed|be\s+considered|be\s+construed|be\s+understood|be\s+read|be\s+regarded|be\s+presumed|"
    r"refer\s+to|"
    r"be\s+amended|be\s+replaced|be\s+inserted|be\s+added|be\s+deleted|be\s+repealed|be\s+corrected|be\s+renumbered|"
    r"be\s+without\s+prejudice|affect|prejudice|not\s+affect|not\s+prejudice|not\s+apply|"
    r"have\s+the\s+right|be\s+entitled|be\s+empowered|have\s+the\s+power|be\s+conferred|have\s+access\s+to\s+justice|enjoy|"
    r"be\s+addressed\s+to\s+the\s+Member\s+States|"
    # constitutive / organisational rules that bind no one (added after validation round 1)
    r"be\s+calculated|be\s+computed|be\s+apportioned|be\s+composed|consist|be\s+chaired|have\s+jurisdiction|"
    r"be\s+in\s+the\s+form\s+of|be\s+taxed|be\s+(?:jointly\s+and\s+severally\s+)?liable|not\s+be\s+liable|"
    r"(?:not\s+)?become\s+applicable|be\s+tacitly\s+extended|put\s+an\s+end|not\s+preclude|be\s+guided|"
    r"be\s+financed|be\s+eligible|be\s+valid|remain\s+valid|remain\s+in\s+force|be\s+extended\s+(?:by|if|where|to)|"
    r"be\s+suspended|be\s+interrupted|begin\s+to\s+run|run\s+from|"
    # round 2 (held-out false positives)
    r"be\s+determined\s+(?:in\s+accordance|on\s+the\s+basis|by\s+reference)|occur|become\s+(?:chargeable|due|payable|effective)|"
    r"be\s+limited\s+to|be\s+allocated|be\s+EUR|amount\s+to|have\s+(?:the\s+)?(?:equivalent\s+)?(?:same\s+)?legal\s+effect|"
    r"remain\s+with|not\s+result\s+in|not\s+entail|be\s+null\s+and\s+void|be\s+(?:automatically\s+)?void|"
    # round 3 (October 2026 addressee recheck): committee boilerplate
    r"be\s+assisted\s+by\s+(?:a|the)\s+committee|be\s+a\s+committee\s+within\s+the\s+meaning)\b", re.I)
DEFN_INCLUDE = re.compile(r"\bshall\s+(?:also\s+)?(?:include|comprise|cover)\b", re.I)
NEG_SUBJECT = re.compile(r"\b(?:no|neither|nor)\s+(?:[\w\-’']+\s+){0,5}?shall\b", re.I)
EXCLUDE_OTHER = re.compile(r"\b(?:is|are)\s+(?:hereby\s+)?(?:replaced|amended|inserted|deleted|repealed)\b|"
                           r"\bshall\s+be\s+amended\s+as\s+follows\b", re.I)

PROHIB = re.compile(r"\b(?:shall\s+not|may\s+not|must\s+not|shall\s+be\s+prohibited|(?:is|are)\s+(?:hereby\s+)?prohibited|prohibited)\b", re.I)
RESTR = re.compile(r"\b(?:may\s+only|shall\s+only|may\b(?:\s+\S+){1,12}?\s+only\s+(?:if|where|when|to\s+the\s+extent|after|for|in|on|with|be))\b", re.I)
DUTY = re.compile(r"\bshall\s+ensure\b", re.I)
OBLIG = re.compile(r"\b(?:shall|must|(?:has|have)\s+to)\b(?!\s+be\s+(?:noted|borne\s+in\s+mind))", re.I)
REQ = re.compile(r"\b(?:(?:is|are|be|been|being)\s+(?:\w+\s+)?required\b(?!\s+by\s+(?:Article|this|Regulation|Directive))|"
                 r"required\s+to\s+\w+|mandatory|obliged\s+to|(?:under|have|has|an?)\s+(?:\w+\s+)?obligation\s+to|"
                 r"requirement\s+to\s+\w+)", re.I)

CLAUSE_SPLIT = re.compile(r"(?<=[;:])\s+|(?<=\.)\s+(?=[A-Z(‘“])")


AMEND_INTRO = re.compile(r"(replaced\s+by(?:\s+the\s+following)?|(?:replaced|supplemented|amended)\s+(?:with|by)\s+the\s+following(?:\s+[\w()]+){0,2}|"
                         r"inserted|added|substituted|following\s+(?:point|paragraph|article|subparagraph|"
                         r"sentence|text|words|annex|section|chapter|title|indent|recital)s?\b.*|as\s+follows|reads?\s+as\s+follows)\s*:?\s*$", re.I)
OPEN_Q = ("‘", "“", "\"")
CLOSE_Q = ("’", "”", "\"")


def strip_quoted(lines):
    """Drop text inserted by amendment instructions: quoted blocks that follow a line like
    '... is replaced by the following:' and run until a line ends with a closing quote."""
    out, inq, prev = [], False, ""
    for l in lines:
        s = l.strip()
        if inq:
            if s.rstrip(" ;,.").endswith(CLOSE_Q):
                inq = False
            continue
        if s.startswith(OPEN_Q) and AMEND_INTRO.search(prev):
            if not s.rstrip(" ;,.").endswith(CLOSE_Q):
                inq = True
            continue                      # quoted amending text: skip (single or multi-line)
        out.append(l)
        prev = s
    return out


def clauses(lines):
    text = "\n".join(lines)
    for para in text.split("\n"):
        for c in CLAUSE_SPLIT.split(para):
            c = c.strip()
            if c:
                yield c


def find_instances(clause):
    """Return list of (category, start, end) for one clause, without double counting overlapping markers."""
    taken, inst = [], []

    def free(a, b):
        return all(b <= x or a >= y for x, y in taken)

    # 'no Member State shall apply ...' is a prohibition even though 'shall apply' is otherwise excluded
    for m in NEG_SUBJECT.finditer(clause):
        a = m.end() - 5
        taken.append((a, m.end())); inst.append(("prohibition", a, m.end()))
    excl = [(m.start(), m.end()) for m in EXCLUDE_SHALL.finditer(clause)] + \
           [(m.start(), m.end()) for m in EXCLUDE_OTHER.finditer(clause)]
    # 'shall include/comprise/cover' is definitional only in definitions (quoted term or 'for the purposes of')
    if re.search(r"‘|“|\bfor\s+the\s+purposes?\s+of\b|\bthe\s+terms?\b", clause, re.I):
        excl += [(m.start(), m.end()) for m in DEFN_INCLUDE.finditer(clause)]
    excl = [e for e in excl if all(e[1] <= x or e[0] >= y for x, y in taken)]
    taken.extend(excl)
    for cat, rx in (("prohibition", PROHIB), ("restricted_permission", RESTR), ("duty_of_result", DUTY), ("obligation", OBLIG)):
        for m in rx.finditer(clause):
            a, b = m.start(), m.end()
            if cat == "restricted_permission" and m.group(0).lower().startswith("may") and " only " not in m.group(0).lower() + " ":
                continue
            if free(a, b):
                taken.append((a, b)); inst.append((cat, a, b))
    if not inst:
        for m in REQ.finditer(clause):
            if free(m.start(), m.end()):
                inst.append(("explicit_requirement", m.start(), m.end()))
    return inst, len(excl)
