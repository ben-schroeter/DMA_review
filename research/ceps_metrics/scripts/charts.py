"""Charts on the development of restrictions over time, from ceps_instruments_metrics.xlsx."""
import datetime as dt, collections, statistics
import openpyxl
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.dates as md

WB = openpyxl.load_workbook("../ceps_instruments_metrics.xlsx", data_only=True)
OUT = "../charts/"
SURF, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
NEUTRAL = "#b5b3ac"
SRC = "Source: CEPS Table 1 (July 2025) instruments; texts from EUR-Lex; restriction counts by automated count (84% precision on a hand-checked sample)."
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5})


def sheet(name):
    ws = WB[name]; h = [c.value for c in ws[1]]
    return [dict(zip(h, r)) for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None]


inst = [r for r in sheet("instruments") if r["adoption_date"] and r["restrictions_total"] is not None]
for r in inst:
    r["date"] = dt.date.fromisoformat(str(r["adoption_date"])[:10])
    c = r["celex_measured"].split(";")[0]
    r["type"] = {"R": "Regulation", "L": "Directive", "D": "Decision"}[c[5]]
inst.sort(key=lambda r: r["date"])
sec = [r for r in sheet("secondary_acts") if r["kind"] in ("implementing", "delegated") and r["date"] and r["restrictions_total"] is not None]
for r in sec:
    r["d"] = dt.date.fromisoformat(str(r["date"])[:10])
sec.sort(key=lambda r: r["d"])
START, END = dt.date(1986, 1, 1), dt.date(2026, 10, 1)


def frame(title, subtitle, figsize=(11, 6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=160)
    fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    ax.set_title(title, loc="left", fontsize=14, color=INK, weight="bold", pad=26)
    ax.text(0, 1.035, subtitle, transform=ax.transAxes, fontsize=10, color=INK2)
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE); ax.tick_params(colors=MUTED, length=0)
    return fig, ax


def finish(fig, name, note=SRC):
    fig.text(0.01, 0.01, note, fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(OUT + name, facecolor=SURF); plt.close(fig)
    print("wrote", name)


def mandates(ax, ytop):
    for d, lab in ((dt.date(2014, 11, 1), "Juncker"), (dt.date(2019, 12, 1), "VdL I"), (dt.date(2024, 12, 1), "VdL II")):
        ax.axvline(d, color=BASE, lw=0.8, ls=(0, (3, 3)), zorder=0)
        ax.text(d + dt.timedelta(days=60), ytop, lab, fontsize=8.5, color=MUTED, ha="left", va="top", clip_on=False)


def cumulative_stack(rows, datef, series, key_of, title, subtitle, name, colors, labels=None):
    X = [START] + [datef(r) for r in rows] + [END]
    cum = {s: 0 for s in series}; Y = {s: [0] for s in series}
    for r in rows:
        for s in series:
            cum[s] += key_of(r, s)
            Y[s].append(cum[s])
    for s in series:
        Y[s].append(cum[s])
    fig, ax = frame(title, subtitle)
    ax.stackplot(X, [Y[s] for s in series], colors=colors, step="post", edgecolor=SURF, linewidth=1.2,
                 labels=[(labels or {}).get(s, s) for s in series])
    tot = sum(cum.values())
    ax.set_xlim(START, END); ax.set_ylim(0, tot * 1.12)
    mandates(ax, tot * 1.11)
    base, mids = 0, []
    for s in series:
        v = cum[s]; mids.append(base + v / 2); base += v
    gap = tot * 0.045                         # keep labels at least this far apart, working down from the top
    ys = mids[:]
    top_limit = tot * 1.0 - gap * 0.6
    for k in range(len(ys) - 1, -1, -1):
        hi = top_limit if k == len(ys) - 1 else ys[k + 1] - gap
        ys[k] = min(ys[k], hi)
    for s, y in zip(series, ys):
        ax.annotate(f"{(labels or {}).get(s, s)}  {cum[s]:,}", xy=(END, y), xytext=(8, 0), textcoords="offset points",
                    va="center", fontsize=9.5, color=INK2, annotation_clip=False)
    ax.annotate(f"Total {tot:,}", xy=(END, tot), xytext=(8, 12), textcoords="offset points", fontsize=10.5,
                color=INK, weight="bold", annotation_clip=False)
    ax.xaxis.set_major_locator(md.YearLocator(4)); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f"{v:,.0f}"))
    ax.legend(loc="upper left", frameon=False, labelcolor=INK2, fontsize=9.5)
    fig.subplots_adjust(right=0.8)
    finish(fig, name)


