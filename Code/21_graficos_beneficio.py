"""Visa-R / 21: beneficio fiscal de mantener la regularidad (de dónde salen los USD 980 por persona) y comparación con la tarifa.
Fuente del beneficio: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), JEEA 23(3), sección 7 y cuadro 7 (USD de 2020, acceso observado a servicios):
  hogar migrante sin PEP: ingresos fiscales 498, gasto público 1.554, costo neto 1.056; hogar con PEP: ingresos 935, gasto 1.545, costo neto 610.
Venezolanos por hogar: 2,28 (GEIH 2026).
Salidas: Outputs/Figures/pr8a_como_se_calcula_beneficio.png, pr8b_ahorro_vs_tarifa.png"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "Outputs" / "Figures"
NAVY, LNAVY, ACC, INK, GRAY, LGRAY = "#1f3b5c", "#9fb3c8", "#a4472f", "#222222", "#6b6b6b", "#c9c9c9"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
miles = lambda x: f"{x:,.0f}".replace(",", ".")

NETO = (1056, 610); AHORRO = NETO[0] - NETO[1]; VEN_HOG = 2.28; ANUAL = AHORRO / VEN_HOG; S5 = ANUAL * 5; FEE = 464

# =============================================================== propuesta A: de dónde salen los USD 980
fig = plt.figure(figsize=(6.6, 4.6))
fig.text(0.03, 0.95, "Cada venezolano regularizado le ahorra al Estado cerca de USD 980", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.895, "Un hogar con permiso le cuesta menos al Estado porque paga más impuestos.", fontsize=10.5, ha="left", color=ACC)
ax = fig.add_axes([0.25, 0.53, 0.72, 0.29])
y = [1, 0]; cols = [LGRAY, NAVY]; labs = ["Hogar sin permiso", "Hogar con permiso"]
ax.barh(y, NETO, 0.55, color=cols)
for yi, v, c in zip(y, NETO, [GRAY, NAVY]):
    ax.text(v + 20, yi, f"USD {miles(v)}", va="center", fontsize=12, fontweight="bold", color=c)
ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=11); ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, 1700); ax.set_ylim(-0.5, 1.75)
ax.text(0, 1.5, "Costo neto para el Estado, por hogar al año", fontsize=10, color=GRAY, va="center")
ax.annotate("", xy=(NETO[1], 0.5), xytext=(NETO[0], 0.5), arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.3))
ax.text(NETO[0] + 30, 0.5, f"USD {AHORRO} menos", ha="left", va="center", fontsize=10.5, color=ACC, fontweight="bold")

bx = fig.add_axes([0.02, 0.08, 0.96, 0.33]); bx.axis("off"); bx.set_xlim(0, 10); bx.set_ylim(0, 3)
pasos = [(f"USD {AHORRO}", "menos por hogar" + NL + "al año", LNAVY, INK),
         (f"USD {ANUAL:.0f}", "por persona" + NL + "al año", LNAVY, INK),
         (f"≈ USD {round(S5, -1):.0f}", "por persona" + NL + "en 5 años", ACC, "white")]
ops = [("÷ 2,3", "venezolanos" + NL + "por hogar"), ("× 5", "años")]
xs = [0.1, 3.75, 7.4]; w = 2.45
for (big, small, fc, tc), x0 in zip(pasos, xs):
    bx.add_patch(FancyBboxPatch((x0, 0.45), w, 2.0, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec="none"))
    bx.text(x0 + w / 2, 1.85, big, ha="center", va="center", fontsize=16, fontweight="bold", color=tc)
    bx.text(x0 + w / 2, 1.0, small, ha="center", va="center", fontsize=10, color=tc)
for x0, op in zip(xs[:2], ops):
    bx.annotate("", xy=(x0 + w + 1.1, 1.45), xytext=(x0 + w + 0.1, 1.45), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.3))
    bx.text(x0 + w + 0.6, 1.62, op[0], ha="center", va="bottom", fontsize=11, color=INK, fontweight="bold")
    bx.text(x0 + w + 0.6, 1.3, op[1], ha="center", va="top", fontsize=8.5, color=GRAY)
fig.text(0.03, 0.02, "Fuente: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), Journal of the European Economic Association; GEIH-DANE 2026.",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr8a_como_se_calcula_beneficio.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== propuesta B: el ahorro acumulado supera la tarifa
anios = np.arange(1, 6); acum = ANUAL * anios
fig, ax = plt.subplots(figsize=(6.4, 3.9)); fig.subplots_adjust(left=0.05, right=0.97, top=0.78, bottom=0.17)
ax.bar(anios, acum, 0.6, color=[LNAVY if a < FEE else ACC for a in acum])
for x_, a in zip(anios, acum):
    ax.text(x_, a - 25, f"USD {miles(a)}", ha="center", va="top", fontsize=11.5, fontweight="bold", color="white" if a >= FEE else INK)
ax.axhline(FEE, color=INK, lw=1.2, ls="--")
ax.text(0.5, FEE + 18, f"Tarifa de la Visa R: USD {FEE}", fontsize=10.5, color=INK, ha="left", va="bottom")
ax.set_xticks(anios); ax.set_xticklabels([f"Año {a}" for a in anios], fontsize=11); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_ylim(0, 1100); ax.set_xlim(0.4, 5.6)
fig.text(0.03, 0.94, "En menos de 3 años, el ahorro supera el valor de la tarifa", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.875, "Ahorro fiscal acumulado por cada venezolano que se mantiene en situación regular.", fontsize=10.5, ha="left", color=ACC)
fig.text(0.03, 0.03, "Fuente: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), Journal of the European Economic Association; GEIH-DANE 2026; Cancillería.",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr8b_ahorro_vs_tarifa.png", dpi=250, facecolor="white"); plt.close(fig)
print("anual", round(ANUAL, 1), "acumulado", acum.round(), "cruce en anio", round(FEE / ANUAL, 2))
