"""Punto de entrada del Sistema de Administración de Vacaciones — Galactic Force Solutions."""

from datetime import datetime, date
from sistema_vacaciones import SistemaVacaciones


def _separador(titulo=""):
    """Imprime una línea separadora con título opcional."""
    if titulo:
        print(f"\n{'─'*10} {titulo} {'─'*10}")
    else:
        print("─" * 50)


def _pedir_fecha(mensaje):
    """Solicita una fecha al usuario en formato YYYY-MM-DD.

    Args:
        mensaje (str): Texto a mostrar al usuario.

    Returns:
        date: Fecha ingresada, o None si el usuario cancela.
    """
    while True:
        texto = input(f"  {mensaje} (YYYY-MM-DD, Enter=cancelar): ").strip()
        if not texto:
            return None
        try:
            return datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            print("  [Error] Formato de fecha inválido. Use YYYY-MM-DD.")


def _pedir_entero(mensaje, minimo=1):
    """Solicita un número entero al usuario.

    Args:
        mensaje (str): Texto a mostrar.
        minimo (int): Valor mínimo aceptable.

    Returns:
        int: Número ingresado, o None si el usuario cancela.
    """
    while True:
        texto = input(f"  {mensaje} (Enter=cancelar): ").strip()
        if not texto:
            return None
        try:
            valor = int(texto)
            if valor >= minimo:
                return valor
            print(f"  [Error] El valor debe ser al menos {minimo}.")
        except ValueError:
            print("  [Error] Ingrese un número entero.")


