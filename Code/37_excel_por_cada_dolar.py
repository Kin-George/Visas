"""Visa-R / 37: Excel que construye, de inicio a fin, la frase
"Por cada dólar que Cancillería deja de recibir por la Visa R, el país gana X".
Hojas: Leeme, Supuestos (insumos con fuente), Calculo (pasos con fórmulas), Sensibilidad (conversión x costo de trámite).
Salida: Docs/Calculo_por_cada_dolar_Visa_R.xlsx"""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Docs" / "Calculo_por_cada_dolar_Visa_R.xlsx"
F = "Arial"
BLUE, GREEN, BLACK = "0000FF", "008000", "000000"
YELLOW = PatternFill("solid", fgColor="FFFF00")
HEAD = PatternFill("solid", fgColor="1F3B5C")
SEC = PatternFill("solid", fgColor="DCE6F2")
KEY = PatternFill("solid", fgColor="FDE9D9")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
USD0, USD2, NUM0, PCT1, X1 = '"USD "#,##0;("USD "#,##0);-', '"USD "#,##0.00', '#,##0;(#,##0);-', '0.0%', '0.0"x"'
COP0 = '"COP "#,##0'

wb = Workbook()


def font(color=BLACK, bold=False, size=10, white=False):
    return Font(name=F, size=size, bold=bold, color="FFFFFF" if white else color)


def header(ws, row, labels, widths=None):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row, j, t); c.font = font(bold=True, white=True); c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[chr(64 + j)].width = w


# ======================================================================== Leeme
ws = wb.active; ws.title = "Leeme"
ws.column_dimensions["A"].width = 110
txt = [
    ("Visa R: «por cada dólar que Cancillería deja de recibir, el país gana X»", True, 14),
    ("Cálculo de inicio a fin. Todo en 2025: PIB DANE, GEIH 2025, TRM 4.052,86.", False, 10),
    ("", False, 10),
    ("Cómo está organizado", True, 11),
    ("1. Supuestos: cada insumo en su propia celda, con unidad y fuente.", False, 10),
    ("2. Calculo: ocho pasos con fórmulas que solo leen de Supuestos. Termina en la frase lista para usar.", False, 10),
    ("3. Sensibilidad: el resultado fiscal según la tasa de conversión y el costo de tramitar cada visa.", False, 10),
    ("4. Visa_cero_2027: si la visa es gratis desde 2027, año a año hasta 2036, con el bono de residencia (hipótesis de mayor consumo) y la regularidad conservada desde 2031.", False, 10),
    ("", False, 10),
    ("Convenciones de color", True, 11),
    ("Texto azul = insumo escrito a mano (se puede cambiar). Texto negro = fórmula. Texto verde = viene de otra hoja.", False, 10),
    ("Fondo amarillo = palancas para discutir (conversión, costo de trámite, años de horizonte).", False, 10),
    ("Fondo rosado = resultados clave.", False, 10),
    ("", False, 10),
    ("La lógica en una línea", True, 11),
    ("X = beneficio anual de las personas que siguen regulares gracias a la tarifa cero ÷ lo que Cancillería deja de recaudar (más el costo de tramitar, si se incluye).", False, 10),
    ("Contrafactual: tarifa de USD 464 frente a tarifa cero. No se compara «regular frente a nada».", False, 10),
    ("", False, 10),
    ("Cuidados para defender la cifra", True, 11),
    ("• El beneficio empieza en mayo de 2031, cuando vence el PPT: antes de esa fecha los titulares ya son regulares.", False, 10),
    ("• El recaudo se pierde una sola vez (2027-2031); el beneficio se repite cada año. Por eso la frase dice «cada año».", False, 10),
    ("• PIB, consumo e impuestos no se suman: los impuestos ya son parte del PIB. Una medida por frase.", False, 10),
    ("• Efectos de la regularidad del PEP 2018 (Ibáñez et al., 2025, JEEA): de corto plazo; extrapolarlos al PPT y a la Visa R es un supuesto.", False, 10),
    ("• Conservador: el costo fiscal del JEEA está en dólares de 2020 y no se incluye el efecto adicional de la residencia permanente.", False, 10),
    ("• Costo de tramitar cada visa: desconocido (pedir a Cancillería). Se incluye como palanca y se calcula el punto de equilibrio.", False, 10),
]
for i, (t, b, s) in enumerate(txt, 1):
    c = ws.cell(i, 1, t); c.font = font(bold=b, size=s); c.alignment = Alignment(wrap_text=True)

