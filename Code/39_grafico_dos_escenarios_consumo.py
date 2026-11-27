"""Visa-R / 39: dos escenarios para el consumo de los hogares venezolanos, 2025-2036 (billones de pesos de 2025).
Solo cambia el consumo: población, precios, PIB y demás variables se mantienen constantes en su nivel de 2025.

Punto de partida (Code/34, t34): consumo de los venezolanos en 2025 = 32,18 billones (2,37 % del consumo de los hogares, DANE).
  - 1,757 M venezolanos (GEIH 2025); 66 % regulares con PPT (EPM VIII-2025); los regulares consumen 48 % más (Ibáñez et al., 2025, JEEA).
  - Regulares: 23,87 billones; irregulares: 8,31 billones.
Tres grupos cada año:
  - Regulares con Visa R: consumen como regulares + 8,8 % por la estabilidad de la residencia (Code/35, escenario central:
    menos ahorro precautorio, De Arcangelis y Joxhe, 2015; menos remesas, Dustmann y Mestres, 2010).
  - Regulares con PPT: consumen como regulares hasta mayo de 2031, cuando vence el PPT (7/12 de 2031); después pasan a irregulares.
  - Irregulares: consumen 1/1,48 de un regular.
Cuántos obtienen la Visa R (sobre 1.990.196 regulares, Migración Colombia; la proporción se aplica a los regulares de la GEIH):
  1. Con tarifa de USD 464: 8.440 visas hoy + tendencia lineal de Cancillería (5.984, 7.450, 8.916, 10.382, 11.848 en 2027-2031).
  2. Tarifa cero desde 2027: 80 % de los 1.770.136 titulares de PPT que quieren quedarse (89,6 %, EPM), según cumplan 5 años
     con PPT (81 % en 2027, 96 % en 2028, 99,6 % en 2029, 100 % desde 2030). 80 %: afiliación a salud de los venezolanos
     con 5 años o más en el país (GEIH).
  Los 14.444 que ya tienen cédula de extranjería siguen regulares en los dos escenarios.
Salida: Outputs/Figures/pr24_dos_escenarios_consumo.png y Outputs/tables/t39_dos_escenarios_consumo.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"
NAVY, BLUE, LBLUE, ORANGE, INK, GRAY = "#1f3b5c", "#2a79d6", "#cfe0f5", "#eb6a35", "#222222", "#6b6b6b"
NL = chr(10)
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "text.color": INK})
pc = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
miles = lambda x: f"{x:,.0f}".replace(",", ".")

# ---- punto de partida 2025 (t34, t35)
t34 = pd.read_csv(TAB / "t34_consumo_venezolanos.csv").set_index("concepto")["valor"]
t35 = pd.read_csv(TAB / "t35_consumo_residencia.csv").set_index("escenario")
C_REG, C_IRR = t34["  regulares (billones)"], t34["  irregulares (billones)"]
BONO = t35.loc["Central", "aumento_pct"] / 100                  # +8,8 % de consumo con residencia permanente
TRM = 4052.86

# ---- personas que obtienen la Visa R (acumulado, base Migración Colombia)
REG_MIG, RES, QUIEREN, CONV, BASE = 1_990_196, 14_444, 1_770_136, 0.80, 8_440
YRS = np.arange(2025, 2037)
ELIG = {2027: 0.8118, 2028: 0.9634, 2029: 0.9956}
VT = {2027: 5_984, 2028: 7_450, 2029: 8_916, 2030: 10_382, 2031: 11_848}
visa_tarifa = BASE + np.cumsum([VT.get(y, 0) for y in YRS])
visa_cero = np.array([BASE if y < 2027 else max(CONV * QUIEREN * ELIG.get(y, 1.0), BASE + sum(v for k, v in VT.items() if k <= y)) for y in YRS])
ppt_vigente = np.array([1.0 if y < 2031 else (7 / 12 if y == 2031 else 0.0) for y in YRS])   # fracción del año con PPT


def consumo(visas):
    """Consumo de los venezolanos (billones). Las proporciones se aplican a los regulares de la GEIH (23,87 billones)."""
    s_v, s_res = visas / REG_MIG, RES / REG_MIG
    s_ppt = 1 - s_v - s_res
    con_visa = C_REG * s_v * (1 + BONO)
    con_res = C_REG * s_res
    con_ppt = C_REG * s_ppt * (ppt_vigente + (1 - ppt_vigente) / 1.48)    # sin PPT consumen como irregulares
    return con_visa + con_res + con_ppt + C_IRR, con_visa, con_ppt


tot_t, visa_t, ppt_t = consumo(visa_tarifa)
tot_c, visa_c, ppt_c = consumo(visa_cero)
recaudo = np.array([VT.get(y, 0) * 464 for y in YRS])              # USD
d = pd.DataFrame({"anio": YRS, "visas_con_tarifa": visa_tarifa.round(0), "visas_tarifa_cero": visa_cero.round(0),
                  "consumo_con_tarifa_billones": tot_t, "consumo_tarifa_cero_billones": tot_c, "diferencia_billones": tot_c - tot_t,
                  "diferencia_USD_M": (tot_c - tot_t) * 1e12 / TRM / 1e6, "recaudo_Cancilleria_USD_M": recaudo / 1e6,
                  "recaudo_Cancilleria_billones": recaudo * TRM / 1e12}).round(3)
d.to_csv(TAB / "t39_dos_escenarios_consumo.csv", index=False)
print(d.to_string())
dif_acum = (tot_c - tot_t)[YRS >= 2027].sum()
rec_tot_usd, rec_tot_bill = recaudo.sum() / 1e6, recaudo.sum() * TRM / 1e12
print("dif acumulada 2027-2036", round(dif_acum, 2), "recaudo total USD M", round(rec_tot_usd, 1), "billones", round(rec_tot_bill, 3))

# ======================= gráfico
fig, ax = plt.subplots(figsize=(9.6, 5.6)); fig.subplots_adjust(left=0.07, right=0.8, top=0.76, bottom=0.12)
ax.fill_between(YRS, tot_t, tot_c, where=YRS >= 2026, color=LBLUE, zorder=1, lw=0)
ax.axhline(C_REG + C_IRR, color=GRAY, lw=0.8, ls=":", zorder=1)
ax.text(2024.9, C_REG + C_IRR - 0.3, f"Hoy: {pc(C_REG + C_IRR)} billones", fontsize=9.5, color=GRAY, va="top")
ax.plot(YRS, tot_c, color=BLUE, lw=3, marker="o", ms=5, zorder=3)
ax.plot(YRS, tot_t, color=ORANGE, lw=3, marker="o", ms=5, zorder=3)
# etiquetas al final de cada línea
ax.text(2036.3, tot_c[-1], f"Tarifa cero" + NL + f"{pc(tot_c[-1])} billones", color=BLUE, fontsize=11.5, fontweight="bold", va="center")
ax.text(2036.3, tot_t[-1], f"Con tarifa de USD 464" + NL + f"{pc(tot_t[-1])} billones", color=ORANGE, fontsize=11.5, fontweight="bold", va="center")
# diferencia en la zona sombreada
ax.annotate("", xy=(2034, tot_c[YRS == 2034][0] - 0.15), xytext=(2034, tot_t[YRS == 2034][0] + 0.15),
            arrowprops=dict(arrowstyle="<->", color=NAVY, lw=1.3))
ax.text(2033.85, (tot_c[-1] + tot_t[-1]) / 2, f"+{pc(tot_c[-1] - tot_t[-1])} billones" + NL + "al año más de consumo" + NL + "con tarifa cero",
        ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
# 2027 y 2031
ax.axvline(2031, color=GRAY, lw=0.8, ls="--", zorder=1)
ax.text(2031.1, 22.4, "Mayo de 2031:" + NL + "vence el PPT", fontsize=9.5, color=GRAY, va="bottom")
ax.text(2027.0, tot_c[YRS == 2027][0] + 0.5, "2027: la Visa R" + NL + "pasa a costar cero", fontsize=9.5, color=BLUE, ha="center", va="bottom")
ax.text(2028.9, 27.4, "Cancillería recauda con la tarifa:" + NL + f"USD {miles(rec_tot_usd)} millones en cinco años" + NL + f"(0,{round(rec_tot_bill * 100):02d} billones de pesos)",
        fontsize=10, color=ORANGE, ha="center", va="center", bbox=dict(boxstyle="round,pad=0.45", fc="white", ec=ORANGE, lw=0.8))

ax.set_xticks(YRS); ax.set_xticklabels([str(y) for y in YRS], fontsize=10)
ax.set_xlim(2024.6, 2036.2); ax.set_ylim(22, 35.5)
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: pc(v, 0)))
ax.tick_params(axis="both", length=0); ax.grid(axis="y", color="#e6e9ee", lw=0.7, zorder=0)
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#999999")
ax.set_ylabel("Billones de pesos de 2025 al año", fontsize=10, color=GRAY)

fig.text(0.03, 0.965, f"Con la Visa R gratis, los hogares venezolanos gastarían {pc(tot_c[-1] - tot_t[-1])} billones de pesos más" + NL +
         f"cada año en Colombia; con la tarifa, Cancillería recauda USD {miles(rec_tot_usd)} millones en total", fontsize=14.5, fontweight="bold", ha="left", va="top")
fig.text(0.03, 0.835, f"Consumo de los hogares venezolanos en Colombia. Tarifa cero: {pc(visa_cero[-1] / 1e6, 2)} millones obtienen la Visa R; con tarifa: {miles(visa_tarifa[-1] / 1e3)} mil."
         + NL + "Todo lo demás se mantiene constante en su nivel de 2025.", fontsize=10, ha="left", va="top", color=GRAY)
fig.text(0.03, 0.02, "Fuente: cálculos propios con DANE (GEIH 2025, cuentas nacionales), EPM VIII-2025, Migración Colombia y Cancillería; Ibáñez et al. (2025), JEEA;"
         + " De Arcangelis y Joxhe (2015).", fontsize=7.4, color=GRAY, ha="left")
fig.savefig(FIG / "pr24_dos_escenarios_consumo.png", dpi=250, facecolor="white"); plt.close(fig)

# ======================= un gráfico por escenario: de qué grupo viene el consumo (misma escala en los dos)
LORANGE, LGRAY, MBLUE = "#f2a27e", "#d9dde3", "#9fc0ea"


def partes(visas):
    s_v, s_res = visas / REG_MIG, RES / REG_MIG
    s_ppt = 1 - s_v - s_res
    irr = C_IRR + C_REG * s_ppt * (1 - ppt_vigente) / 1.48
    ppt = C_REG * s_ppt * ppt_vigente
    visa = C_REG * (s_v + s_res)
    bono = C_REG * s_v * BONO
    return irr, ppt, visa, bono


def grafico(visas, archivo, titulo, sub, recaudo_txt, col_rec):
    irr, ppt, visa, bono = partes(visas)
    tot = irr + ppt + visa + bono
    fig, ax = plt.subplots(figsize=(9.6, 5.6)); fig.subplots_adjust(left=0.07, right=0.76, top=0.76, bottom=0.12)
    capas = [(irr, LGRAY, "Irregulares"), (ppt, MBLUE, "Regulares con PPT"), (visa, NAVY, "Regulares con Visa R"),
             (bono, BLUE, "Gasto adicional por la residencia (+8,8 %)")]
    ax.stackplot(YRS, *[c[0] for c in capas], colors=[c[1] for c in capas], lw=0, zorder=1)
    ax.plot(YRS, tot, color=INK, lw=2.4, marker="o", ms=4.5, zorder=3)
    for y_, v in zip(YRS, tot):
        if y_ in (2025, 2030, 2036):
            ax.text(y_, v + 0.6, pc(v), ha="center", va="bottom", fontsize=11, fontweight="bold", color=INK)
    # capas que siguen en 2036: nombre a la derecha; regulares con PPT: nombre dentro del área (desaparece en 2031)
    nombres = {"Irregulares": ("Irregulares", "#5b6573"), "Regulares con Visa R": ("Regulares con Visa R", NAVY),
               "Gasto adicional por la residencia (+8,8 %)": ("Extra por la residencia", BLUE)}
    yl, b = [], 0
    for serie, col, nom in capas:
        if nom in nombres and serie[-1] > 0.3:
            ylab = b + serie[-1] / 2
            while any(abs(ylab - o) < 1.9 for o in yl):
                ylab += 1.9
            yl.append(ylab)
            ax.text(2036.45, ylab, f"{nombres[nom][0]}: {pc(serie[-1])}", fontsize=10.5, fontweight="bold", color=nombres[nom][1], va="center")
        b += serie[-1]
    ax.text(2025.35, 12, "Regulares con PPT" + NL + "(hasta mayo de 2031)", fontsize=10.5, fontweight="bold", color=NAVY, va="center")
    ax.axvline(2031, color=GRAY, lw=0.8, ls="--", zorder=2)
    ax.text(2031.1, 41.5, "Mayo de 2031: vence el PPT", fontsize=9.5, color=GRAY, va="top")
    ax.text(2025.2, 41.5, recaudo_txt, fontsize=10.5, color=col_rec, va="top", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=col_rec, lw=0.8))
    ax.set_xticks(YRS); ax.set_xticklabels([str(y) for y in YRS], fontsize=10)
    ax.set_xlim(2024.6, 2036.3); ax.set_ylim(0, 42)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: pc(v, 0)))
    ax.tick_params(axis="both", length=0); ax.grid(axis="y", color="#ffffff", lw=0.7, zorder=2)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    ax.set_ylabel("Consumo, billones de pesos de 2025 al año", fontsize=10, color=GRAY)
    fig.text(0.03, 0.965, titulo, fontsize=14.5, fontweight="bold", ha="left", va="top")
    fig.text(0.03, 0.835, sub + NL + "Consumo de los hogares venezolanos en Colombia. Todo lo demás se mantiene constante en su nivel de 2025.",
             fontsize=10, ha="left", va="top", color=GRAY)
    fig.text(0.03, 0.02, "Fuente: cálculos propios con DANE (GEIH 2025, cuentas nacionales), EPM VIII-2025, Migración Colombia y Cancillería; Ibáñez et al. (2025), JEEA;"
             + " De Arcangelis y Joxhe (2015).", fontsize=7.4, color=GRAY, ha="left")
    fig.savefig(FIG / archivo, dpi=250, facecolor="white"); plt.close(fig)
    return tot


tA = grafico(visa_tarifa, "pr24a_escenario_con_tarifa.png",
             f"Escenario 1. Con la tarifa de USD 464, en 2031 el consumo de los" + NL +
             f"hogares venezolanos cae de {pc(tot_t[0])} a {pc(tot_t[-1])} billones de pesos al año",
             f"Solo {miles(visa_tarifa[-1] / 1e3)} mil obtienen la Visa R; el resto de los regulares queda irregular cuando vence el PPT.",
             f"Cancillería recauda USD {miles(rec_tot_usd)} millones en 2027-2031", ORANGE)
tB = grafico(visa_cero, "pr24b_escenario_tarifa_cero.png",
             f"Escenario 2. Con la Visa R gratis desde 2027, el consumo de los hogares" + NL +
             f"venezolanos se mantiene en {pc(tot_c[-1])} billones de pesos al año después de 2031",
             f"{pc(visa_cero[-1] / 1e6, 2)} millones obtienen la Visa R (80 % de quienes quieren quedarse) y siguen regulares cuando vence el PPT.",
             "Cancillería no recauda por la tarifa", BLUE)
print("A", tA.round(2)); print("B", tB.round(2))
