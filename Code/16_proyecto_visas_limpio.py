"""Visa-R / 16: version limpia (v2) del documento 'Proyecto Visas R Cancillería Colombia' (la matriz de comentarios está en 16b, de uso interno).
Entradas: borrador del equipo (datos oficiales de PPT y visas R, suministrados por el equipo), trabajo propio (GEIH, EPM, modelo de demanda) y fuentes verificadas.
Salidas: Docs/20261113 Proyecto Visas R Cancillería Colombia - versión limpia.docx"""
from pathlib import Path
import numpy as np
import pandas as pd
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor

ROOT = Path(__file__).resolve().parents[1]
FIG, TAB, DOCS = ROOT / "Outputs" / "Figures", ROOT / "Outputs" / "tables", ROOT / "Docs"
OUT = DOCS / "20261113 Proyecto Visas R Cancillería Colombia - versión limpia.docx"
OUT_M = DOCS / "20261113 Resolución de comentarios.docx"
FONT, INK, GRIS = "Times New Roman", RGBColor(0x1A, 0x1A, 0x1A), RGBColor(0x55, 0x55, 0x55)
NB = " "

# ------------------------------------------------------------------ datos del equipo (borrador) y propios
N_VEN, N_OFF, N_VISAS = 2_856_029, 1_973_253, 6_148
N_ENTR, N_EXP22 = 2_320_356, 1_448_668
VISAS = {"2024": 1_248, "2025": 3_307, "2026": 1_593}
FEE, FEE_STUDY, FEE_VISA = 464, 56, 408
TRM, SMMLV_2026 = 3235.0, 1_750_905
f_ = lambda x, d=0: f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")          # 1.234,5
pct = lambda x, d=0: f"{x:.{d}f}".replace(".", ",")
r12 = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
N_GEIH = r12["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3
PIB = r12["PIB_implicito_USD_miles_millones"] * 1e9
S = r12["beneficio_fiscal_anual_B_USD_por_persona"] * 5
SC = N_OFF / N_GEIH
asq = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
t4 = pd.read_csv(TAB / "t4_mercado_laboral_por_grupo_anio.csv", index_col=[0, 1])
t12b = pd.read_csv(TAB / "t12b_elegibilidad_por_anio.csv")
t19 = pd.read_csv(TAB / "t19_hogares_con_menores.csv", index_col=0)["valor"]
t19b = pd.read_csv(TAB / "t19b_tarifa_vs_ingreso_individual.csv")
t15 = pd.read_csv(TAB / "t15_emprendimiento_venezolanos_vs_colombianos_2025.csv", index_col=0)
cv = pd.read_csv(TAB / "t17_curva_precio_recaudo.csv")
hog = lambda lab, k=1: asq[(asq.tarifa == lab) & (asq.umbral == f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar")].pct_hogares_con_venezolano.iloc[0]
t20 = pd.read_csv(TAB / "t20_peso_tarifa_persona.csv").set_index("educacion"); t20b = pd.read_csv(TAB / "t20b_peso_tarifa_hogar.csv").set_index("grupo")
H464, H464b, H232, H56 = hog("USD 464 (56+408) vigente"), hog("USD 464 (56+408) vigente", 2), hog("mitad (USD 232)"), hog("solo estudio USD 56 (se elimina la visa)")


def modelo(theta):
    c = cv[cv.theta_meses_de_ingreso == theta].sort_values("tarifa_USD").reset_index(drop=True)
    F = c.tarifa_USD.to_numpy().astype(float); raw = c.conversion.to_numpy()
    tau = pd.Series(raw).rolling(5, center=True, min_periods=1).mean().to_numpy(); tau[0] = raw[0]
    out = {}
    for P in (464, 232, 0):
        t = float(np.interp(P, F, tau)); out[P] = dict(conv=100 * t, rec=N_OFF * t * P / 1e6, tot=N_OFF * t * (P + S) / 1e6)
    return out


M = {th: modelo(th) for th in (1, 2, 3)}; M2 = M[2]
GAIN0 = 100 * (M2[0]["tot"] / M2[464]["tot"] - 1)
UMBRAL5 = 100 * 0.85 / ((S + 464) / S); UMBRAL10 = 100 * 0.85 / ((2 * S + 464) / (2 * S))
REV_MAX_USD, REV_HIST = N_OFF * FEE, N_VISAS * FEE
acum = t12b.pct_titulares_con_5_anios_de_PPT.to_numpy() / 100
ELEG = {2026: acum[0] * N_OFF, 2027: (acum[1] - acum[0]) * N_OFF, 2028: (acum[2] - acum[1]) * N_OFF}
PROY = round(1593 * 365 / 282)                                   # 9 de octubre = dia 282 del anio

# ------------------------------------------------------------------ referencias (numeradas por orden de primera cita)
REFS = {
    "migracion": "Migración Colombia. Venezolanos en Colombia (2.856.029) y PPT autorizados (1.973.253), julio de 2024. Cifras suministradas al equipo; fuente primaria por verificar.",
    "cancilleria_visas": "Ministerio de Relaciones Exteriores. Visas R registradas bajo la actividad ETPV, 2024 al 9 de octubre de 2026 (6.148). Cifras suministradas al equipo; fuente primaria por verificar.",
    "mig2026": "Migración Colombia (julio de 2026). Comunicado sobre el ETPV: 2.320.356 PPT entregados desde la creación del mecanismo y 1.448.668 expedidos desde agosto de 2022; cerca de 1,5 millones de venezolanos regularizados desde agosto de 2022. "
               "Consultado a través de La FM, https://www.lafm.com.co/sociedad/migracion-colombia-venezolanos-permisos-temporales-405599 (la fecha del comunicado, 22 de julio de 2026, se infiere de la publicación). Fuente primaria por verificar.",
    "elnacional": "El Nacional (7 de septiembre de 2026). Más de 150.000 venezolanos están en riesgo de quedar como ilegales en Colombia por no retirar el Permiso por Protección Temporal (informa sobre un llamado de Migración Colombia). "
                  "https://www.elnacional.com/2026/09/150-000-venezolanos-en-riesgo-de-quedar-ilegales-en-colombia/",
    "res971": "Migración Colombia. Resolución 971 de 2021, por la cual se reglamenta el ETPV (vigencia del PPT hasta el 30 de mayo de 2031, no prorrogable salvo decisión del Gobierno), según el resumen de las fuentes consultadas. "
              "https://www.cancilleria.gov.co/sites/default/files/Normograma/docs/resolucion_uaemc_0971_2021.htm. Verificar el texto.",
    "res5477": "Ministerio de Relaciones Exteriores de Colombia. Resolución 5477 de 2022, arts. 11, 12 y 91. https://www.cancilleria.gov.co/normograma/compilacion/docs/resolucion_minrelaciones_5477_2022.htm. Verificar la versión vigente.",
    "costos": "Ministerio de Relaciones Exteriores de Colombia. Costos de trámites de visa: Residente, tiempo acumulado del Estatuto Temporal (estudio USD 56; visa USD 408). https://www.cancilleria.gov.co/atencion-y-servicio-al-ciudadano/tramites-y-servicios/visa/costos (consultado el 12 de noviembre de 2026).",
    "geih": "Departamento Administrativo Nacional de Estadística (DANE). Gran Encuesta Integrada de Hogares (GEIH), microdatos 2022-2026 (2026: enero-agosto). Procesamiento propio.",
    "epm": "DANE (2025). Encuesta Pulso de la Migración (EPM), ronda VIII-2025. Archivo Nacional de Datos, catálogo 879. https://microdatos.dane.gov.co/index.php/catalog/879. Procesamiento propio.",
    "moya": "Moya, A., Rozo, S. V. y Urbina, M. J. (2023). The fine line between nudging and nagging: increasing take-up rates through social media platforms. Policy Research Working Paper 10590, Banco Mundial. "
            "https://documents1.worldbank.org/curated/en/099056510112312194/pdf/IDU0f51680c00611904d4908d0a06b750ed004b1.pdf",
    "jeea": "Ibáñez, A. M., Moya, A., Ortega, M. A., Rozo, S. V. y Urbina, M. J. (2025). Life out of the shadows: impacts of regularization programs on the lives of forced migrants. Journal of the European Economic Association, 23(3), 941. "
            "DOI 10.1093/jeea/jvae044. Versión de trabajo: IZA DP 15049, https://docs.iza.org/dp15049.pdf. Cifras tomadas del resumen del artículo.",
    "oim": "Equilibrium Business, Data & Communities y Organización Internacional para las Migraciones (2025). Análisis de la contribución fiscal y económica de la migración venezolana: una aproximación regional (D. Licheri et al.). "
           "https://lac.iom.int/sites/g/files/tmzbdl2601/files/documents/2025-12/analisis-de-la-contribucion-fiscal-y-economica-de-la-migracion-venezolana_2.pdf",
    "bm": "Banco Mundial (2022). Colombia, notas sectoriales de política: Migración. https://documents1.worldbank.org/curated/en/099545009122237230/pdf/P17786906ffe9a02d0b98907940d5fb95f0.pdf",
    "melo": "Melo-Becerra, L. A., Otero-Cortés, A., Ramos-Forero, J. E. y Tribín-Uribe, A. M. (2020). Impacto fiscal de la migración venezolana. Documento de Trabajo sobre Economía Regional 289, Banco de la República. "
            "Cifras tomadas de [BM]; no se pudo abrir el documento original (bloqueo antibots) y debe revisarse.",
    "pnud": "Programa de las Naciones Unidas para el Desarrollo, Colombia (2024). Estimación del impacto fiscal de la inclusión socioeconómica de la población migrante venezolana. Documento de trabajo 002/2024. "
            "https://www.undp.org/sites/g/files/zskgke326/files/2024-10/undp_co_pub_costos_contribucion_inclusion_socioeconomica_migrantes_oct17_2024.pdf",
    "upc": "Ministerio de Salud y Protección Social. Resolución 2764 de 2025 (UPC 2026: subsidiado COP 1.541.706; contributivo COP 1.658.912), consultada a través de Portafolio. "
           "https://www.portafolio.co/economia/gobierno/la-upc-para-el-2026-aumento-16-48-para-el-regimen-subsidiado-y-9-03-para-el-contributivo-485505",
    "ley1212": "Congreso de la República. Ley 1212 de 2008, tarifas de pasaportes, visas y otros servicios consulares; y Presidencia de la República, Decreto 1067 de 2015 (fijación de tarifas por resolución del Ministerio). "
               "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=31426. Destino del recaudo según el resumen del Gestor Normativo.",
    "mfmp": "Valora Analitik (junio de 2026). Colombia tendrá un déficit fiscal más alto en 2026, según reconoció el Gobierno (Marco Fiscal de Mediano Plazo 2026). "
            "https://www.valoraanalitik.com/colombia-tendra-un-deficit-fiscal-mas-alto-2026-reconocio-gobierno-petro/",
}
_order = []


def cite(*keys):
    for k in keys:
        if k not in _order: _order.append(k)
    return "[" + ", ".join(str(_order.index(k) + 1) for k in keys) + "]"


# ------------------------------------------------------------------ utilidades de formato
def nuevo_doc(landscape=False, margins=(0.9, 0.75)):
    d = Document(); sec = d.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE; sec.page_width, sec.page_height = Inches(11), Inches(8.5)
    else:
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(margins[0]); sec.top_margin = sec.bottom_margin = Inches(margins[1])
    st = d.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(10); st.font.color.rgb = INK
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    st.paragraph_format.space_after = Pt(5); st.paragraph_format.space_before = Pt(0); st.paragraph_format.line_spacing = 1.07
    for name, size, before in (("Heading 1", 11.5, 10), ("Heading 2", 10.5, 7)):
        h = d.styles[name]; h.font.name = FONT; h.font.size = Pt(size); h.font.bold = True; h.font.italic = False; h.font.color.rgb = INK
        h.element.rPr.rFonts.set(qn("w:ascii"), FONT); h.element.rPr.rFonts.set(qn("w:hAnsi"), FONT)
        for at in [k for k in h.element.rPr.rFonts.attrib if "Theme" in k]: del h.element.rPr.rFonts.attrib[at]
        h.element.rPr.rFonts.set(qn("w:cs"), FONT)
        h.paragraph_format.space_before = Pt(before); h.paragraph_format.space_after = Pt(3); h.paragraph_format.keep_with_next = True
    for z in d.settings.element.iter(qn("w:zoom")): z.set(qn("w:percent"), "100")
    fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run(); run.font.size = Pt(9); run.font.name = FONT
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag: e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag)
        else: e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
        run._r.append(e)
    return d


def runs(p, text, size=None, color=None, italic=False, bold=False):
    parts = text.replace(" %", NB + "%").split("**")
    for i, t in enumerate(parts):
        if not t: continue
        r = p.add_run(t); r.font.name = FONT; r.bold = bold or (i % 2 == 1); r.italic = italic
        if size: r.font.size = Pt(size)
        if color is not None: r.font.color.rgb = color


def para(d, text, size=None, color=None, italic=False, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=None, before=None, keep=False, left=None, first=None):
    p = d.add_paragraph(); runs(p, text, size, color, italic, bold); p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if before is not None: p.paragraph_format.space_before = Pt(before)
    if keep: p.paragraph_format.keep_with_next = True
    if left is not None: p.paragraph_format.left_indent = Inches(left)
    if first is not None: p.paragraph_format.first_line_indent = Inches(first)
    return p


def item(d, text, n=None, size=None, after=2):
    p = para(d, (f"{n} " if n else "– ") + text, size=size, after=after, left=0.3, first=-0.2)
    return p


def rule(p, sz=8, color="222222"):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); e = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", "1"), ("w:color", color)): e.set(qn(k), v)
    b.append(e)
    pPr.insert_element_before(b, "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi",
                              "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection",
                              "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")


def caption(d, label, title):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
    r = p.add_run(label + ". "); r.bold = True; r.font.size = Pt(9.5); r.font.name = FONT
    runs(p, title, size=9.5)


def source(d, text):
    return para(d, text, size=8, color=GRIS, align=WD_ALIGN_PARAGRAPH.LEFT, after=6, before=1)


def figure(d, name, width):
    p = d.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(FIG / name), width=Inches(width))


