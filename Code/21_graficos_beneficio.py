"""Visa-R / 21: beneficio fiscal de mantener la regularidad.
Fuente del beneficio: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), JEEA 23(3), sección 7 y cuadro 7 (USD de 2020, acceso observado a servicios):
  hogar migrante sin PEP: ingresos fiscales 498, gasto público 1.554, costo neto 1.056; hogar con PEP: ingresos 935, gasto 1.545, costo neto 610.
Venezolanos por hogar: 2,28 (GEIH 2026). Personas con PPT que piensan quedarse: 89,6 % de 1.975.752 (EPM VIII-2025; Migración Colombia, oct. 2026).
Salidas: Outputs/Figures/pr8a_como_se_calcula_beneficio.png, pr8b_ahorro_acumulado_pais.png"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "Outputs" / "Figures"
NAVY, LNAVY, ACC, INK, GRAY, LGRAY, GREEN = "#1f3b5c", "#9fb3c8", "#a4472f", "#222222", "#6b6b6b", "#c9c9c9", "#4f7d5c"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
miles = lambda x: f"{x:,.0f}".replace(",", ".")

ING = (498, 935); GAS = (1554, 1545); NETO = (1056, 610)
AHORRO = NETO[0] - NETO[1]; VEN_HOG = 2.28; ANUAL = AHORRO / VEN_HOG; S5 = ANUAL * 5
N_QUEDAN = 0.896 * 1_975_752

# =============================================================== gráfico A: de dónde salen los USD 980 (cascada + cadena)
fig = plt.figure(figsize=(6.6, 5.0))
fig.text(0.03, 0.955, "Cada venezolano regularizado le ahorra al Estado cerca de USD 980", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.91, "Por hogar, al año: con permiso paga más impuestos y el gasto público casi no cambia.", fontsize=10.5, ha="left", color=ACC)
ax = fig.add_axes([0.06, 0.47, 0.9, 0.37])
d_ing, d_gas = ING[1] - ING[0], GAS[0] - GAS[1]
etq = ["Costo neto de un" + NL + "hogar sin permiso", "Paga más impuestos" + NL + "(IVA y aportes)", "Gasta un poco" + NL + "menos en servicios", "Costo neto de un" + NL + "hogar con permiso"]
bot = [0, NETO[0] - d_ing, NETO[0] - d_ing - d_gas, 0]; alt = [NETO[0], d_ing, d_gas, NETO[1]]
col = [LGRAY, GREEN, GREEN, NAVY]
ax.bar(range(4), alt, 0.6, bottom=bot, color=col)
txt = [f"USD {miles(NETO[0])}", f"− USD {d_ing}", f"− USD {d_gas}", f"USD {NETO[1]}"]
for i, (b, a, t) in enumerate(zip(bot, alt, txt)):
    ax.text(i, b + a + 25, t, ha="center", va="bottom", fontsize=12, fontweight="bold", color=GREEN if i in (1, 2) else (NAVY if i == 3 else GRAY))
for i in range(3):
    lvl = [NETO[0], NETO[0] - d_ing, NETO[1]][i]
    ax.plot([i + 0.3, i + 0.7], [lvl, lvl], color=GRAY, lw=0.8, ls=":")
ax.set_xticks(range(4)); ax.set_xticklabels(etq, fontsize=9.5); ax.tick_params(axis="x", length=0)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 1250); ax.set_xlim(-0.5, 3.95)
ax.annotate("", xy=(3.38, NETO[1]), xytext=(3.38, NETO[0]), arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.2))
ax.text(3.42, (NETO[0] + NETO[1]) / 2, f"USD {AHORRO}" + NL + "menos", fontsize=10, color=ACC, fontweight="bold", va="center")
ax.plot([0, 3.38], [NETO[0], NETO[0]], color=ACC, lw=0.6, ls=":")

bx = fig.add_axes([0.02, 0.06, 0.96, 0.26]); bx.axis("off"); bx.set_xlim(0, 10); bx.set_ylim(0, 3)
pasos = [(f"USD {AHORRO}", "menos por hogar" + NL + "al año", LNAVY, INK),
         (f"USD {ANUAL:.0f}", "por persona" + NL + "al año", LNAVY, INK),
         (f"≈ USD {round(S5, -1):.0f}", "por persona" + NL + "en 5 años", ACC, "white")]
ops = [("÷ 2,3", "venezolanos" + NL + "por hogar"), ("× 5", "años")]
xs = [0.1, 3.75, 7.4]; w = 2.45
for (big, small, fc, tc), x0 in zip(pasos, xs):
    bx.add_patch(FancyBboxPatch((x0, 0.35), w, 2.3, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec="none"))
    bx.text(x0 + w / 2, 1.9, big, ha="center", va="center", fontsize=16, fontweight="bold", color=tc)
    bx.text(x0 + w / 2, 0.95, small, ha="center", va="center", fontsize=10, color=tc)
for x0, op in zip(xs[:2], ops):
    bx.annotate("", xy=(x0 + w + 1.1, 1.5), xytext=(x0 + w + 0.1, 1.5), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.3))
    bx.text(x0 + w + 0.6, 1.67, op[0], ha="center", va="bottom", fontsize=11, color=INK, fontweight="bold")
    bx.text(x0 + w + 0.6, 1.33, op[1], ha="center", va="top", fontsize=8.5, color=GRAY)
fig.text(0.03, 0.015, "Fuente: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), Journal of the European Economic Association; GEIH-DANE 2026.",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr8a_como_se_calcula_beneficio.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== gráfico B: costo neto anual para el Estado, regulares frente a irregulares
c_reg, c_irr = NETO[1] / VEN_HOG * N_QUEDAN / 1e6, NETO[0] / VEN_HOG * N_QUEDAN / 1e6
fig, ax = plt.subplots(figsize=(6.4, 3.9)); fig.subplots_adjust(left=0.05, right=0.97, top=0.78, bottom=0.2)
x = [0, 1]; vals = [c_reg, c_irr]
ax.bar(x, vals, 0.5, color=[NAVY, LGRAY])
for xi, v, c in zip(x, vals, [NAVY, GRAY]):
    ax.text(xi, v + 18, f"USD {miles(v)} millones", ha="center", va="bottom", fontsize=13, fontweight="bold", color=c)
ax.set_xticks(x); ax.set_xticklabels(["Si siguen" + NL + "en situación regular", "Si pierden" + NL + "la regularidad"], fontsize=11)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 1000); ax.set_xlim(-0.5, 1.9)
ax.annotate("", xy=(1.38, c_reg), xytext=(1.38, c_irr), arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.3))
ax.plot([0.25, 1.38], [c_reg, c_reg], color=ACC, lw=0.7, ls=":")
ax.text(1.43, (c_reg + c_irr) / 2, f"USD {miles(c_irr - c_reg)}" + NL + "millones" + NL + "más cada año", fontsize=11, color=ACC, fontweight="bold", va="center")
fig.text(0.03, 0.94, "Si pierden la regularidad, al Estado le cuestan USD 346 millones más al año", fontsize=12.5, fontweight="bold", ha="left")
fig.text(0.03, 0.875, "Costo neto anual para el Estado de las 1,77 millones de personas con PPT que piensan quedarse.", fontsize=10, ha="left", color=ACC)
fig.text(0.03, 0.03, "Fuente: Ibáñez et al. (2025), JEEA; GEIH-DANE 2026; EPM VIII-2025 (DANE); Migración Colombia (octubre de 2026).",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr8b_costo_regular_vs_irregular.png", dpi=250, facecolor="white"); plt.close(fig)
print("personas", round(N_QUEDAN), "costo regular M", round(c_reg), "irregular M", round(c_irr), "diferencia", round(c_irr - c_reg))
