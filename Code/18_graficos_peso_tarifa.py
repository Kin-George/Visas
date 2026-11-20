"""Visa-R / 18: graficos del peso de la tarifa sobre el ingreso (pr4_peso_tarifa.png) e ingreso mediano por educacion con la tarifa como referencia (pr5_ingreso_educacion.png).
Entradas: t20, t20b (script 17), t18 (script 13)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, GRAY, LGRAY, ACC, INK = "#1f3b5c", "#8c8c8c", "#d9d9d9", "#a4472f", "#222222"
W = 5.9
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 9, "text.color": INK,
    "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.labelcolor": INK, "axes.labelsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "xtick.color": INK, "ytick.color": INK, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "xtick.major.size": 2.5, "ytick.major.size": 0,
    "xtick.major.width": 0.6, "legend.frameon": False, "legend.fontsize": 8.5, "figure.dpi": 100})
pc = lambda x, d=0: f"{x:.{d}f}".replace(".", ",")
save = lambda fig, n: (fig.savefig(FIG / n, dpi=250, facecolor="white"), plt.close(fig))
TRM, SMMLV_2026, FEE_COP = 3235.0, 1_750_905, 464 * 3235.0

t20 = pd.read_csv(TAB / "t20_peso_tarifa_persona.csv").set_index("educacion")
t20b = pd.read_csv(TAB / "t20b_peso_tarifa_hogar.csv").set_index("grupo")

# =============================================================== pr4: cuanto se come la Visa R de un mes de trabajo
fig = plt.figure(figsize=(W, 4.3))
gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1], hspace=0.5, left=0.27, right=0.985, top=0.9, bottom=0.1)
a = fig.add_subplot(gs[0])
opts = [("Tarifa vigente: USD 464", "pct_ingreso_USD 464 (vigente)", ACC), ("Mitad: USD 232", "pct_ingreso_USD 232", NAVY),
        ("Solo el estudio: USD 56", "pct_ingreso_USD 56 (estudio)", NAVY), ("Gratuidad: USD 0", "pct_ingreso_USD 0", NAVY)]
for k, (nom, col, c_) in enumerate(opts):
    y = len(opts) - 1 - k; pct_ = float(t20.loc["Todos", col]); dias = int(round(30 * pct_ / 100))
    for d_ in range(30):
        a.add_patch(Rectangle((d_ + 0.07, y - 0.36), 0.86, 0.72, facecolor=c_ if d_ < dias else "#e9e9e9", edgecolor="none"))
    a.text(-0.8, y + 0.06, nom, ha="right", va="center", fontsize=8.8, color=INK, fontweight="bold" if k == 0 else "normal")
    a.text(30.8, y, f"{dias} días" if dias != 1 else "1 día", ha="left", va="center", fontsize=9, color=c_, fontweight="bold")
a.set_xlim(0, 34.5); a.set_ylim(-0.6, len(opts) - 0.35); a.axis("off")
a.text(0, len(opts) - 0.3, "Cada cuadro es un día del mes de trabajo; ingreso mediano: COP " + pc(t20.loc["Todos", "ingreso_mediano_COP_millones"], 2) + " M", fontsize=7.8, ha="left", va="bottom", color="#555555", style="italic")
a.set_title("a) Días de trabajo de un mes que cuesta la tarifa (persona mediana)", loc="left", fontsize=9, style="italic", x=-0.27, pad=22)
b = fig.add_subplot(gs[1])
hog = [("Hogar con venezolanos@@(mediana)", "Todos los hogares con venezolanos"), ("Hogar con menores@@de 18 años", "Con al menos un menor de 18"), ("Hogar con 3 o más@@venezolanos", "Con 3 o más venezolanos")]
vals = [float(t20b.loc[g_, "mediana_pct_ingreso_mensual_del_hogar"]) for _, g_ in hog]
for k, ((nom, _), v) in enumerate(zip(hog, vals)):
    y = (len(hog) - 1 - k) * 1.0
    b.barh(y + 0.19, 100, 0.34, color="#cfcfcf"); b.barh(y - 0.19, v, 0.34, color=ACC)
    b.text(102, y + 0.19, "Ingreso del hogar en un mes: 100", va="center", fontsize=8, color="#555555")
    b.text(v + 2, y - 0.19, f"Tarifa: {v:.0f}", va="center", fontsize=9, color=ACC, fontweight="bold")
b.set_yticks([(len(hog) - 1 - k) * 1.0 for k in range(len(hog))]); b.set_yticklabels([n.replace("@@", chr(10)) for n, _ in hog], fontsize=8.5)
b.set_xlim(0, 300); b.set_ylim(-0.6, len(hog) - 0.4); b.set_xticks([]); b.spines["bottom"].set_visible(False); b.spines["left"].set_visible(False)
b.set_title("b) Por cada 100 pesos que gana el hogar en un mes, la tarifa de USD 464 por venezolano cuesta:", loc="left", fontsize=9, style="italic", x=-0.27, pad=10)
save(fig, "pr4_peso_tarifa.png")

# =============================================================== pr5: ingreso mediano por educacion, con la tarifa como referencia
t18 = pd.read_csv(TAB / "t18_ingreso_mediano_por_educacion.csv")
cats = ["Todos", "Hasta primaria", "Secundaria", "Media", "Técnica o tecnológica", "Universitaria o más"]
labs = ["Todos los\nocupados", "Hasta\nprimaria", "Secundaria", "Media", "Técnica o\ntecnológica", "Universitaria\no más"]
m = lambda g: [float(t18[(t18.grupo == g) & (t18.educacion == c_)].mediana_ingreso_smmlv.iloc[0]) * SMMLV_2026 / 1e6 for c_ in cats]
col_, ven_, afi_, noa_ = m("Colombianos"), m("Venezolanos"), m("Venezolanos afiliados a salud"), m("Venezolanos no afiliados")
fig, (p, q) = plt.subplots(2, 1, figsize=(W, 3.9), sharex=True); fig.subplots_adjust(left=0.1, right=0.99, top=0.95, bottom=0.14, hspace=0.38)
x = np.arange(len(cats)); w_ = 0.34
p.bar(x - w_ / 2, col_, w_, color=LGRAY, edgecolor="#9a9a9a", linewidth=0.5, label="Colombianos"); p.bar(x + w_ / 2, ven_, w_, color=NAVY, label="Venezolanos")
q.bar(x - w_ / 2, afi_, w_, color=NAVY, label="Venezolanos afiliados a salud"); q.bar(x + w_ / 2, noa_, w_, color="#7f9fc4", label="Venezolanos no afiliados")
for ax, (u, v_) in ((p, (col_, ven_)), (q, (afi_, noa_))):
    for xi, uu, vv in zip(x, u, v_):
        ax.text(xi - w_ / 2, 0.07, pc(uu, 2), ha="center", va="bottom", fontsize=7.5, color=INK if ax is p else "white"); ax.text(xi + w_ / 2, 0.07, pc(vv, 2), ha="center", va="bottom", fontsize=7.5, color="white" if ax is q else "white")
    ax.axhline(FEE_COP / 1e6, color=ACC, lw=1.3, ls="--", zorder=5, label=f"Tarifa Visa R: COP {pc(FEE_COP / 1e6, 2)} M")
    ax.set_ylim(0, 4.3); ax.set_yticks([0, 1, 2, 3, 4]); ax.set_ylabel("Millones de COP al mes"); ax.grid(axis="y", color="#e8e8e8", lw=0.5); ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=8, ncol=3, handlelength=1.4, columnspacing=1.2)
p.set_title("a) Venezolanos y colombianos", loc="left", fontsize=8.8, style="italic", pad=3)
q.set_title("b) Venezolanos según afiliación a salud (indicador de regularización)", loc="left", fontsize=8.8, style="italic", pad=3)
q.set_xticks(x); q.set_xticklabels(labs, fontsize=8)
save(fig, "pr5_ingreso_educacion.png")
print("ok")