# 1. by addressee
ADDR = ["addr_private_parties", "addr_member_states", "addr_eu_institutions", "addr_unclear"]
LAB = {"addr_private_parties": "Private parties", "addr_member_states": "Member States", "addr_eu_institutions": "EU institutions",
       "addr_unclear": "Unclear / none"}
cumulative_stack(inst, lambda r: r["date"], ADDR, lambda r, s: r[s] or 0,
                 "Restrictions in EU digital law, cumulative by adoption date",
                 "Restrictions in the original adopted texts of 105 instruments, by who they bind", "01_cumulative_by_addressee.png",
                 CAT[:3] + [NEUTRAL], LAB)

# 2. by type of legislation
TYPES = ["Regulation", "Directive", "Decision"]
cumulative_stack(inst, lambda r: r["date"], TYPES, lambda r, s: (r["restrictions_total"] or 0) if r["type"] == s else 0,
                 "Restrictions by type of legal act, cumulative by adoption date",
                 "Regulations bind directly; Directive obligations mostly bind Member States, which then transpose them",
                 "02_cumulative_by_act_type.png", CAT[:3], {t: t + "s" for t in TYPES})

# 3. by restriction category
RC = ["r_obligation", "r_duty_of_result", "r_prohibition", "r_restricted_permission", "r_explicit_requirement"]
RL = {"r_obligation": "Obligation (shall/must)", "r_duty_of_result": "Duty of result (shall ensure)", "r_prohibition": "Prohibition",
      "r_restricted_permission": "Restricted permission (may only)", "r_explicit_requirement": "Explicit requirement"}
cumulative_stack(inst, lambda r: r["date"], RC, lambda r, s: r[s] or 0,
                 "Restrictions by kind, cumulative by adoption date", "Same 105 adopted instruments, split by the type of marker counted",
                 "03_cumulative_by_kind.png", CAT[:5], RL)

# 4. main acts vs implementing/delegated acts
rows4 = [{"d": r["date"], "main": r["restrictions_total"] or 0, "secondary": 0} for r in inst] + \
        [{"d": r["d"], "main": 0, "secondary": r["restrictions_total"] or 0} for r in sec]
rows4.sort(key=lambda r: r["d"])
cumulative_stack(rows4, lambda r: r["d"], ["main", "secondary"], lambda r, s: r[s],
                 "Restrictions in the acts themselves vs their implementing and delegated acts",
                 f"Cumulative by date of adoption; {len(sec)} implementing/delegated acts linked in EUR-Lex",
                 "04_main_vs_implementing.png", CAT[:2], {"main": "Main acts", "secondary": "Implementing & delegated acts"})

