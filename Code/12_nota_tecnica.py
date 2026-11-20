"""Visa-R / 12: nota tecnica en Word (maximo 5 paginas). Salida: Visa-R/Docs/Nota_Ejecutiva_Visa-R.docx
Estructura de nota de politica: resumen, secciones numeradas, cuadros de lineas finas, graficos con titulo arriba y fuente abajo,
citas numericas y referencias al final. Cifras leidas de Outputs/tables; graficos de Code/11_graficos_nota.py."""
from pathlib import Path
import numpy as np
import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor

ROOT = Path(__file__).resolve().parents[1]
FIG, TAB = ROOT / "Outputs" / "Figures", ROOT / "Outputs" / "tables"
OUT = ROOT / "Docs" / "Nota_Ejecutiva_Visa-R.docx"
FONT, INK, GRIS = "Times New Roman", RGBColor(0x1A, 0x1A, 0x1A), RGBColor(0x55, 0x55, 0x55)
NB = " "

# ------------------------------------------------------------------ referencias (numeradas por orden de primera cita)
REFS = {
    "costos": "Ministerio de Relaciones Exteriores de Colombia. Costos de trámites de visa: Residente, tiempo acumulado del Estatuto Temporal (estudio USD 56; visa USD 408). "
              "https://www.cancilleria.gov.co/atencion-y-servicio-al-ciudadano/tramites-y-servicios/visa/costos (consultado el 12 de noviembre de 2026).",
    "geih": "Departamento Administrativo Nacional de Estadística (DANE). Gran Encuesta Integrada de Hogares (GEIH), microdatos 2022-2026 (2026: enero-agosto). Procesamiento propio.",
    "oim": "Equilibrium Business, Data & Communities y Organización Internacional para las Migraciones (2025). Análisis de la contribución fiscal y económica de la migración venezolana: "
           "una aproximación regional. Informe final (D. Licheri et al.). https://lac.iom.int/sites/g/files/tmzbdl2601/files/documents/2025-12/analisis-de-la-contribucion-fiscal-y-economica-de-la-migracion-venezolana_2.pdf",
    "epm": "DANE (2025). Encuesta Pulso de la Migración (EPM), ronda VIII-2025. Archivo Nacional de Datos, catálogo 879. https://microdatos.dane.gov.co/index.php/catalog/879. Procesamiento propio.",
    "jeea": "Ibáñez, A. M., Moya, A., Ortega, M. A., Rozo, S. V. y Urbina, M. J. (2025). Life out of the shadows: impacts of regularization programs on the lives of forced migrants. "
            "Journal of the European Economic Association, 23(3), 941. DOI 10.1093/jeea/jvae044. Versión de trabajo: IZA DP 15049 (2022), https://docs.iza.org/dp15049.pdf. "
            "Las cifras se toman del resumen del artículo; no se revisó el texto completo.",
    "upc": "Ministerio de Salud y Protección Social. Resolución 2764 de 2025, por la cual se fija el valor de la Unidad de Pago por Capitación (UPC) para 2026 "
           "(subsidiado COP 1.541.706; contributivo COP 1.658.912). Consultada a través de Portafolio, https://www.portafolio.co/economia/gobierno/la-upc-para-el-2026-aumento-16-48-para-el-regimen-subsidiado-y-9-03-para-el-contributivo-485505",
    "res5477": "Ministerio de Relaciones Exteriores de Colombia. Resolución 5477 de 2022, por la cual se dictan disposiciones en materia de visas, art. 91. "
               "https://www.cancilleria.gov.co/normograma/compilacion/docs/resolucion_minrelaciones_5477_2022.htm. Verificar la versión vigente del artículo.",
    "dec1067": "Presidencia de la República. Decreto 1067 de 2015, Decreto Único Reglamentario del Sector Administrativo de Relaciones Exteriores. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=74000",
    "ley1212": "Congreso de la República. Ley 1212 de 2008, sobre las tarifas de pasaportes, visas y otros servicios consulares. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=31426. "
               "Destino del recaudo según el resumen del Gestor Normativo.",
    "mfmp": "Valora Analitik (junio de 2026). Colombia tendrá un déficit fiscal más alto en 2026, según reconoció el Gobierno (Marco Fiscal de Mediano Plazo 2026). "
            "https://www.valoraanalitik.com/colombia-tendra-un-deficit-fiscal-mas-alto-2026-reconocio-gobierno-petro/",
    "carf": "Portafolio. Tras sincerada de cuentas, el CARF advierte que el déficit fiscal bordeará el 10 % del PIB. "
            "https://www.portafolio.co/economia/gobierno/tras-sincerada-de-cuentas-el-carf-advierte-que-deficit-fiscal-bordeara-el-10-del-pib-y-deja-un-margen-reducido-502274",
    "trm": "Diario del Sur (6 de noviembre de 2026). Precio del dólar en Colombia hoy (TRM de COP 3.235,59). "
           "https://www.diariodelsur.com.co/noticias/precio-del-dolar-en-colombia-hoy-viernes-6-de-noviembre-de-2026",
}
_order = []


