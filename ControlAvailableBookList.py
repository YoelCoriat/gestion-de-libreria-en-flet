from ControlBookList import ControlBookList
import flet as ft

@ft.control
class ControlAvailableBookList(ControlBookList):
    def __init__(self, state):
        super().__init__(state)
        self.width = 600

    def get_allowed_books(self):
        result = []

        search = self.state.search_filter_books.lower().strip()

        for book in self.state.books:
            if book.available:
                if search in book.title.lower():
                    result.append(book)

        return result

