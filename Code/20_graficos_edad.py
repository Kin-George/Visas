"""Visa-R / 20: estructura por edad de venezolanos y colombianos (bono demográfico).
Fuente: GEIH 2026 (enero-agosto). Venezolanos: nacidos en Venezuela sin nacionalidad colombiana; colombianos: nacidos en Colombia.
Salidas: Outputs/Figures/pr7a_edad_de_trabajar.png, pr7b_piramide_edad.png; Outputs/tables/t22_estructura_edad.csv, t22b_piramide.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, LNAVY, ACC, INK, GRAY, LGRAY = "#1f3b5c", "#9fb3c8", "#a4472f", "#222222", "#6b6b6b", "#c9c9c9"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "xtick.color": INK, "ytick.color": INK})
FUENTE = "Fuente: GEIH-DANE 2026 (enero-agosto)."

g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")
g = g[g.anio == 2026][["mes", "fex_c18", "edad", "sexo", "pais_nac", "nacionalidad"]].apply(pd.to_numeric, errors="coerce")
g["w"] = g.fex_c18 / g.mes.nunique()
g["grp"] = np.select([(g.pais_nac == 862) & (g.nacionalidad == 3), g.pais_nac.isna()], ["Venezolanos", "Colombianos"], "otro")
g = g[g.grp != "otro"]


def wmed(x, w):
    o = np.argsort(x.to_numpy()); c = np.cumsum(w.to_numpy()[o]) / w.sum()
    return float(x.to_numpy()[o][np.searchsorted(c, 0.5)])


est = {}
for k, s in g.groupby("grp"):
    b = pd.cut(s.edad, [-1, 14, 64, 200], labels=["Menores de 15", "15 a 64 (edad de trabajar)", "65 y más"])
    sh = s.groupby(b, observed=True).w.sum() / s.w.sum() * 100
    est[k] = {**sh.to_dict(), "edad_mediana": wmed(s.edad, s.w), "dependientes_por_100_en_edad_de_trabajar": 100 * (100 - sh.iloc[1]) / sh.iloc[1]}
est = pd.DataFrame(est).T.round(1); est.to_csv(TAB / "t22_estructura_edad.csv")
V, C = est.loc["Venezolanos"], est.loc["Colombianos"]

# =============================================================== propuesta A: de cada 100 personas
fig, ax = plt.subplots(figsize=(6.4, 3.2)); fig.subplots_adjust(left=0.2, right=0.97, top=0.7, bottom=0.2)
cats = ["Menores de 15", "15 a 64 (edad de trabajar)", "65 y más"]; cols = [LGRAY, NAVY, GRAY]
for y, (nom, r) in enumerate([("Colombianos", C), ("Venezolanos", V)]):
    left = 0
    for c_, col in zip(cats, cols):
        v = r[c_]; ax.barh(y, v, 0.58, left=left, color=col if not (nom == "Venezolanos" and col == NAVY) else ACC)
        if v > 6:
            ax.text(left + v / 2, y, f"{v:.0f}", ha="center", va="center", fontsize=13, fontweight="bold", color="white" if col != LGRAY else INK)
        left += v
ax.set_yticks([0, 1]); ax.set_yticklabels([f"Colombianos{NL}(edad mediana: {C.edad_mediana:.0f})", f"Venezolanos{NL}(edad mediana: {V.edad_mediana:.0f})"], fontsize=10.5)
ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False); ax.set_xticks([]); ax.set_xlim(0, 100)
for x_, t in [(C.iloc[0] / 2, "Menores de 15"), (C.iloc[0] + C.iloc[1] / 2, "15 a 64 años (edad de trabajar)"), (100 - C.iloc[2] / 2, "65 y más")]:
    ax.text(x_, 1.52, t, ha="center", va="bottom", fontsize=9, color=GRAY)
fig.text(0.03, 0.93, "Los venezolanos son una población más joven y en edad de trabajar", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.85, f"De cada 100 venezolanos, {V.iloc[1]:.0f} tienen entre 15 y 64 años; entre los colombianos, {C.iloc[1]:.0f}.", fontsize=11, ha="left", color=ACC)
fig.text(0.03, 0.04, FUENTE, fontsize=8, color=GRAY, ha="left")
fig.savefig(FIG / "pr7a_edad_de_trabajar.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== propuesta B: pirámide comparada (% de cada población)
edges = list(range(0, 80, 5)) + [200]
labs = [f"{a}-{a + 4}" for a in range(0, 75, 5)] + ["75+"]
pir = {}
for k, s in g.groupby("grp"):
    b = pd.cut(s.edad, [e - 0.5 for e in edges], labels=labs)
    t = s.groupby([b, s.sexo], observed=False).w.sum() / s.w.sum() * 100
    pir[k] = t.unstack()
rows = []
for k in pir:
    for a in labs:
        rows.append({"grupo": k, "edad": a, "hombres_pct": pir[k].loc[a, 1], "mujeres_pct": pir[k].loc[a, 2]})
pd.DataFrame(rows).round(2).to_csv(TAB / "t22b_piramide.csv", index=False)
fig, ax = plt.subplots(figsize=(6.4, 4.6)); fig.subplots_adjust(left=0.12, right=0.97, top=0.78, bottom=0.14)
y = np.arange(len(labs))
vh, vm = pir["Venezolanos"][1].reindex(labs).to_numpy(), pir["Venezolanos"][2].reindex(labs).to_numpy()
ch, cm = pir["Colombianos"][1].reindex(labs).to_numpy(), pir["Colombianos"][2].reindex(labs).to_numpy()
wa = (y >= 3) & (y <= 12)                                          # 15-64
ax.barh(y, -vh, 0.85, color=np.where(wa, ACC, LNAVY)); ax.barh(y, vm, 0.85, color=np.where(wa, ACC, LNAVY))
ed = np.r_[y - 0.5, y[-1] + 0.5]
ax.stairs(-ch, ed, orientation="horizontal", baseline=None, color=INK, lw=1.3)
ax.stairs(cm, ed, orientation="horizontal", baseline=None, color=INK, lw=1.3)
ax.axvline(0, color="white", lw=1.5)
ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=8.5); ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
m = 7.5; ax.set_xlim(-m, m); ax.set_xticks([-6, -4, -2, 0, 2, 4, 6]); ax.set_xticklabels(["6 %", "4 %", "2 %", "0", "2 %", "4 %", "6 %"], fontsize=8.5)
ax.text(-m + 0.2, len(labs) - 0.3, "Hombres", fontsize=10, color=GRAY, va="top"); ax.text(m - 0.2, len(labs) - 0.3, "Mujeres", fontsize=10, color=GRAY, ha="right", va="top")
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=ACC), plt.Rectangle((0, 0), 1, 1, color=LNAVY), plt.Line2D([0], [0], color=INK, lw=1.2)],
          labels=["Venezolanos de 15 a 64 años", "Venezolanos de otras edades", "Colombianos"], loc="lower center", frameon=False, fontsize=9, ncol=3,
          bbox_to_anchor=(0.45, 1.0), handlelength=1.4, columnspacing=1.2)
fig.text(0.03, 0.94, "Pirámide de edad: venezolanos frente a colombianos", fontsize=13, fontweight="bold", ha="left")
fig.text(0.03, 0.88, "Los venezolanos se concentran entre los 20 y los 40 años; tienen muy pocos mayores de 65.", fontsize=11, ha="left", color=ACC)
fig.text(0.03, 0.02, FUENTE, fontsize=8, color=GRAY, ha="left")
ax.annotate("Los hijos nacidos en Colombia" + NL + "se cuentan como colombianos", xy=(1.1, 0), xytext=(3.2, -0.2), fontsize=8, color=GRAY, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.7))
ax.set_xlabel("Porcentaje de cada población", fontsize=9, color=GRAY)
fig.savefig(FIG / "pr7b_piramide_edad.png", dpi=250, facecolor="white"); plt.close(fig)
print(est.to_string())
