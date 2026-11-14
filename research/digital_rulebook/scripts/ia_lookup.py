"""Impact assessments and Regulatory Scrutiny Board opinions for the adopted laws (run when inputs change; writes data/ia/).

Step 1 (Cellar SPARQL, publications.europa.eu): proposal CELEX (data/proposals.json) -> interinstitutional dossier ->
         procedure number and the staff documents (CELEX 5YYYYSCnnnn) filed in the dossier.
Step 2 (Commission register API): type and title of each staff document (IMPACT_ASSESS, IMPACT_ASSESS_SUM, SWD, ...).
Step 3 (Legislative Observatory procedure file): SEC documents attached to the procedure; register metadata identifies
         Regulatory Scrutiny Board / Impact Assessment Board opinions; their PDF gives the overall verdict.
Run from research/digital_rulebook: python3 scripts/ia_lookup.py [step]"""
import json, re, subprocess, sys, os, time
OUT = "data/ia"
def curl(url, *extra, out=None):
    args = ["curl", "-sSL", "-m", "90", url, *extra] + (["-o", out] if out else [])
    r = subprocess.run(args, capture_output=True, text=not out)
    return r.stdout
def sparql(Q):
    r = subprocess.run(["curl", "-sS", "-m", "120", "-G", "https://publications.europa.eu/webapi/rdf/sparql", "--data-urlencode", "query=" + Q,
                        "-H", "Accept: application/sparql-results+json"], capture_output=True, text=True)
    return [{k: v["value"] for k, v in b.items()} for b in json.loads(r.stdout)["results"]["bindings"]]
REG = "https://ec.europa.eu/transparency/documents-register/api"
def ref_of_celex(c):  # 52020SC0348 -> SWD(2020)348 or SEC(2020)348 decided by register lookup
    return c[1:5], int(c[7:11])

step = sys.argv[1] if len(sys.argv) > 1 else "all"
links = json.load(open("data/proposals.json"))["links"]
if step in ("all", "1"):
    out = {}
    props = sorted({p for v in links.values() for p in v.get("all_linked_proposals", []) if p.startswith("5")})
    for i in range(0, len(props), 40):
        vals = " ".join(f'"{p}"^^<http://www.w3.org/2001/XMLSchema#string>' for p in props[i:i + 40])
        rows = sparql(f'''PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?pc ?proc ?mc WHERE {{ VALUES ?pc {{ {vals} }} ?w cdm:resource_legal_id_celex ?pc . ?w cdm:work_part_of_dossier ?d .
 OPTIONAL {{ ?d owl:sameAs ?proc . FILTER(CONTAINS(STR(?proc), "/procedure/")) }}
 OPTIONAL {{ ?m cdm:work_part_of_dossier ?d . ?m cdm:resource_legal_id_celex ?mc . FILTER(REGEX(STR(?mc), "^5[0-9]{{4}}SC")) }} }}''')
        for r in rows:
            o = out.setdefault(r["pc"], {"procedures": set(), "sc": set()})
            if r.get("proc"): o["procedures"].add(r["proc"].rsplit("/", 1)[1])
            if r.get("mc"): o["sc"].add(r["mc"])
        time.sleep(1)
    json.dump({k: {"procedures": sorted(v["procedures"]), "sc": sorted(v["sc"])} for k, v in out.items()}, open(f"{OUT}/cellar.json", "w"), indent=1)
    print("step 1:", len(out), "proposals with a dossier of", len(props))

def reg(ref):
    p = f"{OUT}/reg/{ref}.json"
    if os.path.exists(p): return json.load(open(p))
    os.makedirs(f"{OUT}/reg", exist_ok=True)
    try: d = json.loads(curl(f"{REG}/search/{ref}?lang=en"))
    except Exception: d = {}
    if d.get("status") and d.get("status") != 200 and "reference" not in d: d = {}
    json.dump(d, open(p, "w")); time.sleep(0.3)
    return d
def title_of(d):
    t = [v.get("title") for a in d.get("attachments", []) for lang, v in a.get("linguisticVersions", {}).items() if lang == "en" and v.get("title")]
    t = t or [v.get("title") for a in d.get("attachments", []) for v in a.get("linguisticVersions", {}).values() if v.get("title")]
    return (t[0] if t else d.get("title")) or ""
