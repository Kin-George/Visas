"""Visa-R / 10: curva precio-recaudo-derrame de la tarifa de la Visa R.

Modelo ilustrativo (los supuestos estan a la vista; la demanda NO esta medida):
  conversion(F) = techo * P( F * TRM * n_ven_hogar <= theta * ingreso_laboral_mensual_del_hogar )
     - techo : 85% (quienes quieren quedarse: GEIH 83%, EPM 86%)
     - theta : meses de ingreso del hogar que un hogar esta dispuesto a pagar por la tarifa (central 2; sensibilidad 1 y 3)
     - la distribucion de ingresos de los hogares viene de la GEIH 2026 (hogares con venezolanos)
  recaudo(F)  = N * conversion(F) * F             (ingreso de la Cancilleria, una sola vez)
  derrame(F)  = N * conversion(F) * S             (beneficio fiscal/social por persona que convierte, S USD)
  total(F)    = recaudo + derrame
S: central = USD 196 por persona-anio (literatura JEEA, resumen) x 5 anios = USD 980; alternativa A = -USD 255 x 5 (costo de salud, nota 05).
Salidas: Outputs/tables/t17_curva_precio_recaudo.csv y t17b_optimos_por_escenario.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"
TRM = 3235.0
TECHO = 0.85
N = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3
b_B = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]["beneficio_fiscal_anual_B_USD_por_persona"]
b_A = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]["beneficio_fiscal_anual_A_USD_por_persona"]
H = 5                                                            # anios de derrame considerados (conservador)

cols = ["anio", "mes", "directorio", "secuencia_p", "hogar", "fex_c18", "pais_nac", "nacionalidad", "inglabo"]
g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
g = g[g.anio == 2026].apply(pd.to_numeric, errors="coerce")
g["hid"] = g.mes.astype(int).astype(str) + "_" + g.directorio.astype(int).astype(str) + "_" + g.secuencia_p.astype(int).astype(str) + "_" + g.hogar.astype(int).astype(str)
g["ven"] = (g.pais_nac == 862) & (g.nacionalidad == 3)
g["w"] = g.fex_c18 / g.mes.nunique()
h = g.groupby("hid").agg(w=("w", "first"), ing=("inglabo", lambda s: s.where(s > 0).sum()), n_ven=("ven", "sum"))
h = h[h.n_ven > 0]
wp = h.w * h.n_ven                                               # ponderador por persona venezolana


def conversion(F, theta):
    ok = (F * TRM * h.n_ven) <= theta * h.ing
    return TECHO * np.average(ok, weights=wp)


grid = np.arange(0, 701, 10)
rows = []
for theta in (1, 2, 3):
    for F in grid:
        tau = conversion(F, theta)
        rows.append({"theta_meses_de_ingreso": theta, "tarifa_USD": F, "conversion": tau,
                     "recaudo_USD_millones": N * tau * F / 1e6,
                     "derrame_literatura_USD_millones": N * tau * (b_B * H) / 1e6,
                     "derrame_costo_salud_USD_millones": N * tau * (b_A * H) / 1e6})
d = pd.DataFrame(rows)
d["total_con_derrame_USD_millones"] = d.recaudo_USD_millones + d.derrame_literatura_USD_millones
d["total_con_costo_salud_USD_millones"] = d.recaudo_USD_millones + d.derrame_costo_salud_USD_millones
d.round(3).to_csv(TAB / "t17_curva_precio_recaudo.csv", index=False)

opt = []
for theta, s in d.groupby("theta_meses_de_ingreso"):
    for lab, col in [("recaudo de la Cancillería", "recaudo_USD_millones"), ("recaudo + derrame (literatura)", "total_con_derrame_USD_millones"),
                     ("recaudo + costo de salud (contabilidad A)", "total_con_costo_salud_USD_millones")]:
        i = s[col].idxmax()
        opt.append({"theta": theta, "criterio": lab, "tarifa_optima_USD": s.loc[i, "tarifa_USD"], "conversion_en_el_optimo": s.loc[i, "conversion"],
                    "valor_USD_millones": s.loc[i, col]})
    for F in (464, 232, 56):
        j = s[s.tarifa_USD == (460 if F == 464 else (230 if F == 232 else 60))].iloc[0]
        opt.append({"theta": theta, "criterio": f"en USD {F} (aprox.)", "tarifa_optima_USD": j.tarifa_USD, "conversion_en_el_optimo": j.conversion,
                    "valor_USD_millones": j.recaudo_USD_millones})
o = pd.DataFrame(opt)
o.round(3).to_csv(TAB / "t17b_optimos_por_escenario.csv", index=False)
pd.set_option("display.width", 220)
print(f"N={N:,.0f} S_lit={b_B*H:,.0f} S_A={b_A*H:,.0f}")
print(o.round(2).to_string())
print(d[d.theta_meses_de_ingreso == 2][["tarifa_USD", "conversion", "recaudo_USD_millones", "total_con_derrame_USD_millones"]].iloc[::5].round(2).to_string())