def _pedir_opcion(opciones, mensaje="Seleccione una opción"):
    """Solicita al usuario que seleccione una opción de una lista.

    Args:
        opciones (list[str]): Opciones disponibles.
        mensaje (str): Texto de la pregunta.

    Returns:
        str: La opción seleccionada en minúsculas.
    """
    for i, op in enumerate(opciones, 1):
        print(f"    {i}. {op}")
    while True:
        sel = input(f"  {mensaje}: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(opciones):
            return opciones[int(sel) - 1].lower()
        print(f"  [Error] Opción inválida. Ingrese un número del 1 al {len(opciones)}.")


def _mostrar_resultado_empleados(empleados):
    """Imprime una lista de empleados agrupados por tipo.

    Args:
        empleados (list): Lista de objetos Empleado.
    """
    if not empleados:
        print("  Sin resultados.")
        return
    grupos = {}
    for emp in empleados:
        t = emp.get_tipo_empleado()
        grupos.setdefault(t, []).append(emp)
    for tipo, lista in sorted(grupos.items()):
        _separador(f"Empleados {tipo}s")
        for emp in sorted(lista, key=lambda e: e.nombre_completo):
            emp.mostrar_info()
            print()


def _mostrar_resultado_vacaciones(pares):
    """Imprime pares (empleado, vacaciones) agrupados por tipo de empleado.

    Args:
        pares (list): Lista de tuplas (Empleado, VacacionesEmpleado).
    """
    if not pares:
        print("  Sin resultados.")
        return
    grupos = {}
    for emp, vac in pares:
        t = emp.get_tipo_empleado()
        grupos.setdefault(t, []).append((emp, vac))
    for tipo, lista in sorted(grupos.items()):
        _separador(f"Vacaciones — {tipo}s")
        for emp, vac in sorted(lista, key=lambda p: p[0].nombre_completo):
            print(f"  [{emp.numero_empleado}] {emp.nombre_completo}")
            vac.mostrar()
            print()


def _mostrar_resultado_solicitudes(pares):
    """Imprime pares (solicitud, empleado) con información detallada.

    Args:
        pares (list): Lista de tuplas (SolicitudVacaciones, Empleado|None).
    """
    if not pares:
        print("  Sin resultados.")
        return
    for sol, emp in pares:
        sol.mostrar()
        if emp:
            antig = emp.calcular_antiguedad()
            print(f"  Empleado      : {emp.nombre_completo}")
            print(f"  Puesto        : {emp.puesto}")
            print(f"  Departamento  : {emp.departamento}")
            print(f"  Contratación  : {emp.fecha_contratacion}  ({antig} año(s))")
        print()


# ──────────────────────── SUBMENÚS ─────────────────────────────────────────

def menu_consultar_empleados(sistema):
    """Submenú de consulta de empleados."""
    print("\n  Criterios de búsqueda:")
    criterios = [
        ("numero_empleado", "Número de empleado"),
        ("tipo",            "Tipo de empleado"),
        ("nombre",          "Nombre del empleado"),
        ("puesto",          "Puesto"),
        ("departamento",    "Departamento de adscripción"),
        ("sindicato",       "Nombre del sindicato"),
        ("jornada",         "Tipo de jornada"),
        ("nivel_confianza", "Nivel de confianza"),
        ("tipo_contrato",   "Tipo de contrato"),
        ("dia_descanso",    "Día de descanso"),
        ("edad",            "Edad"),
        ("antiguedad",      "Antigüedad (años)"),
    ]
    for i, (_, etiqueta) in enumerate(criterios, 1):
        print(f"    {i:>2}. {etiqueta}")
    sel = input("  Seleccione criterio (número): ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(criterios)):
        print("  [Error] Opción inválida.")
        return
    clave, etiqueta = criterios[int(sel) - 1]
    valor = input(f"  Ingrese el valor para '{etiqueta}': ").strip()
    if not valor:
        return
    resultado = sistema.consultar_empleados(clave, valor)
    _mostrar_resultado_empleados(resultado)
    print(f"  Total encontrados: {len(resultado)}")


def menu_consultar_vacaciones(sistema):
    """Submenú de consulta de vacaciones."""
    print("\n  Criterios disponibles:")
    criterios = [
        ("tipo_departamento",    "Tipo de empleado  y  Departamento"),
        ("departamento_nivel",   "Departamento  y  Nivel de confianza"),
        ("departamento_contrato","Departamento  y  Tipo de contrato"),
        ("departamento_puesto",  "Departamento  y  Puesto"),
        ("fecha_contratacion",   "Fecha de contratación"),
        ("antiguedad",           "Antigüedad (años)"),
        ("sindicato",            "Nombre del sindicato"),
        ("mes_anio",             "Mes y año de contratación"),
        ("edad_sueldo",          "Edad y sueldo mínimo"),
    ]
    for i, (_, etiqueta) in enumerate(criterios, 1):
        print(f"    {i}. {etiqueta}")
    sel = input("  Seleccione criterio (número): ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(criterios)):
        print("  [Error] Opción inválida.")
        return
    clave, etiqueta = criterios[int(sel) - 1]
    pares_valor = etiqueta.split("  y  ")
    valor1 = input(f"  Valor para '{pares_valor[0].strip()}': ").strip()
    valor2 = None
    if len(pares_valor) > 1:
        valor2 = input(f"  Valor para '{pares_valor[1].strip()}': ").strip()
    resultado = sistema.consultar_vacaciones(clave, valor1, valor2)
    _mostrar_resultado_vacaciones(resultado)
    print(f"  Total encontrados: {len(resultado)}")


def menu_consultar_solicitudes(sistema):
    """Submenú de consulta de solicitudes."""
    print("\n  Criterios disponibles:")
    criterios = [
        ("numero_empleado", "Número de empleado"),
        ("estatus",         "Estatus (pendiente / aprobada / rechazada)"),
        ("tipo",            "Tipo de empleado"),
    ]
    for i, (_, etiqueta) in enumerate(criterios, 1):
        print(f"    {i}. {etiqueta}")
    sel = input("  Seleccione criterio (número): ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(criterios)):
        print("  [Error] Opción inválida.")
        return
    clave, etiqueta = criterios[int(sel) - 1]
    valor = input(f"  Valor para '{etiqueta}': ").strip()
    if not valor:
        return
    resultado = sistema.consultar_solicitudes(clave, valor)
    _mostrar_resultado_solicitudes(resultado)
    print(f"  Total encontradas: {len(resultado)}")


def menu_alta_empleado(sistema):
    """Submenú para dar de alta un nuevo empleado."""
    print("\n  Tipo de empleado:")
    tipo = _pedir_opcion(["Sindicalizado", "Confianza", "Temporal"])
    tipo_clave = tipo[0].upper()  # S, C o T

    print("  Ingrese los datos del empleado:")
    datos = {}
    datos["nombre_completo"]   = input("  Nombre completo    : ").strip()
    datos["fecha_nacimiento"]  = _pedir_fecha("Fecha de nacimiento")
    datos["direccion"]         = input("  Dirección          : ").strip()
    datos["correo"]            = input("  Correo electrónico : ").strip()
    datos["telefono"]          = input("  Teléfono           : ").strip()
    datos["salario"]           = input("  Salario            : ").strip()
    datos["puesto"]            = input("  Puesto             : ").strip()
    datos["departamento"]      = input("  Departamento       : ").strip()
    datos["fecha_contratacion"] = _pedir_fecha("Fecha de contratación")
    datos["dia_descanso"]      = input("  Día de descanso    : ").strip()

    if tipo_clave == "S":
        datos["nombre_sindicato"] = input("  Nombre sindicato   : ").strip()
    elif tipo_clave == "C":
        datos["nivel_confianza"] = _pedir_opcion(
            ["junior", "senior", "directivo"], "Nivel de confianza")
        datos["jornada"] = _pedir_opcion(["completa", "medio_tiempo"], "Jornada")
    elif tipo_clave == "T":
        datos["tipo_contrato"] = _pedir_opcion(
            ["obra", "temporada", "interinato"], "Tipo de contrato")
        datos["fecha_inicio_contrato"] = _pedir_fecha("Fecha inicio de contrato")
        datos["fecha_fin_contrato"]    = _pedir_fecha("Fecha fin de contrato")

    try:
        emp = sistema.alta_empleado(tipo_clave, datos)
        print(f"\n  Empleado dado de alta: {emp.numero_empleado} — {emp.nombre_completo}")
    except (ValueError, TypeError) as e:
        print(f"  [Error] No se pudo dar de alta: {e}")


def menu_actualizar_empleado(sistema):
    """Submenú para actualizar datos de un empleado."""
    num = input("  Número de empleado a actualizar: ").strip()
    try:
        emp = sistema._buscar_empleado(num)
    except ValueError as e:
        print(f"  [Error] {e}")
        return

    emp.mostrar_info()
    print("\n  Campos modificables:")
    campos = emp.campos_modificables()
    for i, c in enumerate(campos, 1):
        print(f"    {i}. {c}")

    sel = input("  Seleccione campo a modificar (número): ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(campos)):
        print("  [Error] Opción inválida.")
        return
    campo = campos[int(sel) - 1]
    nuevo_valor = input(f"  Nuevo valor para '{campo}': ").strip()

    try:
        sistema.actualizar_empleado(num, {campo: nuevo_valor})
        print(f"  Empleado {num} actualizado correctamente.")
    except ValueError as e:
        print(f"  [Error] {e}")


def menu_baja_empleado(sistema):
    """Submenú para dar de baja o eliminar empleados."""
    print("\n  Opciones de eliminación:")
    print("  ── Para un empleado individual ──")
    print("    1. Por número de empleado")
    print("    2. Por nombre (primer coincidencia)")
    print("    3. Por correo electrónico")
    print("  ── Para un grupo de empleados ──")
    print("    4. Por departamento")
    print("    5. Por tipo de empleado")
    print("    6. Por día de descanso")

    sel = input("  Seleccione opción: ").strip()
    if sel in ("1", "2", "3"):
        etiquetas = {
            "1": ("número de empleado", "numero_empleado"),
            "2": ("nombre",             "nombre"),
            "3": ("correo",             "correo"),
        }
        etiqueta, criterio = etiquetas[sel]
        valor = input(f"  Ingrese el {etiqueta}: ").strip()
        encontrados = sistema.consultar_empleados(criterio, valor)
        if not encontrados:
            print("  No se encontraron empleados con ese criterio.")
            return
        emp = encontrados[0]
        emp.mostrar_info()
        confirmacion = input("  ¿Confirma la baja? (s/n): ").strip().lower()
        if confirmacion == "s":
            try:
                sistema.baja_empleado(emp.numero_empleado)
                print(f"  Empleado {emp.numero_empleado} dado de baja.")
            except ValueError as e:
                print(f"  [Error] {e}")
    elif sel in ("4", "5", "6"):
        etiquetas = {
            "4": ("departamento",       "departamento"),
            "5": ("tipo de empleado",   "tipo"),
            "6": ("día de descanso",    "dia_descanso"),
        }
        etiqueta, criterio = etiquetas[sel]
        valor = input(f"  Ingrese el {etiqueta}: ").strip()
        encontrados = sistema.consultar_empleados(criterio, valor)
        if not encontrados:
            print("  No se encontraron empleados.")
            return
        print(f"  Se eliminarán {len(encontrados)} empleado(s):")
        for emp in encontrados:
            print(f"    {emp}")
        confirmacion = input("  ¿Confirma la baja grupal? (s/n): ").strip().lower()
        if confirmacion == "s":
            n = sistema.eliminar_empleado(criterio, valor)
            print(f"  {n} empleado(s) eliminado(s).")
    else:
        print("  [Error] Opción inválida.")


def menu_nueva_solicitud(sistema):
    """Submenú para registrar una nueva solicitud de vacaciones."""
    num = input("  Número de empleado: ").strip()
    fecha_inicio = _pedir_fecha("Fecha de inicio de vacaciones")
    if not fecha_inicio:
        return
    dias = _pedir_entero("Días hábiles solicitados")
    if dias is None:
        return
    try:
        sol = sistema.registrar_solicitud(num, fecha_inicio, dias)
        print(f"\n  Solicitud registrada: {sol.numero_solicitud}")
        print(f"  Inicio: {sol.fecha_inicio}  |  Fin: {sol.fecha_fin}  |  Días: {sol.dias_solicitados}")
    except ValueError as e:
        print(f"  [Error] {e}")


def menu_actualizar_solicitud(sistema):
    """Submenú para actualizar una solicitud pendiente."""
    num_sol = input("  Número de solicitud a actualizar: ").strip()
    nueva_fecha = _pedir_fecha("Nueva fecha de inicio de vacaciones")
    if not nueva_fecha:
        return
    nuevos_dias = _pedir_entero("Nuevo número de días hábiles")
    if nuevos_dias is None:
        return
    try:
        sol = sistema.actualizar_solicitud(num_sol, nueva_fecha, nuevos_dias)
        print(f"  Solicitud {sol.numero_solicitud} actualizada.")
        print(f"  Nuevo inicio: {sol.fecha_inicio}  |  Fin: {sol.fecha_fin}")
    except ValueError as e:
        print(f"  [Error] {e}")


def menu_eliminar_solicitud(sistema):
    """Submenú para eliminar solicitudes de vacaciones."""
    print("\n  Opciones de eliminación:")
    print("  ── Para una solicitud individual ──")
    print("    1. Por número de solicitud")
    print("    2. Por número de empleado (primera pendiente)")
    print("    3. Por número de empleado y estatus")
    print("  ── Para un grupo de solicitudes ──")
    print("    4. Por estatus")
    print("    5. Por tipo de empleado")
    print("    6. Por número de empleado (todas)")

    sel = input("  Seleccione opción: ").strip()
    if sel == "1":
        num_sol = input("  Número de solicitud: ").strip()
        try:
            sistema.eliminar_solicitud(num_sol)
            print(f"  Solicitud {num_sol} eliminada.")
        except ValueError as e:
            print(f"  [Error] {e}")
    elif sel == "2":
        num_emp = input("  Número de empleado: ").strip()
        pares = sistema.consultar_solicitudes("numero_empleado", num_emp)
        pendientes = [s for s, _ in pares if s.estatus == "pendiente"]
        if not pendientes:
            print("  No hay solicitudes pendientes para ese empleado.")
            return
        sol = pendientes[0]
        sol.mostrar()
        confirmacion = input("  ¿Eliminar esta solicitud? (s/n): ").strip().lower()
        if confirmacion == "s":
            try:
                sistema.eliminar_solicitud(sol.numero_solicitud)
                print("  Solicitud eliminada.")
            except ValueError as e:
                print(f"  [Error] {e}")
    elif sel == "3":
        num_emp = input("  Número de empleado: ").strip()
        estatus = _pedir_opcion(["pendiente", "aprobada", "rechazada"], "Estatus")
        pares = sistema.consultar_solicitudes("numero_empleado", num_emp)
        con_estatus = [s for s, _ in pares if s.estatus == estatus]
        if not con_estatus:
            print(f"  No hay solicitudes con estatus '{estatus}' para ese empleado.")
            return
        for sol in con_estatus:
            sol.mostrar()
        confirmacion = input(f"  ¿Eliminar {len(con_estatus)} solicitud(es)? (s/n): ").strip().lower()
        if confirmacion == "s":
            for sol in con_estatus:
                sistema.eliminar_solicitud(sol.numero_solicitud)
            print(f"  {len(con_estatus)} solicitud(es) eliminada(s).")
    elif sel in ("4", "5", "6"):
        etiquetas = {
            "4": ("estatus",           "estatus"),
            "5": ("tipo de empleado",  "tipo"),
            "6": ("número de empleado","numero_empleado"),
        }
        etiqueta, criterio = etiquetas[sel]
        valor = input(f"  Ingrese el {etiqueta}: ").strip()
        n = sistema.eliminar_solicitudes(criterio, valor)
        print(f"  {n} solicitud(es) eliminada(s).")
    else:
        print("  [Error] Opción inválida.")


# ──────────────────────── MENÚ PRINCIPAL ───────────────────────────────────

def menu_principal(sistema):
    """Despliega el menú principal del sistema.

    Args:
        sistema (SistemaVacaciones): Instancia del sistema.
    """
    opciones = {
        "1": ("Consultar empleados",             menu_consultar_empleados),
        "2": ("Consultar días de vacaciones",    menu_consultar_vacaciones),
        "3": ("Consultar solicitudes",           menu_consultar_solicitudes),
        "4": ("Alta / Actualización de empleado", None),
        "5": ("Baja de empleado(s)",             menu_baja_empleado),
        "6": ("Nueva solicitud de vacaciones",   menu_nueva_solicitud),
        "7": ("Actualizar solicitud",            menu_actualizar_solicitud),
        "8": ("Eliminar solicitud(es)",          menu_eliminar_solicitud),
        "9": ("Catálogo de vacaciones",          lambda s: s.consultar_catalogo()),
        "10":("Reporte ejecutivo",               lambda s: s.reporte_ejecutivo()),
        "0": ("Cerrar el día y salir",           None),
    }

    while True:
        print("\n" + "=" * 50)
        print(f"{'SISTEMA DE VACACIONES — GALACTIC FORCE':^50}")
        print(f"{'SOLUTIONS':^50}")
        print("=" * 50)
        for clave, (etiqueta, _) in opciones.items():
            print(f"  {clave:>2}. {etiqueta}")
        print("=" * 50)
        sel = input("  Seleccione una opción: ").strip()

        if sel == "0":
            confirmacion = input("  ¿Guardar datos antes de salir? (s/n): ").strip().lower()
            if confirmacion == "s":
                sistema.guardar_archivos()
            print("\n  ¡Hasta luego!\n")
            break
        elif sel == "4":
            print("\n  1. Alta de nuevo empleado")
            print("  2. Actualizar empleado existente")
            sub = input("  Opción: ").strip()
            if sub == "1":
                menu_alta_empleado(sistema)
            elif sub == "2":
                menu_actualizar_empleado(sistema)
        elif sel in opciones:
            _, funcion = opciones[sel]
            if funcion:
                try:
                    funcion(sistema)
                except Exception as e:
                    print(f"  [Error inesperado] {e}")
        else:
            print("  [Error] Opción no válida.")


# ──────────────────────── INICIO ───────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(f"{'Iniciando sistema...':^50}")
    print("=" * 50)
    sistema = SistemaVacaciones()
    try:
        sistema.cargar_archivos()
    except Exception as e:
        print(f"  [Error al cargar] {e}")

    menu_principal(sistema)
