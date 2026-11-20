"""Visa-R / 04: aporte de los venezolanos a la demanda interna y escenarios de cobertura del PPT.

Piezas:
 (1) Masa salarial de los venezolanos ocupados (GEIH 2025) -> demanda de consumo bajo supuestos de ahorro y remesas.
 (2) Prima de formalidad: regresion salarial en GEIH (venezolanos ocupados, 2025-26) con controles.
 (3) Efecto del PPT sobre la formalidad de los ocupados: EPM VIII-2025 (asociacion ajustada).
 (4) Escenarios: cuanto aumentaria la masa salarial si el PPT pasara de la cobertura actual a 80% o 100%.

Todo son ESCENARIOS con supuestos explicitos, no estimaciones causales.
"""
from pathlib import Path
import numpy as np
import pandas as pd

from _utils import wls_cluster

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"

# ---------------------------------------------------------------- GEIH
cols = ["anio", "mes", "directorio", "fex_c18", "dpto", "edad", "sexo", "educ", "pais_nac", "nacionalidad",
        "llegada_anio", "oci", "inglabo", "p6800", "p6920", "ei", "rama2d_r4", "clase"]
d = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
d = d[(d.anio >= 2025) & (pd.to_numeric(d.pais_nac, errors="coerce") == 862) & (pd.to_numeric(d.nacionalidad, errors="coerce") == 3)].copy()
d = d.apply(pd.to_numeric, errors="coerce")
d["nm"] = d.groupby("anio")["mes"].transform("nunique")
d["w"] = d.fex_c18 / d.nm
SMMLV = {2025: 1423500, 2026: 1750905}
d["smmlv"] = d.anio.map(SMMLV)
o = d[(d.oci == 1) & (d.inglabo > 0)].copy()
o["ing_smmlv"] = o.inglabo / o.smmlv
o["formal"] = (o.ei == 1).astype(float)
o["horas"] = o.p6800.where(o.p6800.between(1, 100))
o["lw"] = np.log(o.ing_smmlv / (o.horas * 4.345))

# (1) masa salarial 2025
o25 = o[o.anio == 2025]
masa_mes = (o25.w * o25.inglabo).sum()                  # COP/mes (promedio 2025)
n_ocup = d[(d.anio == 2025) & (d.oci == 1)].w.sum()
ing_medio_inf = np.average(o25.inglabo[o25.formal == 0], weights=o25.w[o25.formal == 0])
ing_medio_for = np.average(o25.inglabo[o25.formal == 1], weights=o25.w[o25.formal == 1])
share_formal = np.average(o25.formal, weights=o25.w)

# (2) prima de formalidad: log salario/hora ~ formal + controles (educ, edad, sexo, cohorte, depto, rama, anio)
X = pd.DataFrame({"const": 1.0, "formal": o.formal, "mujer": (o.sexo == 2).astype(float),
                  "edad": o.edad, "edad2": o.edad ** 2 / 100, "anio26": (o.anio == 2026).astype(float),
                  "urbano": (o.clase == 1).astype(float)}, index=o.index)
coh = pd.cut(o.llegada_anio, [0, 2016, 2018, 2020, 2022, 2100], labels=["<=2016", "2017-18", "2019-20", "2021-22", "2023+"])
for nm, ser in [("educ", o.educ), ("coh", coh), ("dpto", o.dpto), ("rama", o.rama2d_r4)]:
    X = X.join(pd.get_dummies(ser.astype("category"), prefix=nm, drop_first=True, dtype=float))
ok = o.lw.notna() & np.isfinite(o.lw)
beta, se, n = wls_cluster(o.lw[ok], X[ok].fillna(0), o.w[ok], o.directorio[ok])
b_f, se_f = beta[1], se[1]
beta0, se0, _ = wls_cluster(o.lw[ok], X.loc[ok, ["const", "formal"]], o.w[ok], o.directorio[ok])
prima = {"simple_log": beta0[1], "ajustada_log": b_f, "ee_ajustada": se_f, "n": n}
prima_pct = {k: 100 * (np.exp(v) - 1) for k, v in [("simple", beta0[1]), ("ajustada", b_f),
                                                     ("ajustada_inf", b_f - 1.96 * se_f), ("ajustada_sup", b_f + 1.96 * se_f)]}

# ---------------------------------------------------------------- EPM: efecto del PPT sobre la formalidad de ocupados
P = pd.read_stata(ROOT / "Datos/Raw/EPM_VIII_2025/extraido_EPM8_Personas/EPM8_Personas.dta", convert_categoricals=False)
H = pd.read_stata(ROOT / "Datos/Raw/EPM_VIII_2025/extraido_EPM8_Hogares/EPM8_Hogares.dta", convert_categoricals=False)
e = P[(P.Ide16 == 1) & P.Ide14__2.notna()].copy()
e["ppt"] = (e.Ide14__2 == 1).astype(float)
entry = pd.cut(e.sm1, [0, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2100], labels=list("abcdefgh"))
XE = pd.DataFrame({"const": 1.0, "ppt": e.ppt, "mujer": (e.Ide9 == 2).astype(float)}, index=e.index)
for nm, ser in [("edad", e.Ide10), ("entrada", entry), ("act", e.ml21), ("paso", e.sm5 == 2), ("cont", e.sm15)]:
    XE = XE.join(pd.get_dummies(ser.astype("category"), prefix=nm, drop_first=True, dtype=float))
