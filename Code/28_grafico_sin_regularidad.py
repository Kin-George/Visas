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
d_ing = (ing_reg - ing_irr) / TRM
d = {"PIB (valor agregado)": d_ing / SH_LAB,
     "Consumo de los hogares": (cons_reg - cons_irr) / TRM,
     "Ingreso laboral": d_ing,
     "Impuestos y aportes": (935.19 - 498.0) / 2.25}
tot = {k: v * REGULARES / 1e6 for k, v in d.items()}
pib_pct = 100 * tot["PIB (valor agregado)"] * 1e6 * TRM / PIB
pd.DataFrame({"indicador": list(d), "perdida_por_persona_USD_anual": list(d.values()), "perdida_total_USD_M_anual": list(tot.values())}).round(1).to_csv(
    TAB / "t28_sin_regularidad.csv", index=False)

fig, ax = plt.subplots(figsize=(6.8, 4.1)); fig.subplots_adjust(left=0.27, right=0.95, top=0.74, bottom=0.12)
labs = list(d)[::-1]; vals = [tot[k] for k in labs]
cols = [ORANGE if k == "PIB (valor agregado)" else "#f2a27e" for k in labs]
y = np.arange(len(labs))
ax.barh(y, vals, 0.58, color=cols)
for yi, k, v in zip(y, labs, vals):
    extra = f"{pc(pib_pct)} % del PIB · " if k == "PIB (valor agregado)" else ""
    ax.text(v + 20, yi + 0.1, f"−USD {miles(v)} M", va="center", fontsize=12, fontweight="bold", color=ORANGE)
    ax.text(v + 20, yi - 0.24, f"{extra}USD {miles(d[k])} menos por persona al año", va="center", fontsize=8.3, color=GRAY)
ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=11); ax.tick_params(axis="y", length=0)
ax.set_xticks([]); ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, 2600)
fig.text(0.03, 0.94, f"Si los 2 millones de migrantes venezolanos regulares pasaran a ser irregulares," + NL +
         f"Colombia perdería USD {pc(tot['PIB (valor agregado)'] / 1e3, 1)} mil millones de PIB cada año", fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.79, f"Pérdida anual frente a hoy. Regulares hoy: {miles(REGULARES)} (PPT y cédula de extranjería).", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.025, "Fuente: Ibáñez et al. (2025), JEEA; DANE, GEIH 2025, EPM VIII-2025 y cuentas nacionales; Migración Colombia (2026).", fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr15_sin_regularidad.png", dpi=250, facecolor="white"); plt.close(fig)
print({k: (round(d[k]), round(tot[k])) for k in d}, "PIB %", round(pib_pct, 3))
