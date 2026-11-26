"""Visa-R / 27: hilo de tres gráficos.
 A. Si todo sigue igual (tarifa vigente): personas que quedan irregulares al vencer el PPT y su costo para el PIB.
 B. Migrante regular frente a irregular: ingreso laboral, consumo e impuestos y aportes por persona al año.
 C. Beneficios para la economía si se favorece la residencia (sin tarifa, 50 % y 80 % de conversión) frente a dejar la tarifa.
Supuestos comunes:
 - Demanda potencial: 1.770.136 personas con PPT que quieren quedarse; con la tarifa, 53.733 visas a may-2031 (tendencia 2024-2026).
 - Por persona (GEIH 2025): masa salarial COP 13,8 billones / 1,76 M venezolanos; 66 % con permiso (EPM). Con permiso: ingreso laboral +22 % y
   consumo +48 % (Ibáñez et al., 2025). Consumo = ingreso x (1 - 10 % ahorro - 10 % remesas).
 - Impuestos y aportes por persona: USD 498 (sin permiso) y USD 935 (con permiso) por hogar / 2,25 venezolanos por hogar (Ibáñez et al., 2025).
 - Valor agregado = ingreso laboral / 0,54 (participación del trabajo en el PIB, DANE). PIB 2025 = COP 1.852,7 billones. TRM 4.052,86.
Salidas: Outputs/Figures/pr12a_si_todo_sigue_igual.png, pr12b_regular_vs_irregular.png, pr12c_beneficios_residencia.png; Outputs/tables/t26_hilo.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, INK, GRAY, LGRAY = "#1f3b5c", "#2a79d6", "#9fc0ea", "#eb6a35", "#222222", "#6b6b6b", "#d9d9d9"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK,
                     "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False})
pc = lambda x, d=2: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")
FUENTE = "Fuente: Ibáñez et al. (2025), JEEA; DANE, GEIH 2025, EPM VIII-2025 y cuentas nacionales; Migración Colombia (oct-2026); Cancillería."

TRM, PIB, SH_LAB = 4052.86, 1852.7e12, 0.54
BASE, CON_TARIFA = 1_770_136, 53_733
COB, EF_ING, EF_CONS = 0.66, 0.22, 0.48
ing_prom = 13.8e12 / 1.76e6
ing_irr = ing_prom / ((1 - COB) + COB * (1 + EF_ING)); ing_reg = ing_irr * (1 + EF_ING)
cons_prom = ing_prom * 0.8
cons_irr = cons_prom / ((1 - COB) + COB * (1 + EF_CONS)); cons_reg = cons_irr * (1 + EF_CONS)
imp_irr, imp_reg = 498 / 2.25, 935.19 / 2.25                       # USD por persona al año
usd = lambda cop: cop / TRM
pib_pp = usd((ing_reg - ing_irr) / SH_LAB)                           # valor agregado adicional por persona regular (USD/año)
cons_pp = usd(cons_reg - cons_irr); fis_pp = 198.29
pib_usd = PIB / TRM

# ---- escenarios
irreg_tarifa = BASE - CON_TARIFA
esc = {"50 %": 0.5 * BASE - CON_TARIFA, "80 %": 0.8 * BASE - CON_TARIFA}     # personas más que siguen regulares frente a la tarifa
rows = [{"concepto": "Ingreso laboral por persona (USD/año)", "irregular": usd(ing_irr), "regular": usd(ing_reg)},
        {"concepto": "Consumo por persona (USD/año)", "irregular": usd(cons_irr), "regular": usd(cons_reg)},
        {"concepto": "Impuestos y aportes por persona (USD/año)", "irregular": imp_irr, "regular": imp_reg},
        {"concepto": "Costo PIB si todo sigue igual (USD M/año)", "irregular": irreg_tarifa * pib_pp / 1e6, "regular": 100 * irreg_tarifa * pib_pp / pib_usd}]
for k, p in esc.items():
    rows.append({"concepto": f"Beneficio {k}: PIB, consumo, fiscal (USD M/año)", "irregular": p * pib_pp / 1e6, "regular": p * cons_pp / 1e6, "extra": p * fis_pp / 1e6})
pd.DataFrame(rows).round(1).to_csv(TAB / "t26_hilo.csv", index=False)

# =============================================================== A. si todo sigue igual
perdida = irreg_tarifa * pib_pp
fig, ax = plt.subplots(figsize=(6.6, 4.1)); fig.subplots_adjust(left=0.05, right=0.97, top=0.74, bottom=0.2)
x = np.array([0, 1])
ax.bar(0, BASE / 1e6, 0.5, color=BLUE)
ax.bar(1, CON_TARIFA / 1e6, 0.5, color=BLUE); ax.bar(1, irreg_tarifa / 1e6, 0.5, bottom=CON_TARIFA / 1e6, color=ORANGE)
ax.text(0, BASE / 1e6 / 2, "1,77 M" + NL + "con estatus" + NL + "regular (PPT)", ha="center", va="center", fontsize=12, color="white", fontweight="bold")
ax.text(1, (CON_TARIFA + irreg_tarifa / 2) / 1e6, f"{pc(irreg_tarifa / 1e6)} M" + NL + "irregulares", ha="center", va="center", fontsize=12, color="white", fontweight="bold")
ax.annotate(f"{miles(CON_TARIFA / 1e3)} mil con visa", xy=(1.25, CON_TARIFA / 2e6), xytext=(1.4, 0.25), fontsize=10.5, color=BLUE, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8))
ax.set_xticks(x); ax.set_xticklabels(["Hoy (2026)", "Mayo de 2031" + NL + "con la tarifa vigente"], fontsize=11)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 2.05); ax.set_xlim(-0.5, 2.0)
ax.text(1.75, 1.5, "Costo para" + NL + "la economía:", ha="center", va="center", fontsize=10.5, color=GRAY)
ax.text(1.75, 1.02, f"−USD {pc(perdida / 1e9, 1)}" + NL + "mil millones" + NL + "de PIB al año", ha="center", va="center", fontsize=13, color=ORANGE, fontweight="bold")
ax.text(1.75, 0.6, f"({pc(100 * perdida / pib_usd)} % del PIB)", ha="center", va="center", fontsize=10.5, color=ORANGE)
fig.text(0.03, 0.94, "Si todo sigue igual, 1,72 millones de personas que quieren quedarse" + NL + "quedarían irregulares cuando venza el PPT",
         fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.785, "Personas con PPT que quieren quedarse en Colombia, hoy y en mayo de 2031 si se mantiene la tarifa de USD 464.", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.03, FUENTE, fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr12a_si_todo_sigue_igual.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== B. regular frente a irregular
conc = [("Ingreso laboral", usd(ing_irr), usd(ing_reg)), ("Consumo", usd(cons_irr), usd(cons_reg)), ("Impuestos y aportes", imp_irr, imp_reg)]
fig, ax = plt.subplots(figsize=(6.6, 4.1)); fig.subplots_adjust(left=0.05, right=0.97, top=0.74, bottom=0.2)
xx = np.arange(3); w = 0.36
for i, (lab, a, b) in enumerate(conc):
    ax.bar(i - w / 2, a, w, color=LGRAY); ax.bar(i + w / 2, b, w, color=BLUE)
    ax.text(i - w / 2, a + 30, f"USD {miles(a)}", ha="center", va="bottom", fontsize=10, color=GRAY)
    ax.text(i + w / 2, b + 30, f"USD {miles(b)}", ha="center", va="bottom", fontsize=10.5, color=BLUE, fontweight="bold")
    ax.text(i, max(a, b) + 230, f"+{100 * (b / a - 1):.0f} %", ha="center", va="bottom", fontsize=14, color=NAVY, fontweight="bold")
ax.set_xticks(xx); ax.set_xticklabels([c[0] for c in conc], fontsize=11.5)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 2550); ax.set_xlim(-0.6, 2.6)
ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=LGRAY), plt.Rectangle((0, 0), 1, 1, color=BLUE)], labels=["Migrante irregular", "Migrante regular"],
          loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False, fontsize=10)
fig.text(0.03, 0.94, "Un migrante regular gana 22 % más, consume 48 % más" + NL + "y paga 88 % más en impuestos y aportes",
         fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.785, "Por persona venezolana, en dólares al año.", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.03, FUENTE, fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr12b_regular_vs_irregular.png", dpi=250, facecolor="white"); plt.close(fig)

# =============================================================== C. beneficios si se favorece la residencia
ind = [("Más PIB", pib_pp, NAVY), ("Más consumo", cons_pp, BLUE), ("Ahorro fiscal", fis_pp, LBLUE)]
fig, ax = plt.subplots(figsize=(6.6, 4.1)); fig.subplots_adjust(left=0.05, right=0.97, top=0.74, bottom=0.2)
xx = np.arange(3); w = 0.36
for j, (k, p) in enumerate(esc.items()):
    vals = [p * pp / 1e6 for _, pp, _ in ind]
    off = (j - 0.5) * w
    ax.bar(xx + off, vals, w, color=[c for _, _, c in ind], alpha=0.55 if j == 0 else 1.0)
    for xi, v in zip(xx, vals):
        ax.text(xi + off, v + 15, f"{miles(v)}", ha="center", va="bottom", fontsize=10.5, fontweight="bold", color=INK)
        ax.text(xi + off, 12, k, ha="center", va="bottom", fontsize=9, color=INK if j == 0 else "white", fontweight="bold")
ax.set_xticks(xx); ax.set_xticklabels([f"{n}" + NL + "(USD millones al año)" for n, _, _ in ind], fontsize=11)
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0, 1050); ax.set_xlim(-0.6, 2.6)
pib50, pib80 = esc["50 %"] * pib_pp, esc["80 %"] * pib_pp
fig.text(0.03, 0.94, f"Con la Visa R sin costo, el PIB crece entre {pc(100 * pib50 / pib_usd)} % y {pc(100 * pib80 / pib_usd)} % al año," + NL +
         "a cambio de USD 21 millones de recaudo en cinco años", fontsize=13, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.785, "Beneficio anual frente a mantener la tarifa, si 50 % u 80 % de quienes quieren quedarse obtiene la visa.", fontsize=9.5, ha="left", color=ORANGE)
fig.text(0.03, 0.03, FUENTE, fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr12c_beneficios_residencia.png", dpi=250, facecolor="white"); plt.close(fig)
print("por persona USD: ingreso", round(usd(ing_irr)), round(usd(ing_reg)), "consumo", round(usd(cons_irr)), round(usd(cons_reg)), "imp", round(imp_irr), round(imp_reg),
      "| PIB pp", round(pib_pp), "| perdida tarifa USD M", round(perdida / 1e6), round(100 * perdida / pib_usd, 3),
      "| beneficio 50/80 PIB", round(pib50 / 1e6), round(pib80 / 1e6), round(100 * pib50 / pib_usd, 3), round(100 * pib80 / pib_usd, 3))

# =============================================================== D. toda la historia en una figura (dos paneles)
mil_ = lambda v: (pc(v / 1e6) + ' M') if v >= 1e6 else (miles(v / 1e3) + ' mil')
fig = plt.figure(figsize=(10.5, 4.9))
gl = fig.add_axes([0.04, 0.25, 0.36, 0.48]); gr = fig.add_axes([0.53, 0.25, 0.42, 0.48])
# panel izquierdo: por persona
for i, (lab, a, b) in enumerate(conc):
    gl.bar(i - 0.19, a, 0.36, color=LGRAY); gl.bar(i + 0.19, b, 0.36, color=BLUE)
    gl.text(i - 0.19, a + 30, miles(a), ha="center", va="bottom", fontsize=9, color=GRAY)
    gl.text(i + 0.19, b + 30, miles(b), ha="center", va="bottom", fontsize=9.5, color=BLUE, fontweight="bold")
    gl.text(i, max(a, b) + 260, f"+{100 * (b / a - 1):.0f} %", ha="center", va="bottom", fontsize=13, color=NAVY, fontweight="bold")
gl.set_xticks(range(3)); gl.set_xticklabels(["Ingreso" + NL + "laboral", "Consumo", "Impuestos" + NL + "y aportes"], fontsize=10.5)
gl.set_yticks([]); gl.spines["left"].set_visible(False); gl.set_ylim(0, 2600)
gl.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=LGRAY), plt.Rectangle((0, 0), 1, 1, color=BLUE)], labels=["Sin permiso", "Con permiso (PEP o PPT)"],
          loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, frameon=False, fontsize=9.5)
gl.set_title("1. Por qué importa: un migrante con permiso aporta más" + NL + "(USD por persona al año)", loc="left", fontsize=10.5, fontweight="bold", color=INK)
# panel derecho: PIB que aporta la regularidad de quienes tienen visa en 2031
sc = [("Se mantiene" + NL + "la tarifa", CON_TARIFA, ORANGE), ("Sin tarifa:" + NL + "50 % obtiene la visa", 0.5 * BASE, BLUE), ("Sin tarifa:" + NL + "80 % obtiene la visa", 0.8 * BASE, NAVY)]
xs_ = np.arange(3)
for xi, (lab, con_, col) in zip(xs_, sc):
    v = con_ * pib_pp / 1e6
    gr.bar(xi, v, 0.55, color=col)
    gr.text(xi, v + 25, f"USD {miles(v)} M", ha="center", va="bottom", fontsize=13, fontweight="bold", color=col)
    gr.text(xi, v + 175, f"{mil_(con_)} con visa", ha="center", va="bottom", fontsize=9.5, color=GRAY)
gr.set_xticks(xs_); gr.set_xticklabels([s_[0] for s_ in sc], fontsize=10.5)
gr.set_yticks([]); gr.spines["left"].set_visible(False); gr.set_ylim(0, 1300); gr.set_xlim(-0.55, 2.55)
gr.text(0, 560, "Además, Cancillería" + NL + "recibe USD 21 M" + NL + "en cinco años", ha="center", va="center", fontsize=9.5, color=ORANGE)
gr.set_title("2. Qué está en juego: PIB adicional que aporta cada año" + NL + "la regularidad de quienes tienen visa en 2031", loc="left", fontsize=10.5, fontweight="bold", color=INK)
fig.text(0.04, 0.95, "Mantener regulares a los venezolanos sostiene la economía: quitar la tarifa de la Visa R suma" + NL +
         f"entre USD {miles(esc['50 %'] * pib_pp / 1e6)} y {miles(esc['80 %'] * pib_pp / 1e6)} millones de PIB al año, a cambio de USD 21 millones de recaudo", fontsize=13.5, fontweight="bold", ha="left", va="top")
fig.text(0.04, 0.012, FUENTE, fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr13_historia_completa.png", dpi=250, facecolor="white"); plt.close(fig)
