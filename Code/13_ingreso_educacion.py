"""Visa-R / 13: ingreso laboral mediano por nivel educativo (GEIH 2025-2026).

Grupos: colombianos; venezolanos (sin nacionalidad colombiana); venezolanos afiliados a salud (PROXY de regularizacion: en la EPM 91% de
quienes tienen PPT esta afiliado y 18% de quienes no lo tienen); venezolanos no afiliados.
La GEIH no pregunta por el PPT y la EPM no tiene ingresos: el cruce directo PPT x ingreso no es posible.
Ingreso = INGLABO de ocupados de 18+ con ingreso positivo, expresado en salarios minimos de cada anio (2025: 1.423.500; 2026: 1.750.905).
Salidas: Outputs/tables/t18_ingreso_mediano_por_educacion.csv, t18b_composicion_educativa.csv, t18c_prima_afiliacion_ajustada.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

from _utils import wls_cluster

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"
SMMLV = {2025: 1_423_500, 2026: 1_750_905}
EDU = {1: "Hasta primaria", 2: "Hasta primaria", 3: "Hasta primaria", 4: "Secundaria", 5: "Media", 6: "Media", 7: "Media",
       8: "Técnica o tecnológica", 9: "Técnica o tecnológica", 10: "Universitaria o más", 11: "Universitaria o más", 12: "Universitaria o más", 13: "Universitaria o más"}
ORD = ["Hasta primaria", "Secundaria", "Media", "Técnica o tecnológica", "Universitaria o más"]
MIN_N = 80                                          # no se reporta una mediana con menos observaciones

cols = ["anio", "mes", "directorio", "fex_c18", "dpto", "edad", "sexo", "clase", "educ", "pais_nac", "nacionalidad", "nace_donde", "llegada_anio", "oci", "inglabo", "p6800", "p6090"]
d = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
d = d[d.anio >= 2025].apply(pd.to_numeric, errors="coerce")
d["w"] = d.fex_c18 / d.groupby("anio")["mes"].transform("nunique")
d["ven"] = (d.pais_nac == 862) & (d.nacionalidad == 3)
d["col"] = d.nace_donde.isin([1, 2])
d = d[(d.ven | d.col) & (d.oci == 1) & (d.inglabo > 0) & (d.edad >= 18)].copy()
d["smmlv"] = d.anio.map(SMMLV)
d["ing"] = d.inglabo / d.smmlv
d["ing_hora"] = 1000 * d.ing / (d.p6800.where(d.p6800.between(1, 100)) * 4.345)       # milesimas de SMMLV por hora
d["edu"] = d.educ.map(EDU)
d["afil"] = d.p6090.map({1: True, 2: False})                                        # 9 = no sabe -> NaN


def wmed(x, w):
    m = x.notna() & w.notna()
    if not m.any(): return np.nan
    xs, ws = x[m].to_numpy(), w[m].to_numpy(); o = np.argsort(xs); c = np.cumsum(ws[o]) / ws.sum()
    return float(xs[o][np.searchsorted(c, 0.5)])


grupos = {"Colombianos": d.col, "Venezolanos": d.ven, "Venezolanos afiliados a salud": d.ven & (d.afil == True), "Venezolanos no afiliados": d.ven & (d.afil == False)}
rows = []
for g, mask in grupos.items():
    s = d[mask]
    for e in ["Todos"] + ORD:
        t = s if e == "Todos" else s[s.edu == e]
        n = len(t)
        rows.append({"grupo": g, "educacion": e, "n_muestra": n, "ocupados_miles": t.w.sum() / 1e3 / 2,
                     "mediana_ingreso_smmlv": wmed(t.ing, t.w) if n >= MIN_N else np.nan,
                     "mediana_ingreso_hora_milesimas_smmlv": wmed(t.ing_hora, t.w) if n >= MIN_N else np.nan})
t18 = pd.DataFrame(rows)
t18.round(3).to_csv(TAB / "t18_ingreso_mediano_por_educacion.csv", index=False)

# composicion educativa (ocupados)
comp = []
for g, mask in grupos.items():
    s = d[mask & d.edu.notna()]
    tot = s.w.sum()
    comp.append({"grupo": g, **{e: 100 * s.w[s.edu == e].sum() / tot for e in ORD}})
pd.DataFrame(comp).round(1).to_csv(TAB / "t18b_composicion_educativa.csv", index=False)

# prima de afiliacion (venezolanos): log ingreso por hora ~ afiliado + educacion + edad + sexo + urbano + depto + cohorte de llegada + anio
v = d[d.ven & d.afil.notna() & d.ing_hora.notna() & (d.ing_hora > 0)].copy()
v["lw"] = np.log(v.ing_hora)
coh = pd.cut(v.llegada_anio, [0, 2016, 2018, 2020, 2022, 2100], labels=["<=2016", "2017-18", "2019-20", "2021-22", "2023+"])
base = pd.DataFrame({"const": 1.0, "afil": v.afil.astype(float), "mujer": (v.sexo == 2).astype(float), "edad": v.edad, "edad2": v.edad ** 2 / 100,
                     "anio26": (v.anio == 2026).astype(float), "urbano": (v.clase == 1).astype(float)}, index=v.index)
res = []
for nombre, extra in [("sin controles", []), ("+ educación", ["edu"]), ("+ educación, edad, sexo, zona, departamento", ["edu", "dpto", "dem"]),
                      ("+ lo anterior y año de llegada", ["edu", "dpto", "dem", "coh"])]:
    X = base[["const", "afil"]].copy() if not extra else base.copy()
    if "edu" in extra: X = X.join(pd.get_dummies(v.edu, prefix="e", drop_first=True, dtype=float))
    if "dpto" in extra: X = X.join(pd.get_dummies(v.dpto, prefix="d", drop_first=True, dtype=float))
    if "coh" in extra: X = X.join(pd.get_dummies(coh.astype("category"), prefix="c", drop_first=True, dtype=float))
    if "dem" in extra: pass
    X = X.fillna(0)
    ok = v.lw.notna()
    b, se, n = wls_cluster(v.lw[ok], X[ok], v.w[ok], v.directorio[ok])
    res.append({"especificacion": nombre, "dif_pct": 100 * (np.exp(b[1]) - 1), "IC95_inf_pct": 100 * (np.exp(b[1] - 1.96 * se[1]) - 1),
                "IC95_sup_pct": 100 * (np.exp(b[1] + 1.96 * se[1]) - 1), "n": n})
pd.DataFrame(res).round(1).to_csv(TAB / "t18c_prima_afiliacion_ajustada.csv", index=False)

pd.set_option("display.width", 220)
pv = t18.pivot(index="educacion", columns="grupo", values="mediana_ingreso_smmlv").reindex(["Todos"] + ORD)
pn = t18.pivot(index="educacion", columns="grupo", values="n_muestra").reindex(["Todos"] + ORD)
print(pv.round(2).to_string()); print(pn.to_string())
print(pd.DataFrame(comp).round(1).to_string()); print(pd.DataFrame(res).to_string())

# robustez: solo zona urbana (los colombianos de baja educacion se concentran en zonas rurales)
rob = []
for g, mask in {"Colombianos": d.col, "Venezolanos": d.ven}.items():
    for zona, zm in (("urbano", d.clase == 1), ("rural", d.clase == 2)):
        s = d[mask & zm]
        for e in ["Todos"] + ORD:
            t = s if e == "Todos" else s[s.edu == e]
            rob.append({"grupo": g, "zona": zona, "educacion": e, "n_muestra": len(t), "mediana_ingreso_smmlv": wmed(t.ing, t.w) if len(t) >= MIN_N else np.nan})
rb = pd.DataFrame(rob)
rb.round(3).to_csv(TAB / "t18d_ingreso_por_educacion_y_zona.csv", index=False)
print(rb.pivot_table(index="educacion", columns=["zona", "grupo"], values="mediana_ingreso_smmlv").reindex(["Todos"] + ORD).round(2).to_string())
print("composicion zona:", d.groupby(["col", "clase"]).w.sum().groupby(level=0).apply(lambda s: s / s.sum()).round(2).to_dict())