# ======================================================================== Supuestos
ws = wb.create_sheet("Supuestos")
header(ws, 1, ["Insumo", "Valor", "Unidad", "Fuente"], [52, 18, 22, 95])
S = {}
rows = [
    ("sec", "A. Ingreso de los venezolanos"),
    ("masa", "Ingreso laboral anual de los venezolanos", 13.801e12, "COP al año", COP0,
     "DANE, GEIH 2025 (12 meses): suma de INGLABO x factor de expansión. Venezolanos = nacidos en Venezuela con nacionalidad solo extranjera (Code/34)."),
    ("pob", "Población venezolana en la GEIH", 1_757_000, "personas", NUM0, "DANE, GEIH 2025, promedio de los 12 meses (Code/34)."),
    ("cob", "Proporción con permiso (regulares)", 0.66, "fracción", PCT1, "DANE, Encuesta Pulso de la Migración (EPM) VIII-2025."),
    ("ef", "Efecto del permiso sobre el ingreso laboral", 0.22, "fracción", PCT1,
     "Ibáñez, Moya, Ortega, Rozo y Urbina (2025), Life Out of the Shadows, Journal of the European Economic Association 23(3)."),
    ("shl", "Participación del trabajo en el PIB", 0.54, "fracción", PCT1, "DANE, cuentas nacionales, enfoque del ingreso (supuesto usado en todo el proyecto)."),
    ("trm", "Tasa de cambio", 4052.86, "COP por USD", '#,##0.00', "Banco de la República, TRM promedio 2025."),
    ("sec", "B. Costo fiscal neto por hogar"),
    ("fsin", "Costo fiscal neto por hogar sin permiso", 1056, "USD de 2020 al año", USD0, "Ibáñez et al. (2025), JEEA, cuadro 7."),
    ("fcon", "Costo fiscal neto por hogar con permiso", 610, "USD de 2020 al año", USD0, "Ibáñez et al. (2025), JEEA, cuadro 7."),
    ("hog", "Venezolanos por hogar", 2.25, "personas", '0.00', "Ibáñez et al. (2025), JEEA (tamaño del hogar de la muestra)."),
    ("sec", "C. Población y visas"),
    ("quieren", "Titulares de PPT que quieren quedarse", 1_770_136, "personas", NUM0,
     "1.975.752 PPT autorizados (Migración Colombia, oct-2026) x 89,6 % que quiere quedarse (EPM VIII-2025)."),
    ("conv", "Tasa de conversión con tarifa cero", 0.80, "fracción", PCT1,
     "Palanca. 80 % = afiliación a salud de venezolanos con 5+ años en el país (81 %, GEIH); menor que el 86 % que completó el ETPV. Prudente: 50 % (54,8 % de titulares de PPT con cuenta bancaria, EPM)."),
    ("vt31", "Visas R a mayo de 2031 si se mantiene la tarifa", 53_733, "visas", NUM0, "Tendencia lineal de las visas R otorgadas a venezolanos (Cancillería)."),
    ("vt", "Visas R pagadas entre 2027 y 2031 si se mantiene la tarifa", 44_580, "visas", NUM0, "Misma tendencia, solo 2027-2031 (lo que dejaría de recaudarse)."),
    ("tar", "Tarifa de la Visa R", 464, "USD por visa", USD0, "Cancillería, tarifa vigente (estudio + expedición)."),
    ("sec", "D. Palancas de discusión"),
    ("ctram", "Costo de tramitar cada visa (si se incluye)", 0, "USD por visa", USD0, "Palanca. Dato no disponible: pedir a Cancillería. 0 = no se incluye; ver punto de equilibrio en Calculo."),
    ("anios", "Años de beneficio que se cuentan", 5, "años", '0', "Palanca. Años de beneficio desde mayo de 2031 para el cociente acumulado (5 = 2031-2036)."),
    ("sec", "E. Residencia permanente (hipótesis) y calendario desde 2027"),
    ("vbase", "Venezolanos con Visa R antes de 2027", 8_440, "visas", NUM0, "Excel del equipo (base de la tendencia de visas con tarifa)."),
    ("ahorro", "Parte del ingreso que ahorran hoy", 0.10, "fracción", PCT1, "Supuesto del proyecto (Code/27-35)."),
    ("remesas", "Parte del ingreso que envían en remesas hoy", 0.10, "fracción", PCT1, "Supuesto del proyecto (Code/27-35)."),
    ("efcons", "Efecto del permiso sobre el consumo", 0.48, "fracción", PCT1, "Ibáñez et al. (2025), JEEA."),
    ("facah", "Cuánto más ahorran los migrantes temporales que los permanentes", 0.26, "fracción", PCT1,
     "De Arcangelis y Joxhe (2015), IZA Journal of Migration: propensión a ahorrar 26 % mayor en temporales (Reino Unido)."),
    ("remperm", "Remesas con residencia permanente", 0.05, "fracción del ingreso", PCT1,
     "Palanca (hipótesis). Dustmann y Mestres (2010): cambiar los planes de retorno cambia mucho las remesas; el 5 % es supuesto propio."),
    ("incres", "Aumento del ingreso con residencia permanente", 0.0, "fracción", PCT1,
     "Palanca (hipótesis). 0 = escenario central. Escenario alto: 6 % (piso del efecto salarial de la legalización permanente IRCA, EE. UU., 1986)."),
]
r = 2
for row in rows:
    if row[0] == "sec":
        c = ws.cell(r, 1, row[1]); c.font = font(bold=True);
        for j in range(1, 5):
            ws.cell(r, j).fill = SEC
        r += 1; continue
    key, lab, val, uni, fmt, src = row
    ws.cell(r, 1, lab).font = font()
    c = ws.cell(r, 2, val); c.font = font(BLUE); c.number_format = fmt; c.border = BOX
    if key in ("conv", "ctram", "anios", "remperm", "incres"):
        c.fill = YELLOW
    ws.cell(r, 3, uni).font = font()
    s = ws.cell(r, 4, src); s.font = font(size=9); s.alignment = Alignment(wrap_text=True, vertical="top")
    S[key] = f"Supuestos!$B${r}"
    r += 1
