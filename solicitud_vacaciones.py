"""Módulo con la clase SolicitudVacaciones."""

from datetime import date, timedelta


class SolicitudVacaciones:
    """Representa una solicitud de vacaciones de un empleado.

    Attributes:
        numero_solicitud (str): Identificador único de la solicitud.
        numero_empleado (str): Número del empleado que solicita.
        fecha_solicitud (date): Fecha en que se registra la solicitud.
        fecha_inicio (date): Primer día de vacaciones.
        fecha_fin (date): Último día de vacaciones (sin contar sáb/dom).
        dias_solicitados (int): Días hábiles solicitados.
        estatus (str): 'pendiente', 'aprobada' o 'rechazada'.
    """

    ESTATUS_VALIDOS = ("pendiente", "aprobada", "rechazada")
    DIAS_ANTICIPACION_MINIMOS = 7

    def __init__(self, numero_solicitud, numero_empleado, fecha_solicitud,
                 fecha_inicio, fecha_fin, dias_solicitados, estatus="pendiente"):
        self.numero_solicitud = numero_solicitud
        self.numero_empleado = numero_empleado
        self.fecha_solicitud = fecha_solicitud
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dias_solicitados = int(dias_solicitados)
        self.estatus = estatus.lower()

    @staticmethod
    def calcular_fecha_fin(fecha_inicio, dias_habiles):
        """Calcula la fecha de fin excluyendo sábados y domingos.

        Args:
            fecha_inicio (date): Primer día de vacaciones.
            dias_habiles (int): Días hábiles solicitados.

        Returns:
            date: Fecha en que terminan las vacaciones.
        """
        contados = 0
        dia = fecha_inicio
        while contados < dias_habiles:
            if dia.weekday() < 5:   # 0=lun … 4=vie, 5=sáb, 6=dom
                contados += 1
            if contados < dias_habiles:
                dia += timedelta(days=1)
        return dia

    @staticmethod
    def validar_anticipacion(fecha_solicitud, fecha_inicio):
        """Verifica que la solicitud tenga al menos 7 días de anticipación.

        Args:
            fecha_solicitud (date): Fecha en que se registra la solicitud.
            fecha_inicio (date): Fecha de inicio de vacaciones.

        Returns:
            bool: True si cumple la anticipación mínima.
        """
        return (fecha_inicio - fecha_solicitud).days >= SolicitudVacaciones.DIAS_ANTICIPACION_MINIMOS

    def cambiar_estatus(self, nuevo_estatus):
        """Cambia el estatus de la solicitud (solo si está pendiente).

        Args:
            nuevo_estatus (str): 'aprobada' o 'rechazada'.

        Raises:
            ValueError: Si el estatus es inválido o la solicitud no está pendiente.
        """
        if nuevo_estatus not in self.ESTATUS_VALIDOS:
            raise ValueError(f"Estatus inválido: '{nuevo_estatus}'.")
        if self.estatus != "pendiente":
            raise ValueError("Solo se pueden modificar solicitudes con estatus 'pendiente'.")
        self.estatus = nuevo_estatus

    def mostrar(self):
        """Imprime la información de la solicitud."""
        print(f"  Num. Solicitud: {self.numero_solicitud}")
        print(f"  Num. Empleado : {self.numero_empleado}")
        print(f"  Fecha Solic.  : {self.fecha_solicitud}")
        print(f"  Inicio Vac.   : {self.fecha_inicio}")
        print(f"  Fin Vac.      : {self.fecha_fin}")
        print(f"  Días Solic.   : {self.dias_solicitados}")
        print(f"  Estatus       : {self.estatus.capitalize()}")

    def a_csv(self):
        """Retorna la representación CSV de la solicitud.

        Returns:
            str: Línea en formato CSV.
        """
        return (f"{self.numero_solicitud},{self.numero_empleado},"
                f"{self.fecha_solicitud},{self.fecha_inicio},"
                f"{self.fecha_fin},{self.dias_solicitados},{self.estatus}")
