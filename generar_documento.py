"""Genera el documento PDF del proyecto final."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import date
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sistema_vacaciones import SistemaVacaciones
from empleado_sindicalizado import EmpleadoSindicalizado
from empleado_confianza import EmpleadoConfianza
from empleado_temporal import EmpleadoTemporal


def estilos():
    base = getSampleStyleSheet()
    titulo   = ParagraphStyle("titulo",   parent=base["Title"],   fontSize=16, alignment=TA_CENTER, spaceAfter=4)
    seccion  = ParagraphStyle("seccion",  parent=base["Heading1"], fontSize=13, spaceBefore=12, spaceAfter=4)
    subsec   = ParagraphStyle("subsec",   parent=base["Heading2"], fontSize=11, spaceBefore=8,  spaceAfter=3)
    normal   = ParagraphStyle("normal",   parent=base["Normal"],   fontSize=10, leading=13, spaceAfter=4)
    bullet   = ParagraphStyle("bullet",   parent=base["Normal"],   fontSize=10, leading=13, leftIndent=14, spaceAfter=2)
    return titulo, seccion, subsec, normal, bullet


def simple_tabla(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1,-1), 9),
        ("GRID",          (0, 0), (-1,-1), 0.5, colors.grey),
        ("TOPPADDING",    (0, 0), (-1,-1), 3),
        ("BOTTOMPADDING", (0, 0), (-1,-1), 3),
        ("LEFTPADDING",   (0, 0), (-1,-1), 5),
        ("ROWBACKGROUNDS",(0, 1), (-1,-1), [colors.white, colors.HexColor("#f0f0f0")]),
    ]))
    return t


def generar_pdf():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Documento_Proyecto_Final.pdf")

    sistema = SistemaVacaciones()
    sistema.cargar_archivos()

    doc = SimpleDocTemplate(ruta, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)

    T, SEC, SUB, NOR, BUL = estilos()
    story = []

    # ── PORTADA ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Proyecto Final: Administración de Vacaciones", T))
    story.append(Paragraph("Galactic Force Solutions", T))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Materia: Programación", NOR))
    story.append(Paragraph("Profesor: M.I. Gerardo Avilés Rosas", NOR))
    story.append(Paragraph("Facultad de Ciencias, UNAM", NOR))
    story.append(Paragraph(f"Fecha: {date.today()}", NOR))
    story.append(PageBreak())

    # ── SECCIÓN 1: METODOLOGÍA OOP ──────────────────────────────────────────
    story.append(Paragraph("1. Metodología de Diseño Orientado a Objetos", SEC))

    # 1.1 Clases descubiertas
    story.append(Paragraph("1.1 Descubrimiento de clases", SUB))
    story.append(Paragraph(
        "A partir del análisis del problema se identificaron las siguientes clases:", NOR))

    clases = [
        ["Clase", "Descripción"],
        ["Empleado (abstracta)",        "Clase base con atributos comunes a todos los empleados. No se instancia directamente."],
        ["EmpleadoSindicalizado",       "Hereda de Empleado. Agrega el sindicato al que pertenece."],
        ["EmpleadoConfianza",           "Hereda de Empleado. Agrega nivel de confianza y tipo de jornada."],
        ["EmpleadoTemporal",            "Hereda de Empleado. Agrega tipo de contrato y fechas de vigencia."],
        ["CatalogoVacaciones",          "Contiene la tabla de días de vacaciones por ley (LFT) según antigüedad."],
        ["VacacionesEmpleado",          "Registra el saldo de vacaciones de un empleado en el año actual."],
        ["SolicitudVacaciones",         "Representa una petición de vacaciones con sus fechas y estatus."],
        ["SistemaVacaciones",           "Clase principal que coordina todas las operaciones del sistema."],
    ]
    story.append(simple_tabla(clases, [1.8*inch, 4.4*inch]))
    story.append(Spacer(1, 0.1*inch))

    # 1.2 Responsabilidades
    story.append(Paragraph("1.2 Responsabilidades", SUB))

    resps = [
        ["Clase", "Responsabilidades"],
        ["Empleado",               "Guardar datos personales y laborales. Calcular edad y antigüedad."],
        ["EmpleadoSindicalizado",  "Calcular 5 días extra de vacaciones a partir del 2.º año."],
        ["EmpleadoConfianza",      "Calcular 3 días extra si es senior/directivo, jornada completa y ≥ 2 años."],
        ["EmpleadoTemporal",       "Calcular vacaciones proporcionales: días_ley × (meses_laborados / 12)."],
        ["CatalogoVacaciones",     "Devolver los días de vacaciones que corresponden según los años trabajados."],
        ["VacacionesEmpleado",     "Llevar el conteo de días otorgados, usados y restantes. Indicar si están habilitadas."],
        ["SolicitudVacaciones",    "Calcular la fecha fin sin contar sábados/domingos. Validar 7 días de anticipación."],
        ["SistemaVacaciones",      "Cargar y guardar archivos CSV. Gestionar empleados, vacaciones y solicitudes."],
    ]
    story.append(simple_tabla(resps, [1.8*inch, 4.4*inch]))
    story.append(Spacer(1, 0.1*inch))

    # 1.3 Escenarios
    story.append(Paragraph("1.3 Escenarios", SUB))

    escenarios = [
        ("Inicio del sistema",
         ["Se ejecuta main.py.",
          "SistemaVacaciones carga los archivos CSV (empleados, vacaciones, solicitudes, catálogo).",
          "Se revisa si algún empleado cumplió un nuevo año laboral: si es así, se resetean sus vacaciones.",
          "Se muestra el menú principal."]),
        ("Registrar solicitud de vacaciones",
         ["El usuario ingresa número de empleado, fecha de inicio y días deseados.",
          "Se valida que el empleado exista, tenga días disponibles y la solicitud tenga ≥ 7 días de anticipación.",
          "Se calcula la fecha fin sin contar sábados ni domingos.",
          "Se genera un número único de solicitud y se descuentan los días del saldo del empleado."]),
        ("Dar de baja a un empleado",
         ["El usuario busca al empleado por algún criterio y confirma la eliminación.",
          "El empleado se elimina de la lista activa.",
          "Sus datos se guardan en empleados_borrados.csv para no perder trazabilidad."]),
        ("Cierre del sistema",
         ["El usuario selecciona 'Cerrar el día y salir'.",
          "Se guardan todos los cambios en los archivos CSV.",
          "El sistema termina."]),
    ]

    for titulo_esc, pasos in escenarios:
        story.append(Paragraph(f"<b>Escenario: {titulo_esc}</b>", NOR))
        for i, paso in enumerate(pasos, 1):
            story.append(Paragraph(f"{i}. {paso}", BUL))
        story.append(Spacer(1, 0.05*inch))

    # 1.4 Diagrama de clases
    story.append(Paragraph("1.4 Diagrama de clases", SUB))
    story.append(diagrama_clases())
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(
        "Nota: Las flechas indican herencia. SistemaVacaciones contiene instancias de "
        "las demás clases y coordina su interacción.", NOR))
    story.append(PageBreak())

    # ── SECCIÓN 2: REPORTE EJECUTIVO ────────────────────────────────────────
    story.append(Paragraph("2. Reporte Ejecutivo — Estatus Inicial", SEC))
    story.append(Paragraph(f"Fecha de generación: {date.today()}", NOR))

    emps  = sistema.empleados
    vacs  = sistema.vacaciones
    sols  = sistema.solicitudes
    mapa  = {e.numero_empleado: e for e in emps}

    sinds = [e for e in emps if isinstance(e, EmpleadoSindicalizado)]
    confs = [e for e in emps if isinstance(e, EmpleadoConfianza)]
    temps = [e for e in emps if isinstance(e, EmpleadoTemporal)]

    # Total de empleados
    story.append(Paragraph("2.1 Total de empleados", SUB))
    t_emps = [
        ["Tipo", "Cantidad"],
        ["Sindicalizados",  str(len(sinds))],
        ["Confianza",       str(len(confs))],
        ["Temporales",      str(len(temps))],
        ["Total",           str(len(emps))],
    ]
    story.append(simple_tabla(t_emps, [3*inch, 3*inch]))
    story.append(Spacer(1, 0.1*inch))

    # Empleados de mayor antigüedad
    story.append(Paragraph("2.2 Empleados con mayor antigüedad", SUB))
    top = sorted(emps, key=lambda e: e.calcular_antiguedad(), reverse=True)[:10]
    t_top = [["Nombre", "Tipo", "Antigüedad", "Departamento"]]
    for e in top:
        t_top.append([e.nombre_completo, e.get_tipo_empleado(),
                      f"{e.calcular_antiguedad()} años", e.departamento])
    story.append(simple_tabla(t_top, [2.3*inch, 1.3*inch, 1*inch, 1.6*inch]))
    story.append(Spacer(1, 0.1*inch))

    # Solicitudes totales
    story.append(Paragraph("2.3 Solicitudes de vacaciones", SUB))

    por_tipo   = {}
    por_estatus = {"pendiente": 0, "aprobada": 0, "rechazada": 0}
    for sol in sols:
        emp = mapa.get(sol.numero_empleado)
        tipo = emp.get_tipo_empleado() if emp else "Desconocido"
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        por_estatus[sol.estatus] = por_estatus.get(sol.estatus, 0) + 1

    t_sols = [["Criterio", "Cantidad"]]
    t_sols.append(["Total de solicitudes", str(len(sols))])
    for tipo, cnt in sorted(por_tipo.items()):
        t_sols.append([f"  Por tipo: {tipo}", str(cnt)])
    for est, cnt in por_estatus.items():
        t_sols.append([f"  Por estatus: {est.capitalize()}", str(cnt)])
    story.append(simple_tabla(t_sols, [3*inch, 3*inch]))
    story.append(Spacer(1, 0.1*inch))

    # Resumen de días de vacaciones
    story.append(Paragraph("2.4 Resumen de días de vacaciones por tipo de empleado", SUB))
    t_dias = [["Tipo", "Con vacaciones\nhabilitadas", "Días totales\notorgados", "Días\nusados", "Días\nrestantes"]]
    for tipo, lista in [("Sindicalizado", sinds), ("Confianza", confs), ("Temporal", temps)]:
        hab    = [e for e in lista if vacs.get(e.numero_empleado) and vacs[e.numero_empleado].habilitado]
        totales = sum(vacs[e.numero_empleado].dias_totales    for e in hab)
        usados  = sum(vacs[e.numero_empleado].dias_utilizados for e in hab)
        rest    = sum(vacs[e.numero_empleado].dias_restantes  for e in hab)
        t_dias.append([tipo, str(len(hab)), str(totales), str(usados), str(rest)])
    story.append(simple_tabla(t_dias, [1.4*inch, 1.3*inch, 1.3*inch, 1.1*inch, 1.1*inch]))

    doc.build(story)
    print(f"PDF generado: {ruta}")
    return ruta


def diagrama_clases():
    """Genera el diagrama de clases como tabla ASCII/visual sencilla."""
    COLOR_BASE = colors.HexColor("#cce0f5")
    COLOR_SUB  = colors.HexColor("#d9f0d9")
    COLOR_OTR  = colors.HexColor("#fff3cc")

    def caja(nombre, attrs, meths, color):
        lineas = [[Paragraph(f"<b>{nombre}</b>",
                             ParagraphStyle("h", fontSize=8.5, fontName="Helvetica-Bold", alignment=TA_CENTER))]]
        for a in attrs:
            lineas.append([Paragraph(f"  {a}", ParagraphStyle("a", fontSize=7.5, fontName="Courier", leading=10))])
        lineas.append([Paragraph("───", ParagraphStyle("sep", fontSize=7, alignment=TA_CENTER))])
        for m in meths:
            lineas.append([Paragraph(f"  {m}", ParagraphStyle("m", fontSize=7.5, fontName="Courier",
                                                               leading=10, textColor=colors.HexColor("#003399")))])
        t = Table(lineas, colWidths=[2*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), color),
            ("BOX",           (0, 0), (-1,-1), 0.8, colors.black),
            ("INNERGRID",     (0, 0), (-1,-1), 0.3, colors.grey),
            ("TOPPADDING",    (0, 0), (-1,-1), 2),
            ("BOTTOMPADDING", (0, 0), (-1,-1), 2),
            ("LEFTPADDING",   (0, 0), (-1,-1), 4),
        ]))
        return t

    empleado = caja("<<abstracta>> Empleado",
        ["numero_empleado", "nombre_completo", "fecha_nacimiento",
         "correo, telefono, salario", "puesto, departamento",
         "fecha_contratacion, dia_descanso"],
        ["calcular_edad()", "calcular_antiguedad()",
         "get_tipo_empleado()  abstracto",
         "calcular_dias_extra()  abstracto"],
        COLOR_BASE)

    sind = caja("EmpleadoSindicalizado",
        ["nombre_sindicato"],
        ["get_tipo_empleado()", "calcular_dias_extra()"],
        COLOR_SUB)

    conf = caja("EmpleadoConfianza",
        ["nivel_confianza", "jornada"],
        ["get_tipo_empleado()", "calcular_dias_extra()"],
        COLOR_SUB)

    temp = caja("EmpleadoTemporal",
        ["tipo_contrato", "fecha_inicio_contrato", "fecha_fin_contrato"],
        ["get_tipo_empleado()", "calcular_dias_extra()",
         "calcular_vacaciones_proporcionales()"],
        COLOR_SUB)

    catalogo = caja("CatalogoVacaciones",
        ["_TABLA (tabla LFT)"],
        ["obtener_dias(antiguedad)"],
        COLOR_OTR)

    vac_emp = caja("VacacionesEmpleado",
        ["numero_empleado", "year", "dias_otorgados_ley",
         "dias_extra", "dias_totales",
         "dias_utilizados", "habilitado"],
        ["usar_dias(n)", "devolver_dias(n)"],
        COLOR_OTR)

    solicitud = caja("SolicitudVacaciones",
        ["numero_solicitud", "numero_empleado",
         "fecha_solicitud", "fecha_inicio",
         "fecha_fin", "dias_solicitados", "estatus"],
        ["calcular_fecha_fin()", "validar_anticipacion()",
         "cambiar_estatus()"],
        COLOR_OTR)

    sistema = caja("SistemaVacaciones",
        ["empleados: list", "catalogo", "vacaciones: dict", "solicitudes: list"],
        ["cargar_archivos()", "guardar_archivos()",
         "alta_empleado()", "baja_empleado()",
         "registrar_solicitud()",
         "consultar_empleados()", "reporte_ejecutivo()"],
        COLOR_BASE)

    flecha = Paragraph("▼  hereda", ParagraphStyle("f", fontSize=9, alignment=TA_CENTER,
                                                    fontName="Helvetica-Bold"))
    contiene = Paragraph("◆  contiene / usa", ParagraphStyle("f2", fontSize=8,
                                                              alignment=TA_CENTER,
                                                              textColor=colors.darkgreen))

    layout = Table([
        ["",         empleado,  "",         ""],
        ["", flecha, flecha,    flecha    ],
        [sind,       conf,      temp,       ""],
        ["", "",     "",        ""],
        [catalogo,   vac_emp,   solicitud,  ""],
        ["",         contiene,  "",         ""],
        ["",         sistema,   "",         ""],
    ], colWidths=[2.1*inch, 2.1*inch, 2.1*inch, 0.4*inch])

    layout.setStyle(TableStyle([
        ("ALIGN",  (0,0),(-1,-1), "CENTER"),
        ("VALIGN", (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
    ]))
    return layout


if __name__ == "__main__":
    generar_pdf()
