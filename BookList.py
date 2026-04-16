import flet as ft
from Book import Book

@ft.control
class BookList(ft.Container):
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

        self.content = self.empty_text

    def add_book(self, book: Book):
        if not self.state.books:
            self.content = self.list_view

        self.state.books.append(book)
        self.list_view.controls.append(book)
        self.state.notify()

    def remove_book(self, book: Book):
        self.state.books.remove(book)
        self.list_view.controls.remove(book)

        if not self.state.books:
            self.content = self.empty_text
        self.state.notify()

    def force_update(self):
        if not self.state.books:
            self.content = self.empty_text
        else:
            self.content = self.list_view


    def force_sync(self):
        self.force_update()