def cell_fmt(cell, top=None, bottom=None, shade=None):
    tcPr = cell._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
    for side, spec in (("top", top), ("left", None), ("bottom", bottom), ("right", None)):
        e = OxmlElement(f"w:{side}")
        if spec: e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(spec)); e.set(qn("w:color"), "222222")
        else: e.set(qn("w:val"), "nil")
        b.append(e)
    tcPr.insert_element_before(b, "w:shd", "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")
    if shade:
        sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), shade)
        tcPr.insert_element_before(sh, "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")
    m = OxmlElement("w:tcMar")
    for side, v in (("top", 35), ("left", 70), ("bottom", 35), ("right", 70)):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    tcPr.insert_element_before(m, "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")


def tabla(d, rows, widths, size=9, center_from=1, hl_row=None, grid=False, keep_last=True, keep_rows=True):
    t = d.add_table(rows=len(rows), cols=len(widths)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j]); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            pp = c.paragraphs[0]; pp.paragraph_format.space_after = Pt(0); pp.paragraph_format.keep_with_next = keep_rows and ((i < len(rows) - 1) or keep_last)
            runs(pp, v, size=size, bold=(i == 0 or i == hl_row))
            pp.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < center_from else WD_ALIGN_PARAGRAPH.CENTER
            if grid: cell_fmt(c, top=12 if i == 0 else 4, bottom=12 if i == len(rows) - 1 else (8 if i == 0 else 4))
            else: cell_fmt(c, top=12 if i == 0 else None, bottom=12 if i == len(rows) - 1 else (6 if i == 0 else None))
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 1440)))
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:cantSplit"))
    return t


