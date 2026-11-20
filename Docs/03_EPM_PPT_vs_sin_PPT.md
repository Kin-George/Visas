# Visa-R · 03 · EPM VIII-2025: venezolanos con PPT vs sin PPT

Código: `Code/03_epm_ppt_comparacion.py`. Tablas: `Outputs/tables/t7_epm_ppt_vs_sin_ppt.csv` (completa, con IC) y `t7b_epm_ppt_por_anio_entrada.csv`.
Diccionario de variables (del DDI del DANE): `Docs/diccionario_EPM8_ddi.csv`.

## Método
- Muestra: 6.443 personas con nacionalidad venezolana a quienes se pregunta por permisos (65,6% ponderado tiene PPT).
- Modelo de probabilidad lineal ponderado (`FEX_PER`), errores agrupados por hogar. Controles: sexo, edad (3 grupos), año de primera entrada, actividad en Venezuela, entrada por paso no oficial, contactos previos, estado de origen.
- Dos comparaciones: **A** PPT vs todos los demás; **B** PPT vs quienes declaran no tener ningún permiso.
- **Es asociación, no efecto causal.** El PPT depende de la fecha de llegada (casi nadie llegado desde 2023 lo tiene) y de haberse inscrito.

## Resultados (diferencia ajustada, puntos porcentuales; comparación B entre paréntesis)
| Indicador | Con PPT | Sin PPT (A) | Dif. ajustada A (B) |
|---|---|---|---|
| Afiliado a salud | 90,6% | 17,6% | **+66 (+75)** |
| Afiliado a pensión | 13,1% | 1,9% | **+10 (+11)** |
| Ocupados con contrato escrito | 20,5% | 3,9% | **+16 (+16)** |
| Tiene cuenta en entidad financiera | 54,8% | 11,4% | **+38 (+38)** |
| Necesitó servicio de salud y no pudo acceder | 15,3% | 55,8% | **−37 (−42)** |
| Buscando trabajo | 4,2% | 6,7% | −2,2 (−2,7) |
| Trabajó la semana pasada | 66,9% | 62,8% | +3,2 (+4,3), no significativo en A |
| Horas semanales (ocupados) | 53,3 | 54,4 | −1,8 (−1,8), no significativo |
| Hogar: 3 comidas al día o más | 75,2% | 73,9% | +3,9 (+5,5), borde de significancia |
| Hogar: dificultad para comprar alimentos | 37,3% | 38,3% | −1,6 (−3,4), no significativo |
| Se ha sentido discriminado | 26,7% | 24,6% | −1,4 (−3,0), no significativo |
| Piensa permanecer en Colombia a 1 año | 89,6% | 84,0% | +3,8 (+4,7) |
| Envió remesas el último mes | 26,8% | 25,9% | −1,5 (+3,5), no significativo |

Los errores estándar y los IC95 están en `t7`.

## Lectura
1. El PPT se asocia con una **mejor inclusión formal**: salud, pensión, contrato escrito, acceso a servicios de salud y cuenta financiera. Son efectos grandes y robustos a los controles.
2. En **empleo, horas, seguridad alimentaria, discriminación y remesas** casi no hay diferencia una vez se controla por año de llegada. Con PPT hay algo más de ocupación (+3 a +4 pp) y menos búsqueda de empleo, pero el efecto no es preciso.
3. La antigüedad en el empleo parece una diferencia sin controles (+10 pp), pero desaparece al controlar por año de llegada: refleja que quienes tienen PPT llevan más tiempo en el país.
4. Los PPT se obtuvieron sobre todo en 2022 (52%) y 2021 (25%) (`Ide14_2`). Por año de primera entrada tiene PPT ≈ 75–83% de los llegados hasta 2020, 70% de 2021, 40% de 2022, 16% de 2023 y 6% de 2024+. Entre quienes entraron antes de 2022, el grupo sin PPT es pequeño y puede ser distinto (por ejemplo, no se inscribió o tuvo otro permiso).

## Cautelas
- Selección: quien obtiene PPT puede diferir en cosas no observadas (información, redes, documentos). Las diferencias en salud y contrato escrito son en parte mecánicas (la afiliación exige documento válido).
- "Necesitó servicio y no pudo acceder" se mide solo entre los 1.403 que tuvieron una necesidad de salud.
- Encuesta telefónica en 23 ciudades; no incluye ingresos ni gasto, y no hay un grupo de colombianos.
- La encuesta no identifica el municipio de residencia en Colombia (`Estado`/`Mpio` son del lugar de origen), así que no se controla por ciudad.
