"""Visa-R / 07: horizonte de permanencia y emprendimiento de los venezolanos (GEIH 2025, EPM VIII-2025).

Pregunta: si muchos piensan quedarse, ¿cuanto de su actividad es emprendimiento/negocio propio, que tan formal es, y que se asocia con tener PPT?
GEIH: P3373S3 (pais nacimiento), P3374 (nacionalidad), P3375 (intencion de quedarse), P6430 (posicion), P1800 (tiene empleados),
      P3067 (negocio registrado en Camara de Comercio), P6775 (lleva contabilidad), P3069 (personas en el negocio), P6426 (meses en el trabajo).
EPM : sm6 (intencion a 1 anio), sm7 (razon para quedarse), ml7 (medio por el que consiguio el trabajo; 9 = independiente), ml31 (cuenta financiera).
"""
from pathlib import Path
import numpy as np
import pandas as pd

from _utils import wls_cluster

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"
GEIH = Path.home() / "Documents" / "Databases" / "GEIH" / "GEIH_2025_total.dta"
CACHE = ROOT / "Datos" / "geih_2025_negocios.pkl"

cols = ["MES", "FEX_C18", "P3373S3", "P3374", "P3375", "P6040", "OCI", "P6430", "P1800", "P3067", "P3065", "P6775", "P3069", "P6426",
        "INGLABO", "P6800", "EI", "P3373S3A1"]
if CACHE.exists():
    g = pd.read_pickle(CACHE)
else:
    disp = set(pd.io.stata.StataReader(GEIH).variable_labels())
    parts = [c for c in pd.read_stata(GEIH, chunksize=250_000, columns=[c for c in cols if c in disp], convert_categoricals=False)]
    g = pd.concat(parts, ignore_index=True).apply(pd.to_numeric, errors="coerce")
    g.to_pickle(CACHE)
g["w"] = g.FEX_C18 / g.MES.nunique()
g["grupo"] = np.select([(g.P3373S3 == 862) & (g.P3374 == 3), g.P3373S3.isna()], ["ven", "col"], default="otro")
# nota: P3373S3 nulo = nacido en Colombia o sin dato (el campo solo se llena si nacio en otro pais)
g = g[g.grupo.isin(["ven", "col"])]

# ------------------------------------------------------------------ 1. horizonte de permanencia (venezolanos)
v = g[g.grupo == "ven"].copy()
v["anios_en_col"] = 2025 - v.P3373S3A1.where(v.P3373S3A1.between(1950, 2025))
q = lambda x, w, p: x[x.notna()].sort_values().iloc[np.searchsorted(np.cumsum(w[x.notna()].loc[x[x.notna()].sort_values().index]) / w[x.notna()].sum(), p)]
h = {
    "pct_intencion_quedarse_si": 100 * np.average((v.P3375 == 1)[v.P3375.notna()], weights=v.w[v.P3375.notna()]),
    "pct_intencion_no_sabe": 100 * np.average(v.P3375.isin([3, 9])[v.P3375.notna()], weights=v.w[v.P3375.notna()]),
    "pct_con_5_o_mas_anios_en_colombia": 100 * np.average((v.anios_en_col >= 5)[v.anios_en_col.notna()], weights=v.w[v.anios_en_col.notna()]),
    "anios_en_colombia_mediana": float(q(v.anios_en_col, v.w, 0.5)),
}
v["coh"] = pd.cut(v.P3373S3A1, [0, 2016, 2018, 2020, 2022, 2100], labels=["<=2016", "2017-18", "2019-20", "2021-22", "2023+"])
byc = v[v.P3375.notna()].groupby("coh", observed=True).apply(lambda s: 100 * np.average(s.P3375 == 1, weights=s.w), include_groups=False)
byc.rename("pct_quiere_quedarse").round(1).to_csv(TAB / "t14_intencion_quedarse_por_cohorte.csv")

# ------------------------------------------------------------------ 2. emprendimiento y formalizacion de negocios (GEIH)
o = g[g.OCI == 1].copy()
rows = []
for gr, s in o.groupby("grupo"):
    ind = s[s.P6430.isin([4, 5])]                      # cuenta propia o patron
    pat = s[s.P6430 == 5]
    r = {"grupo": gr, "ocupados_miles": s.w.sum() / 1e3,
         "pct_cuenta_propia": 100 * np.average(s.P6430 == 4, weights=s.w),
         "pct_patron": 100 * np.average(s.P6430 == 5, weights=s.w),
         "independientes_miles": ind.w.sum() / 1e3,
         "pct_indep_con_empleados": 100 * np.average(ind.P1800 == 1, weights=ind.w) if ind.P1800.notna().any() else np.nan}
    m = ind.P3067.isin([1, 2])
    r["pct_indep_negocio_registrado_camara"] = 100 * np.average(ind.P3067[m] == 1, weights=ind.w[m]) if m.any() else np.nan
    m = ind.P6775.isin([1, 2])
    r["pct_indep_lleva_contabilidad"] = 100 * np.average(ind.P6775[m] == 1, weights=ind.w[m]) if m.any() else np.nan
    m = ind.P6426.notna()
    r["meses_en_el_negocio_mediana"] = float(q(ind.P6426, ind.w, 0.5)) if m.any() else np.nan
    m = ind.EI.isin([0, 1])
    r["pct_indep_formales_EI"] = 100 * np.average(ind.EI[m] == 1, weights=ind.w[m])
    ii = ind[(ind.INGLABO > 0)]
    r["ingreso_mediano_indep_COP"] = float(q(ii.INGLABO, ii.w, 0.5))
    rows.append(r)