def cite(*keys):
    for k in keys:
        if k not in _order:
            _order.append(k)
    return "[" + ", ".join(str(_order.index(k) + 1) for k in keys) + "]"


# ------------------------------------------------------------------ cifras desde las tablas
r12 = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
asq = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
be = pd.read_csv(TAB / "t13b_punto_equilibrio_tarifa.csv")
t4 = pd.read_csv(TAB / "t4_mercado_laboral_por_grupo_anio.csv", index_col=[0, 1])
t15 = pd.read_csv(TAB / "t15_emprendimiento_venezolanos_vs_colombianos_2025.csv", index_col=0)
t3 = pd.read_csv(TAB / "t3_perfil_demografico.csv", index_col=0)
TRM, N, PIB = r12["TRM_COP_por_USD"], r12["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3, r12["PIB_implicito_USD_miles_millones"] * 1e9
es = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")
rev = lambda f: N * f * TRM / 1e12
hog = lambda lab, k=1: asq[(asq.tarifa == lab) & (asq.umbral == f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar")].pct_hogares_con_venezolano.iloc[0]
conv = lambda t, tau: 100 * be[(be.horizonte == 10) & (be.conversion_con_tarifa_464 == tau) & (be.tarifa_alternativa == t)].conversion_necesaria_para_no_perder.iloc[0]
h464, h464b, h232, h56 = hog("USD 464 (56+408) vigente"), hog("USD 464 (56+408) vigente", 2), hog("mitad (USD 232)"), hog("solo estudio USD 56 (se elimina la visa)")
cv = pd.read_csv(TAB / "t17_curva_precio_recaudo.csv")
_S = r12["beneficio_fiscal_anual_B_USD_por_persona"] * 5
_at = lambda arr, f, F: float(np.interp(f, F, arr))


def modelo(theta):
    c = cv[cv.theta_meses_de_ingreso == theta].sort_values("tarifa_USD").reset_index(drop=True)
    F = c.tarifa_USD.to_numpy().astype(float); raw = c.conversion.to_numpy()
    tau = pd.Series(raw).rolling(5, center=True, min_periods=1).mean().to_numpy(); tau[0] = raw[0]
    rec = N * tau * F / 1e6; tot = rec + N * tau * _S / 1e6
    return F, tau, rec, tot


_F, _tau, _rec, _tot = modelo(2)
M = {P: dict(conv=100 * _at(_tau, P, _F), rec=_at(_rec, P, _F), tot=_at(_tot, P, _F)) for P in (464, 232, 56, 0)}
F_REC = float(_F[int(_rec.argmax())])
GAIN0 = 100 * (M[0]["tot"] / M[464]["tot"] - 1)
S1, S3 = modelo(1), modelo(3)
TH = {th: dict(conv=100 * _at(m[1], 464, m[0]), tot464=_at(m[3], 464, m[0]), tot0=_at(m[3], 0, m[0])) for th, m in ((1, S1), (3, S3))}
UMBRAL5 = 100 * 0.85 / ((_S + 464) / _S)            # conversion maxima con tarifa vigente para que la gratuidad compense (derrame a 5 anios)
UMBRAL10 = 100 * 0.85 / ((2 * _S + 464) / (2 * _S))  # idem, derrame a 10 anios
COP_REC464 = M[464]["rec"] * TRM / 1e6

# ------------------------------------------------------------------ documento
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(0.9); sec.top_margin = Inches(0.75); sec.bottom_margin = Inches(0.75)
st = doc.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(10); st.font.color.rgb = INK
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.paragraph_format.space_after = Pt(5); st.paragraph_format.space_before = Pt(0); st.paragraph_format.line_spacing = 1.07
for name, size in (("Heading 1", 11.5), ("Heading 2", 10.5)):
    h = doc.styles[name]; h.font.name = FONT; h.font.size = Pt(size); h.font.bold = True; h.font.italic = False; h.font.color.rgb = INK
    h.element.rPr.rFonts.set(qn("w:ascii"), FONT); h.element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
    for at in [k for k in h.element.rPr.rFonts.attrib if "Theme" in k]:
        del h.element.rPr.rFonts.attrib[at]
    h.element.rPr.rFonts.set(qn("w:cs"), FONT)
    h.paragraph_format.space_before = Pt(7); h.paragraph_format.space_after = Pt(3); h.paragraph_format.keep_with_next = True


def runs(p, text, size=None, color=None, italic=False, bold=False):
    text = text.replace(" %", NB + "%")
    parts = text.split("**")
    for i, t in enumerate(parts):
        if not t: continue
        r = p.add_run(t); r.font.name = FONT; r.bold = bold or (i % 2 == 1); r.italic = italic
        if size: r.font.size = Pt(size)
        if color is not None: r.font.color.rgb = color


def para(text, size=None, color=None, italic=False, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=None, before=None, keep=False, indent=None):
    p = doc.add_paragraph(); runs(p, text, size, color, italic, bold); p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if before is not None: p.paragraph_format.space_before = Pt(before)
    if keep: p.paragraph_format.keep_with_next = True
    if indent is not None: p.paragraph_format.left_indent = Inches(indent)
    return p


def heading(text):
    return doc.add_heading(text, level=1)


def rule(p, where="bottom", sz=6, color="888888"):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement(f"w:{where}")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "1"), ("w:color", color)): e.set(qn(k), v)
    b.append(e)
    pPr.insert_element_before(b, "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
                              "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
                              "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")


def caption(label, title):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
    r = p.add_run(label + ". "); r.bold = True; r.font.size = Pt(9.5); r.font.name = FONT
    runs(p, title, size=9.5)
    return p


def source(text):
    return para(text, size=8, color=GRIS, align=WD_ALIGN_PARAGRAPH.LEFT, after=6, before=1)


def figure(name, width=5.9):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(FIG / name), width=Inches(width))


