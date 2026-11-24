"""Visa-R / 19: en qué año cumplen 5 años con PPT (requisito de la Visa R, art. 91) los venezolanos que hoy tienen PPT.
Fuente: EPM VIII-2025 (DANE), año y mes desde el que tiene el PPT (Ide14_2, Ide14_3), personas de nacionalidad venezolana con PPT (Ide14__2 = 1).
Escala: 1.975.752 venezolanos con PPT autorizado (Migración Colombia, tablero OM3, corte octubre de 2026).
Salidas: Outputs/Figures/pr6_anios_elegibilidad.png y Outputs/tables/t21_elegibilidad_por_anio.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, LNAVY, ACC, INK, GRAY = "#1f3b5c", "#9fb3c8", "#a4472f", "#222222", "#6b6b6b"
N_PPT = 1_975_752                        # PPT autorizado, Migración Colombia (tablero OM3), corte octubre 2026 (dato del equipo)
HOY = (2026, 11)                          # fecha de referencia para "ya cumplen"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "xtick.color": INK, "ytick.left": False, "ytick.labelleft": False})
miles = lambda x: f"{x:,.0f}".replace(",", ".")

P = pd.read_stata(ROOT / "Datos/Raw/EPM_VIII_2025/extraido_EPM8_Personas/EPM8_Personas.dta", convert_categoricals=False)
e = P[(P.Ide16 == 1) & (P.Ide14__2 == 1)].copy()
e["anio_eleg"] = e.Ide14_2 + 5
e["w"] = e.FEX_PER / e.FEX_PER.sum()
ya = float(e.w[(e.anio_eleg < HOY[0]) | ((e.anio_eleg == HOY[0]) & (e.Ide14_3 <= HOY[1]))].sum())

grupos = [("Antes de" + NL + "2026", e.anio_eleg < 2026), ("2026", e.anio_eleg == 2026), ("2027", e.anio_eleg == 2027),
          ("2028", e.anio_eleg == 2028), ("2029-2030", e.anio_eleg >= 2029)]
sh = np.array([float(e.w[m].sum()) for _, m in grupos]); n = sh * N_PPT; acum = np.cumsum(sh)
pd.DataFrame({"anio_en_que_cumple_5_anios": [g.replace(NL, " ") for g, _ in grupos], "pct_titulares": 100 * sh, "personas_escala_oficial": n.round(),
              "pct_acumulado": 100 * acum}).round(1).to_csv(TAB / "t21_elegibilidad_por_anio.csv", index=False)

fig, ax = plt.subplots(figsize=(6.4, 4.1)); fig.subplots_adjust(left=0.13, right=0.97, top=0.76, bottom=0.25)
x = np.arange(len(grupos))
ax.bar(x, n / 1e3, 0.62, color=[LNAVY, NAVY, NAVY, LNAVY, LNAVY])
for xi, v in zip(x, n):
    ax.text(xi, v / 1e3 + 18, f"{miles(v / 1e3)} mil", ha="center", va="bottom", fontsize=11, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels([g for g, _ in grupos], fontsize=10)
for xi, a in zip(x, acum):
    ax.text(xi, -205, f"{100 * a:.0f} %", ha="center", va="top", fontsize=9.5, color=GRAY)
ax.text(-0.5, -205, "Acumulado", ha="right", va="top", fontsize=9.5, color=GRAY)
ax.set_ylim(0, 1150); ax.set_xlim(-0.5, len(grupos) - 0.4)
ax.annotate("Pico: más de 1 millón" + NL + "de personas en 2027", xy=(2.33, 960), xytext=(3.0, 1000), fontsize=9.5, color=ACC, va="center",
            arrowprops=dict(arrowstyle="-", color=ACC, lw=0.8))
fig.text(0.03, 0.95, "¿En qué año cumplen 5 años con PPT los venezolanos que hoy lo tienen?", fontsize=12.5, fontweight="bold", ha="left")
fig.text(0.03, 0.82, "Personas que cumplen cada año el requisito de tiempo de la Visa R (5 años con PPT)." + NL +
         f"A noviembre de 2026 ya lo cumplen unas {miles(ya * N_PPT / 1e3)} mil ({100 * ya:.0f} %). El PPT vence el 30 de mayo de 2031.",
         fontsize=9.5, ha="left", color=INK)
fig.text(0.03, 0.02, f"Fuente: EPM VIII-2025 (DANE): año desde el que tiene el PPT + 5 años; escala de {miles(N_PPT)} PPT autorizados (Migración Colombia, oct. 2026)." + NL +
         "No cuenta el tiempo previo con PEP, por lo que subestima la elegibilidad temprana. «Antes de 2026»: reportan un año anterior a 2021 (probablemente su PEP).",
         fontsize=7, color=GRAY, ha="left")
fig.savefig(FIG / "pr6_anios_elegibilidad.png", dpi=250, facecolor="white"); plt.close(fig)
print(pd.read_csv(TAB / "t21_elegibilidad_por_anio.csv").to_string(), NL + "ya cumplen:", round(100 * ya, 1), miles(ya * N_PPT))
