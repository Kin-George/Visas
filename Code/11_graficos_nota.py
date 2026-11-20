"""Visa-R / 11: graficos de la nota tecnica (estilo de articulo: serif, paleta sobria, titulos y fuentes en el documento).
Salida: Outputs/Figures/gr1_*.png ... gr5_*.png (se insertan al tamano real, 5,9 in de ancho)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
TAB, FIG = ROOT / "Outputs" / "tables", ROOT / "Outputs" / "Figures"

NAVY, GRAY, LGRAY, ACC, INK = "#1f3b5c", "#8c8c8c", "#cfcfcf", "#a4472f", "#222222"
W = 5.9
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 9, "text.color": INK,
    "axes.edgecolor": "#555555", "axes.linewidth": 0.6, "axes.labelcolor": INK, "axes.labelsize": 8.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
    "grid.color": "#e4e4e4", "grid.linewidth": 0.5, "xtick.color": INK, "ytick.color": INK, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "xtick.direction": "out", "ytick.direction": "out", "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "legend.frameon": False, "legend.fontsize": 8.5, "figure.dpi": 100})
pc = lambda x, d=0: f"{x:.{d}f}".replace(".", ",")


def save(fig, name):
    fig.savefig(FIG / name, dpi=250, facecolor="white")
    plt.close(fig)


def val(ax, x, y, text, **kw):
    ax.text(x, y, text, ha="center", va="bottom", fontsize=8, color=kw.pop("color", INK), **kw)


# ---------------------------------------------------------------- Grafico 1: con vs sin PPT
t7 = pd.read_csv(TAB / "t7_epm_ppt_vs_sin_ppt.csv"); t7 = t7[t7.especificacion.str.startswith("A")].set_index("indicador")
items = [("Afiliados\na salud", "Afiliado a salud (%)"), ("Cuenta en entidad\nfinanciera", "Cuenta en entidad financiera (%)"),
         ("Contrato escrito\n(ocupados)", "ocupados: contrato escrito (%)"), ("Afiliados\na pensión", "Afiliado a pension (%)"),
         ("No pudo acceder\na salud*", "Necesito servicio de salud y no pudo acceder (%)")]
fig, ax = plt.subplots(figsize=(W, 1.85)); fig.subplots_adjust(left=0.09, right=0.99, top=0.95, bottom=0.27)
x = np.arange(len(items)); w_ = 0.34
con = [t7.loc[k, "media_con_PPT"] for _, k in items]; sin = [t7.loc[k, "media_sin_PPT"] for _, k in items]
ax.bar(x - w_ / 2, con, w_, color=NAVY, label="Con PPT"); ax.bar(x + w_ / 2, sin, w_, color=LGRAY, edgecolor="#9a9a9a", linewidth=0.5, label="Sin PPT")
for xi, c, s_ in zip(x, con, sin):
    val(ax, xi - w_ / 2, c + 1.2, pc(c)); val(ax, xi + w_ / 2, s_ + 1.2, pc(s_))
ax.set_xticks(x); ax.set_xticklabels([i[0] for i in items]); ax.set_ylim(0, 105); ax.set_ylabel("% de personas"); ax.legend(loc="upper right", ncol=2)
save(fig, "gr1_con_vs_sin_ppt.png")

# ---------------------------------------------------------------- Grafico 2: afiliacion a salud
t4 = pd.read_csv(TAB / "t4_mercado_laboral_por_grupo_anio.csv", index_col=[0, 1])
t5 = pd.read_csv(TAB / "t5_indicadores_por_cohorte_llegada_2025_2026.csv", index_col=0)
fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.0), gridspec_kw={"width_ratios": [1, 1.15]}); fig.subplots_adjust(left=0.09, right=0.99, top=0.86, bottom=0.21, wspace=0.28)
yrs = [2022, 2023, 2024, 2025, 2026]
ven = [t4.loc[("ven_ext", y_), "afiliado_salud_pct"] for y_ in yrs]; col = [t4.loc[("col", y_), "afiliado_salud_pct"] for y_ in yrs]
a.plot(yrs, col, color=GRAY, lw=1.2, ls="--", marker="s", ms=2.5); a.plot(yrs, ven, color=NAVY, lw=1.4, marker="o", ms=3.5)
for x_, v in zip(yrs, ven): a.text(x_, v - 8, pc(v), ha="center", fontsize=7.5, color=NAVY)
a.text(2022.05, 90, "Colombianos", fontsize=8, color=GRAY, va="top", ha="left"); a.text(2024.55, 74, "Venezolanos", fontsize=8, color=NAVY, ha="center")
a.set_ylim(0, 105); a.set_xlim(2021.7, 2026.3); a.set_xticks(yrs); a.set_xticklabels(["2022", "2023", "2024", "2025", "2026*"]); a.set_ylabel("% afiliados")
a.set_title("a) Por año", loc="left", fontsize=8.5, style="italic")
coh = ["<=2016", "2017-2018", "2019-2020", "2021-2022", "2023+"]; vals = [t5.loc[c_, "afiliado_salud_pct"] for c_ in coh]
b.bar(range(5), vals, color=[NAVY] * 4 + [ACC], width=0.6)
for i, v in enumerate(vals): val(b, i, v + 1.2, pc(v))
b.set_xticks(range(5)); b.set_xticklabels(["hasta\n2016", "2017-\n2018", "2019-\n2020", "2021-\n2022", "desde\n2023"], fontsize=8); b.set_ylim(0, 105)
b.set_title("b) Por año de llegada al país, 2025-2026", loc="left", fontsize=8.5, style="italic")
save(fig, "gr2_afiliacion_salud.png")

# ---------------------------------------------------------------- Grafico 3: calendario de elegibilidad
el = pd.read_csv(TAB / "t12b_elegibilidad_por_anio.csv")
nuevos = el.titulares_elegibles_miles.diff().fillna(el.titulares_elegibles_miles.iloc[0])
fig, ax = plt.subplots(figsize=(W, 2.3)); fig.subplots_adjust(left=0.09, right=0.99, top=0.95, bottom=0.2)
ax.bar(el.anio, nuevos, color=NAVY, width=0.55)
for x_, v in zip(el.anio, nuevos):
    if v > 15: val(ax, x_, v + 8, f"{v:.0f}")
ax.set_xticks(el.anio); ax.set_xticklabels([f"{a_}\n({p_:.0f} %)".replace(".", ",") for a_, p_ in zip(el.anio, el.pct_titulares_con_5_anios_de_PPT)])
ax.set_ylim(0, 700); ax.set_ylabel("Miles de titulares")
ax.axvline(2031 - 0.4, color=ACC, lw=0.9, ls="--"); ax.text(2031 - 0.46, 660, "Vencimiento del PPT\n(28 de mayo de 2031)", color=ACC, fontsize=8, ha="right", va="top")
save(fig, "gr3_calendario_elegibilidad.png")

# ---------------------------------------------------------------- Grafico 4: asequibilidad
asq = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
fees = [("USD 464\n(vigente)", "USD 464 (56+408) vigente"), ("USD 232\n(propuesta)", "mitad (USD 232)"), ("USD 56\n(solo estudio)", "solo estudio USD 56 (se elimina la visa)")]
g = lambda f, k: asq[(asq.tarifa == f) & (asq.umbral == f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar")].pct_hogares_con_venezolano.iloc[0]
fig, ax = plt.subplots(figsize=(W, 2.25)); fig.subplots_adjust(left=0.09, right=0.99, top=0.95, bottom=0.2)
x = np.arange(3); w_ = 0.3
v1 = [g(f, 1) for _, f in fees]; v2 = [g(f, 2) for _, f in fees]
ax.bar(x - w_ / 2, v1, w_, color=NAVY, label="Más de 1 mes de ingreso"); ax.bar(x + w_ / 2, v2, w_, color=LGRAY, edgecolor="#9a9a9a", linewidth=0.5, label="Más de 2 meses de ingreso")
for xi, a_, b_ in zip(x, v1, v2): val(ax, xi - w_ / 2, a_ + 1, pc(a_)); val(ax, xi + w_ / 2, b_ + 1, pc(b_))
ax.set_xticks(x); ax.set_xticklabels([n for n, _ in fees]); ax.set_ylim(0, 80); ax.set_ylabel("% de hogares con venezolanos"); ax.legend(loc="upper right")
save(fig, "gr4_asequibilidad.png")


# ---------------------------------------------------------------- Grafico: ingreso laboral mediano por nivel educativo
t18 = pd.read_csv(TAB / "t18_ingreso_mediano_por_educacion.csv")
cats = ["Todos", "Hasta primaria", "Secundaria", "Media", "Técnica o tecnológica", "Universitaria o más"]
labs = ["Todos los\nocupados", "Hasta\nprimaria", "Secundaria", "Media", "Técnica o\ntecnológica", "Universitaria\no más"]
m = lambda g: [float(t18[(t18.grupo == g) & (t18.educacion == c_)].mediana_ingreso_smmlv.iloc[0]) for c_ in cats]
col_, ven_, afi_, noa_ = m("Colombianos"), m("Venezolanos"), m("Venezolanos afiliados a salud"), m("Venezolanos no afiliados")
fig, (a, b) = plt.subplots(2, 1, figsize=(W, 3.5), sharex=True); fig.subplots_adjust(left=0.09, right=0.99, top=0.95, bottom=0.15, hspace=0.36)
x = np.arange(len(cats)); w_ = 0.34
a.bar(x - w_ / 2, col_, w_, color=LGRAY, edgecolor="#9a9a9a", linewidth=0.5, label="Colombianos"); a.bar(x + w_ / 2, ven_, w_, color=NAVY, label="Venezolanos")
b.bar(x - w_ / 2, afi_, w_, color=NAVY, label="Venezolanos afiliados a salud"); b.bar(x + w_ / 2, noa_, w_, color=ACC, label="Venezolanos no afiliados")
for ax_, (u, v_) in ((a, (col_, ven_)), (b, (afi_, noa_))):
    for xi, uu, vv in zip(x, u, v_):
        if ax_ is a:
            val(ax_, xi - w_ / 2, uu + 0.03, pc(uu, 2)); val(ax_, xi + w_ / 2, vv + 0.03, pc(vv, 2))
        else:
            val(ax_, xi - w_ / 2, uu + 0.03, pc(uu, 2)); val(ax_, xi + w_ / 2, vv + 0.03, pc(vv, 2))
    ax_.set_ylim(0, 2.35); ax_.set_yticks([0, 0.5, 1, 1.5, 2]); ax_.set_yticklabels(["0", "0,5", "1", "1,5", "2"]); ax_.set_ylabel("Salarios mínimos")
    ax_.legend(loc="upper left", fontsize=8, ncol=2, handlelength=1.2, columnspacing=1.2)
a.set_title("a) Venezolanos y colombianos", loc="left", fontsize=8.5, style="italic", pad=3)
b.set_title("b) Venezolanos según afiliación a salud (indicador de regularización del estatus)", loc="left", fontsize=8.5, style="italic", pad=3)
b.set_xticks(x); b.set_xticklabels(labs, fontsize=8)
save(fig, "gr6_ingreso_educacion.png")


# ---------------------------------------------------------------- Grafico combinado: calendario (a) y asequibilidad (b)
el2 = pd.read_csv(TAB / "t12b_elegibilidad_por_anio.csv"); nuevos2 = el2.titulares_elegibles_miles.diff().fillna(el2.titulares_elegibles_miles.iloc[0])
asq2 = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
fees2 = [("USD 464\n(vigente)", "USD 464 (56+408) vigente"), ("USD 232", "mitad (USD 232)"), ("USD 56\n(estudio)", "solo estudio USD 56 (se elimina la visa)"), ("USD 0", None)]
g2 = lambda f, k: 0.0 if f is None else asq2[(asq2.tarifa == f) & (asq2.umbral == f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar")].pct_hogares_con_venezolano.iloc[0]
fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.3), gridspec_kw={"width_ratios": [1.25, 1]}); fig.subplots_adjust(left=0.09, right=0.99, top=0.88, bottom=0.25, wspace=0.28)
yrs2 = el2.anio.to_numpy()[:5]
a.bar(yrs2, nuevos2.to_numpy()[:5], color=NAVY, width=0.55)
for x_, v_ in zip(yrs2, nuevos2.to_numpy()[:5]): val(a, x_, v_ + 8, f"{v_:.0f}")
a.set_xticks(yrs2); a.set_xticklabels([f"{a_}\n({p_:.0f} %)".replace(".", ",") for a_, p_ in zip(el2.anio[:5], el2.pct_titulares_con_5_anios_de_PPT[:5])], fontsize=8)
a.set_ylim(0, 700); a.set_ylabel("Miles de titulares"); a.set_title("a) Titulares que cumplen 5 años de PPT", loc="left", fontsize=8.5, style="italic")
a.text(2029.5, 640, "El PPT vence\nel 28 de mayo\nde 2031", color=ACC, fontsize=7.5, ha="center", va="top")
x2 = np.arange(4); w2 = 0.34
v1 = [g2(f, 1) for _, f in fees2]; v2 = [g2(f, 2) for _, f in fees2]
b.bar(x2 - w2 / 2, v1, w2, color=NAVY, label="Más de 1 mes"); b.bar(x2 + w2 / 2, v2, w2, color=LGRAY, edgecolor="#9a9a9a", linewidth=0.5, label="Más de 2 meses")
for xi, a_, b_ in zip(x2, v1, v2): val(b, xi - w2 / 2, a_ + 1, pc(a_)); val(b, xi + w2 / 2, b_ + 1, pc(b_))
b.set_xticks(x2); b.set_xticklabels([n for n, _ in fees2], fontsize=8); b.set_ylim(0, 80); b.set_ylabel("% de hogares"); b.legend(loc="upper right", fontsize=7.5, handlelength=1.2)
b.set_title("b) Tarifa frente al ingreso del hogar", loc="left", fontsize=8.5, style="italic")
save(fig, "gr34_calendario_asequibilidad.png")

# ---------------------------------------------------------------- Grafico 5: demanda, recaudo y derrame (gratuidad)
cv = pd.read_csv(TAB / "t17_curva_precio_recaudo.csv"); cv = cv[cv.theta_meses_de_ingreso == 2].sort_values("tarifa_USD").reset_index(drop=True)
r12 = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
N = r12["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3; S = r12["beneficio_fiscal_anual_B_USD_por_persona"] * 5
F = cv.tarifa_USD.to_numpy().astype(float); raw = cv.conversion.to_numpy(); tau = pd.Series(raw).rolling(5, center=True, min_periods=1).mean().to_numpy(); tau[0] = raw[0]
Q = N * tau / 1e3
rec = N * tau * F / 1e6; tot = rec + N * tau * S / 1e6
at = lambda arr, f: float(np.interp(f, F, arr))
fig, (a, b) = plt.subplots(1, 2, figsize=(W, 2.65), gridspec_kw={"width_ratios": [1, 1.1]}); fig.subplots_adjust(left=0.09, right=0.99, top=0.9, bottom=0.19, wspace=0.3)
a.plot(Q, F, color=NAVY, lw=1.6)
q1 = at(Q, 464)
a.add_patch(Rectangle((0, 0), q1, 464, facecolor="#e4e4e4", edgecolor="#7a7a7a", linewidth=0.8, zorder=1))
a.text(q1 / 2, 464 - 45, f"Ingreso = {at(rec, 464):.0f} M", ha="center", fontsize=8, color=INK)
a.text(q1 + 14, 464 + 6, f"P = 464; {q1:.0f} mil", fontsize=8, ha="left")
q0 = at(Q, 0)
a.scatter([q0], [0], color=ACC, s=26, zorder=4, clip_on=False)
a.annotate(f"P = 0; {q0:.0f} mil\n(sin costo)", xy=(q0, 0), xytext=(585, 130), fontsize=8, color=ACC, ha="center", arrowprops=dict(arrowstyle="-", color=ACC, lw=0.7))
a.set_xlim(0, 1000); a.set_ylim(0, 700); a.set_xlabel("Titulares que convierten (miles)"); a.set_ylabel("Precio por persona (USD)")
a.set_title("a) Demanda e ingreso por la tarifa", loc="left", fontsize=8.5, style="italic")
b.fill_between(F, rec, tot, color="#dfe6ee", lw=0, label="Derrame")
b.plot(F, tot, color=NAVY, lw=1.6, label="Recaudo + derrame"); b.plot(F, rec, color=ACC, lw=1.6, label="Recaudo de la Cancillería")
for P, c in ((0, ACC), (464, INK)):
    b.axvline(P, ymax=0.62, color=c, lw=0.7, ls=":")
    b.scatter([P], [at(tot, P)], color=c, s=22, zorder=4, clip_on=False)
b.text(12, at(tot, 0) - 85, f"{at(tot, 0):.0f}", fontsize=8, color=ACC, ha="left", va="top")
b.text(464 - 14, at(tot, 464) - 40, f"{at(tot, 464):.0f}", fontsize=8, color=INK, ha="right", va="top")
b.set_xlim(0, 700); b.set_ylim(0, 1150); b.set_xlabel("Precio por persona (USD)"); b.set_ylabel("Millones de USD")
b.set_xticks([0, 232, 464, 600]); b.set_xticklabels(["0\n(sin costo)", "232", "464\n(vigente)", "600"], fontsize=8)
b.legend(loc="upper right", fontsize=8, handlelength=1.6)
b.set_title("b) Recaudo y valor total", loc="left", fontsize=8.5, style="italic")
save(fig, "gr5_demanda_recaudo_derrame.png")
print("ok", round(at(rec, 464)), round(at(tot, 464)), round(at(tot, 0)), round(at(tot, 232)), round(at(Q, 464)), round(q0))