# =====================================================================================================================
# DOCUMENTO PRINCIPAL
# =====================================================================================================================
d = nuevo_doc()
para(d, "PROYECTO VISAS R · CANCILLERÍA DE COLOMBIA · versión limpia (v2), 13 de noviembre de 2026", size=8.5, color=GRIS, align=WD_ALIGN_PARAGRAPH.LEFT, after=2)
p = para(d, "Visa R para titulares del Permiso por Protección Temporal: propuesta de tarifa cero", size=15, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, after=4); rule(p)

# ------------------------------------------------------------------ 1
d.add_heading("1. Propuesta", level=1)
para(d, f"Colombia ha tenido una experiencia muy exitosa con la regularización de la población venezolana mediante el Estatuto Temporal de Protección para Migrantes Venezolanos (ETPV): a julio de 2024 se habían autorizado "
        f"{f_(N_OFF)} Permisos por Protección Temporal (PPT), 69,1 % de los {f_(N_VEN)} venezolanos en el país {cite('migracion')}, y a julio de 2026 se habían entregado {f_(N_ENTR)} PPT {cite('mig2026')}. La Visa R del artículo 91 de la Resolución 5477 de 2022 es la vía para que quienes "
        f"cumplen los requisitos avancen hacia una residencia más estable y aumenten los beneficios sociales, económicos y políticos de una presencia migratoria ordenada, segura y regular {cite('res5477')}.")
para(d, f"Sin embargo, el costo del trámite para quienes requieren realizarlo (USD {FEE}: USD {FEE_STUDY} de estudio y USD {FEE_VISA} de visa {cite('costos')}) puede convertirse en una barrera, incluso entre personas que ya cumplen los "
        f"requisitos migratorios. El costo también puede estimular prácticas ilícitas de intermediación y falsificación. Por ello se propone establecer una **tarifa de cero dólares** para los beneficiarios del artículo 91, "
        f"es decir, quienes acumulan cinco años de permanencia bajo PEP o PPT y tienen un PPT vigente.")
para(d, "La propuesta se sustenta en cuatro consideraciones: (i) consolidar la inversión pública realizada en regularización; (ii) facilitar la continuidad de las trayectorias económicas y sociales de la población regularizada; "
        "(iii) evitar barreras financieras que limiten el acceso a la residencia; y (iv) promover una gestión administrativa y fiscal más eficiente, considerando los beneficios potenciales de largo plazo frente al recaudo inmediato del trámite. "
        "La gratuidad debe evaluarse no solo por los ingresos que dejaría de percibir la administración, sino también por los costos de mantener una barrera económica y por los beneficios potenciales de ampliar el acceso a la residencia.")
para(d, "La gratuidad no se presenta como una medida humanitaria ni se afirma que aumente automáticamente la formalidad o el recaudo. Las cifras de este documento son asociaciones y escenarios con supuestos explícitos, no efectos causales.")

# ------------------------------------------------------------------ 2
d.add_heading("2. Contexto: lo que se ha logrado con el ETPV y el uso de la Visa R", level=1)
para(d, "El Cuadro 1 reúne las cifras que dan el contexto general: cuántos venezolanos hay en el país, cuántos PPT se han autorizado y entregado, y cuántas visas R se han registrado.")
caption(d, "Cuadro 1", "Contexto: venezolanos, PPT y visas R")
rows = [["Indicador", "Dato", "Corte", "Fuente"],
        ["Venezolanos en Colombia", f_(N_VEN), "jul. 2024", f"Migración Colombia {cite('migracion')}"],
        ["PPT autorizados", f_(N_OFF), "jul. 2024", f"Migración Colombia {cite('migracion')}"],
        ["PPT autorizados respecto al total de venezolanos", "69,1 %", "jul. 2024", "Cálculo propio"],
        ["PPT entregados desde la creación del mecanismo", f_(N_ENTR), "jul. 2026", f"Migración Colombia {cite('mig2026')}"],
        ["PPT expedidos desde agosto de 2022", f_(N_EXP22), "jul. 2026", f"Migración Colombia {cite('mig2026')}"],
        ["Venezolanos regularizados desde agosto de 2022", "cerca de 1,5 millones", "jul. 2026", f"Migración Colombia {cite('mig2026')}"],
        ["PPT aprobados que aún no se han retirado", "más de 150.000", "sep. 2026", f"Migración Colombia, vía prensa {cite('elnacional')}"],
        ["Visas R registradas bajo actividad ETPV", f_(N_VISAS), "9 oct. 2026", f"Cancillería {cite('cancilleria_visas')}"],
        ["Visas R respecto a PPT autorizados / entregados", f"{pct(100*N_VISAS/N_OFF,2)} % / {pct(100*N_VISAS/N_ENTR,2)} %", "", "Cálculo propio"]]
