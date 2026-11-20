"""Visa-R / 14: composicion de los hogares con venezolanos (responsabilidades de cuidado) y tarifa frente al ingreso individual por nivel educativo.
Responde al comentario 'sustentar con data' (hogares con ingresos bajos, empleo informal o responsabilidades de cuidado).
Salidas: Outputs/tables/t19_hogares_con_menores.csv y t19b_tarifa_vs_ingreso_individual.csv"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"
TRM, SMMLV_2026, FEE_USD = 3235.0, 1_750_905, 464.0

cols = ["anio", "mes", "directorio", "secuencia_p", "hogar", "fex_c18", "edad", "pais_nac", "nacionalidad", "sexo", "parentesco"]
g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
g = g[g.anio == 2026].apply(pd.to_numeric, errors="coerce")
g["hid"] = g.mes.astype(int).astype(str) + "_" + g.directorio.astype(int).astype(str) + "_" + g.secuencia_p.astype(int).astype(str) + "_" + g.hogar.astype(int).astype(str)
g["ven"] = (g.pais_nac == 862) & (g.nacionalidad == 3)
g["w"] = g.fex_c18 / g.mes.nunique()
g["menor15"] = g.edad < 15; g["menor18"] = g.edad < 18; g["menor5"] = g.edad < 5
h = g.groupby("hid").agg(w=("w", "first"), n=("w", "size"), n_ven=("ven", "sum"), m5=("menor5", "sum"), m15=("menor15", "sum"), m18=("menor18", "sum"))
h = h[h.n_ven > 0]
wm = lambda x: float(np.average(x, weights=h.w))
res = {"hogares_con_venezolano_miles(escala GEIH)": h.w.sum() / 1e3, "personas_por_hogar": wm(h.n), "venezolanos_por_hogar": wm(h.n_ven),
       "pct_hogares_con_menor_de_5": 100 * wm(h.m5 > 0), "pct_hogares_con_menor_de_15": 100 * wm(h.m15 > 0), "pct_hogares_con_menor_de_18": 100 * wm(h.m18 > 0),
       "menores_de_18_por_hogar": wm(h.m18)}
v = g[g.ven]
res["pct_venezolanos_menores_de_18"] = 100 * float(np.average(v.menor18, weights=v.w))
pd.Series(res).round(2).to_csv(TAB / "t19_hogares_con_menores.csv", header=["valor"])

t18 = pd.read_csv(TAB / "t18_ingreso_mediano_por_educacion.csv")
fee_cop = FEE_USD * TRM
rows = []
for e in ["Todos", "Hasta primaria", "Secundaria", "Media", "Técnica o tecnológica", "Universitaria o más"]:
    m = float(t18[(t18.grupo == "Venezolanos") & (t18.educacion == e)].mediana_ingreso_smmlv.iloc[0])
    rows.append({"educacion": e, "ingreso_mediano_smmlv": m, "ingreso_mediano_COP_2026": m * SMMLV_2026, "tarifa_USD464_en_meses_de_ingreso_mediano": fee_cop / (m * SMMLV_2026)})
pd.DataFrame(rows).round(2).to_csv(TAB / "t19b_tarifa_vs_ingreso_individual.csv", index=False)
print(pd.Series(res).round(1).to_string()); print(pd.DataFrame(rows).round(2).to_string())