def cell_border(cell, top=None, bottom=None):
    tcPr = cell._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
    for side, spec in (("top", top), ("left", None), ("bottom", bottom), ("right", None)):
        e = OxmlElement(f"w:{side}")
        if spec: e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(spec)); e.set(qn("w:color"), "222222")
        else: e.set(qn("w:val"), "nil")
        b.append(e)
    tcPr.insert_element_before(b, "w:shd", "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")
    m = OxmlElement("w:tcMar")
    for side, v in (("top", 35), ("left", 70), ("bottom", 35), ("right", 70)):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    tcPr.insert_element_before(m, "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")


def table(rows, widths, size=9, first_left=True):
    t = doc.add_table(rows=len(rows), cols=len(widths)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j]); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            pp = c.paragraphs[0]; pp.paragraph_format.space_after = Pt(0); pp.paragraph_format.keep_with_next = i < len(rows) - 1
            runs(pp, v, size=size, bold=(i == 0))
            pp.alignment = WD_ALIGN_PARAGRAPH.LEFT if (j == 0 and first_left) else WD_ALIGN_PARAGRAPH.CENTER
            cell_border(c, top=12 if i == 0 else None, bottom=12 if i == len(rows) - 1 else (6 if i == 0 else None))
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:cantSplit"))
    return t