ws.freeze_panes = "A2"

# ======================================================================== Calculo
ws = wb.create_sheet("Calculo")
header(ws, 1, ["Paso", "Concepto", "Valor", "Unidad", "Fórmula en palabras"], [7, 58, 20, 20, 80])
C = {}
steps = [
    ("sec", "Paso 1. Ingreso laboral por persona: regular frente a irregular"),
    ("1a", "ing_prom", "Ingreso laboral promedio por venezolano", f"={S['masa']}/{S['pob']}", "COP al año", COP0, "Ingreso total de los venezolanos ÷ población venezolana"),
    ("1b", "ing_irr", "Ingreso de un irregular", f"=C{{ing_prom}}/((1-{S['cob']})+{S['cob']}*(1+{S['ef']}))", "COP al año", COP0,
     "El promedio mezcla 34 % irregulares y 66 % regulares que ganan 22 % más: promedio ÷ (0,34 + 0,66 x 1,22)"),
    ("1c", "ing_reg", "Ingreso de un regular", f"=C{{ing_irr}}*(1+{S['ef']})", "COP al año", COP0, "Irregular x 1,22"),
    ("sec", "Paso 2. Aporte al PIB por persona"),
    ("2a", "pib_irr", "PIB que genera un irregular", f"=C{{ing_irr}}/{S['shl']}/{S['trm']}", "USD al año", USD0, "Ingreso ÷ 0,54 (el trabajo es 54 % del PIB) ÷ TRM"),
    ("2b", "pib_reg", "PIB que genera un regular", f"=C{{ing_reg}}/{S['shl']}/{S['trm']}", "USD al año", USD0, "Ingreso ÷ 0,54 ÷ TRM"),
    ("2c", "pib_pp", "PIB adicional por ser regular", "=C{pib_reg}-C{pib_irr}", "USD por persona al año", USD0, "Regular − irregular"),
    ("sec", "Paso 3. Costo fiscal neto por persona"),
    ("3a", "fis_irr", "Costo fiscal neto de un irregular", f"={S['fsin']}/{S['hog']}", "USD al año", USD0, "Costo por hogar sin permiso ÷ venezolanos por hogar"),
    ("3b", "fis_reg", "Costo fiscal neto de un regular", f"={S['fcon']}/{S['hog']}", "USD al año", USD0, "Costo por hogar con permiso ÷ venezolanos por hogar"),
    ("3c", "fis_pp", "Ahorro fiscal por ser regular", "=C{fis_irr}-C{fis_reg}", "USD por persona al año", USD0,
     "Con permiso el hogar paga más IVA y aportes y recibe casi el mismo gasto público"),
    ("sec", "Paso 4. ¿Cuántas personas más siguen regulares gracias a la tarifa cero?"),
    ("4a", "v0", "Visas con tarifa cero", f"={S['conv']}*{S['quieren']}", "personas", NUM0, "Conversión x titulares de PPT que quieren quedarse"),
    ("4b", "vt31", "Visas si se mantiene la tarifa", f"={S['vt31']}", "personas", NUM0, "Tendencia a mayo de 2031"),
    ("4c", "adic", "Personas adicionales que siguen regulares", "=C{v0}-C{vt31}", "personas", NUM0, "Tarifa cero − con tarifa"),
    ("sec", "Paso 5. Denominador: lo que deja de recibir Cancillería"),
    ("5a", "rec", "Recaudo que se deja de recibir (2027-2031)", f"={S['vt']}*{S['tar']}", "USD (una sola vez)", USD0,
     "Solo pierde lo que habrían pagado quienes iban a sacar la visa de todos modos"),
    ("5b", "tram", "Costo de tramitar las visas adicionales", f"=C{{adic}}*{S['ctram']}", "USD (una sola vez)", USD0, "Personas adicionales x costo por visa (0 si no se incluye)"),
    ("5c", "den", "Costo total para el Estado", "=C{rec}+C{tram}", "USD (una sola vez)", USD0, "Recaudo perdido + costo de trámite"),
    ("sec", "Paso 6. Numerador: lo que gana el país cada año desde 2031"),
    ("6a", "ben_pib", "PIB que se conserva cada año", "=C{adic}*C{pib_pp}", "USD al año", USD0, "Personas adicionales x PIB adicional por persona"),
    ("6b", "ben_fis", "Ahorro fiscal neto cada año", "=C{adic}*C{fis_pp}", "USD al año", USD0, "Personas adicionales x ahorro fiscal por persona"),
    ("sec", "Paso 7. Resultado: por cada dólar"),
    ("7a", "x_pib", "Dólares de PIB por cada dólar, cada año", "=IF(C{den}=0,0,C{ben_pib}/C{den})", "USD por USD", '0.0', "PIB anual ÷ costo total"),
    ("7b", "x_fis", "Dólares de ahorro fiscal por cada dólar, cada año", "=IF(C{den}=0,0,C{ben_fis}/C{den})", "USD por USD", '0.0', "Ahorro fiscal anual ÷ costo total"),
    ("7c", "x_pib_h", "Dólares de PIB por cada dólar, acumulado en el horizonte", f"=C{{x_pib}}*{S['anios']}", "USD por USD", '0.0', "Por cada dólar x años de horizonte"),
    ("7d", "x_fis_h", "Dólares de ahorro fiscal por cada dólar, acumulado en el horizonte", f"=C{{x_fis}}*{S['anios']}", "USD por USD", '0.0', "Por cada dólar x años de horizonte"),
    ("7e", "equil", "Punto de equilibrio: costo de trámite por visa que cubre un solo año de ahorro fiscal",
     "=(C{ben_fis}-C{rec})/C{adic}", "USD por visa", USD0, "(Ahorro fiscal de un año − recaudo perdido) ÷ personas adicionales"),
    ("sec", "Paso 8. La frase"),
    ("8a", "frase", "Frase lista para usar",
     '="Eliminar la tarifa le cuesta al Estado unos USD "&TEXT(C{den}/1000000,"0")&" millones. A cambio, desde 2031 la economía conserva cerca de USD "&TEXT(C{ben_pib}/1000000,"#,##0")&" millones de PIB al año y el Estado se ahorra unos USD "&TEXT(C{ben_fis}/1000000,"0")&" millones al año: por cada dólar que Cancillería deja de recaudar, el Estado recupera "&TEXT(C{x_fis},"0")&" dólares cada año y la economía produce "&TEXT(C{x_pib},"0")&" dólares más cada año."',
     "", None, "Se actualiza sola al cambiar los supuestos"),
]
r = 2
pending = []
for st in steps:
    if st[0] == "sec":
        c = ws.cell(r, 1, st[1]); c.font = font(bold=True)
        for j in range(1, 6):
            ws.cell(r, j).fill = SEC
        r += 1; continue
    paso, key, lab, f, uni, fmt, expl = st
    C[key] = r
    ws.cell(r, 1, paso).font = font()
    ws.cell(r, 2, lab).font = font(); ws.cell(r, 2).alignment = Alignment(wrap_text=True, vertical="top")
    pending.append((r, f, fmt, key))
    ws.cell(r, 4, uni).font = font()
    e = ws.cell(r, 5, expl); e.font = font(size=9); e.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
