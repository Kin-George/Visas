"""Visa-R / 21: beneficio fiscal de mantener la regularidad (de dónde salen los USD 980 por persona) y beneficio total según la tarifa.
Fuente del beneficio: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), JEEA 23(3), sección 7 y cuadro 7 (USD de 2020, acceso observado a servicios):
  hogar migrante sin PEP: ingresos fiscales 498, gasto público 1.554, costo neto 1.056; hogar con PEP: ingresos 935, gasto 1.545, costo neto 610.
Venezolanos por hogar: 2,28 (GEIH 2026). Conversión a la Visa R: modelo ilustrativo de Code/10 (theta = 2): 43,6 % con USD 464 y 85 % con tarifa cero.
Escala: 1.975.752 PPT autorizados (Migración Colombia, octubre 2026).
Salidas: Outputs/Figures/pr8a_como_se_calcula_beneficio.png, pr8b_beneficio_total.png"""
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

ING = (498, 935); GAS = (1554, 1545); NETO = (1056, 610)
AHORRO = NETO[0] - NETO[1]; VEN_HOG = 2.28; ANUAL = AHORRO / VEN_HOG; S5 = ANUAL * 5
N_PPT = 1_975_752; CONV = {"Tarifa actual" + NL + "(USD 464)": 0.43596, "Tarifa cero": 0.85}

# =============================================================== propuesta A: de dónde salen los USD 980
fig = plt.figure(figsize=(6.6, 5.0))
fig.text(0.03, 0.95, "Cada venezolano regularizado le ahorra al Estado cerca de USD 980", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.905, "Un hogar con permiso paga más impuestos y cuesta casi lo mismo en servicios públicos (por hogar, al año).", fontsize=10, ha="left", color=ACC)
ax = fig.add_axes([0.2, 0.47, 0.76, 0.36])
grupos = ["Ingresos fiscales" + NL + "(IVA y aportes)", "Gasto público" + NL + "(salud, educación,\nasistencia)".replace("\n", NL), "Costo neto" + NL + "para el Estado"]
vals = [ING, GAS, NETO]; y = np.arange(3)[::-1]; h = 0.36
for yi, (a, b) in zip(y, vals):
    ax.barh(yi + h / 2, a, h, color=LGRAY); ax.barh(yi - h / 2, b, h, color=NAVY)
    ax.text(a + 25, yi + h / 2, f"USD {miles(a)}", va="center", fontsize=9.5, color=GRAY)
    ax.text(b + 25, yi - h / 2, f"USD {miles(b)}", va="center", fontsize=9.5, color=NAVY, fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels(grupos, fontsize=9.5); ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, 2000)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=LGRAY), plt.Rectangle((0, 0), 1, 1, color=NAVY)],
          labels=["Hogar sin permiso", "Hogar con permiso (PEP)"], loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=2, frameon=False, fontsize=9.5)
ax.text(1460, 0.0, f"USD {AHORRO} menos" + NL + "por hogar al año", fontsize=9.5, color=ACC, va="center", fontweight="bold")

bx = fig.add_axes([0.02, 0.07, 0.96, 0.3]); bx.axis("off"); bx.set_xlim(0, 10); bx.set_ylim(0, 3)
pasos = [(f"USD {AHORRO}", "menos de costo neto" + NL + "por hogar al año", LNAVY, INK),
         (f"USD {ANUAL:.0f}", "por persona al año", LNAVY, INK),
         (f"≈ USD {round(S5, -1):.0f}", "por persona" + NL + "en 5 años", ACC, "white")]
ops = [f"÷ {VEN_HOG:.1f}".replace(".", ",") + NL + "venezolanos" + NL + "por hogar", "× 5 años"]
xs = [0.2, 3.75, 7.3]; w = 2.5
for (big, small, fc, tc), x0 in zip(pasos, xs):
    bx.add_patch(FancyBboxPatch((x0, 0.55), w, 1.9, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec="none"))
    bx.text(x0 + w / 2, 1.85, big, ha="center", va="center", fontsize=15, fontweight="bold", color=tc)
    bx.text(x0 + w / 2, 1.05, small, ha="center", va="center", fontsize=9.5, color=tc)
for x0, op in zip(xs[:2], ops):
    bx.annotate("", xy=(x0 + w + 0.95, 1.5), xytext=(x0 + w + 0.1, 1.5), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.2))
    bx.text(x0 + w + 0.52, 1.75, op, ha="center", va="bottom", fontsize=8.5, color=GRAY)
fig.text(0.03, 0.02, "Fuente: Ibáñez, Moya, Ortega, Rozo y Urbina (2025), Journal of the European Economic Association (USD de 2020); GEIH-DANE 2026.",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr8a_como_se_calcula_beneficio.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== propuesta B: beneficio total según la tarifa
fig, ax = plt.subplots(figsize=(6.4, 3.9)); fig.subplots_adjust(left=0.05, right=0.95, top=0.78, bottom=0.2)
labs = list(CONV); per = np.array([CONV[k] * N_PPT for k in labs]); ben = per * S5 / 1e6
x = np.arange(2)
ax.bar(x, ben, 0.5, color=[LNAVY, ACC])
for xi, b, p in zip(x, ben, per):
    ax.text(xi, b + 30, f"USD {miles(b)} millones", ha="center", va="bottom", fontsize=13, fontweight="bold", color=ACC if xi == 1 else INK)
    ax.text(xi, b / 2, (f"{p / 1e6:.2f}".replace(".", ",") + " millones" + NL + "de personas pasan" if p >= 1e6 else f"{miles(p / 1e3)} mil" + NL + "personas pasan") + NL + "a la Visa R", ha="center", va="center", fontsize=10, color="white" if xi == 1 else INK)
ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=11); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_ylim(0, 1950); ax.set_xlim(-0.6, 1.6)
fig.text(0.03, 0.94, "Con tarifa cero, el beneficio fiscal casi se duplica", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.875, "Ahorro fiscal en 5 años de las personas con PPT que pasan a la Visa R (USD 980 por persona).", fontsize=10.5, ha="left", color=ACC)
fig.text(0.03, 0.03, "Fuente: Ibáñez et al. (2025), JEEA; GEIH-DANE 2026; EPM VIII-2025 (DANE); Migración Colombia (PPT autorizados, octubre de 2026).",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr8b_beneficio_total.png", dpi=250, facecolor="white"); plt.close(fig)
print("ahorro hogar", AHORRO, "anual persona", round(ANUAL, 1), "5 anios", round(S5, 1), "| personas", per.round(), "beneficio M", ben.round())
