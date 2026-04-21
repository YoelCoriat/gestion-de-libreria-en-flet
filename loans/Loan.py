import uuid  # importa la librería uuid para generar identificadores únicos

class Loan:
    # será constructor de la clase Loan (aka préstamo)
    # ejecuta cada vez que se crea un nuevo objeto de tipo Loan
    def __init__(self, book, client):

        # genera un identificador único para cada préstamo
        # uuid4() crea un ID aleatorio que evita duplicados de números
        self.uuid = str(uuid.uuid4())

        # irá guardando una referencia al objeto Book que está siendo prestado
        # permite saber qué libro pertenece a este préstamo
        self.book = book

        # va guardar una referencia al objeto Client que tomó el libro
        # para saber qué cliente tiene el libro prestado
        self.client = client
