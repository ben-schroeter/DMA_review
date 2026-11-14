"""Fills the hand-designed site pages from their sources, so the database is the one source of truth.
- Charts: every embedded chart sits between <!--@chart SOURCE--> and <!--@end-->. SOURCE is file:<path under site/> or
  json:<file>/<key>/<key>. The block is replaced with the current output of the chart builders.
- Figures: <span data-fact="KEY">…</span> gets the text of KEY in site/facts.json (written by site/facts.py).
- Data blocks: the Legal instruments list (const DATA, const FILES) and the evidence library (const S) are rebuilt
  from the database and site/studies_data.json.
--mark: one-off setup that wraps charts and figures that are not yet marked (see MARK_FACTS below).
--check: reports multi-digit figures in page text that are not tied to a fact.
Run from research/digital_rulebook."""
import re, json, glob, os, sys, collections, openpyxl

SITE = "site"; PAGES = sorted(glob.glob(f"{SITE}/mockup/*.dc.html"))
SKIP = lambda p: os.path.basename(p).startswith(("Act-", "Fc-")) or os.path.basename(p) in ("Instrument.dc.html", "Forthcoming.dc.html", "DigitalPolicy.dc.html", "FurtherReading.dc.html")

def load_source(src):
    kind, ref = src.split(":", 1)
    if kind == "file":
        t = open(f"{SITE}/{ref}").read().strip()
    else:
        f, *path = ref.split("/"); o = json.load(open(f"{SITE}/{f}"))
        for k in path: o = o[int(k)] if isinstance(o, list) else o[k]
        t = o.strip()
    return re.sub(r'^<svg xmlns="http://www.w3.org/2000/svg" ', "<svg ", t)

def all_sources():
    src = {}
    for f in glob.glob(f"{SITE}/*.svg") + glob.glob(f"{SITE}/infographics/*.svg") + glob.glob(f"{SITE}/*_table.html"):
        r = "file:" + os.path.relpath(f, SITE); src[r] = load_source(r)
    for f in ("mock_charts.json", "reporting_charts.json", "why_charts.json", "evidence_front_options.json", "gap_options.json", "hero_options.json"):
        if not os.path.exists(f"{SITE}/{f}"): continue
        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items(): walk(v, path + [k])
            elif isinstance(o, str) and o.lstrip().startswith("<svg"):
                src["json:" + "/".join([f] + path)] = load_source("json:" + "/".join([f] + path))
        walk(json.load(open(f"{SITE}/{f}")), [])
    return src

aria = lambda s: (re.search(r'aria-label="([^"]*)"', s[:4000]) or [None, None])[1]

def mark_charts(s, src):
    byexact = {v: k for k, v in src.items()}
    byaria = {}
    for k, v in src.items():
        a = aria(v)
        if a: byaria.setdefault(a.split(":")[0][:60], k)
    out, pos, n = [], 0, 0
    for m in re.finditer(r"<svg\b.*?</svg>", s, re.S):
        if s[max(0, m.start() - 200):m.start()].rstrip().endswith("-->") and "@chart" in s[max(0, m.start() - 200):m.start()]: continue
        sv = m.group(0); k = byexact.get(sv)
        if not k and aria(sv): k = byaria.get(aria(sv).split(":")[0][:60])
        if not k or len(sv) < 500: continue
        out.append(s[pos:m.start()] + f"<!--@chart {k}-->" + sv + "<!--@end-->"); pos = m.end(); n += 1
    out.append(s[pos:]); return "".join(out), n

def fill_charts(s):
    def rep(m):
        try: return f"<!--@chart {m.group(1)}-->" + load_source(m.group(1)) + "<!--@end-->"
        except Exception as e: print("  missing source", m.group(1), e); return m.group(0)
    return re.sub(r"<!--@chart (\S+?)-->.*?<!--@end-->", rep, s, flags=re.S)

FACTS = json.load(open(f"{SITE}/facts.json")) if os.path.exists(f"{SITE}/facts.json") else {}
def fill_facts(s):
    return re.sub(r'<span data-fact="([^"]+)">[^<]*</span>', lambda m: f'<span data-fact="{m.group(1)}">{FACTS[m.group(1)]["text"]}</span>' if m.group(1) in FACTS else m.group(0), s)

