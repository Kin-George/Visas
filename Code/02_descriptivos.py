"""Visa-R / 02: descriptivos de la poblacion venezolana en Colombia (GEIH 2022-2026).

Entrada : Visa-R/Datos/geih_migracion_2021_2026.pkl  (script 01)
Salida  : Visa-R/Outputs/tables/*.csv y Visa-R/Outputs/Figures/*.png

Grupos
  ven_ext  : nacido en Venezuela y SIN nacionalidad colombiana (P3374 = 3)  <- migrante venezolano
  ven_col  : nacido en Venezuela con nacionalidad colombiana (retornados / hijos de colombianos / binacionales)
  otro_ext : nacido en otro pais
  col      : nacido en Colombia
2021 se excluye: el modulo de migracion solo se aplico parcialmente (5.6 mil registros vs ~35-44 mil).
2026 cubre enero-agosto.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"
FIG = ROOT / "Outputs" / "Figures"
TAB.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

SMMLV = {2021: 908526, 2022: 1000000, 2023: 1160000, 2024: 1300000, 2025: 1423500, 2026: 1750905}
EDUC = {1: "Ninguno/preescolar", 2: "Ninguno/preescolar", 3: "Primaria", 4: "Secundaria",
        5: "Media", 6: "Media", 7: "Media", 8: "Tecnica/tecnologica", 9: "Tecnica/tecnologica",
        10: "Universitaria o mas", 11: "Universitaria o mas", 12: "Universitaria o mas",
        13: "Universitaria o mas"}
EDUC_ORD = ["Ninguno/preescolar", "Primaria", "Secundaria", "Media", "Tecnica/tecnologica", "Universitaria o mas"]
DEPTO = {5: "Antioquia", 8: "Atlantico", 11: "Bogota", 13: "Bolivar", 15: "Boyaca", 17: "Caldas", 18: "Caqueta",
         19: "Cauca", 20: "Cesar", 23: "Cordoba", 25: "Cundinamarca", 27: "Choco", 41: "Huila", 44: "La Guajira",
         47: "Magdalena", 50: "Meta", 52: "Narino", 54: "Norte de Santander", 63: "Quindio", 66: "Risaralda",
         68: "Santander", 70: "Sucre", 73: "Tolima", 76: "Valle del Cauca", 81: "Arauca", 85: "Casanare",
         86: "Putumayo", 88: "San Andres", 91: "Amazonas", 94: "Guainia", 95: "Guaviare", 97: "Vaupes", 99: "Vichada"}

d = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")
d = d[d.anio >= 2022].drop(columns=["educ_fuente", "vivia_12m", "salud", "pension", "formal", "p6240", "p6426"])
d = d.reset_index(drop=True)
for c in d.columns:                      # ahorra memoria (maquina de 8 GB)
    if c != "fex_c18":
        d[c] = pd.to_numeric(d[c], errors="coerce").astype("float32")
d["fex_c18"] = pd.to_numeric(d["fex_c18"], errors="coerce").astype("float64")
d["nm"] = d.groupby("anio")["mes"].transform("nunique")
d["w"] = d.fex_c18 / d.nm          # peso de "promedio anual": poblacion promedio del periodo

d["grupo"] = np.select(
    [(d.pais_nac == 862) & (d.nacionalidad == 3),
     (d.pais_nac == 862),
     (d.nace_donde == 3),
     d.nace_donde.isin([1, 2])],
    ["ven_ext", "ven_col", "otro_ext", "col"], default="sin_dato")
d["smmlv"] = d.anio.map(SMMLV)
d["ocupado"] = d.oci == 1
d["pet15"] = d.pet == 1
d["educ_g"] = d.educ.map(EDUC)
d["afil_salud"] = (d.p6090 == 1).astype(float)
d.loc[d.p6090 == 9, "afil_salud"] = np.nan
d["ing"] = d.inglabo.where(d.ocupado & (d.inglabo > 0))
d["ing_smmlv"] = d.ing / d.smmlv
d["ing_real"] = d.ing / d.smmlv                 # en unidades de SMMLV: comparable entre anios
d["llegada"] = d.llegada_anio.where(d.llegada_anio.between(1950, 2026))
d["llegada_mes"] = d.llegada_mes.where(d.llegada_mes.between(1, 12))
d["anios_en_col"] = (d.anio - d.llegada).where(d.llegada.notna())
d["trab_formal_ss"] = ((d.p6920 == 1)).astype(float).where(d.ocupado)   # cotiza a pension
# OJO: en esta base EI = 1 marca empleo FORMAL (100% de los empleados del gobierno y quienes cotizan
# pension tienen EI=1; promedio 45% en colombianos = tasa de formalidad DANE). Informal = EI == 0.
d["informal"] = (d.ei == 0).astype(float).where(d.ocupado & d.ei.notna())
d["hogar_id"] = (d.anio.astype(str) + "_" + d.mes.astype(str) + "_" + d.directorio.astype(str) + "_"
                 + d.secuencia_p.astype(str) + "_" + d.hogar.astype(str))


def wmean(x, w):
    m = x.notna() & w.notna()
    return np.average(x[m], weights=w[m]) if m.any() and w[m].sum() > 0 else np.nan


def wquant(x, w, q=0.5):
    m = x.notna() & w.notna()
    if not m.any():
        return np.nan
    xs, ws = x[m].to_numpy(), w[m].to_numpy()
    o = np.argsort(xs)
    c = np.cumsum(ws[o]) / ws.sum()
    return xs[o][np.searchsorted(c, q)]


# ---------------------------------------------------------------------------------------------
# T1. Stock de personas por grupo y anio
# ---------------------------------------------------------------------------------------------
t1 = d.pivot_table(index="anio", columns="grupo", values="w", aggfunc="sum").fillna(0)
t1["total"] = t1.sum(axis=1)
t1["ven_nacidos"] = t1["ven_ext"] + t1["ven_col"]
t1["pct_ven_ext_pob"] = 100 * t1["ven_ext"] / t1["total"]
t1["pct_ven_nacidos_pob"] = 100 * t1["ven_nacidos"] / t1["total"]
n = d.groupby(["anio", "grupo"]).size().unstack(fill_value=0).add_prefix("n_muestra_")
t1 = t1.join(n)
t1.round(1).to_csv(TAB / "t1_stock_por_grupo_anio.csv")

# ---------------------------------------------------------------------------------------------
# T2. Llegada: distribucion por anio de llegada (migrantes venezolanos sin nacionalidad colombiana)
# ---------------------------------------------------------------------------------------------
v = d[d.grupo == "ven_ext"].copy()
v_recent = v[v.anio >= 2025]       # 2025 + ene-ago 2026 (muestra mas grande y reciente)
arr = v_recent.groupby("llegada").w.sum() / v_recent.w.sum() * 100
arr = arr[arr.index >= 2008]
arr.rename("pct_de_los_venezolanos_presentes").round(2).to_csv(TAB / "t2_anio_llegada_2025_2026.csv")


def cohorte(a):
    if pd.isna(a): return "sin dato"
    if a <= 2016: return "<=2016"
    if a <= 2018: return "2017-2018"
    if a <= 2020: return "2019-2020"
    if a <= 2022: return "2021-2022"
    return "2023+"


v["cohorte"] = v.llegada.map(cohorte)
COH = ["<=2016", "2017-2018", "2019-2020", "2021-2022", "2023+", "sin dato"]
coh = v.groupby(["anio", "cohorte"]).w.sum().unstack(fill_value=0)[COH]
(100 * coh.div(coh.sum(axis=1), axis=0)).round(1).to_csv(TAB / "t2b_cohorte_llegada_por_anio.csv")

# ---------------------------------------------------------------------------------------------
# T3. Perfil demografico (promedio 2022-2026, por grupo)
# ---------------------------------------------------------------------------------------------
rows = []
for g, gd in d[d.grupo.isin(["ven_ext", "ven_col", "col"])].groupby("grupo"):
    r = {"grupo": g, "personas_prom_miles": gd.w.sum() / gd.anio.nunique() / 1e3}
    r["edad_media"] = wmean(gd.edad, gd.w)
    r["edad_mediana"] = wquant(gd.edad, gd.w)
    r["pct_menor15"] = 100 * wmean((gd.edad < 15).astype(float), gd.w)
    r["pct_15_29"] = 100 * wmean(gd.edad.between(15, 29).astype(float), gd.w)
    r["pct_30_59"] = 100 * wmean(gd.edad.between(30, 59).astype(float), gd.w)
    r["pct_60mas"] = 100 * wmean((gd.edad >= 60).astype(float), gd.w)
    r["pct_mujeres"] = 100 * wmean((gd.sexo == 2).astype(float), gd.w)
    r["pct_urbano"] = 100 * wmean((gd.clase == 1).astype(float), gd.w)
    a = gd[gd.edad >= 25]
    for e in EDUC_ORD:
        r["educ25+_" + e] = 100 * wmean((a.educ_g == e).astype(float).where(a.educ_g.notna()), a.w)
    rows.append(r)
pd.DataFrame(rows).set_index("grupo").round(1).T.to_csv(TAB / "t3_perfil_demografico.csv")

# distribucion departamental
dep = v[v.anio >= 2025].groupby("dpto").w.sum()
dep = (100 * dep / dep.sum()).rename("pct_venezolanos")
allp = d[(d.anio >= 2025)].groupby("dpto").w.sum()
dep = pd.concat([dep, (100 * v[v.anio >= 2025].groupby("dpto").w.sum() / allp).rename("pct_de_la_poblacion_depto")], axis=1)
dep.index = [DEPTO.get(int(i), str(i)) for i in dep.index]
dep.sort_values("pct_venezolanos", ascending=False).round(2).to_csv(TAB / "t3b_departamentos_2025_2026.csv")

# intencion de quedarse (P3375: 1 si, 2 no, 3 no sabe?, 9 ns)  - solo migrantes que responden
iq = v[v.intencion_quedarse.notna()].groupby(["anio", "intencion_quedarse"]).w.sum().unstack(fill_value=0)
(100 * iq.div(iq.sum(axis=1), axis=0)).round(1).to_csv(TAB / "t3c_intencion_quedarse.csv")

# ---------------------------------------------------------------------------------------------
# T4. Mercado laboral, seguridad social e ingresos: por grupo y anio
# ---------------------------------------------------------------------------------------------
def indicadores(g):
    p = g[g.pet15]
    o = g[g.ocupado]
    r = {}
    r["n_muestra_pet"] = len(p)
    r["n_muestra_ocupados"] = len(o)
    r["personas_pet_miles"] = p.w.sum() / 1e3
    r["ocupados_miles"] = o.w.sum() / 1e3
    r["TO_pct"] = 100 * o.w.sum() / p.w.sum()
    ft = p[p.ft == 1]
    r["TGP_pct"] = 100 * ft.w.sum() / p.w.sum()
    r["TD_pct"] = 100 * ft[ft.dsi == 1].w.sum() / ft.w.sum() if ft.w.sum() > 0 else np.nan
    r["informalidad_pct"] = 100 * wmean(o.informal, o.w)
    r["cotiza_pension_pct"] = 100 * wmean(o.trab_formal_ss, o.w)
    r["cuenta_propia_pct"] = 100 * wmean((o.p6430 == 4).astype(float), o.w)
    r["asalariado_pct"] = 100 * wmean(o.p6430.isin([1, 2, 3, 7]).astype(float), o.w)
    r["horas_semana_media"] = wmean(o.p6800.where(o.p6800.between(1, 100)), o.w)
    oi = o[o.ing.notna()]
    r["ingreso_mediano_smmlv"] = wquant(oi.ing_smmlv, oi.w)
    r["ingreso_medio_smmlv"] = wmean(oi.ing_smmlv.clip(upper=oi.ing_smmlv.quantile(0.999)), oi.w)
    r["pct_gana_menos_1smmlv"] = 100 * wmean((oi.ing_smmlv < 1).astype(float), oi.w)
    r["pct_gana_menos_075smmlv"] = 100 * wmean((oi.ing_smmlv < 0.75).astype(float), oi.w)
    h = oi[oi.p6800.between(1, 100)]
    r["ingreso_hora_mediano_smmlv_x1000"] = 1000 * wquant(h.ing_smmlv / (h.p6800 * 4.345), h.w)
    # seguridad social en salud (todas las edades)
    r["afiliado_salud_pct"] = 100 * wmean(g.afil_salud, g.w)
    gs = g[g.afil_salud == 1]
    r["salud_contributivo_pct_afiliados"] = 100 * wmean((gs.p6100 == 1).astype(float), gs.w)
    r["salud_subsidiado_pct_afiliados"] = 100 * wmean((gs.p6100 == 3).astype(float), gs.w)
    r["masa_salarial_mensual_miles_millones_COP"] = (oi.w * oi.ing).sum() / 1e9
    return pd.Series(r)


gr = d[d.grupo.isin(["ven_ext", "ven_col", "col"])]
t4 = gr.groupby(["grupo", "anio"]).apply(indicadores, include_groups=False)
t4.round(2).to_csv(TAB / "t4_mercado_laboral_por_grupo_anio.csv")

# ranking de ocupaciones/ramas (2 digitos CIIU) de los venezolanos ocupados 2025-2026
RAMA = {1: "Agricultura", 2: "Silvicultura", 3: "Pesca", 5: "Carbon", 6: "Petroleo", 7: "Metales", 8: "Otras minas",
        10: "Alimentos", 11: "Bebidas", 13: "Textiles", 14: "Confeccion", 15: "Cuero/calzado", 16: "Madera",
        24: "Metalurgia", 25: "Prod. metal", 31: "Muebles", 41: "Construccion edificios", 42: "Obras civiles",
        43: "Constr. especializada", 45: "Comercio/rep. vehiculos", 46: "Comercio mayorista", 47: "Comercio minorista",
        49: "Transporte terrestre", 52: "Almacenamiento", 53: "Correo", 55: "Alojamiento", 56: "Comidas y bebidas",
        68: "Inmobiliarias", 78: "Empleo", 80: "Seguridad", 81: "Aseo y jardineria", 82: "Apoyo oficina",
        85: "Educacion", 86: "Salud", 88: "Asistencia social", 94: "Asociaciones", 95: "Reparacion", 96: "Otros serv. personales",
        97: "Hogares empleadores"}
ov = d[(d.anio >= 2025) & d.ocupado & d.grupo.isin(["ven_ext", "col"])]
ram = ov.groupby(["grupo", "rama2d_r4"]).w.sum().unstack(0).fillna(0)
ram = 100 * ram / ram.sum()
ram.index = [f"{int(i)} {RAMA.get(int(i), '')}".strip() for i in ram.index]
ram.sort_values("ven_ext", ascending=False).head(15).round(1).to_csv(TAB / "t4b_ramas_2025_2026.csv")

# ---------------------------------------------------------------------------------------------
# T5. Por cohorte de llegada (migrantes venezolanos, 2025-2026): condiciones segun tiempo en Colombia
# ---------------------------------------------------------------------------------------------
vv = v[v.anio >= 2025]
t5 = vv.groupby("cohorte").apply(indicadores, include_groups=False).reindex(COH)
t5.round(2).to_csv(TAB / "t5_indicadores_por_cohorte_llegada_2025_2026.csv")

# ---------------------------------------------------------------------------------------------
# T6. Hogares: ingreso laboral per capita (proxy de vulnerabilidad; NO es la pobreza monetaria oficial)
# ---------------------------------------------------------------------------------------------
h = d.groupby("hogar_id").agg(
    anio=("anio", "first"), n=("w", "size"), w=("w", "first"),
    ing=("ing", "sum"), smmlv=("smmlv", "first"),
    n_ven_ext=("grupo", lambda s: (s == "ven_ext").sum()),
    n_ocup=("ocupado", "sum"),
)
h["pc_smmlv"] = h.ing / h.n / h.smmlv
h["tipo"] = np.where(h.n_ven_ext > 0, "hogar con venezolano(s)", "hogar sin venezolanos")
h["w_pers"] = h.w * h.n
ht = []
for (a, t), g in h.groupby(["anio", "tipo"]):
    ht.append({"anio": a, "tipo": t, "hogares_miles": g.w.sum() / 1e3,
               "personas_por_hogar": wmean(g.n, g.w),
               "ocupados_por_hogar": wmean(g.n_ocup, g.w),
               "ing_lab_pc_mediano_smmlv": wquant(g.pc_smmlv, g.w_pers),
               "pct_personas_ing_pc_<0.5smmlv": 100 * wmean((g.pc_smmlv < 0.5).astype(float), g.w_pers),
               "pct_personas_ing_pc_<0.25smmlv": 100 * wmean((g.pc_smmlv < 0.25).astype(float), g.w_pers),
               "pct_hogares_sin_ocupados": 100 * wmean((g.n_ocup == 0).astype(float), g.w)})
pd.DataFrame(ht).round(2).to_csv(TAB / "t6_hogares_con_y_sin_venezolanos.csv", index=False)

# ---------------------------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------------------------
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
AZ, NA, GR = "#1f4e79", "#d9822b", "#7f7f7f"

fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.bar(t1.index.astype(str), t1["ven_ext"] / 1e6, color=AZ, label="Venezuela, sin nacionalidad colombiana")
ax.bar(t1.index.astype(str), t1["ven_col"] / 1e6, bottom=t1["ven_ext"] / 1e6, color=NA, label="Venezuela, con nacionalidad colombiana")
for i, (a, r) in enumerate(t1.iterrows()):
    ax.text(i, r["ven_nacidos"] / 1e6 + 0.03, f"{r['ven_nacidos']/1e6:.2f}", ha="center")
ax.set_ylabel("Millones de personas"); ax.set_title("Nacidos en Venezuela residentes en Colombia (GEIH)")
ax.legend(frameon=False, fontsize=8, loc="lower center"); ax.set_ylim(0, 2.8)
ax.text(0.99, -0.16, "2026: enero-agosto. Fuente: GEIH-DANE, calculos propios.", transform=ax.transAxes, ha="right", fontsize=7, color=GR)
fig.tight_layout(); fig.savefig(FIG / "fig1_stock_venezolanos.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 3.8))
a = arr[arr.index >= 2012]
ax.bar(a.index.astype(int).astype(str), a.values, color=AZ)
ax.set_ylabel("% de los venezolanos presentes"); ax.set_title("Anio de llegada a Colombia (venezolanos presentes en 2025-26)")
plt.setp(ax.get_xticklabels(), rotation=45)
fig.tight_layout(); fig.savefig(FIG / "fig2_anio_llegada.png", dpi=200); plt.close(fig)

# piramide de edad
fig, ax = plt.subplots(figsize=(6, 4.2))
bins = list(range(0, 85, 5)) + [120]
labs = [f"{b}-{b+4}" for b in bins[:-2]] + ["80+"]
for g, col, off in [("ven_ext", AZ, 0), ("col", GR, 0)]:
    gd = d[(d.grupo == g) & (d.anio >= 2025)]
    cut = pd.cut(gd.edad, bins=bins, right=False, labels=labs)
    s = gd.groupby(cut, observed=False).w.sum()
    s = 100 * s / s.sum()
    if g == "ven_ext":
        ax.barh(labs, s.values, color=col, alpha=0.85, label="Venezolanos (sin nac. colombiana)")
    else:
        ax.plot(s.values, labs, color=NA, marker="o", lw=1.5, label="Colombianos")
ax.set_xlabel("% de la poblacion del grupo"); ax.set_title("Estructura por edad, 2025-26")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(FIG / "fig3_estructura_edad.png", dpi=200); plt.close(fig)

# comparativo de indicadores clave (2025)
k = t4.xs(2025, level="anio")
fig, axs = plt.subplots(1, 4, figsize=(11, 3.6))
for ax, (col, ttl) in zip(axs, [("informalidad_pct", "Informalidad (% ocupados)"),
                                ("afiliado_salud_pct", "Afiliado a salud (%)"),
                                ("cotiza_pension_pct", "Cotiza a pension (% ocupados)"),
                                ("ingreso_mediano_smmlv", "Ingreso laboral mediano (SMMLV)")]):
    vals = [k.loc[g, col] for g in ["ven_ext", "ven_col", "col"]]
    ax.bar(["Ven.", "Ven. con\nnac. col.", "Colomb."], vals, color=[AZ, NA, GR])
    for i, x in enumerate(vals):
        ax.text(i, x, f"{x:.1f}" if col != "ingreso_mediano_smmlv" else f"{x:.2f}", ha="center", va="bottom", fontsize=8)
    ax.set_title(ttl, fontsize=9)
fig.suptitle("Condiciones de vida y trabajo, 2025", y=1.02)
fig.tight_layout(); fig.savefig(FIG / "fig4_indicadores_2025.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# gradiente por cohorte
c = t5.reindex(COH[:-1])
fig, axs = plt.subplots(1, 3, figsize=(10, 3.4))
for ax, (col, ttl) in zip(axs, [("afiliado_salud_pct", "Afiliado a salud (%)"),
                                ("informalidad_pct", "Informalidad (%)"),
                                ("ingreso_mediano_smmlv", "Ingreso mediano (SMMLV)")]):
    ax.bar(c.index, c[col], color=AZ)
    ax.set_title(ttl, fontsize=9); plt.setp(ax.get_xticklabels(), rotation=30, fontsize=8)
fig.suptitle("Venezolanos por cohorte de llegada (2025-26)", y=1.02)
fig.tight_layout(); fig.savefig(FIG / "fig5_cohorte_llegada.png", dpi=200, bbox_inches="tight"); plt.close(fig)
print("ok")
