"""Visa-R / 09: nota ejecutiva en Word (max. 5 paginas). Salida: Visa-R/Docs/Nota_Ejecutiva_Visa-R.docx
Lee cifras de Outputs/tables y usa las figuras nota_fig*.png de Outputs/Figures (script 08)."""
from pathlib import Path
import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor, Emu

ROOT = Path(__file__).resolve().parents[1]
FIG, TAB = ROOT / "Outputs" / "Figures", ROOT / "Outputs" / "tables"
OUT = ROOT / "Docs" / "Nota_Ejecutiva_Visa-R.docx"

AZ, NA, GRIS, NEGRO = RGBColor(0x1F, 0x5F, 0xB0), RGBColor(0xD2, 0x54, 0x1F), RGBColor(0x52, 0x51, 0x4E), RGBColor(0x1A, 0x1A, 0x19)
FONT = "Calibri"
PBDR_AFTER = ("w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap", "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")

# ---- cifras desde las tablas
r12 = pd.read_csv(TAB / "t12_visaR_resumen.csv", index_col=0)["valor"]
asq = pd.read_csv(TAB / "t12c_asequibilidad_hogares.csv")
be = pd.read_csv(TAB / "t13b_punto_equilibrio_tarifa.csv")
TRM = r12["TRM_COP_por_USD"]; N = r12["titulares_PPT_estimados_miles(escala GEIH)"] * 1e3
PIB = r12["PIB_implicito_USD_miles_millones"] * 1e9


def hogares(fee_label, k=1):
    u = f"tarifa del hogar >= {k} mes(es) de ingreso laboral del hogar"
    return asq[(asq.tarifa == fee_label) & (asq.umbral == u)].pct_hogares_con_venezolano.iloc[0]


def conv(tarifa, tau, H=10):
    return be[(be.horizonte == H) & (be.conversion_con_tarifa_464 == tau) & (be.tarifa_alternativa == tarifa)].conversion_necesaria_para_no_perder.iloc[0]


h464, h232, h56 = hogares("USD 464 (56+408) vigente"), hogares("mitad (USD 232)"), hogares("solo estudio USD 56 (se elimina la visa)")
rev = lambda f: N * f * TRM / 1e12
es = lambda x, d=1: f"{x:.{d}f}".replace(".", ",")


# ---- curva precio-recaudo-derrame (t17), mismo suavizado que la figura
cv = pd.read_csv(TAB / "t17_curva_precio_recaudo.csv"); cv = cv[cv.theta_meses_de_ingreso == 2].sort_values("tarifa_USD").reset_index(drop=True)
_tau = cv.conversion.rolling(5, center=True, min_periods=1).mean().to_numpy(); _F = cv.tarifa_USD.to_numpy().astype(float)
_S = r12["beneficio_fiscal_anual_B_USD_por_persona"] * 5
_rec = N * _tau * _F / 1e6; _tot = _rec + N * _tau * _S / 1e6
_at = lambda arr, f: float(__import__("numpy").interp(f, _F, arr))
F_REC = float(_F[int(_rec.argmax())]); F_TOT = float(_F[int(_tot.argmax())])
PCT_MAX = 100 * _at(_tot, 232) / _tot.max(); REC_RATIO = 100 * _at(_rec, 232) / _at(_rec, 464)
TAU464, TAU232 = 100 * _at(_tau, 464), 100 * _at(_tau, 232)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(0.8)
sec.top_margin, sec.bottom_margin = Inches(0.7), Inches(0.7)
CW = 8.5 - 1.6                                      # ancho util (pulgadas)

st = doc.styles["Normal"]; st.font.name = FONT; st.font.size = Pt(10); st.font.color.rgb = NEGRO
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.paragraph_format.space_after = Pt(4); st.paragraph_format.space_before = Pt(0); st.paragraph_format.line_spacing = 1.05


def para(text="", bold=False, size=None, color=None, align=None, after=None, before=None, italic=False, keep=False):
    p = doc.add_paragraph()
    if text:
        add_runs(p, text, bold=bold, size=size, color=color, italic=italic)
    if align: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if before is not None: p.paragraph_format.space_before = Pt(before)
    if keep: p.paragraph_format.keep_with_next = True
    return p


def add_runs(p, text, bold=False, size=None, color=None, italic=False):
    """Texto con **negrita** inline."""
    parts = text.split("**")
    for i, t in enumerate(parts):
        if not t: continue
        run = p.add_run(t); run.bold = bold or (i % 2 == 1); run.italic = italic
        run.font.name = FONT
        if size: run.font.size = Pt(size)
        if color is not None: run.font.color.rgb = color


