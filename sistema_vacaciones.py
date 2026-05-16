"""Módulo con la clase SistemaVacaciones: lógica central del sistema de RH."""

from datetime import date

from catalogo_vacaciones import CatalogoVacaciones
from vacaciones_empleado import VacacionesEmpleado
from solicitud_vacaciones import SolicitudVacaciones
from empleado_sindicalizado import EmpleadoSindicalizado
from empleado_confianza import EmpleadoConfianza
from empleado_temporal import EmpleadoTemporal
import gestor_archivos as ga


class SistemaVacaciones:
    """Sistema central de administración de vacaciones de Galactic Force Solutions.

    Attributes:
        empleados (list): Lista de todos los empleados activos.
        catalogo (CatalogoVacaciones): Catálogo de días por antigüedad.
        vacaciones (dict): {numero_empleado: VacacionesEmpleado}
        solicitudes (list): Lista de todas las solicitudes de vacaciones.
    """

    def __init__(self):
        self.empleados = []
        self.catalogo = CatalogoVacaciones()
        self.vacaciones = {}
        self.solicitudes = []
        self._contador_solicitud = 1

    # ─────────────────────── CARGA Y CIERRE DEL DÍA ────────────────────────

    def cargar_archivos(self):
        """Carga todos los datos al iniciar el día y actualiza vacaciones."""
        ga.inicializar_archivos()
        self.empleados = ga.cargar_empleados()
        self.vacaciones = ga.cargar_vacaciones()
        self.solicitudes = ga.cargar_solicitudes()
        self._ajustar_contador_solicitudes()
        self._revisar_anios_laborales()
        print(f"  Sistema iniciado. {len(self.empleados)} empleado(s) cargado(s).")

    def guardar_archivos(self):
        """Persiste todos los datos al cerrar el sistema."""
        ga.guardar_empleados(self.empleados)
        ga.guardar_vacaciones(self.vacaciones)
        ga.guardar_solicitudes(self.solicitudes)
        ga.guardar_catalogo(self.catalogo)
        print("  Datos guardados correctamente.")

    def _ajustar_contador_solicitudes(self):
        """Ajusta el contador interno al máximo número de solicitud existente."""
        numeros = [
            int(s.numero_solicitud.replace("SOL", ""))
            for s in self.solicitudes
            if s.numero_solicitud.startswith("SOL")
        ]
        if numeros:
            self._contador_solicitud = max(numeros) + 1

    def _revisar_anios_laborales(self):
        """Revisa si algún empleado cumplió nuevo año laboral y resetea vacaciones."""
        hoy = date.today()
        resetados = []
        for emp in self.empleados:
            num = emp.numero_empleado
            antiguedad = emp.calcular_antiguedad()
            if num not in self.vacaciones:
                vac = self._generar_vacaciones(emp)
                self.vacaciones[num] = vac
                continue
            vac_actual = self.vacaciones[num]
            if antiguedad >= 1 and vac_actual.year != hoy.year:
                resetados.append(vac_actual)
                self.vacaciones[num] = self._generar_vacaciones(emp)
        if resetados:
            ga.archivar_vacaciones_anteriores(resetados)

    def _generar_vacaciones(self, emp):
        """Crea un registro de VacacionesEmpleado para el empleado dado.

        Args:
            emp (Empleado): Empleado para quien se genera el registro.

        Returns:
            VacacionesEmpleado: Nuevo registro de vacaciones.
        """
        hoy = date.today()
        antiguedad = emp.calcular_antiguedad()
        if antiguedad < 1:
            return VacacionesEmpleado(emp.numero_empleado, hoy.year, 0, 0, 0, 0, False)

        dias_ley = self.catalogo.obtener_dias(antiguedad)

        if isinstance(emp, EmpleadoTemporal):
            dias_totales = emp.calcular_vacaciones_proporcionales(dias_ley)
            dias_extra = 0
        else:
            dias_extra = emp.calcular_dias_extra(antiguedad)
            dias_totales = dias_ley + dias_extra

        return VacacionesEmpleado(
            emp.numero_empleado, hoy.year, dias_ley,
            dias_extra, dias_totales, 0, True
        )

    # ─────────────────────── GENERADORES DE ID ─────────────────────────────

    def _nuevo_numero_empleado(self):
        """Genera un número de empleado único en formato 'EMP####'.

        Returns:
            str: Nuevo número de empleado.
        """
        existentes = {emp.numero_empleado for emp in self.empleados}
        n = 1001
        while f"EMP{n}" in existentes:
            n += 1
        return f"EMP{n}"

    def _nuevo_numero_solicitud(self):
        """Genera un número de solicitud único en formato 'SOL####'.

        Returns:
            str: Nuevo número de solicitud.
        """
        num = f"SOL{self._contador_solicitud:04d}"
        self._contador_solicitud += 1
        return num

    # ─────────────────────── ALTA / ACTUALIZACIÓN DE EMPLEADOS ─────────────

    def alta_empleado(self, tipo, datos):
        """Da de alta un nuevo empleado en el sistema.

        Args:
            tipo (str): 'S' (sindicalizado), 'C' (confianza) o 'T' (temporal).
            datos (dict): Datos del empleado (sin numero_empleado).

        Returns:
            Empleado: El empleado creado.

        Raises:
            ValueError: Si el tipo es inválido.
        """
        datos["numero_empleado"] = self._nuevo_numero_empleado()
        tipo = tipo.strip().upper()
        if tipo == "S":
            emp = EmpleadoSindicalizado(**datos)
        elif tipo == "C":
            emp = EmpleadoConfianza(**datos)
        elif tipo == "T":
            emp = EmpleadoTemporal(**datos)
        else:
            raise ValueError(f"Tipo de empleado inválido: '{tipo}'.")
        self.empleados.append(emp)
        self.vacaciones[emp.numero_empleado] = self._generar_vacaciones(emp)
        return emp

    def actualizar_empleado(self, numero_empleado, cambios):
        """Actualiza los datos modificables de un empleado.

        Args:
            numero_empleado (str): Número del empleado a actualizar.
            cambios (dict): {campo: nuevo_valor}

        Raises:
            ValueError: Si el empleado no existe o el campo no es modificable.
        """
        emp = self._buscar_empleado(numero_empleado)
        no_permitidos = {"numero_empleado", "fecha_contratacion"}
        for campo, valor in cambios.items():
            if campo in no_permitidos:
                raise ValueError(f"El campo '{campo}' no puede modificarse.")
            if campo not in emp.campos_modificables():
                raise ValueError(f"Campo '{campo}' no válido para este tipo de empleado.")
            setattr(emp, campo, valor)

    def baja_empleado(self, numero_empleado):
        """Elimina un empleado del sistema y lo archiva.

        Args:
            numero_empleado (str): Número del empleado a eliminar.

        Raises:
            ValueError: Si el empleado no existe.
        """
        emp = self._buscar_empleado(numero_empleado)
        self.empleados.remove(emp)
        self.vacaciones.pop(numero_empleado, None)
        ga.archivar_empleado_borrado(emp)

    def eliminar_empleado(self, criterio, valor):
        """Elimina un grupo de empleados que coincidan con el criterio.

        Args:
            criterio (str): Campo de búsqueda.
            valor (str): Valor del criterio.

        Returns:
            int: Número de empleados eliminados.
        """
        encontrados = self.consultar_empleados(criterio, valor)
        for emp in encontrados:
            self.empleados.remove(emp)
            self.vacaciones.pop(emp.numero_empleado, None)
            ga.archivar_empleado_borrado(emp)
        return len(encontrados)

    # ─────────────────────── SOLICITUDES DE VACACIONES ─────────────────────

    def registrar_solicitud(self, numero_empleado, fecha_inicio, dias_solicitados):
        """Registra una nueva solicitud de vacaciones.

        Args:
            numero_empleado (str): Número del empleado.
            fecha_inicio (date): Primer día de vacaciones.
            dias_solicitados (int): Días hábiles solicitados.

        Returns:
            SolicitudVacaciones: La solicitud creada.

        Raises:
            ValueError: Si no se cumplen las condiciones del negocio.
        """
        self._buscar_empleado(numero_empleado)  # valida que exista
        vac = self.vacaciones.get(numero_empleado)

        if not vac or not vac.habilitado:
            raise ValueError("El empleado no tiene vacaciones habilitadas (requiere 1 año de antigüedad).")
        if dias_solicitados <= 0:
            raise ValueError("Los días solicitados deben ser mayor a 0.")
        if dias_solicitados > vac.dias_restantes:
            raise ValueError(
                f"Días insuficientes. Disponibles: {vac.dias_restantes}, "
                f"solicitados: {dias_solicitados}."
            )
        hoy = date.today()
        if not SolicitudVacaciones.validar_anticipacion(hoy, fecha_inicio):
            raise ValueError("La solicitud debe hacerse con al menos 7 días de anticipación.")

        fecha_fin = SolicitudVacaciones.calcular_fecha_fin(fecha_inicio, dias_solicitados)
        num_sol = self._nuevo_numero_solicitud()
        sol = SolicitudVacaciones(num_sol, numero_empleado, hoy,
                                  fecha_inicio, fecha_fin, dias_solicitados)
        self.solicitudes.append(sol)
        vac.usar_dias(dias_solicitados)
        return sol

    def actualizar_solicitud(self, numero_solicitud, nueva_fecha_inicio, nuevos_dias):
        """Actualiza una solicitud pendiente con nueva fecha e inicio y días.

        Args:
            numero_solicitud (str): Número de la solicitud.
            nueva_fecha_inicio (date): Nueva fecha de inicio.
            nuevos_dias (int): Nuevo número de días hábiles.

        Returns:
            SolicitudVacaciones: La solicitud actualizada.

        Raises:
            ValueError: Si la solicitud no está pendiente o no cumple validaciones.
        """
        sol = self._buscar_solicitud(numero_solicitud)
        if sol.estatus != "pendiente":
            raise ValueError("Solo se pueden modificar solicitudes con estatus 'pendiente'.")

        hoy = date.today()
        if not SolicitudVacaciones.validar_anticipacion(hoy, nueva_fecha_inicio):
            raise ValueError("La nueva fecha debe ser al menos 7 días después de hoy.")

        vac = self.vacaciones.get(sol.numero_empleado)
        dias_adicionales = nuevos_dias - sol.dias_solicitados
        if dias_adicionales > vac.dias_restantes:
            raise ValueError(
                f"No hay suficientes días. Adicionales necesarios: {dias_adicionales}, "
                f"disponibles: {vac.dias_restantes}."
            )
        vac.devolver_dias(sol.dias_solicitados)
        vac.usar_dias(nuevos_dias)

        sol.fecha_solicitud = hoy
        sol.fecha_inicio = nueva_fecha_inicio
        sol.fecha_fin = SolicitudVacaciones.calcular_fecha_fin(nueva_fecha_inicio, nuevos_dias)
        sol.dias_solicitados = nuevos_dias
        return sol

    def eliminar_solicitud(self, numero_solicitud):
        """Elimina una solicitud y devuelve los días al empleado.

        Args:
            numero_solicitud (str): Número de la solicitud.

        Raises:
            ValueError: Si la solicitud no existe.
        """
        sol = self._buscar_solicitud(numero_solicitud)
        self.solicitudes.remove(sol)
        vac = self.vacaciones.get(sol.numero_empleado)
        if vac and sol.estatus == "pendiente":
            vac.devolver_dias(sol.dias_solicitados)
        ga.archivar_solicitud_borrada(sol)

    def eliminar_solicitudes(self, criterio, valor):
        """Elimina todas las solicitudes que coincidan con el criterio.

        Args:
            criterio (str): 'estatus', 'numero_empleado' o 'tipo'.
            valor (str): Valor del criterio.

        Returns:
            int: Número de solicitudes eliminadas.
        """
        encontradas = [s for s, _ in self.consultar_solicitudes(criterio, valor)]
        for sol in encontradas:
            self.solicitudes.remove(sol)
            vac = self.vacaciones.get(sol.numero_empleado)
            if vac and sol.estatus == "pendiente":
                vac.devolver_dias(sol.dias_solicitados)
            ga.archivar_solicitud_borrada(sol)
        return len(encontradas)

    # ─────────────────────── CONSULTAS ─────────────────────────────────────

    def consultar_empleados(self, criterio, valor):
        """Busca empleados según un criterio.

        Criterios soportados: numero_empleado, tipo, nombre, puesto,
        departamento, sindicato, jornada, nivel_confianza, tipo_contrato,
        dia_descanso, edad, antiguedad.

        Args:
            criterio (str): Campo de búsqueda.
            valor (str/int): Valor a buscar.

        Returns:
            list: Empleados que coinciden con el criterio.
        """
        valor_str = str(valor).strip().lower()
        resultado = []
        for emp in self.empleados:
            coincide = False
            if criterio == "numero_empleado":
                coincide = emp.numero_empleado.lower() == valor_str
            elif criterio == "tipo":
                coincide = emp.get_tipo_empleado().lower() == valor_str
            elif criterio == "nombre":
                coincide = valor_str in emp.nombre_completo.lower()
            elif criterio == "puesto":
                coincide = valor_str in emp.puesto.lower()
            elif criterio == "departamento":
                coincide = valor_str in emp.departamento.lower()
            elif criterio == "sindicato":
                if isinstance(emp, EmpleadoSindicalizado):
                    coincide = valor_str in emp.nombre_sindicato.lower()
            elif criterio == "jornada":
                if isinstance(emp, EmpleadoConfianza):
                    coincide = emp.jornada.lower() == valor_str
            elif criterio == "nivel_confianza":
                if isinstance(emp, EmpleadoConfianza):
                    coincide = emp.nivel_confianza.lower() == valor_str
            elif criterio == "tipo_contrato":
                if isinstance(emp, EmpleadoTemporal):
                    coincide = emp.tipo_contrato.lower() == valor_str
            elif criterio == "dia_descanso":
                coincide = emp.dia_descanso.lower() == valor_str
            elif criterio == "edad":
                try:
                    coincide = emp.calcular_edad() == int(valor)
                except ValueError:
                    pass
            elif criterio == "antiguedad":
                try:
                    coincide = emp.calcular_antiguedad() == int(valor)
                except ValueError:
                    pass
            if coincide:
                resultado.append(emp)
        return resultado

    def consultar_vacaciones(self, criterio, valor1, valor2=None):
        """Busca registros de vacaciones según criterio de par o individual.

        Criterios soportados: tipo_departamento, departamento_nivel,
        departamento_contrato, departamento_puesto, fecha_contratacion,
        antiguedad, sindicato, mes_anio, edad_sueldo.

        Args:
            criterio (str): Tipo de criterio.
            valor1 (str): Primer valor.
            valor2 (str, optional): Segundo valor (para criterios de par).

        Returns:
            list: Lista de tuplas (Empleado, VacacionesEmpleado).
        """
        v1 = str(valor1).strip().lower()
        v2 = str(valor2).strip().lower() if valor2 else None
        resultado = []

        for emp in self.empleados:
            vac = self.vacaciones.get(emp.numero_empleado)
            if not vac or not vac.habilitado:
                continue
            coincide = False
            if criterio == "tipo_departamento":
                coincide = (emp.get_tipo_empleado().lower() == v1
                            and emp.departamento.lower() == v2)
            elif criterio == "departamento_nivel":
                if isinstance(emp, EmpleadoConfianza):
                    coincide = (emp.departamento.lower() == v1
                                and emp.nivel_confianza.lower() == v2)
            elif criterio == "departamento_contrato":
                if isinstance(emp, EmpleadoTemporal):
                    coincide = (emp.departamento.lower() == v1
                                and emp.tipo_contrato.lower() == v2)
            elif criterio == "departamento_puesto":
                coincide = (emp.departamento.lower() == v1
                            and emp.puesto.lower() == v2)
            elif criterio == "fecha_contratacion":
                coincide = str(emp.fecha_contratacion) == v1
            elif criterio == "antiguedad":
                try:
                    coincide = emp.calcular_antiguedad() == int(v1)
                except ValueError:
                    pass
            elif criterio == "sindicato":
                if isinstance(emp, EmpleadoSindicalizado):
                    coincide = v1 in emp.nombre_sindicato.lower()
            elif criterio == "mes_anio":
                try:
                    mes, anio = int(v1), int(v2)
                    coincide = (emp.fecha_contratacion.month == mes
                                and emp.fecha_contratacion.year == anio)
                except (ValueError, TypeError):
                    pass
            elif criterio == "edad_sueldo":
                try:
                    coincide = (emp.calcular_edad() == int(v1)
                                and emp.salario >= float(v2))
                except (ValueError, TypeError):
                    pass
            if coincide:
                resultado.append((emp, vac))
        return resultado

    def consultar_solicitudes(self, criterio, valor):
        """Filtra solicitudes según un criterio.

        Criterios soportados: numero_empleado, estatus, tipo.

        Args:
            criterio (str): Campo de filtrado.
            valor (str): Valor a buscar.

        Returns:
            list: Lista de tuplas (SolicitudVacaciones, Empleado|None).
        """
        valor = str(valor).strip().lower()
        mapa = {emp.numero_empleado: emp for emp in self.empleados}
        resultado = []
        for sol in self.solicitudes:
            emp = mapa.get(sol.numero_empleado)
            coincide = False
            if criterio == "numero_empleado":
                coincide = sol.numero_empleado.lower() == valor
            elif criterio == "estatus":
                coincide = sol.estatus.lower() == valor
            elif criterio == "tipo":
                if emp:
                    coincide = emp.get_tipo_empleado().lower() == valor
            if coincide:
                resultado.append((sol, emp))
        return resultado

    def consultar_catalogo(self):
        """Muestra el catálogo de vacaciones."""
        self.catalogo.mostrar()

    # ─────────────────────── REPORTE EJECUTIVO ─────────────────────────────

    def reporte_ejecutivo(self):
        """Imprime un resumen ejecutivo del estado de vacaciones de la empresa."""
        total = len(self.empleados)
        por_tipo = {}
        for emp in self.empleados:
            t = emp.get_tipo_empleado()
            por_tipo[t] = por_tipo.get(t, 0) + 1

        mas_antiguos = sorted(self.empleados,
                              key=lambda e: e.calcular_antiguedad(), reverse=True)[:3]

        por_estatus = {"pendiente": 0, "aprobada": 0, "rechazada": 0}
        sol_por_tipo = {}
        mapa = {emp.numero_empleado: emp for emp in self.empleados}
        for sol in self.solicitudes:
            por_estatus[sol.estatus] = por_estatus.get(sol.estatus, 0) + 1
            emp = mapa.get(sol.numero_empleado)
            if emp:
                t = emp.get_tipo_empleado()
                sol_por_tipo[t] = sol_por_tipo.get(t, 0) + 1

        sep = "=" * 55
        print(f"\n{sep}")
        print(f"{'REPORTE EJECUTIVO — GALACTIC FORCE SOLUTIONS':^55}")
        print(sep)
        print(f"  Total de empleados activos : {total}")
        for tipo, cnt in sorted(por_tipo.items()):
            print(f"    {tipo:<28}: {cnt}")
        print(f"\n  Empleados con mayor antigüedad:")
        for emp in mas_antiguos:
            print(f"    {emp.nombre_completo:<30} {emp.calcular_antiguedad()} año(s)")
        print(f"\n  Total solicitudes          : {len(self.solicitudes)}")
        for tipo, cnt in sorted(sol_por_tipo.items()):
            print(f"    Por tipo {tipo:<22}: {cnt}")
        print(f"  Por estatus:")
        for estatus, cnt in por_estatus.items():
            print(f"    {estatus.capitalize():<28}: {cnt}")
        print(sep)

    # ─────────────────────── UTILIDADES INTERNAS ───────────────────────────

    def _buscar_empleado(self, numero_empleado):
        """Retorna el empleado con el número dado.

        Args:
            numero_empleado (str): Número de empleado.

        Returns:
            Empleado: Empleado encontrado.

        Raises:
            ValueError: Si no existe el empleado.
        """
        for emp in self.empleados:
            if emp.numero_empleado == numero_empleado:
                return emp
        raise ValueError(f"Empleado '{numero_empleado}' no encontrado.")

    def _buscar_solicitud(self, numero_solicitud):
        """Retorna la solicitud con el número dado.

        Args:
            numero_solicitud (str): Número de solicitud.

        Returns:
            SolicitudVacaciones: Solicitud encontrada.

        Raises:
            ValueError: Si no existe la solicitud.
        """
        for sol in self.solicitudes:
            if sol.numero_solicitud == numero_solicitud:
                return sol
        raise ValueError(f"Solicitud '{numero_solicitud}' no encontrada.")
