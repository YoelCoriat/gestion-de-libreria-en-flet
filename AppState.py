from Book import Book
from Loan import Loan

"""
Este es el centro del programa.
Todos los datos importantes para ser utilizados a traves del programa se deben almacenar aqui para ser accedidos por
los demas controles.
Idealmente definir metodos para cada cambio en el programa, no es ideal llamar .notify() fuera de esta clase.
"""


class AppState:
    def __init__(self):
        self.books = []
        self.clients = []
        self.loans = []
        self._listeners = []
        self.search_filter_books = ""
        self.search_filter_clients = ""

    def subscribe(self, callback):
        self._listeners.append(callback)

    def notify(self):
        for callback in self._listeners:
            callback()

    def add_book(self, book_add):
        self.books.append(book_add)
        self.notify()

    def remove_book(self, book_remove):
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

    # Gestión de Clientes 
    # Se agrego metodos para manejar la lista de clientes y el filtro de búsqueda.
    # Estos siguen el mismo patrón que los métodos de libros de la Parte 1.

    def add_client(self, client):
        self.clients.append(client)
        self.notify()

    def remove_client(self, client_remove):
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

    def get_book_by_uuid(self, book_uuid):
        for book in self.books:
            if book.uuid == book_uuid:
                return book
        return None
    
    # Préstamo de libro
    
    def create_loan(self, book, client):
        book.available = False
        self.loans.append(Loan(book, client))

        self.notify()