tabla(d, rows, [3.0, 1.25, 0.8, 1.55], size=8.5, center_from=1)
source(d, "Los números entre corchetes remiten a la lista de referencias. «Autorizados», «entregados» y «expedidos» son las categorías que usa Migración Colombia y no son directamente comparables. "
          "Las cifras de julio de 2024 y de visas R fueron suministradas al equipo y, como las de 2026, deben verificarse en la fuente primaria.")
para(d, f"Lo logrado se ve en la inclusión de la población regularizada. Según la GEIH, la afiliación a salud de los venezolanos pasó de 31 % en 2022 a 66 % en 2026, y en la EPM 91 % de quienes tienen PPT está afiliado {cite('geih', 'epm')} (Gráfico 1). "
        f"El avance es desigual: entre quienes llegaron desde 2023 la afiliación es de 26 %.")
caption(d, "Gráfico 1", "Afiliación a salud de los venezolanos")
figure(d, "gr2_afiliacion_salud.png", 5.0)
source(d, "Fuente: GEIH-DANE 2022-2026, cálculos propios. *2026: enero-agosto. Venezolanos sin nacionalidad colombiana.")
para(d, f"Frente a ese universo, la transición hacia la Visa R avanza a escala reducida. Entre 2024 y 2025 las visas pasaron de {f_(VISAS['2024'])} a {f_(VISAS['2025'])} (+165,0 %), un crecimiento importante sobre una base baja. "
        f"En 2026 se habían registrado {f_(VISAS['2026'])} hasta el 9 de octubre; proyectado linealmente al fin del año, el resultado sería cercano a {f_(PROY)}, una caída de {pct(100*(1-PROY/VISAS['2025']),1)} % frente a 2025. "
        f"No es un pronóstico: puede haber estacionalidad, rezagos de registro o cambios en la demanda (Gráfico 2).")
caption(d, "Gráfico 2", "Visas R registradas bajo la actividad ETPV, por año")
figure(d, "pr1_visas_por_anio.png", 4.6)
source(d, f"Fuente: Cancillería {cite('cancilleria_visas')}. La barra rayada es una proyección lineal del acumulado al 9 de octubre de 2026, no un pronóstico.")
para(d, f"La razón de 0,31 % se mide frente a todos los PPT, pero solo cumple los cinco años quien obtuvo PEP o PPT antes: con la fecha de obtención del PPT en la EPM, 29 % de los titulares será elegible en 2026, 81 % en 2027 y 96 % en 2028 "
        f"(Gráfico 4a) {cite('epm')}. Frente a unas {f_(ELEG[2026]/1e3)} mil personas elegibles en 2026, las {f_(VISAS['2026'])} solicitudes del año son menos de 0,3 %. La estimación subestima la elegibilidad, porque no cuenta el tiempo con PEP.")
para(d, "La baja demanda puede tener varias causas, una de las cuales es el costo. Otras son la información, los documentos, los tiempos, los requisitos, la falta de confianza y la baja percepción de beneficios. "
        "En la EPM, entre quienes no tienen ningún permiso, 43 % reporta dificultades con la entidad y 18 % no cumplir los requisitos; el costo no figura entre las opciones de esa pregunta. "
        "La existencia de una ruta legal no garantiza que las personas puedan o decidan completarla: la gratuidad puede eliminar la barrera económica, aunque no necesariamente resuelve las demás.")

# ------------------------------------------------------------------ 3
d.add_heading("3. Quiénes son y cuánto pesa la tarifa", level=1)
para(d, "La tarifa pesa más en Colombia sobre los hogares venezolanos que sobre los colombianos, porque su situación laboral es más frágil, aunque su ingreso mediano sea parecido (Cuadro 2).")
caption(d, "Cuadro 2", "Venezolanos y colombianos: empleo, ingreso y protección social")
rows = [["Indicador", "Venezolanos", "Colombianos", "Diferencia"],
        ["Ocupados en empleo informal (%)", "79,6", "54,8", "+24,8 pp"],
        ["Ingreso laboral mediano (salarios mínimos)", "0,91", "1,00", "−9 %"],
        ["Afiliados a salud (%)", "65,5", "97,3", "−31,8 pp"],
        ["Ocupados que cotizan a pensión (%)", "16,6", "44,3", "−27,7 pp"],
        ["Negocios independientes registrados en Cámara de Comercio (%)", "21,7", "36,3", "−14,6 pp"]]
tabla(d, rows, [3.3, 1.1, 1.1, 1.1], size=8.5, center_from=1)
source(d, f"Fuente: GEIH-DANE 2025 {cite('geih')}, cálculos propios. Venezolanos: nacidos en Venezuela sin nacionalidad colombiana. pp = puntos porcentuales.")
para(d, f"El contraste es más fuerte en la protección que en el ingreso. Los ocupados venezolanos ganan en la mediana 9 % menos que los colombianos, pero casi ocho de cada diez trabaja en la informalidad (frente a poco más de la mitad de los colombianos) y solo dos de cada tres está afiliado a salud (frente a casi todos los colombianos). "
        f"Tampoco tienen el respaldo de un empleo formal para absorber un gasto como este. A ello se suma la carga de cuidado: {pct(t19['pct_hogares_con_menor_de_18'])} % de los hogares con venezolanos tiene al menos un menor de 18 años ({pct(t19['menores_de_18_por_hogar'],1)} por hogar, en promedio) y 30 % de los venezolanos son menores de edad.")
