"""Módulo con la clase EmpleadoTemporal."""

from empleado import Empleado


class EmpleadoTemporal(Empleado):
    """Empleado con contrato temporal.

    Atributos adicionales:
        tipo_contrato (str): 'obra', 'temporada' o 'interinato'.
        fecha_inicio_contrato (date): Inicio del contrato temporal.
        fecha_fin_contrato (date): Fin del contrato temporal.

    Regla de vacaciones (proporcional):
        dias_ley * (meses_laborados / 12)
    """

    CONTRATOS_VALIDOS = ("obra", "temporada", "interinato")

    def __init__(self, numero_empleado, nombre_completo, fecha_nacimiento,
                 direccion, correo, puesto, telefono, salario, departamento,
                 fecha_contratacion, dia_descanso, tipo_contrato,
                 fecha_inicio_contrato, fecha_fin_contrato):
        super().__init__(numero_empleado, nombre_completo, fecha_nacimiento,
                         direccion, correo, puesto, telefono, salario,
                         departamento, fecha_contratacion, dia_descanso)
        self.tipo_contrato = tipo_contrato.lower()
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.fecha_fin_contrato = fecha_fin_contrato

    def get_tipo_empleado(self):
        """Retorna el tipo de empleado."""
        return "Temporal"

    def calcular_dias_extra(self, antiguedad):
        """Los temporales no reciben días extra.

        Args:
            antiguedad (int): Años de antigüedad (no se usa).

        Returns:
            int: Siempre 0.
        """
        return 0

    def calcular_vacaciones_proporcionales(self, dias_ley):
        """Calcula días de vacaciones proporcionales al tiempo laborado.

        Formula del proyecto: dias_ley * (meses_laborados / 12)
        Ejemplo: 14 meses laborados, año 2 (14 días ley) → 14*(14/12) ≈ 16 días.

        Args:
            dias_ley (int): Días por ley según el catálogo para su antigüedad.

        Returns:
            int: Días de vacaciones proporcionales (truncados).
        """
        meses = self.calcular_meses_laborados()
        return int(dias_ley * (meses / 12))

    def campos_modificables(self):
        """Agrega tipo_contrato y fecha_fin_contrato a los campos modificables."""
        return super().campos_modificables() + ["tipo_contrato", "fecha_fin_contrato"]

    def mostrar_info(self):
        """Muestra información completa del empleado temporal."""
        super().mostrar_info()
        print(f"  Tipo Contrato : {self.tipo_contrato.capitalize()}")
        print(f"  Inicio Ctto.  : {self.fecha_inicio_contrato}")
        print(f"  Fin Ctto.     : {self.fecha_fin_contrato}")

    def a_csv(self):
        """Retorna la línea CSV del empleado temporal.

        Returns:
            str: Datos separados por coma, con tipo 'T' al inicio.
        """
        return (f"T,{self.numero_empleado},{self.nombre_completo},"
                f"{self.fecha_nacimiento},{self.direccion},{self.correo},"
                f"{self.telefono},{self.salario},{self.puesto},"
                f"{self.departamento},{self.fecha_contratacion},"
                f"{self.dia_descanso},{self.tipo_contrato},"
                f"{self.fecha_inicio_contrato},{self.fecha_fin_contrato}")
