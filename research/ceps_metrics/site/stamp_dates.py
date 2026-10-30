"""Set every "Data as of <Month Year>" date in the mockup pages to the current month.
Run before each publish so the footer date follows the latest update.
Usage: python3 site/stamp_dates.py <folder with .dc.html files> [...]"""
import datetime, pathlib, re, sys

stamp = datetime.date.today().strftime("%B %Y")
pat = re.compile(r'(Data as of (?:<span data-updated="month">)?)[A-Z][a-z]+ \d{4}')
for folder in sys.argv[1:]:
    for f in sorted(pathlib.Path(folder).glob("*.dc.html")):
        s = f.read_text()
        t = pat.sub(lambda m: m.group(1) + stamp, s)
        if t != s:
            f.write_text(t)
            print(f.name, "->", stamp)