# ------------------------------------------------------------------ encabezado
para("NOTA TÉCNICA DE POLÍTICA · 13 de noviembre de 2026", size=8.5, color=GRIS, align=WD_ALIGN_PARAGRAPH.LEFT, after=2)
p = para("Gratuidad de la Visa R para titulares del Permiso por Protección Temporal: evidencia para eliminar la tarifa", size=15, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, after=4)
rule(p, "bottom", 8, "222222")
para("Resumen", bold=True, size=10.5, align=WD_ALIGN_PARAGRAPH.LEFT, after=1, before=4, keep=True)
para(f"Los migrantes venezolanos con Permiso por Protección Temporal (PPT) deberán convertirlo en una visa antes del 28 de mayo de 2031. La Visa R de residente por tiempo acumulado cuesta hoy "
     f"USD 464 por persona, entre estudio y expedición {cite('costos')}. Esta nota sostiene que la tarifa debe ser cero. La tarifa recauda poco en términos fiscales (como máximo {es(100*N*464/PIB, 2)} % del PIB, una sola vez), "
     f"equivale a más de un mes de ingreso laboral para {h464:.0f} % de los hogares con venezolanos y coincide con una concentración de trámites en 2027 y 2028. "
     f"Con una curva de demanda ilustrativa, la gratuidad eleva la conversión de {M[464]['conv']:.0f} % a {M[0]['conv']:.0f} %, que es el máximo posible, y aumenta {GAIN0:.0f} % el valor total (recaudo más derrame), "
     f"a cambio de que la Cancillería deje de percibir unos USD {M[464]['rec']:.0f} millones (COP {es(COP_REC464, 2)} billones). Se recomienda fijar la tarifa en cero, compensar a la Cancillería y escalonar los trámites. "
     f"Las cifras son asociaciones y escenarios con supuestos explícitos, no efectos causales.", size=10)

# ------------------------------------------------------------------ 1
heading("1. Población y aporte económico")
para(f"Según la GEIH, en 2025 residían en Colombia 1,76 millones de venezolanos sin nacionalidad colombiana (2,1 millones de nacidos en Venezuela) {cite('geih')}. "
     f"El 83 % declara que piensa quedarse y la mediana de residencia es de seis años. Su ingreso laboral suma cerca de COP 13,8 billones al año y el estudio de Equilibrium y la OIM estima su aporte fiscal en "
     f"COP 1,5 billones, equivalente a 1,9 % del recaudo de personas naturales {cite('oim')}. Una parte importante trabaja por cuenta propia, en proporción similar a la de los colombianos, "
     f"pero con negocios menos formales (Cuadro 1).")
caption("Cuadro 1", "Venezolanos y colombianos: indicadores del mercado laboral y la seguridad social, 2025")
v = lambda g, c: t4.loc[(g, 2025), c]
rows = [["Indicador", "Venezolanos", "Colombianos"],
        ["Ocupados en empleo informal (%)", es(v("ven_ext", "informalidad_pct")), es(v("col", "informalidad_pct"))],
        ["Ocupados que cotizan a pensión (%)", es(v("ven_ext", "cotiza_pension_pct")), es(v("col", "cotiza_pension_pct"))],
        ["Ingreso laboral mediano (salarios mínimos)", es(v("ven_ext", "ingreso_mediano_smmlv"), 2), es(v("col", "ingreso_mediano_smmlv"), 2)],
        ["Afiliados a salud (%)", es(v("ven_ext", "afiliado_salud_pct")), es(v("col", "afiliado_salud_pct"))],
        ["Negocios independientes registrados en Cámara de Comercio (%)", es(float(t15.loc["pct_indep_negocio_registrado_camara", "ven"])), es(float(t15.loc["pct_indep_negocio_registrado_camara", "col"]))]]
