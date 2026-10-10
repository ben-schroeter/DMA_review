"""Turn EUR-Lex HTML into plain text and split it into parts."""
import html as htmllib, re

BLOCK = re.compile(r"</?(p|div|br|tr|li|h\d|table|td)[^>]*>", re.I)


def html_to_lines(raw):
    raw = re.sub(r"<(script|style|head)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"</td>", " ", raw, flags=re.I)          # keep table cells of one row together
    raw = BLOCK.sub("\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = htmllib.unescape(raw).replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", l).strip() for l in raw.split("\n")]
    return [l for l in lines if l]


ADOPTED = re.compile(r"^(HAS|HAVE) ADOPTED TH(IS|E PRESENT) (REGULATION|DIRECTIVE|DECISION|RECOMMENDATION)", re.I)
WHEREAS = re.compile(r"^Whereas\b", re.I)
ANNEX = re.compile(r"^ANNEX(ES)?(\s+[IVXLC0-9]+[a-z]?)?\s*$|^Annex(\s+[IVXLC0-9]+[a-z]?)?$")
DONE_AT = re.compile(r"^(Done at|Hecho en|Fait à) ", re.I)
LFS = re.compile(r"^LEGISLATIVE FINANCIAL (AND DIGITAL )?STATEMENT", re.I)
WORD = re.compile(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9'’\-]*")


def words(text):
    return len(WORD.findall(text))


def split_parts(lines, is_proposal=False):
    """Return dict part -> list of lines. Parts: memorandum, preamble, articles, annexes, financial_statement."""
    parts = {"memorandum": [], "preamble": [], "articles": [], "annexes": [], "financial_statement": []}
    start = 0
    if is_proposal:
        # legal text begins at the last 'Proposal for a ...' heading that is followed by 'Having regard'
        cands = [i for i, l in enumerate(lines) if re.match(r"^Proposal for an?\b", l, re.I)]
        for i in reversed(cands):
            if any(l.startswith("Having regard") for l in lines[i:i + 15]):
                start = i
                break
        parts["memorandum"] = lines[:start]
    adopted = next((i for i in range(start, len(lines)) if ADOPTED.match(lines[i])), None)
    if adopted is None:                 # e.g. Commission notices / guidance: no preamble split
        body_start = start
    else:
        parts["preamble"] = lines[start:adopted + 1]
        body_start = adopted + 1
    done = next((i for i in range(body_start, len(lines)) if DONE_AT.match(lines[i])), None)
    tail_start = done if done is not None else None
    if tail_start is None:
        tail_start = next((i for i in range(body_start, len(lines)) if ANNEX.match(lines[i])), len(lines))
    parts["articles"] = lines[body_start:tail_start]
    tail = lines[tail_start:]

    def is_annex(i, seq):
        nxt = " ".join(seq[i + 1:i + 3]).lower()
        return bool(ANNEX.match(seq[i])) and "financial statement" not in nxt and "legislative financial" not in nxt
    f = next((i for i, l in enumerate(tail) if LFS.match(l)), None)
    if f is None:
        a = next((i for i in range(len(tail)) if is_annex(i, tail)), None)
        if a is not None:
            parts["annexes"] = tail[a:]
    else:
        a_before = next((i for i in range(f) if is_annex(i, tail)), None)
        a_after = next((i for i in range(f + 1, len(tail)) if is_annex(i, tail)), None)
        if a_before is not None:
            parts["annexes"] = tail[a_before:f]
            parts["financial_statement"] = tail[f:]
        else:
            parts["financial_statement"] = tail[f:a_after] if a_after else tail[f:]
            parts["annexes"] = tail[a_after:] if a_after else []
    return parts


def recital_lines(preamble):
    i = next((k for k, l in enumerate(preamble) if WHEREAS.match(l)), None)
    return preamble[i:] if i is not None else []
