"""Módulo con el catálogo de vacaciones según la Ley Federal del Trabajo."""


class CatalogoVacaciones:
    """Catálogo de días de vacaciones por años de antigüedad (LFT México).

    Tabla oficial:
        Año 1      → 12 días
        Año 2      → 14 días
        Año 3      → 16 días
        Año 4      → 18 días
        Año 5      → 20 días
        6-10 años  → 22 días
        11-15 años → 24 días
        16-20 años → 26 días
        21-25 años → 28 días
        26-30 años → 30 días
        31-35 años → 32 días
    """

    # Cada entrada: (anio_min, anio_max, dias_vacaciones)
    _TABLA = [
        (1,  1,  12),
        (2,  2,  14),
        (3,  3,  16),
        (4,  4,  18),
        (5,  5,  20),
        (6,  10, 22),
        (11, 15, 24),
        (16, 20, 26),
        (21, 25, 28),
        (26, 30, 30),
        (31, 35, 32),
    ]

    def obtener_dias(self, antiguedad):
        """Retorna los días de vacaciones por ley según la antigüedad.

        Args:
            antiguedad (int): Años de antigüedad del empleado.

        Returns:
            int: Días de vacaciones (0 si < 1 año, 32 si > 35 años).
        """
        if antiguedad < 1:
            return 0
        for anio_min, anio_max, dias in self._TABLA:
            if anio_min <= antiguedad <= anio_max:
                return dias
        return 32  # Para antigüedad > 35 años se mantiene el máximo

    def mostrar(self):
        """Imprime el catálogo completo de vacaciones."""
        sep = "=" * 45
        print(f"\n{sep}")
        print(f"{'CATÁLOGO DE VACACIONES':^45}")
        print(sep)
        print(f"  {'AÑOS LABORADOS':<22} {'DÍAS':>8}")
        print("-" * 45)
        etiquetas = [
            "Año 1", "Año 2", "Año 3", "Año 4", "Año 5",
            "6 a 10 años", "11 a 15 años", "16 a 20 años",
            "21 a 25 años", "26 a 30 años", "31 a 35 años",
        ]
        for etiqueta, (_, _, dias) in zip(etiquetas, self._TABLA):
            print(f"  {etiqueta:<22} {dias:>6} días")
        print(sep)

    def a_csv(self):
        """Retorna el catálogo como lista de líneas CSV.

        Returns:
            list[str]: Líneas con formato 'anio_min,anio_max,dias'.
        """
        return [f"{a},{b},{d}" for a, b, d in self._TABLA]
