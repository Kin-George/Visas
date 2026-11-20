# Visa-R · 09 · Curva precio–recaudo–derrame de la tarifa

Código: `Code/10_curva_precio_recaudo.py` (cálculo) y `Code/08_figuras_nota.py` (figura `nota_fig7_curva_precio.png`). Tablas: `t17_curva_precio_recaudo.csv`, `t17b_optimos_por_escenario.csv`.
**Es un modelo ilustrativo: la demanda de la visa no está medida.**

## Modelo
- **Conversión(F)** = 85% × proporción de hogares con venezolanos para los que `F × TRM × n.º de venezolanos del hogar ≤ θ × ingreso laboral mensual del hogar` (GEIH 2026, ponderado por persona). El 85% es el techo de quienes quieren quedarse (GEIH 83%, EPM 86%). θ = meses de ingreso que un hogar pagaría por la tarifa: central 2; sensibilidad 1 y 3.
- **Recaudo(F)** = titulares (≈ 1,15 M) × conversión × F: ingreso de la Cancillería, una sola vez.
- **Derrame(F)** = titulares × conversión × S, con S = USD 196 por persona-año × 5 años = USD 980 (contabilidad de la literatura, resumen del JEEA; alternativa A: −USD 255 × 5, costo de salud).
- **Valor total** = recaudo + derrame.

## Resultados (θ = 2)
- El recaudo de la Cancillería es máximo cerca de **USD 500** por persona: **el precio vigente (USD 464) ya está cerca de ese máximo**, pero solo convierte 44% de los titulares.
- Con el derrame, el valor total es máximo en ≈ **USD 140** (conversión ≈ 78%).
- De USD 464 a USD 232: conversión 44% → 69%; recaudo de la Cancillería −21% (conserva 79%); valor total +33%; con USD 232 se alcanza 97% del valor máximo.

## Sensibilidad (`t17b`)
| θ (meses de ingreso que se pagarían) | Precio que maximiza el recaudo | Precio que maximiza recaudo + derrame |
|---|---|---|
| 1 | USD 270 | USD 0 |
| 2 (central) | USD 500 | USD 140 |
| 3 | USD 690 | USD 270 |

- Si θ = 1, el precio vigente ya está por encima del que maximiza el recaudo: bajarlo *aumenta* lo que recauda la Cancillería.
- Con la contabilidad A (el costo de salud domina y no hay derrame positivo), el óptimo es un precio alto: **la conclusión de reducir la tarifa depende de que el derrame sea positivo**.

## Cautelas
- La forma de la demanda (techo de 85%, θ) es un supuesto; solo se puede medir con evidencia de conversión (por ejemplo, un piloto o la experiencia con otras visas).
- El derrame de USD 980 por persona se basa en un resumen de un tercero y en el reparto del costo neto entre 2,3 venezolanos por hogar; no incluye costos de educación ni otros.
- No se descuentan flujos futuros ni se modelan efectos de segunda vuelta.

## Valores clave para la posición de tarifa cero (θ = 2, suavizado anclado en F = 0)
| Tarifa (USD) | Conversión | Recaudo esperado (USD M) | Valor total (USD M) |
|---|---|---|---|
| 464 | 44% | 233 | 725 |
| 232 | 69% | 185 | 963 |
| 56 | 80% | 52 | 956 |
| 0 | 85% | 0 | 959 |

Sensibilidad en θ (tarifa vigente frente a gratuidad): θ = 1, conversión 19% y valor total 310 frente a 959; θ = 3, conversión 60% y valor total 992 frente a 959. La gratuidad supera a la tarifa vigente si esta convierte menos de 58% (derrame a 5 años) o 69% (a 10 años).
