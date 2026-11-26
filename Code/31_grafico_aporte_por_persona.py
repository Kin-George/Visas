"""Visa-R / 31: ¿cuánto aporta al año un migrante venezolano regular y uno irregular?
Por persona y por año, en USD (TRM 4.052,86):
  - Ingreso laboral: masa salarial COP 13,8 billones / 1,76 M venezolanos (GEIH 2025); 66 % con permiso (EPM VIII-2025);
    con permiso ganan 22 % más (Ibáñez et al., 2025, JEEA).
  - Aporte al PIB (valor agregado) = ingreso laboral / 0,54 (participación del trabajo en el PIB, DANE).
  - Consumo: ingreso x (1 - 10 % ahorro - 10 % remesas); con permiso consumen 48 % más (Ibáñez et al., 2025).
  - Impuestos y aportes: USD 935 frente a USD 498 por hogar (Ibáñez et al., 2025, cuadro 7) / 2,25 venezolanos por hogar.
El consumo y el PIB no se suman: son dos formas de medir el aporte.
Salida: Outputs/Figures/pr18_aporte_por_persona.png y Outputs/tables/t31_aporte_por_persona.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, ORANGE, LORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#eb6a35", "#f2a27e", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
miles = lambda x: f"{x:,.0f}".replace(",", ".")

TRM, SH_LAB, COB = 4052.86, 0.54, 0.66
ing_prom = 13.8e12 / 1.76e6
ing_irr = ing_prom / ((1 - COB) + COB * 1.22); ing_reg = ing_irr * 1.22
cons_prom = ing_prom * 0.8
cons_irr = cons_prom / ((1 - COB) + COB * 1.48); cons_reg = cons_irr * 1.48
rows = [("Produce" + NL + "(aporte al PIB)", ing_reg / SH_LAB / TRM, ing_irr / SH_LAB / TRM),
        ("Gasta en el país" + NL + "(consumo)", cons_reg / TRM, cons_irr / TRM),
        ("Paga en impuestos" + NL + "y aportes", 935.19 / 2.25, 498.0 / 2.25)]
pd.DataFrame({"concepto": [r[0].replace(NL, " ") for r in rows], "regular_USD": [r[1] for r in rows], "irregular_USD": [r[2] for r in rows],
              "diferencia_USD": [r[1] - r[2] for r in rows], "diferencia_pct": [100 * (r[1] / r[2] - 1) for r in rows]}).round(1).to_csv(
    TAB / "t31_aporte_por_persona.csv", index=False)

fig, ax = plt.subplots(figsize=(7.6, 4.8)); fig.subplots_adjust(left=0.2, right=0.97, top=0.76, bottom=0.12)
h = 0.34
for i, (k, reg, irr) in enumerate(rows):
    y = -i
    ax.barh(y + h / 2, reg, h * 0.92, color=BLUE)
    ax.barh(y - h / 2, irr, h * 0.92, color=LORANGE)
    ax.text(reg + 40, y + h / 2, f"USD {miles(reg)}", va="center", fontsize=11, fontweight="bold", color=BLUE)
    ax.text(irr + 40, y - h / 2, f"USD {miles(irr)}", va="center", fontsize=11, fontweight="bold", color=ORANGE)
    ax.text(5450, y, f"+USD {miles(reg - irr)}" + NL + f"(+{reg / irr * 100 - 100:.0f} %)", va="center", ha="right", fontsize=11.5,
            fontweight="bold", color=NAVY)
ax.set_yticks([-i for i in range(3)]); ax.set_yticklabels([r[0] for r in rows], fontsize=11)
ax.tick_params(axis="y", length=0); ax.set_xticks([]); ax.set_xlim(0, 5500); ax.set_ylim(-2.55, 0.55)
for s in ax.spines.values():
    s.set_visible(False)
ax.text(5450, 0.5, "Diferencia", ha="right", va="bottom", fontsize=10, color=NAVY)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=LORANGE)],
          labels=["Migrante con estatus regular", "Migrante irregular"], loc="upper center", bbox_to_anchor=(0.4, -0.01), ncol=2, frameon=False, fontsize=10.5)
dif = rows[0][1] - rows[0][2]
fig.text(0.03, 0.965, f"Cada año, un migrante regular produce USD {miles(dif)} más que uno irregular:" + NL +
         "más que toda la tarifa de la Visa R (USD 464), que se paga una sola vez", fontsize=13.5, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.835, "Aporte promedio por persona al año, en dólares. La misma persona, con y sin estatus regular.", fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.02, "Fuente: Ibáñez et al. (2025), Journal of the European Economic Association; DANE, GEIH 2025, EPM VIII-2025 y cuentas nacionales.",
         fontsize=7.6, color=GRAY, ha="left")
fig.savefig(FIG / "pr18_aporte_por_persona.png", dpi=250, facecolor="white"); plt.close(fig)
for r in rows:
    print(r[0].replace(NL, " "), round(r[1]), round(r[2]), round(r[1] - r[2]))
