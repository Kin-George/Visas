"""Visa-R / 05: aportes fiscales y costos de los venezolanos (GEIH 2025) y escenarios de cobertura del PPT.

Ingresos: aportes a pension y salud de los ocupados formales, IVA sobre su consumo.
Costos : UPC de salud de los afiliados (subsidiado y contributivo).
NO incluye (omitido): educacion, otros subsidios/transferencias, atencion de urgencias de no afiliados, impuestos distintos del IVA, aportes
patronales exonerados, efectos de segunda vuelta, efectos en el empleo de los colombianos.
Todo son supuestos explicitos -> ver bloque PARAMETROS.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "Outputs" / "tables"

# ------------------------------------------------------------------ PARAMETROS
SMMLV_2025 = 1_423_500
UPC_SUB_2026, UPC_CONTR_2026 = 1_541_706, 1_658_912            # Res. 2764/2025 (fuente: Consultorsalud / Portafolio)
UPC_SUB = UPC_SUB_2026 / 1.1649                                  # 2025: la UPC subsidiada subio 16,49% en 2026
UPC_CONTR = UPC_CONTR_2026 / 1.0903                              # 2025: el contributivo subio 9,03% en 2026
T_PENS, T_SAL_DEP, T_SAL_IND = 0.16, 0.04, 0.125                 # dependiente: 4%+12% pension, 4% salud (empleador exonerado <10 SMMLV)
IBC_IND = 0.40                                                    # independiente: IBC = 40% del ingreso, minimo 1 SMMLV
AHORRO, REMESAS = 0.10, 0.10                                      # supuestos (no vienen de datos)
IVA_EF = {"bajo": 0.03, "central": 0.05, "alto": 0.07}            # incidencia efectiva del IVA sobre el consumo: SUPUESTO
SUPUESTOS = {"SMMLV_2025": SMMLV_2025, "UPC_subsidiado_2025": round(UPC_SUB), "UPC_contributivo_2025": round(UPC_CONTR),
             "tasa_pension_total": T_PENS, "tasa_salud_dependiente": T_SAL_DEP, "tasa_salud_independiente": T_SAL_IND,
             "IBC_independiente": IBC_IND, "ahorro": AHORRO, "remesas": REMESAS, **{f"IVA_{k}": v for k, v in IVA_EF.items()}}

# ------------------------------------------------------------------ GEIH 2025: venezolanos
cols = ["anio", "mes", "fex_c18", "edad", "pais_nac", "nacionalidad", "oci", "inglabo", "p6430", "p6090", "p6100", "ei"]
d = pd.read_pickle(ROOT / "Datos" / "geih_migracion_2021_2026.pkl")[cols]
d = d[d.anio == 2025]
d = d.apply(pd.to_numeric, errors="coerce")
d = d[(d.pais_nac == 862) & (d.nacionalidad == 3)].copy()
d["w"] = d.fex_c18 / d.mes.nunique()
POB = d.w.sum()
o = d[(d.oci == 1) & (d.inglabo > 0)].copy()
o["dep"] = o.p6430.isin([1, 2, 3, 7, 8])
o["formal"] = o.ei == 1


def aportes(df):
    """Aportes anuales (COP) por trabajador segun reglas generales; df con inglabo, dep."""
    ibc_dep = df.inglabo.clip(SMMLV_2025, 25 * SMMLV_2025)
    ibc_ind = (IBC_IND * df.inglabo).clip(SMMLV_2025, 25 * SMMLV_2025)
    ibc = np.where(df.dep, ibc_dep, ibc_ind)
    sal = np.where(df.dep, T_SAL_DEP, T_SAL_IND) * ibc * 12
    pen = T_PENS * ibc * 12
    return pd.DataFrame({"salud": sal, "pension": pen}, index=df.index)


A = aportes(o)
o["aporte_salud"], o["aporte_pension"] = A.salud, A.pension
f = o[o.formal]; i = o[~o.formal]
rev = {
    "aportes_salud_formales_actuales": (f.w * f.aporte_salud).sum(),
    "aportes_pension_formales_actuales": (f.w * f.aporte_pension).sum(),
    "aportes_salud_si_informales_cotizaran(potencial)": (i.w * i.aporte_salud).sum(),
    "aportes_pension_si_informales_cotizaran(potencial)": (i.w * i.aporte_pension).sum(),
}
masa_anual = (o.w * o.inglabo).sum() * 12
consumo = masa_anual * (1 - AHORRO - REMESAS)
iva = {k: v * consumo for k, v in IVA_EF.items()}

# costos de salud: afiliados por regimen (todas las edades)
afil = d[d.p6090 == 1]
n_contr = afil.w[afil.p6100 == 1].sum()
n_sub = afil.w[afil.p6100 == 3].sum()
n_esp = afil.w[afil.p6100 == 2].sum()
costo_sub = n_sub * UPC_SUB
costo_contr = n_contr * UPC_CONTR

base = pd.Series({
    "poblacion_venezolana_miles": POB / 1e3,
    "ocupados_miles": o.w.sum() / 1e3,
    "ocupados_formales_miles": f.w.sum() / 1e3,
    "afiliados_contributivo_miles": n_contr / 1e3, "afiliados_subsidiado_miles": n_sub / 1e3,
    "masa_salarial_anual_billones": masa_anual / 1e12,
    "INGRESOS_aportes_salud_billones": rev["aportes_salud_formales_actuales"] / 1e12,
    "INGRESOS_aportes_pension_billones": rev["aportes_pension_formales_actuales"] / 1e12,
    "INGRESOS_IVA_billones_bajo": iva["bajo"] / 1e12, "INGRESOS_IVA_billones_central": iva["central"] / 1e12,
    "INGRESOS_IVA_billones_alto": iva["alto"] / 1e12,
    "COSTO_UPC_subsidiado_billones": costo_sub / 1e12,
    "COSTO_UPC_contributivo_billones": costo_contr / 1e12,
    "potencial_aportes_salud_informales_billones": rev["aportes_salud_si_informales_cotizaran(potencial)"] / 1e12,
    "potencial_aportes_pension_informales_billones": rev["aportes_pension_si_informales_cotizaran(potencial)"] / 1e12,
})
# balances
base["BALANCE_salud_(aportes - UPC total)_billones"] = base["INGRESOS_aportes_salud_billones"] - (costo_sub + costo_contr) / 1e12
base["BALANCE_estricto_(IVA central - UPC subsidiado)_billones"] = base["INGRESOS_IVA_billones_central"] - costo_sub / 1e12
base["BALANCE_amplio_(IVA + aportes salud - UPC total)_billones"] = (base["INGRESOS_IVA_billones_central"]
                                                                   + base["INGRESOS_aportes_salud_billones"] - (costo_sub + costo_contr) / 1e12)
base.round(3).to_csv(TAB / "t10_fiscal_base_2025.csv", header=["valor"])
pd.Series(SUPUESTOS).to_csv(TAB / "t10b_supuestos_fiscales.csv", header=["valor"])

# ------------------------------------------------------------------ escenarios PPT
res = pd.read_csv(TAB / "t8b_resumen_demanda_interna.csv", index_col=0)["valor"]
prima = res["prima_formalidad_ajustada_pct"] / 100
b_pens, se_pens = res["EPM_efecto_PPT_pension_ocupados_pp"] / 100, res["EPM_ee_pension_ocupados"] / 100
cov0 = res["EPM_cobertura_PPT_pct"] / 100
t7 = pd.read_csv(TAB / "t7_epm_ppt_vs_sin_ppt.csv")
b_sal = t7[(t7.especificacion.str.startswith("A")) & (t7.indicador == "Afiliado a salud (%)")].dif_ajustada.iloc[0] / 100
tasa_sal_f = rev["aportes_salud_formales_actuales"] / (f.w * f.inglabo * 12).sum()    # aporte salud / ingreso (formales)
tasa_pen_f = rev["aportes_pension_formales_actuales"] / (f.w * f.inglabo * 12).sum()
ing_inf = np.average(i.inglabo, weights=i.w)
n_ocup = o.w.sum()
sh_sub = n_sub / (n_sub + n_contr)
upc_med = sh_sub * UPC_SUB + (1 - sh_sub) * UPC_CONTR

sc = []
for cov in (0.80, 1.00):
    dcov = cov - cov0
    for lab, bp in [("central", b_pens), ("inferior", b_pens - 1.96 * se_pens), ("superior", b_pens + 1.96 * se_pens)]:
        nuevos = dcov * bp * n_ocup                       # trabajadores que se formalizan
        ing_nuevo = ing_inf * (1 + prima)
        d_aportes_sal = nuevos * ing_nuevo * 12 * tasa_sal_f
        d_aportes_pen = nuevos * ing_nuevo * 12 * tasa_pen_f
        d_masa = nuevos * ing_inf * prima * 12             # aumento de la masa salarial (solo los que se formalizan)
        d_iva = d_masa * (1 - AHORRO - REMESAS) * IVA_EF["central"]
        nuevos_afil = dcov * POB * b_sal                   # nuevos afiliados a salud
        d_costo = nuevos_afil * upc_med
        sc.append({"cobertura_PPT_pct": 100 * cov, "efecto_PPT_formalidad": lab,
                   "trabajadores_que_se_formalizan_miles": nuevos / 1e3,
                   "nuevos_afiliados_salud_miles": nuevos_afil / 1e3,
                   "d_aportes_salud_mil_millones": d_aportes_sal / 1e9, "d_aportes_pension_mil_millones": d_aportes_pen / 1e9,
                   "d_IVA_mil_millones": d_iva / 1e9, "d_costo_UPC_mil_millones": d_costo / 1e9,
                   "balance_amplio_mil_millones(aportes salud+IVA-UPC)": (d_aportes_sal + d_iva - d_costo) / 1e9,
                   "balance_con_pension_mil_millones": (d_aportes_sal + d_aportes_pen + d_iva - d_costo) / 1e9})
t11 = pd.DataFrame(sc)
t11.round(1).to_csv(TAB / "t11_escenarios_fiscales_PPT.csv", index=False)
pd.set_option("display.width", 250)
print(base.round(2).to_string())
print(t11.round(1).T.to_string())
print("tasa salud/ingreso formales", round(tasa_sal_f, 4), "pension", round(tasa_pen_f, 4), "UPC medio", round(upc_med), "share sub", round(sh_sub, 3))

# ------------------------------------------------------------------ escenario alternativo con efectos de la literatura (JEEA, Ibanez et al.)
# Efectos del PEP 2018 reportados (resumen del articulo, no verificados en texto completo): empleo formal +10 pp, ingreso laboral +22%,
# consumo per capita +48%. Se aplican a la poblacion que pasaria a estar regularizada (la que hoy no tiene PPT).
JEEA = {"formal_pp": 0.10, "ingreso": 0.22, "consumo": 0.48}
alt = []
for cov in (0.80, 1.00):
    sh = cov - cov0
    nuevos_f = sh * JEEA["formal_pp"] * n_ocup
    d_masa_alt = sh * masa_anual * JEEA["ingreso"]
    d_cons_alt = sh * consumo * JEEA["consumo"]
    d_iva_alt = d_cons_alt * IVA_EF["central"]
    ing_nuevo_alt = ing_inf * (1 + JEEA["ingreso"])
    d_sal = nuevos_f * ing_nuevo_alt * 12 * tasa_sal_f
    d_pen = nuevos_f * ing_nuevo_alt * 12 * tasa_pen_f
    d_cost = sh * POB * b_sal * upc_med
    alt.append({"cobertura_PPT_pct": 100 * cov, "trabajadores_que_se_formalizan_miles": nuevos_f / 1e3,
                "aumento_masa_salarial_billones": d_masa_alt / 1e12, "aumento_consumo_billones": d_cons_alt / 1e12,
                "d_IVA_mil_millones": d_iva_alt / 1e9, "d_aportes_salud_mil_millones": d_sal / 1e9,
                "d_aportes_pension_mil_millones": d_pen / 1e9, "d_costo_UPC_mil_millones": d_cost / 1e9,
                "balance_amplio_mil_millones": (d_iva_alt + d_sal - d_cost) / 1e9,
                "balance_con_pension_mil_millones": (d_iva_alt + d_sal + d_pen - d_cost) / 1e9})
t11b = pd.DataFrame(alt)
t11b.round(2).to_csv(TAB / "t11b_escenario_efectos_literatura.csv", index=False)
print(t11b.round(2).T.to_string())
