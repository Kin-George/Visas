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
ING_USD = ING / TRM
TASAS = [0.10, 0.20, 0.30]
meses = {t: FEE_USD / (t * ING_USD) for t in TASAS}
pd.DataFrame({"tasa_ahorro": TASAS, "ahorro_mensual_USD": [t * ING_USD for t in TASAS], "meses_persona": [meses[t] for t in TASAS],
              "meses_hogar_2_28_venezolanos": [meses[t] * VEN_HOG for t in TASAS]}).round(2).to_csv(TAB / "t23_meses_ahorro.csv", index=False)
FUENTE = "Fuente: GEIH-DANE 2026 (enero-agosto) y Cancillería (tarifa de la Visa R)."
AH = 0.10 * ING_USD

# =============================================================== propuesta A: cuánto lleva y cuánto le falta, mes a mes (ahorro del 10 %)
n = int(np.ceil(FEE_USD / AH)); mm_ = np.arange(1, n + 1); lleva = AH * mm_
fig, ax = plt.subplots(figsize=(6.6, 4.0)); fig.subplots_adjust(left=0.04, right=0.97, top=0.76, bottom=0.17)
for x_, l in zip(mm_, lleva):
    ok = l >= FEE_USD
    ax.bar(x_, min(l, FEE_USD) if not ok else l, 0.7, color=ACC if ok else NAVY)
    if not ok:
        ax.bar(x_, FEE_USD - l, 0.7, bottom=l, facecolor="white", edgecolor=LNAVY, hatch="////", linewidth=0.6)
        ax.text(x_, FEE_USD + 12, f"faltan" + NL + f"USD {miles(FEE_USD - l)}", ha="center", va="bottom", fontsize=8, color=GRAY)
        ax.text(x_, l - 10 if l > 60 else l + 8, f"USD {miles(l)}", ha="center", va="top" if l > 60 else "bottom", fontsize=7.8,
                color="white" if l > 60 else NAVY, fontweight="bold")
    else:
        ax.text(x_, l + 12, f"¡Alcanza!" + NL + f"USD {miles(l)}", ha="center", va="bottom", fontsize=9, color=ACC, fontweight="bold")
ax.axhline(FEE_USD, color=INK, lw=1.0, ls="--")
ax.text(n + 0.5, FEE_USD, "Visa R:" + NL + f"USD {FEE_USD}", ha="left", va="center", fontsize=9.5, color=INK, fontweight="bold", bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
ax.set_xticks(mm_); ax.set_xticklabels([f"Mes {k}" for k in mm_], fontsize=9); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.set_ylim(0, 620); ax.set_xlim(0.4, n + 1.5)
fig.text(0.03, 0.94, f"Ahorrando USD {miles(AH)} al mes, un venezolano tarda {n} meses en pagar la Visa R", fontsize=12.5, fontweight="bold", ha="left")
fig.text(0.03, 0.875, f"Ahorro acumulado y lo que le falta, si guarda el 10 % de su ingreso promedio (USD {miles(ING_USD)} al mes).", fontsize=10,
         ha="left", color=ACC)
fig.text(0.03, 0.03, FUENTE, fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr9a_meses_ahorro.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== propuesta B: calendario de ahorro, persona y hogar (10 %)
t = 0.10; mp, mh = meses[t], meses[t] * VEN_HOG; tot = int(np.ceil(mh))
fig, ax = plt.subplots(figsize=(6.6, 3.5)); fig.subplots_adjust(left=0.22, right=0.98, top=0.7, bottom=0.12)
filas = [("Un hogar" + NL + f"({pc(VEN_HOG)} venezolanos)", mh, f"Meta: USD {miles(FEE_USD * VEN_HOG)}", ACC),
         ("Una persona", mp, f"Meta: USD {FEE_USD}", NAVY)]
for row, (nom, mm, meta, col) in enumerate(filas):
    for k in range(tot):
        fill = min(max(mm - k, 0), 1)
        ax.add_patch(Rectangle((k + 0.06, row - 0.3), 0.88, 0.6, facecolor=LGRAY, edgecolor="none"))
        if fill > 0:
            ax.add_patch(Rectangle((k + 0.06, row - 0.3), 0.88 * fill, 0.6, facecolor=col, edgecolor="none"))
    ax.text(-0.4, row + 0.08, nom, ha="right", va="center", fontsize=10.5)
    ax.text(-0.4, row - 0.38 if row == 1 else row - 0.42, meta, ha="right", va="center", fontsize=9, color=GRAY)
    ax.text(tot + 0.4, row, f"{int(np.ceil(mm))} meses", ha="left", va="center", fontsize=13, fontweight="bold", color=col)
ax.set_xlim(0, tot + 4.6); ax.set_ylim(-0.6, 1.6); ax.axis("off")
fig.text(0.03, 0.93, "Reunir la tarifa de la Visa R toma casi 2 años a un hogar venezolano", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.86, f"Meses de ahorro si cada persona guarda USD {miles(AH)} al mes (10 % de su ingreso promedio de USD {miles(ING_USD)}).", fontsize=10,
         ha="left", color=ACC)
fig.text(0.03, 0.79, "Cada cuadro es un mes.", fontsize=9.5, ha="left", color=GRAY)
fig.text(0.03, 0.03, FUENTE, fontsize=7.8, color=GRAY, ha="left")
fig.savefig(FIG / "pr9b_ahorro_persona_hogar.png", dpi=250, facecolor="white"); plt.close(fig)
print("ingreso USD", round(ING_USD, 1), "ahorro mes", round(AH, 1), "meses", round(mp, 2), "hogar", round(mh, 1), "meta hogar", FEE_USD * VEN_HOG)