RX = re.compile(r"\b(SWD|SEC)\s*\((\d{4})\)\s*0*(\d+)")
if step in ("all", "2"):
    cel = json.load(open(f"{OUT}/cellar.json"))
    laws = {}
    for law, v in links.items():
        props = [p for p in v.get("all_linked_proposals", []) if p.startswith("5")]
        rec = json.load(open(f"data/impact/{law}.json")) if os.path.exists(f"data/impact/{law}.json") else {}
        text = rec.get("impact_assessment") or ""
        refs = {f"{k}({y}){int(n)}" for k, y, n in RX.findall(text)}
        procs = sorted({pr for p in props for pr in cel.get(p, {}).get("procedures", [])})
        for p in props:
            for c in cel.get(p, {}).get("sc", []):
                y, n = ref_of_celex(c)
                for k in ("SWD", "SEC"):
                    d = reg(f"{k}({y}){n}")
                    if d.get("reference"): refs.add(f"{k}({y}){n}"); break
        docs = {r: {"type": reg(r).get("type"), "title": title_of(reg(r))[:300], "date": reg(r).get("date")} for r in sorted(refs)}
        laws[law] = {"proposals": props, "proposal_date": v.get("proposal_date"), "procedures": procs, "record_text": text, "docs": docs}
    json.dump(laws, open(f"{OUT}/laws.json", "w"), indent=1, ensure_ascii=False)
    print("step 2:", len(laws), "laws;", sum(1 for x in laws.values() if any(d["type"] == "IMPACT_ASSESS" for d in x["docs"].values())), "with a register IMPACT_ASSESS document")

# ---------- step 3: classify each law (full / swd / none / codification / pre / unknown)
if step in ("all", "3"):
    L = json.load(open(f"{OUT}/laws.json")); OV = json.load(open(f"{OUT}/overrides.json"))
    st = {}
    for law, v in L.items():
        if law in OV:
            st[law] = {k: OV[law][k] for k in ("status", "main", "note")}; continue
        py = int((v["proposal_date"] or "0000")[:4]); t = (v["record_text"] or "").lower()
        ias = [r for r, d in v["docs"].items() if d["type"] == "IMPACT_ASSESS" and py - 2 <= int(r[4:8]) <= py]
        swds = [r for r, d in v["docs"].items() if d["type"] == "SWD" and py - 1 <= int(r[4:8]) <= py]
        if ias:
            s = "full"; main = ias
        elif py and py < 2003:
            s = "pre"; main = []
        elif "codif" in t:
            s = "codification"; main = []
        elif swds:
            s = "swd"; main = swds
        else:
            s = "none"; main = []
        st[law] = {"status": s, "main": main, "note": v["record_text"]}
    json.dump(st, open(f"{OUT}/ia_status.json", "w"), indent=1, ensure_ascii=False)
    import collections; print("step 3:", collections.Counter(x["status"] for x in st.values()))

# ---------- step 4: Regulatory Scrutiny Board (from 2016) / Impact Assessment Board opinions, via the procedure file
def oeil_secs(proc):  # "2020_361" -> SEC refs attached to the procedure
    y, n = proc.split("_")
    for suf in ("COD", "CNS", "NLE", "APP", "SYN"):
        ref = f"{y}/{int(n):04d}({suf})"
        p = f"{OUT}/oeil/{y}_{n}_{suf}.html"
        if not os.path.exists(p):
            os.makedirs(f"{OUT}/oeil", exist_ok=True)
            curl(f"https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference={ref}", out=p); time.sleep(0.5)
        s = open(p, encoding="utf-8", errors="ignore").read()
        if ref in s and "Key events" in s:
            return ref, sorted({f"SEC({a}){int(b)}" for a, b in re.findall(r"SEC\((\d{4})\)(\d{4})", s)})
    return None, []
