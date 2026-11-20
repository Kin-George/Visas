"""Visa-R / 17: peso de la tarifa de la Visa R sobre el ingreso laboral mensual (persona y hogar).
Persona: tarifa / ingreso laboral mediano de los ocupados venezolanos, por nivel educativo (t18).
Hogar: tarifa x n.o de venezolanos del hogar / ingreso laboral mensual del hogar (GEIH 2026, hogares con al menos un venezolano sin nacionalidad colombiana).
Salidas: Outputs/tables/t20_peso_tarifa_persona.csv y t20b_peso_tarifa_hogar.csv"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"
TRM, SMMLV_2026 = 3235.0, 1_750_905
FEES = {"USD 464 (vigente)": 464.0, "USD 232": 232.0, "USD 56 (estudio)": 56.0, "USD 0": 0.0}

# ---- persona (medianas de t18, salarios minimos de 2026)
t18 = pd.read_csv(TAB / "t18_ingreso_mediano_por_educacion.csv")
rows = []
for e in ["Todos", "Hasta primaria", "Secundaria", "Media", "Técnica o tecnológica", "Universitaria o más"]:
    m = float(t18[(t18.grupo == "Venezolanos") & (t18.educacion == e)].mediana_ingreso_smmlv.iloc[0]); ing = m * SMMLV_2026
    r = {"educacion": e, "ingreso_mediano_COP_millones": ing / 1e6}
    for k, f in FEES.items():
        r[f"pct_ingreso_{k}"] = 100 * f * TRM / ing
    r["dias_de_ingreso_tarifa_vigente"] = 30 * 464 * TRM / ing
    rows.append(r)
pd.DataFrame(rows).round(2).to_csv(TAB / "t20_peso_tarifa_persona.csv", index=False)

# ---- hogar
cols = ["anio", "mes", "directorio", "secuencia_p", "hogar", "fex_c18", "edad", "pais_nac", "nacionalidad", "inglabo"]
g = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
g = g[g.anio == 2026].apply(pd.to_numeric, errors="coerce")
g["hid"] = g.mes.astype(int).astype(str) + "_" + g.directorio.astype(int).astype(str) + "_" + g.secuencia_p.astype(int).astype(str) + "_" + g.hogar.astype(int).astype(str)
g["ven"] = (g.pais_nac == 862) & (g.nacionalidad == 3)
g["w"] = g.fex_c18 / g.mes.nunique()
g["menor18"] = g.edad < 18
h = g.groupby("hid").agg(w=("w", "first"), ing=("inglabo", lambda s: s.where(s > 0).sum()), n_ven=("ven", "sum"), m18=("menor18", "sum"))
h = h[h.n_ven > 0].copy()
h["ratio"] = np.where(h.ing > 0, 464 * TRM * h.n_ven / h.ing, np.inf)


def wmed(x, w):
    o = np.argsort(x.to_numpy()); xs, ws = x.to_numpy()[o], w.to_numpy()[o]; c = np.cumsum(ws) / ws.sum()
    return float(xs[np.searchsorted(c, 0.5)])


res = []
for lab, mask in [("Todos los hogares con venezolanos", h.index == h.index), ("Con al menos un menor de 18", h.m18 > 0), ("Sin menores de 18", h.m18 == 0),
                  ("Con 1 venezolano", h.n_ven == 1), ("Con 2 venezolanos", h.n_ven == 2), ("Con 3 o más venezolanos", h.n_ven >= 3)]:
    s = h[mask]; w = s.w
    res.append({"grupo": lab, "hogares_miles(escala GEIH)": w.sum() / 1e3, "mediana_tarifa_hogar_COP_millones": float(np.median(464 * TRM * s.n_ven) / 1e6),
                "mediana_pct_ingreso_mensual_del_hogar": 100 * wmed(s.ratio, w),
                "pct_hogares_tarifa_mayor_a_1_mes": 100 * float(np.average(s.ratio > 1, weights=w)),
                "pct_hogares_sin_ingreso_laboral": 100 * float(np.average(s.ing <= 0, weights=w))})
pd.DataFrame(res).round(1).to_csv(TAB / "t20b_peso_tarifa_hogar.csv", index=False)
pd.set_option("display.width", 220)
print(pd.DataFrame(rows).round(2).to_string()); print(pd.DataFrame(res).round(1).to_string())
