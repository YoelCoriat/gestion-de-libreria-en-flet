from books.ControlAvailableBookList import ControlAvailableBookList
import flet as ft

"""
Hereditario de ControlAvailableBookList que tiene un override al método de get_allowed_books que se actualiza con el AppState
para filtrarse con el buscador.
"""

@ft.control
class ControlUnavailableBookList(ControlAvailableBookList):
    def __init__(self, state):
        super().__init__(state)
        self.width = 600

    def get_allowed_books(self):
        result = []

        search = self.state.search_filter_books.lower().strip()

        for book in self.state.books:
            if not book.available:
                if search in book.title.lower():
                    result.append(book)

        return result

