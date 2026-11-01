"""Set every footer date ("Last update: <d Month YYYY>", formerly "Data as of <Month Year>") in the mockup pages to today.
Run before each publish so the footer date follows the latest update.
Usage: python3 site/stamp_dates.py <folder with .dc.html files> [...]"""
import datetime, pathlib, re, sys

d = datetime.date.today()
stamp = f"Last update: {d.day} {d:%B %Y}"
pat = re.compile(r'Data as of (?:<span data-updated="month">)?[A-Z][a-z]+ \d{4}(?:</span>)?|Last update: \d{1,2} [A-Z][a-z]+ \d{4}')
for folder in sys.argv[1:]:
    for f in sorted(pathlib.Path(folder).glob("*.dc.html")):
        s = f.read_text()
        t = pat.sub(stamp, s)
        if t != s:
            f.write_text(t)
            print(f.name, "->", stamp)