def heading(text):
    p = para(text, bold=True, size=13, color=AZ, before=9, after=3, keep=True)
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"), ("w:color", "C9C8C3")): bt.set(qn(k), v)
    b.append(bt)
    pPr.insert_element_before(b, *PBDR_AFTER)
    return p


def bullet(text, after=2):
    p = doc.add_paragraph(style="List Bullet"); add_runs(p, text)
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.left_indent = Inches(0.22)
    return p


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexfill); tcPr.insert_element_before(shd, "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")


def borders(cell, **kw):
    tcPr = cell._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}"); spec = kw.get(side)
        if spec: e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(spec[0])); e.set(qn("w:color"), spec[1])
        else: e.set(qn("w:val"), "nil")
        b.append(e)
    tcPr.insert_element_before(b, "w:shd", "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")


def margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr(); m = OxmlElement("w:tcMar")
    for side, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(v)); e.set(qn("w:type"), "dxa"); m.append(e)
    tcPr.insert_element_before(m, "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")


def table(rows, widths, header=True, size=9, align_center_from=1, keep_rows=True):
    t = doc.add_table(rows=len(rows), cols=len(widths)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j]); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
            add_runs(c.paragraphs[0], val, bold=(header and i == 0), size=size, color=(RGBColor(255, 255, 255) if header and i == 0 else None))
            if j >= align_center_from: c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            margins(c)
            if keep_rows and i < len(rows) - 1: c.paragraphs[0].paragraph_format.keep_with_next = True
            if header and i == 0: shade(c, "1F5FB0"); borders(c)
            else: borders(c, bottom=(4, "D9D8D3"))
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
    return t


FIG_N = [0]


def figure(name, caption, width=6.2, keep_next=False):
    """Las figuras se dibujan al tamano real (6,2 in): se insertan sin escalar. El pie lleva solo el numero de figura."""
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0); p.paragraph_format.space_before = Pt(4); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(FIG / name), width=Inches(5.4))
    FIG_N[0] += 1
    c = para(f"Figura {FIG_N[0]}.", size=8, color=GRIS, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)
    return c


# ------------------------------------------------------------------ titulo
para("NOTA PARA DECISORES · 12 DE NOVIEMBRE DE 2026", bold=True, size=8.5, color=GRIS, after=1)
para("Reducir el costo de la Visa R conviene", bold=True, size=22, color=AZ, after=1)
para("Migrantes venezolanos con PPT: aporte económico, inclusión formal y costo fiscal", size=11, color=GRIS, after=6)

# mensaje central
box = doc.add_table(rows=1, cols=1); box.alignment = WD_TABLE_ALIGNMENT.CENTER
c = box.cell(0, 0); c.width = Inches(CW); shade(c, "EAF1FB"); margins(c, 110, 110, 160, 160)
borders(c, left=(24, "1F5FB0"))
p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
add_runs(p, f"**Recomendación: reducir a la mitad la tarifa de la Visa R (de USD 464 a ≈ USD 232) y exonerar a menores y hogares vulnerables.** "
            f"La tarifa recauda como máximo **{es(100*N*464/PIB, 2)}% del PIB, una sola vez**, y el recaudo va al Fondo Rotatorio de la Cancillería, no al presupuesto general. "
            f"En cambio, para **dos de cada tres hogares** con venezolanos equivale a más de un mes de su ingreso, justo cuando 0,8 millones de titulares pasan a ser elegibles en 2027–28 "
            f"y el PPT vence en mayo de 2031. Quien no pueda pagar vuelve a la irregularidad y pierde lo ganado con el PPT: salud, cuenta financiera y contrato.", size=10.5)

para("", after=3)
# KPIs
k = doc.add_table(rows=2, cols=4); k.alignment = WD_TABLE_ALIGNMENT.CENTER
kpi = [("1,76 M", "venezolanos sin nacionalidad colombiana (GEIH 2025)"), ("83%", "piensa quedarse; 6 años de residencia mediana"),
       (f"USD 464", f"tarifa vigente: estudio 56 + visa 408 (≈ COP {es(464*TRM/1e6)} M)"), (f"{h464:.0f}%", "de los hogares pagaría ≥ 1 mes de su ingreso laboral")]
