"""Visa-R / 38: el gráfico principal: Visa R gratis desde 2027, lo que deja de recibir Cancillería frente a lo que gana el país, año a año.
Mismos insumos y fórmulas que Docs/Calculo_por_cada_dolar_Visa_R.xlsx (hoja Visa_cero_2027, escenario central):
  - 2027-2030: consumo adicional de los nuevos residentes (hipótesis de residencia: +8,8 % de consumo, USD 154 por persona al año).
  - Desde 2031: PIB que se conserva porque 1,36 millones siguen regulares cuando vence el PPT (USD 689 por persona al año; 7/12 de 2031).
  - Recaudo que deja de recibir Cancillería: visas que se habrían pagado con la tarifa x USD 464.
No se suman las dos medidas: hasta 2030 se muestra el consumo adicional y desde 2031 el PIB conservado (el mayor de los dos).
Salida: Outputs/Figures/pr23_visa_cero_2027.png"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#9fc0ea", "#eb6a35", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
miles = lambda x: f"{x:,.0f}".replace(",", ".")
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")

# ---- insumos (hoja Supuestos del Excel)
TRM, SH_LAB, COB, EF, EFC = 4052.86, 0.54, 0.66, 0.22, 0.48
ing_prom = 13.801e12 / 1_757_000
ing_irr = ing_prom / ((1 - COB) + COB * (1 + EF)); ing_reg = ing_irr * (1 + EF)
pib_pp = (ing_reg - ing_irr) / SH_LAB / TRM
cons_reg = ing_prom * 0.8 / ((1 - COB) + COB * (1 + EFC)) * (1 + EFC) / TRM
bono_pp = cons_reg * ((1 - 0.10 / 1.26 - 0.05) / 0.8 - 1)
QUIEREN, CONV, BASE = 1_770_136, 0.80, 8_440
YRS = np.arange(2027, 2037)
ELIG = {2027: 0.8118, 2028: 0.9634, 2029: 0.9956}
VT = {2027: 5_984, 2028: 7_450, 2029: 8_916, 2030: 10_382, 2031: 11_848}
t0 = np.array([CONV * QUIEREN * ELIG.get(y, 1.0) for y in YRS])
tt = BASE + np.cumsum([VT.get(y, 0) for y in YRS])
ad = t0 - tt
rec = np.array([VT.get(y, 0) * 464 / 1e6 for y in YRS])
frac = np.array([7 / 12 if y == 2031 else (1.0 if y > 2031 else 0.0) for y in YRS])
bono = ad * bono_pp / 1e6
pib = ad * pib_pp * frac / 1e6
gana = np.where(YRS < 2031, bono, np.maximum(pib, bono))
print("bono", bono.round(0), "pib", pib.round(0), "rec", rec.round(1), "total rec", rec.sum().round(1))

fig, ax = plt.subplots(figsize=(9.4, 5.4)); fig.subplots_adjust(left=0.04, right=0.98, top=0.7, bottom=0.23)
x = np.arange(len(YRS)); w = 0.62
cols = [LBLUE if y < 2031 else NAVY for y in YRS]
ax.bar(x, gana, w, color=cols, zorder=2)
ax.bar(x[rec > 0], rec[rec > 0], w, color=ORANGE, zorder=3)
for xi, g, r_ in zip(x, gana, rec):
    ax.text(xi, g + 18, miles(g), ha="center", va="bottom", fontsize=11, fontweight="bold", color=NAVY)
    if r_ > 0:
        ax.text(xi, -22, f"−{pc(r_)}", ha="center", va="top", fontsize=10, fontweight="bold", color=ORANGE)
ax.axhline(0, color="#555555", lw=0.6)
ax.set_xticks(x); ax.set_xticklabels([str(y) for y in YRS], fontsize=10.5)
ax.tick_params(axis="x", length=0, pad=24)
ax.set_yticks([]); ax.set_ylim(-60, 1300); ax.set_xlim(-0.6, len(YRS) - 0.4)
for s in ["top", "right", "left", "bottom"]:
    ax.spines[s].set_visible(False)
ax.axvline(3.5, color=GRAY, lw=0.8, ls=":", zorder=1)
ax.text(1.5, 560, "Desde 2027" + NL + "los nuevos residentes" + NL + "gastan más en Colombia", ha="center", va="center", fontsize=11, color=BLUE, fontweight="bold")
ax.text(3.65, 1270, "Desde 2031, cuando vence el PPT," + NL + f"{pc(ad[-1] / 1e6, 2)} millones siguen regulares y su aporte al PIB se conserva",
        ha="left", va="top", fontsize=11, color=NAVY, fontweight="bold")
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=LBLUE), plt.Rectangle((0, 0), 1, 1, color=NAVY), plt.Rectangle((0, 0), 1, 1, color=ORANGE)],
          labels=["Consumo adicional de los nuevos residentes", "PIB que se conserva", "Lo que deja de recibir Cancillería"],
          loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False, fontsize=10.5, handlelength=1.2)
fig.text(0.03, 0.965, "Visa R gratis desde 2027: Cancillería dejaría de recibir USD 21 millones" + NL +
         "en cinco años, y el país ganaría cientos de millones de dólares cada año", fontsize=15, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.825, f"Millones de dólares al año. Por cada dólar que deja de recibir Cancillería, el país gana {miles(np.floor(bono[:4].sum() / rec[:4].sum() / 10) * 10)} dólares"
         + NL + f"en consumo antes de 2031 y {miles(np.floor(pib.sum() / rec.sum() / 10) * 10)} dólares en PIB hasta 2036.", fontsize=10.5, ha="left", va="top", color=GRAY)
fig.text(0.03, 0.015, "Fuente: cálculos propios con DANE (GEIH 2025, cuentas nacionales), EPM VIII-2025, Migración Colombia y Cancillería; Ibáñez et al. (2025), JEEA."
         + " Escenario central: 80 % de quienes quieren quedarse obtiene la visa.", fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr23_visa_cero_2027.png", dpi=250, facecolor="white"); plt.close(fig)