para(d, f"La tarifa de USD {FEE} equivale a unos COP {pct(FEE*TRM/1e6,1)} millones por persona (0,86 salarios mínimos de 2026). Para el ocupado venezolano mediano son {pct(float(t20.loc['Todos','pct_ingreso_USD 464 (vigente)']))} % de su ingreso laboral mensual: {int(round(30*float(t20.loc['Todos','pct_ingreso_USD 464 (vigente)'])/100))} de los 30 días de un mes de trabajo (Gráfico 3a). "
        f"Una tarifa de USD 232 costaría {int(round(30*float(t20.loc['Todos','pct_ingreso_USD 232'])/100))} días y solo el estudio (USD 56), {int(round(30*float(t20.loc['Todos','pct_ingreso_USD 56 (estudio)'])/100))} días.")
para(d, f"El peso no baja mucho con la educación (Gráfico 5): para quienes tienen primaria o menos la tarifa supera el ingreso de un mes ({pct(float(t20.loc['Hasta primaria','pct_ingreso_USD 464 (vigente)']))} %) y, aun con educación universitaria, equivale a {pct(float(t20.loc['Universitaria o más','pct_ingreso_USD 464 (vigente)']))} %.")
para(d, f"En el hogar el peso es mayor, porque la tarifa se paga por persona. Si todos los venezolanos del hogar pagaran, la tarifa equivaldría, en la mediana de los hogares, a {pct(float(t20b.loc['Todos los hogares con venezolanos','mediana_pct_ingreso_mensual_del_hogar']))} % de su ingreso laboral mensual ({pct(float(t20b.loc['Con al menos un menor de 18','mediana_pct_ingreso_mensual_del_hogar']))} % en los hogares con menores y {pct(float(t20b.loc['Con 3 o más venezolanos','mediana_pct_ingreso_mensual_del_hogar']))} % en los de tres o más venezolanos; Gráfico 3b). "
        f"Supera el ingreso de un mes del hogar en {H464:.0f} % de los hogares y el de dos meses en {H464b:.0f} % (Gráfico 4b).")
caption(d, "Gráfico 3", "Peso de la tarifa de la Visa R sobre el ingreso laboral mensual")
figure(d, "pr4_peso_tarifa.png", 5.9)
source(d, "Fuente: GEIH 2026 (enero-agosto), cálculos propios. Ocupados venezolanos (sin nacionalidad colombiana) con ingreso laboral positivo; en los hogares, tarifa por el número de venezolanos del hogar sobre el ingreso laboral mensual total del hogar (mediana ponderada). "
          "a) Cada cuadro es un día de un mes de 30 días, redondeado al día más cercano. b) Escenario en que todos los venezolanos del hogar pagan la tarifa a la vez: costo = USD 464 × número de venezolanos del hogar; el ingreso es el ingreso laboral mensual total del hogar (100). La tarifa pesa más en los hogares con más venezolanos porque su costo crece con cada persona, mientras que el ingreso del hogar no crece en la misma proporción (hay menores, cuidadores y personas sin empleo); el último grupo incluye hogares con 3, 4 o más venezolanos. En la práctica las familias podrían pagar de forma escalonada. TRM de COP 3.235; no incluye el timbre.")
caption(d, "Gráfico 4", "Calendario de elegibilidad y asequibilidad de la tarifa")
figure(d, "pr2_calendario_asequibilidad.png", 5.9)
source(d, f"Fuente: EPM VIII-2025 y GEIH 2026 (enero-agosto), cálculos propios. a) Año de obtención del PPT más cinco años, aplicado a los {f_(N_OFF)} PPT autorizados; no cuenta el tiempo con PEP. Entre paréntesis, porcentaje acumulado. "
          "b) Se toman los hogares con al menos un venezolano. Para cada hogar, la tarifa total es USD 464 (o la tarifa indicada) por el número de venezolanos que viven en él, es decir, supone que todos pagan; se compara con el ingreso laboral mensual de todo el hogar. "
          "Las barras indican el porcentaje de hogares en que esa tarifa total supera el ingreso de un mes (azul) o de dos meses (gris). Ejemplo: un hogar con tres venezolanos y COP 3 millones de ingreso mensual debería pagar COP 4,5 millones, 1,5 meses de ingreso. Los hogares sin ingreso laboral se cuentan como superados. TRM de COP 3.235.")
caption(d, "Gráfico 5", "Ingreso laboral mensual mediano por nivel educativo")
figure(d, "pr5_ingreso_educacion.png", 5.0)
source(d, "Fuente: GEIH-DANE 2025-2026 (2026: enero-agosto), cálculos propios. Ocupados de 18 años o más con ingreso positivo; salarios mínimos de cada año. La afiliación a salud es un indicador imperfecto de regularización "
          "(en la EPM, 91 % de quienes tienen PPT está afiliado y 18 % de quienes no lo tienen).")
para(d, "El Gráfico 5 compara el ingreso mediano con la tarifa. Entre los colombianos, estudiar paga: el ingreso mediano sube de 0,57 salarios mínimos con primaria o menos a 2,00 con educación universitaria o más. "
        "Entre los venezolanos casi no cambia (de 0,80 a 1,02). Por eso los venezolanos con educación universitaria ganan 49 % menos que los colombianos con el mismo nivel, y con primaria o menos ganan más que ellos. "
        "La educación no protege a los venezolanos de que la tarifa pese sobre su ingreso.")
para(d, f"Dentro de los venezolanos, los afiliados a salud ganan por hora cerca de 10 % más que los no afiliados (intervalo de confianza de 95 %: 7 % a 14 %), incluso al controlar por educación, edad, sexo, zona, departamento y año de llegada. Es un orden de magnitud y no el efecto del PPT. "
        f"Los costos de acceso también importan cuando el trámite es gratuito: Moya, Rozo y Urbina documentan, para el registro del PPT, la falta de dinero para llegar a los puntos de registro y el costo de perder parte de la jornada de trabajo {cite('moya')}. "
        f"No evalúan la Visa R, pero muestran que el costo de acceso es una restricción real para esta población.")

# ------------------------------------------------------------------ 4
d.add_heading("4. Argumentos", level=1)
d.add_heading("4.1 Consolidar la inversión: lo que ya se logró con el PPT", level=2)
para(d, f"El PPT ya permite trabajar y acceder a servicios bajo las reglas generales; la Visa R no abre por primera vez el acceso al empleo o a la salud. La diferencia clave es la estabilidad del estatus y la perspectiva de permanencia. "
        f"Los avances de la regularización son visibles en la EPM {cite('epm')}: con PPT, 91 % de los venezolanos está afiliado a salud (18 % sin PPT), 55 % tiene cuenta financiera (11 %) y 20 % de los ocupados tiene contrato escrito (4 %) (Gráfico 6). "
        f"Controlando por sexo, edad, año de llegada y otros factores, las diferencias son de 66, 38 y 16 puntos porcentuales; no se observan diferencias claras en empleo, horas, seguridad alimentaria ni remesas.")