# figures to mark: (fact key, regex with one group for the number, in page text only)
MARK_FACTS = [
 ("laws_adopted", r"\b(105)(?= (?:adopted|laws|EU digital|legal instruments|of the|acts))"), ("laws_adopted", r"(?<=all )(105)\b"), ("laws_adopted", r"(?<=of )(105)(?= laws)"),
 ("obligations_main", r"\b(21,374)\b"), ("obligations_main_k", r"\b(21,400)\b"), ("words_m", r"\b(2\.5)(?=m| million)"),
 ("secondary_acts", r"\b(690)(?= implementing)"), ("implementing_acts", r"\b(605)(?= implementing)"), ("delegated_acts", r"\b(85)(?= delegated)"),
 ("obligations_secondary", r"\b(10,840)\b"), ("obligations_secondary_k", r"\b(10,800)\b"), ("amending_acts", r"\b(172)(?= amending)"),
 ("national_measures", r"\b(48,158)\b"), ("private_main", r"\b(7,106)\b"), ("private_secondary", r"\b(6,167)\b"), ("private_total", r"\b(13,273)\b"),
 ("private_total_k", r"\b(13,300)\b"), ("obligations_since_2018", r"\b(16,730)\b"), ("grew_in_negotiation", r"\b(84)(?= of 99)"), ("compared_with_proposal", r"(?<=84 of )(99)\b"),
 ("studies_evidence", r"\b(476)(?= (?:studies|evaluations|sources))"), ("studies_causal", r"\b(68)(?= (?:of them causal|with a causal|studies with a causal))"),
 ("sources_total", r"\b(571)(?= sources)"), ("objectives", r"\b(398)(?= objectives)"),
 ("obj_never_pct", r"\b(47%)(?= of those objectives)"), ("rs_main_n", r"\b(20,212)\b"), ("rs_secondary_n", r"\b(10,544)\b"), ("rs_total_k", r"\b(30,800)\b"),
 ("forthcoming_total", r"(?<=See all )(\d+)(?= forthcoming)"),
 ("src_official", r"(?<=: )(241)(?= official)"),
 ("ct_PR", r"\b(3,718)\b"), ("ct_FI", r"\b(3,413)\b"), ("ct_GK", r"\b(1,452)\b"), ("ct_CL", r"\b(1,358)\b"), ("ct_baseline", r"\b(1,987)\b"),
 ("ct_GK_2018", r"(?<=from )(21)(?= specific)"), ("ct_reporting_share", r"(?<=on companies, )(15%)"), ("firm_micro_pct", r"\b(93%)(?= of the rules)"),
 ("firm_company_obligations", r"\b(11,988)\b"), ("firm_relief_removed", r"(?<=only )(828)\b"), ("prohib_since_2018", r"\b(5\.8%)"), ("prohib_before_2018", r"(?<=about )(9\.5%)"),
 ("growth_words_median", r"(?<=grew by )(45%)"), ("growth_obligations_median", r"(?<= and )(27%)(?= in obligations)"), ("precision", r"\b(89%)(?= precision)"),
 ("rs_no_duty_main", r"(?<=impose no duty \()(1,137)"), ("rs_no_duty_secondary", r"(?<=\(1,137 and )(833)(?=\))"), ("rs_agreement", r"(?<=the coding agreed )(92%)"),
 ("rs_all_main_R", r"(?<=obligation, )(73%)(?= of those)"), ("rs_all_main_standard_like", r"(?<=are rules and )(25%)(?= are standards)"), ("rs_comp_main_R", r"(?<=much the same: )(72%)(?= rules)"),
 ("rs_all_sec_R", r"(?<=that follow, )(84%)(?= are rules)"), ("rs_comp_sec_R", r"(?<=rules, and )(83%)(?= of those on companies)"),
 ("rs_acts_more_rules", r"(?<=in )(26)(?= of the 30 laws)"), ("rs_acts_second_layer", r"(?<= of the )(30)(?= laws with a sizeable)"),
 ("rs_ecodesign_main", r"(?<=Ecodesign Regulation \()(65%)"), ("rs_ecodesign_sec", r"(?<=Ecodesign Regulation \(65% to )(94%)"),
 ("rs_csa_main", r"(?<=Cybersecurity Act \()(62%)"), ("rs_csa_sec", r"(?<=Cybersecurity Act \(62% to )(88%)"), ("rs_dora_main", r"(?<=DORA \()(55%)"), ("rs_dora_sec", r"(?<=DORA \(55% to )(81%)"),
 ("rs_nis2_main", r"(?<=falls from )(75%)"), ("rs_nis2_sec", r"(?<=from 75% to )(52%)"),
 ("precision", r"\b(89%)(?= were genuine| of counted| on EU acts| of counted items)"), ("precision", r"(?<=Approximate: )(89%)"),
 ("addressee_accuracy", r"(?<=correct for )(90%)"), ("addressee_accuracy", r"(?<=right )(90%)"),
 ("rep_total", r"\b(5,484)\b"), ("rep_private", r"(?<=Companies carry )(2,075)"), ("rep_states", r"(?<=member states )(1,826)"), ("rep_eu", r"(?<=EU institutions )(1,582)"),
 ("rep_precision", r"\b(94%)(?= of counted items were genuine reporting)"), ("rep_precision", r"(?<=were genuine \()(94%)"), ("rep_recall", r"(?<=estimated )(83%)"),
 ("rep_estimate_k", r"\b(6,200)\b"), ("evmap_check", r"(?<=found )(86%)"), ("us_precision", r"(?<=Precision on US text was )(80%)"), ("us_precision", r"(?<= and )(80%)(?= in US laws)"),
 ("sox_precision", r"\b(68%)(?= for Sarbanes-Oxley| on Sarbanes-Oxley)"), ("model_clauses_k", r"(?<=about )(4,800)(?= distinct)"),
 ("area_finance_k", r"(?<=hold about )(3,500)"), ("area_trust_k", r"(?<= and )(3,400)(?=\.)"),
 ("ex_ai_proposal", r"(?<=AI Act \()(392)"), ("ex_ai_adopted", r"(?<=AI Act \(392 to )(764)"), ("ex_mica_proposal", r"(?<=MiCA \()(766)"), ("ex_mica_adopted", r"(?<=MiCA \(766 to )(1,114)"),
 ("ex_ehds_proposal", r"(?<=Health Data Space \()(395)"), ("ex_ehds_adopted", r"(?<=Health Data Space \(395 to )(603)"), ("obj_never_pct", r"^(47%)$"), ("src_academic", r"\b(127)(?= academic)"), ("src_thinktank", r"\b(48)(?= think tank or NGO)"), ("src_industry", r"\b(51)(?= consultancy)"),
]
def text_segments(s):
    """Yields (start, end) of text between tags, outside svg/script/style and outside DC {{…}} and comments."""
    skip = 0
    for m in re.finditer(r"<!--.*?-->|<(/?)(svg|script|style|helmet)\b[^>]*>|<[^>]+>|[^<]+", s, re.S):
        g = m.group(0)
        if g.startswith("<"):
            if m.group(2):
                skip += -1 if m.group(1) else (0 if g.endswith("/>") else 1)
            continue
        if skip <= 0: yield m.start(), m.end()

