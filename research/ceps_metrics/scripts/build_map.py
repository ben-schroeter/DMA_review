"""Write data/instrument_map.csv: one line per CSV row -> CELEX(es) of the text measured."""
import csv, sys, re
sys.path.insert(0, ".")
from common import celex_from_identifier

PENDING = {  # procedure -> (CELEX measured, status Oct 2026, note)
    "2022/0084(COD)": ("52022PC0119", "proposed", ""),
    "2022/0155(COD)": ("52022PC0209", "proposed", ""),
    "2022/0407(CNS)": ("32025L0516", "adopted", "Adopted after CEPS snapshot: Council Directive (EU) 2025/516 (11 Mar 2025)"),
    "2023/0129(COD)": ("32025R2645", "adopted", "Adopted after CEPS snapshot: Regulation (EU) 2025/2645 (16 Dec 2025)"),
    "2023/0205(COD)": ("52023PC0360", "proposed", ""),
    "2023/0210(COD)": ("52023PC0367", "agreed", "Provisional agreement 27 Nov 2025; measured on the 2023 Commission proposal (user choice). Council final compromise text ST 8221/26: 431 Council-format pages, 74,497 words of legal text, 588 restrictions (323 on private parties)"),
    "2023/0209(COD)": ("52023PC0366", "agreed", "Provisional agreement 27 Nov 2025; measured on the 2023 Commission proposal (user choice). Council final compromise text ST 8222/26: 167 Council-format pages, 30,433 words of legal text, 266 restrictions (56 on private parties)"),
    "2023/0212(COD)": ("52023PC0369", "proposed", ""),
    "2023/0202(COD)": ("32025R2518", "adopted", "Adopted after CEPS snapshot: Regulation (EU) 2025/2518 (26 Nov 2025)"),
    "2023/0290(COD)": ("32025R2509", "adopted", "Adopted after CEPS snapshot: Regulation (EU) 2025/2509 (26 Nov 2025)"),
    "2023/0323(COD)": ("52023PC0533", "proposed", ""),
    "2024/0035(COD)": ("52024PC0060", "proposed", ""),
    "2024/0670(COD)": ("52024PC0670", "proposed", ""),
    "COM(2025) 335": ("52025PC0335", "proposed", ""),
}
rows = list(csv.DictReader(open("../data/ceps_instruments.csv")))
out = csv.writer(open("../data/instrument_map.csv", "w", newline=""), lineterminator="\n")
out.writerow(["row_id", "name", "identifier", "celex_measured", "status_ceps_jul2025", "status_oct2026", "note"])
for i, r in enumerate(rows, 1):
    if r["status"] == "adopted":
        cel, st, note = ";".join(celex_from_identifier(r["identifier"])), "adopted", ""
    else:
        cel, st, note = PENDING[r["identifier"]]
    out.writerow([i, r["name"], r["identifier"], cel, r["status"], st, note])
print(len(rows))
