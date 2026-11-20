"""Refresh site/forthcoming_oeil.json from the European Parliament's Legislative Observatory (OEIL) procedure files.

For every procedure listed in site/forthcoming_procs.py (PROC), fetch the procedure file and keep: title, stage reached,
committee responsible and rapporteur, key events (date, event, reference, link), the Commission documents (COM, SWD)
mentioned, the documentation gateway rows (type, reference, date, institution) and Council mentions. A procedure that
cannot be fetched keeps its previous record. Run from research/digital_rulebook: python3 scripts/oeil_fetch.py"""
import html, json, re, sys, urllib.request

sys.path.insert(0, "site")
from forthcoming_procs import PROC

OUT = "site/forthcoming_oeil.json"
URL = "https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference={}"
txt = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def section(t, start, end="</table>"):
    i = t.find(start)
    return t[i:t.find(end, i)] if i >= 0 else ""


def parse(ref, t):
    t = re.sub(r"\s+", " ", t)
    rec = {"ref": ref}
    m = re.search(r'<h2[^>]*class="[^"]*erpl_title-h2[^"]*"[^>]*>(.*?)</h2>', t) or re.search(r'<p class="es_title-h4[^"]*"[^>]*>(.*?)</p>', t)
    rec["title"] = txt(m.group(1)) if m else ""
    m = re.search(r"Stage reached in procedure</th>\s*<td[^>]*>(.*?)</td>", t)
    rec["stage"] = txt(m.group(1)) if m else ""
    cr = section(t, "Committee responsible</th>")
    body = cr[cr.find("<tbody>"):]
    first = re.search(r"<tr>(.*?)</tr>", body)
    if first and "Pending final decision" not in first.group(1):
        badge = re.search(r'es_badge-committee[^>]*>([A-Z]+)<', first.group(1))
        name = re.search(r'font-weight-normal">([^<]+)<', first.group(1))
        rap = re.search(r'class="rapporteur[^>]*>\s*<span>([^<]+)</span>', first.group(1))
        rec["committee"] = f"{badge.group(1)} ({txt(name.group(1))})" if badge and name else ""
        rec["rapporteur"] = txt(rap.group(1)) if rap else ""
    else:
        rec["committee"], rec["rapporteur"] = "", ""
    ev = section(t, "Key events</h2>")
    rec["events"] = []
    for row in re.findall(r"<tr>(.*?)</tr>", ev[ev.find("<tbody>"):]):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row)
        if len(tds) >= 3:
            a = re.search(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', tds[2])
            rec["events"].append([txt(tds[0]), txt(tds[1]), a.group(2).strip() if a else "", html.unescape(a.group(1)) if a else ""])
    fc = section(t, "Forecasts</h2>")
    for row in re.findall(r"<tr>(.*?)</tr>", fc[fc.find("<tbody>"):]):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row)
        if len(tds) == 2:
            rec["events"].append([txt(tds[0]), txt(tds[1]), "", ""])
    rec["swd"] = sorted(set(re.findall(r"SWD\(\d{4}\)\d{4}", t)))
    rec["com"] = re.findall(r"COM\(\d{4}\)\d{4}", t)
    gw = t[t.find('id="erplAccordionDocGateway"'):]
    rec["gateway"] = []
    for inst, block in re.findall(r'<span class="t-x">([^<]+)</span>.*?<tbody>(.*?)</tbody>', gw[:gw.find('class="es_product-section"') if 'class="es_product-section"' in gw else None]):
        for row in re.findall(r"<tr>(.*?)</tr>", block):
            typ = re.search(r'font-weight-normal">([^<]+)<', row)
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row)
            refm = re.search(r">([^<>]+)</a>", row) or re.search(r"<span>([^<>]+)</span>", row)
            date = next((txt(c) for c in cells if re.fullmatch(r"\d{2}/\d{2}/\d{4}", txt(c))), "")
            if typ:
                rec["gateway"].append([txt(typ.group(1)), refm.group(1).strip() if refm else "", date, txt(inst)])
    rec["council"] = re.findall(r"Council of the European Union", t)
    rec["swd_links"] = {s: "" for s in rec["swd"]}
    return rec


old = json.load(open(OUT))
refs = sorted({r for rs in PROC.values() for r in rs} | set(old))
out, failed = {}, []
for ref in refs:
    try:
        with urllib.request.urlopen(urllib.request.Request(URL.format(ref), headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as r:
            rec = parse(ref, r.read().decode("utf8", "ignore"))
        if not rec["events"]:
            raise ValueError("no key events parsed")
        rec["title"] = rec["title"] or old.get(ref, {}).get("title", "")
        out[ref] = rec
    except Exception as e:
        failed.append((ref, str(e)[:80])); out[ref] = old.get(ref, {"ref": ref})
json.dump(out, open(OUT, "w"), ensure_ascii=False)
for ref in refs:
    o, n = old.get(ref, {}), out[ref]
    if len(n.get("events", [])) != len(o.get("events", [])) or n.get("stage") != o.get("stage") or len(n.get("gateway", [])) != len(o.get("gateway", [])):
        print(ref, "|", o.get("stage"), "->", n.get("stage"), "| events", len(o.get("events", [])), "->", len(n.get("events", [])),
              "| gateway", len(o.get("gateway", [])), "->", len(n.get("gateway", [])), "|", (n.get("events") or [[""] * 2])[-1][:2])
print("failed:", failed)
