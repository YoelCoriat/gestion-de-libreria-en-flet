from __future__ import annotations

import flet as ft
from Form import Form
from Book import Book
from BookList import BookList

@ft.control
class AddBook(ft.Container):

    @ft.control
    class _ButtonAddBook(ft.OutlinedButton):
        def __init__(self, on_submit_callback, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.content = "Agregar Libro"
            self.on_submit_callback = on_submit_callback
            self.on_click = self.on_submit
            self.style = ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=4),
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE)
                )
            self.height=35

        def on_submit(self, e):
            self.on_submit_callback(e)

    def __init__(self, book_list: BookList, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
        self.width = 550
        self.height = 300
        self.border_radius = 13

        self.book_list = book_list
        self.title = Form(
            label="Titulo",
            width=500,
            max_length=50,
            on_submit_callback=self.event_add_book)
        self.author = Form(
            label="Autor",
            width=500,
            max_length=50,
            on_submit_callback=self.event_add_book)
        self.isbn = Form(
            label="ISBN",
            width=350,
            max_length=16,
            hint_text="XXX-X-XXXXX-XX-X",
            on_submit_callback=self.event_add_book)

        self.button_add_book = self._ButtonAddBook(on_submit_callback=self.event_add_book)

        self.content = ft.Column(controls=[
            ft.Row(
                controls=[
                    self.title],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER),

            ft.Row(
                controls=[
                    self.author],
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER),

            ft.Row(
                controls=[
                    self.isbn,
                    ft.Container(
                        content=self.button_add_book,
                        padding=ft.Padding.only(top=25, right=1))],
                vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.CENTER,
            )
        ])

    def event_add_book(self, e):
        return self.add_book()

    def add_book(self):
        error = False
        if self.title.text_field.value == "":
            error = True
            self.title.wrong("Titulo no puede estar vacio")
        else:
            self.title.valid()

        if self.author.text_field.value == "":
            error = True
            self.author.wrong("Autor no puede estar vacio")
        else:
            self.author.valid()

        if len(self.isbn.text_field.value) < 16:
            error = True
            self.isbn.wrong("Ingrese un ISBN correcto")
        else:
            self.isbn.valid()

        if error:
            return 0

        self.book_list.add_book(Book(
            title=self.title.text_field.value,
        author=self.author.text_field.value,
        isbn=self.isbn.text_field.value,
        book_list=self.book_list)
        )

        self.book_list.update()
        return 1

if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "AddBook"
        book_list = BookList()
        add_book = AddBook(book_list)
        page.add(add_book)

    ft.run(main)