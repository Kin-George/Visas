"""Visa-R / 22: cuánto tiempo de ahorro necesita un venezolano para pagar la Visa R (USD 464).
Ingreso: ingreso laboral mensual promedio de los ocupados venezolanos (nacidos en Venezuela sin nacionalidad colombiana) con ingreso positivo, GEIH 2026 (enero-agosto).
Tarifa: USD 464 (USD 56 estudio + USD 408 visa) a TRM de COP 3.235. Tasas de ahorro: supuestos (10 %, 20 %, 30 % del ingreso).
Salidas: Outputs/Figures/pr9a_meses_ahorro.png, pr9b_ahorro_persona_hogar.png; Outputs/tables/t23_meses_ahorro.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, LNAVY, ACC, INK, GRAY, LGRAY = "#1f3b5c", "#9fb3c8", "#a4472f", "#222222", "#6b6b6b", "#e3e3e3"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
miles = lambda x: f"{x:,.0f}".replace(",", ".")
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
TRM, FEE_USD, VEN_HOG = 3235.0, 464, 2.28
FEE = FEE_USD * TRM

g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")
g = g[g.anio == 2026][["mes", "fex_c18", "pais_nac", "nacionalidad", "oci", "inglabo"]].apply(pd.to_numeric, errors="coerce")
g["w"] = g.fex_c18 / g.mes.nunique()
v = g[(g.pais_nac == 862) & (g.nacionalidad == 3) & (g.oci == 1) & (g.inglabo > 0)]
ING = float(np.average(v.inglabo, weights=v.w))
TASAS = [0.10, 0.20, 0.30]
meses = {t: FEE / (t * ING) for t in TASAS}
pd.DataFrame({"tasa_ahorro": TASAS, "ahorro_mensual_COP": [t * ING for t in TASAS], "meses_persona": [meses[t] for t in TASAS],
              "meses_hogar_2_28_venezolanos": [meses[t] * VEN_HOG for t in TASAS]}).round(2).to_csv(TAB / "t23_meses_ahorro.csv", index=False)
FUENTE = "Fuente: GEIH-DANE 2026 (enero-agosto) y Cancillería (tarifa de la Visa R)."

# =============================================================== propuesta A: meses de ahorro según cuánto ahorre
fig, ax = plt.subplots(figsize=(6.4, 3.9)); fig.subplots_adjust(left=0.05, right=0.97, top=0.76, bottom=0.2)
x = np.arange(3); m = [meses[t] for t in TASAS]
ax.bar(x, m, 0.55, color=[ACC, NAVY, NAVY])
for xi, mm in zip(x, m):
    ax.text(xi, mm + 0.2, f"{pc(mm)} meses", ha="center", va="bottom", fontsize=13, fontweight="bold", color=ACC if xi == 0 else INK)
ax.set_xticks(x); ax.set_xticklabels([f"Ahorra el {int(t * 100)} %" + NL + f"(COP {miles(t * ING / 1e3)} mil al mes)" for t in TASAS], fontsize=10.5)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 11.5); ax.set_xlim(-0.5, 2.5)
fig.text(0.03, 0.94, f"Un venezolano necesita más de {int(meses[0.10])} meses de ahorro para pagar la Visa R", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.875, f"Si ahorra el 10 % de su ingreso promedio (COP {pc(ING / 1e6, 2)} millones al mes). La visa cuesta COP {pc(FEE / 1e6, 2)} millones.",
         fontsize=10, ha="left", color=ACC)
fig.text(0.03, 0.03, FUENTE, fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr9a_meses_ahorro.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== propuesta B: calendario de ahorro, persona y hogar (10 %)
t = 0.10; mp, mh = meses[t], meses[t] * VEN_HOG; tot = int(np.ceil(mh))
fig, ax = plt.subplots(figsize=(6.6, 3.4)); fig.subplots_adjust(left=0.2, right=0.98, top=0.7, bottom=0.14)
for row, (nom, mm) in enumerate([("Un hogar" + NL + f"({pc(VEN_HOG)} venezolanos)", mh), ("Una persona", mp)]):
    for k in range(tot):
        fill = min(max(mm - k, 0), 1)
        ax.add_patch(Rectangle((k + 0.06, row - 0.32), 0.88, 0.64, facecolor=LGRAY, edgecolor="none"))
        if fill > 0:
            ax.add_patch(Rectangle((k + 0.06, row - 0.32), 0.88 * fill, 0.64, facecolor=ACC if row == 0 else NAVY, edgecolor="none"))
    ax.text(-0.4, row, nom, ha="right", va="center", fontsize=10.5)
    ax.text(tot + 0.4, row, f"{pc(mm, 0)} meses", ha="left", va="center", fontsize=13, fontweight="bold", color=ACC if row == 0 else NAVY)
ax.set_xlim(0, tot + 4.6); ax.set_ylim(-0.6, 1.6); ax.axis("off")
fig.text(0.03, 0.93, "Reunir la tarifa de la Visa R toma casi 2 años a un hogar venezolano", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.86, f"Meses de ahorro si cada persona guarda el 10 % de su ingreso promedio (COP {pc(ING / 1e6, 2)} millones al mes).", fontsize=10,
         ha="left", color=ACC)
fig.text(0.03, 0.79, "Cada cuadro es un mes.", fontsize=9.5, ha="left", color=GRAY)
fig.text(0.03, 0.03, FUENTE, fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr9b_ahorro_persona_hogar.png", dpi=250, facecolor="white"); plt.close(fig)
print("ingreso promedio", round(ING), "tarifa COP", FEE, "pct", round(100 * FEE / ING, 1), {k: round(v_, 1) for k, v_ in meses.items()}, "hogar 10%", round(mh, 1))