for r_, f, fmt, key in pending:
    f2 = f
    for k, v in C.items():
        f2 = f2.replace("{" + k + "}", str(v))
    f2 = f2.replace("{{", "{").replace("}}", "}")
    c = ws.cell(r_, 3, f2); c.border = BOX
    only_link = f2.startswith("=Supuestos!") and "*" not in f2 and "/" not in f2
    c.font = font(GREEN if only_link else BLACK, bold=key in ("x_pib", "x_fis", "ben_pib", "ben_fis", "den"))
    if fmt:
        c.number_format = fmt
    if key in ("x_pib", "x_fis", "ben_pib", "ben_fis", "den", "equil"):
        c.fill = KEY
fr = C["frase"]
ws.merge_cells(start_row=fr, start_column=3, end_row=fr, end_column=5)
ws.cell(fr, 3).alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[fr].height = 75
ws.freeze_panes = "A2"

# ======================================================================== Sensibilidad
ws = wb.create_sheet("Sensibilidad")
ws.column_dimensions["A"].width = 30
for col in "BCDEFG":
    ws.column_dimensions[col].width = 14
ws["A1"] = "Dólares de ahorro fiscal por cada dólar, cada año (desde 2031)"; ws["A1"].font = font(bold=True, size=11)
ws["A2"] = "Filas: tasa de conversión con tarifa cero. Columnas: costo de tramitar cada visa (USD). Los demás supuestos vienen de Supuestos."
ws["A2"].font = font(size=9)
convs = [0.5, 0.6, 0.7, 0.8, 0.9]
costos = [0, 25, 50, 100, 150]


