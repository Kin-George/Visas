"""Visa-R / 15: graficos de la version limpia del proyecto 'Visas R Cancilleria'. Escala OFICIAL de PPT (1.973.253 autorizados, julio 2024).
Salida: Outputs/Figures/pr1_visas_por_anio.png, pr2_calendario_asequibilidad.png, pr3_demanda_recaudo_derrame.png (gr1 y gr6 se reutilizan de Code/11)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, GRAY, LGRAY, ACC, INK = "#1f3b5c", "#8c8c8c", "#cfcfcf", "#a4472f", "#222222"
W = 5.9
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 9, "text.color": INK,
    "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.labelcolor": INK, "axes.labelsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
    "grid.color": "#e4e4e4", "grid.linewidth": 0.5, "xtick.color": INK, "ytick.color": INK, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "legend.frameon": False, "legend.fontsize": 8.5, "figure.dpi": 100})
pc = lambda x, d=0: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")
N_OFF = 1_973_253                                         # PPT autorizados (julio 2024), dato del borrador (Migracion Colombia)
r12 = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
N_GEIH = r12["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3
S = r12["beneficio_fiscal_anual_B_USD_por_persona"] * 5
save = lambda fig, n: (fig.savefig(FIG / n, dpi=250, facecolor="white"), plt.close(fig))
val = lambda ax, x, y, t, **k: ax.text(x, y, t, ha="center", va="bottom", fontsize=8, color=k.pop("color", INK), **k)

# ---------------------------------------------------------------- pr1: visas R por anio
fig, ax = plt.subplots(figsize=(W, 2.1)); fig.subplots_adjust(left=0.1, right=0.99, top=0.95, bottom=0.17)
anios, v = ["2024", "2025", "2026\n(al 9 de octubre)"], [1248, 3307, 1593]
proy = round(1593 * 365 / 282)                                   # 9 de octubre = dia 282
ax.bar([0, 1], v[:2], 0.5, color=NAVY); ax.bar(2, v[2], 0.5, color=NAVY)
ax.bar(2, proy - v[2], 0.5, bottom=v[2], facecolor="white", edgecolor=NAVY, hatch="////", linewidth=0.8)
for x_, y_ in zip([0, 1, 2], v): val(ax, x_, y_ + 40 if x_ < 2 else y_ - 420, miles(y_), color=INK if x_ < 2 else "white")
val(ax, 2, proy + 40, f"≈ {miles(proy)}\n(proyección lineal)")
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(anios); ax.set_ylim(0, 4000); ax.set_ylabel("Visas R, actividad ETPV")
save(fig, "pr1_visas_por_anio.png")

# ---------------------------------------------------------------- pr2: calendario (escala oficial) y asequibilidad
el = pd.read_csv(TAB / "t12b_elegibilidad_por_anio.csv"); acum = el.pct_titulares_con_5_anios_de_PPT.to_numpy() / 100
nuevos = np.diff(np.r_[0, acum]) * N_OFF / 1e3
asq = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
fees = [("USD 464\n(vigente)", "USD 464 (56+408) vigente"), ("USD 232", "mitad (USD 232)"), ("USD 56\n(estudio)", "solo estudio USD 56 (se elimina la visa)"), ("USD 0", None)]
g = lambda f, k: 0.0 if f is None else asq[(asq.tarifa == f) & (asq.umbral == f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar")].pct_hogares_con_venezolano.iloc[0]
fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.45), gridspec_kw={"width_ratios": [1.25, 1]}); fig.subplots_adjust(left=0.1, right=0.99, top=0.88, bottom=0.25, wspace=0.3)
yr = el.anio.to_numpy()[:5]
a.bar(yr, nuevos[:5], color=NAVY, width=0.55)
for x_, v_ in zip(yr, nuevos[:5]): val(a, x_, v_ + 20, miles(v_))
a.set_xticks(yr); a.set_xticklabels([f"{y_}\n({p_*100:.0f} %)" for y_, p_ in zip(yr, acum[:5])], fontsize=8)
a.set_ylim(0, 1250); a.set_ylabel("Miles de titulares"); a.set_title("a) Titulares que cumplen 5 años de PEP o PPT", loc="left", fontsize=8.5, style="italic")
a.text(2029.5, 1150, "El PPT vence el\n30 de mayo de 2031", color=ACC, fontsize=7.5, ha="center", va="top")
x = np.arange(4); w = 0.34
v1 = [g(f, 1) for _, f in fees]; v2 = [g(f, 2) for _, f in fees]
b.bar(x - w / 2, v1, w, color=NAVY, label="Más de 1 mes"); b.bar(x + w / 2, v2, w, color=LGRAY, edgecolor="#9a9a9a", linewidth=0.5, label="Más de 2 meses")
for xi, p, q in zip(x, v1, v2): val(b, xi - w / 2, p + 1, pc(p)); val(b, xi + w / 2, q + 1, pc(q))
b.set_xticks(x); b.set_xticklabels([n for n, _ in fees], fontsize=7.5); b.set_ylim(0, 80); b.set_ylabel("% de hogares con venezolanos"); b.legend(loc="upper right", fontsize=7.5, handlelength=1.2)
b.set_title("b) Hogares donde la tarifa supera su ingreso", loc="left", fontsize=8.5, style="italic")
save(fig, "pr2_calendario_asequibilidad.png")

# ---------------------------------------------------------------- pr3: demanda, recaudo y derrame (escala oficial)
cv = pd.read_csv(TAB / "t17_curva_precio_recaudo.csv"); cv = cv[cv.theta_meses_de_ingreso == 2].sort_values("tarifa_USD").reset_index(drop=True)
F = cv.tarifa_USD.to_numpy().astype(float); raw = cv.conversion.to_numpy()
tau = pd.Series(raw).rolling(5, center=True, min_periods=1).mean().to_numpy(); tau[0] = raw[0]
Q = N_OFF * tau / 1e3; rec = N_OFF * tau * F / 1e6; tot = rec + N_OFF * tau * S / 1e6
at = lambda arr, f: float(np.interp(f, F, arr))
fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.75), gridspec_kw={"width_ratios": [1, 1.1]}); fig.subplots_adjust(left=0.1, right=0.99, top=0.9, bottom=0.2, wspace=0.32)
a.plot(Q, F, color=NAVY, lw=1.6); q1 = at(Q, 464)
a.add_patch(Rectangle((0, 0), q1, 464, facecolor="#e4e4e4", edgecolor="#7a7a7a", linewidth=0.8, zorder=1))
a.text(q1 / 2, 464 - 45, f"Ingreso = {at(rec, 464):.0f} M", ha="center", fontsize=8)
a.text(q1 + 20, 464 + 6, f"P = 464; {miles(q1)} mil", fontsize=8, ha="left")
q0 = at(Q, 0); a.scatter([q0], [0], color=ACC, s=26, zorder=4, clip_on=False)
a.annotate(f"P = 0; {miles(q0)} mil\n(sin costo)", xy=(q0, 0), xytext=(1000, 150), fontsize=8, color=ACC, ha="center", arrowprops=dict(arrowstyle="-", color=ACC, lw=0.7))
a.set_xlim(0, 1750); a.set_ylim(0, 700); a.set_xlabel("Titulares que convierten (miles)"); a.set_ylabel("Precio por persona (USD)")
a.set_title("a) Demanda e ingreso por la tarifa", loc="left", fontsize=8.5, style="italic")
b.fill_between(F, rec, tot, color="#dfe6ee", lw=0, label="Derrame"); b.plot(F, tot, color=NAVY, lw=1.6, label="Recaudo + derrame"); b.plot(F, rec, color=ACC, lw=1.6, label="Recaudo de la Cancillería")
for P, c in ((0, ACC), (464, INK)):
    b.axvline(P, ymax=0.62, color=c, lw=0.7, ls=":"); b.scatter([P], [at(tot, P)], color=c, s=22, zorder=4, clip_on=False)
b.text(12, at(tot, 0) - 140, f"{at(tot, 0):,.0f}".replace(",", "."), fontsize=8, color=ACC, ha="left", va="top")
b.text(464 - 14, at(tot, 464) - 60, f"{at(tot, 464):,.0f}".replace(",", "."), fontsize=8, color=INK, ha="right", va="top")
b.set_xlim(0, 700); b.set_ylim(0, 2000); b.set_xlabel("Precio por persona (USD)"); b.set_ylabel("Millones de USD")
b.set_xticks([0, 232, 464, 600]); b.set_xticklabels(["0\n(sin costo)", "232", "464\n(vigente)", "600"], fontsize=8); b.legend(loc="upper right", fontsize=7.5, handlelength=1.6)
b.set_title("b) Recaudo y valor total", loc="left", fontsize=8.5, style="italic")
save(fig, "pr3_demanda_recaudo_derrame.png")
print("ok", miles(nuevos[0]), miles(nuevos[1]), round(at(rec, 464)), round(at(tot, 464)), round(at(tot, 0)), round(q1), round(q0), proy)
