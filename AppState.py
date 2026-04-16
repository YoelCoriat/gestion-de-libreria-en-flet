from Book import Book

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

        self._listeners = []

        self.search_filter_books = ""

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