def opinion(ref):
    d = reg(ref)
    if d.get("type") != "OPIN_IMPACT_ASSESS": return None
    a = (d.get("attachments") or [{}])[0]
    ers = next((v.get("ersId") for v in a.get("linguisticVersions", {}).values() if v.get("ersId")), None)
    p = f"{OUT}/rsb/{ref}.pdf"
    if ers and not os.path.exists(p):
        os.makedirs(f"{OUT}/rsb", exist_ok=True)
        curl(f"{REG}/files/{ref}_0/{ers}?rendition=false", out=p); time.sleep(0.3)
    txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout if os.path.exists(p) else ""
    m = re.search(r"Overall opinion\s*:?\s*(POSITIVE WITH RESERVATIONS|POSITIVE|NEGATIVE)", txt, re.I)
    board = "Impact Assessment Board" if re.search(r"Impact Assessment Board", txt) and not re.search(r"Regulatory Scrutiny Board", txt) else "Regulatory Scrutiny Board"
    return {"ref": ref, "date": d.get("date"), "verdict": m.group(1).lower() if m else None, "board": board, "url": f"{REG}/files/{ref}_0/{ers}?rendition=false" if ers else ""}
if step in ("all", "4"):
    L = json.load(open(f"{OUT}/laws.json")); S = json.load(open(f"{OUT}/ia_status.json"))
    res = {}
    for law, s in S.items():
        if s["status"] != "full": continue
        procs = L[law]["procedures"]
        ops = []; oref = None
        for pr in procs:
            oref, secs = oeil_secs(pr)
            for sref in secs:
                o = opinion(sref)
                if o: ops.append(o)
        res[law] = {"procedure": oref, "opinions": sorted(ops, key=lambda o: o["date"] or "")}
    json.dump(res, open(f"{OUT}/rsb.json", "w"), indent=1)
    import collections
    print("step 4:", len(res), "laws with an IA;", sum(1 for v in res.values() if v["procedure"]), "procedure found;",
          sum(1 for v in res.values() if v["opinions"]), "with an opinion;", collections.Counter(o["verdict"] for v in res.values() for o in v["opinions"]))

# ---------- step 5: every verdict in each opinion; for a negative opinion, look for the resubmission opinion
# among neighbouring SEC numbers (same impact assessment title)
def verdicts(ref):
    p = f"{OUT}/rsb/{ref}.pdf"
    t = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout if os.path.exists(p) else ""
    title = (re.search(r"Title\s*:\s*(.+)", t) or [None, ""])[1].strip()
    found = re.findall(r"Overall\s+(?:(\d)\s*(?:st|nd|rd|th)\s+)?opinion\s*:?\s*(POSITIVE WITH RESERVATIONS|POSITIVE|NEGATIVE)", t, re.I)
    seq = sorted(((int(o) if o else 1), i, v.lower()) for i, (o, v) in enumerate(found))   # by ordinal (1st, 2nd), then order in the text
    return [v for _, _, v in seq], title
if step in ("all", "5"):
    R = json.load(open(f"{OUT}/rsb.json"))
    for law, v in R.items():
        for o in v["opinions"]:
            o["verdicts"], o["title"] = verdicts(o["ref"])
        if v["opinions"] and all(o["verdicts"][-1:] == ["negative"] for o in v["opinions"] if o["verdicts"]):
            o0 = v["opinions"][0]; y, n = re.match(r"SEC\((\d{4})\)(\d+)", o0["ref"]).groups(); n = int(n)
            for k in list(range(n + 1, n + 25)) + list(range(max(1, n - 24), n)):
                cand = f"SEC({y}){k}"
                o = opinion(cand)
                if not o: continue
                o["verdicts"], o["title"] = verdicts(cand)
                if o["title"] and o0["title"] and o["title"].lower() == o0["title"].lower() and o["ref"] not in {x["ref"] for x in v["opinions"]}:
                    v["opinions"].append(o)
            v["opinions"].sort(key=lambda o: (o["date"] or "", o["ref"]))
        allv = [x for o in v["opinions"] for x in o["verdicts"]]
        v["first"] = allv[0] if allv else None; v["final"] = allv[-1] if allv else None
    json.dump(R, open(f"{OUT}/rsb.json", "w"), indent=1)
    import collections
    print("step 5:", collections.Counter((v["first"], v["final"]) for v in R.values() if v["opinions"]))

