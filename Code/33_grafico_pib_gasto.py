"""Visa-R / 33: PIB de Colombia 2025 por el enfoque del gasto.
Datos: DANE, PIB trimestral a precios corrientes, enfoque del gasto (anex-GastoCorriente-IIItrim2026.xlsx, Cuadro 1, datos originales,
actualizado 17-nov-2026). Suma de los cuatro trimestres de 2025pr. Miles de millones de pesos -> billones.
Salida: Outputs/Figures/pr20_pib_gasto_2025.png y Outputs/tables/t33_pib_gasto_2025.csv"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#9fc0ea", "#eb6a35", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")

d = pd.read_excel(ROOT / "Datos" / "DANE" / "anex-GastoCorriente-IIItrim2026.xlsx", "Cuadro 1", header=None)
anio = d.iloc[9].ffill()
c25 = [c for c in d.columns[2:] if str(anio[c]).startswith("2025")]
val = {str(d.loc[r, 0]).strip(): d.loc[r, c25].astype(float).sum() / 1e3 for r in range(12, 21)}     # billones de COP
comp = [("Consumo de" + NL + "los hogares", val["P.311 + P.313 + P.323"], BLUE),
        ("Gasto del" + NL + "gobierno", val["P.312 + P.322"], LBLUE),
        ("Inversión", val["P.5"], LBLUE),
        ("Exportaciones", val["P.6"], LBLUE),
        ("Importaciones" + NL + "(se restan)", -val["P.7"], ORANGE)]
PIB = val["B.1b"]
assert abs(sum(v for _, v, _ in comp) - PIB) < 0.5
pd.DataFrame({"componente": [k.replace(NL, " ") for k, _, _ in comp] + ["PIB"], "billones_COP": [v for _, v, _ in comp] + [PIB],
              "pct_PIB": [100 * v / PIB for _, v, _ in comp] + [100]}).round(2).to_csv(TAB / "t33_pib_gasto_2025.csv", index=False)

fig, ax = plt.subplots(figsize=(8.4, 4.9)); fig.subplots_adjust(left=0.04, right=0.98, top=0.76, bottom=0.14)
base = 0
for i, (k, v, c) in enumerate(comp):
    lo = base + min(v, 0)
    ax.bar(i, abs(v), 0.62, bottom=lo, color=c)
    ax.text(i, lo + abs(v) + 25, f"{'−' if v < 0 else ''}{miles(abs(v))}" + NL + f"({pc(100 * abs(v) / PIB, 0)} %)", ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=ORANGE if v < 0 else NAVY)
    ax.plot([i + 0.31, i + 0.69], [base + v, base + v], color="#999999", lw=0.7, ls=":")
    base += v
ax.bar(5, PIB, 0.62, color=NAVY)
ax.text(5, PIB + 25, f"{miles(PIB)}" + NL + "(100 %)", ha="center", va="bottom", fontsize=11, fontweight="bold", color=NAVY)
ax.set_xticks(range(6)); ax.set_xticklabels([k for k, _, _ in comp] + ["PIB 2025"], fontsize=10.5)
ax.get_xticklabels()[-1].set_fontweight("bold")
ax.set_yticks([]); ax.set_ylim(0, 2650); ax.set_xlim(-0.55, 5.55)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
fig.text(0.03, 0.965, f"De los {miles(PIB)} billones de pesos del PIB de Colombia en 2025," + NL +
         f"{pc(100 * comp[0][1] / PIB, 0)} % es consumo de los hogares", fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.835, "PIB por el enfoque del gasto, billones de pesos corrientes. Entre paréntesis, porcentaje del PIB.", fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.02, "Fuente: DANE, cuentas nacionales trimestrales, PIB a precios corrientes por el enfoque del gasto (2025 preliminar).",
         fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr20_pib_gasto_2025.png", dpi=250, facecolor="white"); plt.close(fig)
print({k.replace(NL, " "): round(v, 1) for k, v, _ in comp}, "PIB", round(PIB, 1))
