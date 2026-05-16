"""Script para generar 1500 empleados de prueba (500 por tipo) y sus archivos CSV."""

import random
import os
from datetime import date, timedelta

random.seed(42)

DIRECTORIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")

# ── Datos de muestra ────────────────────────────────────────────────────────

NOMBRES = [
    "Ana", "Carlos", "Lucía", "Roberto", "Patricia", "Miguel", "Sandra",
    "Eduardo", "Diana", "Fernando", "Valeria", "Javier", "Karla", "Andrés",
    "Sofía", "Héctor", "Mónica", "Ricardo", "Gabriela", "Alejandro",
    "Fernanda", "Jorge", "Claudia", "Raúl", "Leticia", "Arturo", "Verónica",
    "Sergio", "Mariana", "Pablo", "Esperanza", "Gustavo", "Adriana", "Enrique",
    "Silvia", "Daniel", "Yolanda", "Ignacio", "Berenice", "Alfredo",
    "Liliana", "Ernesto", "Norma", "Víctor", "Ángela", "Salvador", "Irene",
    "Gerardo", "Alicia", "Hugo",
]

APELLIDOS = [
    "Pérez", "López", "García", "Martínez", "Rodríguez", "González",
    "Sánchez", "Ramírez", "Torres", "Flores", "Rivera", "Morales",
    "Jiménez", "Vargas", "Reyes", "Cruz", "Mendoza", "Ortiz", "Castillo",
    "Gutiérrez", "Ramos", "Herrera", "Medina", "Aguilar", "Vega",
    "Chavez", "Rojas", "Núñez", "Díaz", "Muñoz", "Alvarez", "Ruiz",
    "Romero", "Contreras", "Guerrero", "Campos", "Espinoza", "Delgado",
    "Mejía", "Santiago", "Fuentes", "Ríos", "Lara", "Mora", "Palacios",
    "Salinas", "Figueroa", "Cervantes", "Soto", "Ibarra",
]

PUESTOS = [
    "Analista", "Técnico", "Auxiliar", "Coordinador", "Operador",
    "Especialista", "Supervisor", "Asistente", "Gestor", "Consultor",
    "Desarrollador", "Diseñador", "Contador", "Auditor", "Representante",
]

DEPARTAMENTOS = [
    "Recursos Humanos", "Sistemas", "Contabilidad", "Producción",
    "Logística", "Administración", "Marketing", "Finanzas",
    "Operaciones", "Ventas", "Calidad", "Soporte Técnico",
]

DIAS_DESCANSO = ["Sábado", "Domingo"]

SINDICATOS = ["STIDC", "SUTERM", "CTM", "CROC", "CROM", "STRM", "SNTSS"]

NIVELES = ["junior", "senior", "directivo"]
JORNADAS = ["completa", "medio_tiempo"]
CONTRATOS = ["obra", "temporada", "interinato"]


def fecha_aleatoria(anio_min, anio_max):
    """Genera una fecha aleatoria entre dos años."""
    inicio = date(anio_min, 1, 1)
    fin = date(anio_max, 12, 31)
    delta = (fin - inicio).days
    return inicio + timedelta(days=random.randint(0, delta))


def nombre_completo():
    """Genera un nombre completo aleatorio."""
    return f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}"


def correo(nombre, numero):
    """Genera un correo único basado en nombre y número."""
    n = nombre.lower().split()[0]
    return f"{n}.{numero}@gfs.mx"


def generar_empleados():
    """Genera 1500 empleados: 500 sindicalizados, 500 confianza, 500 temporales."""
    lineas = []
    hoy = date.today()

    for i in range(1, 1501):
        num = f"EMP{1000 + i}"
        nombre = nombre_completo()
        nac = fecha_aleatoria(1965, 2000)
        direccion = f"Calle {random.choice(APELLIDOS)} #{random.randint(1, 999)}"
        email = correo(nombre, i)
        tel = f"55{random.randint(10000000, 99999999)}"
        salario = round(random.uniform(10000, 70000), 2)
        puesto = random.choice(PUESTOS)
        depto = random.choice(DEPARTAMENTOS)
        contratacion = fecha_aleatoria(2005, 2024)
        descanso = random.choice(DIAS_DESCANSO)

        if i <= 500:
            # Sindicalizado
            sindicato = random.choice(SINDICATOS)
            lineas.append(
                f"S,{num},{nombre},{nac},{direccion},{email},{tel},"
                f"{salario},{puesto},{depto},{contratacion},{descanso},{sindicato}"
            )
        elif i <= 1000:
            # Confianza
            nivel = random.choice(NIVELES)
            jornada = random.choice(JORNADAS)
            lineas.append(
                f"C,{num},{nombre},{nac},{direccion},{email},{tel},"
                f"{salario},{puesto},{depto},{contratacion},{descanso},{nivel},{jornada}"
            )
        else:
            # Temporal
            tipo_ctto = random.choice(CONTRATOS)
            inicio_ctto = contratacion
            fin_ctto = inicio_ctto + timedelta(days=random.randint(180, 730))
            lineas.append(
                f"T,{num},{nombre},{nac},{direccion},{email},{tel},"
                f"{salario},{puesto},{depto},{contratacion},{descanso},"
                f"{tipo_ctto},{inicio_ctto},{fin_ctto}"
            )

    return lineas


