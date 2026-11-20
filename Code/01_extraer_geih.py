"""Visa-R / 01: extrae de la GEIH 2021-2026 las variables necesarias para describir
a la poblacion venezolana en Colombia y la guarda en Visa-R/Datos/geih_migracion_2021_2026.pkl.

Los .dta de la GEIH viven en ~/Documents/Databases/GEIH (no estan en el repo).
Los nombres de variable cambian entre anios (p. ej. 2022 usa EDAD/SEXO, 2025 usa P6040/P3271),
asi que se estandarizan aqui.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GEIH = Path.home() / "Documents" / "Databases" / "GEIH"
OUT = ROOT / "Datos" / "geih_migracion_2021_2026.pkl"

CANDIDATAS = [
    "DIRECTORIO", "SECUENCIA_P", "ORDEN", "HOGAR", "MES", "FEX_C18", "CLASE", "AREA", "DPTO",
    "P6040", "EDAD", "P3271", "SEXO", "P6050", "P3042", "NIVEL_MAS_ALTO",
    "P3373", "LUGAR_NACIMIENTO", "P3373S3", "LUGAR_NACIMIENTO_EX", "P3373S3A1", "P3373S3A2",
    "P3374", "P3374S1", "P3375", "P3384", "P3385", "P3386",
    "OCI", "DSI", "FT", "PET", "INGLABO", "P6430", "P6800", "P6920", "P6090", "P6100", "P6240",
    "SALUD", "PENSION", "FORMAL", "EI", "RAMA2D_R4", "P6426",
]


def num(s):
    return pd.to_numeric(s, errors="coerce")


def cargar(anio):
    ruta = GEIH / f"GEIH_{anio}_total.dta"
    disp = set(pd.io.stata.StataReader(ruta).variable_labels())
    cols = [c for c in CANDIDATAS if c in disp]
    partes = [c for c in pd.read_stata(ruta, chunksize=250_000, columns=cols,
                                       convert_categoricals=False)]
    d = pd.concat(partes, ignore_index=True)
    out = pd.DataFrame(index=d.index)
    out["anio"] = anio
    for c in ["DIRECTORIO", "SECUENCIA_P", "ORDEN", "HOGAR", "MES", "FEX_C18", "CLASE", "AREA", "DPTO"]:
        out[c.lower()] = num(d[c]) if c in d else pd.NA
    out["edad"] = num(d["P6040"] if "P6040" in d else d["EDAD"])
    out["sexo"] = num(d["P3271"] if "P3271" in d else d["SEXO"])
    out["parentesco"] = num(d["P6050"]) if "P6050" in d else pd.NA
    # educacion: P3042 (2021, 2023+) o NIVEL_MAS_ALTO (2022); los codigos pueden diferir
    if "P3042" in d:
        out["educ"] = num(d["P3042"]); out["educ_fuente"] = "P3042"
    else:
        out["educ"] = num(d["NIVEL_MAS_ALTO"]); out["educ_fuente"] = "NIVEL_MAS_ALTO"
    out["nace_donde"] = num(d["P3373"] if "P3373" in d else d["LUGAR_NACIMIENTO"])
    pais = d["P3373S3"] if "P3373S3" in d else d["LUGAR_NACIMIENTO_EX"]
    out["pais_nac"] = num(pais.astype(str).str.strip())
    out["llegada_anio"] = num(d["P3373S3A1"]) if "P3373S3A1" in d else pd.NA
    out["llegada_mes"] = num(d["P3373S3A2"]) if "P3373S3A2" in d else pd.NA
    out["nacionalidad"] = num(d["P3374"]) if "P3374" in d else pd.NA
    out["nacionalidad_pais"] = num(d["P3374S1"].astype(str).str.strip()) if "P3374S1" in d else pd.NA
    out["intencion_quedarse"] = num(d["P3375"]) if "P3375" in d else pd.NA
    out["vivia_12m"] = num(d["P3384"]) if "P3384" in d else pd.NA
    for c in ["OCI", "DSI", "FT", "PET", "INGLABO", "P6430", "P6800", "P6920", "P6090", "P6100",
              "P6240", "SALUD", "PENSION", "FORMAL", "EI", "RAMA2D_R4", "P6426"]:
        out[c.lower()] = num(d[c]) if c in d else pd.NA
    return out


if __name__ == "__main__":
    partes = []
    for a in range(2021, 2027):
        print("cargando", a, flush=True)
        df = cargar(a)
        print("  filas", len(df), "meses", sorted(df["mes"].dropna().unique().tolist()), flush=True)
        partes.append(df)
    todo = pd.concat(partes, ignore_index=True)
    OUT.parent.mkdir(exist_ok=True)
    todo.to_pickle(OUT)
    print("guardado", OUT, todo.shape)