table(rows, [4.5, 1.05, 1.05])
source("Fuente: GEIH-DANE 2025, cálculos propios. Venezolanos: nacidos en Venezuela sin nacionalidad colombiana.")

# ------------------------------------------------------------------ 2
heading("2. Efectos de la regularización")
para(f"De acuerdo con la EPM, 65,6 % de los venezolanos encuestados tiene PPT {cite('epm')}. Quienes lo tienen presentan mayor afiliación a salud (91 % frente a 18 %), más cuentas en entidades financieras "
     f"(55 % frente a 11 %) y más contratos escritos entre los ocupados (20 % frente a 4 %) (Gráfico 1). Al controlar por sexo, edad, año de llegada, actividad previa en Venezuela, forma de entrada y contactos en Colombia, "
     f"las diferencias son de 66, 38 y 16 puntos porcentuales, y la probabilidad de no poder acceder a salud cuando se necesita es 37 puntos menor. No se observan diferencias claras en empleo, horas trabajadas, seguridad alimentaria ni remesas. "
     f"En la GEIH, la afiliación a salud de los venezolanos pasó de 31 % en 2022 a 66 % en 2026, pero es de 26 % entre quienes llegaron desde 2023 (Gráfico 2). "
     f"Para el Permiso Especial de Permanencia, Ibáñez et al. reportan aumentos de cerca de 10 puntos en el empleo formal, 22 % en el ingreso laboral y 48 % en el consumo per cápita {cite('jeea')}.")
caption("Gráfico 1", "Condiciones de acceso a servicios formales según tenencia de PPT")
figure("gr1_con_vs_sin_ppt.png", 4.2)
source("Fuente: EPM VIII-2025 (DANE), cálculos propios. Diferencias ajustadas: +66, +38, +16, +10 y −37 puntos. *De quienes necesitaron atención. Asociación, no causalidad.")
caption("Gráfico 2", "Afiliación a salud de los venezolanos")
figure("gr2_afiliacion_salud.png")
source("Fuente: GEIH-DANE 2022-2026, cálculos propios. *2026: enero-agosto. Venezolanos sin nacionalidad colombiana.")
para(f"Regularizar también tiene un costo: si el PPT cubriera a todos los titulares, el gasto neto adicional en salud sería de entre COP 0,4 y 0,5 billones al año, según una estimación propia basada en la UPC {cite('upc')}. "
     f"La tarifa no compensa ese gasto ni lo evita. El argumento para eliminarla se refiere, entonces, a conservar los avances de inclusión una vez venza el PPT.")

# ------------------------------------------------------------------ 3
heading("3. Ingresos por nivel educativo")
para(f"La GEIH no pregunta por el PPT y la EPM no registra ingresos, de modo que no es posible comparar directamente el ingreso de quienes tienen PPT con el de quienes no. Como aproximación se usa la afiliación a salud, "
     f"que en la EPM alcanza 91 % entre quienes tienen PPT y 18 % entre quienes no lo tienen {cite('epm')}. La medida es la mediana del ingreso laboral mensual de los ocupados de 18 años o más, en salarios mínimos de cada año.")
para("La mediana de los venezolanos es de 0,91 salarios mínimos, frente a 1,00 de los colombianos; entre los venezolanos es de 0,96 para los afiliados y de 0,86 para los no afiliados (Gráfico 3). "
     "El ingreso de los venezolanos varía poco con la educación: va de 0,80 con primaria o menos a 1,02 con educación universitaria o más, mientras que el de los colombianos pasa de 0,57 a 2,00. "
     "Con educación hasta secundaria la mediana de los venezolanos es similar o superior a la de los colombianos; con educación media o más es inferior, y con educación universitaria es la mitad. "
     "El patrón se mantiene en las zonas urbanas. Es consistente con una pérdida de valor de las calificaciones, aunque la GEIH no permite distinguir sus causas (homologación de títulos, tipo de ocupación o informalidad). "
     "Además, 12 % de los ocupados venezolanos tiene educación universitaria o más, frente a 22 % de los colombianos.")
