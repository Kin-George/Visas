"""Visa-R / 06: costo de la Visa R (USD 464) para titulares del PPT: asequibilidad, ingresos por tarifa y escenarios de eliminarla.

Marco normativo: Visa R para titulares de PEP/PPT con 5 anios de titularidad (Res. 5477, art. 91). Tarifa OFICIAL (pagina 'Costos tramites'
de la Cancilleria, categoria 'Residente - Tiempo acumulado Estatuto Temporal', captura aportada por el usuario el 12-nov-2026):
estudio USD 56 + visa USD 408 = USD 464 (EUR 44 + 314 en Europa y Cuba); el timbre puede ir aparte. El PPT vence el 28-may-2031.
TRM aprox. 3.235 COP/USD (6-nov-2026, prensa).

Salidas: t12_visaR_resumen.csv, t12b_elegibilidad_por_anio.csv, t12c_asequibilidad_hogares.csv, t13_escenarios_tarifa.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"

TRM = 3235.0
SMMLV_2026 = 1_750_905
BASE_F = 464.0
FEES = {"USD 464 (56+408) vigente": BASE_F, "mitad (USD 232)": 232.0, "solo estudio USD 56 (se elimina la visa)": 56.0, "gratis": 0.0}
SUPUESTOS_PIB_USD = 529_154_660 / 0.0015          # PIB implicito en OIM/Equilibrium: aporte de USD 529 M = 0,15% del PIB

res = pd.read_csv(TAB / "t8b_resumen_demanda_interna.csv", index_col=0)["valor"]
cov = res["EPM_cobertura_PPT_pct"] / 100          # 65,6% con PPT (EPM)
base = pd.read_csv(TAB / "t10_fiscal_base_2025.csv", index_col=0)["valor"]
POB = base["poblacion_venezolana_miles"] * 1e3
N = POB * cov                                       # titulares de PPT a escala GEIH

# ----------------------------------------------------------- edad (menores) y asequibilidad (GEIH 2026)
cols = ["anio", "mes", "directorio", "secuencia_p", "hogar", "fex_c18", "edad", "pais_nac", "nacionalidad", "inglabo", "oci"]
g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
g = g[g.anio == 2026].apply(pd.to_numeric, errors="coerce")
g["hid"] = g.mes.astype(int).astype(str) + "_" + g.directorio.astype(int).astype(str) + "_" + g.secuencia_p.astype(int).astype(str) + "_" + g.hogar.astype(int).astype(str)
g["ven"] = (g.pais_nac == 862) & (g.nacionalidad == 3)
g["w"] = g.fex_c18 / g.mes.nunique()
v = g[g.ven]
pct_menor18 = 100 * np.average(v.edad < 18, weights=v.w)
pct_menor15 = 100 * np.average(v.edad < 15, weights=v.w)
h = g.groupby("hid").agg(w=("w", "first"), ing=("inglabo", lambda s: s.where(s > 0).sum()), n_ven=("ven", "sum"), n=("w", "size"))
h = h[h.n_ven > 0].copy()
rows = []
for lab, F in FEES.items():
    if F == 0:
        continue
    fee_cop = F * TRM
    tot = fee_cop * h.n_ven                         # si todos los miembros venezolanos deben pagar
    for k in (1, 2, 3):
        rows.append({"tarifa": lab, "fee_por_persona_COP": fee_cop, "fee_por_persona_en_SMMLV": fee_cop / SMMLV_2026,
                     "umbral": f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar",
                     "pct_hogares_con_venezolano": 100 * np.average(tot >= k * h.ing, weights=h.w),
                     "tarifa_hogar_mediana_COP": float(np.median(tot))})
    rows.append({"tarifa": lab, "fee_por_persona_COP": fee_cop, "fee_por_persona_en_SMMLV": fee_cop / SMMLV_2026,
                 "umbral": "tarifa del hogar >= 3 SMMLV", "pct_hogares_con_venezolano": 100 * np.average(tot >= 3 * SMMLV_2026, weights=h.w),
                 "tarifa_hogar_mediana_COP": float(np.median(tot))})
asq = pd.DataFrame(rows)
asq.round(1).to_csv(TAB / "t12c_asequibilidad_hogares.csv", index=False)
n_h = h.n_ven.mean()

# ----------------------------------------------------------- elegibilidad por anio (EPM: anio de obtencion del PPT)
P = pd.read_stata(ROOT / "Datos/Raw/EPM_VIII_2025/extraido_EPM8_Personas/EPM8_Personas.dta", convert_categoricals=False)
e = P[(P.Ide16 == 1) & (P.Ide14__2 == 1)]
dist = e.groupby("Ide14_2").FEX_PER.sum()
dist = dist / dist.sum()
yrs = range(2026, 2032)
el = pd.Series({y: dist[dist.index + 5 <= y].sum() for y in yrs})
el_t = pd.DataFrame({"anio": list(yrs), "pct_titulares_con_5_anios_de_PPT": 100 * el.values,
                     "titulares_elegibles_miles": el.values * N / 1e3})
el_t.round(1).to_csv(TAB / "t12b_elegibilidad_por_anio.csv", index=False)
# (ignora tiempo previo con PEP, asi que subestima la elegibilidad)

# ----------------------------------------------------------- escenarios de tarifa
BENEF_USD_HOGAR = 1056 - 610                       # JEEA/JDC: ahorro de costo neto por hogar con PEP [resumen, no verificado]
b_B = BENEF_USD_HOGAR / n_h                       # USD por persona-anio (contabilidad B)
# contabilidad A (mia): costo neto de regularizar por persona-anio
t11 = pd.read_csv(TAB / "t11_escenarios_fiscales_PPT.csv")
bal100 = t11[(t11.cobertura_PPT_pct == 100) & (t11.efecto_PPT_formalidad == "central")]["balance_amplio_mil_millones(aportes salud+IVA-UPC)"].iloc[0] * 1e9
b_A = (bal100 / (POB * (1 - cov))) / TRM         # USD por persona-anio (negativo = costo)
sc = []
for H in (5, 10):
    for lab, F in FEES.items():
        for tau in (0.5, 0.7, 0.9):
            rev = N * tau * F / 1e6                  # USD millones, unica vez
            sc.append({"horizonte_anios_post_2031": H, "tarifa": lab, "tasa_de_conversion": tau,
                       "ingreso_por_tarifa_USD_millones": rev, "ingreso_por_tarifa_COP_billones": rev * 1e6 * TRM / 1e12,
                       "ingreso_como_pct_del_PIB": 100 * rev * 1e6 / SUPUESTOS_PIB_USD,
                       "personas_que_convierten_miles": N * tau / 1e3,
                       "personas_que_quedan_irregulares_en_2031_miles": N * (1 - tau) / 1e3,
                       "efecto_fiscal_anual_de_cada_convertido_USD_(B_literatura)": b_B,
                       "efecto_fiscal_anual_de_cada_convertido_USD_(A_UPC)": b_A})
t13 = pd.DataFrame(sc)
t13.round(2).to_csv(TAB / "t13_escenarios_tarifa.csv", index=False)

# punto de equilibrio: conversion necesaria si la tarifa baja de F a F' para no perder fiscalmente (contabilidad B)
be = []
for H in (5, 10):
    for tau in (0.5, 0.7):
        for lab, Fp in [("gratis", 0.0), ("solo estudio USD 56", 56.0), ("mitad USD 232", 232.0)]:
            tp = tau * (b_B * H + BASE_F) / (b_B * H + Fp)
            be.append({"horizonte": H, "conversion_con_tarifa_464": tau, "tarifa_alternativa": lab,
                       "conversion_necesaria_para_no_perder": min(tp, 9.99), "factible(<=100%)": tp <= 1.0})
pd.DataFrame(be).round(3).to_csv(TAB / "t13b_punto_equilibrio_tarifa.csv", index=False)

resumen = pd.Series({
    "TRM_COP_por_USD": TRM, "titulares_PPT_estimados_miles(escala GEIH)": N / 1e3,
    "pct_menores_18": pct_menor18, "pct_menores_15": pct_menor15, "personas_venezolanas_por_hogar_promedio": n_h,
    "PIB_implicito_USD_miles_millones": SUPUESTOS_PIB_USD / 1e9,
    "ingreso_maximo_por_tarifa_464_USD_millones": N * BASE_F / 1e6, "ingreso_maximo_por_tarifa_464_COP_billones": N * BASE_F * TRM / 1e12,
    "ingreso_maximo_464_como_pct_PIB": 100 * N * BASE_F / SUPUESTOS_PIB_USD,
    "beneficio_fiscal_anual_B_USD_por_persona": b_B, "beneficio_fiscal_anual_A_USD_por_persona": b_A,
    "pct_sin_permiso_razon_dificultad_con_la_entidad(EPM)": 43.0, "pct_sin_permiso_no_cumple_requisitos(EPM)": 17.7,
})
resumen.round(2).to_csv(TAB / "t12_visaR_resumen.csv", header=["valor"])
pd.set_option("display.width", 250)
print(resumen.round(2).to_string()); print(el_t.round(1).to_string())
print(asq.round(1).to_string()); print(pd.DataFrame(be).round(2).to_string())
print(t13[(t13.horizonte_anios_post_2031 == 10) & (t13.tasa_de_conversion == 0.7)].round(2).T.to_string())
