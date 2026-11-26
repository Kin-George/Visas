"""Visa-R / 25: lo que Cancillería deja de recibir frente al beneficio económico para el país.
Costo: recaudo de la tarifa con la tendencia de visas 2027-2031 = 44.580 visas x USD 464 = USD 20,7 M (en cinco años).
Beneficio anual por cada persona adicional que conserva su estatus regular gracias a la gratuidad:
  - Consumo adicional: el PEP aumenta 48 % el consumo por persona (Ibáñez et al., 2025, JEEA). Consumo base por persona =
    masa salarial anual de los venezolanos (COP 13,8 billones, GEIH 2025) x (1 - 10 % ahorro - 10 % remesas) / 1,76 M venezolanos (GEIH 2025),
    descompuesto entre regulares (66 %) e irregulares: C_irregular = C_promedio / (0,34 + 0,66 x 1,48). Ganancia = 0,48 x C_irregular.
  - Ahorro fiscal: USD 198,29 por persona al año (Ibáñez et al., 2025; 2,25 venezolanos por hogar).
Personas adicionales con visa (escenarios de conversión, Code/24): 122.340, 309.329 y 663.951. TRM 2025 = 4.052,86.
Salida: Outputs/Figures/pr10_costo_vs_beneficio.png y Outputs/tables/t24_costo_vs_beneficio.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#9fc0ea", "#eb6a35", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
miles = lambda x: f"{x:,.0f}".replace(",", ".")

TRM = 4052.86
MASA, POB, AHORRO, REMESAS, COB, EFECTO = 13.8e12, 1.76e6, 0.10, 0.10, 0.66, 0.48
c_prom = MASA * (1 - AHORRO - REMESAS) / POB
c_irr = c_prom / ((1 - COB) + COB * (1 + EFECTO))
gan_cons_usd = EFECTO * c_irr / TRM                 # consumo adicional por persona al año (USD)
FISCAL = 198.29
COSTO = 44_580 * 464 / 1e6
pers = {"Conservador": 122_340, "Intermedio": 309_329, "Optimista": 663_951}
cons = {k: v * gan_cons_usd / 1e6 for k, v in pers.items()}
fis = {k: v * FISCAL / 1e6 for k, v in pers.items()}
tot = {k: cons[k] + fis[k] for k in pers}
pd.DataFrame({"escenario": list(pers), "personas_adicionales": list(pers.values()), "consumo_adicional_USD_M_anual": list(cons.values()),
              "ahorro_fiscal_USD_M_anual": list(fis.values()), "beneficio_total_USD_M_anual": list(tot.values()),
              "veces_el_recaudo_de_5_anios": [t / COSTO for t in tot.values()]}).round(1).to_csv(TAB / "t24_costo_vs_beneficio.csv", index=False)

fig, ax = plt.subplots(figsize=(6.6, 4.0)); fig.subplots_adjust(left=0.27, right=0.96, top=0.76, bottom=0.2)
labs = ["Cancillería deja" + NL + "de recibir (5 años)"] + [f"El país gana" + NL + f"cada año: {k.lower()}" for k in pers]
y = np.arange(4)[::-1]
ax.barh(y[0], COSTO, 0.6, color=ORANGE)
ax.text(COSTO + 8, y[0], f"USD {COSTO:.0f} M", va="center", fontsize=12, fontweight="bold", color=ORANGE)
for yi, k in zip(y[1:], pers):
    ax.barh(yi, cons[k], 0.6, color=BLUE)
    ax.barh(yi, fis[k], 0.6, left=cons[k], color=NAVY)
    ax.text(tot[k] + 8, yi, f"USD {tot[k]:.0f} M", va="center", fontsize=12, fontweight="bold", color=NAVY)
ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=10); ax.tick_params(axis="y", length=0)
ax.set_xticks([]); ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, 660)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=NAVY)],
          labels=["Consumo adicional de los hogares", "Ahorro fiscal del Estado"], loc="upper center", bbox_to_anchor=(0.4, -0.02), ncol=2, frameon=False, fontsize=9.5)
fig.text(0.03, 0.94, f"Cancillería deja de recibir USD {COSTO:.0f} millones; el país gana" + NL + f"entre USD {min(tot.values()):.0f} y {max(tot.values()):.0f} millones cada año",
         fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.8, "Recaudo de la tarifa en 2027-2031 frente al beneficio anual de quienes obtienen la Visa R sin tarifa.", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.03, "Fuente: Ibáñez et al. (2025), JEEA; DANE, GEIH 2025 y EPM VIII-2025; Migración Colombia (oct-2026); Cancillería.", fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr10_costo_vs_beneficio.png", dpi=250, facecolor="white"); plt.close(fig)
print("consumo base COP", round(c_prom), "irregular", round(c_irr), "ganancia USD", round(gan_cons_usd, 1), "costo", round(COSTO, 1), {k: round(v, 1) for k, v in tot.items()},
      {k: round(v, 1) for k, v in cons.items()})