def generar_vacaciones(empleados_csv):
    """Genera el archivo vacaciones_empleados.csv coherente con los empleados."""
    from catalogo_vacaciones import CatalogoVacaciones
    from empleado_sindicalizado import EmpleadoSindicalizado
    from empleado_confianza import EmpleadoConfianza
    from empleado_temporal import EmpleadoTemporal
    from datetime import datetime

    catalogo = CatalogoVacaciones()
    hoy = date.today()
    lineas = []

    for linea in empleados_csv:
        p = linea.split(",")
        tipo = p[0]
        num = p[1]
        nac = datetime.strptime(p[3], "%Y-%m-%d").date()
        contratacion = datetime.strptime(p[10], "%Y-%m-%d").date()

        # Calcular antigüedad real
        antiguedad = hoy.year - contratacion.year - (
            (hoy.month, hoy.day) < (contratacion.month, contratacion.day)
        )
        meses = (hoy.year - contratacion.year) * 12 + (hoy.month - contratacion.month)

        if antiguedad < 1:
            lineas.append(f"{num},{hoy.year},0,0,0,0,False")
            continue

        dias_ley = catalogo.obtener_dias(antiguedad)

        if tipo == "S":
            dias_extra = 5 if antiguedad >= 2 else 0
            dias_totales = dias_ley + dias_extra
        elif tipo == "C":
            nivel = p[12].strip()
            jornada = p[13].strip()
            aplica = (antiguedad >= 2
                      and jornada == "completa"
                      and nivel in ("senior", "directivo"))
            dias_extra = 3 if aplica else 0
            dias_totales = dias_ley + dias_extra
        else:  # T
            dias_extra = 0
            dias_totales = int(dias_ley * (meses / 12))

        dias_usados = random.randint(0, min(dias_totales, dias_totales // 2))
        lineas.append(
            f"{num},{hoy.year},{dias_ley},{dias_extra},{dias_totales},{dias_usados},True"
        )

    return lineas


def generar_solicitudes(empleados_csv, vacaciones_csv):
    """Genera solicitudes de vacaciones para ~30% de los empleados."""
    from datetime import datetime

    hoy = date.today()
    vac_dict = {}
    for v in vacaciones_csv:
        p = v.split(",")
        vac_dict[p[0]] = {
            "dias_totales": int(p[4]),
            "dias_usados": int(p[5]),
            "habilitado": p[6].strip() == "True",
        }

    lineas = []
    contador = 1
    estatus_opciones = ["aprobada", "aprobada", "pendiente", "rechazada"]

    for i, linea in enumerate(empleados_csv):
        # Solo ~30% de empleados tienen solicitudes
        if random.random() > 0.30:
            continue
        num = linea.split(",")[1]
        vac = vac_dict.get(num)
        if not vac or not vac["habilitado"] or vac["dias_totales"] == 0:
            continue

        dias_disp = vac["dias_totales"] - vac["dias_usados"]
        if dias_disp <= 0:
            continue

        dias_sol = random.randint(1, min(dias_disp, 10))
        dias_atras = random.randint(30, 200)
        fecha_sol = hoy - timedelta(days=dias_atras)
        fecha_ini = fecha_sol + timedelta(days=random.randint(7, 30))
        # Calcular fecha fin (días hábiles)
        contados = 0
        dia = fecha_ini
        while contados < dias_sol:
            if dia.weekday() < 5:
                contados += 1
            if contados < dias_sol:
                dia += timedelta(days=1)
        fecha_fin = dia
        estatus = random.choice(estatus_opciones)
        num_sol = f"SOL{contador:04d}"
        contador += 1
        lineas.append(
            f"{num_sol},{num},{fecha_sol},{fecha_ini},{fecha_fin},{dias_sol},{estatus}"
        )

    return lineas


if __name__ == "__main__":
    os.makedirs(DIRECTORIO, exist_ok=True)

    print("Generando 1500 empleados...")
    empleados = generar_empleados()
    with open(os.path.join(DIRECTORIO, "empleados.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(empleados) + "\n")
    print(f"  empleados.csv: {len(empleados)} registros")

    print("Generando vacaciones...")
    vacaciones = generar_vacaciones(empleados)
    with open(os.path.join(DIRECTORIO, "vacaciones_empleados.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(vacaciones) + "\n")
    print(f"  vacaciones_empleados.csv: {len(vacaciones)} registros")

    print("Generando solicitudes...")
    solicitudes = generar_solicitudes(empleados, vacaciones)
    with open(os.path.join(DIRECTORIO, "solicitudes_empleados.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(solicitudes) + "\n")
    print(f"  solicitudes_empleados.csv: {len(solicitudes)} registros")

    print("\nDatos generados correctamente.")
