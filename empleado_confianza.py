"""Módulo con la clase EmpleadoConfianza."""

from empleado import Empleado


class EmpleadoConfianza(Empleado):
    """Empleado de confianza de la empresa.

    Atributos adicionales:
        nivel_confianza (str): 'junior', 'senior' o 'directivo'.
        jornada (str): 'completa' o 'medio_tiempo'.

    Regla de vacaciones:
        Días por ley + 3 días extra si antigüedad >= 2,
        nivel es 'senior' o 'directivo' Y jornada es 'completa'.
    """

    NIVELES_VALIDOS = ("junior", "senior", "directivo")
    JORNADAS_VALIDAS = ("completa", "medio_tiempo")

    def __init__(self, numero_empleado, nombre_completo, fecha_nacimiento,
                 direccion, correo, puesto, telefono, salario, departamento,
                 fecha_contratacion, dia_descanso, nivel_confianza, jornada):
        super().__init__(numero_empleado, nombre_completo, fecha_nacimiento,
                         direccion, correo, puesto, telefono, salario,
                         departamento, fecha_contratacion, dia_descanso)
        self.nivel_confianza = nivel_confianza.lower()
        self.jornada = jornada.lower()

    def get_tipo_empleado(self):
        """Retorna el tipo de empleado."""
        return "Confianza"

    def calcular_dias_extra(self, antiguedad):
        """Retorna 3 días extra si cumple todas las condiciones, 0 si no.

        Condiciones: antigüedad >= 2, nivel senior/directivo, jornada completa.

        Args:
            antiguedad (int): Años de antigüedad.

        Returns:
            int: Días extra de vacaciones.
        """
        # BUG ORIGINAL: '== in [...]' es error de sintaxis; debe ser solo 'in [...]'
        if (antiguedad >= 2
                and self.jornada == "completa"
                and self.nivel_confianza in ("senior", "directivo")):
            return 3
        return 0

    def campos_modificables(self):
        """Agrega nivel_confianza y jornada a los campos modificables."""
        return super().campos_modificables() + ["nivel_confianza", "jornada"]

    def mostrar_info(self):
        """Muestra información completa del empleado de confianza."""
        super().mostrar_info()
        print(f"  Nivel         : {self.nivel_confianza.capitalize()}")
        print(f"  Jornada       : {self.jornada.replace('_', ' ').capitalize()}")

    def a_csv(self):
        """Retorna la línea CSV del empleado de confianza.

        Returns:
            str: Datos separados por coma, con tipo 'C' al inicio.
        """
        return (f"C,{self.numero_empleado},{self.nombre_completo},"
                f"{self.fecha_nacimiento},{self.direccion},{self.correo},"
                f"{self.telefono},{self.salario},{self.puesto},"
                f"{self.departamento},{self.fecha_contratacion},"
                f"{self.dia_descanso},{self.nivel_confianza},{self.jornada}")
