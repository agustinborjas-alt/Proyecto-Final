"""Módulo para lectura y escritura de los archivos CSV del sistema."""

import os
from datetime import date, datetime

from empleado_sindicalizado import EmpleadoSindicalizado
from empleado_confianza import EmpleadoConfianza
from empleado_temporal import EmpleadoTemporal
from vacaciones_empleado import VacacionesEmpleado
from solicitud_vacaciones import SolicitudVacaciones


DIRECTORIO_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

ARCHIVOS = {
    "empleados":      os.path.join(DIRECTORIO_DATOS, "empleados.csv"),
    "catalogo":       os.path.join(DIRECTORIO_DATOS, "catalogo.csv"),
    "vacaciones":     os.path.join(DIRECTORIO_DATOS, "vacaciones_empleados.csv"),
    "solicitudes":    os.path.join(DIRECTORIO_DATOS, "solicitudes_empleados.csv"),
    "vac_anteriores": os.path.join(DIRECTORIO_DATOS, "vacaciones_anteriores.csv"),
    "emp_borrados":   os.path.join(DIRECTORIO_DATOS, "empleados_borrados.csv"),
    "sol_borradas":   os.path.join(DIRECTORIO_DATOS, "solicitudes_borradas.csv"),
}


def _fecha(texto):
    """Convierte una cadena 'YYYY-MM-DD' a objeto date.

    Args:
        texto (str): Fecha en formato ISO.

    Returns:
        date: Objeto date.
    """
    return datetime.strptime(texto.strip(), "%Y-%m-%d").date()


def _bool(texto):
    """Convierte una cadena a booleano.

    Args:
        texto (str): Valor textual del booleano.

    Returns:
        bool: Valor booleano correspondiente.
    """
    return texto.strip().lower() in ("true", "1", "sí", "si")


# ─────────────────────────── CARGA ─────────────────────────────────────────