for j, (big, small) in enumerate(kpi):
    a_, b_ = k.cell(0, j), k.cell(1, j)
    for cc in (a_, b_): cc.width = Inches(CW / 4); borders(cc, top=(4, "D9D8D3") if cc is a_ else None, bottom=(4, "D9D8D3") if cc is b_ else None); margins(cc, 40, 40, 80, 80)
    a_.paragraphs[0].paragraph_format.space_after = Pt(0); b_.paragraphs[0].paragraph_format.space_after = Pt(0)
    add_runs(a_.paragraphs[0], big, bold=True, size=19, color=(NA if j >= 2 else AZ)); a_.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_runs(b_.paragraphs[0], small, size=8, color=GRIS); b_.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

heading("Qué se recomienda decidir")
bullet("**Reducir la tarifa total a la mitad (≈ USD 232):** mantener el estudio (USD 56) y bajar la visa de USD 408 a ≈ USD 176, por resolución del Ministerio de Relaciones Exteriores, que fija las tarifas (Decreto 1067 de 2015).")
bullet("**Exonerar a menores y a hogares vulnerables** y permitir el pago en cuotas.")
bullet("**Escalonar los trámites** por año de elegibilidad (2027–28) y evaluar ampliar el plazo del PPT, que vence el 28 de mayo de 2031.")
bullet("**Decidir antes de 2027**, cuando se concentran los trámites, y medir la conversión durante el primer año para ajustar.", after=4)

# ------------------------------------------------------------------ 1
heading("1. Los venezolanos ya son parte de la economía y se quedan")
para("Son **1,76 millones** (GEIH 2025), el **83% piensa quedarse** y la mediana lleva **6 años** en el país. Su ingreso laboral suma ≈ **COP 13,8 billones al año** y el estudio de la OIM "
     "estima su aporte fiscal en **COP 1,5 billones** (1,9% del recaudo de personas naturales). Emprenden como los colombianos, pero con negocios más pequeños "
     "y menos formales (42% de los ocupados trabaja por cuenta propia, pero solo 22% de esos negocios está registrado, frente a 36% de los colombianos). Un permiso estable y asequible alarga su horizonte de inversión; el PPT, en cambio, caduca en 2031.")

# ------------------------------------------------------------------ 2
heading("2. Con PPT, los migrantes entran al sistema formal")
para("Con PPT, **91% está afiliado a salud (18% sin PPT)**, 55% tiene cuenta financiera (11%) y 20% de los ocupados tiene contrato escrito (4%) (Figura 1). "
     "Controlando por sexo, edad, año de llegada y otros factores, las diferencias son de **+66, +38 y +16 puntos**, y la dificultad para acceder a salud cuando se necesita baja **37 puntos**. "
     "La afiliación pasó de 31% en 2022 a 66% en 2026, pero es de apenas 26% entre los llegados desde 2023 (Figura 2). Los estudios sobre el PEP reportan +10 puntos de empleo formal, "
     "+22% de ingreso y +48% de consumo (Ibáñez et al., JEEA).")
figure("nota_fig2_con_vs_sin_ppt.png", "Figura 2. Cifras sin ajustar, EPM VIII-2025 (6.443 venezolanos). Asociación, no causalidad.", width=5.0)
figure("nota_fig1_afiliacion_salud.png", "Figura 3. Venezolanos sin nacionalidad colombiana. 2026*: enero–agosto.", width=5.3)
para("**El costo de salud existe con o sin tarifa.** Regularizar implica gasto en salud (≈ COP 0,4–0,5 billones al año si el PPT cubriera a todos) y la tarifa no lo compensa. "
     "La razón para reducirla es otra: **evitar que en 2031 se pierda lo ganado** y que quien no pueda pagar vuelva a la irregularidad.")

# ------------------------------------------------------------------ 3
heading("3. La tarifa recauda poco y excluye a muchos")
para(f"La Cancillería cobra **USD 56 de estudio y USD 408 de visa**. Si todos los titulares pagaran, el recaudo sería de ≈ **COP {es(rev(464))} billones ({es(100*N*464/PIB, 2)}% del PIB)**, "
     f"una sola vez y repartido hasta 2031: ≈ 0,03% del PIB por año frente a un déficit proyectado de 5,3% en 2026, y equivale a un año del aporte fiscal que la OIM estima para los venezolanos (COP 1,5 billones). "
     f"Del otro lado, la ola de trámites es inminente: **29% de los titulares será elegible en 2026, 81% en 2027 y 96% en 2028** (Figura 3), y para el **{h464:.0f}% de los hogares** con venezolanos "
     f"la tarifa equivale a más de un mes de su ingreso laboral (Figura 4); la tarifa mediana por hogar es de COP 3,0 millones.")