def grid(top, title, per_pp_ref):
    ws.cell(top, 1, title).font = font(bold=True)
    ws.cell(top + 1, 1, "Conversión \\ costo por visa").font = font(bold=True, white=True); ws.cell(top + 1, 1).fill = HEAD
    for j, cst in enumerate(costos, 2):
        c = ws.cell(top + 1, j, cst); c.font = font(BLUE, bold=True); c.number_format = USD0; c.fill = SEC
    for i, cv in enumerate(convs):
        rr = top + 2 + i
        c = ws.cell(rr, 1, cv); c.font = font(BLUE, bold=True); c.number_format = PCT1; c.fill = SEC
        for j in range(2, 2 + len(costos)):
            col = chr(64 + j)
            adic = f"($A{rr}*{S['quieren']}-{S['vt31']})"
            f = f"=IF(({S['vt']}*{S['tar']}+{adic}*{col}${top + 1})=0,0,{adic}*{per_pp_ref}/({S['vt']}*{S['tar']}+{adic}*{col}${top + 1}))"
            c = ws.cell(rr, j, f); c.number_format = '0.0'; c.font = font(); c.border = BOX
            if abs(cv - 0.8) < 1e-9 and costos[j - 2] == 0:
                c.fill = KEY


grid(4, "A. Ahorro fiscal del Estado", f"Calculo!$C${C['fis_pp']}")
ws["A12"] = "Dólares de PIB por cada dólar, cada año (desde 2031)"; ws["A12"].font = font(bold=True, size=11)
grid(13, "B. PIB de la economía", f"Calculo!$C${C['pib_pp']}")
ws["A21"] = "Celda rosada = escenario central (80 %, sin costo de trámite). Con costo de trámite el cociente baja, pero sigue por encima de 1 mientras el costo por visa sea menor al punto de equilibrio (Calculo, paso 7e)."
ws["A21"].font = font(size=9)

# ======================================================================== Escenario 2027: año a año con bono de residencia
ws = wb.create_sheet("Visa_cero_2027")
ws.column_dimensions["A"].width = 62
YRS = list(range(2027, 2037))
for j in range(len(YRS) + 2):
    ws.column_dimensions[chr(66 + j)].width = 13
ws["A1"] = "Visa R gratis desde 2027: beneficios año a año (tarifa cero frente a mantener USD 464)"; ws["A1"].font = font(bold=True, size=12)
ws["A2"] = ("Dos beneficios distintos: (1) bono de residencia: consumo adicional de quienes obtienen la visa, desde el año en que la obtienen (hipótesis); "
            "(2) regularidad conservada: desde junio de 2031, cuando vence el PPT, quienes no tienen visa pasan a ser irregulares.")
ws["A2"].font = font(size=9); ws["A2"].alignment = Alignment(wrap_text=True); ws.merge_cells("A2:L2"); ws.row_dimensions[2].height = 30

# --- bloque por persona
P = {}
pp = [("sec", "A. Por persona al año"),
      ("cons_prom", "Consumo promedio por venezolano en Colombia (COP)", f"=Calculo!$C${C['ing_prom']}*(1-{S['ahorro']}-{S['remesas']})", COP0,
       "Ingreso promedio x (1 − ahorro − remesas)"),
      ("cons_reg", "Consumo de un regular (USD)", f"=C{{cons_prom}}/((1-{S['cob']})+{S['cob']}*(1+{S['efcons']}))*(1+{S['efcons']})/{S['trm']}", USD0,
       "Mismo método que el ingreso: con permiso consumen 48 % más"),
      ("bono_pct", "Aumento del consumo con residencia permanente", f"=(1-{S['ahorro']}/(1+{S['facah']})-{S['remperm']})/(1-{S['ahorro']}-{S['remesas']})*(1+{S['incres']})-1",
       PCT1, "Ahorran menos (÷1,26), envían menos remesas y, si se activa, ganan más. Central: 8,8 %; bajo (sin cambio en remesas): 2,6 %; alto (+6 % de ingreso): 15,4 %"),
      ("bono_pp", "Consumo adicional por residencia (USD por persona al año)", "=C{cons_reg}*C{bono_pct}", USD0, "Consumo de un regular x aumento"),
      ("pibres_pp", "PIB adicional por residencia (USD por persona al año)", f"=Calculo!$C${C['pib_reg']}*{S['incres']}", USD0, "Solo si se activa el aumento de ingreso"),
      ("pib_pp", "PIB adicional por seguir regular (USD por persona al año)", f"=Calculo!$C${C['pib_pp']}", USD0, "Calculo, paso 2"),
      ("fis_pp", "Ahorro fiscal por seguir regular (USD por persona al año)", f"=Calculo!$C${C['fis_pp']}", USD0, "Calculo, paso 3")]