XE = XE.fillna(0)
trab = e.ml5 == 1
ep = {}
for nm, y in [("pension_ocupados", (e.sd2 == 1).astype(float).where(trab & e.sd2.isin([1, 2]))),
              ("contrato_escrito_ocupados", (e.ml3_19 == 2).astype(float).where(trab & e.ml3_19.isin([1, 2])))]:
    bb, ss, nn = wls_cluster(y, XE, e.FEX_PER, e.DIRECTORIO)
    ep[nm] = (100 * bb[1], 100 * ss[1], nn)
cobertura_actual = 100 * np.average(e.ppt, weights=e.FEX_PER)

# ---------------------------------------------------------------- (1) tabla de consumo
rows = []
for ahorro in (0.0, 0.10, 0.20):
    for rem in (0.0, 0.10, 0.20):
        rows.append({"propension_a_ahorrar": ahorro, "fraccion_enviada_como_remesas": rem,
                     "consumo_anual_billones_COP": masa_mes * 12 * (1 - ahorro - rem) / 1e12})
t8 = pd.DataFrame(rows)
t8.round(2).to_csv(TAB / "t8_consumo_anual_venezolanos_supuestos.csv", index=False)

# ---------------------------------------------------------------- (4) escenarios de cobertura del PPT
sc = []
for cov in (cobertura_actual, 80.0, 100.0):
    dcov = (cov - cobertura_actual) / 100
    for lab, pe in [("PPT -> pension: punto", ep["pension_ocupados"][0]),
                    ("PPT -> pension: limite inferior", ep["pension_ocupados"][0] - 1.96 * ep["pension_ocupados"][1]),
                    ("PPT -> pension: limite superior", ep["pension_ocupados"][0] + 1.96 * ep["pension_ocupados"][1])]:
        dformal = dcov * pe / 100                       # cambio en la tasa de formalidad (fraccion de ocupados)
        for pl, pr in [("prima 0%", 0.0), ("prima ajustada", prima_pct["ajustada"] / 100),
                       ("prima simple", prima_pct["simple"] / 100)]:
            gain_mes = dformal * n_ocup * ing_medio_inf * pr
            sc.append({"cobertura_PPT_pct": round(cov, 1), "supuesto_efecto_PPT_formalidad": lab, "prima_salarial": pl,
                       "delta_tasa_formalidad_pp": 100 * dformal,
                       "trabajadores_que_se_formalizan_miles": dformal * n_ocup / 1e3,
                       "aumento_masa_salarial_mensual_miles_millones_COP": gain_mes / 1e9,
                       "aumento_pct_de_la_masa_salarial": 100 * gain_mes / masa_mes})
t9 = pd.DataFrame(sc)
t9.round(3).to_csv(TAB / "t9_escenarios_cobertura_PPT.csv", index=False)

resumen = pd.Series({
    "masa_salarial_mensual_miles_millones_COP_2025": masa_mes / 1e9,
    "masa_salarial_anual_billones_COP_2025": masa_mes * 12 / 1e12,
    "ocupados_venezolanos_miles_2025": n_ocup / 1e3,
    "tasa_formalidad_pct_2025": 100 * share_formal,
    "ingreso_medio_informales_COP": ing_medio_inf, "ingreso_medio_formales_COP": ing_medio_for,
    "prima_formalidad_simple_pct": prima_pct["simple"], "prima_formalidad_ajustada_pct": prima_pct["ajustada"],
    "prima_ajustada_IC95_inf_pct": prima_pct["ajustada_inf"], "prima_ajustada_IC95_sup_pct": prima_pct["ajustada_sup"],
    "n_regresion_prima": n,
    "EPM_cobertura_PPT_pct": cobertura_actual,
    "EPM_efecto_PPT_pension_ocupados_pp": ep["pension_ocupados"][0], "EPM_ee_pension_ocupados": ep["pension_ocupados"][1],
    "EPM_efecto_PPT_contrato_escrito_pp": ep["contrato_escrito_ocupados"][0], "EPM_ee_contrato": ep["contrato_escrito_ocupados"][1],
})
resumen.round(2).to_csv(TAB / "t8b_resumen_demanda_interna.csv", header=["valor"])
pd.set_option("display.width", 220)
print(resumen.round(2).to_string())
print(t8.round(2).to_string())
print(t9[t9.cobertura_PPT_pct == 100][t9.supuesto_efecto_PPT_formalidad == "PPT -> pension: punto"].round(2).to_string())
print(t9[(t9.cobertura_PPT_pct == 100) & (t9.prima_salarial == "prima ajustada")].round(2).to_string())
