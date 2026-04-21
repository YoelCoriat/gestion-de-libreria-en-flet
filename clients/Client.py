import uuid

"""
Estructura de datos de Cliente para almacenar en AppState.
Cada cliente tiene un nombre, apellido, cedula/ID (identificador unico),
y un uuid interno para verificaciones de integridad.
"""

class Client:
    def __init__(self, name, last_name, cedula, dropped=False):
        self.name = name
        self.last_name = last_name
        self.cedula = cedula  # Identificador unico visible para el usuario
        self.dropped = dropped
        # El uuid se usa internamente para verificar integridad
        self.uuid = str(uuid.uuid4())

    @property
    def full_name(self):
        """Retorna el nombre completo del cliente."""
        return f"{self.name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.cedula})"