# 5. per-act restrictions and intensity over time (scatter + 5-year medians)
fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), dpi=160)
fig.patch.set_facecolor(SURF)
for ax, key, title, f in ((axes[0], "restrictions_total", "Restrictions per act", lambda r: r["restrictions_total"]),
                          (axes[1], "density", "Restrictions per 1,000 words of articles and annexes",
                           lambda r: 1000 * r["restrictions_total"] / max(1, (r["words_articles"] or 0) + (r["words_annexes"] or 0)))):
    ax.set_facecolor(SURF)
    for t, c in zip(TYPES, CAT):
        pts = [r for r in inst if r["type"] == t]
        ax.scatter([r["date"] for r in pts], [f(r) for r in pts], s=34, color=c, edgecolor=SURF, linewidth=1.5, label=t + "s", zorder=3)
    bins = collections.defaultdict(list)
    for r in inst:
        bins[(r["date"].year // 5) * 5].append(r)
    xs = sorted(b for b in bins if len(bins[b]) >= 3)
    mid = lambda rs: dt.date.fromordinal(int(statistics.median(x["date"].toordinal() for x in rs)))
    ax.plot([mid(bins[b]) for b in xs], [statistics.mean(f(x) for x in bins[b]) for b in xs], color=INK, lw=2, label="5-year average", zorder=4)
    ax.set_title(title, loc="left", fontsize=12, color=INK, weight="bold")
    ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE); ax.tick_params(colors=MUTED, length=0)
    ax.xaxis.set_major_locator(md.YearLocator(8)); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
import json as _json
try:
    _sox = _json.load(open("../data/benchmark_sox.json"))
    for ax, val in ((axes[0], _sox["all_text"]["restrictions_total"]), (axes[1], _sox["all_text"]["per_1000_words"])):
        ax.axhline(val, color=CAT[6], lw=1.4, ls=(0, (5, 3)), zorder=2)
        ax.text(START + dt.timedelta(days=200), val, f"Sarbanes-Oxley Act (US, 2002): {val:g}", color=CAT[6], fontsize=8.5,
                va="bottom", ha="left")
except FileNotFoundError:
    pass
axes[0].legend(loc="upper left", frameon=False, labelcolor=INK2, fontsize=9)
top = sorted(inst, key=lambda r: -r["restrictions_total"])[:5]
for r in top:
    axes[0].annotate(r["name"].split(" (")[0], xy=(r["date"], r["restrictions_total"]), xytext=(-6, 4), textcoords="offset points",
                     ha="right", fontsize=8, color=INK2)
fig.suptitle("New acts carry more restrictions, but not denser ones", x=0.01, ha="left", fontsize=14, color=INK, weight="bold")
finish(fig, "05_per_act_and_density.png")

# 6. small multiples by policy area (cumulative)
areas = sorted({r["policy_area_ceps"] for r in inst}, key=lambda a: -sum(r["restrictions_total"] for r in inst if r["policy_area_ceps"] == a))
fig, axes = plt.subplots(3, 4, figsize=(14, 8.5), dpi=160, sharex=True, sharey=True)
fig.patch.set_facecolor(SURF)
for ax, a in zip(axes.flat, areas):
    rs = [r for r in inst if r["policy_area_ceps"] == a]
    X = [START] + [r["date"] for r in rs] + [END]
    yp, yo = [0], [0]; p = o = 0
    for r in rs:
        p += r["addr_private_parties"] or 0; o += (r["restrictions_total"] or 0) - (r["addr_private_parties"] or 0)
        yp.append(p); yo.append(o)
    yp.append(p); yo.append(o)
    ax.set_facecolor(SURF)
    ax.stackplot(X, [yp, yo], colors=[CAT[0], NEUTRAL], step="post", edgecolor=SURF, linewidth=0.8)
    ax.set_title(f"{a}  ({p + o:,})", loc="left", fontsize=9.5, color=INK, weight="bold")
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASE); ax.tick_params(colors=MUTED, length=0, labelsize=8)
    ax.xaxis.set_major_locator(md.YearLocator(10)); ax.xaxis.set_major_formatter(md.DateFormatter("%Y"))
fig.suptitle("Cumulative restrictions by CEPS policy area", x=0.01, ha="left", fontsize=14, color=INK, weight="bold")
fig.text(0.01, 0.945, "Blue: restrictions binding private parties; grey: all other addressees. Panels share axes; ordered by total.",
         fontsize=10, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 0.93)); fig.text(0.01, 0.01, SRC, fontsize=8, color=MUTED)
fig.savefig(OUT + "06_by_policy_area.png", facecolor=SURF); plt.close(fig); print("wrote 06_by_policy_area.png")

# 7. addressee shares by period (100% stacked bars)
periods = [(1985, 1999, "1985–99"), (2000, 2009, "2000–09"), (2010, 2014, "2010–14"), (2015, 2019, "2015–19"), (2020, 2024, "2020–24"), (2025, 2026, "2025–26")]
fig, ax = frame("Who new restrictions bind, by period of adoption", "Share of restrictions in acts adopted in each period")
left = [0] * len(periods)
shares = []
for p0, p1, lab in periods:
    rs = [r for r in inst if p0 <= r["date"].year <= p1]
    tot = sum(r["restrictions_total"] for r in rs) or 1
    shares.append([sum(r[a] or 0 for r in rs) / tot for a in ADDR] + [len(rs)])