caption(d, "Gráfico 6", "Acceso a servicios formales según tenencia de PPT")
figure(d, "gr1_con_vs_sin_ppt.png", 4.4)
source(d, "Fuente: EPM VIII-2025 (DANE), cálculos propios. Diferencias ajustadas: +66, +38, +16, +10 y −37 puntos. *De quienes necesitaron atención. Asociación, no causalidad.")
para(d, "Esa estabilidad favorece decisiones de largo plazo: 83 % de los venezolanos dice que piensa quedarse y la mediana de residencia es de seis años (GEIH). La Visa R ofrece una vía de residencia más estable, aunque sujeta a condiciones y causales de pérdida de vigencia, "
        "lo que puede favorecer la continuidad laboral, la adquisición de activos (productivos o de vivienda), la vinculación al sistema financiero, la inversión en educación o formación técnica y la planificación familiar. También puede ampliar la confianza de los empleadores y estimular la formalización del empleo. "
        f"Estos son efectos potenciales, y hay espacio para ellos: solo 21,7 % de los negocios independientes de los venezolanos está registrado en Cámara de Comercio (36,3 % entre los colombianos) y solo 16,6 % de los ocupados cotiza a pensión (44,3 % entre los colombianos).")

d.add_heading("4.2 El recaudo inmediato debe compararse con el costo de la barrera y con el beneficio de largo plazo", level=2)
para(d, f"Con la tarifa vigente, las {f_(N_VISAS)} visas registradas habrían generado, como máximo, USD {f_(REV_HIST)} (COP {pct(REV_HIST*TRM/1e9,1)} mil millones). No es el recaudo histórico verificado: es una cota superior hipotética que supone que cada registro pagó la tarifa vigente "
        f"y no considera exenciones ni cambios de tarifa. Tampoco se conoce cuánto cuesta procesar cada solicitud. Mirando hacia adelante, si los {f_(N_OFF)} PPT autorizados pagaran la tarifa, el recaudo sería de unos USD {f_(REV_MAX_USD/1e6)} millones "
        f"(COP {pct(REV_MAX_USD*TRM/1e12,1)} billones, {pct(100*REV_MAX_USD/PIB,2)} % del PIB), una sola vez y repartido hasta 2031, en un contexto de déficit fiscal proyectado de 5,3 % del PIB para 2026 {cite('mfmp')}. "
        f"El recaudo esperado depende de cuántos titulares conviertan: con la demanda ilustrativa de la sección 6, la tarifa vigente recaudaría unos USD {M2[464]['rec']:.0f} millones y la gratuidad, ninguno.")
para(d, "La comparación correcta no es «USD 2,9 millones frente a cero», sino:")
item(d, "**Recaudo neto actual** = pagos efectivamente recibidos − costo administrativo de procesar las solicitudes.")
item(d, "**Balance de la gratuidad** = recaudo que se deja de percibir − costos adicionales de procesamiento + beneficios fiscales y económicos incrementales de las transiciones adicionales.", after=4)
para(d, "La pregunta es si el cobro actual genera un ingreso neto significativo y si ese ingreso compensa mantener una barrera que puede limitar la transición a la residencia, con costos directos e indirectos para el Estado derivados de ampliar el número de personas en situación de irregularidad migratoria.")

d.add_heading("4.3 Evitar discontinuidades documentales hacia 2031", level=2)
para(d, f"El PPT tiene vigencia hasta el 30 de mayo de 2031, no prorrogable salvo decisión del Gobierno {cite('res971')}. La Visa R permite que quienes cumplen los requisitos no dependan indefinidamente de un instrumento temporal. "
        f"Los trámites se concentrarán en 2027, cuando 81 % de los titulares cumplirá los cinco años (cerca de {pct(ELEG[2027]/1e6,2)} millones de nuevos elegibles ese año según la estimación del Gráfico 4a). "
        f"No quiere decir que todos pierdan automáticamente su estatus en 2031 ni que todos los titulares de PPT sean elegibles. El mensaje es que conviene facilitar la transición de quienes sí cumplen los requisitos, con tiempo suficiente y sin una barrera económica evitable.")

d.add_heading("4.4 La integración económica genera beneficios fiscales; la discusión es de magnitud relativa", level=2)
para(d, "La población venezolana es receptora de gasto público y, a la vez, realiza aportes fiscales y contribuciones al crecimiento. La evidencia disponible:")
item(d, f"Equilibrium y la OIM estiman una contribución fiscal de USD 529 millones (datos a 2023) y un potencial de USD 804 millones con mayor integración laboral y menos barreras de formalización {cite('oim')}.")
item(d, f"Melo-Becerra et al. (2020), citados por el Banco Mundial, estiman un IVA de facturas de hogares venezolanos de COP 500.993 millones en 2019 (0,03 % del PIB) y un impuesto de renta de COP 129.150 millones en 2018 (0,01 % del PIB) {cite('melo', 'bm')}.")
item(d, f"El Banco Mundial estima un efecto positivo en el PIB de entre 0,14 % y 0,17 % a mediano y largo plazo, y un costo de atención de entre 0,4 % y 0,5 % del PIB al año en el corto plazo {cite('bm')}.")
item(d, f"El PNUD estima contribuciones de COP 29,79 billones en 2022-2028 en un escenario moderado de inclusión, frente a costos de COP 50,42 billones {cite('pnud')}. En ese horizonte, los costos superan las contribuciones: la inclusión no se financia sola.")
item(d, f"Ibáñez et al. estiman, para quienes recibieron el Permiso Especial de Permanencia, aumentos de cerca de 10 puntos en el empleo formal, 22 % en el ingreso laboral y 48 % en el consumo per cápita {cite('jeea')}.", after=4)
para(d, f"Con datos propios, el ingreso laboral de al menos 1,76 millones de venezolanos suma cerca de COP 13,8 billones al año (GEIH 2025; la encuesta subestima la población). Estos estudios respaldan la importancia económica de la integración migratoria, pero no demuestran que la Visa R por sí sola produzca esos beneficios, "
        f"y varios muestran que el balance fiscal de corto plazo es negativo. El argumento fiscal sólido no es que la integración «se pague sola», sino que el ingreso de la tarifa es pequeño frente a esos montos y a los costos de que parte de la población no consolide su residencia.")