r = 4
pend = []
for it in pp:
    if it[0] == "sec":
        ws.cell(r, 1, it[1]).font = font(bold=True)
        for j in range(1, 13):
            ws.cell(r, j).fill = SEC
        r += 1; continue
    k, lab, f, fmt, expl = it
    P[k] = r; ws.cell(r, 1, lab).font = font(); pend.append((r, f, fmt))
    e = ws.cell(r, 4, expl); e.font = font(size=9); ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=12)
    r += 1
for r_, f, fmt in pend:
    for k, v in P.items():
        f = f.replace("{" + k + "}", str(v))
    f = f.replace("{{", "{").replace("}}", "}")
    c = ws.cell(r_, 3, f); c.number_format = fmt; c.border = BOX
    c.font = font(GREEN if f.startswith("=Calculo!") and "*" not in f else BLACK)
    if r_ == P["bono_pct"]:
        c.fill = KEY

# --- bloque año a año
r += 1
ws.cell(r, 1, "B. Año a año").font = font(bold=True)
for j in range(1, 13):
    ws.cell(r, j).fill = SEC
r += 1
hy = r
ws.cell(hy, 1, "Concepto").font = font(bold=True, white=True); ws.cell(hy, 1).fill = HEAD
for j, y in enumerate(YRS):
    c = ws.cell(hy, 2 + j, str(y)); c.font = font(bold=True, white=True); c.fill = HEAD; c.alignment = Alignment(horizontal="center")
c = ws.cell(hy, 2 + len(YRS), "Total"); c.font = font(bold=True, white=True); c.fill = HEAD
ELIG = {2027: 0.8118, 2028: 0.9634, 2029: 0.9956}
VT = {2027: 5_984, 2028: 7_450, 2029: 8_916, 2030: 10_382, 2031: 11_848}
FRAC = {2031: 7 / 12}
R = {}
lines = [
    ("elig", "Titulares de PPT que ya pueden pedir la visa (acumulado)", "in", lambda y: ELIG.get(y, 1.0), PCT1,
     "EPM VIII-2025: año de obtención del PPT; se puede pedir la visa tras 5 años."),
    ("vt", "Visas nuevas por año si se mantiene la tarifa", "in", lambda y: VT.get(y, 0), NUM0,
     "Tendencia lineal (Excel del equipo); suma 2027-2031 = 44.580. Después de 2031 no se cuentan."),
    ("frac", "Parte del año con el PPT vencido", "in", lambda y: FRAC.get(y, 1.0 if y > 2031 else 0.0), '0.00',
     "El PPT vence el 30 de mayo de 2031: 7/12 de 2031 y años completos después."),
    ("t0", "Titulares de visa con tarifa cero", "f", lambda col, prev: f"={S['conv']}*{S['quieren']}*{col}{{elig}}", NUM0, "Conversión x quieren quedarse x elegibles"),
    ("tt", "Titulares de visa si se mantiene la tarifa", "f",
     lambda col, prev: f"={S['vbase']}+{col}{{vt}}" if prev is None else f"={prev}{{tt}}+{col}{{vt}}", NUM0, "Base + visas acumuladas"),
    ("ad", "Titulares adicionales gracias a la tarifa cero", "f", lambda col, prev: f"={col}{{t0}}-{col}{{tt}}", NUM0, "Tarifa cero − con tarifa"),
    ("rec", "Recaudo que deja de recibir Cancillería (USD M)", "f", lambda col, prev: f"={col}{{vt}}*{S['tar']}/1000000", '#,##0.0', "Visas que se habrían pagado x USD 464"),
    ("tram", "Costo de tramitar las visas adicionales (USD M)", "f",
     lambda col, prev: f"=MAX({col}{{ad}}-{('0' if prev is None else prev + '{ad}')},0)*{S['ctram']}/1000000", '#,##0.0', "Visas nuevas adicionales x costo por visa"),
    ("bono", "(1) Bono de residencia: consumo adicional (USD M)", "f", lambda col, prev: f"={col}{{ad}}*$C${P['bono_pp']}/1000000", '#,##0.0',
     "Hipótesis: desde que obtienen la visa"),
    ("pibres", "(1) Bono de residencia: PIB adicional por ingreso (USD M)", "f", lambda col, prev: f"={col}{{ad}}*$C${P['pibres_pp']}/1000000", '#,##0.0',
     "Solo si se activa el aumento de ingreso"),
    ("pib", "(2) Regularidad conservada: PIB (USD M)", "f", lambda col, prev: f"={col}{{ad}}*$C${P['pib_pp']}*{col}{{frac}}/1000000", '#,##0.0', "Desde junio de 2031"),
    ("fis", "(2) Regularidad conservada: ahorro fiscal (USD M)", "f", lambda col, prev: f"={col}{{ad}}*$C${P['fis_pp']}*{col}{{frac}}/1000000", '#,##0.0',
     "Desde junio de 2031"),
]
r = hy + 1
for key, *_ in lines:
    R[key] = r; r += 1