y = list(range(len(periods)))[::-1]
for k, (a, c) in enumerate(zip(ADDR, CAT[:3] + [NEUTRAL])):
    vals = [s[k] for s in shares]
    ax.barh(y, vals, left=left, color=c, edgecolor=SURF, linewidth=2, height=0.62, label=LAB[a])
    for yi, v, l in zip(y, vals, left):
        if v >= 0.07:
            ax.text(l + v / 2, yi, f"{v:.0%}", ha="center", va="center", fontsize=9, color=INK if c in (CAT[2], NEUTRAL, CAT[3]) else "white")
    left = [l + v for l, v in zip(left, vals)]
ax.set_yticks(y); ax.set_yticklabels([f"{p[2]}  (n={s[-1]})" for p, s in zip(periods, shares)], color=INK2)
ax.set_xlim(0, 1); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0)); ax.xaxis.grid(True, color=GRID); ax.yaxis.grid(False)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol=4, frameon=False, labelcolor=INK2)
finish(fig, "07_addressee_share_by_period.png")

# 8. proposal vs adopted
cmp = [r for r in inst if isinstance(r.get("proposal_restrictions_total"), (int, float))]
fig, ax = frame("Restrictions grow between proposal and adoption",
                f"{len(cmp)} acts: original Commission proposal (x) vs adopted text (y); above the line = more restrictions after negotiation",
                figsize=(9, 7.5))
mx = max(max(r["proposal_restrictions_total"], r["restrictions_total"]) for r in cmp) * 1.05
ax.plot([0, mx], [0, mx], color=BASE, lw=1, ls=(0, (4, 3)), zorder=1)
for t, c in zip(TYPES, CAT):
    pts = [r for r in cmp if r["type"] == t]
    ax.scatter([r["proposal_restrictions_total"] for r in pts], [r["restrictions_total"] for r in pts], s=38, color=c,
               edgecolor=SURF, linewidth=1.5, label=t + "s", zorder=3)
lab = sorted(sorted(cmp, key=lambda r: -abs(r["restrictions_total"] - r["proposal_restrictions_total"]))[:7], key=lambda r: -r["restrictions_total"])
prev = None
for r in lab:
    dy = 3
    if prev is not None and abs(prev - r["restrictions_total"]) < 35:
        dy = -12
    prev = r["restrictions_total"]
    name = r["name"].split(" (")[0]
    if "Open Internet" in name:
        name += " (2013 proposal was the wider 'Connected Continent' package)"
    ax.annotate(name, xy=(r["proposal_restrictions_total"], r["restrictions_total"]), xytext=(5, dy),
                textcoords="offset points", fontsize=8, color=INK2)
ax.set_xlim(0, mx); ax.set_ylim(0, mx); ax.set_xlabel("Restrictions in proposal", color=INK2); ax.set_ylabel("Restrictions in adopted act", color=INK2)
ax.xaxis.grid(True, color=GRID, lw=0.8)
up = sum(r["restrictions_total"] > r["proposal_restrictions_total"] for r in cmp)
ax.legend(loc="upper left", frameon=False, labelcolor=INK2, title=f"{up} of {len(cmp)} acts gained restrictions", title_fontsize=9.5)
finish(fig, "08_proposal_vs_adopted.png")

# 9. External benchmark: Sarbanes-Oxley vs EU acts
import json as _json, random as _random
sox = _json.load(open("../data/benchmark_sox.json"))["all_text"]
SOXC = CAT[6]
fig = plt.figure(figsize=(11.5, 6.2), dpi=160); fig.patch.set_facecolor(SURF)
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1], wspace=0.35)
ax1, ax2 = (fig.add_subplot(gs[0, i]) for i in range(2))
for ax in (ax1, ax2):
    ax.set_facecolor(SURF)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color(BASE); ax.tick_params(colors=MUTED, length=0)

