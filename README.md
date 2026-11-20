# Visa R para titulares del PPT

Migrantes venezolanos en Colombia, Permiso por Protección Temporal (PPT) y Visa R (art. 91, Resolución 5477 de 2022): descriptivos, efectos de la regularización, aportes fiscales y análisis de la tarifa (USD 464). La propuesta es fijar la tarifa en cero para los beneficiarios del artículo 91.

## Documentos

- `Docs/20261113 Proyecto Visas R Cancillería Colombia - versión limpia.docx`: documento principal (generado por `Code/14` a `Code/18` y `Code/16`).
- `Docs/Nota_Ejecutiva_Visa-R.docx`: nota técnica corta (generada por `Code/11_graficos_nota.py` y `Code/12_nota_tecnica.py`; `Code/08` y `Code/09` quedan como historial).
- `Docs/00_Resumen_Visa-R.md` a `Docs/10_Ingreso_por_educacion.md`: notas de trabajo de cada análisis.
- `Docs/diccionario_EPM8_ddi.csv`: diccionario de variables de la EPM VIII-2025.

## Código

Los scripts de `Code/` se ejecutan desde la raíz de esta carpeta, en orden numérico:

| Script | Qué hace |
|---|---|
| 01 | Extrae de la GEIH (DANE) 2021-2026 las variables de migración, empleo e ingreso |
| 02 | Descriptivos de la población venezolana |
| 03 | EPM: comparación con y sin PPT (diferencias ajustadas) |
| 04-05 | Escenarios de demanda interna y aportes fiscales |
| 06 | Tarifa de la Visa R: elegibilidad, asequibilidad y escenarios |
| 07 | Intención de quedarse y emprendimiento |
| 10 | Curva precio-recaudo-derrame (modelo de demanda ilustrativo) |
| 11-12 | Gráficos y nota técnica |
| 13 | Ingreso mediano por nivel educativo |
| 14 | Hogares con menores y tarifa frente al ingreso individual |
| 15 | Gráficos de la versión limpia (escala oficial de PPT) |
| 16 | Documento de la versión limpia |
| 17-18 | Peso de la tarifa sobre el ingreso (persona y hogar) y sus gráficos |

Los resultados quedan en `Outputs/tables` (CSV) y `Outputs/Figures` (PNG).

## Datos

- **EPM VIII-2025 (DANE)** se incluye en `Datos/Raw/EPM_VIII_2025`.
- **GEIH (DANE)**: los microdatos no se incluyen por tamaño. Se descargan del catálogo de microdatos del DANE (https://microdatos.dane.gov.co) y `Code/01_extraer_geih.py` genera `Datos/geih_migracion_2021_2026.pkl`; `Code/07` genera `Datos/geih_2025_negocios.pkl`.
- Las cifras oficiales de PPT, venezolanos y visas R (Migración Colombia y Cancillería) se citan en el documento y deben verificarse en la fuente primaria.

Las cifras son asociaciones y escenarios con supuestos explícitos, no efectos causales.
