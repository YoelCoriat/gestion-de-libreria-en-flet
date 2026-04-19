import uuid

"""
Estructura de datos de libro para almacenar en AppState
"""
class Book:
    def __init__(self, title, author, isbn, available=True, dropped=False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

        # El uuid se usa ocasionalmente para verificar integridades
        self.uuid = str(uuid.uuid4())

        # Recordatorio a la UI si el elemento estaba expandido o no
        self.dropped = dropped

    def __str__(self):
        return f"{self.title} escrito por {self.author} ({self.isbn})"