figure("nota_fig3_ola_de_tramites.png", "Figura 4. PPT + 5 años.", width=5.4)
figure("nota_fig4_asequibilidad.png", "Figura 5. Tarifa por persona.", width=5.4)

# ------------------------------------------------------------------ 4
heading("4. La opción recomendada: reducir a la mitad")
para(f"**El precio óptimo no es el que más recauda.** Con una demanda ilustrativa (la conversión cae cuando sube el precio), el recaudo de la Cancillería es máximo cerca de USD {F_REC:.0f} por persona: "
     f"el precio vigente ya está cerca de ese máximo, pero solo convierte {TAU464:.0f}% de los titulares. Cada persona que convierte genera un derrame (acceso a salud, aportes, formalización) que la literatura "
     f"sitúa en ≈ USD 980 en 5 años. Contando ese derrame, el valor total es máximo cerca de USD {F_TOT:.0f}; **con USD 232 se alcanza {PCT_MAX:.0f}% de ese máximo, la conversión sube de {TAU464:.0f}% a {TAU232:.0f}% "
     f"y la Cancillería conserva {REC_RATIO:.0f}% de su recaudo** (Figura 5).")
figure("nota_fig7_curva_precio.png", "Figura 6. Escenario ilustrativo.", width=5.4)
rows = [["Opción", "Tarifa por persona", "Ingreso máximo (COP billones)", "Hogares con tarifa ≥ 1 mes de ingreso", "Conversión necesaria para no perder fiscalmente*"],
        ["Vigente", "USD 464", f"{es(rev(464))}", f"{h464:.0f}%", "—"],
        ["**Mitad (recomendada)**", "**USD 232**", f"**{es(rev(232))}**", f"**{h232:.0f}%**", f"**{100*conv('mitad USD 232',0.5):.0f}% (si hoy es 50%) · {100*conv('mitad USD 232',0.7):.0f}% (si es 70%)**"],
        ["Solo estudio", "USD 56", f"{es(rev(56))}", f"{h56:.0f}%", f"{100*conv('solo estudio USD 56',0.5):.0f}% · {100*conv('solo estudio USD 56',0.7):.0f}%"],
        ["Sin costo", "USD 0", "0,0", "0%", f"{100*conv('gratis',0.5):.0f}% · {100*conv('gratis',0.7):.0f}%"]]
table(rows, [1.2, 1.05, 1.25, 1.55, 1.85], size=8.5, keep_rows=True)
para("* Horizonte de 10 años y contabilidad de la literatura (la regularización reduce el costo neto por hogar). Reducir a la mitad se paga con un aumento realista de la conversión "
     f"({100*conv('mitad USD 232',0.5):.0f}% desde 50%, o {100*conv('mitad USD 232',0.7):.0f}% desde 70%), frente a un techo de ≈ 83–86% (quienes quieren quedarse). "
     "Eliminar la tarifa solo se paga con aumentos cercanos al techo: por eso se recomienda la mitad.", size=8.5, color=GRIS, before=3, after=4)
para("**Decisión solicitada:** expedir antes de 2027 la resolución que reduce la tarifa y fija las exoneraciones. Las salvedades de la evidencia están en el anexo.", before=2, after=3)




# ------------------------------------------------------------------ anexo
para("", after=6)
heading("Anexo. Evidencia, supuestos y salvedades")
rows = [["Cifra", "Valor", "Fuente", "Estado"],
        ["Venezolanos sin nacionalidad colombiana", "1,76 M (2025)", "GEIH-DANE", "Calculado con microdatos"],
        ["Intención de quedarse; años de residencia", "83%; mediana 6", "GEIH 2025", "Calculado con microdatos"],
        ["Ingreso laboral anual de los venezolanos", "COP 13,8 billones", "GEIH 2025", "Calculado con microdatos"],
        ["Aporte fiscal anual", "COP 1,5 billones (1,9%)", "OIM/Equilibrium (2025); U. del Rosario", "Estudio OIM leído; cifra Rosario por prensa"],
        ["Con PPT vs sin PPT (salud, cuenta, contrato, acceso)", "+66, +38, +16, −37 pp", "EPM VIII-2025 (DANE)", "Calculado; asociación ajustada"],
        ["Efecto de la regularización (PEP)", "+10 pp formal, +22% ingreso, +48% consumo", "Ibáñez et al., JEEA", "Solo resumen; texto completo sin leer"],
        ["Tarifa de la Visa R (tiempo acumulado ETPV)", "USD 56 + 408 = 464", "Cancillería, “Costos trámites”", "Verificada (página oficial, 12-nov-2026)"],
        ["Requisitos: 5 años de PEP/PPT y PPT vigente", "Art. 91, Res. 5477/2022", "Cancillería (normograma)", "Verificado; versión vigente por confirmar"],
        ["Destino del recaudo", "Fondo Rotatorio", "Ley 1212 de 2008", "Resumen del Gestor Normativo"],
        ["Déficit fiscal 2026", "5,3% del PIB", "Marco Fiscal 2026", "Prensa (Valora Analitik)"],
        ["Titulares de PPT", "≈ 1,15 M", "GEIH × EPM", "Estimación; cifra oficial pendiente"]]
