# Visa-R · 04 · Aporte a la demanda interna y escenarios de cobertura del PPT

Código: `Code/04_demanda_interna_escenarios.py`. Tablas: `t8_consumo_anual_venezolanos_supuestos.csv`, `t8b_resumen_demanda_interna.csv`, `t9_escenarios_cobertura_PPT.csv`.
Son **escenarios con supuestos explícitos**, no estimaciones causales.

## 1. Cuánto ingreso laboral aportan hoy (GEIH 2025)
- 877 mil venezolanos ocupados (sin nacionalidad colombiana). Masa salarial: **COP 1,15 billones al mes ≈ COP 13,8 billones al año** (≈ 2,6% del ingreso laboral nacional). No incluye primas ni ingresos no laborales.
- Demanda de consumo implícita = masa salarial × (1 − ahorro − remesas). Con ahorro 0–20% y remesas 0–20% del ingreso, el consumo anual queda entre **COP 8,3 y 13,8 billones** (tabla `t8`). Los supuestos de ahorro y de monto de remesas no vienen de datos: la EPM solo dice que 27% envió remesas el último mes, no cuánto.
- Este aporte **ya existe con o sin PPT**: la mayoría trabaja en la informalidad (79%).

## 2. Qué aportaría el PPT adicionalmente (canal de formalización)
Encadeno dos estimaciones asociativas:
1. **EPM:** entre ocupados, tener PPT se asocia con +14,8 pp (EE 1,9) de afiliación a pensión y +16,0 pp (EE 1,9) de contrato escrito, con controles.
2. **GEIH:** entre venezolanos ocupados 2025–26, el empleo formal tiene un salario por hora **29% mayor** con controles de educación, edad, sexo, cohorte, departamento y rama (IC95 25–34%); sin controles la brecha es 55%.

Si la cobertura del PPT sube de 65,6% a 100%, la formalidad subiría ≈ 5 pp (3,9–6,4 pp con el IC de la EPM) y unos **45 mil trabajadores** se formalizarían. Con la prima ajustada, la masa salarial subiría **≈ COP 16 mil millones al mes (≈ 1,4%)**, con un rango de 12 a 19 mil millones según el IC. Con la prima simple (55%) serían ≈ 29 mil millones (2,6%). Con cobertura de 80% el efecto es aproximadamente la mitad de lo anterior (tabla `t9`).

## 3. Lectura para la tesis
- **La contribución económica de los venezolanos no depende de tener PPT**: ya aportan ≈ COP 14 billones anuales de ingreso laboral que se transforma en consumo. Este argumento no necesita el PPT.
- **El PPT agrega un canal pequeño en ingreso (≈ 1–3% de la masa salarial) pero grande en inclusión**: salud, pensión, contrato, bancarización y acceso a servicios (nota 03). Esos beneficios tienen valor para los migrantes y para la sostenibilidad del sistema, y no se capturan en la demanda.
- Si el argumento fuera "el PPT aumenta el aporte económico", con estos datos solo se sostiene como un efecto moderado, vía formalidad. Falta medir los aportes fiscales (cotizaciones, IVA), que van más allá de lo que estima este script.

## 4. Cautelas
- Todo se apoya en asociaciones: la prima de formalidad puede reflejar habilidades no observadas, y el efecto del PPT sobre la formalidad puede reflejar quién se inscribe.
- Se mezclan dos encuestas (EPM de 23 ciudades por teléfono y GEIH nacional); se asume que el efecto del PPT medido en la primera aplica a la segunda.
- Se supone que los nuevos formalizados ganan el ingreso medio de los informales más la prima; no se modelan cambios de horas, de ocupación ni desempleo, ni efectos sobre el empleo de los colombianos.
- La masa salarial es del 2025 en pesos corrientes; la GEIH subcubre a los migrantes recientes, por lo que probablemente es una cota inferior.