def mark_facts(s):
    segs = list(text_segments(s)); out, pos, n = [], 0, 0
    blocks = [(m.start(), m.end()) for m in re.finditer(r"<!--@chart \S+?-->.*?<!--@end-->", s, re.S)]
    for a, b in segs:
        if any(x <= a < y for x, y in blocks): continue
        t = s[a:b]
        if re.search(r'<span data-fact="[^"]+">$', s[max(0, a - 80):a]): continue
        for key, rx in MARK_FACTS:
            t2 = re.sub(rx, lambda m: f'<span data-fact="{key}">{m.group(1)}</span>', t)
            if t2 != t: n += t2.count("data-fact") - t.count("data-fact"); t = t2
        out.append(s[pos:a] + t); pos = b
    out.append(s[pos:]); return "".join(out), n

def fill_data_blocks(p, s):
    name = os.path.basename(p)
    if name == "Instruments.dc.html":
        wb = openpyxl.load_workbook("digital_rulebook.xlsx", read_only=True, data_only=True)
        r = list(wb["instruments"].iter_rows(values_only=True)); h = r[0]; I = [dict(zip(h, x)) for x in r[1:] if x[0]]
        sr = list(wb["secondary_acts"].iter_rows(values_only=True)); sh = sr[0]
        nsec = collections.Counter(x[0] for x in sr[1:] if x[sh.index("kind")] in ("implementing", "delegated"))
        files = json.load(open(f"{SITE}/instrument_pages.json"))
        D = [[x["row_id"], x["name"], int(str(x["adoption_date"])[:4]), {"R": "Regulation", "L": "Directive", "D": "Decision"}.get(str(x["celex_measured"])[5:6], (x["identifier"] or "").split()[0]), x["policy_area"], x["restrictions_total"] or 0,
              nsec.get(x["row_id"], 0), x["impact_evidence_level"] or "none", x["n_impact_studies"] or 0]
             for x in sorted(I, key=lambda x: x["name"].lower()) if x["status"] == "adopted"]
        s = re.sub(r"const DATA = \[\[.*?\]\];", lambda m: "const DATA = " + json.dumps(D, ensure_ascii=False, separators=(",", ":")) + ";", s, count=1, flags=re.S)
        s = re.sub(r"const FILES = \{.*?\};", lambda m: "const FILES = " + json.dumps({str(k): v for k, v in files.items()}) + ";", s, count=1, flags=re.S)
    if name == "Studies.dc.html":
        L = json.load(open(f"{SITE}/studies_data.json"))["L"]
        s = re.sub(r"const S = \[\[.*?\]\];\n", lambda m: "const S = " + json.dumps(L, ensure_ascii=False) + ";\n", s, count=1, flags=re.S)
    return s