t15 = pd.DataFrame(rows).set_index("grupo")
t15.round(1).T.to_csv(TAB / "t15_emprendimiento_venezolanos_vs_colombianos_2025.csv")

# empleos creados por patrones venezolanos (tamano del negocio P3069: codigos DANE)
pat = o[(o.grupo == "ven") & (o.P6430 == 5)]
tam = pat.groupby("P3069").w.sum()
tam = (100 * tam / tam.sum()).round(1)
tam.rename("pct_patrones_venezolanos_por_codigo_tamano_P3069").to_csv(TAB / "t15b_tamano_negocio_patrones_venezolanos.csv")

# ------------------------------------------------------------------ 3. EPM: permanencia y emprendimiento con y sin PPT
P = pd.read_stata(ROOT / "Datos/Raw/EPM_VIII_2025/extraido_EPM8_Personas/EPM8_Personas.dta", convert_categoricals=False)
e = P[(P.Ide16 == 1) & P.Ide14__2.notna()].copy()
e["ppt"] = (e.Ide14__2 == 1).astype(float)
w = e.FEX_PER
epm_tab = e.groupby("ppt").apply(lambda s: pd.Series({
    "permanecer_1_anio_pct": 100 * np.average(s.sm6 == 1, weights=s.FEX_PER),
    "regresar_a_Venezuela_pct": 100 * np.average(s.sm6 == 2, weights=s.FEX_PER),
    "tiene_cuenta_financiera_pct": 100 * np.average(s.ml31 == 1, weights=s.FEX_PER),
    "independiente_entre_ocupados_pct": 100 * np.average((s.ml7 == 9)[s.ml5 == 1], weights=s.FEX_PER[s.ml5 == 1]),
    "n": len(s)}), include_groups=False)
razones = e[e.sm6 == 1].groupby("sm7").FEX_PER.sum()
razones = (100 * razones / razones.sum()).round(1)
epm_tab.round(1).to_csv(TAB / "t16_epm_permanencia_y_emprendimiento_por_PPT.csv")
razones.rename("pct_razon_para_quedarse_(sm7)").to_csv(TAB / "t16b_epm_razon_para_quedarse.csv")

# ajustado: independiente (entre ocupados) y cuenta financiera ~ PPT + controles
entry = pd.cut(e.sm1, [0, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2100], labels=list("abcdefgh"))
X = pd.DataFrame({"const": 1.0, "ppt": e.ppt, "mujer": (e.Ide9 == 2).astype(float)}, index=e.index)
for nm, ser in [("edad", e.Ide10), ("entrada", entry), ("act", e.ml21), ("paso", e.sm5 == 2), ("cont", e.sm15)]:
    X = X.join(pd.get_dummies(ser.astype("category"), prefix=nm, drop_first=True, dtype=float))
X = X.fillna(0)
aj = []
for nm, y in [("Independiente entre ocupados (%)", (e.ml7 == 9).astype(float).where(e.ml5 == 1)),
              ("Cuenta financiera (%)", (e.ml31 == 1).astype(float)),
              ("Quiere permanecer 1 anio (%)", (e.sm6 == 1).astype(float))]:
    b, s, n = wls_cluster(y, X, e.FEX_PER, e.DIRECTORIO)
    aj.append({"indicador": nm, "dif_ajustada_pp": 100 * b[1], "ee": 100 * s[1], "IC95_inf": 100 * (b[1] - 1.96 * s[1]), "IC95_sup": 100 * (b[1] + 1.96 * s[1]), "n": n})
pd.DataFrame(aj).round(2).to_csv(TAB / "t16c_epm_ajustado_emprendimiento.csv", index=False)

pd.set_option("display.width", 220)
print(pd.Series(h).round(1).to_string()); print(byc.round(1).to_string()); print(t15.round(1).T.to_string())
print(tam.to_string()); print(epm_tab.round(1).to_string()); print(razones.to_string()); print(pd.DataFrame(aj).round(1).to_string())
