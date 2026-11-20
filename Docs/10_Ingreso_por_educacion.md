# Visa-R · 10 · Ingreso laboral mediano por nivel educativo

Código: `Code/13_ingreso_educacion.py`. Tablas: `t18` (medianas y n por celda), `t18b` (composición educativa), `t18c` (prima de afiliación ajustada), `t18d` (por zona urbana/rural).

## Limitación de datos
La GEIH tiene ingresos pero no pregunta por el PPT; la EPM tiene el PPT pero no ingresos. **No se puede cruzar PPT × ingreso.** Como indicador de regularización se usa la **afiliación a salud** (EPM: 91% de quienes tienen PPT está afiliado y 18% de quienes no lo tienen). Es un indicador imperfecto.

## Resultados (GEIH 2025-2026, ocupados de 18+ con ingreso positivo, salarios mínimos de cada año)
| Nivel educativo | Colombianos | Venezolanos | Venezolanos afiliados | Venezolanos no afiliados |
|---|---|---|---|---|
| Todos | 1,00 | 0,91 | 0,96 | 0,86 |
| Hasta primaria | 0,57 | 0,80 | 0,74 | 0,83 |
| Secundaria | 0,70 | 0,84 | 0,84 | 0,84 |
| Media | 1,00 | 0,91 | 0,97 | 0,86 |
| Técnica o tecnológica | 1,10 | 1,00 | 1,00 | 0,91 |
| Universitaria o más | 2,00 | 1,02 | 1,03 | 1,00 |

- El ingreso de los venezolanos casi no sube con la educación (0,80 → 1,02); el de los colombianos pasa de 0,57 a 2,00. Con educación universitaria, la mediana de los venezolanos es la mitad.
- En zonas urbanas el patrón se mantiene (colombianos / venezolanos): primaria 0,67 / 0,80; secundaria 0,81 / 0,84; media 1,00 / 0,91; técnica 1,12 / 1,00; universitaria 2,00 / 1,03. En zonas rurales no hay suficientes venezolanos con educación técnica o universitaria.
- Composición: 12% de los ocupados venezolanos tiene educación universitaria o más (22% de los colombianos).
- Ingreso por hora de afiliados frente a no afiliados (venezolanos): +9% sin controles; +7% controlando educación; +10% con educación, edad, sexo, zona y departamento; +11% además con año de llegada (IC95 de la última: 7% a 14%).

## Cautelas
- El indicador clasifica mal a una parte de las personas (reduce la diferencia estimada) y la afiliación puede reflejar rasgos no observados (la aumenta). No es un efecto del PPT ni es comparable con el +22% del JEEA para el PEP.
- Medianas de ingreso laboral de ocupados: excluyen a quienes no trabajan; las celdas más pequeñas (técnica o tecnológica, no afiliados) tienen 224 observaciones.
- La pérdida de valor de las calificaciones es una lectura consistente con los datos; la GEIH no permite distinguir entre homologación de títulos, tipo de ocupación e informalidad.
