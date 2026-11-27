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


def grafico(visas, tot, col, archivo, titulo, sub, notas, recaudo_txt, etq_anios=(2030, 2036)):
    """Una sola línea: el consumo total, comparado con hoy. Verde-azul donde gana, naranja donde pierde."""
    hoy = tot[0]
    fig, ax = plt.subplots(figsize=(9.6, 5.6)); fig.subplots_adjust(left=0.05, right=0.97, top=0.76, bottom=0.12)
    ax.fill_between(YRS, hoy, tot, where=tot >= hoy, interpolate=True, color=BLUE, alpha=0.18, lw=0, zorder=1)
    ax.fill_between(YRS, hoy, tot, where=tot <= hoy, interpolate=True, color=ORANGE, alpha=0.18, lw=0, zorder=1)
    ax.axhline(hoy, color=GRAY, lw=1, ls=":", zorder=2)
    ax.text(2024.75, hoy + 0.25, f"Hoy: {pc(hoy)} billones", fontsize=10, color=GRAY, va="bottom")
    ax.plot(YRS, tot, color=col, lw=3.4, marker="o", ms=6, zorder=3)
    for y_, v in zip(YRS, tot):
        if y_ in etq_anios:
            arriba = v >= hoy
            ax.text(y_, v + (0.35 if arriba else -0.35), pc(v), ha="center", va="bottom" if arriba else "top", fontsize=13, fontweight="bold", color=col)
    for (x_, y_, txt, c_, ha) in notas:
        ax.text(x_, y_, txt, fontsize=11, color=c_, ha=ha, va="center", fontweight="bold", linespacing=1.3)
    ax.axvline(2031, color=GRAY, lw=0.8, ls="--", zorder=1)
    ax.text(2031.1, 35.8, "Mayo de 2031:" + NL + "vence el PPT", fontsize=9.5, color=GRAY, va="top")
    ax.text(2025.0, 23.0, recaudo_txt, fontsize=11, color=NAVY, va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=NAVY, lw=0.8))
    ax.set_xticks(YRS); ax.set_xticklabels([str(y) for y in YRS], fontsize=10.5)
    ax.set_xlim(2024.6, 2036.5); ax.set_ylim(22, 36)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0)
    for s_ in ["top", "right", "left"]:
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    fig.text(0.03, 0.965, titulo, fontsize=15, fontweight="bold", ha="left", va="top")
    fig.text(0.03, 0.835, sub, fontsize=10.5, ha="left", va="top", color=GRAY)
    fig.text(0.03, 0.02, "Fuente: cálculos propios con DANE (GEIH 2025, cuentas nacionales), EPM VIII-2025, Migración Colombia y Cancillería; Ibáñez et al. (2025), JEEA;"
             + " De Arcangelis y Joxhe (2015).", fontsize=7.4, color=GRAY, ha="left")
    fig.savefig(FIG / archivo, dpi=250, facecolor="white"); plt.close(fig)


SUB = "Consumo de los hogares venezolanos en Colombia, billones de pesos de 2025 al año. Todo lo demás se mantiene igual que en 2025."
irr_t = 1 - (visa_tarifa[-1] + RES) / REG_MIG
irr_c = 1 - (visa_cero[-1] + RES) / REG_MIG
gan_c = (tot_c - tot_c[0])[(YRS >= 2027) & (YRS <= 2030)].max()
grafico(visa_tarifa, tot_t, ORANGE, "pr24a_escenario_con_tarifa.png",
        "Escenario 1: si se mantiene la tarifa de USD 464, el consumo" + NL +
        f"de los hogares venezolanos cae {pc(tot_t[0] - tot_t[-1])} billones de pesos al año desde 2032",
        SUB,
        [(2028, 33.6, "2027-2030: pocos pagan la visa," + NL + "el consumo casi no cambia", GRAY, "center"),
         (2034, 28.4, f"−{pc(tot_t[0] - tot_t[-1])} billones al año frente a hoy:" + NL +
          f"el {pc(100 * irr_t, 0)} % de los regulares queda irregular" + NL + "y gasta 32 % menos", ORANGE, "center")],
        f"Cancillería recauda USD {miles(rec_tot_usd)} millones" + NL + "en cinco años (2027-2031)")
grafico(visa_cero, tot_c, BLUE, "pr24b_escenario_tarifa_cero.png",
        "Escenario 2: con la Visa R gratis desde 2027, el consumo de los hogares" + NL +
        f"venezolanos sube {pc(gan_c)} billones al año y casi no cae cuando vence el PPT",
        SUB,
        [(2028.2, 35.1, f"+{pc(gan_c)} billones al año frente a hoy:" + NL + "con residencia permanente gastan 8,8 % más", BLUE, "center"),
         (2034, 29.0, f"−{pc(tot_c[0] - tot_c[-1])} billones frente a hoy:" + NL +
          f"solo el {pc(100 * irr_c, 0)} % de los regulares no obtiene" + NL + "la visa y queda irregular", ORANGE, "center")],
        "Cancillería no recauda por la tarifa", etq_anios=(2036,))
