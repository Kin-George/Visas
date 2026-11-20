# Visa-R · 06 · Contraste de mis estimaciones con estudios existentes

Nivel de verificación de cada fuente: **[T]** leí el texto del documento; **[R]** solo vi el resumen/abstract o un resumen de prensa o de buscador (no verificado en el texto completo); **[X]** no pude abrirlo (403 o bloqueo anti-bots; no lo eludí).

## Fuentes
| Fuente | Qué aporta | Nivel |
|---|---|---|
| OIM / Equilibrium BDC (Licheri et al.), [Análisis de la contribución fiscal y económica de la migración venezolana, oct. 2025](https://lac.iom.int/sites/g/files/tmzbdl2601/files/documents/2025-12/analisis-de-la-contribucion-fiscal-y-economica-de-la-migracion-venezolana_2.pdf) | Colombia: aporte fiscal real y potencial; consumo de la población venezolana | [T] |
| Infobae, [nota sobre el estudio U. del Rosario–OIM, mar. 2025](https://www.infobae.com/colombia/2025/03/10/migrantes-venezolanos-contribuyen-con-15-billones-al-recaudo-fiscal-en-colombia/) | COP 1,5 billones al recaudo hasta 2024 (1,91%) | [R] |
| Ibáñez, Moya, Ortega, Rozo y Urbina, *Life Out of the Shadows* (JEEA 2024/25; [IZA DP 15049](https://docs.iza.org/dp15049.pdf)) | Efectos de la regularización (PEP) en empleo formal, ingreso, consumo y salud | [R] (abstract y resúmenes); página de la revista [X] |
| Valencia et al., [BID WP-1170, *Do Immigrants Bring Fiscal Dividends?*](https://publications.iadb.org/en/do-immigrants-bring-fiscal-dividends-case-venezuelan-immigration-colombia) (2020) | Modelo de equilibrio general: costo fiscal de corto plazo y dividendo de largo plazo | [R] (abstract) |
| Banco Mundial y FMI ([FMI 2022](https://www.elibrary.imf.org/view/journals/087/2022/019/article-A001-en.xml)) | Costo fiscal agregado de la migración (0,4–0,5% del PIB), no del PPT en particular | [R] por buscador; el documento del FMI [X] |
| IPA/ACNUR, [evaluación del PEPFF](https://poverty-action.org/regularizing-venezuelan-refugees-and-migrants-through-employment-measuring-impacts-pepff-program) | Regularización por empleo: ingresos y empleo a mediano plazo | [T] de la página (sin errores estándar) |

## Comparación con mis cifras
| Tema | Estudios | Mis estimaciones (GEIH 2025, EPM 2025) | ¿Coherente? |
|---|---|---|---|
| Consumo de la población venezolana | ≈ COP 12,8 billones al año (OIM/Equilibrium [T], año 2022–23) | COP 8,3–13,8 billones según ahorro y remesas | Sí, mismo orden |
| Aporte fiscal actual | COP 1,5 billones (USD 529 M; 1,91% del recaudo de personas naturales, 0,15% del PIB), sobre todo IVA ([T], [R]) | IVA 0,33–0,77 (central 0,55) + aportes a salud 0,22 + pensión 0,63 = **0,8–1,4** billones | Sí: con pensión (1,4) queda cerca; sin pensión queda por debajo |
| Aporte fiscal potencial | +USD 804 M en total (2,9% del recaudo, 0,23% del PIB) con inserción eficiente / regularización plena [T] | Aportes que se recaudarían si los informales cotizaran: ≈ 3,0 billones (salud 0,98 + pensión 1,98); solo parte es ingreso del Estado | Orden comparable, definiciones distintas |
| Efecto de regularizar en formalidad | +10 pp de empleo formal con el PEP [R] | +14,8 pp de pensión y +16 pp de contrato escrito entre ocupados con PPT (EPM) | Sí, mismo orden (el mío puede incluir selección) |
| Efecto en ingreso laboral | +22% (versión publicada; +31% en el borrador) [R] | No medible en la EPM; prima de formalidad GEIH 29% por hora | Mi estimación de ingreso es indirecta |
| Efecto en consumo | +48% per cápita (publicado; +60% en el borrador) [R] | Supuse consumo proporcional al ingreso | **No**: mi escenario inicial subestima el consumo |
| Efecto en salud/acceso | Mejora de 1,2 desv. estándar en un índice de salud [R] | Afiliación +66 pp; sin acceso cuando lo necesitó: 56% → 15% | Mismo sentido |
| Costo fiscal | Banco Mundial/FMI: 0,4–0,5% del PIB en 2019–20 por toda la migración (salud, educación, ayuda) [R]. Corto plazo negativo, mediano plazo positivo (FMI, BID) [R] | UPC de toda la población venezolana ≈ 1,6 billones (≈ 0,1% del PIB, con un PIB aproximado que no verifiqué); costo adicional de llevar el PPT a 100% ≈ 0,55 billones | Mi costo es solo de salud, por eso queda muy por debajo del agregado; el signo coincide con "costo de corto plazo" |
| Balance por hogar regularizado | Hogares sin PEP: costo neto de USD 1.056 al año; con PEP: USD 610 ([R], resumen de JDC) | Costo neto *mayor* con más afiliación | **No coincide** (ver abajo) |

## Escenario alternativo con efectos de la literatura (`t11b`)
Uso los efectos del JEEA aplicados a la población que pasaría a estar regularizada (formalidad +10 pp, ingreso +22%, consumo +48%) con cobertura de 100%:

| | Billones COP/año |
|---|---|
| Aumento de la masa salarial | +1,04 |
| Aumento del consumo | +1,82 |
| IVA adicional (5% de incidencia efectiva, supuesto) | +0,09 |
| Aportes a salud adicionales | +0,03 |
| Costo adicional de UPC | −0,55 |
| **Balance amplio** | **−0,43** (con pensión −0,35) |

Con efectos de ingreso y consumo mucho mayores que los míos, el balance sigue siendo negativo en el corto plazo: la conclusión de la nota 05 **no depende** de esa diferencia.

## Por qué mi balance podría estar sesgado hacia el costo
1. **Costo por afiliado:** supongo que cada nuevo afiliado cuesta una UPC completa. La UPC es una prima ajustada por riesgo; una población joven (solo 2,6% tiene 60 años o más) puede costar menos que el promedio.
2. **Contrafactual sin PPT:** no resto el costo actual de urgencias y de atención a no afiliados, que ya se financia con recursos públicos. El menor costo neto por hogar con PEP del JEEA parece incluir este tipo de efecto.
3. **Impuestos:** solo cuento IVA y aportes. Otros impuestos elevan los ingresos.
4. **Horizonte:** el BID y el FMI encuentran que el balance mejora en el mediano plazo por mayor producto y empleo; mi cálculo es estático.
5. **Selección:** el efecto de la EPM sobre la afiliación puede sobrestimar el efecto causal del PPT.

## Conclusión para la tesis
- **Respaldado por estudios:** los migrantes venezolanos aportan una contribución económica positiva y sustancial (consumo ≈ COP 12–14 billones; aporte fiscal ≈ COP 1,5 billones, 1,9% del recaudo de personas naturales, sobre todo IVA). El potencial adicional ronda +USD 275 M (de 529 a 804 M).
- **Respaldado por estudios:** regularizar mejora formalidad (+10 pp), ingreso (+22%), consumo (+48%) y salud (JEEA, [R]). Es la mejor evidencia causal para tu hipótesis. La mía (EPM, GEIH) es correlacional y apunta en el mismo sentido en formalidad, salud y contrato, pero no encuentra mejor empleo ni seguridad alimentaria.
- **A matizar:** no hay evidencia de que el PPT "se pague solo" en el corto plazo. Los estudios lo ven como un costo de corto plazo con dividendo de mediano plazo; la excepción es el menor costo neto por hogar con PEP del JEEA, que debes revisar en el texto completo antes de citarlo.
- **Pendiente antes de presentar:** leer en texto completo el JEEA (cifras y cálculo fiscal por hogar), el BID WP-1170, el estudio del FMI y la nota del Banco Mundial; contrastar el costo por afiliado con datos de ADRES.
