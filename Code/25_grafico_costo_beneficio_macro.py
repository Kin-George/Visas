"""Visa-R / 25: lo que Cancillería deja de recibir frente al beneficio económico para el país (3 escenarios).
Escenarios (sobre la demanda potencial: 1.770.136 personas con PPT que quieren quedarse):
  1. Se mantiene la tarifa: visas por tendencia 2024-2026 = 53.733 a may-2031; Cancillería recauda 44.580 visas 2027-2031 x USD 464 = USD 20,7 M.
  2. Sin tarifa, 50 % de la demanda obtiene la visa. Referencia: 54,8 % de los titulares de PPT abrió una cuenta financiera (EPM VIII-2025),
     un paso formal voluntario que el permiso habilita y que exige trámites: cerca de la mitad lo da.
  3. Sin tarifa, 80 % de la demanda obtiene la visa. Referencia: 81 % de los venezolanos con 5 años o más en Colombia está afiliado a salud
     (GEIH 2025), un beneficio gratuito al que accede casi toda la población elegible. Por debajo de los techos: 86 % de quienes iniciaron el ETPV
     obtuvo el PPT (Migración Colombia) y 89,6 % quiere quedarse (EPM).
Beneficio anual por persona adicional con visa (frente al escenario 1):
  - Consumo adicional: +48 % por el permiso (Ibáñez et al., 2025). Consumo base = masa salarial COP 13,8 billones x (1 - 10 % ahorro - 10 % remesas)
    / 1,76 M venezolanos (GEIH 2025); C_irregular = C_promedio / (0,34 + 0,66 x 1,48); ganancia = 0,48 x C_irregular = USD 564 (TRM 4.052,86).
  - Ahorro fiscal: USD 198,29 por persona al año (Ibáñez et al., 2025; 2,25 venezolanos por hogar).
Salida: Outputs/Figures/pr10_costo_vs_beneficio.png y Outputs/tables/t24_costo_vs_beneficio.csv"""
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
miles = lambda x: f"{x:,.0f}".replace(",", ".")

TRM, BASE, CON_TARIFA = 4052.86, 1_770_136, 53_733
MASA, POB, AHORRO, REMESAS, COB, EFECTO = 13.8e12, 1.76e6, 0.10, 0.10, 0.66, 0.48
c_irr = MASA * (1 - AHORRO - REMESAS) / POB / ((1 - COB) + COB * (1 + EFECTO))
CONS_PP = EFECTO * c_irr / TRM                       # consumo adicional por persona al año (USD)
FISCAL_PP = 198.29
COSTO = 44_580 * 464 / 1e6                           # recaudo de la tarifa 2027-2031 (USD M)
TASAS = {"50 %": 0.50, "80 %": 0.80}
con = {k: BASE * t for k, t in TASAS.items()}
extra = {k: v - CON_TARIFA for k, v in con.items()}
cons = {k: v * CONS_PP / 1e6 for k, v in extra.items()}
fis = {k: v * FISCAL_PP / 1e6 for k, v in extra.items()}
tot = {k: cons[k] + fis[k] for k in TASAS}
pd.DataFrame({"escenario": ["Se mantiene la tarifa"] + [f"Sin tarifa, {k} de la demanda" for k in TASAS],
              "con_visa_a_may_2031": [CON_TARIFA] + [round(con[k]) for k in TASAS],
              "personas_adicionales": [0] + [round(extra[k]) for k in TASAS],
              "recaudo_Cancilleria_USD_M_5_anios": [COSTO, 0, 0],
              "consumo_adicional_USD_M_anual": [0] + [cons[k] for k in TASAS],
              "ahorro_fiscal_USD_M_anual": [0] + [fis[k] for k in TASAS],
              "beneficio_total_USD_M_anual": [0] + [tot[k] for k in TASAS]}).round(1).to_csv(TAB / "t24_costo_vs_beneficio.csv", index=False)

fig, ax = plt.subplots(figsize=(6.6, 4.1)); fig.subplots_adjust(left=0.31, right=0.96, top=0.75, bottom=0.2)
y = np.array([2, 1, 0])
labs = ["Se mantiene la tarifa" + NL + f"({miles(CON_TARIFA / 1e3)} mil visas a 2031)",
        "Sin tarifa: 50 % de la demanda" + NL + f"obtiene la visa ({miles(con['50 %'] / 1e3)} mil)",
        "Sin tarifa: 80 % de la demanda" + NL + f"obtiene la visa (1,42 millones)"]
ax.barh(y[0], COSTO, 0.58, color=ORANGE)
ax.text(COSTO + 15, y[0], f"Cancillería recibe USD {COSTO:.0f} M" + NL + "en cinco años", va="center", fontsize=11, fontweight="bold", color=ORANGE)
for yi, k in zip(y[1:], TASAS):
    ax.barh(yi, cons[k], 0.58, color=BLUE); ax.barh(yi, fis[k], 0.58, left=cons[k], color=NAVY)
    ax.text(tot[k] + 15, yi, f"El país gana" + NL + f"USD {miles(tot[k])} M al año", va="center", fontsize=11, fontweight="bold", color=NAVY)
ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=10); ax.tick_params(axis="y", length=0)
ax.set_xticks([]); ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False); ax.set_xlim(0, 1450)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=BLUE), plt.Rectangle((0, 0), 1, 1, color=NAVY)],
          labels=["Consumo adicional de los hogares", "Ahorro fiscal del Estado"], loc="upper center", bbox_to_anchor=(0.35, -0.02), ncol=2, frameon=False, fontsize=9.5)
fig.text(0.03, 0.94, f"Quitar la tarifa le cuesta a Cancillería USD {COSTO:.0f} millones; al país" + NL + f"le deja entre USD {miles(min(tot.values()))} y {miles(max(tot.values()))} millones cada año",
         fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.795, "Demanda potencial: 1,77 millones de personas con PPT que quieren quedarse.", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.03, "Fuente: Ibáñez et al. (2025), JEEA; DANE, GEIH 2025 y EPM VIII-2025; Migración Colombia (oct-2026); Cancillería.", fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr10_costo_vs_beneficio.png", dpi=250, facecolor="white"); plt.close(fig)
print("por persona: consumo", round(CONS_PP, 1), "fiscal", FISCAL_PP, "| con visa", {k: round(v) for k, v in con.items()}, "| extra", {k: round(v) for k, v in extra.items()},
      "| consumo M", {k: round(v, 1) for k, v in cons.items()}, "| fiscal M", {k: round(v, 1) for k, v in fis.items()}, "| total", {k: round(v, 1) for k, v in tot.items()})
