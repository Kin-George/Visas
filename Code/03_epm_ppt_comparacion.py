"""Visa-R / 03: EPM ronda VIII-2025: condiciones de migrantes venezolanos con PPT vs sin PPT.

Muestra: personas con nacionalidad venezolana (Ide16 = 1), a quienes se les pregunta por permisos (Ide14).
Tratamiento: tiene PPT (Ide14__2 = 1).  Controles ("sin PPT"): (A) todos los demas; (B) solo quienes declaran no tener ningun permiso (Ide14__5 = 1).
Metodo: minimos cuadrados ponderados (FEX_PER), modelo de probabilidad lineal; errores robustos agrupados por hogar (DIRECTORIO).
Controles: sexo, grupo de edad, anio de primera entrada, actividad en Venezuela antes de migrar, entrada por paso no oficial,
contactos previos en Colombia, origen (estado de Venezuela con >=150 registros).
IMPORTANTE: es asociacion, no causalidad. El PPT no se asigna al azar: depende de la fecha y forma de entrada, y de haberse inscrito.
"""
from pathlib import Path
import numpy as np
import pandas as pd

from _utils import wls_cluster

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "Datos" / "Raw" / "EPM_VIII_2025"
OUT = ROOT / "Outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

P = pd.read_stata(RAW / "extraido_EPM8_Personas" / "EPM8_Personas.dta", convert_categoricals=False)
H = pd.read_stata(RAW / "extraido_EPM8_Hogares" / "EPM8_Hogares.dta", convert_categoricals=False)
d = P.merge(H[["DIRECTORIO", "SECUENCIA_P", "ch7", "ch15", "Ide12", "ch9"]], on=["DIRECTORIO", "SECUENCIA_P"], how="left")
d = d[(d.Ide16 == 1) & d.Ide14__2.notna()].copy()
d["ppt"] = (d.Ide14__2 == 1).astype(float)
d["ninguno"] = (d.Ide14__5 == 1)
d["otro_permiso"] = (d.Ide14__2 != 1) & (d.Ide14__5 != 1)

b = lambda cond, base=None: cond.astype(float).where(base) if base is not None else cond.astype(float)
trab = d.ml5 == 1
Y = {
    "Afiliado a salud (%)": b(d.ml17 == 1, d.ml17.isin([1, 2])),
    "  de los afiliados: contributivo (%)": b(d.ml18 == 1, d.ml18.isin([1, 2, 3])),
    "Afiliado a pension (%)": b(d.sd2 == 1, d.sd2.isin([1, 2])),
    "Trabajo la semana pasada (%)": b(trab),
    "Buscando trabajo (%)": b(d.ml5 == 2),
    "  ocupados: contrato escrito (%)": b(d.ml3_19 == 2, trab & d.ml3_19.isin([1, 2])),
    "  ocupados: horas semanales": d.ml3_18.where(trab & d.ml3_18.between(1, 100)),
    "  ocupados: lleva > 1 anio en el trabajo (%)": b(d.ml6 == 5, trab & d.ml6.notna()),
    "Cuenta en entidad financiera (%)": b(d.ml31 == 1, d.ml31.isin([1, 2])),
    "Envio remesas el ultimo mes (%)": b(d.ir7 == 1, d.ir7.isin([1, 2])),
    "Salud buena o muy buena (%)": b(d.sd1.isin([1, 2]), d.sd1.notna()),
    "Necesito servicio de salud y no pudo acceder (%)": b(d.sd4 == 2, d.sd4.isin([1, 2])),
    "Hogar: 3 comidas al dia o mas (%)": b(d.ch7 == 3, d.ch7.isin([1, 2, 3])),
    "Hogar: dificultad para comprar alimentos (%)": b(d.ch15 == 1, d.ch15.isin([1, 2])),
    "Se ha sentido discriminado (%)": b(d.pd1 == 1, d.pd1.isin([1, 2])),
    "Piensa permanecer en Colombia 1 anio (%)": b(d.sm6 == 1, d.sm6.notna()),
}

# controles
entry = pd.cut(d.sm1, [0, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2100],
               labels=["<=2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024+"])
X = pd.DataFrame({"mujer": (d.Ide9 == 2).astype(float)}, index=d.index)
for lab, ser in [("edad", d.Ide10), ("entrada", entry), ("act_ven", d.ml21), ("paso_no_oficial", (d.sm5 == 2)),
                 ("contactos", d.sm15), ("origen", d.Estado.where(d.Estado.map(d.Estado.value_counts()) >= 150, -1))]:
    dm = pd.get_dummies(ser.astype("category"), prefix=lab, drop_first=True, dtype=float)
    X = X.join(dm)
X = X.fillna(0)


rows = []
for spec, mask in [("A: PPT vs todos los demas", pd.Series(True, index=d.index)),
                   ("B: PPT vs ningun permiso", d.ppt.eq(1) | d.ninguno)]:
    s = d[mask]
    for name, y in Y.items():
        ys = y[mask]
        ok = ys.notna()
        w = s.FEX_PER
        tr, co = (s.ppt == 1) & ok, (s.ppt == 0) & ok
        if tr.sum() < 30 or co.sum() < 30:
            continue
        scale = 100 if "(%)" in name else 1
        m1 = np.average(ys[tr], weights=w[tr]) * scale
        m0 = np.average(ys[co], weights=w[co]) * scale
        # ajustado
        xx = pd.concat([pd.Series(1.0, index=s.index, name="const"), s.ppt.rename("ppt"), X.loc[s.index]], axis=1)
        beta, se, n = wls_cluster(ys, xx, w, s.DIRECTORIO)
        # error de la diferencia simple (sin controles)
        beta0, se0, _ = wls_cluster(ys, xx[["const", "ppt"]], w, s.DIRECTORIO)
        rows.append({"especificacion": spec, "indicador": name.strip(), "media_con_PPT": m1, "media_sin_PPT": m0,
                     "dif_simple": beta0[1] * scale, "ee_simple": se0[1] * scale,
                     "dif_ajustada": beta[1] * scale, "ee_ajustada": se[1] * scale,
                     "IC95_inf": (beta[1] - 1.96 * se[1]) * scale, "IC95_sup": (beta[1] + 1.96 * se[1]) * scale,
                     "n": n, "n_con_PPT": int(tr.sum())})
res = pd.DataFrame(rows)
res.round(2).to_csv(OUT / "t7_epm_ppt_vs_sin_ppt.csv", index=False)
pd.set_option("display.width", 250)
print(res[["especificacion", "indicador", "media_con_PPT", "media_sin_PPT", "dif_simple", "dif_ajustada", "ee_ajustada", "n"]].round(1).to_string())

# distribucion del PPT por anio de entrada: quien tiene PPT
g = d.groupby(entry, observed=True).apply(lambda s: pd.Series({"n": len(s), "pct_PPT": 100 * np.average(s.ppt, weights=s.FEX_PER),
                                                              "pct_ningun_permiso": 100 * np.average(s.ninguno, weights=s.FEX_PER)}), include_groups=False)
g.round(1).to_csv(OUT / "t7b_epm_ppt_por_anio_entrada.csv")
print(g.round(1))
print("PPT por anio de obtencion (Ide14_2):", d[d.ppt == 1].groupby("Ide14_2").FEX_PER.sum().div(d[d.ppt == 1].FEX_PER.sum()).mul(100).round(1).to_dict())
