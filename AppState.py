from Book import Book

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
        print(self.search_filter_books)