d.add_heading("4.5 Una tarifa cero es una medida de eficiencia y acceso, no solo un subsidio", level=2)
para(d, "La gratuidad se justifica como decisión de política pública cuando: (a) el Estado ya cuenta con la información y la infraestructura administrativa generadas por el ETPV; (b) la persona ya pasó por un proceso de identificación y regularización; "
        "(c) la residencia estable puede producir beneficios públicos de largo plazo; (d) el costo puede excluir precisamente a quienes tienen mayor vulnerabilidad económica; y (e) el ingreso neto que obtiene la entidad por la tarifa es pequeño frente al beneficio público potencial. "
        f"El esquema de tarifas de la Cancillería ya incluye categorías sin costo (por ejemplo, algunas visas de cortesía) y, según el artículo 11 de la Resolución 5477, las visas de tarifa cero siguen el mismo procedimiento de liquidación {cite('res5477', 'ley1212')}; la medida no exigiría crear un trámite nuevo (texto por confirmar).")

# ------------------------------------------------------------------ 5
d.add_heading("5. Costos de mantener la tarifa", level=1)
para(d, "**Transiciones que no se realizan.** Quien cumple los requisitos pero no puede pagar puede postergar o desistir. Esto no significa que pierda de inmediato su regularidad migratoria, porque el PPT sigue siendo válido bajo sus condiciones, "
        "sino que permanece más tiempo en un régimen temporal. El costo para el país es una transición más lenta hacia una residencia estable y la pérdida posible de beneficios de largo plazo.")
para(d, "**Exclusión por capacidad de pago.** La Visa R-ETPV se dirige a personas que ya acumularon cinco años bajo PEP o PPT. El costo introduce una barrera ajena al cumplimiento de esos requisitos: la tarifa selecciona por capacidad de pago y no por elegibilidad (sección 3).")
para(d, f"**Solicitudes que no se completan.** Según los artículos 11 y 12 de la Resolución 5477, la persona tiene diez días calendario para pagar el estudio y, una vez autorizada la visa, diez días para pagar la expedición; si no paga, la solicitud se entiende desistida {cite('res5477')}. "
        "Mantener una tarifa elevada puede generar solicitudes que no se convierten en visas expedidas, con trabajo administrativo sin culminación. Para medirlo se necesitan las cifras de solicitudes iniciadas, pagos, desistimientos y autorizaciones pendientes de pago.")
para(d, "**Costo fiscal de oportunidad.** El recaudo del trámite es un ingreso directo, pero su eliminación puede facilitar transiciones que, a largo plazo, contribuyan a mayor formalización laboral y de emprendimientos, mayor afiliación y contribución a la seguridad social, "
        "mayor consumo formal y pago de impuestos indirectos, y mayor estabilidad de los hogares. Estas cifras provienen de procesos de inclusión más amplios, no del efecto causal de pasar del PPT a la Visa R; su incremento atribuible a la Visa R debe cuantificarse.")
para(d, "**Costo institucional.** Colombia creó una ruta especial de residencia para quienes han construido una trayectoria de permanencia. Mantener una barrera elevada puede reducir su alcance efectivo y debilitar un avance que ha sido bueno: no basta con crear una vía legal de transición, es necesario que las personas elegibles puedan acceder a ella.")

# ------------------------------------------------------------------ 6
d.add_heading("6. Escenarios y cálculos", level=1)
para(d, f"Para estimar cuántas personas adicionales harían el trámite si fuera gratuito se usa una curva de demanda ilustrativa. La conversión acumulada hasta 2031 es el 85 % (proporción que desea quedarse) multiplicado por la fracción de hogares cuya tarifa no supera dos meses de su ingreso laboral (GEIH 2026), "
        f"aplicada a los {f_(N_OFF)} PPT autorizados. Cada persona que convierte genera un derrame (acceso a salud, aportes, formalización) que se aproxima con USD 980 en cinco años a partir de la literatura {cite('jeea')}. "
        f"El valor total es el recaudo más el derrame. La demanda no está medida: es un escenario, no un pronóstico.")
caption(d, "Cuadro 3", "Evaluación económica de escenarios (demanda ilustrativa, escala de PPT autorizados)")
rows = [["Variable", "Escenario 1: tarifa actual (USD 464)", "Escenario 2: tarifa reducida (USD 232)", "Escenario 3: tarifa cero"],
        ["Costo de acceso", "Alto", "Intermedio", "Nulo"],
        ["Hogares con tarifa > 1 mes de ingreso (%)", f"{H464:.0f}", f"{H232:.0f}", "0"],
        ["Conversión esperada hasta 2031 (%)", f"{M2[464]['conv']:.0f}", f"{M2[232]['conv']:.0f}", f"{M2[0]['conv']:.0f}"],
        ["Recaudo esperado (millones de USD)", f"{M2[464]['rec']:.0f}", f"{M2[232]['rec']:.0f}", "0"],
        ["Costos administrativos de procesamiento", "Por estimar", "Por estimar", "Por estimar"],
        ["Valor total: recaudo + derrame (millones de USD)", f"{f_(M2[464]['tot'])}", f"{f_(M2[232]['tot'])}", f"{f_(M2[0]['tot'])}"],
        ["Equidad de acceso", "Menor", "Intermedia", "Mayor"]]
tabla(d, rows, [2.4, 1.45, 1.45, 1.3], size=8.5, center_from=1)
source(d, f"Fuente: cálculos propios. El valor total de la gratuidad supera en {GAIN0:.0f} % al de la tarifa actual; el de la tarifa reducida es casi igual al de la gratuidad. La elección de cero frente a USD 232 se apoya en la conversión máxima, "
          "la simplicidad (sin cobros, verificación de pagos ni excepciones) y el menor riesgo de exclusión, no en una diferencia de valor en el modelo.")
caption(d, "Gráfico 7", "Demanda, ingreso por la tarifa y valor total (escenario ilustrativo)")
figure(d, "pr3_demanda_recaudo_derrame.png", 5.7)
source(d, "Fuente: cálculos propios con GEIH 2026, EPM y PPT autorizados. En a), el rectángulo es el ingreso por la tarifa vigente, en millones de USD; el punto en P = 0 es la conversión máxima.")
para(d, f"La gratuidad supera a la tarifa vigente, en valor total, si esta convierte menos de {UMBRAL5:.0f} % de los titulares ({UMBRAL10:.0f} % si el derrame se cuenta a diez años); con la demanda ilustrativa convierte {M2[464]['conv']:.0f} %. "
        f"La sensibilidad es importante: si los hogares pagaran hasta un mes de ingreso, la tarifa vigente convertiría {M[1][464]['conv']:.0f} % y su valor total sería de USD {f_(M[1][464]['tot'])} millones, frente a USD {f_(M[1][0]['tot'])} millones sin costo; "
        f"si pagaran hasta tres meses, convertiría {M[3][464]['conv']:.0f} % y su valor total (USD {f_(M[3][464]['tot'])} millones) superaría ligeramente al de la gratuidad (USD {f_(M[3][0]['tot'])} millones). "
        f"El uso observado hasta hoy (menos de 0,3 % de los elegibles) es más cercano a una demanda baja. Si el PPT no se amplía, la demanda se vuelve menos elástica cerca de 2031 y el recaudo que se deja de percibir podría acercarse a la cota de USD {f_(REV_MAX_USD/1e6)} millones. "
        f"Si regularizar implicara un costo neto de salud sin beneficios compensatorios (con cobertura total, entre COP 0,4 y 0,5 billones al año según la UPC {cite('upc')}), no habría razón fiscal para reducir la tarifa.")