caption("Gráfico 3", "Ingreso laboral mensual mediano por nivel educativo")
figure("gr6_ingreso_educacion.png", 5.4)
source("Fuente: GEIH-DANE 2025-2026 (2026: enero-agosto), cálculos propios. Ocupados de 18 años o más con ingreso positivo; salarios mínimos de cada año; entre 224 y 13.492 observaciones por grupo. "
       "En zonas urbanas, medianas de colombianos / venezolanos: primaria 0,67 / 0,80; secundaria 0,81 / 0,84; media 1,00 / 0,91; técnica o tecnológica 1,12 / 1,00; universitaria 2,00 / 1,03. "
       "La afiliación a salud es un indicador imperfecto de regularización.")
para("Los venezolanos afiliados ganan por hora cerca de 10 % más que los no afiliados (intervalo de confianza de 95 %: 7 % a 14 %), incluso al controlar por educación, edad, sexo, zona, departamento y año de llegada. "
     "Es un orden de magnitud y no un efecto del PPT: el indicador clasifica mal a una parte de las personas (18 % de quienes no tienen PPT está afiliado), lo que tiende a reducir la diferencia estimada, "
     "y la afiliación puede reflejar rasgos no observados, lo que podría aumentarla. No es comparable con el aumento de 22 % que reportan Ibáñez et al. para el PEP " + cite('jeea') + ".")

heading("4. La tarifa y su calendario")
para(f"La tarifa vigente es de USD 56 por el estudio y USD 408 por la expedición de la visa; el valor depende de la categoría {cite('costos')}. Los requisitos son cinco años como titular de PEP o PPT y un PPT vigente "
     f"{cite('res5477')}. Las tarifas se fijan por resolución del Ministerio de Relaciones Exteriores {cite('dec1067')} y su recaudo se destina al Fondo Rotatorio de la entidad {cite('ley1212')}. "
     f"Con unos 1,15 millones de titulares (estimación a partir de la GEIH y la EPM), si todos pagaran el recaudo sería de unos USD {N*464/1e6:.0f} millones (COP {es(rev(464))} billones a una TRM de COP 3.235 {cite('trm')}), "
     f"cerca de {es(100*N*464/PIB, 2)} % del PIB, una sola vez y repartido hasta 2031. El déficit fiscal proyectado para 2026 es de 5,3 % del PIB {cite('mfmp')}, y el Comité Autónomo de la Regla Fiscal anticipa "
     f"cerca de 10 % en 2027 {cite('carf')}. El recaudo máximo equivale, además, a un año del aporte fiscal estimado en la sección 1. Con la demanda ilustrativa de la sección 5, el recaudo esperado con la tarifa vigente sería de unos USD {M[464]['rec']:.0f} millones "
     f"(COP {es(COP_REC464, 2)} billones), porque solo convertiría una parte de los titulares.")
para(f"Con cinco años de PPT, 29 % de los titulares será elegible en 2026, 81 % en 2027 y 96 % en 2028 (Gráfico 4a). Para {h464:.0f} % de los hogares con venezolanos la tarifa equivale a más de un mes de su ingreso laboral y "
     f"para {h464b:.0f} %, a más de dos meses (Gráfico 4b).")
caption("Gráfico 4", "Calendario de elegibilidad y asequibilidad de la tarifa")
figure("gr34_calendario_asequibilidad.png")
source("Fuente: EPM VIII-2025 y GEIH 2026 (enero-agosto), cálculos propios. a) Año de obtención del PPT más cinco años; no cuenta el tiempo con PEP, por lo que subestima; entre paréntesis, porcentaje acumulado. "
       "b) Todos los miembros venezolanos del hogar pagan la tarifa por persona; TRM de COP 3.235.")

