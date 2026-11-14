"""One command from data to site: rebuilds the database (digital_rulebook.xlsx) and every page from it.
  python3 scripts/build_all.py            database, derived data, charts, pages, figures, dates, page heights
  python3 scripts/build_all.py --no-heights   skip the browser measurement of page heights
Stage 0 (not run here, run when its inputs change): text download and measurement (scripts/download.py, measure.py),
the obligation and addressee classifiers, the rules/standards coding, impact records (scripts/rec_*.py) and the analyses
in scripts/ (rs_*.py, company_types.py, evidence_map.py, policy_eras.py, firm_size.py). Their outputs in data/ are the
inputs of this build. Run from research/digital_rulebook."""
import subprocess, sys, time
STEPS = [
 ("pending initiatives and Forthcoming pages", ["python3", "build_forthcoming.py"], "site"),
 ("database: measured laws", ["python3", "build_workbook.py"], "scripts"),
 ("database: pending initiatives and reviews", ["python3", "scripts/db_pending.py"], "."),
 ("evidence library data", ["python3", "site/build_studies_data.py"], "."),
] + [(f"chart: {c}", ["python3", f"site/{c}.py"], ".") for c in (
 "build_mock_charts", "build_reporting_charts", "build_why_charts", "build_evidence_front", "build_evidence_front_options", "build_evidence_map",
 "build_rules_standards", "build_grid_charts", "build_rules_kinds", "build_ia_table", "build_us_pairs", "build_company_types", "build_company_types_kinds", "build_company_types_pie",
 "build_company_types_time", "build_company_types_speed", "build_company_types_cards", "build_company_types_cards_html", "build_firm_size", "build_firm_relief", "build_front_productivity",
 "build_infographic", "build_infographic_areas_growth", "build_infographic_gap", "build_infographic_hq", "build_infographics_more", "build_infographics_batch2", "build_policy_timeline",
 "build_gap_options", "hero_options", "build_studies_area", "build_causal_cluster", "build_evidence_blocks")] + [
 ("figures", ["python3", "site/facts.py"], "."),
 ("law pages", ["python3", "site/build_instrument_pages.py"], "."),
 ("digital policy page", ["python3", "site/build_digital_policy_page.py"], "."),
 ("further reading page", ["python3", "site/build_further_reading.py"], "."),
 ("fill charts, figures and lists into the pages", ["python3", "site/assemble.py", "--fill"], "."),
 ("last-update date", ["python3", "site/stamp_dates.py", "site/mockup"], "."),
]
if "--no-heights" not in sys.argv:
    STEPS.append(("page heights", ["python3", "site/measure_heights.py"], "."))
STEPS.append(("untracked figures report", ["python3", "site/assemble.py", "--check"], "."))
t0 = time.time()
for name, cmd, cwd in STEPS:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or [""])[-1][:110]
    print(f"{'ok ' if r.returncode == 0 else 'FAIL'} {name}: {last}")
    if r.returncode != 0:
        print(r.stderr[-2000:]); sys.exit(1)
print(f"done in {time.time() - t0:.0f}s")