d.add_heading("Información que se necesita", level=2)
rows = [["Información", "Qué permitiría demostrar", "Estado"],
        ["Solicitudes iniciadas y pagos de estudio", "Cuántas personas no completan el primer pago", "Pendiente (Cancillería)"],
        ["Visas autorizadas y pagos de expedición", "Cuántas personas no culminan el trámite tras ser aprobadas", "Pendiente (Cancillería)"],
        ["Desistimientos por falta de pago", "Cuánto abandono puede asociarse a la tarifa", "Pendiente (Cancillería)"],
        ["Recaudo efectivo por etapa", "Cuánto dinero recibe realmente el Estado", "Pendiente (Cancillería)"],
        ["Costo administrativo por solicitud", "Si el recaudo compensa los costos de procesamiento", "Pendiente (Cancillería)"],
        ["Personas elegibles por año", "Universo potencial de beneficiarios", "Estimación propia (Gráfico 4a); confirmar con Migración Colombia"],
        ["Perfil socioeconómico de solicitantes y no solicitantes", "Si el costo excluye a hogares vulnerables", "Estimación propia con GEIH y EPM; falta el perfil de solicitantes"],
        ["Tiempo de procesamiento e interoperabilidad", "Costo real de la transición para la administración", "Pendiente (Cancillería)"],
        ["Tarifa por año, exenciones y conceptos incluidos", "Refina el recaudo histórico", "No esencial para el argumento"]]
tabla(d, rows, [2.3, 2.6, 1.7], size=8.5, center_from=3, grid=False, keep_last=False)

# ------------------------------------------------------------------ 7
d.add_heading("7. Conclusión", level=1)
para(d, "1. **La gratuidad consolida una inversión pública.** Facilita que la población ya regularizada avance hacia una residencia más estable y da continuidad a la estrategia de integración.", after=2, left=0.3, first=-0.2)
para(d, "2. **La tarifa puede ser una barrera de acceso.** No distingue entre quienes cumplen los requisitos y quienes tienen mayor capacidad de pago: equivale a 28 de los 30 días de trabajo de un ocupado venezolano mediano y supera un mes de ingreso del hogar en dos de cada tres hogares con venezolanos.", after=2, left=0.3, first=-0.2)
para(d, "3. **La inclusión puede generar beneficios económicos y fiscales.** La evidencia sobre regularización muestra mejoras en ingresos, consumo y acceso a servicios; una transición más accesible puede ayudar a consolidarlas, aunque su efecto incremental debe medirse. El balance fiscal de corto plazo de la inclusión es negativo en varios estudios.", after=2, left=0.3, first=-0.2)
para(d, "4. **Mantener el cobro también tiene costos:** exclusión, desistimientos, menor aprovechamiento de la ruta de residencia y retrasos en la consolidación de la política migratoria.", after=5, left=0.3, first=-0.2)
para(d, f"La eliminación de la tarifa de la Visa R para los beneficiarios del artículo 91 de la Resolución 5477 de 2022 debe entenderse como una medida de eficiencia económica e institucional. Al reducir una barrera financiera para una población que ya avanzó en su regularización, Colombia puede consolidar su inversión pública, "
        f"promover una transición ordenada hacia la residencia y fortalecer las condiciones para la integración económica y fiscal de largo plazo. El recaudo inmediato asociado al trámite debe evaluarse frente a los costos de exclusión y a los beneficios potenciales de una mayor cobertura de la ruta de residencia. "
        f"Con la demanda ilustrativa, la gratuidad eleva la conversión de {M2[464]['conv']:.0f} % a {M2[0]['conv']:.0f} % y el valor total en {GAIN0:.0f} %, a cambio de que la Cancillería deje de percibir unos USD {M2[464]['rec']:.0f} millones; se recomienda compensar ese recaudo con una transferencia presupuestal y medir la conversión real durante el primer año.")

# ------------------------------------------------------------------ referencias y anexo
d.add_heading("Referencias", level=1)
for i, k in enumerate(_order, 1):
    p = para(d, f"[{i}] {REFS[k]}", size=8, align=WD_ALIGN_PARAGRAPH.LEFT, after=2, left=0.3, first=-0.3)
d.add_heading("Anexo. Supuestos de los escenarios", level=1)
for t in [f"Escala: {f_(N_OFF)} PPT autorizados (julio de 2024); con los {f_(N_ENTR)} PPT entregados a julio de 2026 la escala sería {pct(100*(N_ENTR/N_OFF-1))} % mayor. A escala de la GEIH (≈ {f_(N_GEIH/1e6,2)} millones de titulares estimados) las cifras de recaudo y valor total son {pct(100*(1-1/SC))} % menores; las proporciones no cambian.",
          f"Tarifa vigente: USD {FEE} (USD {FEE_STUDY} de estudio y USD {FEE_VISA} de visa, categoría de residente por tiempo acumulado del Estatuto Temporal) y TRM de COP {f_(TRM)} por USD; los borradores previos usaban USD 450 y USD 454.",
          "PIB: USD 353 mil millones, implícito en la relación entre el aporte de USD 529 millones y 0,15 % del PIB reportada por Equilibrium y la OIM.",
          "Conversión: 85 % por la fracción de hogares cuya tarifa no supera dos meses de ingreso laboral (GEIH 2026, ponderada por persona). Con un mes y con tres meses el valor total con la tarifa vigente cambia como se indica en la sección 6.",
          "Derrame: USD 196 por persona-año durante cinco años (reducción de USD 446 anuales del costo neto del hogar, repartida entre 2,3 venezolanos por hogar), a partir del resumen de Ibáñez et al.",
          "Elegibilidad: año de obtención del PPT (EPM) más cinco años; no considera el tiempo previo con PEP, por lo que subestima.",
          "Proyección lineal de 2026: 1.593 × 365 / 282 (9 de octubre = día 282)."]:
    item(d, t, size=9.5, after=1.5)
d.save(OUT)
print("guardado", OUT.name, "| referencias:", len(_order))