# panel 1: restrictions per act
recent = [r for r in inst if r["date"].year >= 2020]
pick = ["Artificial Intelligence Act", "Digital Services Act", "General Data Protection Regulation", "Digital Markets Act", "Data Act"]
bars = [(n, next(r["restrictions_total"] for r in inst if r["name"] == n), CAT[0]) for n in pick]
bars += [("EU average, acts since 2020", round(statistics.mean(r["restrictions_total"] for r in recent)), NEUTRAL),
         ("EU average, all 105 acts", round(statistics.mean(r["restrictions_total"] for r in inst)), NEUTRAL),
         ("Sarbanes-Oxley Act (US, 2002)", sox["restrictions_total"], SOXC)]
bars.sort(key=lambda b: b[1])
y = range(len(bars))
ax1.barh(list(y), [b[1] for b in bars], color=[b[2] for b in bars], height=0.62, edgecolor=SURF, linewidth=2)
for yi, (n, v, c) in zip(y, bars):
    ax1.text(v + 12, yi, f"{v:,}", va="center", fontsize=9.5, color=INK, weight="bold" if c == SOXC else "normal")
ax1.set_yticks(list(y)); ax1.set_yticklabels([b[0].replace("General Data Protection Regulation", "GDPR").replace("Artificial Intelligence Act", "AI Act") for b in bars], color=INK2, fontsize=9.5)
for lab in ax1.get_yticklabels():
    if "Sarbanes" in lab.get_text():
        lab.set_color(SOXC); lab.set_weight("bold")
ax1.xaxis.grid(True, color=GRID, lw=0.8); ax1.set_axisbelow(True)
ax1.set_xlim(0, max(b[1] for b in bars) * 1.15)
ax1.set_title("Restrictions per act", loc="left", fontsize=12, color=INK, weight="bold")

# panel 2: density strip
dens = [1000 * r["restrictions_total"] / max(1, (r["words_articles"] or 0) + (r["words_annexes"] or 0)) for r in inst]
_random.seed(3)
xs = [0.75 + _random.uniform(-0.18, 0.18) for _ in dens]
ax2.scatter(xs, dens, s=22, color=CAT[0], alpha=0.55, edgecolor=SURF, linewidth=0.8, zorder=3)
med = statistics.median(dens)
ax2.plot([0.5, 1.0], [med, med], color=INK, lw=2, zorder=4)
ax2.text(1.03, med, f"EU median {med:.1f}", va="center", fontsize=9.5, color=INK)
ax2.scatter([1.6], [sox["per_1000_words"]], s=110, color=SOXC, edgecolor=SURF, linewidth=1.5, zorder=4)
ax2.text(1.6, sox["per_1000_words"] - 1.4, f"SOX {sox['per_1000_words']:g}", ha="center", va="top", fontsize=9.5, color=SOXC, weight="bold")
ax2.set_xlim(0.35, 2.0); ax2.set_xticks([0.75, 1.6]); ax2.set_xticklabels(["105 EU acts", "Sarbanes-Oxley"], color=INK2)
ax2.set_ylim(0, max(dens) * 1.08)
ax2.yaxis.grid(True, color=GRID, lw=0.8); ax2.set_axisbelow(True)
ax2.set_title("Restrictions per 1,000 words", loc="left", fontsize=12, color=INK, weight="bold")

fig.suptitle("EU digital acts vs the Sarbanes-Oxley Act", x=0.01, ha="left", fontsize=15, color=INK, weight="bold", y=0.99)
fig.text(0.01, 0.915, "Recent EU acts carry more restrictions than SOX and pack them more densely",
         fontsize=10, color=INK2)
fig.text(0.01, 0.01, "Same automated counter for both; precision 84% on EU acts, 68% on SOX (so SOX is, if anything, overstated). "
         "SOX words = enacted text; EU words = articles + annexes (recitals excluded).", fontsize=8, color=MUTED)
fig.subplots_adjust(left=0.22, right=0.95, top=0.82, bottom=0.14)
fig.savefig(OUT + "09_benchmark_sox.png", facecolor=SURF); plt.close(fig); print("wrote 09_benchmark_sox.png")
