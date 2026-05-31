"""Script que genera el documento PDF del proyecto: metodología OOP y reporte ejecutivo."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import date
import os
import sys

# Importar el sistema para obtener datos reales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sistema_vacaciones import SistemaVacaciones
from empleado_sindicalizado import EmpleadoSindicalizado
from empleado_confianza import EmpleadoConfianza
from empleado_temporal import EmpleadoTemporal


# ─────────────────────────── ESTILOS ───────────────────────────────────────

def crear_estilos():
    base = getSampleStyleSheet()

    titulo_doc = ParagraphStyle(
        "TituloDoc", parent=base["Title"],
        fontSize=22, textColor=colors.HexColor("#1a3c5e"),
        spaceAfter=6, alignment=TA_CENTER, fontName="Helvetica-Bold"
    )
    subtitulo_doc = ParagraphStyle(
        "SubtituloDoc", parent=base["Normal"],
        fontSize=13, textColor=colors.HexColor("#2c6496"),
        spaceAfter=4, alignment=TA_CENTER, fontName="Helvetica"
    )
    seccion = ParagraphStyle(
        "Seccion", parent=base["Heading1"],
        fontSize=14, textColor=colors.white,
        backColor=colors.HexColor("#1a3c5e"),
        spaceBefore=14, spaceAfter=8,
        leftIndent=-6, rightIndent=-6,
        borderPad=5, fontName="Helvetica-Bold"
    )
    subseccion = ParagraphStyle(
        "Subseccion", parent=base["Heading2"],
        fontSize=12, textColor=colors.HexColor("#1a3c5e"),
        spaceBefore=10, spaceAfter=4,
        fontName="Helvetica-Bold", borderPad=2
    )
    cuerpo = ParagraphStyle(
        "Cuerpo", parent=base["Normal"],
        fontSize=10, leading=14, alignment=TA_JUSTIFY,
        spaceAfter=6, fontName="Helvetica"
    )
    bullet = ParagraphStyle(
        "Bullet", parent=base["Normal"],
        fontSize=10, leading=13,
        leftIndent=16, bulletIndent=6, spaceAfter=3,
        fontName="Helvetica"
    )
    codigo = ParagraphStyle(
        "Codigo", parent=base["Code"],
        fontSize=8, leading=11, fontName="Courier",
        backColor=colors.HexColor("#f4f4f4"),
        borderColor=colors.HexColor("#cccccc"),
        borderWidth=0.5, borderPad=4,
        spaceAfter=6
    )
    nota = ParagraphStyle(
        "Nota", parent=base["Normal"],
        fontSize=9, leading=12, textColor=colors.HexColor("#555555"),
        fontName="Helvetica-Oblique", spaceAfter=4
    )
    return {
        "titulo_doc": titulo_doc, "subtitulo_doc": subtitulo_doc,
        "seccion": seccion, "subseccion": subseccion,
        "cuerpo": cuerpo, "bullet": bullet,
        "codigo": codigo, "nota": nota,
    }


# ─────────────────────────── HELPERS DE TABLA ──────────────────────────────

HEADER_COLOR  = colors.HexColor("#1a3c5e")
ROW_ALT_COLOR = colors.HexColor("#e8f0f7")
BORDER_COLOR  = colors.HexColor("#bbbbbb")


def estilo_tabla(n_cols, header=True):
    cmds = [
        ("FONTNAME",    (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("GRID",        (0, 0), (-1, -1), 0.4, BORDER_COLOR),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ROW_ALT_COLOR]),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        cmds += [
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_COLOR),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, 0), 10),
        ]
    return TableStyle(cmds)


def tabla(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths)
    t.setStyle(estilo_tabla(len(data[0]), header))
    return t


# ─────────────────────────── PORTADA ───────────────────────────────────────

def portada(story, estilos):
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("SISTEMA DE ADMINISTRACIÓN DE VACACIONES", estilos["titulo_doc"]))
    story.append(Paragraph("Galactic Force Solutions", estilos["subtitulo_doc"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2c6496")))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "Metodología de Diseño Orientado a Objetos<br/>y Reporte Ejecutivo Inicial",
        estilos["subtitulo_doc"]
    ))
    story.append(Spacer(1, 0.8 * inch))

    datos_portada = [
        ["Materia:",        "Programación"],
        ["Profesor:",       "M.I. Gerardo Avilés Rosas"],
        ["Facultad:",       "Ciencias, UNAM"],
        ["Fecha:",          str(date.today())],
        ["Proyecto:",       "Final — Administración de Vacaciones"],
    ]
    t = Table(datos_portada, colWidths=[1.8 * inch, 4 * inch])
    t.setStyle(TableStyle([
        ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",  (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a3c5e")),
    ]))
    story.append(t)
    story.append(PageBreak())


# ─────────────────────────── SECCIÓN 1: METODOLOGÍA OOP ────────────────────

def seccion_metodologia(story, estilos):
    S = estilos

    story.append(Paragraph("1. METODOLOGÍA DE DISEÑO ORIENTADO A OBJETOS", S["seccion"]))
    story.append(Spacer(1, 0.1 * inch))

    # 1.1 Descubrimiento de clases
    story.append(Paragraph("1.1 Descubrimiento de Clases y Objetos", S["subseccion"]))
    story.append(Paragraph(
        "A partir del análisis del problema se identificaron los siguientes conceptos "
        "clave que se modelan como clases en la solución:", S["cuerpo"]
    ))

    clases = [
        ["Clase", "Tipo", "Justificación"],
        ["Empleado", "Abstracta (ABC)", "Concepto central del dominio. Define atributos y comportamientos comunes a los tres tipos de empleados. No se instancia directamente."],
        ["EmpleadoSindicalizado", "Concreta (hereda Empleado)", "Especialización de Empleado que pertenece a un sindicato. Regla de vacaciones: +5 días desde el 2.º año."],
        ["EmpleadoConfianza", "Concreta (hereda Empleado)", "Especialización con nivel de confianza y jornada. Regla: +3 días si senior/directivo, jornada completa y ≥2 años."],
        ["EmpleadoTemporal", "Concreta (hereda Empleado)", "Especialización con contrato por tiempo definido. Vacaciones proporcionales: días_ley × (meses/12)."],
        ["CatalogoVacaciones", "Servicio", "Encapsula la tabla oficial LFT de días de vacaciones por antigüedad. Provee obtener_dias(años)."],
        ["VacacionesEmpleado", "Entidad de estado", "Registra el saldo de vacaciones de un empleado en el año actual: días otorgados, usados y restantes."],
        ["SolicitudVacaciones", "Entidad de transacción", "Representa una petición de vacaciones. Calcula fechas fin excluyendo sábados/domingos y valida anticipación mínima."],
        ["SistemaVacaciones", "Fachada (Facade)", "Clase controladora central que coordina todas las operaciones: altas, bajas, consultas, solicitudes y reportes."],
    ]
    t = tabla(clases, [1.4*inch, 1.5*inch, 3.7*inch])
    story.append(t)
    story.append(Spacer(1, 0.15 * inch))

    # 1.2 Responsabilidades
    story.append(Paragraph("1.2 Responsabilidades de las Clases", S["subseccion"]))

    responsabilidades = [
        ["Clase", "Responsabilidades principales"],
        ["Empleado (ABC)",
         "• Almacenar datos personales y laborales comunes.\n• Calcular edad y antigüedad exactas.\n• Definir contrato abstracto para calcular días extra y serialización CSV."],
        ["EmpleadoSindicalizado",
         "• Almacenar nombre del sindicato.\n• Implementar regla de 5 días extra ≥ 2 años."],
        ["EmpleadoConfianza",
         "• Almacenar nivel (junior/senior/directivo) y jornada.\n• Implementar regla de 3 días extra condicionados."],
        ["EmpleadoTemporal",
         "• Almacenar tipo de contrato e intervalo de fechas.\n• Calcular vacaciones proporcionales al tiempo laborado."],
        ["CatalogoVacaciones",
         "• Proveer días de vacaciones por ley según tabla LFT.\n• Mostrar catálogo completo.\n• Serializar a CSV."],
        ["VacacionesEmpleado",
         "• Mantener saldo de días: otorgados, extra, usados y restantes.\n• Descontar días al registrar solicitud.\n• Devolver días al cancelar solicitud.\n• Indicar si el empleado ya cumplió su primer año."],
        ["SolicitudVacaciones",
         "• Registrar datos de la petición de vacaciones.\n• Calcular fecha fin saltando sábados/domingos.\n• Validar anticipación mínima de 7 días.\n• Controlar cambios de estatus solo en pendientes."],
        ["SistemaVacaciones",
         "• Cargar y guardar todos los archivos CSV al iniciar/cerrar el día.\n• Revisar aniversarios laborales y resetear vacaciones.\n• Ejecutar todas las operaciones de negocio (CRUD).\n• Generar reporte ejecutivo."],
    ]
    t = tabla(responsabilidades, [1.6*inch, 5*inch])
    story.append(t)
    story.append(Spacer(1, 0.15 * inch))

    # 1.3 Escenarios
    story.append(Paragraph("1.3 Escenarios Principales", S["subseccion"]))

    escenarios = [
        ("Escenario 1: Inicio del día",
         ["El especialista de RH inicia el sistema (main.py).",
          "SistemaVacaciones.cargar_archivos() lee empleados.csv, vacaciones_empleados.csv, solicitudes_empleados.csv y catalogo.csv.",
          "Para cada empleado se revisa si cumplió un nuevo año laboral.",
          "Si cumplió año: se archivan las vacaciones anteriores en vacaciones_anteriores.csv y se generan nuevas con el catálogo.",
          "Si acaba de cumplir su primer año: se habilitan sus vacaciones.",
          "El menú principal queda disponible para operar."]),
        ("Escenario 2: Alta de nueva solicitud de vacaciones",
         ["El especialista selecciona 'Nueva solicitud' en el menú.",
          "Ingresa el número de empleado, la fecha de inicio y los días hábiles deseados.",
          "SistemaVacaciones valida: empleado existe, vacaciones habilitadas, días disponibles ≥ días solicitados, anticipación ≥ 7 días.",
          "SolicitudVacaciones.calcular_fecha_fin() determina la fecha final saltando sábados y domingos.",
          "Se genera un número de solicitud único (SOL####) y la fecha de solicitud es la actual.",
          "VacacionesEmpleado.usar_dias() descuenta los días del saldo.",
          "La solicitud queda en estatus 'pendiente' y se agrega a la lista."]),
        ("Escenario 3: Baja de un empleado",
         ["El especialista selecciona 'Baja de empleado' y el criterio de búsqueda.",
          "SistemaVacaciones.consultar_empleados() encuentra las coincidencias.",
          "El especialista confirma la eliminación.",
          "El empleado se elimina de la lista activa y su registro de vacaciones se elimina del diccionario.",
          "gestor_archivos.archivar_empleado_borrado() agrega el registro a empleados_borrados.csv con la fecha de baja para trazabilidad."]),
        ("Escenario 4: Cierre del día",
         ["El especialista selecciona 'Cerrar el día y salir' en el menú.",
          "SistemaVacaciones.guardar_archivos() escribe el estado actualizado en todos los CSV.",
          "Los archivos quedan listos para ser leídos al siguiente inicio del sistema."]),
    ]

    for titulo, pasos in escenarios:
        story.append(Paragraph(titulo, S["subseccion"]))
        for i, paso in enumerate(pasos, 1):
            story.append(Paragraph(f"  {i}. {paso}", S["bullet"]))
        story.append(Spacer(1, 0.08 * inch))

    # 1.4 Diagrama de clases
    story.append(Paragraph("1.4 Diagrama de Clases", S["subseccion"]))
    story.append(Paragraph(
        "El siguiente diagrama ilustra la jerarquía de herencia y las relaciones "
        "entre las clases del sistema:", S["cuerpo"]
    ))

    diagrama_clases(story, estilos)
    story.append(PageBreak())


def diagrama_clases(story, estilos):
    """Genera una representación visual del diagrama de clases con tablas de ReportLab."""
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors

    COLOR_ABC    = colors.HexColor("#1a3c5e")
    COLOR_SUB    = colors.HexColor("#2c6496")
    COLOR_SERV   = colors.HexColor("#2e7d32")
    COLOR_ENTIDAD = colors.HexColor("#6a1b9a")
    BLANCO = colors.white

    def clase_box(nombre, tipo_color, atributos, metodos):
        header = [[Paragraph(f"<b>{nombre}</b>",
                             ParagraphStyle("ch", fontSize=9, textColor=BLANCO,
                                            fontName="Helvetica-Bold", alignment=TA_CENTER))]]
        attrs  = [[Paragraph(a, ParagraphStyle("ca", fontSize=7.5, fontName="Courier",
                                               leading=10))] for a in atributos]
        meths  = [[Paragraph(m, ParagraphStyle("cm", fontSize=7.5, fontName="Courier",
                                               leading=10, textColor=colors.HexColor("#1a3c5e")))]
                  for m in metodos]

        data = header + [["─── atributos ───"]] + attrs + [["─── métodos ───"]] + meths
        t = Table(data, colWidths=[2.1 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), tipo_color),
            ("BACKGROUND",    (0, 1), (-1, 1), colors.HexColor("#dddddd")),
            ("BACKGROUND",    (0, len(atributos)+2), (-1, len(atributos)+2), colors.HexColor("#dddddd")),
            ("FONTNAME",      (0, 1), (-1, 1), "Helvetica-BoldOblique"),
            ("FONTSIZE",      (0, 1), (-1, 1), 7),
            ("FONTNAME",      (0, len(atributos)+2), (-1, len(atributos)+2), "Helvetica-BoldOblique"),
            ("FONTSIZE",      (0, len(atributos)+2), (-1, len(atributos)+2), 7),
            ("BOX",           (0, 0), (-1, -1), 1, tipo_color),
            ("INNERGRID",     (0, 0), (-1, -1), 0.3, colors.HexColor("#cccccc")),
            ("TOPPADDING",    (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ]))
        return t

    # Clase abstracta Empleado
    emp = clase_box(
        "«abstract» Empleado", COLOR_ABC,
        ["numero_empleado: str", "nombre_completo: str", "fecha_nacimiento: date",
         "direccion: str", "correo: str", "telefono: str",
         "salario: float", "puesto: str", "departamento: str",
         "fecha_contratacion: date", "dia_descanso: str"],
        ["+ calcular_edad(): int", "+ calcular_antiguedad(): int",
         "+ calcular_meses_laborados(): int",
         "# get_tipo_empleado(): str  «abstract»",
         "# calcular_dias_extra(a): int  «abstract»",
         "# a_csv(): str  «abstract»"]
    )

    sind = clase_box(
        "EmpleadoSindicalizado", COLOR_SUB,
        ["nombre_sindicato: str"],
        ["+ get_tipo_empleado(): str", "+ calcular_dias_extra(a): int"]
    )
    conf = clase_box(
        "EmpleadoConfianza", COLOR_SUB,
        ["nivel_confianza: str", "jornada: str"],
        ["+ get_tipo_empleado(): str", "+ calcular_dias_extra(a): int"]
    )
    temp = clase_box(
        "EmpleadoTemporal", COLOR_SUB,
        ["tipo_contrato: str", "fecha_inicio_contrato: date", "fecha_fin_contrato: date"],
        ["+ get_tipo_empleado(): str", "+ calcular_dias_extra(a): int",
         "+ calcular_vacaciones_proporcionales(d): int"]
    )
    cat = clase_box(
        "CatalogoVacaciones", COLOR_SERV,
        ["_TABLA: list[(int,int,int)]"],
        ["+ obtener_dias(antiguedad): int", "+ mostrar(): void", "+ a_csv(): list"]
    )
    vac = clase_box(
        "VacacionesEmpleado", COLOR_ENTIDAD,
        ["numero_empleado: str", "year: int", "dias_otorgados_ley: int",
         "dias_extra: int", "dias_totales: int",
         "dias_utilizados: int", "habilitado: bool", "dias_restantes: int"],
        ["+ usar_dias(n): void", "+ devolver_dias(n): void", "+ a_csv(): str"]
    )
    sol = clase_box(
        "SolicitudVacaciones", COLOR_ENTIDAD,
        ["numero_solicitud: str", "numero_empleado: str",
         "fecha_solicitud: date", "fecha_inicio: date",
         "fecha_fin: date", "dias_solicitados: int", "estatus: str"],
        ["+ cambiar_estatus(e): void", "+ a_csv(): str",
         "@ calcular_fecha_fin(f,d): date",
         "@ validar_anticipacion(fs,fi): bool"]
    )
    sis = clase_box(
        "SistemaVacaciones", COLOR_SERV,
        ["empleados: list", "catalogo: CatalogoVacaciones",
         "vacaciones: dict", "solicitudes: list"],
        ["+ cargar_archivos(): void", "+ guardar_archivos(): void",
         "+ alta_empleado(tipo, datos): Empleado",
         "+ baja_empleado(num): void",
         "+ registrar_solicitud(num,fi,d): Solicitud",
         "+ consultar_empleados(c,v): list",
         "+ consultar_vacaciones(c,v1,v2): list",
         "+ reporte_ejecutivo(): void"]
    )

    leyenda = [
        [Paragraph("<b>Leyenda de colores</b>",
                   ParagraphStyle("l", fontSize=8, fontName="Helvetica-Bold"))],
        [Paragraph("  Azul oscuro: clase abstracta base",
                   ParagraphStyle("l2", fontSize=8, fontName="Helvetica",
                                  textColor=COLOR_ABC))],
        [Paragraph("  Azul medio: subclases concretas",
                   ParagraphStyle("l3", fontSize=8, fontName="Helvetica",
                                  textColor=COLOR_SUB))],
        [Paragraph("  Verde: clases de servicio/sistema",
                   ParagraphStyle("l4", fontSize=8, fontName="Helvetica",
                                  textColor=COLOR_SERV))],
        [Paragraph("  Morado: clases de entidad/estado",
                   ParagraphStyle("l5", fontSize=8, fontName="Helvetica",
                                  textColor=COLOR_ENTIDAD))],
    ]
    tl = Table(leyenda, colWidths=[2.5*inch])
    tl.setStyle(TableStyle([
        ("BOX", (0,0),(-1,-1), 0.5, colors.HexColor("#999999")),
        ("TOPPADDING",(0,0),(-1,-1),2), ("BOTTOMPADDING",(0,0),(-1,-1),2),
        ("LEFTPADDING",(0,0),(-1,-1),5),
    ]))

    # Layout del diagrama
    layout = Table(
        [
            [emp, "", ""],
            ["▼ hereda", "▼ hereda", "▼ hereda"],
            [sind, conf, temp],
            ["", "", ""],
            [cat, vac, sol],
            ["", sis, ""],
        ],
        colWidths=[2.2*inch, 2.2*inch, 2.2*inch]
    )
    layout.setStyle(TableStyle([
        ("ALIGN",   (0,0),(-1,-1), "CENTER"),
        ("VALIGN",  (0,0),(-1,-1), "TOP"),
        ("FONTNAME",(0,1),(-1,1), "Helvetica-Bold"),
        ("FONTSIZE",(0,1),(-1,1), 9),
        ("TEXTCOLOR",(0,1),(-1,1), COLOR_ABC),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("SPAN", (0,0),(0,0)),
    ]))

    story.append(layout)
    story.append(Spacer(1, 0.1*inch))
    story.append(tl)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Nota: @ = método estático. El patrón de herencia es simple (una rama por tipo de empleado). "
        "SistemaVacaciones agrega instancias de CatalogoVacaciones y contiene listas de los demás objetos.",
        estilos["nota"]
    ))


# ─────────────────────────── SECCIÓN 2: REPORTE EJECUTIVO ──────────────────

def seccion_reporte(story, estilos, sistema):
    S = estilos
    hoy = date.today()

    story.append(Paragraph("2. REPORTE EJECUTIVO — ESTATUS INICIAL", S["seccion"]))
    story.append(Paragraph(
        f"Información consolidada al {hoy.strftime('%d de %B de %Y')}. "
        "Generada automáticamente a partir de los archivos de datos del sistema.",
        S["nota"]
    ))
    story.append(Spacer(1, 0.1 * inch))

    emps = sistema.empleados
    vacs = sistema.vacaciones
    sols = sistema.solicitudes

    sinds = [e for e in emps if isinstance(e, EmpleadoSindicalizado)]
    confs = [e for e in emps if isinstance(e, EmpleadoConfianza)]
    temps = [e for e in emps if isinstance(e, EmpleadoTemporal)]

    # 2.1 Resumen general
    story.append(Paragraph("2.1 Resumen General de Empleados", S["subseccion"]))
    resumen = [
        ["Indicador", "Valor"],
        ["Total de empleados activos",         str(len(emps))],
        ["Empleados sindicalizados",           str(len(sinds))],
        ["Empleados de confianza",             str(len(confs))],
        ["Empleados temporales",               str(len(temps))],
        ["Empleados con vacaciones habilitadas",
         str(sum(1 for v in vacs.values() if v.habilitado))],
        ["Empleados sin vacaciones (< 1 año)",
         str(sum(1 for v in vacs.values() if not v.habilitado))],
        ["Total solicitudes registradas",      str(len(sols))],
    ]
    story.append(tabla(resumen, [4*inch, 2*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.2 Empleados de mayor antigüedad (top 10)
    story.append(Paragraph("2.2 Empleados con Mayor Antigüedad (Top 10)", S["subseccion"]))
    top10 = sorted(emps, key=lambda e: e.calcular_antiguedad(), reverse=True)[:10]
    top_data = [["#", "Nombre", "Tipo", "Departamento", "Contratación", "Antigüedad"]]
    for i, emp in enumerate(top10, 1):
        top_data.append([
            str(i), emp.nombre_completo, emp.get_tipo_empleado(),
            emp.departamento, str(emp.fecha_contratacion),
            f"{emp.calcular_antiguedad()} año(s)"
        ])
    story.append(tabla(top_data, [0.3*inch, 1.7*inch, 0.9*inch, 1.3*inch, 0.95*inch, 0.85*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.3 Distribución de vacaciones
    story.append(Paragraph("2.3 Distribución de Días de Vacaciones", S["subseccion"]))
    dias_data = {}
    for emp in emps:
        t_emp = emp.get_tipo_empleado()
        v = vacs.get(emp.numero_empleado)
        if v and v.habilitado:
            if t_emp not in dias_data:
                dias_data[t_emp] = {"ley": 0, "extra": 0, "usados": 0, "restantes": 0, "n": 0}
            dias_data[t_emp]["ley"]       += v.dias_otorgados_ley
            dias_data[t_emp]["extra"]     += v.dias_extra
            dias_data[t_emp]["usados"]    += v.dias_utilizados
            dias_data[t_emp]["restantes"] += v.dias_restantes
            dias_data[t_emp]["n"]         += 1

    vac_table = [["Tipo", "Empleados", "Total días\notorgados", "Total días\nextra",
                  "Total días\nusados", "Total días\nrestantes", "Promedio\nrestantes"]]
    for tipo, d in sorted(dias_data.items()):
        prom = round(d["restantes"] / d["n"], 1) if d["n"] else 0
        vac_table.append([
            tipo, str(d["n"]),
            str(d["ley"]), str(d["extra"]),
            str(d["usados"]), str(d["restantes"]), str(prom)
        ])
    story.append(tabla(vac_table, [1.1*inch, 0.8*inch, 1*inch, 0.8*inch, 0.85*inch, 0.95*inch, 0.9*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.4 Solicitudes por tipo y estatus
    story.append(Paragraph("2.4 Solicitudes de Vacaciones por Tipo de Empleado y Estatus", S["subseccion"]))
    mapa = {emp.numero_empleado: emp for emp in emps}
    conteo = {}
    for sol in sols:
        emp = mapa.get(sol.numero_empleado)
        tipo = emp.get_tipo_empleado() if emp else "Desconocido"
        key = (tipo, sol.estatus)
        conteo[key] = conteo.get(key, 0) + 1

    tipos_sol = sorted({k[0] for k in conteo})
    estatus_list = ["pendiente", "aprobada", "rechazada"]
    sol_table = [["Tipo de empleado"] + [e.capitalize() for e in estatus_list] + ["Total"]]
    totales = {e: 0 for e in estatus_list}
    for tipo in tipos_sol:
        fila = [tipo]
        subtotal = 0
        for est in estatus_list:
            v = conteo.get((tipo, est), 0)
            fila.append(str(v))
            totales[est] += v
            subtotal += v
        fila.append(str(subtotal))
        sol_table.append(fila)
    fila_total = ["TOTAL"] + [str(totales[e]) for e in estatus_list] + [str(len(sols))]
    sol_table.append(fila_total)
    t_sol = tabla(sol_table, [1.6*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1*inch])
    # Fila de totales en negrita
    t_sol._argH[-1] = 0.3*inch
    story.append(t_sol)
    story.append(Spacer(1, 0.15*inch))

    # 2.5 Sindicatos
    story.append(Paragraph("2.5 Distribución por Sindicato", S["subseccion"]))
    sind_count = {}
    for emp in sinds:
        sind_count[emp.nombre_sindicato] = sind_count.get(emp.nombre_sindicato, 0) + 1
    sind_table = [["Sindicato", "Empleados", "% del total sindicalizado"]]
    for sind, cnt in sorted(sind_count.items(), key=lambda x: -x[1]):
        pct = round(cnt / len(sinds) * 100, 1) if sinds else 0
        sind_table.append([sind, str(cnt), f"{pct}%"])
    story.append(tabla(sind_table, [2.5*inch, 1.5*inch, 2.5*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.6 Nivel de confianza
    story.append(Paragraph("2.6 Empleados de Confianza por Nivel y Jornada", S["subseccion"]))
    conf_data = {}
    for emp in confs:
        key = (emp.nivel_confianza.capitalize(), emp.jornada.replace("_", " ").capitalize())
        conf_data[key] = conf_data.get(key, 0) + 1
    conf_table = [["Nivel", "Jornada", "Empleados"]]
    for (niv, jor), cnt in sorted(conf_data.items()):
        conf_table.append([niv, jor, str(cnt)])
    story.append(tabla(conf_table, [2*inch, 2*inch, 2*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.7 Contratos temporales
    story.append(Paragraph("2.7 Empleados Temporales por Tipo de Contrato", S["subseccion"]))
    ctto_count = {}
    for emp in temps:
        ctto_count[emp.tipo_contrato.capitalize()] = ctto_count.get(emp.tipo_contrato.capitalize(), 0) + 1
    ctto_table = [["Tipo de contrato", "Empleados", "% del total temporal"]]
    for ctto, cnt in sorted(ctto_count.items(), key=lambda x: -x[1]):
        pct = round(cnt / len(temps) * 100, 1) if temps else 0
        ctto_table.append([ctto, str(cnt), f"{pct}%"])
    story.append(tabla(ctto_table, [2.5*inch, 1.5*inch, 2.5*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.8 Top 5 empleados con más días restantes
    story.append(Paragraph("2.8 Top 10 Empleados con Más Días de Vacaciones Disponibles", S["subseccion"]))
    pares_vac = [(emp, vacs[emp.numero_empleado])
                 for emp in emps
                 if emp.numero_empleado in vacs and vacs[emp.numero_empleado].habilitado]
    top_vac = sorted(pares_vac, key=lambda x: x[1].dias_restantes, reverse=True)[:10]
    tv_data = [["Nombre", "Tipo", "Departamento", "Días totales", "Días usados", "Días restantes"]]
    for emp, vac in top_vac:
        tv_data.append([
            emp.nombre_completo, emp.get_tipo_empleado(), emp.departamento,
            str(vac.dias_totales), str(vac.dias_utilizados), str(vac.dias_restantes)
        ])
    story.append(tabla(tv_data, [1.8*inch, 0.9*inch, 1.3*inch, 0.85*inch, 0.85*inch, 0.9*inch]))
    story.append(Spacer(1, 0.15*inch))

    # 2.9 Conclusiones
    story.append(Paragraph("2.9 Conclusiones y Observaciones", S["subseccion"]))
    hab = sum(1 for v in vacs.values() if v.habilitado)
    pct_hab = round(hab / len(emps) * 100, 1) if emps else 0
    pend = sum(1 for s in sols if s.estatus == "pendiente")
    apro = sum(1 for s in sols if s.estatus == "aprobada")
    rech = sum(1 for s in sols if s.estatus == "rechazada")

    conclusiones = [
        f"El {pct_hab}% de los empleados ({hab} de {len(emps)}) ya tienen vacaciones habilitadas, "
        f"lo que indica una plantilla con buena estabilidad laboral.",
        f"El {round(pend/len(sols)*100,1) if sols else 0}% de las solicitudes ({pend}) están pendientes de revisión, "
        f"requiriendo atención prioritaria del área de Recursos Humanos.",
        f"Las solicitudes aprobadas representan el {round(apro/len(sols)*100,1) if sols else 0}% ({apro}) "
        f"y las rechazadas el {round(rech/len(sols)*100,1) if sols else 0}% ({rech}).",
        f"La plantilla está equilibrada: {len(sinds)} sindicalizados, {len(confs)} de confianza y "
        f"{len(temps)} temporales, representando cada grupo el 33.3% del total.",
    ]
    for obs in conclusiones:
        story.append(Paragraph(f"• {obs}", S["bullet"]))


# ─────────────────────────── MAIN ──────────────────────────────────────────

def generar_pdf():
    ruta_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "Documento_Proyecto_Final.pdf")

    print("Cargando datos del sistema...")
    sistema = SistemaVacaciones()
    sistema.cargar_archivos()

    print("Generando PDF...")
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=0.8*inch, leftMargin=0.8*inch,
        topMargin=0.8*inch, bottomMargin=0.8*inch,
        title="Sistema de Administración de Vacaciones — Galactic Force Solutions",
        author="Equipo de Programación, Facultad de Ciencias UNAM",
    )

    estilos = crear_estilos()
    story = []

    portada(story, estilos)
    seccion_metodologia(story, estilos)
    seccion_reporte(story, estilos, sistema)

    doc.build(story)
    print(f"PDF generado: {ruta_pdf}")
    return ruta_pdf


if __name__ == "__main__":
    generar_pdf()