# any number in page text: thousands, percentages, decimals and plain integers of two or more digits
NUM = re.compile(r"(?<![\w.,/(§-])(?:\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?%|\d+\.\d+|\d{2,})(?![\w/-])")
ALLOW = []   # (page, figure, context substring) reviewed as not depending on the law set: site/check_allowlist.tsv
if os.path.exists(f"{SITE}/check_allowlist.tsv"):
    for l in open(f"{SITE}/check_allowlist.tsv"):
        if l.strip() and not l.startswith("#"):
            a, b, c, *_ = l.rstrip("\n").split("\t"); ALLOW.append((a, b, c))
def is_exempt(t, m):
    v = m.group(0); ctx = t[max(0, m.start() - 70):m.end() + 50]
    if re.fullmatch(r"(19|20)\d\d", v): return True                       # years
    if re.search(r"(Articles?|Arts?\.?|Annex|Recital|COM|SWD|SEC|No|Regulation \(EU\)|Directive \(EU\)|Decision \(EU\)|L|C)\s*\(?$", t[max(0, m.start() - 20):m.start()]): return True
    if re.match(r"\s?(px|em|rem)\b", t[m.end():m.end() + 4]): return True
    return any(pg in ("*", CUR_PAGE[0]) and fig == v and c in re.sub(r"\s+", " ", ctx) for pg, fig, c in ALLOW)
CUR_PAGE = [""]
CTX = []
def check(s, page=""):
    CUR_PAGE[0] = page
    found = collections.Counter()
    blocks = [(m.start(), m.end()) for m in re.finditer(r"<!--@chart \S+?-->.*?<!--@end-->|<!-- LATEST-PROPOSALS -->.*?<!-- /LATEST-PROPOSALS -->", s, re.S)]  # charts, and the proposal cards built from the same data as the skipped Fc- pages
    for a, b in text_segments(s):
        if re.search(r'<span data-fact="[^"]+">$', s[max(0, a - 80):a]) or any(x <= a < y for x, y in blocks): continue
        t = s[a:b]
        for m in re.finditer(NUM, t):
            if is_exempt(t, m): continue
            found[m.group(0)] += 1; CTX.append((page, m.group(0), re.sub(r"\s+", " ", t[max(0, m.start() - 70):m.end() + 50]).strip()))
    return found

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--fill"
    src = all_sources() if mode == "--mark" else None
    tot = collections.Counter()
    for p in PAGES:
        if SKIP(p):
            if mode == "--fill" and "precision" in FACTS:   # generated pages: only the shared footer figure
                s = open(p).read(); t = re.sub(r"approximate \(\d+% precision\)", f"approximate ({FACTS['precision']['text']} precision)", s)
                if t != s: open(p, "w").write(t); tot["pages_changed"] += 1
            continue
        s = open(p).read(); s0 = s
        if mode == "--mark":
            s, nc = mark_charts(s, src); s, nf = mark_facts(s); tot["charts"] += nc; tot["facts"] += nf
            if nc or nf: print(f"{os.path.basename(p)}: {nc} charts, {nf} figures marked")
        if mode in ("--mark", "--fill"):
            s = fill_data_blocks(p, fill_facts(fill_charts(s)))
        if mode == "--check":
            c = check(s, os.path.basename(p))
            if c: print(f"{os.path.basename(p)}: {sum(c.values())} untracked figures: " + ", ".join(f"{k}" for k, _ in c.most_common(12)))
            tot["untracked"] += sum(c.values())
        if s != s0: open(p, "w").write(s); tot["pages_changed"] += 1
    if mode == "--check":
        open(f"{SITE}/untracked_figures.txt", "w").write("Figures in page text not tied to site/facts.json (page | figure | context)\n" + "\n".join(f"{a} | {b} | {c}" for a, b, c in CTX))
    print(dict(tot))