table(rows, [2.25, 1.45, 1.75, 1.45], size=8, align_center_from=9)
para("", after=4)
para("Supuestos de los escenarios", bold=True, size=10, color=AZ, after=2, keep=True)
bullet("**Ingreso por la tarifa:** titulares × tarifa × TRM (COP 3.235 por USD, 6-nov-2026); PIB implícito de USD 353 mil millones (relación del estudio de la OIM).")
bullet("**Asequibilidad:** todos los miembros venezolanos del hogar pagan; se compara con el ingreso laboral mensual del hogar (GEIH 2026, enero–agosto).")
bullet("**Conversión necesaria:** la regularización reduce el costo neto por hogar en USD 446 al año (JEEA, resumen), repartidos entre 2,3 venezolanos por hogar; horizonte de 10 años; sin descuento.")
bullet("**Costo de salud (si el PPT cubriera a todos):** UPC 2025 de COP 1,32 millones (subsidiado) y 1,52 millones (contributivo); IVA efectivo de 5% (rango 3–7%); ahorro y remesas de 10% cada uno del ingreso.")
bullet("**Curva precio–recaudo–derrame (Figura 5):** conversión = 85% (quienes quieren quedarse) × hogares que pagan hasta 2 meses de su ingreso (GEIH 2026); derrame = USD 196 por persona-año × 5 años (literatura, resumen). "
       "Sensibilidad: si el hogar solo paga hasta 1 mes de ingreso, el recaudo máximo está en USD 270; hasta 3 meses, en USD 690. Con derrame, el valor máximo está en USD 0, 140 y 270, respectivamente.")
bullet("**Elegibilidad:** año de obtención del PPT (EPM) más 5 años; no considera el tiempo previo con PEP, por lo que subestima.", after=4)
para("Salvedades", bold=True, size=10, color=AZ, after=2, before=4, keep=True)
bullet("Las cifras son **asociaciones y escenarios** con supuestos, no efectos causales. En empleo, horas, seguridad alimentaria y remesas, la EPM **no muestra diferencias claras** entre quienes tienen PPT y quienes no.")
bullet("La **demanda de la visa no está medida**; la curva es ilustrativa. Si en vez de derrame cada persona regularizada implicara un costo neto de salud (contabilidad A), el precio óptimo sería alto y no habría razón fiscal para reducirlo.")
bullet("Con otra contabilidad (costo de salud por nuevo afiliado), más regularizados implican **más gasto público**; no se descuenta el costo actual de urgencias. Es el principal riesgo de la propuesta.")
bullet("Falta verificar la **tarifa de beneficiarios (menores)**, el impuesto de timbre y el texto vigente del art. 91 de la Res. 5477. El total de titulares (≈ 1,15 M) es de la GEIH; el oficial puede ser mayor.")
bullet("**Próximos pasos:** obtener la cifra oficial de titulares, leer en detalle los estudios citados y medir el efecto de la tarifa sobre la conversión.", after=4)
para("Fuentes y detalle de métodos: carpeta Visa-R (Docs/00 a 08, Outputs/tables, Code/01 a 10). Cálculos propios.", size=8, color=GRIS, italic=True)

# ---- pie con numero de pagina
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run("Visa R · Nota ejecutiva · página "); r.font.size = Pt(8); r.font.color.rgb = GRIS
run = fp.add_run(); run.font.size = Pt(8); run.font.color.rgb = GRIS
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tag:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
    run._r.append(e)

for z in doc.settings.element.iter(qn("w:zoom")):
    z.set(qn("w:percent"), "100")
doc.save(OUT)
print("guardado", OUT)
