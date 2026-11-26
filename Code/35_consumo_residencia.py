"""Visa-R / 35: hipótesis: ¿cuánto subiría el consumo de los venezolanos regulares si tuvieran residencia permanente?
Base: consumo de los venezolanos regulares en 2025 = COP 23,9 billones (Code/34). Hoy gastan en Colombia 80 % de su ingreso:
ahorran 10 % y envían 10 % en remesas (supuestos de Code/27-34).
Canales (no hay un estudio que mida el efecto total de pasar de permiso temporal a residencia):
  - Ahorro por precaución: los migrantes temporales tienen una propensión a ahorrar 26 % mayor que los permanentes
    (De Arcangelis y Joxhe, 2015, IZA Journal of Migration, Reino Unido) -> ahorro de 10 % a 7,9 %.
  - Remesas: cambiar los planes de retorno cambia mucho las remesas (Dustmann y Mestres, 2010) -> hipótesis: de 10 % a 5 %.
  - Ingreso: la legalización permanente de IRCA (EE. UU., 1986) subió salarios entre 6 % y 13 % (Kossoudji y Cobb-Clark) -> se usa el piso, 6 %.
Escenarios: bajo = solo ahorro; central = ahorro + remesas; alto = ahorro + remesas + ingreso 6 %.
Salida: Outputs/Figures/pr22_consumo_residencia.png y Outputs/tables/t35_consumo_residencia.csv"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, INK, GRAY = "#1f3b5c", "#2a79d6", "#9fc0ea", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")
TRM = 4052.86

t34 = pd.read_csv(TAB / "t34_consumo_venezolanos.csv").set_index("concepto")["valor"]
C_REG = t34["  regulares (billones)"]
AH, REM = 0.10, 0.10
ah_perm = AH / 1.26
esc = {"Bajo": (1 - ah_perm - REM) / (1 - AH - REM),
       "Central": (1 - ah_perm - 0.05) / (1 - AH - REM),
       "Alto": (1 - ah_perm - 0.05) / (1 - AH - REM) * 1.06}
desc = {"Bajo": "Ahorran menos por precaución",
        "Central": "Ahorran menos y envían" + NL + "menos remesas",
        "Alto": "Además, su ingreso" + NL + "sube 6 %"}
d = pd.DataFrame({"escenario": list(esc), "aumento_pct": [100 * (f - 1) for f in esc.values()],
                  "consumo_regulares_billones": [C_REG * f for f in esc.values()], "consumo_adicional_billones": [C_REG * (f - 1) for f in esc.values()],
                  "consumo_adicional_USD_M": [C_REG * (f - 1) * 1e12 / TRM / 1e6 for f in esc.values()]}).round(2)
d.to_csv(TAB / "t35_consumo_residencia.csv", index=False); print("base", round(C_REG, 2)); print(d.to_string(index=False))

fig, ax = plt.subplots(figsize=(7.8, 4.9)); fig.subplots_adjust(left=0.05, right=0.97, top=0.72, bottom=0.2)
cols = [LBLUE, BLUE, NAVY]
for i, r in d.iterrows():
    ax.bar(i, r.consumo_adicional_billones, 0.58, color=cols[i])
    ax.text(i, r.consumo_adicional_billones + 0.08, f"+{pc(r.consumo_adicional_billones)} billones" + NL + f"(USD {miles(r.consumo_adicional_USD_M)} M)",
            ha="center", va="bottom", fontsize=11.5, fontweight="bold", color=NAVY)
    ax.text(i, -0.12, f"{r.escenario}: +{pc(r.aumento_pct)} %", ha="center", va="top", fontsize=11.5, fontweight="bold", color=INK)
    ax.text(i, -0.45, desc[r.escenario], ha="center", va="top", fontsize=10, color=GRAY)
ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(0, 4.9); ax.set_xlim(-0.55, 2.55)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
fig.text(0.03, 0.965, "Con residencia permanente, los venezolanos regulares podrían gastar" + NL +
         f"entre {pc(d.consumo_adicional_billones.min())} y {pc(d.consumo_adicional_billones.max())} billones de pesos más al año en Colombia",
         fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.835, f"Consumo adicional al año frente a hoy ({pc(C_REG)} billones). Hipótesis: con estabilidad, ahorran menos por precaución," + NL +
         "envían menos dinero fuera y mejoran su ingreso.", fontsize=10, ha="left", va="top", color=GRAY)
fig.text(0.03, 0.02, "Fuente: cálculos propios con DANE (cuentas nacionales y GEIH 2025); De Arcangelis y Joxhe (2015); Dustmann y Mestres (2010); Kossoudji y Cobb-Clark (IRCA).",
         fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr22_consumo_residencia.png", dpi=250, facecolor="white"); plt.close(fig)
