"""Visa-R / 28: ¿cómo estaría la economía si toda la migración venezolana regular de hoy fuera irregular?
Migrantes regulares hoy: 1.975.752 con PPT autorizado (Migración Colombia, oct-2026) + 14.444 con cédula de extranjería (residentes; feb-2026) = 1.990.196.
Diferencia anual por persona entre un migrante con permiso y uno sin permiso (cálculo de Code/27):
  - Ingreso laboral: +22 % (Ibáñez et al., 2025). Base: masa salarial COP 13,8 billones / 1,76 M venezolanos (GEIH 2025), 66 % con permiso (EPM).
  - Valor agregado (PIB) = ingreso laboral / 0,54 (participación del trabajo en el PIB, DANE).
  - Consumo de los hogares: +48 % (Ibáñez et al., 2025); consumo = ingreso x (1 - 10 % ahorro - 10 % remesas).
  - Impuestos y aportes: USD 935 frente a USD 498 por hogar / 2,25 venezolanos por hogar (Ibáñez et al., 2025).
PIB 2025 = COP 1.852,7 billones (DANE); TRM 4.052,86.
Salida: Outputs/Figures/pr15_sin_regularidad.png y Outputs/tables/t28_sin_regularidad.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, ORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#eb6a35", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
pc = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")

TRM, PIB, SH_LAB = 4052.86, 1852.7e12, 0.54
REGULARES = 1_975_752 + 14_444
COB, EF_ING, EF_CONS = 0.66, 0.22, 0.48
ing_prom = 13.8e12 / 1.76e6
ing_irr = ing_prom / ((1 - COB) + COB * (1 + EF_ING)); ing_reg = ing_irr * (1 + EF_ING)
cons_prom = ing_prom * 0.8
cons_irr = cons_prom / ((1 - COB) + COB * (1 + EF_CONS)); cons_reg = cons_irr * (1 + EF_CONS)
lev = {"PIB (valor agregado)": (ing_reg / SH_LAB / TRM, ing_irr / SH_LAB / TRM),
       "Consumo de los hogares": (cons_reg / TRM, cons_irr / TRM),
       "Ingreso laboral": (ing_reg / TRM, ing_irr / TRM),
       "Impuestos y aportes": (935.19 / 2.25, 498.0 / 2.25)}
tot = {k: (a * REGULARES / 1e9, b * REGULARES / 1e9) for k, (a, b) in lev.items()}
pib_hoy, pib_irr = (100 * v * 1e9 * TRM / PIB for v in tot["PIB (valor agregado)"])
pd.DataFrame({"indicador": list(tot), "hoy_regulares_USD_miles_M": [a for a, b in tot.values()], "si_irregulares_USD_miles_M": [b for a, b in tot.values()],
              "perdida_USD_M": [(a - b) * 1e3 for a, b in tot.values()], "caida_pct": [100 * (1 - b / a) for a, b in tot.values()]}).round(2).to_csv(TAB / "t28_sin_regularidad.csv", index=False)

fig, ax = plt.subplots(figsize=(7.0, 4.3)); fig.subplots_adjust(left=0.04, right=0.98, top=0.72, bottom=0.2)
x = np.arange(4); w = 0.36; names = list(tot)
for i, k in enumerate(names):
    a, b = tot[k]
    ax.bar(i - w / 2, a, w, color=BLUE); ax.bar(i + w / 2, b, w, color="#f2a27e")
    ax.text(i - w / 2, a + 0.1, pc(a, 1), ha="center", va="bottom", fontsize=11, fontweight="bold", color=BLUE)
    ax.text(i + w / 2, b + 0.1, pc(b, 1), ha="center", va="bottom", fontsize=11, fontweight="bold", color=ORANGE)
    ax.text(i, a + 0.85, f"−{100 * (1 - b / a):.0f} %", ha="center", va="bottom", fontsize=14, fontweight="bold", color=ORANGE)
ax.set_xticks(x); ax.set_xticklabels([n.replace(" (", NL + "(").replace("de los ", "de los" + NL) for n in names], fontsize=10.5)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 9.5); ax.set_xlim(-0.6, 3.6)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color="#f2a27e")],
          labels=["Hoy: con estatus regular", "Si pasaran a ser irregulares"], loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=10)
fig.text(0.03, 0.95, "Si los 2 millones de migrantes regulares pasaran a ser irregulares, su aporte" + NL +
         f"al PIB caería de {pc(pib_hoy)} % a {pc(pib_irr)} %, y lo que pagan en impuestos, casi a la mitad", fontsize=12.5, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.8, f"Aporte anual de los {miles(REGULARES)} venezolanos regulares de hoy (PPT y cédula de extranjería), en miles de millones de USD.",
         fontsize=9.3, ha="left", color=ORANGE)
fig.text(0.03, 0.015, "Fuente: Ibáñez et al. (2025), JEEA; DANE, GEIH 2025, EPM VIII-2025 y cuentas nacionales; Migración Colombia (2026).", fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr15_sin_regularidad.png", dpi=250, facecolor="white"); plt.close(fig)
print({k: (round(a, 2), round(b, 2)) for k, (a, b) in tot.items()}, round(pib_hoy, 2), round(pib_irr, 2))
