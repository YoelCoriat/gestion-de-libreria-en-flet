from books.Book import Book
from loans.Loan import Loan

"""
Este es el centro de nuestro programa como proyecto final.
Todos los datos importantes para ser utilizados a traves del programa estan almacendaos aqui para ser accedidos por
los demas controles.

No es ideal llamar .notify() fuera de esta clase.

Reglas de integridad implementadas:
- Un libro no puede eliminarse si tiene un prestamo activo.
- Un cliente no puede eliminarse si tiene un prestamo activo.
- Al devolver un libro, se marca como disponible y se elimina el prestamo de la lista.
"""

#En mi PC todo funciona perfecto.
#El problema es que el mundo no es mi PC.


class AppState:
    def __init__(self):
        self.books = []
        self.clients = []
        self.loans = []        # Lista de préstamos activos
        self._listeners = []
        self.search_filter_books = ""
        self.search_filter_clients = ""

    def subscribe(self, callback):
        self._listeners.append(callback)

    def notify(self):
        for callback in self._listeners:
            callback()

    #  Libros 

    def add_book(self, book_add):
        self.books.append(book_add)
        self.notify()

    def remove_book(self, book_remove):
        # No se permite eliminar un libro que tiene un prestamo activo.
        # ControlBook deshabilita el boton visualmente, pero esta validacion
        # actua como segunda capa de proteccion.
        if self.book_has_active_loan(book_remove):
            return
        for book in self.books:
            if book.uuid == book_remove.uuid:
                self.books.remove(book)
                self.notify()
                return

    def set_book_available(self, book_change_available: Book, available):
        for book in self.books:
            if book.uuid == book_change_available.uuid:
                book.available = available
                self.notify()

    def update_search_filter_books(self, search_filter_books):
        self.search_filter_books = search_filter_books
        self.notify()

    def get_book_by_uuid(self, book_uuid):
        for book in self.books:
            if book.uuid == book_uuid:
                return book
        return None

    def book_has_active_loan(self, book) -> bool:
        """Retorna True si el libro tiene al menos un préstamo activo."""
        return any(loan.book.uuid == book.uuid for loan in self.loans)

    #  Clientes 
    # Metodos para manejar la lista de clientes y el filtro de busqueda.
    # Siguen el mismo patron que los metodos de libros de la Parte A.

    def add_client(self, client):
        self.clients.append(client)
        self.notify()

    def remove_client(self, client_remove):
        # No se permite eliminar un cliente que tiene un prestamo activo.
        # ControlClient deshabilita el boton visualmente, pero esta validacion
        # actúa como segunda capa de protección.
        if self.client_has_active_loan(client_remove):
            return
        for client in self.clients:
            if client.uuid == client_remove.uuid:
                self.clients.remove(client)
                self.notify()
                return

    def update_search_filter_clients(self, search_filter_clients):
        self.search_filter_clients = search_filter_clients
        self.notify()

    def get_client_by_cedula(self, cedula):
        for client in self.clients:
            if client.cedula == cedula:
                return client
        return None

    def get_client_by_uuid(self, uuid):
        for client in self.clients:
            if client.uuid == uuid:
                return client
        return None

    def client_has_active_loan(self, client) -> bool:
        """Retorna True si el cliente tiene al menos un préstamo activo."""
        return any(loan.client.uuid == client.uuid for loan in self.loans)

    # Préstamos 

    def create_loan(self, book, client):
        """
        Crea un préstamo entre un libro y un cliente.
        Marca el libro como no disponible y agrega el préstamo a la lista.
        Notifica a todos los controles suscritos para que se actualicen.
        """
        book.available = False
        self.loans.append(Loan(book, client))
        self.notify()

    def return_loan(self, loan):
        """
        Procesa la devolución de un libro.
        Marca el libro como disponible nuevamente y elimina el préstamo de la lista.
        Notifica a todos los controles para que reflejen el cambio.
        """
        loan.book.available = True
        if loan in self.loans:
            self.loans.remove(loan)
        self.notify()
