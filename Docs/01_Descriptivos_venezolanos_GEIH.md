# Visa-R · 01 · Descriptivos de la población venezolana en Colombia (GEIH 2022–2026)

Objetivo: tener los números básicos para plantear el problema (cuántos son, quiénes son, cómo viven y trabajan) antes de
estudiar si la regularización (PPT) se asocia con mejores condiciones.

Reproducir: `python Visa-R/Code/01_extraer_geih.py` y luego `python Visa-R/Code/02_descriptivos.py` (desde la raíz del repo).
Los `.dta` de la GEIH están en `~/Documents/Databases/GEIH`. Tablas en `Outputs/tables/`, figuras en `Outputs/Figures/`.

## Definiciones
| Grupo | Criterio GEIH |
|---|---|
| **Venezolano migrante** (`ven_ext`) | Nacido en Venezuela (`P3373S3` = 862) y **sin** nacionalidad colombiana (`P3374` = 3) |
| Nacido en Venezuela con nacionalidad colombiana (`ven_col`) | Retornados, hijos de colombianos, binacionales (`P3374` = 1 ó 2) |
| Colombianos (`col`) | Nacidos en Colombia |

- Pesos: `FEX_C18` dividido por el número de meses del año (población promedio). 2026 = enero–agosto.
- **2021 se excluye**: el módulo de migración se aplicó parcialmente (5,6 mil registros de venezolanos vs. 35–44 mil en 2022–2025).
- Antes de 2021 la GEIH no trae país de nacimiento ni llegada: no se puede construir la serie histórica con esta fuente.

## Hallazgos principales

**1. Cuántos son** (`t1`, `fig1`)
- Venezolanos sin nacionalidad colombiana: **2,04 M (2022) → 1,76 M (2025)**, 3,3–4,0% de la población. Nacidos en Venezuela (incluye los
  que tienen nacionalidad colombiana): 2,4 M (2022) → 2,1 M (2025–26).
- La baja 2022→2025 puede ser real (salida, naturalizaciones) o efecto de calibración de los factores de expansión; no se puede distinguir con la GEIH.

**2. Cuándo llegaron** (`t2`, `fig2`)
- Entre los presentes en 2025–26: ≈11% llegó hasta 2016, 30% en 2017–18, 28% en 2019–20, 15% en 2021–22 y 17% desde 2023.
  Cerca de 68% llegó en 2020 o antes (≥5 años en Colombia).
- Aproximadamente 82% dice tener la intención de quedarse (`t3c`; 2025–26).

**3. Quiénes son** (`t3`, `t3b`, `fig3`)
- Población joven: edad mediana 25 años (colombianos: 33); 2,6% tiene 60 años o más (colombianos: 16%). 52% son mujeres; 87% vive en zona urbana.
- Educación (25+ años): 43,6% con media completa, 14,6% con universitaria o más (colombianos: 18,3%); 21% solo secundaria.
- Concentración: Bogotá 18%, Antioquia 17%, Valle 10%, Cundinamarca 8%, Norte de Santander 7,5%. Como proporción de la población local
  destacan Arauca (14%), Norte de Santander (7,7%) y La Guajira (7,1%).

**4. Cómo trabajan** (`t4`, `t4b`, `fig4`; 2025)
- Participación laboral más alta que la de los colombianos (TGP 74% vs 64%) y desempleo similar (8,9% vs 8,9%).
- **Informalidad ≈ 80%** (colombianos 55%); cotizan a pensión 16,6% (colombianos 44%).
- Ingreso laboral mediano **0,91 SMMLV** (colombianos 1,00); por hora 4,31 vs 5,00 (milésimas de SMMLV); trabajan ≈ 47 h/semana vs 43 h.
  58,5% gana menos de un SMMLV (colombianos 46%).
- Ramas: 21% en restaurantes y comidas (colombianos 6%), 12,5% comercio minorista, 7,5% construcción.
- **Masa salarial**: ≈ COP 1,15 billones al mes en 2025 (≈ 2,6% de la masa salarial nacional). Es el dato más directo del
  aporte a la demanda interna; es ingreso laboral, no consumo.

**5. Hogares** (`t6`, proxy; no es la pobreza monetaria oficial)
- Hogares con venezolanos: 3,5 personas y 1,6 ocupados por hogar (sin venezolanos: 2,8 y 1,3). Solo 4,5% sin ningún ocupado (otros hogares: 17%).
- Ingreso laboral per cápita mediano ≈ 0,33 SMMLV (otros hogares 0,35); 71% de las personas vive en hogares con ingreso laboral per cápita < 0,5 SMMLV (otros: 63%).

**6. Seguridad social: lo más cercano a "regularizados" que trae la GEIH** (`t4`, `t5`, `fig5`)
- Afiliación a salud de venezolanos: **31% (2022) → 51% → 60% → 65% (2025)**; colombianos 97%. Entre los afiliados, ≈ 75% está en régimen subsidiado.
- Para extranjeros la afiliación a salud en Colombia requiere un documento válido (PEP/PPT), de modo que la afiliación es un proxy razonable (imperfecto) de regularización.
  El salto 2022→2025 coincide con la implementación del Estatuto Temporal de Protección (PPT) — **correlación, no causalidad**.
- Por cohorte de llegada (2025–26): afiliación 78% (≤2016), 80% (2017–18), 76% (2019–20), 59% (2021–22) y **26% (2023+)**;
  informalidad 77% → 92% para los llegados desde 2023. Quienes llegaron después del cierre del registro tienen mucha menor cobertura.
- Ingreso mediano por cohorte casi plano (0,86–0,91 SMMLV): la afiliación varía mucho más que el ingreso.

## Cautelas
- La GEIH es encuesta de hogares: subcubre migrantes recientes e irregulares (miedo a declarar) y su factor de expansión usa proyecciones del censo 2018.
  Las cifras administrativas de Migración Colombia / R4V (del orden de 2,8 M de venezolanos; **no verificado aquí**) son mayores que las de la GEIH.
- `EI` en la base es empleo **formal** (=1), no informal; aquí informal = `EI` = 0. (La primera corrida del script usaba la definición opuesta y daba 20% de informalidad: corregido.)
- Ingresos en múltiplos del SMMLV de cada año (2022: 1 000 000; 2023: 1 160 000; 2024: 1 300 000; 2025: 1 423 500; 2026: 1 750 905) para compararlos entre años.
- La GEIH no tiene variable de PPT/PEP ni de nacionalidad de origen más detallada; todo lo que sigue sobre regularización es proxy.

## Siguientes pasos sugeridos
1. Descargar y revisar la EPM del DANE (¿hay PPT, ingresos, gasto, salud?) y los registros de Migración Colombia / Mintrabajo del PPT para calibrar cobertura por cohorte.
2. Estimar diferencias ajustadas (edad, sexo, educación, ciudad, año) entre venezolanos y colombianos y entre venezolanos con y sin afiliación a salud.
3. Dimensionar el aporte a la demanda interna (masa salarial × propensión a consumir) y escenarios de cobertura del PPT.
