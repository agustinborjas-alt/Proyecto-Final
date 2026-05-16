"""Módulo con la clase base abstracta Empleado."""

from abc import ABC, abstractmethod
from datetime import date


class Empleado(ABC):
    """Clase base abstracta para todos los tipos de empleado de Galactic Force Solutions.

    Attributes:
        numero_empleado (str): Identificador único del empleado.
        nombre_completo (str): Nombre completo del empleado.
        fecha_nacimiento (date): Fecha de nacimiento.
        direccion (str): Dirección del empleado.
        correo (str): Correo electrónico.
        puesto (str): Puesto que ocupa.
        telefono (str): Número de teléfono.
        salario (float): Salario mensual.
        departamento (str): Departamento de adscripción.
        fecha_contratacion (date): Fecha de contratación.
        dia_descanso (str): Día de descanso semanal.
    """

    def __init__(self, numero_empleado, nombre_completo, fecha_nacimiento,
                 direccion, correo, puesto, telefono, salario, departamento,
                 fecha_contratacion, dia_descanso):
        self.numero_empleado = numero_empleado
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.correo = correo
        self.puesto = puesto
        self.telefono = telefono
        self.salario = float(salario)
        self.departamento = departamento
        self.fecha_contratacion = fecha_contratacion  # BUG ORIGINAL: decía 'fecha' (no definida)
        self.dia_descanso = dia_descanso

    @abstractmethod
    def get_tipo_empleado(self):
        """Retorna el tipo de empleado como cadena."""
        pass

    @abstractmethod
    def calcular_dias_extra(self, antiguedad):
        """Calcula los días extra de vacaciones según el tipo de empleado.

        Args:
            antiguedad (int): Años de antigüedad del empleado.

        Returns:
            int: Días extra de vacaciones otorgados.
        """
        pass

    def calcular_antiguedad(self):
        """Calcula los años exactos de antigüedad del empleado.

        Returns:
            int: Años de antigüedad completos.
        """
        hoy = date.today()
        c = self.fecha_contratacion
        # BUG ORIGINAL: faltaba descontar si aún no ha pasado el aniversario este año
        return hoy.year - c.year - ((hoy.month, hoy.day) < (c.month, c.day))

    def calcular_edad(self):
        """Calcula la edad actual del empleado en años completos.

        Returns:
            int: Edad en años.
        """
        hoy = date.today()
        n = self.fecha_nacimiento
        # BUG ORIGINAL: faltaba descontar si aún no ha pasado el cumpleaños este año
        return hoy.year - n.year - ((hoy.month, hoy.day) < (n.month, n.day))

    def calcular_meses_laborados(self):
        """Calcula los meses totales laborados desde la contratación.

        Returns:
            int: Meses laborados.
        """
        hoy = date.today()
        c = self.fecha_contratacion
        return (hoy.year - c.year) * 12 + (hoy.month - c.month)

    def campos_modificables(self):
        """Retorna los atributos que pueden actualizarse (sin numero_empleado ni fecha_contratacion).

        Returns:
            list[str]: Nombres de atributos modificables.
        """
        return ["nombre_completo", "fecha_nacimiento", "direccion", "correo",
                "telefono", "salario", "puesto", "departamento", "dia_descanso"]

    def mostrar_info(self):
        """Imprime la información general del empleado."""
        print(f"  Num. Empleado : {self.numero_empleado}")
        print(f"  Tipo          : {self.get_tipo_empleado()}")
        print(f"  Nombre        : {self.nombre_completo}")
        print(f"  Fecha Nac.    : {self.fecha_nacimiento}  ({self.calcular_edad()} años)")
        print(f"  Dirección     : {self.direccion}")
        print(f"  Correo        : {self.correo}")
        print(f"  Teléfono      : {self.telefono}")
        print(f"  Salario       : ${self.salario:,.2f}")
        print(f"  Puesto        : {self.puesto}")
        print(f"  Departamento  : {self.departamento}")
        print(f"  Contratación  : {self.fecha_contratacion}  ({self.calcular_antiguedad()} año(s))")
        print(f"  Día Descanso  : {self.dia_descanso}")

    @abstractmethod
    def a_csv(self):
        """Retorna la representación CSV del empleado."""
        pass

    def __str__(self):
        return f"[{self.numero_empleado}] {self.nombre_completo} ({self.get_tipo_empleado()})"
