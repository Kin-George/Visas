# Visa-R · 02 · Encuesta Pulso de la Migración (EPM, DANE): qué trae y qué no

Fuente: catálogo de microdatos del DANE (lectura de las páginas de variables, 12-nov-2026). Lo marcado *(no verificado)* salió de resúmenes y no de texto literal.

| Ronda | Catálogo | Campo | Personas completas |
|---|---|---|---|
| V-2023 | [799](https://microdatos.dane.gov.co/index.php/catalog/799) | mar–may 2023 | 6.581 |
| VI-2023 | [809](https://microdatos.dane.gov.co/index.php/catalog/809) | 2023 | *(no leído)* |
| VIII-2025 | [879](https://microdatos.dane.gov.co/index.php/catalog/879) | 12 may–11 jul 2025 | 7.532 |

## Sí trae (ronda VIII-2025)
- **Permiso**: `Ide14__1…6` (selección múltiple: salvoconducto, **PPT**, PEP, PEPFF, ninguno, otro); año y mes del PPT (`Ide14_2`, `Ide14_3`); motivo de no tener permiso (`Ide15__1…8`).
- **Empleo**: actividad última semana (`ml5`), horas semanales (`ml3_18`), tipo de contrato (`ml3_19`), dificultades para conseguir empleo (`ml15`, `ml16`).
- **Salud y pensión**: afiliación (`ml17`), régimen (`ml18`), razón de no afiliación (`ml20`), pensión (`sd2`).
- **Llegada**: año de primera y última entrada (`sm1`, `sm3`). **Remesas** enviadas el último mes (`ir7`). Nacionalidad (`Ide16`).
- **Proxies de bienestar**: comidas al día (`ch7`), dificultad para comprar alimentos (`ch15`).

## No trae (en los grupos que leí)
- **Ingresos laborales o del hogar**: no aparecen. Falta revisar el grupo VG5 de la ronda 8 y los grupos de las rondas 5 y 6.
- **Gasto o consumo del hogar**: tampoco; solo proxies de seguridad alimentaria.
- No incluye colombianos como grupo de comparación (solo conteo de personas del hogar).

## Diseño
- Hogares con al menos un migrante venezolano mayor de 15 años; **23 ciudades y áreas metropolitanas**; excluye San Andrés, Arauca, Casanare, Putumayo, Amazonas, Guaviare, Guainía, Vaupés y Vichada.
- Entrevista telefónica. Muestra a partir de la GEIH; factores de expansión ajustados por estrato, género, tipo de migrante y mes.
- Desde la ronda 8 incluye venezolanos con 5 años o más en el país (nacidos en Venezuela); antes, solo los de los últimos 5 años y retornados.

## Cifras publicadas del PPT (prensa, no verificadas con microdatos)
- Ronda VI-2023: 63,7% reporta PPT ([La República](https://www.larepublica.co/economia/mas-de-81-de-migrantes-venezolanos-se-quedaria-en-colombia-en-proximos-anos-3760365)).
- Ronda VIII-2025: 65,6% reporta PPT ([Portafolio](https://www.portafolio.co/economia/crecimiento/ocho-de-cada-diez-migrantes-venezolanos-planean-quedarse-en-colombia-segun-el-dane-643062)).
- Comparar con la afiliación a salud en la GEIH 2025 (65,5%): coinciden, lo que respalda usarla como proxy de regularización.

## Descarga y verificación (12-nov-2026)
- Descargados desde el catálogo 879 del DANE (acceso libre, sin registro): `Datos/Raw/EPM_VIII_2025/EPM8_Personas.zip` (811 KB) y `EPM8_Hogares.zip` (106 KB), con .csv, .dta y .sav (descomprimidos en `extraido_*`). Las etiquetas de variable vienen vacías: se necesita el diccionario del catálogo.
- Personas: 7.532 registros, 103 variables; hogares: 4.110 registros, 17 variables. Factor de expansión `FEX_PER` (suma 975 mil; 818 mil entre quienes respondieron la pregunta de permiso).
- **Confirmado: no hay variables de ingreso ni de gasto** en personas ni en hogares (el módulo de hogares es de seguridad alimentaria).
- PPT (`Ide14__2`) ponderado: **65,6%** (coincide con Portafolio); ninguno de los permisos: 30,6%; PEP 1,5%.
- Primera mirada, entre quienes respondieron: afiliación a salud 90,1% con PPT vs 17,5% sin PPT; cotiza a pensión 12,8% vs 1,9%; ocupado la última semana 66,9% vs 62,8%. Sin controles; los registros sin dato en `Ide14` son los de nacionalidad 2 y 3 (`Ide16`), que no se les pregunta.
- La afiliación a salud es entonces un proxy muy fuerte del PPT, lo que valida su uso en la GEIH.
