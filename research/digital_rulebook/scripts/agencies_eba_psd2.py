"""Add PSD2 guidelines listed on the EBA legacy page but missing from the publications listing."""
import json, re, sys, html as H, urllib.parse
sys.path.insert(0, ".")
from common import fetch
from agencies_map import measure_doc
BASE = "https://www.eba.europa.eu"
PAGES = {
 "Guidelines on authorisation and registration under PSD2 (EBA/GL/2017/09)": "/activities/single-rulebook/regulatory-activities/payment-services-and-electronic-money/guidelines-authorisation-and-registration-under-psd2",
 "Guidelines on procedures for complaints of alleged infringements of the PSD2 (EBA/GL/2017/13)": "/activities/single-rulebook/regulatory-activities/payment-services-and-electronic-money/guidelines-procedures-complaints",
 "Guidelines on the criteria on how to stipulate the minimum monetary amount of the PII under PSD2 (EBA/GL/2017/08)": "/activities/single-rulebook/regulatory-activities/payment-services-and-electronic-money/guidelines-criteria-how-stipulat",
 "Guidelines on the conditions to benefit from an exemption from the contingency mechanism (EBA/GL/2018/07)": "/legacy/regulation-and-policy/regulatory-activities/payment-services-and-electronic-money/guidelines",
}
FALLBACK = {"EBA/GL/2017/09": "https://www.eba.europa.eu/documents/10180/1904583/f0e94433-f59b-4c24-9cec-2d6a2277b62c/Final%20Guidelines%20on%20Authorisations%20of%20Payment%20Institutions%20(EBA-GL-2017-09).pdf",
            "EBA/GL/2017/08": "https://www.eba.europa.eu/documents/10180/1901998/6411f24d-e430-4e05-ab03-1393a3f865cb/Final%20Guidelines%20on%20PII%20under%20PSD2%20(EBA-GL-2017-08).pdf",
            "EBA/GL/2018/07": "https://www.eba.europa.eu/sites/default/files/documents/10180/2250578/4e3b9449-ecf9-4756-8006-cbbe74db6d03/Final%20Report%20on%20Guidelines%20on%20the%20exemption%20to%20the%20fall%20back.pdf"}
items = json.load(open("../data/agency_eba.json"))
for title, path in PAGES.items():
    pdf = None
    try:
        h = fetch(BASE + path if path.startswith("/") else path)
        # find full page if the path was truncated in the listing
        pdfs = [x for x in re.findall(r'href="([^"]+\.pdf[^"]*)"', h) if re.search(r"final|guidelines|GL", x, re.I)
                and not re.search(r"_(BG|ES|CS|DA|DE|ET|EL|FR|GA|HR|IT|LV|LT|HU|MT|NL|PL|PT|RO|SK|SL|FI|SV)\b|consultation|CP", x)]
        pdf = (BASE + pdfs[0]) if pdfs and pdfs[0].startswith("/") else (pdfs[0] if pdfs else None)
    except Exception as e:
        pass
    code = re.search(r"EBA/GL/\d{4}/\d{2}", title).group(0)
    pdf = pdf or FALLBACK.get(code)
    if not pdf:
        print("no PDF for", title); continue
    try:
        text, m = measure_doc(pdf)
    except Exception as e:
        print("fail", title, e); continue
    items.append({"title": title, "pdf": pdf, "date_text": None, "agency": "EBA", "parent": "32015L2366",
                  "source": "EBA legacy PSD2 guidelines page", **(m or {})})
    print("added", title, m.get("pages"), m.get("restrictions_total"))
json.dump(items, open("../data/agency_eba.json", "w"), indent=1)
