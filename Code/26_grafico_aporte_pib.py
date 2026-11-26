"""Visa-R / 26: aporte al PIB del trabajo de los venezolanos, hoy y según la regularidad.
- Ingreso laboral anual de los venezolanos: COP 13,8 billones (GEIH 2025; incluye asalariados e independientes).
- De ingreso laboral a valor agregado: el ingreso laboral (remuneración de asalariados + ingreso mixto) es ≈ 54 % del PIB
  (DANE, cuentas nacionales por enfoque del ingreso: 53,5 % en 2019 y 55,5 % en 2020). Valor agregado = ingreso laboral / 0,54.
- PIB 2025: COP 1.852,7 billones (DANE, PIB departamental 2025 preliminar).
- Efecto del permiso sobre el ingreso laboral: +22 % (Ibáñez et al., 2025, JEEA, PEP). 66 % de los venezolanos tiene permiso (EPM VIII-2025).
  Con igual ocupación, la masa salarial de los irregulares es 0,34 / (0,34 + 0,66 x 1,22) = 29,7 % del total.
- Escenarios: si pierden la regularidad, la masa de los regulares cae a 1/1,22; con regularidad plena, la de los irregulares sube 22 %.
Salida: Outputs/Figures/pr11_aporte_pib.png y Outputs/tables/t25_aporte_pib.csv"""
from pathlib import Path
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
pc = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")

MASA, PIB, SH_LAB, TRM = 13.8e12, 1852.7e12, 0.54, 4052.86
COB, EF = 0.66, 0.22
sh_irr = (1 - COB) / ((1 - COB) + COB * (1 + EF))
m_irr, m_reg = MASA * sh_irr, MASA * (1 - sh_irr)
esc = {"Si pierden la regularidad": m_irr + m_reg / (1 + EF),
       "Hoy (66 % con permiso)": MASA,
       "Con regularidad plena": m_irr * (1 + EF) + m_reg}
va = {k: v / SH_LAB for k, v in esc.items()}
pct = {k: 100 * v / PIB for k, v in va.items()}
usd = {k: v / TRM / 1e9 for k, v in va.items()}
perd = va["Hoy (66 % con permiso)"] - va["Si pierden la regularidad"]; gan = va["Con regularidad plena"] - va["Hoy (66 % con permiso)"]
pd.DataFrame({"escenario": list(esc), "ingreso_laboral_billones_COP": [v / 1e12 for v in esc.values()], "valor_agregado_billones_COP": [v / 1e12 for v in va.values()],
              "pct_PIB_2025": list(pct.values()), "valor_agregado_miles_millones_USD": list(usd.values())}).round(3).to_csv(TAB / "t25_aporte_pib.csv", index=False)

fig, ax = plt.subplots(figsize=(6.4, 4.0)); fig.subplots_adjust(left=0.05, right=0.97, top=0.74, bottom=0.2)
x = range(3); cols = [ORANGE, BLUE, NAVY]
ax.bar(x, list(pct.values()), 0.55, color=cols)
for xi, k, c in zip(x, esc, cols):
    ax.text(xi, pct[k] + 0.03, f"{pc(pct[k])} % del PIB", ha="center", va="bottom", fontsize=13, fontweight="bold", color=c)
    dlt = {0: f"−{pc(100 * perd / PIB)} pp" + NL + "frente a hoy", 2: f"+{pc(100 * gan / PIB)} pp" + NL + "frente a hoy"}.get(xi, "")
    ax.text(xi, pct[k] / 2, f"USD {pc(usd[k], 1)}" + NL + "mil millones" + (NL + NL + dlt if dlt else ""), ha="center", va="center", fontsize=10.5, color="white")
ax.set_xticks(list(x)); ax.set_xticklabels([k.replace(" (", NL + "(") for k in esc], fontsize=10.5)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 1.75); ax.set_xlim(-0.55, 2.55)
fig.text(0.03, 0.94, f"Si pierden la regularidad, la economía pierde {pc(100 * perd / PIB)} % del PIB" + NL + f"cada año (≈ USD {miles(round(perd / TRM / 1e6, -2))} millones)",
         fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.785, "Valor agregado que genera el trabajo de los venezolanos en Colombia (PIB de 2025).", fontsize=10, ha="left", color=ORANGE)
fig.text(0.03, 0.03, "Fuente: DANE, GEIH 2025, EPM VIII-2025 y cuentas nacionales; Ibáñez et al. (2025), JEEA (ingreso laboral +22 % con permiso).",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr11_aporte_pib.png", dpi=250, facecolor="white"); plt.close(fig)
print({k: (round(pct[k], 3), round(usd[k], 2)) for k in esc}, "perdida %PIB", round(100 * perd / PIB, 3), "USD M", round(perd / TRM / 1e6),
      "ganancia %PIB", round(100 * gan / PIB, 3), "USD M", round(gan / TRM / 1e6))