# ---------- step 6: for impact assessments from 2016 without an opinion found, read the verdict from the
# impact assessment's own annex on procedural information ("the Board issued a ... opinion")
if step in ("all", "6"):
    R = json.load(open(f"{OUT}/rsb.json")); S = json.load(open(f"{OUT}/ia_status.json"))
    VRX = re.compile(r"(negative|positive with reservations|positive)\s+opinion|opinion\s*(?:was|is)?\s*:?\s*(negative|positive with reservations|positive)", re.I)
    for law, v in R.items():
        mains = S[law]["main"]
        if v["opinions"] or not mains or int(mains[0][4:8]) < 2016: continue
        ref = mains[0]; d = reg(ref)
        a = (d.get("attachments") or [{}])[0]
        ers = next((x.get("ersId") for lang, x in a.get("linguisticVersions", {}).items() if lang == "en" and x.get("ersId")), None) \
              or next((x.get("ersId") for x in a.get("linguisticVersions", {}).values() if x.get("ersId")), None)
        p = f"{OUT}/ia_pdf/{ref}.pdf"
        if ers and not os.path.exists(p):
            os.makedirs(f"{OUT}/ia_pdf", exist_ok=True); curl(f"{REG}/files/{ref}_0/{ers}?rendition=false", out=p); time.sleep(0.5)
        t = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout if os.path.exists(p) else ""
        t1 = re.sub(r"\s+", " ", t)
        hits = []
        for m in re.finditer(r"Regulatory Scrutiny Board", t1):
            seg = t1[m.start(): m.start() + 600]
            hits += [(x[0] or x[1]).lower() for x in VRX.findall(seg)]
        if hits:
            first = hits[0]; final = "positive with reservations" if "positive with reservations" in hits and hits[0] == "negative" else hits[-1]
            v["from_ia_annex"] = {"ref": ref, "mentions": hits[:6]}
            v["first"], v["final"] = first, (final if len(hits) > 1 else first)
    json.dump(R, open(f"{OUT}/rsb.json", "w"), indent=1)
    import collections
    print("step 6:", sum(1 for v in R.values() if v.get("from_ia_annex")), "verdicts from the impact assessment annex;",
          collections.Counter((v.get("first"), v.get("final")) for v in R.values() if v.get("from_ia_annex")))

# ---------- step 7: one record per law (data/ia/ia_laws.json) for the site builders and the workbook
if step in ("all", "7"):
    S = json.load(open(f"{OUT}/ia_status.json")); R = json.load(open(f"{OUT}/rsb.json")); M = json.load(open(f"{OUT}/rsb_manual.json"))
    L = json.load(open(f"{OUT}/laws.json"))
    lab = lambda r: re.sub(r"(SWD|SEC)\((\d{4})\)(\d+)", r"\1(\2) \3", r)
    url = lambda r: f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:5{r[4:8]}SC{int(r[9:]):04d}"
    out = {}
    for law, s in S.items():
        rv = R.get(law, {}); man = M.get(law)
        ops = [{"ref": lab(o["ref"]), "url": o["url"], "verdicts": o.get("verdicts", [])} for o in rv.get("opinions", [])]
        if ops:
            rsb = {"first": rv.get("first"), "final": rv.get("final"), "source": "Board opinion", "opinions": ops}
        elif man:
            rsb = {"first": man["first"], "final": man["final"], "source": man["source"], "quote": man["quote"], "opinions": []}
        else:
            rsb = None
        out[law] = {"status": s["status"], "docs": [{"ref": lab(r), "url": url(r)} for r in s["main"]], "note": s["note"],
                    "proposal_year": int(L[law]["proposal_date"][:4]) if L[law].get("proposal_date") else None, "board": rsb}
    json.dump(out, open(f"{OUT}/ia_laws.json", "w"), indent=1, ensure_ascii=False)
    import collections
    print("step 7:", collections.Counter(v["status"] for v in out.values()), "board verdicts:", sum(1 for v in out.values() if v["board"]))