for key, lab, kind, fn, fmt, note in lines:
    rr = R[key]
    ws.cell(rr, 1, lab).font = font(bold=key in ("bono", "pib", "fis", "rec"))
    ws.cell(rr, 1).comment = Comment(note, "Visa-R")
    prev = None
    for j, y in enumerate(YRS):
        col = chr(66 + j)
        if kind == "in":
            c = ws.cell(rr, 2 + j, fn(y)); c.font = font(BLUE)
        else:
            f = fn(col, prev)
            for k, v in R.items():
                f = f.replace("{" + k + "}", str(v))
            c = ws.cell(rr, 2 + j, f); c.font = font()
        c.number_format = fmt; c.border = BOX
        prev = col
    if key in ("rec", "tram", "bono", "pibres", "pib", "fis"):
        tc = chr(66 + len(YRS))
        c = ws.cell(rr, 2 + len(YRS), f"=SUM(B{rr}:{chr(65 + len(YRS))}{rr})"); c.number_format = fmt; c.font = font(bold=True); c.border = BOX

# --- resultados
r += 1
ws.cell(r, 1, "C. Por cada dólar que deja de recibir Cancillería (acumulado 2027-2036)").font = font(bold=True)
for j in range(1, 13):
    ws.cell(r, j).fill = SEC
r += 1
TOT = chr(66 + len(YRS))
den = f"({TOT}{R['rec']}+{TOT}{R['tram']})"
res = [("Costo total para el Estado (USD M)", f"={den}", '#,##0.0'),
       ("Dólares de consumo adicional por residencia (1)", f"=IF({den}=0,0,{TOT}{R['bono']}/{den})", '0.0'),
       ("Dólares de PIB por regularidad conservada (2)", f"=IF({den}=0,0,({TOT}{R['pib']}+{TOT}{R['pibres']})/{den})", '0.0'),
       ("Dólares de ahorro fiscal por regularidad conservada (2)", f"=IF({den}=0,0,{TOT}{R['fis']}/{den})", '0.0'),
       ("Solo 2027-2030 (antes de que venza el PPT): dólares de consumo adicional por residencia",
        f"=IF(SUM(B{R['rec']}:E{R['rec']})=0,0,SUM(B{R['bono']}:E{R['bono']})/(SUM(B{R['rec']}:E{R['rec']})+SUM(B{R['tram']}:E{R['tram']})))", '0.0')]
for lab, f, fmt in res:
    ws.cell(r, 1, lab).font = font(bold=True)
    c = ws.cell(r, 3, f); c.number_format = fmt; c.font = font(bold=True); c.fill = KEY; c.border = BOX
    r += 1
r += 1
notas = ["Cómo leerlo:",
         "• (1) y (2) no se suman: el consumo es parte del PIB por el lado del gasto, y el ahorro fiscal es otra forma de medir. Una medida por frase.",
         "• El bono de residencia es una hipótesis (ahorran menos por precaución y envían menos remesas): úsese como «podría», no como un hecho.",
         "• El bono se mide sobre el consumo de la GEIH (USD 1.740 por regular). Medido sobre las cuentas nacionales sería cerca de 3 veces mayor; aquí se deja el conservador.",
         "• Antes de 2031 el único beneficio nuevo es el bono de residencia: la regularidad ya la da el PPT. Esa fila responde a «¿qué gana el país si la visa es gratis desde 2027?» en los primeros años.",
         "• Palancas en Supuestos (amarillo): conversión, costo de trámite, remesas con residencia y aumento del ingreso."]
for t in notas:
    c = ws.cell(r, 1, t); c.font = font(size=9, bold=t.endswith(":")); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12)
    r += 1
ws.freeze_panes = ws.cell(hy + 1, 2)

# ======================================================================== Grafico (pr23 en Excel)
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties

gs = wb.create_sheet("Grafico")
gs.column_dimensions["A"].width = 60
for j in range(len(YRS)):
    gs.column_dimensions[chr(66 + j)].width = 10
gs["A1"] = "Visa R gratis desde 2027: lo que deja de recibir Cancillería frente a lo que gana el país (USD millones al año)"
gs["A1"].font = font(bold=True, size=12)
gs["A2"] = ("Hasta 2030: consumo adicional de los nuevos residentes (fila 1 de Visa_cero_2027). Desde 2031: PIB que se conserva (fila 2), el mayor de los dos. "
            "No se suman. Todo se recalcula al cambiar Supuestos.")
