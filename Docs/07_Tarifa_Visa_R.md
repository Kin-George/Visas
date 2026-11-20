> **Actualización (13-nov-2026):** la nota ejecutiva adopta la posición de **tarifa cero** (ver `Docs/Nota_Ejecutiva_Visa-R.docx` y `Docs/09_Curva_precio_recaudo.md`). La conclusión de esta nota (reducción selectiva a USD 232) corresponde a la posición anterior; los hechos y las cifras de asequibilidad siguen vigentes.

# Visa-R · 07 · ¿Conviene eliminar el costo de la Visa R en un contexto de crisis fiscal?

Código: `Code/06_visa_r_tarifa.py`. Tablas: `t12_visaR_resumen`, `t12b_elegibilidad_por_anio`, `t12c_asequibilidad_hogares`, `t13_escenarios_tarifa`, `t13b_punto_equilibrio_tarifa` (en `Outputs/tables/`).

## Hechos y su verificación
- **Tarifa oficial (verificada):** en la página "Costos trámites" de la Cancillería, la categoría **"Residente – Tiempo acumulado Estatuto Temporal"** cuesta **estudio USD 56 + visa USD 408 = USD 464** (EUR 44 + 314 en Europa y Cuba). Captura aportada por el usuario el 12-nov-2026. La tarifa **depende de la actividad/ocupación**: p. ej. "Migrante – Profesional independiente" cuesta USD 56 + 279. La cifra de USD 239 (56 + 183) que había leído en un resumen de la Res. 3969 de 2026 corresponde a otra categoría, no a esta; los USD 455 de las guías de terceros son una aproximación (55 + 400) cercana a la oficial.
- No vi el texto "Tenga en cuenta que…" de la página (quedó cortado en la captura): ahí pueden estar el impuesto de timbre, el pago en pesos y las reglas para beneficiarios (hijos). **La tarifa de los beneficiarios (menores) no está verificada.**
- **Requisitos (Res. 5477 de 2022, art. 91):** haber sido titular del PEP o del PPT durante 5 años (o 5 años acumulados entre ambos) y tener un PPT vigente al solicitar ([Cancillería, normograma](https://www.cancilleria.gov.co/normograma/compilacion/docs/resolucion_minrelaciones_5477_2022.htm); [Sentencia T-187 de 2025](https://www.corteconstitucional.gov.co/relatoria/2025/t-187-25.htm)). Una copia en SUIN muestra el encabezado del art. 91 vigente solo hasta 27-dic-2023: el texto actual pudo cambiar y no lo comparé.
- **La Visa R dura 5 años y se renueva por traspaso**; no es residencia indefinida.
- **Quién fija la tarifa y a dónde va:** el Ministerio de Relaciones Exteriores, por resolución ([Decreto 1067 de 2015](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=74000); Res. 3969 de 2026, que modifica la 10452 de 2023). Los ingresos van al **Fondo Rotatorio del Ministerio**, no al presupuesto general ([Ley 1212 de 2008](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=31426)).
- El PPT vence el **28-may-2031** y se cancela al aprobar la visa (guías de terceros; no verificado en la norma).
- TRM ≈ COP 3.235/USD (6-nov-2026, [prensa](https://www.diariodelsur.com.co/noticias/precio-del-dolar-en-colombia-hoy-viernes-6-de-noviembre-de-2026)): USD 464 ≈ **COP 1,50 millones por persona** (0,86 SMMLV 2026).
- Crisis fiscal: el Marco Fiscal 2026 proyecta un déficit de 5,3% del PIB y el gobierno reconoce que no cumplirá la regla fiscal ([Valora Analitik](https://www.valoraanalitik.com/colombia-tendra-un-deficit-fiscal-mas-alto-2026-reconocio-gobierno-petro/)); el CARF advierte un déficit cercano a 10% en 2027 ([Portafolio](https://www.portafolio.co/economia/gobierno/tras-sincerada-de-cuentas-el-carf-advierte-que-deficit-fiscal-bordeara-el-10-del-pib-y-deja-un-margen-reducido-502274)).

## 1. Cuánto dinero está en juego (cuantitativo)
- Titulares de PPT (escala GEIH: 1,76 M de venezolanos × 65,6% con PPT): **≈ 1,15 millones de personas** (30% menores de 18). Las cifras administrativas pueden ser mayores (no verificadas).
- Ingreso máximo por la tarifa, una sola vez: **USD 535 M ≈ COP 1,7 billones ≈ 0,15% del PIB** (PIB implícito del estudio de la OIM). Con 70% de conversión: COP 1,2 billones.
- Como se cobraría entre 2026 y 2031, ≈ 0,03% del PIB por año frente a un déficit de 5,3%: **no resuelve ni agrava la crisis fiscal**. Además, el recaudo va al Fondo Rotatorio de la Cancillería: eliminar la tarifa afecta el financiamiento de esa entidad, no directamente el déficit del Gobierno Nacional Central.
- **Ola de solicitudes:** con 5 años de PPT/PEP, solo 29% de los titulares es elegible en 2026, **81% en 2027 y 96% en 2028** (año de obtención del PPT en la EPM; subestima la elegibilidad al ignorar el PEP): ≈ 0,8 millones de nuevos elegibles en 2027–28 (603 mil + 175 mil; el acumulado llega a 1,1 millones en 2028).

## 2. ¿Puede pagarla la gente? (cuantitativo)
Hogares con venezolanos (GEIH 2026, 2,3 venezolanos por hogar), si todos sus miembros venezolanos pagan:
| Tarifa por persona | Tarifa del hogar ≥ 1 mes de ingreso laboral | ≥ 2 meses | ≥ 3 SMMLV |
|---|---|---|---|
| USD 464 (vigente) | **65%** | 37% | 19% |
| Mitad (USD 232) | 37% | 15% | 1% |
| Solo estudio (USD 56) | 8% | 6% | 0% |

La tarifa mediana del hogar es COP 3,0 millones (1,7 SMMLV), con una mediana de ingreso laboral de 0,9 SMMLV por ocupado y 79% de informalidad. Es una barrera alta para buena parte de los hogares.

## 3. ¿Qué pasa si no pagan? (cuantitativo, con dos contabilidades)
Quien no convierte queda sin estatus en 2031. El efecto fiscal de esa persona depende de cómo se cuente:
- **(A) Mi contabilidad (UPC + aportes + IVA, nota 05):** regularizar cuesta al fisco ≈ USD 255 por persona-año (afiliación a salud subsidiada). Con esta lectura, la baja conversión "ahorra" dinero y eliminar la tarifa tendría un costo.
- **(B) Literatura (JEEA, resumen no verificado):** los hogares con PEP cuestan USD 446 menos al año al Estado (≈ USD 196 por persona-año con 2,3 venezolanos por hogar; ≈ USD 110 si el hogar es de 4). Con esta lectura, eliminarla **puede ser favorable fiscalmente**.
- **Punto de equilibrio bajo (B):** si la tarifa se elimina, la conversión debe subir de 50% a **≥ 62%** (horizonte de 10 años), o de 70% a **≥ 87%**, para no perder fiscalmente. Con horizonte de 5 años y conversión base de 70% no alcanza ni con 100%. Eliminar solo la visa (dejar el estudio de USD 56) exige 60% y 84%; una rebaja a la mitad, 55% y 77% (`t13b`).
- La contabilidad (A) no incluye costos que se evitan al tener a la gente regularizada (urgencias, informalidad, riesgos de salud pública) y (B) puede no ser trasladable a 2026. **La evidencia no permite concluir que el balance fiscal sea favorable a eliminar la tarifa.**

## 4. Argumentos cualitativos
**A favor de eliminarla o reducirla**
- La regularización (PEP) mejora formalidad, ingreso, consumo y salud (JEEA, notas 04 y 06); un trámite caro puede dejar a una parte de los PPT en la irregularidad en 2031 y revertir esos efectos (EPM, sin PPT: afiliación a salud 17,6% vs 90,6%).
- El PPT fue gratuito y tuvo cobertura alta (65,6%); en la EPM, entre quienes no tienen permiso, 43% señala dificultades con la entidad y 17,7% no cumplir requisitos: el costo no aparece como opción medida. La tarifa añadiría una barrera nueva.
- Capacidad administrativa: ola de ~0,8 M de nuevos elegibles en dos años; un trámite masivo y barato es más fácil de ordenar.
- Seguridad jurídica: 1,15 M de personas con un vencimiento común en 2031 (riesgo de "acantilado").
- El ingreso esperado (USD 535 M una vez) es pequeño frente al aporte económico y fiscal anual de esta población (≈ COP 1,5 billones al año según la OIM).
- La tarifa ya diferencia por categoría: esta es una de las más altas (USD 408 de visa frente a USD 279 para profesional independiente), lo que sugiere margen para ajustarla por resolución.

**En contra**
- Crisis fiscal: son ingresos que el Ministerio deja de percibir (hasta COP 1,7 billones), sin contrapartida segura; el recaudo financia al Fondo Rotatorio.
- Equidad y precedentes: otros extranjeros pagan por su visa; una exención amplia genera presión por trato igual.
- Recuperación de costos: el estudio (USD 56) cubre el análisis del trámite; la visa (USD 408) es en buena parte un ingreso.
- El PPT sigue vigente hasta 2031: no hay urgencia y el plazo puede ampliarse.
- La Visa R (5 años, renovable por traspaso) da más estabilidad que el PPT; en la contabilidad A, más gasto público posterior.

## 5. Conclusión
- **No hay evidencia suficiente para afirmar que eliminar la tarifa mejore el balance fiscal**, pero tampoco que lo empeore de forma importante: está en juego como máximo 0,15% del PIB, una sola vez, y esos ingresos son del Fondo Rotatorio.
- La opción mejor respaldada es una **reducción selectiva y gradual**, no una eliminación total: (1) reducir la tarifa total a la mitad (≈ USD 232): mantener el estudio (USD 56) y bajar la visa de USD 408 a ≈ USD 176; (2) exonerar a menores y hogares vulnerables; (3) permitir pagos en cuotas; (4) escalonar los trámites por año de elegibilidad (2027–28) y evaluar la ampliación del plazo del PPT. Solo con el estudio, la tarifa del hogar supera un mes de ingreso en 8% de los hogares, en vez de 65%.
- Nota 08: el 83% de los venezolanos quiere quedarse y la mediana de residencia es de 6 años, lo que acota la conversión máxima (~83–90%) y refuerza el argumento de horizonte de inversión, aunque la EPM no muestra que el PPT aumente el emprendimiento.
- Pendiente para sostenerlo con rigor: (i) leer el recuadro "Tenga en cuenta que…" y la fila de beneficiarios (menores) en la misma página; (ii) confirmar el texto vigente del art. 91 de la Res. 5477; (iii) obtener el número oficial de titulares de PPT y su antigüedad; (iv) leer el JEEA completo (cálculo fiscal por hogar); (v) medir el efecto precio sobre la conversión (hoy es una suposición).