# ------------------------------------------------------------------ 4
heading("5. Comparación de opciones")
para(f"El precio que maximiza el recaudo no coincide con el que maximiza el beneficio total. Si la conversión decrece con el precio (Gráfico 5a), el ingreso de la Cancillería alcanza su máximo cerca de "
     f"USD {F_REC:.0f} por persona, pero a USD 464 solo convierte {M[464]['conv']:.0f} % de los titulares. Cada persona que convierte genera un derrame en acceso a salud, aportes y formalización, "
     f"que se aproxima con USD 980 en cinco años a partir de la literatura. Con ese derrame, el valor total (recaudo más derrame) es de USD {M[464]['tot']:.0f} millones con la tarifa vigente y de USD {M[0]['tot']:.0f} millones "
     f"sin costo, un aumento de {GAIN0:.0f} %, con la conversión en {M[0]['conv']:.0f} % (Gráfico 5b). Las tarifas intermedias dan un valor total similar (USD {M[232]['tot']:.0f} millones con USD 232), "
     f"pero dejan sin convertir a una parte de los titulares y obligan a la Cancillería a cobrar, verificar pagos y administrar excepciones. El Cuadro 2 compara las opciones.")
caption("Cuadro 2", "Opciones de tarifa (demanda ilustrativa)")
rows = [["Opción", "Tarifa (USD)", "Conversión (%)", "Recaudo esperado (millones de USD)", "Valor total (millones de USD)", "Hogares con tarifa > 1 mes de ingreso (%)"],
        ["Tarifa vigente", "464", f"{M[464]['conv']:.0f}", f"{M[464]['rec']:.0f}", f"{M[464]['tot']:.0f}", f"{h464:.0f}"],
        ["Reducción a la mitad", "232", f"{M[232]['conv']:.0f}", f"{M[232]['rec']:.0f}", f"{M[232]['tot']:.0f}", f"{h232:.0f}"],
        ["Solo estudio", "56", f"{M[56]['conv']:.0f}", f"{M[56]['rec']:.0f}", f"{M[56]['tot']:.0f}", f"{h56:.0f}"],
        ["**Sin costo**", "**0**", f"**{M[0]['conv']:.0f}**", "**0**", f"**{M[0]['tot']:.0f}**", "**0**"]]
table(rows, [1.35, 0.7, 0.85, 1.25, 1.1, 1.35], size=8.5)
source(f"Fuente: cálculos propios. Recaudo esperado = titulares × conversión × tarifa; valor total = recaudo + derrame (USD 980 por persona que convierte). "
       f"La gratuidad supera a la tarifa vigente si esta convierte menos de {UMBRAL5:.0f} % de los titulares ({UMBRAL10:.0f} % si el derrame se cuenta a diez años). La conversión máxima es de 85 %, proporción que piensa quedarse.")
caption("Gráfico 5", "Demanda, ingreso por la tarifa y valor total (escenario ilustrativo)")
figure("gr5_demanda_recaudo_derrame.png")
source("Fuente: cálculos propios con GEIH 2026 y EPM. En a), el rectángulo es el ingreso por la tarifa vigente, en millones de USD; el punto en P = 0 es la conversión máxima. La demanda no está medida; ver supuestos en el anexo.")

# ------------------------------------------------------------------ 6
heading("6. Recomendación y limitaciones")
para(f"Se recomienda: (a) fijar en cero la tarifa de estudio y expedición de la Visa R para los titulares de PEP o PPT que cumplan los requisitos; (b) compensar a la Cancillería, con una transferencia del presupuesto, el recaudo "
     f"que dejaría de percibir (hasta USD {M[464]['rec']:.0f} millones, COP {es(COP_REC464, 2)} billones, repartidos hasta 2031 según el escenario ilustrativo) y financiar la capacidad para procesar cerca de un millón de solicitudes; "
     f"(c) escalonar los trámites según el año de elegibilidad y evaluar la ampliación del plazo del PPT; y (d) expedir la resolución antes de 2027 y medir la conversión durante el primer año.")