gs["A2"].font = font(size=9); gs.merge_cells("A2:K2"); gs["A2"].alignment = Alignment(wrap_text=True); gs.row_dimensions[2].height = 28
gs.cell(4, 1, "Año").font = font(bold=True, white=True); gs.cell(4, 1).fill = HEAD
gs.cell(5, 1, "Lo que gana el país").font = font(bold=True)
gs.cell(6, 1, "Lo que deja de recibir Cancillería").font = font(bold=True)
V = "Visa_cero_2027"
for j, y in enumerate(YRS):
    col = chr(66 + j)
    c = gs.cell(4, 2 + j, str(y)); c.font = font(bold=True, white=True); c.fill = HEAD; c.alignment = Alignment(horizontal="center")
    if y < 2031:
        f = f"={V}!{col}{R['bono']}"
    else:
        f = f"=MAX({V}!{col}{R['pib']}+{V}!{col}{R['pibres']},{V}!{col}{R['bono']})"
    c = gs.cell(5, 2 + j, f); c.font = font(GREEN); c.number_format = '#,##0'; c.border = BOX
    c = gs.cell(6, 2 + j, f"=-{V}!{col}{R['rec']}"); c.font = font(GREEN); c.number_format = '#,##0.0;-#,##0.0;-'; c.border = BOX
gs.cell(8, 1, "Cifras del título y subtítulo").font = font(bold=True)
TT = chr(66 + len(YRS))
sub = [("Recaudo total que deja de recibir Cancillería 2027-2031 (USD M)", f"={V}!{TT}{R['rec']}", '#,##0.0'),
       ("Personas que siguen regulares desde 2031 gracias a la tarifa cero", f"={V}!K{R['ad']}", NUM0),
       ("Dólares de consumo por cada dólar, 2027-2030", f"=SUM({V}!B{R['bono']}:E{R['bono']})/SUM({V}!B{R['rec']}:E{R['rec']})", '0.0'),
       ("Dólares de PIB por cada dólar, hasta 2036", f"=({V}!{TT}{R['pib']}+{V}!{TT}{R['pibres']})/{V}!{TT}{R['rec']}", '0.0')]
for i, (lab, f, fmt) in enumerate(sub):
    gs.cell(9 + i, 1, lab).font = font()
    c = gs.cell(9 + i, 2, f); c.number_format = fmt; c.font = font(GREEN, bold=True); c.fill = KEY; c.border = BOX

ch = BarChart(); ch.type = "col"; ch.grouping = "clustered"; ch.overlap = 100; ch.gapWidth = 60
ch.title = "Visa R gratis desde 2027 (USD millones al año)"
ch.y_axis.title = "USD millones"; ch.y_axis.majorGridlines = None
ch.add_data(Reference(gs, min_col=1, max_col=1 + len(YRS), min_row=5, max_row=6), from_rows=True, titles_from_data=True)
ch.set_categories(Reference(gs, min_col=2, max_col=1 + len(YRS), min_row=4, max_row=4))
s_gana, s_rec = ch.series
s_gana.graphicalProperties = GraphicalProperties(solidFill="1F3B5C")
for idx, y in enumerate(YRS):
    if y < 2031:
        dp = DataPoint(idx=idx); dp.graphicalProperties = GraphicalProperties(solidFill="9FC0EA"); s_gana.dPt.append(dp)
s_rec.graphicalProperties = GraphicalProperties(solidFill="EB6A35")
for s_ in (s_gana, s_rec):
    s_.dLbls = DataLabelList(); s_.dLbls.showVal = True
    for a in ("showSerName", "showCatName", "showLegendKey", "showPercent"):
        setattr(s_.dLbls, a, False)
s_gana.dLbls.numFmt = '#,##0'; s_rec.dLbls.numFmt = '"−"#,##0.0;"−"#,##0.0;'
s_gana.dLbls.position = 'outEnd'; s_rec.dLbls.position = 'outEnd'
ch.legend.position = "b"; ch.legend.overlay = False
ch.roundedCorners = False
ch.x_axis.delete = False; ch.y_axis.delete = False
ch.title.overlay = False; ch.y_axis.title.overlay = False
ch.y_axis.scaling.min = -200; ch.y_axis.scaling.max = 1200; ch.y_axis.majorUnit = 200
ch.x_axis.tickLblPos = "low"
ch.height = 10; ch.width = 24
gs.add_chart(ch, "A14")

wb.calculation.fullCalcOnLoad = True        # Excel recalcula todas las fórmulas al abrir
OUT.parent.mkdir(exist_ok=True)
wb.save(OUT)
print("guardado", OUT)
