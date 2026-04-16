from ControlBookList import ControlBookList
import flet as ft

@ft.control
class UnavailableControlBookList(ControlBookList):
    def __init__(self, state):
        super().__init__(state)
        self.width = 600

    def get_allowed_books(self):
        return [book for book in self.state.books if not book.available]