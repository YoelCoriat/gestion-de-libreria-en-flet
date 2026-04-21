import flet as ft
from ControlBook import ControlBook

"""
Esta clase controla a una BookList
Sincroniza sus datos a traves de force_sync en un callback en AppState
"""

@ft.control
class ControlBookList(ft.Container):
    def __init__(self, state):
        super().__init__()
        self.width = 700
        self.padding = 10
        self.border_radius = 10
        self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)


        self.state = state

        self.empty_text = ft.Text(
            value="Sin libros",
            size=45,
            text_align=ft.TextAlign.CENTER,
        opacity=0.2)

        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        self.content = self.list_view

    def get_allowed_books(self):
        return self.state.books

    def force_sync(self):
        self.list_view.controls.clear()
        for book in self.get_allowed_books():
            self.list_view.controls.append(
                ControlBook(
                    book=book,
                    state=self.state
                )
            )
        self.list_view.update()
