"""Chart 12: euro-area-4 labour productivity per hour relative to the US, 1995 = 100 (after Schnabel, ECB, 16 Feb 2024)."""
import json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
GREY, UP, DOWN = "#8f8d86", "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5})
d = json.load(open("../data/external/ea4_us_productivity.json"))
Y = {o["year"]: o["ratio_1995_100"] for o in d}
fig, ax = plt.subplots(figsize=(11, 6.6), dpi=160)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ax.axvspan(1945, 1995, color=UP, alpha=0.06, lw=0)
ax.axvspan(1995, 2022.6, color=DOWN, alpha=0.08, lw=0)
for (a, b), c in (((1900, 1945), GREY), ((1945, 1995), UP), ((1995, 2022), DOWN)):
    xs = [y for y in sorted(Y) if a <= y <= b]
    ax.plot(xs, [Y[y] for y in xs], color=c, lw=3, solid_capstyle="round", solid_joinstyle="round", zorder=3)
ax.axhline(100, color=INK, lw=1, zorder=2)
ax.fill_between([y for y in sorted(Y) if y >= 1995], [Y[y] for y in sorted(Y) if y >= 1995], 100, color=DOWN, alpha=0.25, lw=0)
t = min((y for y in Y if 1940 <= y <= 1950), key=lambda y: Y[y])
for x, c in ((t, GREY), (1995, UP), (2022, DOWN)):
    ax.scatter([x], [Y[x]], s=70, color=c, edgecolor=SURF, linewidth=2, zorder=4)
ax.text(1900.5, 102, "1995 level = 100", fontsize=10.5, color=INK, weight="bold", va="bottom")
ax.annotate(f"{Y[t]:.0f}", (t, Y[t]), xytext=(8, -4), textcoords="offset points", fontsize=11, color=GREY, weight="bold")
ax.annotate(f"{Y[2022] - 100:+.0f}%", (2015, (Y[2022] + 100) / 2 + 3), fontsize=17, color=DOWN, weight="bold", ha="center")
ax.annotate(f"{Y[2022]:.0f}", (2022, Y[2022]), xytext=(9, -4), textcoords="offset points", fontsize=11, color=DOWN, weight="bold")
ax.text(1903, 36, "1914–45\nTwo world wars", fontsize=11, color=GREY, linespacing=1.3)
ax.text(1960, 14, "1945–95\nEurope catches up: engines,\nelectricity, chemistry", fontsize=11, color=UP, weight="bold", linespacing=1.3)
ax.text(1997, 52, "Since 1995\nEurope falls behind\nin the ICT era", fontsize=11, color=DOWN, weight="bold", linespacing=1.3)
ax.set_xlim(1900, 2026); ax.set_ylim(0, 118)
ax.set_xticks([1900, 1920, 1945, 1970, 1995, 2022])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(BASE); ax.tick_params(colors=MUTED, length=0, labelsize=10.5)
fig.suptitle("Europe missed the technology revolution", x=0.01, ha="left", fontsize=16, color=INK, weight="bold", y=0.975)
fig.text(0.01, 0.905, "Labour productivity per hour worked, Germany, France, Italy and Spain relative to the United States (ratio in 1995 = 100)",
         fontsize=10.5, color=INK2)
fig.text(0.01, 0.015, "Source: Bergeaud, Cette & Lecat, Long-Term Productivity Database v2.7 (Banque de France); own calculation, EA-4 weighted by approximate GDP. "
         "After I. Schnabel, ECB, 16 Feb 2024.\nShown relative to 1995 because levels depend on data vintage and weights: this vintage puts EA-4 above the US in 1995, "
         "the ECB's chart shows parity. The fall since 1995 is about 20% in both.", fontsize=8, color=MUTED)
fig.subplots_adjust(left=0.05, right=0.97, top=0.86, bottom=0.12)
fig.savefig("../charts/12_productivity_gap.png", facecolor=SURF); plt.close(fig); print("wrote 12_productivity_gap.png")
