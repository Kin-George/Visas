# Visa-R · 05 · Aportes fiscales y costos de la población venezolana

Código: `Code/05_aportes_fiscales.py`. Tablas: `t10_fiscal_base_2025.csv`, `t10b_supuestos_fiscales.csv`, `t11_escenarios_fiscales_PPT.csv`.
Cifras en COP de 2025 (billones = 10^12). **Son estimaciones con supuestos explícitos; el resultado depende de ellos.**

## Supuestos (todos en `t10b`)
- Aportes: dependientes 16% pensión + 4% salud sobre el ingreso (IBC entre 1 y 25 SMMLV); independientes 16% + 12,5% sobre el 40% del ingreso (mínimo 1 SMMLV) ([UGPP/Actualícese](https://actualicese.com/calculadora-ibc/)). El aporte patronal de salud se supone exonerado para salarios < 10 SMMLV (no verificado en esta sesión) y no se cuenta aparte.
- Costos de salud: UPC 2026 subsidiado COP 1.541.706 y contributivo 1.658.912 ([Portafolio](https://www.portafolio.co/economia/gobierno/la-upc-para-el-2026-aumento-16-48-para-el-regimen-subsidiado-y-9-03-para-el-contributivo-485505)); para 2025 se deflactan por los aumentos de 2026 (16,49% y 9,03%): 1,32 y 1,52 millones por afiliado.
- IVA: incidencia efectiva sobre el consumo de 3% / 5% / 7% (**supuesto mío**, sin fuente); consumo = ingreso laboral × (1 − 10% ahorro − 10% remesas).
- Formales = ocupados con `EI` = 1; los demás no cotizan.

## 1. Balance base 2025 (1,76 M de venezolanos sin nacionalidad colombiana)
| Concepto | Billones COP/año |
|---|---|
| Ingresos: aportes a salud (179 mil formales) | 0,22 |
| Ingresos: aportes a pensión (ahorro pensional, no ingreso neto del Estado) | 0,63 |
| Ingresos: IVA (rango 0,33–0,77) | 0,55 |
| Costo: UPC subsidiado (856 mil afiliados) | 1,13 |
| Costo: UPC contributivo (290 mil afiliados) | 0,44 |
| **Balance estricto** (IVA − UPC subsidiado) | **−0,58** |
| **Balance amplio** (IVA + aportes salud − UPC total) | **−0,80** |

- Con las reglas generales, si los informales cotizaran, los aportes serían **+0,98 billones en salud y +1,98 en pensión**: la informalidad (79%) es la principal fuente de aportes no recaudados.
- El déficit en salud es típico de un hogar de ingresos bajos: los aportes de un trabajador de ~1,2 SMMLV financian una parte de una UPC de 1,3–1,5 millones por afiliado. No es exclusivo de migrantes; no lo calculé para colombianos de ingresos comparables.

## 2. Escenarios de cobertura del PPT (efecto estático, anual)
Efectos tomados de la EPM (+66 pp de afiliación a salud; +14,8 pp de pensión entre ocupados) y la prima de formalidad de la GEIH (29%) (notas 03 y 04):

| Cobertura PPT | Trabajadores que se formalizan | Nuevos afiliados a salud | Aportes salud + IVA | Costo UPC | Balance amplio |
|---|---|---|---|---|---|
| 80% | 18 mil (14–23) | 168 mil | +0,02 | −0,23 | **−0,21 billones** |
| 100% | 44 mil (33–55) | 402 mil | +0,05 | −0,55 | **−0,50 billones** (−0,49 a −0,51) |

Contando los aportes a pensión (+0,13 billones en el escenario de 100%) el balance mejora a −0,37.

## 3. Lectura
- **En el corto plazo, regularizar tiene un costo fiscal neto**, dominado por la afiliación a salud subsidiada (≈ COP 1,4 millones por nuevo afiliado al año). Los aportes y el IVA adicionales cubren menos de una décima parte de ese costo; para cubrirlo con aportes de salud harían falta aproximadamente diez veces más formalizaciones que las que se asocian con el PPT (≈ 5 pp).
- Esto **no incluye beneficios que no se monetizan o no se miden**: el acceso a salud pasa de 44% a 85% entre quienes lo necesitaron (EPM), se evita parte de la atención de urgencias que hoy se financia igual con recursos públicos, y los efectos de largo plazo (formalización, capital humano, niños en el sistema educativo) quedan fuera.
- **No incluye costos de educación** ni otros subsidios, y supone que el costo por nuevo afiliado equivale a la UPC; los no afiliados actuales ya consumen urgencias, cuyo costo no se resta.
- Para la tesis: el caso fiscal del PPT **no se sostiene como "se paga solo" en el corto plazo con estos datos**. La contribución económica de los migrantes está en su ingreso y consumo (nota 04) y en el potencial de formalización (≈ COP 3 billones de aportes si cotizaran), no en un ahorro fiscal inmediato.

## 4. Cautelas
- Resultados muy sensibles a los supuestos (IVA efectivo, UPC como costo medio, proporción subsidiado/contributivo, sin netear urgencias).
- La división contributivo/subsidiado es de la GEIH (75% subsidiado); la EPM da 80% contributivo entre afiliados con PPT, una discrepancia que no pude resolver (puede ser autorreporte o la cobertura de 23 ciudades).
- Se aplica el efecto de la EPM (15+, 23 ciudades) a toda la población venezolana de la GEIH.
- Falta contrastar con estudios existentes (p. ej. estimaciones del costo fiscal del PPT) antes de presentar cifras como definitivas.
