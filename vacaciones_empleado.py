"""Módulo con la clase VacacionesEmpleado."""


class VacacionesEmpleado:
    """Registro de vacaciones de un empleado para el año actual.

    Attributes:
        numero_empleado (str): Número de empleado.
        year (int): Año al que corresponden las vacaciones.
        dias_otorgados_ley (int): Días por ley según el catálogo.
        dias_extra (int): Días extra según tipo de empleado.
        dias_totales (int): dias_otorgados_ley + dias_extra.
        dias_utilizados (int): Días de vacaciones ya consumidos.
        habilitado (bool): True si el empleado cumplió su primer año laboral.
    """

    def __init__(self, numero_empleado, year, dias_otorgados_ley, dias_extra,
                 dias_totales, dias_utilizados, habilitado):
        self.numero_empleado = numero_empleado
        self.year = int(year)
        self.dias_otorgados_ley = int(dias_otorgados_ley)
        self.dias_extra = int(dias_extra)
        self.dias_totales = int(dias_totales)
        self.dias_utilizados = int(dias_utilizados)   # BUG ORIGINAL: faltaba '= dias_utilizados'
        self.habilitado = str(habilitado).strip().lower() in ("true", "1", "sí", "si")
        self.dias_restantes = self.dias_totales - self.dias_utilizados

    def _recalcular_restantes(self):
        """Actualiza dias_restantes después de cualquier cambio."""
        self.dias_restantes = self.dias_totales - self.dias_utilizados

    def usar_dias(self, cantidad):
        """Descuenta días del saldo disponible.

        Args:
            cantidad (int): Días a consumir.

        Raises:
            ValueError: Si no hay suficientes días disponibles.
        """
        if cantidad > self.dias_restantes:
            raise ValueError(
                f"Días insuficientes. Disponibles: {self.dias_restantes}, "
                f"solicitados: {cantidad}."
            )
        self.dias_utilizados += cantidad
        self._recalcular_restantes()

    def devolver_dias(self, cantidad):
        """Devuelve días al saldo (cancelación de solicitud).

        Args:
            cantidad (int): Días a devolver.
        """
        self.dias_utilizados = max(0, self.dias_utilizados - cantidad)
        self._recalcular_restantes()

    def mostrar(self):
        """Imprime el resumen de vacaciones."""
        estado = "Habilitadas" if self.habilitado else "No habilitadas (< 1 año)"
        print(f"  Año           : {self.year}")
        print(f"  Estado        : {estado}")
        print(f"  Días por ley  : {self.dias_otorgados_ley}")
        print(f"  Días extra    : {self.dias_extra}")
        print(f"  Días totales  : {self.dias_totales}")
        print(f"  Días usados   : {self.dias_utilizados}")
        print(f"  Días restant. : {self.dias_restantes}")

    def a_csv(self):
        """Retorna la representación CSV del registro de vacaciones.

        Returns:
            str: Línea en formato CSV.
        """
        return (f"{self.numero_empleado},{self.year},{self.dias_otorgados_ley},"
                f"{self.dias_extra},{self.dias_totales},{self.dias_utilizados},"
                f"{self.habilitado}")
