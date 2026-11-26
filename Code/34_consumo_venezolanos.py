"""Visa-R / 34: ¿qué parte del consumo de los hogares de Colombia (2025) corresponde a los migrantes venezolanos?
1. Consumo de los hogares 2025 = COP 1.356,9 billones (DANE, enfoque del gasto, Code/33).
2. Participación venezolana en el ingreso laboral, GEIH 2025 (12 meses): venezolanos = nacidos en Venezuela con nacionalidad
   solo extranjera (P3373S3 = 862, P3374 = 3). El archivo GEIH disponible no trae el módulo de otros ingresos (arriendos,
   pensiones, transferencias), así que se usa el ingreso laboral (INGLABO).
3. Los venezolanos envían 10 % de su ingreso como remesas: gastan en Colombia 90 % de lo que ganan, frente a 100 % del resto.
   Participación en el consumo = 0,9 s / (0,9 s + 1 - s).
4. Regulares frente a irregulares: 66 % tiene permiso (EPM VIII-2025) y con permiso consumen 48 % más (Ibáñez et al., 2025, JEEA).
Salida: Outputs/Figures/pr21_consumo_venezolanos.png y Outputs/tables/t34_consumo_venezolanos.csv"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, LORANGE, INK, GRAY, LGRAY = "#1f3b5c", "#2a79d6", "#9fc0ea", "#eb6a35", "#f2a27e", "#222222", "#6b6b6b", "#cfd5dd"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")

CONS = pd.read_csv(TAB / "t33_pib_gasto_2025.csv").set_index("componente").loc["Consumo de los hogares", "billones_COP"]
g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")
g = g[g.anio == 2025][["mes", "fex_c18", "pais_nac", "nacionalidad", "inglabo"]].apply(pd.to_numeric, errors="coerce")
g["w"] = g.fex_c18 / g.mes.nunique()
ven = (g.pais_nac == 862) & (g.nacionalidad == 3)
masa = lambda m: (g.inglabo.fillna(0) * g.w)[m].sum() * 12 / 1e12
M_TOT, M_VEN, POB_VEN = masa(g.index == g.index), masa(ven), g.w[ven].sum()
s_ing = M_VEN / M_TOT
s_cons = 0.9 * s_ing / (0.9 * s_ing + 1 - s_ing)
C_VEN = CONS * s_cons; C_RESTO = CONS - C_VEN
COB, EF = 0.66, 0.48
sh_reg = COB * (1 + EF) / ((1 - COB) + COB * (1 + EF))
C_REG, C_IRR = C_VEN * sh_reg, C_VEN * (1 - sh_reg)
t = pd.DataFrame({"concepto": ["Ingreso laboral total GEIH (billones)", "Ingreso laboral venezolanos GEIH (billones)", "Población venezolana GEIH (millones)",
                               "Participación en el ingreso laboral (%)", "Participación en el consumo (%)", "Consumo de los hogares DANE (billones)",
                               "Consumo venezolanos (billones)", "  regulares (billones)", "  irregulares (billones)", "Consumo resto de hogares (billones)"],
                  "valor": [M_TOT, M_VEN, POB_VEN / 1e6, 100 * s_ing, 100 * s_cons, CONS, C_VEN, C_REG, C_IRR, C_RESTO]}).round(3)
t.to_csv(TAB / "t34_consumo_venezolanos.csv", index=False); print(t.to_string(index=False))

fig = plt.figure(figsize=(9.0, 4.9))
a1 = fig.add_axes([0.04, 0.52, 0.92, 0.13]); a2 = fig.add_axes([0.62, 0.14, 0.34, 0.13])
a1.barh(0, C_RESTO, color=LGRAY); a1.barh(0, C_VEN, left=C_RESTO, color=BLUE)
a1.text(C_RESTO / 2, 0, f"Colombianos y otros hogares: {miles(C_RESTO)} billones ({pc(100 - 100 * s_cons)} %)", ha="center", va="center", fontsize=11.5, fontweight="bold", color=NAVY)
a1.text(CONS, 0.62, f"Venezolanos: {pc(C_VEN)} billones ({pc(100 * s_cons)} %)", ha="right", va="bottom", fontsize=11.5, fontweight="bold", color=BLUE)
a1.set_xlim(0, CONS); a1.set_ylim(-0.5, 0.5); a1.axis("off")
a2.barh(0, C_REG, color=BLUE); a2.barh(0, C_IRR, left=C_REG, color=LORANGE)
a2.text(C_REG / 2, 0, f"Regulares{NL}{pc(C_REG)} billones", ha="center", va="center", fontsize=10.5, fontweight="bold", color="white")
a2.text(C_REG + C_IRR / 2, 0, f"Irregulares{NL}{pc(C_IRR)}", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#7a2e0e")
a2.set_xlim(0, C_VEN); a2.set_ylim(-0.5, 0.5); a2.axis("off")
for xa, xb in [(C_RESTO, 0), (CONS, C_VEN)]:
    fig.add_artist(ConnectionPatch((xa, -0.5), (xb, 0.5), "data", "data", axesA=a1, axesB=a2, color=GRAY, lw=0.8, ls="--"))
fig.text(0.04, 0.24, f"Los venezolanos regulares hacen {pc(100 * sh_reg, 0)} % del consumo" + NL + "venezolano, aunque son 66 % de los" + NL +
         "venezolanos: con permiso consumen 48 % más.", fontsize=10.5, color=INK, va="center")
fig.text(0.03, 0.965, f"De los {miles(CONS)} billones de pesos que consumieron los hogares en Colombia en 2025," + NL +
         f"cerca de {miles(C_VEN)} billones los gastaron migrantes venezolanos", fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.835, "Consumo de los hogares 2025, billones de pesos corrientes.", fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.02, "Fuente: DANE, cuentas nacionales (enfoque del gasto, 2025pr) y GEIH 2025; EPM VIII-2025; Ibáñez et al. (2025), Journal of the European Economic Association.",
         fontsize=7.6, color=GRAY, ha="left")
fig.savefig(FIG / "pr21_consumo_venezolanos.png", dpi=250, facecolor="white"); plt.close(fig)
