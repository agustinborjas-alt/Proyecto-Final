"""Módulo con la clase EmpleadoSindicalizado."""

from empleado import Empleado


class EmpleadoSindicalizado(Empleado):
    """Empleado que pertenece a un sindicato.

    Atributo adicional:
        nombre_sindicato (str): Nombre del sindicato al que pertenece.

    Regla de vacaciones:
        Días por ley + 5 días extra a partir del segundo año de antigüedad.
    """

    def __init__(self, numero_empleado, nombre_completo, fecha_nacimiento,
                 direccion, correo, puesto, telefono, salario, departamento,
                 fecha_contratacion, dia_descanso, nombre_sindicato):
        super().__init__(numero_empleado, nombre_completo, fecha_nacimiento,
                         direccion, correo, puesto, telefono, salario,
                         departamento, fecha_contratacion, dia_descanso)
        self.nombre_sindicato = nombre_sindicato

    def get_tipo_empleado(self):
        """Retorna el tipo de empleado."""
        return "Sindicalizado"

    def calcular_dias_extra(self, antiguedad):
        """Retorna 5 días extra si la antigüedad es >= 2 años, 0 en caso contrario.

        Args:
            antiguedad (int): Años de antigüedad.

        Returns:
            int: Días extra de vacaciones.
        """
        # BUG ORIGINAL: el método se llamaba 'calcular_dias_extras' (con 's'),
        # inconsistente con el método abstracto 'calcular_dias_extra'
        return 5 if antiguedad >= 2 else 0

    def campos_modificables(self):
        """Agrega nombre_sindicato a los campos modificables."""
        return super().campos_modificables() + ["nombre_sindicato"]

    def mostrar_info(self):
        """Muestra información completa del empleado sindicalizado."""
        super().mostrar_info()
        print(f"  Sindicato     : {self.nombre_sindicato}")

    def a_csv(self):
        """Retorna la línea CSV del empleado sindicalizado.

        Returns:
            str: Datos separados por coma, con tipo 'S' al inicio.
        """
        return (f"S,{self.numero_empleado},{self.nombre_completo},"
                f"{self.fecha_nacimiento},{self.direccion},{self.correo},"
                f"{self.telefono},{self.salario},{self.puesto},"
                f"{self.departamento},{self.fecha_contratacion},"
                f"{self.dia_descanso},{self.nombre_sindicato}")
