"""Visa-R / 32: tres escenarios para 2031, cuando vence el PPT, sobre los 1.990.196 venezolanos que hoy son regulares.
  1. Todos pasan a ser irregulares, salvo los 14.444 que ya tienen cédula de extranjería (residentes).
  2. Se mantiene la tarifa de USD 464: 53.733 visas a mayo de 2031 (tendencia lineal, Cancillería) + 14.444 residentes.
  3. Tarifa cero: 80 % de los 1.770.136 titulares de PPT que quieren quedarse (89,6 %, EPM) obtiene la visa + 14.444 residentes.
     80 %: afiliación a salud de los venezolanos con 5 años o más en el país (81 %, GEIH).
Por persona al año (Code/31): PIB USD 3.817 regular vs 3.128 irregular; costo fiscal neto USD 1.056 vs 610 por hogar
(Ibáñez et al., 2025, cuadro 7) / 2,25 venezolanos por hogar. Recaudo de la tarifa: 44.580 visas 2027-2031 x USD 464 / 5.
No incluye el efecto adicional de la estabilidad de una visa de residencia (supuesto conservador: la visa vale lo mismo que el PPT).
Salida: Outputs/Figures/pr19_tres_escenarios.png y Outputs/tables/t32_tres_escenarios.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, ORANGE, LORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#eb6a35", "#f2a27e", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
miles = lambda x: f"{x:,.0f}".replace(",", ".")
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")

TRM, SH_LAB, COB = 4052.86, 0.54, 0.66
REG, RES = 1_990_196, 14_444
ing_prom = 13.8e12 / 1.76e6
ing_irr = ing_prom / ((1 - COB) + COB * 1.22); ing_reg = ing_irr * 1.22
pib_r, pib_i = ing_reg / SH_LAB / TRM, ing_irr / SH_LAB / TRM
fis_r, fis_i = 610 / 2.25, 1056 / 2.25
TARIFA = 44_580 * 464 / 5 / 1e6

esc = {"1. Todos pierden" + NL + "el estatus regular": RES,
       "2. Se mantiene" + NL + "la tarifa de USD 464": 53_733 + RES,
       "3. Tarifa cero: 80 %" + NL + "obtiene la visa": round(0.8 * 1_770_136) + RES}
pib = lambda r: (r * pib_r + (REG - r) * pib_i) / 1e6
fis = lambda r: (r * fis_r + (REG - r) * fis_i) / 1e6
hoy_pib, hoy_fis = pib(REG), fis(REG)
d = pd.DataFrame({"escenario": [k.replace(NL, " ") for k in esc], "regulares_2031": list(esc.values()),
                  "PIB_USD_M": [pib(r) for r in esc.values()], "perdida_PIB_vs_hoy_USD_M": [hoy_pib - pib(r) for r in esc.values()],
                  "costo_fiscal_neto_USD_M": [fis(r) for r in esc.values()], "costo_fiscal_extra_vs_hoy_USD_M": [fis(r) - hoy_fis for r in esc.values()],
                  "recaudo_tarifa_USD_M": [0, TARIFA, 0]}).round(1)
d.to_csv(TAB / "t32_tres_escenarios.csv", index=False)
print(d.to_string()); print("hoy PIB", round(hoy_pib), "hoy fiscal", round(hoy_fis))

cols = [ORANGE, LORANGE, BLUE]
panels = [("Siguen con estatus regular" + NL + "en 2031", d["regulares_2031"] / 1e3, lambda v: f"{pc(v / 1e3, 2)} millones" if v >= 1e3 else f"{miles(v)} mil", 1.35 * REG / 1e3),
          ("PIB que se pierde cada año" + NL + "frente a hoy (USD millones)", d["perdida_PIB_vs_hoy_USD_M"], lambda v: f"−{miles(v)}", 1.35 * d["perdida_PIB_vs_hoy_USD_M"].max()),
          ("Costo fiscal extra para el Estado" + NL + "cada año (USD millones)", d["costo_fiscal_extra_vs_hoy_USD_M"], lambda v: f"+{miles(v)}", 1.35 * d["costo_fiscal_extra_vs_hoy_USD_M"].max())]
fig = plt.figure(figsize=(10.4, 4.9))
y = -np.arange(3)
for j, (tit, vals, fmt, xmax) in enumerate(panels):
    ax = fig.add_axes([0.2 + j * 0.27, 0.13, 0.22, 0.56])
    ax.barh(y, vals, 0.62, color=cols)
    for yi, v, c in zip(y, vals, cols):
        ax.text(v + xmax * 0.02, yi, fmt(v), va="center", fontsize=12, fontweight="bold", color=NAVY if c == BLUE else ORANGE)
    ax.set_xlim(0, xmax); ax.set_ylim(-2.5, 0.5); ax.set_xticks([])
    ax.set_yticks(y); ax.set_yticklabels([k for k in esc] if j == 0 else [], fontsize=10.5)
    ax.tick_params(axis="y", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.axvline(0, color="#555555", lw=0.6)
    ax.set_title(tit, loc="left", fontsize=10.5, fontweight="bold", color=INK)
    if j == 0:
        ax.text(0, 0.62 + 0.5, "", fontsize=1)
fig.text(0.2, 0.065, f"Hoy: {pc(REG / 1e6, 2)} millones con estatus regular, que aportan USD {miles(hoy_pib)} millones de PIB al año." +
         f" Con la tarifa, Cancillería recauda USD {pc(TARIFA)} millones al año.", fontsize=9.5, color=GRAY, ha="left")
fig.text(0.03, 0.965, "Mantener la tarifa da casi el mismo resultado que si todos perdieran su estatus regular;" + NL +
         f"con tarifa cero se evita {pc(100 * (1 - d.iloc[2, 3] / d.iloc[0, 3]), 0)} % de la pérdida de PIB y del costo fiscal", fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.83, "Qué pasa en 2031, cuando vence el PPT, con los 2 millones de venezolanos que hoy son regulares.", fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.015, "Fuente: Ibáñez et al. (2025), Journal of the European Economic Association; DANE, GEIH 2025, EPM VIII-2025 y cuentas nacionales; Migración Colombia (2026); Cancillería.",
         fontsize=7.6, color=GRAY, ha="left")
fig.savefig(FIG / "pr19_tres_escenarios.png", dpi=250, facecolor="white"); plt.close(fig)
