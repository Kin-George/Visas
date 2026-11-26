"""Visa-R / 29: ¿cuánto producen los migrantes venezolanos regulares? Comparación con el PIB de los departamentos.
PIB que generan los 1.990.196 migrantes regulares (PPT y cédula de extranjería): USD 3.817 por persona al año con permiso y USD 3.128 sin permiso
(ingreso laboral GEIH 2025 / 0,54; efecto del permiso +22 %, Ibáñez et al., 2025), a TRM 4.052,86.
PIB departamental 2025pr: DANE, boletín PIBDEP (03-jul-2026), miles de millones de pesos a precios corrientes.
Salida: Outputs/Figures/pr16_pib_departamentos.png"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "Outputs" / "Figures"
NAVY, BLUE, ORANGE, INK, GRAY, LGRAY = "#1f3b5c", "#2a79d6", "#eb6a35", "#222222", "#6b6b6b", "#cfd5dd"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")

TRM, PIB, SH_LAB, REG = 4052.86, 1852.7, 0.54, 1_990_196
ing_prom = 13.8e12 / 1.76e6
ing_irr = ing_prom / (0.34 + 0.66 * 1.22); ing_reg = ing_irr * 1.22
mig_hoy = REG * ing_reg / SH_LAB / 1e12                 # billones de COP
mig_irr = REG * ing_irr / SH_LAB / 1e12
DEP = {"Huila": 32.125, "Risaralda": 31.644, "Caldas": 31.615, "Cesar": 31.535, "Norte de Santander": 30.133, "Nariño": 28.593,
       "Magdalena": 26.858, "Casanare": 23.660}
items = [(k, v, LGRAY) for k, v in DEP.items()] + [("Migrantes regulares (hoy)", mig_hoy, BLUE), ("Si fueran irregulares", mig_irr, ORANGE)]
items.sort(key=lambda t: t[1])

fig, ax = plt.subplots(figsize=(6.8, 4.6)); fig.subplots_adjust(left=0.3, right=0.95, top=0.76, bottom=0.08)
y = np.arange(len(items))
for yi, (k, v, c) in zip(y, items):
    ax.barh(yi, v, 0.66, color=c)
    mig = c != LGRAY
    ax.text(v + 0.3, yi, f"{pc(v)}" + (f"  ({pc(100 * v / PIB, 2)} % del PIB)" if mig else ""), va="center", fontsize=10.5 if mig else 9.5,
            fontweight="bold" if mig else "normal", color=c if mig else GRAY)
ax.set_yticks(y); ax.set_yticklabels([k for k, _, _ in items], fontsize=10)
for t, (k, _, c) in zip(ax.get_yticklabels(), items):
    if c != LGRAY:
        t.set_color(c); t.set_fontweight("bold")
ax.tick_params(axis="y", length=0); ax.set_xticks([]); ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
ax.set_xlim(0, 44)
fig.text(0.03, 0.95, "Los migrantes venezolanos regulares producen al año más que todo" + NL + "Norte de Santander o Nariño, y casi tanto como Caldas",
         fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.82, "PIB de 2025, billones de pesos. Si pasaran a ser irregulares, su aporte bajaría al nivel de Casanare.", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.02, "Fuente: DANE, PIB departamental 2025pr, GEIH 2025 y EPM VIII-2025; Ibáñez et al. (2025), JEEA; Migración Colombia (2026).",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr16_pib_departamentos.png", dpi=250, facecolor="white"); plt.close(fig)
print("migrantes hoy (billones COP)", round(mig_hoy, 2), "irregulares", round(mig_irr, 2))
