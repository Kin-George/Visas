"""Visa-R / 36: pr21 + hipótesis de residencia permanente (pr22) en un solo gráfico.
Entradas: Outputs/tables/t34_consumo_venezolanos.csv (Code/34) y t35_consumo_residencia.csv (Code/35, escenario central y rango).
Salida: Outputs/Figures/pr21b_consumo_venezolanos_residencia.png"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LORANGE, INK, GRAY, LGRAY, GREEN = "#1f3b5c", "#2a79d6", "#f2a27e", "#222222", "#6b6b6b", "#cfd5dd", "#1f3b5c"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK, "hatch.color": "white"})
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")

t = pd.read_csv(TAB / "t34_consumo_venezolanos.csv").set_index("concepto")["valor"]
r = pd.read_csv(TAB / "t35_consumo_residencia.csv").set_index("escenario")
CONS, C_VEN, C_REG, C_IRR = t["Consumo de los hogares DANE (billones)"], t["Consumo venezolanos (billones)"], t["  regulares (billones)"], t["  irregulares (billones)"]
C_RESTO = CONS - C_VEN
EXTRA, LO, HI, PCT = r.loc["Central", "consumo_adicional_billones"], r.loc["Bajo", "consumo_adicional_billones"], r.loc["Alto", "consumo_adicional_billones"], r.loc["Central", "aumento_pct"]

fig = plt.figure(figsize=(9.0, 5.6))
a1 = fig.add_axes([0.04, 0.6, 0.92, 0.11])
a1.barh(0, C_RESTO, color=LGRAY); a1.barh(0, C_VEN, left=C_RESTO, color=BLUE)
a1.text(C_RESTO / 2, 0, f"Colombianos y otros hogares: {miles(C_RESTO)} billones ({pc(100 * C_RESTO / CONS)} %)", ha="center", va="center", fontsize=11.5, fontweight="bold", color=NAVY)
a1.text(CONS, 0.62, f"Venezolanos: {pc(C_VEN)} billones ({pc(100 * C_VEN / CONS)} %)", ha="right", va="bottom", fontsize=11.5, fontweight="bold", color=BLUE)
a1.set_xlim(0, CONS); a1.set_ylim(-0.5, 0.5); a1.axis("off")

XMAX = C_VEN + EXTRA
a2 = fig.add_axes([0.5, 0.12, 0.46, 0.3])
yh, yr = 1, 0
a2.barh(yh, C_REG, 0.42, color=BLUE); a2.barh(yh, C_IRR, 0.42, left=C_REG, color=LORANGE)
a2.barh(yr, C_REG, 0.42, color=BLUE); a2.barh(yr, EXTRA, 0.42, left=C_REG, color=NAVY, hatch="///", edgecolor="white", lw=0)
a2.barh(yr, C_IRR, 0.42, left=C_REG + EXTRA, color=LORANGE)
for y in (yh, yr):
    a2.text(C_REG / 2, y, f"Regulares{NL}{pc(C_REG)}", ha="center", va="center", fontsize=10.5, fontweight="bold", color="white")
    a2.text(XMAX if y == yr else C_VEN, y, "", fontsize=1)
a2.text(C_REG + C_IRR / 2, yh, f"Irregulares{NL}{pc(C_IRR)}", ha="center", va="center", fontsize=10, fontweight="bold", color="#7a2e0e")
a2.text(C_REG + EXTRA + C_IRR / 2, yr, f"Irregulares{NL}{pc(C_IRR)}", ha="center", va="center", fontsize=10, fontweight="bold", color="#7a2e0e")
a2.annotate(f"+{pc(EXTRA)} billones (+{pc(PCT, 0)} %)", xy=(C_REG + EXTRA / 2, yr - 0.22), xytext=(C_REG + EXTRA / 2, yr - 0.55), ha="center", va="top",
            fontsize=11, fontweight="bold", color=NAVY, arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9))
a2.text(-0.4, yh, "Hoy", ha="right", va="center", fontsize=11, fontweight="bold", color=INK)
a2.text(-0.4, yr, "Con residencia" + NL + "permanente", ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
a2.set_xlim(0, XMAX); a2.set_ylim(-0.95, 1.4); a2.axis("off")
for xa, xb in [(C_RESTO, 0), (CONS, C_VEN)]:
    fig.add_artist(ConnectionPatch((xa, -0.5), (xb, yh + 0.21), "data", "data", axesA=a1, axesB=a2, color=GRAY, lw=0.8, ls="--"))

fig.text(0.04, 0.3, "Hoy, los regulares hacen 74 % del consumo" + NL + "venezolano: con permiso consumen 48 % más." + NL + NL +
         "Hipótesis: con residencia permanente," + NL + "ahorran menos por precaución y envían" + NL + f"menos remesas. Rango: +{pc(LO)} a +{pc(HI)} billones.",
         fontsize=10.5, color=INK, va="center")
fig.text(0.03, 0.965, f"Los venezolanos gastaron cerca de {miles(C_VEN)} billones de pesos en Colombia en 2025;" + NL +
         f"con residencia permanente, los regulares podrían gastar {pc(EXTRA)} billones más al año", fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.855, "Consumo de los hogares 2025, billones de pesos corrientes.", fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.02, "Fuente: DANE, cuentas nacionales (2025pr) y GEIH 2025; EPM VIII-2025; Ibáñez et al. (2025), JEEA; De Arcangelis y Joxhe (2015); Dustmann y Mestres (2010).",
         fontsize=7.5, color=GRAY, ha="left")
fig.savefig(FIG / "pr21b_consumo_venezolanos_residencia.png", dpi=250, facecolor="white"); plt.close(fig)