def cargar_empleados():
    """Lee empleados.csv y retorna la lista de empleados.

    Returns:
        list: Lista de objetos Empleado (y subclases).
    """
    empleados = []
    ruta = ARCHIVOS["empleados"]
    if not os.path.exists(ruta):
        return empleados

    with open(ruta, encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            p = linea.split(",")
            tipo = p[0].strip().upper()
            try:
                base = dict(
                    numero_empleado=p[1].strip(),
                    nombre_completo=p[2].strip(),
                    fecha_nacimiento=_fecha(p[3]),
                    direccion=p[4].strip(),
                    correo=p[5].strip(),
                    telefono=p[6].strip(),
                    salario=p[7].strip(),
                    puesto=p[8].strip(),
                    departamento=p[9].strip(),
                    fecha_contratacion=_fecha(p[10]),
                    dia_descanso=p[11].strip(),
                )
                if tipo == "S":
                    emp = EmpleadoSindicalizado(**base, nombre_sindicato=p[12].strip())
                elif tipo == "C":
                    emp = EmpleadoConfianza(**base,
                                            nivel_confianza=p[12].strip(),
                                            jornada=p[13].strip())
                elif tipo == "T":
                    emp = EmpleadoTemporal(**base,
                                           tipo_contrato=p[12].strip(),
                                           fecha_inicio_contrato=_fecha(p[13]),
                                           fecha_fin_contrato=_fecha(p[14]))
                else:
                    print(f"  [Aviso] Línea {num_linea}: tipo desconocido '{tipo}', omitida.")
                    continue
                empleados.append(emp)
            except (IndexError, ValueError) as e:
                print(f"  [Aviso] Línea {num_linea} en empleados.csv ignorada: {e}")
    return empleados


def cargar_vacaciones():
    """Lee vacaciones_empleados.csv y retorna un diccionario de vacaciones.

    Returns:
        dict: {numero_empleado: VacacionesEmpleado}
    """
    vacaciones = {}
    ruta = ARCHIVOS["vacaciones"]
    if not os.path.exists(ruta):
        return vacaciones

    with open(ruta, encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            p = linea.split(",")
            try:
                vac = VacacionesEmpleado(
                    numero_empleado=p[0].strip(),
                    year=p[1].strip(),
                    dias_otorgados_ley=p[2].strip(),
                    dias_extra=p[3].strip(),
                    dias_totales=p[4].strip(),
                    dias_utilizados=p[5].strip(),
                    habilitado=p[6].strip(),
                )
                vacaciones[vac.numero_empleado] = vac
            except (IndexError, ValueError) as e:
                print(f"  [Aviso] Línea {num_linea} en vacaciones_empleados.csv ignorada: {e}")
    return vacaciones


def cargar_solicitudes():
    """Lee solicitudes_empleados.csv y retorna la lista de solicitudes.

    Returns:
        list: Lista de objetos SolicitudVacaciones.
    """
    solicitudes = []
    ruta = ARCHIVOS["solicitudes"]
    if not os.path.exists(ruta):
        return solicitudes

    with open(ruta, encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea:
                continue
            p = linea.split(",")
            try:
                sol = SolicitudVacaciones(
                    numero_solicitud=p[0].strip(),
                    numero_empleado=p[1].strip(),
                    fecha_solicitud=_fecha(p[2]),
                    fecha_inicio=_fecha(p[3]),
                    fecha_fin=_fecha(p[4]),
                    dias_solicitados=p[5].strip(),
                    estatus=p[6].strip(),
                )
                solicitudes.append(sol)
            except (IndexError, ValueError) as e:
                print(f"  [Aviso] Línea {num_linea} en solicitudes_empleados.csv ignorada: {e}")
    return solicitudes


# ─────────────────────────── GUARDADO ──────────────────────────────────────

def guardar_empleados(empleados):
    """Escribe la lista completa de empleados en empleados.csv.

    Args:
        empleados (list): Lista de objetos Empleado.
    """
    with open(ARCHIVOS["empleados"], "w", encoding="utf-8") as f:
        for emp in empleados:
            f.write(emp.a_csv() + "\n")


def guardar_vacaciones(vacaciones_dict):
    """Escribe todos los registros de vacaciones en vacaciones_empleados.csv.

    Args:
        vacaciones_dict (dict): {numero_empleado: VacacionesEmpleado}
    """
    with open(ARCHIVOS["vacaciones"], "w", encoding="utf-8") as f:
        for vac in vacaciones_dict.values():
            f.write(vac.a_csv() + "\n")


def guardar_solicitudes(solicitudes):
    """Escribe todas las solicitudes en solicitudes_empleados.csv.

    Args:
        solicitudes (list): Lista de objetos SolicitudVacaciones.
    """
    with open(ARCHIVOS["solicitudes"], "w", encoding="utf-8") as f:
        for sol in solicitudes:
            f.write(sol.a_csv() + "\n")


def guardar_catalogo(catalogo):
    """Escribe el catálogo de vacaciones en catalogo.csv.

    Args:
        catalogo (CatalogoVacaciones): Instancia del catálogo.
    """
    with open(ARCHIVOS["catalogo"], "w", encoding="utf-8") as f:
        for linea in catalogo.a_csv():
            f.write(linea + "\n")


# ─────────────────────────── ARCHIVADO ─────────────────────────────────────

def archivar_vacaciones_anteriores(vacaciones_list):
    """Agrega vacaciones reseteadas a vacaciones_anteriores.csv (append).

    Args:
        vacaciones_list (list): Lista de VacacionesEmpleado a archivar.
    """
    with open(ARCHIVOS["vac_anteriores"], "a", encoding="utf-8") as f:
        for vac in vacaciones_list:
            f.write(vac.a_csv() + "\n")


def archivar_empleado_borrado(empleado):
    """Agrega un empleado eliminado a empleados_borrados.csv (append).

    Args:
        empleado (Empleado): Empleado eliminado.
    """
    with open(ARCHIVOS["emp_borrados"], "a", encoding="utf-8") as f:
        f.write(empleado.a_csv() + f",{date.today()}\n")


def archivar_solicitud_borrada(solicitud):
    """Agrega una solicitud eliminada a solicitudes_borradas.csv (append).

    Args:
        solicitud (SolicitudVacaciones): Solicitud eliminada.
    """
    with open(ARCHIVOS["sol_borradas"], "a", encoding="utf-8") as f:
        f.write(solicitud.a_csv() + f",{date.today()}\n")


def inicializar_archivos():
    """Crea el directorio de datos y los archivos de trazabilidad si no existen."""
    os.makedirs(DIRECTORIO_DATOS, exist_ok=True)
    for clave in ("emp_borrados", "sol_borradas", "vac_anteriores"):
        ruta = ARCHIVOS[clave]
        if not os.path.exists(ruta):
            open(ruta, "w", encoding="utf-8").close()
