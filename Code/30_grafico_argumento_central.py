"""Visa-R / 30: el argumento central en un gráfico (áreas proporcionales).
- Lo que la tarifa le deja a Cancillería al año: 44.580 visas 2027-2031 x USD 464 / 5 = USD 4,1 M (tendencia de las visas; Cancillería).
- Lo que aportan de más a la economía por ser regulares: 1.990.196 regulares x USD 688 de PIB adicional por persona al año
  (ingreso laboral +22 % con permiso, Ibáñez et al., 2025, JEEA; ingreso GEIH 2025 / 0,54, participación del trabajo en el PIB, DANE) = USD 1.370 M.
- Lo que aportan en total al PIB: 1.990.196 x USD 3.817 = USD 7.596 M (1,66 % del PIB 2025).
Áreas proporcionales a los valores. Salida: Outputs/Figures/pr17_argumento_central.png"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#cfe0f5", "#eb6a35", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
miles = lambda x: f"{x:,.0f}".replace(",", ".")
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")

TRM, SH_LAB, REG = 4052.86, 0.54, 1_990_196
ing_prom = 13.8e12 / 1.76e6
ing_irr = ing_prom / (0.34 + 0.66 * 1.22); ing_reg = ing_irr * 1.22
TOTAL = REG * ing_reg / SH_LAB / TRM / 1e6                    # USD M
EXTRA = REG * (ing_reg - ing_irr) / SH_LAB / TRM / 1e6
TARIFA = 44_580 * 464 / 5 / 1e6
VECES = EXTRA / TARIFA

fig = plt.figure(figsize=(7.6, 5.0)); ax = fig.add_axes([0.03, 0.08, 0.6, 0.66]); ax.set_aspect("equal"); ax.axis("off")
s_tot = 1.0; s_ext = np.sqrt(EXTRA / TOTAL); s_tar = np.sqrt(TARIFA / TOTAL)
ax.add_patch(Rectangle((0, 0), s_tot, s_tot, facecolor=LBLUE, edgecolor="none"))
ax.add_patch(Rectangle((0, 0), s_ext, s_ext, facecolor=BLUE, edgecolor="none"))
ax.add_patch(Rectangle((s_ext + 0.03, 0), s_tar, s_tar, facecolor=ORANGE, edgecolor="none"))
ax.set_xlim(-0.01, 1.01); ax.set_ylim(-0.01, 1.01)
ax.text(0.5, 0.75, f"USD {miles(TOTAL)} M" + NL + "al año", ha="center", va="center", fontsize=17, fontweight="bold", color=NAVY)
ax.text(s_ext / 2, s_ext / 2, f"USD {miles(EXTRA)} M", ha="center", va="center", fontsize=14, fontweight="bold", color="white")
ax.annotate("", xy=(s_ext + 0.03 + s_tar, s_tar), xytext=(s_ext + 0.24, 0.2), arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.2))
ax.text(s_ext + 0.25, 0.21, f"USD {pc(TARIFA)} M", ha="left", va="bottom", fontsize=13, fontweight="bold", color=ORANGE)

tx = 0.66
fig.text(tx, 0.66, "Lo que aportan al PIB los" + NL + "2 millones de migrantes regulares", fontsize=11.5, fontweight="bold", color=NAVY, va="top")
fig.text(tx, 0.565, f"{pc(100 * TOTAL * 1e6 * TRM / 1852.7e12, 2)} % del PIB de Colombia: casi tanto" + NL + "como el departamento de Caldas.", fontsize=10, color=INK, va="top")
fig.text(tx, 0.45, "Lo que aportan de más" + NL + "por tener un estatus regular", fontsize=11.5, fontweight="bold", color=BLUE, va="top")
fig.text(tx, 0.355, "Con permiso ganan 22 % más, consumen" + NL + "48 % más y pagan 88 % más impuestos.", fontsize=10, color=INK, va="top")
fig.text(tx, 0.24, "Lo que la tarifa de la Visa R" + NL + "le deja a Cancillería", fontsize=11.5, fontweight="bold", color=ORANGE, va="top")
fig.text(tx, 0.145, "Promedio 2027-2031 si se mantiene" + NL + "la tarifa de USD 464.", fontsize=10, color=INK, va="top")

fig.text(0.03, 0.965, f"Por cada dólar que la tarifa de la Visa R le deja a Cancillería, los migrantes" + NL +
         f"regulares le aportan a la economía más de {miles(np.floor(VECES / 10) * 10)} dólares adicionales al año",
         fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.835, "Cada área es proporcional a su valor anual, en millones de USD.", fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.02, "Fuente: Ibáñez et al. (2025), Journal of the European Economic Association; DANE, GEIH 2025 y cuentas nacionales; Migración Colombia (2026); Cancillería.",
         fontsize=7.6, color=GRAY, ha="left")
fig.savefig(FIG / "pr17_argumento_central.png", dpi=250, facecolor="white"); plt.close(fig)
print("total", round(TOTAL), "extra", round(EXTRA), "tarifa", round(TARIFA, 2), "veces", round(VECES))

# =============================================================== contraste: hoy frente a mayo de 2031 si se mantiene la tarifa
va_reg, va_irr = ing_reg / SH_LAB / TRM, ing_irr / SH_LAB / TRM            # USD por persona al año
REG_2031 = 53_733 + 14_444                                                   # con la tarifa: visas a 2031 + cédula de extranjería
esc2 = {"Hoy": REG, "Mayo de 2031" + NL + "si se mantiene la tarifa": REG_2031}
tot2 = {k: (r * va_reg + (REG - r) * va_irr) / 1e6 for k, r in esc2.items()}     # aporte total al PIB de los 1,99 M
ext2 = {k: r * (va_reg - va_irr) / 1e6 for k, r in esc2.items()}                 # de eso, por ser regulares
fig = plt.figure(figsize=(9.6, 5.4))
ref = TOTAL                                                                  # misma escala en los dos paneles
for j, k in enumerate(esc2):
    ax = fig.add_axes([0.03 + j * 0.5, 0.12, 0.44, 0.6]); ax.set_aspect("equal"); ax.axis("off")
    st, se, sr = np.sqrt(tot2[k] / ref), np.sqrt(ext2[k] / ref), np.sqrt(TARIFA / ref)
    ax.add_patch(Rectangle((0, 0), st, st, facecolor=LBLUE, edgecolor="none"))
    ax.add_patch(Rectangle((0, 0), se, se, facecolor=BLUE, edgecolor="none"))
    ax.add_patch(Rectangle((max(se, 0.0) + 0.03, 0), sr, sr, facecolor=ORANGE, edgecolor="none"))
    ax.set_xlim(-0.01, 1.05); ax.set_ylim(-0.01, 1.12)
    ax.text(0, 1.06, k.replace(NL, " "), ha="left", va="bottom", fontsize=13, fontweight="bold", color=NAVY if j == 0 else ORANGE)
    ax.text(st / 2, st * 0.78, f"USD {miles(tot2[k])} M" + NL + "aporte total al PIB", ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY)
    if se > 0.15:
        ax.text(se / 2, se / 2, f"USD {miles(ext2[k])} M" + NL + "por ser regulares", ha="center", va="center", fontsize=10.5, fontweight="bold", color="white")
    else:
        ax.annotate(f"USD {miles(ext2[k])} M por ser regulares", xy=(se, se), xytext=(0.12, 0.42), fontsize=10.5, fontweight="bold", color=BLUE,
                    arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
    ax.annotate(f"Tarifa: USD {pc(TARIFA)} M", xy=(se + 0.03 + sr, sr), xytext=(max(se, 0.1) + 0.2, 0.17), fontsize=10.5, fontweight="bold", color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1))
    ax.text(0, -0.06, (pc(esc2[k] / 1e6, 2) + " millones" if esc2[k] >= 1e6 else f"{miles(esc2[k] / 1e3)} mil") + " con estatus regular", ha="left", va="top", fontsize=10, color=GRAY)
fig.text(0.03, 0.965, f"Si se mantiene la tarifa, en 2031 el aporte de la regularidad caería de USD {miles(ext2['Hoy'])} millones" + NL +
         f"a USD {miles(ext2[list(esc2)[1]])} millones al año, para recaudar USD {pc(TARIFA)} millones al año", fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.83, "Aporte al PIB de los 2 millones de migrantes venezolanos que hoy son regulares. Cada área es proporcional a su valor anual.",
         fontsize=10, ha="left", color=GRAY)
fig.text(0.03, 0.02, "Fuente: Ibáñez et al. (2025), Journal of the European Economic Association; DANE, GEIH 2025 y cuentas nacionales; Migración Colombia (2026); Cancillería.",
         fontsize=7.6, color=GRAY, ha="left")
fig.savefig(FIG / "pr17b_contraste_tarifa.png", dpi=250, facecolor="white"); plt.close(fig)
print({k.replace(NL, " "): (round(tot2[k]), round(ext2[k])) for k in esc2})