para(f"Limitaciones. La demanda de la visa no está medida y la curva del Gráfico 5 es ilustrativa. En el modelo, el valor total con gratuidad (USD {M[0]['tot']:.0f} millones) es casi igual al de una tarifa de USD 232 "
     f"(USD {M[232]['tot']:.0f} millones); la preferencia por la gratuidad se apoya en la conversión más alta, en la ausencia de cobros, verificaciones de pago y focalización, y en el riesgo de que quien no pueda pagar pierda su estatus en 2031. "
     f"Es una decisión de política y no un resultado del modelo. Si los hogares pagaran hasta tres meses de ingreso, la tarifa vigente convertiría {TH[3]['conv']:.0f} % y su valor total (USD {TH[3]['tot464']:.0f} millones) superaría ligeramente al de la gratuidad. "
     f"Los resultados dependen de que el derrame sea positivo; si cada persona regularizada implicara un costo neto de salud sin beneficios compensatorios, no habría razón fiscal para reducir la tarifa. "
     f"No se estimó el costo de procesar las solicitudes sin ingreso por tarifa. No se verificó la tarifa de los beneficiarios (menores), el impuesto de timbre ni el texto vigente del artículo 91 de la resolución citada. "
     f"El número de titulares proviene de la GEIH y puede diferir del dato oficial. Las estimaciones de Ibáñez et al. se tomaron del resumen del artículo.")

# ------------------------------------------------------------------ anexo
heading("Anexo. Supuestos de los escenarios")
for t in [f"Ingreso por la tarifa: titulares × tarifa × TRM (COP {TRM:,.0f} por USD).".replace(",", "."),
          "PIB: USD 353 mil millones, implícito en la relación entre el aporte de USD 529 millones y 0,15 % del PIB reportada por Equilibrium y la OIM.",
          f"Conversión: 85 % (proporción que desea quedarse) por la fracción de hogares cuya tarifa no supera dos meses de ingreso laboral (GEIH 2026). Con un mes, la conversión con la tarifa vigente es de {TH[1]['conv']:.0f} % y el valor total de USD {TH[1]['tot464']:.0f} millones; con tres meses, de {TH[3]['conv']:.0f} % y USD {TH[3]['tot464']:.0f} millones; sin costo, el valor total es de USD {M[0]['tot']:.0f} millones en los tres casos.",
          "Derrame: USD 196 por persona-año durante cinco años (reducción de USD 446 anuales en el costo neto del hogar, repartida entre 2,3 venezolanos por hogar).",
          "Costo de salud (cobertura total del PPT): UPC de 2025 de COP 1,32 millones (subsidiado) y 1,52 millones (contributivo), IVA efectivo de 5 % (3 % a 7 %), ahorro y remesas de 10 % del ingreso cada uno.",
          "Elegibilidad: año de obtención del PPT (EPM) más cinco años."]:
    p = para(t, size=9.5, after=1.5, indent=0.0)
    p.paragraph_format.left_indent = Inches(0.25); p.paragraph_format.first_line_indent = Inches(-0.18)
    p.runs[0].text = "– " + p.runs[0].text


# ------------------------------------------------------------------ referencias
heading("Referencias")
for i, k in enumerate(_order, 1):
    p = para(f"[{i}] {REFS[k]}", size=8, align=WD_ALIGN_PARAGRAPH.LEFT, after=2)
    p.paragraph_format.left_indent = Inches(0.3); p.paragraph_format.first_line_indent = Inches(-0.3)

# ------------------------------------------------------------------ pie de pagina
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = fp.add_run(); run.font.size = Pt(9); run.font.name = FONT
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tag:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
    run._r.append(e)
for z in doc.settings.element.iter(qn("w:zoom")):
    z.set(qn("w:percent"), "100")
doc.save(OUT)
print("guardado", OUT, "| referencias:", len(_order))
