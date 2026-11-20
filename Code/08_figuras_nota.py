"""Visa-R / 08: figuras de la nota ejecutiva (Outputs/Figures/nota_*.png).

Diseno: cada figura se dibuja al TAMANO REAL con que se inserta en el Word (6,2 in de ancho), asi la letra (9-11 pt) se lee sin escalar.
Una idea por figura, titulo = conclusion, etiquetas directas, sin ejes redundantes. Lee tablas ya calculadas (Outputs/tables).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"

AZ, NA, GR, TX, TX2 = "#2a78d6", "#eb6834", "#a8a7a2", "#0b0b0b", "#52514e"
W = 6.2
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#c9c8c3", "xtick.color": TX2, "ytick.color": TX, "axes.labelcolor": TX2, "figure.dpi": 100})

es = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")


def start(h, title, subtitle=None):
    fig = plt.figure(figsize=(W, h))
    fig.text(0.0, 1 - 0.09 / h, title, fontsize=11.5, fontweight="bold", color=TX, ha="left", va="top")
    if subtitle:
        fig.text(0.0, 1 - 0.32 / h, subtitle, fontsize=8.5, color=TX2, ha="left", va="top")
    return fig


def foot(fig, text, width=118):
    import textwrap
    fig.text(0.0, 0.01, "\n".join(textwrap.wrap(text, width)), fontsize=7.5, color=TX2, ha="left", va="bottom", linespacing=1.25)


def save(fig, name):
    fig.savefig(FIG / name, dpi=230, facecolor="white")
    plt.close(fig)


def clean_x(ax):
    ax.spines["bottom"].set_visible(False); ax.spines["left"].set_color("#c9c8c3"); ax.set_xticks([]); ax.tick_params(axis="y", length=0)


# ------------------------------------------------------------------ emprendimiento (Figura 1 de la nota)
t15 = pd.read_csv(TAB / "t15_emprendimiento_venezolanos_vs_colombianos_2025.csv", index_col=0)
items = [("Son patrones\n(% de los ocupados)", "pct_patron"), ("Tienen empleados\n(% de los independientes)", "pct_indep_con_empleados"),
         ("Negocio registrado en\nCámara de Comercio (%)", "pct_indep_negocio_registrado_camara"), ("Llevan contabilidad\n(% de los independientes)", "pct_indep_lleva_contabilidad")]
fig = start(2.6, "Emprenden como los colombianos, con negocios más pequeños", "GEIH 2025 · independientes = cuenta propia y patrones")
ax = fig.add_axes([0.30, 0.04, 0.66, 0.62])
yy = np.arange(len(items))[::-1] * 1.0
for y_, (lab, k) in zip(yy, items):
    v, c = float(t15.loc[k, "ven"]), float(t15.loc[k, "col"])
    ax.barh(y_ + 0.19, v, height=0.34, color=AZ); ax.barh(y_ - 0.19, c, height=0.34, color=GR)
    ax.text(v + 0.7, y_ + 0.19, (f"{v:.0f}%" if v >= 5 else es(v) + "%"), va="center", fontsize=9.5, color=AZ, fontweight="bold")
    ax.text(c + 0.7, y_ - 0.19, (f"{c:.0f}%" if c >= 5 else es(c) + "%"), va="center", fontsize=9.5, color=TX2)
ax.set_yticks(yy); ax.set_yticklabels([i[0] for i in items], fontsize=9); ax.set_xlim(0, 44); clean_x(ax)
fig.text(0.62, 0.72, "■ Venezolanos", color=AZ, fontsize=9.5, fontweight="bold", ha="left"); fig.text(0.81, 0.72, "■ Colombianos", color=TX2, fontsize=9.5, ha="left")
save(fig, "nota_fig6_emprendimiento.png")

# ------------------------------------------------------------------ con vs sin PPT (Figura 2)
t7 = pd.read_csv(TAB / "t7_epm_ppt_vs_sin_ppt.csv"); t7 = t7[t7.especificacion.str.startswith("A")].set_index("indicador")
rows = [("Afiliados a salud", "Afiliado a salud (%)"), ("Con cuenta en una\nentidad financiera", "Cuenta en entidad financiera (%)"),
        ("Ocupados con\ncontrato escrito", "ocupados: contrato escrito (%)"), ("Afiliados a pensión", "Afiliado a pension (%)"),
        ("No pudieron acceder a salud\n(de quienes la necesitaron)", "Necesito servicio de salud y no pudo acceder (%)")]
fig = start(3.05, "Con PPT, los migrantes entran al sistema formal", "EPM VIII-2025 (DANE), 6.443 venezolanos · % de personas")
ax = fig.add_axes([0.34, 0.14, 0.46, 0.57])
y = np.arange(len(rows))[::-1]
for yy_, (lab, key) in zip(y, rows):
    c, s_, d = t7.loc[key, "media_con_PPT"], t7.loc[key, "media_sin_PPT"], t7.loc[key, "dif_ajustada"]
    ax.plot([s_, c], [yy_, yy_], color="#d9d8d3", lw=3, zorder=1, solid_capstyle="round")
    ax.scatter([s_], [yy_], color=NA, s=70, zorder=3); ax.scatter([c], [yy_], color=AZ, s=70, zorder=3)
    left_is_sin = s_ < c
    ax.text(s_ + (-4 if left_is_sin else 4), yy_, f"{s_:.0f}%", color=NA, ha="right" if left_is_sin else "left", va="center", fontsize=10, fontweight="bold")
    ax.text(c + (4 if left_is_sin else -4), yy_, f"{c:.0f}%", color=AZ, ha="left" if left_is_sin else "right", va="center", fontsize=10, fontweight="bold")
    ax.text(117, yy_, f"{d:+.0f}".replace("-", "−"), ha="center", va="center", fontsize=11.5, fontweight="bold", color=TX, clip_on=False)
ax.set_yticks(y); ax.set_yticklabels([r_[0] for r_ in rows], fontsize=9); ax.set_xlim(-16, 100); clean_x(ax)
ax.text(117, len(rows) - 0.4, "Diferencia\najustada (pts)", ha="center", va="bottom", fontsize=8.5, color=TX2, clip_on=False)
fig.text(0.34, 0.775, "● Con PPT", color=AZ, fontsize=9.5, fontweight="bold", ha="left"); fig.text(0.50, 0.775, "● Sin PPT", color=NA, fontsize=9.5, fontweight="bold", ha="left")
foot(fig, "Diferencia ajustada por sexo, edad, año de llegada y otros controles. Asociación, no causalidad.")
save(fig, "nota_fig2_con_vs_sin_ppt.png")

# ------------------------------------------------------------------ afiliacion a salud (Figura 3)
t4 = pd.read_csv(TAB / "t4_mercado_laboral_por_grupo_anio.csv", index_col=[0, 1])
t5 = pd.read_csv(TAB / "t5_indicadores_por_cohorte_llegada_2025_2026.csv", index_col=0)
fig = start(2.65, "La afiliación a salud avanza, pero los recién llegados quedan atrás", "GEIH-DANE · venezolanos sin nacionalidad colombiana · % afiliados")
a = fig.add_axes([0.05, 0.14, 0.40, 0.55]); b = fig.add_axes([0.58, 0.14, 0.40, 0.55])
yrs = [2022, 2023, 2024, 2025, 2026]
ven = [t4.loc[("ven_ext", y_), "afiliado_salud_pct"] for y_ in yrs]; col = [t4.loc[("col", y_), "afiliado_salud_pct"] for y_ in yrs]
a.plot(yrs, col, color=GR, lw=2, ls="--"); a.plot(yrs, ven, color=AZ, lw=3, marker="o", ms=6)
for x_, v in zip(yrs, ven): a.text(x_, v + 7, f"{v:.0f}%", ha="center", fontsize=9.5, color=AZ, fontweight="bold")
a.text(2022, 82, "Colombianos: 97%", fontsize=9, color=TX2, ha="left")
a.text(2022.1, 17, "Venezolanos", fontsize=9.5, color=AZ, fontweight="bold", ha="left")
a.set_ylim(0, 108); a.set_xticks(yrs); a.set_xticklabels(["2022", "'23", "'24", "'25", "'26*"], fontsize=9); a.set_yticks([]); a.spines["left"].set_visible(False)
a.set_title("Por año", loc="left", fontsize=9.5, color=TX2, pad=4)
coh = ["<=2016", "2017-2018", "2019-2020", "2021-2022", "2023+"]; vals = [t5.loc[c_, "afiliado_salud_pct"] for c_ in coh]
b.bar(range(5), vals, color=[AZ] * 4 + [NA], width=0.66)
for i, v in enumerate(vals): b.text(i, v + 2.5, f"{v:.0f}%", ha="center", fontsize=9.5, color=NA if i == 4 else AZ, fontweight="bold")
b.set_xticks(range(5)); b.set_xticklabels(["hasta\n2016", "2017\n-18", "2019\n-20", "2021\n-22", "desde\n2023"], fontsize=8.5)
b.set_ylim(0, 100); b.set_yticks([]); b.spines["left"].set_visible(False)
b.set_title("Por año de llegada al país (2025-26)", loc="left", fontsize=9.5, color=TX2, pad=4)
foot(fig, "*2026: enero-agosto.")
save(fig, "nota_fig1_afiliacion_salud.png")

# ------------------------------------------------------------------ magnitudes (Figura 4)
r = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
masa = pd.read_csv(TAB / "t8b_resumen_demanda_interna.csv", index_col=0)["valor"]["masa_salarial_anual_billones_COP_2025"]
tarifa = r["ingreso_maximo_por_tarifa_464_COP_billones"]
fig = start(2.1, "La tarifa recauda, una vez, lo de un año de aporte fiscal", "Billones de pesos · todos los titulares de PPT pagando la tarifa vigente")
ax = fig.add_axes([0.30, 0.20, 0.62, 0.47])
data = [("Ingreso laboral de\nlos venezolanos", masa, AZ, "cada año"), ("Aporte fiscal\n(estudio OIM)", 1.5, AZ, "cada año"), ("Tarifa de la Visa R\n(ingreso máximo)", tarifa, NA, "una sola vez")]
yy = np.arange(3)[::-1]
for y_, (lab, v, c_, note) in zip(yy, data):
    ax.barh(y_, v, color=c_, height=0.56)
    ax.text(v + 0.35, y_, f"{es(v)}  {note}", va="center", fontsize=9.5, color=c_, fontweight="bold")
ax.set_yticks(yy); ax.set_yticklabels([d[0] for d in data], fontsize=9); ax.set_xlim(0, 22); clean_x(ax)
foot(fig, f"La tarifa equivale a {es(r['ingreso_maximo_464_como_pct_PIB'], 2)}% del PIB, una sola vez. Fuentes: GEIH 2025; OIM/Equilibrium y U. del Rosario; cálculos propios.")
save(fig, "nota_fig5_magnitudes.png")

# ------------------------------------------------------------------ ola de tramites (Figura 5)
el = pd.read_csv(TAB / "t12b_elegibilidad_por_anio.csv")
nuevos = el.titulares_elegibles_miles.diff().fillna(el.titulares_elegibles_miles.iloc[0])
fig = start(2.5, "Dos de cada tres titulares serán elegibles en 2027-2028", "Titulares de PPT que cumplen 5 años, por año · miles de personas")
ax = fig.add_axes([0.14, 0.31, 0.84, 0.41])
cols = [NA if a_ in (2027, 2028) else AZ for a_ in el.anio]
ax.bar(el.anio, nuevos, color=cols, width=0.62)
for x_, v in zip(el.anio, nuevos):
    if v > 15: ax.text(x_, v + 14, f"{v:.0f} mil", ha="center", fontsize=10, color=TX, fontweight="bold")
ax.set_xticks(el.anio); ax.set_xticklabels([str(a_) for a_ in el.anio], fontsize=9.5); ax.set_yticks([]); ax.set_ylim(0, 720); ax.spines["left"].set_visible(False)
for x_, p_ in zip(el.anio, el.pct_titulares_con_5_anios_de_PPT):
    ax.text(x_, -0.27, f"{p_:.0f}%", ha="center", va="top", fontsize=9, color=TX2, clip_on=False, transform=ax.get_xaxis_transform())
ax.text(2025.5, -0.27, "Acumulado:", ha="right", va="top", fontsize=8.5, color=TX2, clip_on=False, transform=ax.get_xaxis_transform())
ax.axvline(2031 - 0.38, color=NA, lw=1.3, ls="--"); ax.text(2031 - 0.44, 690, "28 may 2031:\nvence el PPT", color=NA, fontsize=8.5, ha="right", va="top")
foot(fig, "PPT + 5 años; no cuenta el tiempo con PEP (subestima). ≈1,15 M de titulares (GEIH × EPM).")
save(fig, "nota_fig3_ola_de_tramites.png")

# ------------------------------------------------------------------ asequibilidad (Figura 6)
asq = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
u = "tarifa del hogar >= 1 mes(es) de ingreso laboral del hogar"
opts = [("Tarifa vigente", "USD 464", "USD 464 (56+408) vigente", AZ), ("Propuesta: mitad", "USD 232", "mitad (USD 232)", NA), ("Solo estudio", "USD 56", "solo estudio USD 56 (se elimina la visa)", AZ)]
fig = start(2.4, "Dos de cada tres hogares pagarían más de un mes de ingreso", "% de hogares con venezolanos cuya tarifa equivale a más de 1 mes de ingreso laboral")
ax = fig.add_axes([0.05, 0.34, 0.92, 0.38])
vals = [asq[(asq.tarifa == f) & (asq.umbral == u)].pct_hogares_con_venezolano.iloc[0] for _, _, f, _ in opts]
for i, ((nm, usd, f, c_), v) in enumerate(zip(opts, vals)):
    ax.bar(i, v, color=c_, width=0.55)
    ax.text(i, v + 2.5, f"{v:.0f}%", ha="center", fontsize=14, fontweight="bold", color=c_)
ax.set_xticks(range(3)); ax.set_xticklabels([f"{nm}\n{usd}" for nm, usd, _, _ in opts], fontsize=9.5)
ax.set_ylim(0, 80); ax.set_yticks([]); ax.spines["left"].set_visible(False)
foot(fig, "GEIH 2026 (ene-ago); todos los venezolanos del hogar pagan; TRM COP 3.235; tarifas de la Cancillería.")
save(fig, "nota_fig4_asequibilidad.png")

# ------------------------------------------------------------------ curva precio - recaudo - derrame (Figura 6 de la nota)
cv = pd.read_csv(TAB / "t17_curva_precio_recaudo.csv")
cv = cv[cv.theta_meses_de_ingreso == 2].sort_values("tarifa_USD").reset_index(drop=True)
_r12 = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
N_ti = _r12["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3
S_der = _r12["beneficio_fiscal_anual_B_USD_por_persona"] * 5          # USD por persona que convierte (5 anios)
Fg = cv.tarifa_USD.to_numpy().astype(float)
tau_s = cv.conversion.rolling(5, center=True, min_periods=1).mean().to_numpy()      # suavizado: los datos de hogares son discretos
tau = tau_s * 100
rec = N_ti * tau_s * Fg / 1e6
tot = rec + N_ti * tau_s * S_der / 1e6
at = lambda arr, f: float(np.interp(f, Fg, arr))
i_tot = int(np.argmax(tot))
d_rec = at(rec, 232) / at(rec, 464) - 1; d_tot = at(tot, 232) / at(tot, 464) - 1
fig = start(3.6, "Con un precio menor, pagan más y el beneficio total sube",
            f"De USD 464 a 232: recaudo {d_rec*100:+.0f}%, valor total {d_tot*100:+.0f}%, conversión de {at(tau,464):.0f}% a {at(tau,232):.0f}%".replace("-", "−"))
a = fig.add_axes([0.075, 0.30, 0.27, 0.43]); b = fig.add_axes([0.50, 0.30, 0.48, 0.43])
# panel A: cuantos convierten
a.plot(Fg, tau, color=AZ, lw=3)
for f_ in (464, 232):
    c_ = NA if f_ == 232 else TX2
    a.scatter([f_], [at(tau, f_)], color=c_, s=55, zorder=3)
    a.text(f_ + 22, at(tau, f_) + 5, f"{at(tau, f_):.0f}%", fontsize=10.5, fontweight="bold", color=c_, ha="left")
    a.axvline(f_, color=c_, lw=0.8, ls=":")
a.set_ylim(0, 100); a.set_xlim(0, 700); a.set_xticks([232, 464])
a.set_xticklabels(["232", "464"], fontsize=8.5); a.set_yticks([0, 50, 100]); a.set_yticklabels(["0", "50", "100"], fontsize=8.5)
a.get_xticklabels()[0].set_color(NA); a.get_xticklabels()[1].set_color(TX2)
a.set_title("Titulares que convierten (%)", loc="left", fontsize=9.5, color=TX2, pad=5); a.set_xlabel("Precio por persona (USD)", fontsize=8.5, color=TX2)
# panel B: recaudo y derrame
b.fill_between(Fg, rec, tot, color="#d6e5f8", lw=0)
b.plot(Fg, tot, color=AZ, lw=3); b.plot(Fg, rec, color=NA, lw=3)
b.text(690, 1010, "Recaudo + derrame", color=AZ, fontsize=9.5, fontweight="bold", ha="right")
b.text(690, 345, "Recaudo de la Cancillería", color=NA, fontsize=9.5, fontweight="bold", ha="right")
b.text(55, 640, "derrame\n(salud, aportes,\nformalización)", color=AZ, fontsize=8.5, ha="left", va="center", style="italic")
for f_ in (464, 232):
    c_ = NA if f_ == 232 else TX2
    b.axvline(f_, color=c_, lw=0.8, ls=":")
    b.scatter([f_, f_], [at(rec, f_), at(tot, f_)], color=c_, s=45, zorder=3)
b.scatter([Fg[i_tot]], [tot[i_tot]], marker="*", s=130, color=AZ, zorder=4)
b.text(Fg[i_tot] + 15, tot[i_tot] + 75, f"valor máximo: USD {Fg[i_tot]:.0f}", fontsize=8.5, color=AZ, ha="center")
b.set_ylim(0, 1180); b.set_xlim(0, 700); b.set_yticks([0, 400, 800]); b.set_yticklabels(["0", "400", "800"], fontsize=8.5)
b.set_xticks([232, 464]); b.set_xticklabels(["Propuesta\nUSD 232", "Vigente\nUSD 464"], fontsize=8.5, fontweight="bold")
b.get_xticklabels()[0].set_color(NA); b.get_xticklabels()[1].set_color(TX2)
b.set_title("USD millones", loc="left", fontsize=9.5, color=TX2, pad=5)
foot(fig, "Ilustrativo: la demanda no está medida. Conversión = 85% × hogares que pagan hasta 2 meses de ingreso (GEIH 2026). Derrame = USD 980 por persona en 5 años (literatura); con costo de salud en vez de derrame, el óptimo sería un precio alto.", 108)
save(fig, "nota_fig7_curva_precio.png")
print("fig7", round(d_rec, 3), round(d_tot, 3), round(float(Fg[int(np.argmax(rec))])), round(float(Fg[i_tot])), round(at(tau, 232)), round(at(tau, 464)))

print("ok")
