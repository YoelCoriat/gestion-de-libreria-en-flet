from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ControlBookList import ControlBookList

"""
Este es el control de cada libro. Se puede expandir, y tiene diferentes metodos para todas las diferentes opciones como
expandirse, eliminar, o minimizar
También tiene un checkbox, que al ser apretado se le notifica al AppState a través de un uuid unico por Book que debe
ser notificado a través de un método en AppState.py
"""

import flet as ft
from Book import Book

@ft.control
class ControlBook(ft.Container):
    def __init__(self, book: Book, state, visible=True, *args, **kwargs):
        super().__init__()
        self.book = book
        self.state = state
        self.visible = visible

        self.dropdown_arrow = ft.IconButton(
            icon=ft.Icon(
                icon=ft.Icons.ARROW_DROP_DOWN,
                color="white"),
            on_click=self.on_submit_dropdown_arrow)

        self.button_trash = ft.IconButton(
            icon=ft.Icon(icon=ft.Icons.DELETE,
                         color=ft.Colors.WHITE,
                         size=25),
            on_click=self.on_submit_trash)

        self.checkbox_available = ft.Checkbox(
            label="Disponible",
            value=self.book.available,
            on_change=self.checkbox_change)

        self.info_column = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(f"Escrito por: {self.book.author}", expand=True, size=20)
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"ISBN: {self.book.isbn}", expand=True, size=20)
                    ],
                ),
                ft.Row(
                    controls=[
                        self.button_trash
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )

            ],
            visible=False
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.BOOK,
                                color=ft.Colors.WHITE,
                                size=25),
                        ft.Text(
                            self.book.title,
                            expand=True,
                            size=25
                        ),
                        self.checkbox_available,
                        self.dropdown_arrow,

                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10),
                self.info_column,

            ]
        )

        self.padding = 10
        self.border_radius = 6
        self.bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE)

        self.update_dropdown()


    def on_submit_dropdown_arrow(self, e):
        if self.book.dropped:
            self.book.dropped = False
        else:
            self.book.dropped = True

        self.update_dropdown()
        self.state.notify()

    def update_dropdown(self):
        if self.book.dropped:
            self.height = 200
            self.info_column.visible = True
            self.dropdown_arrow.icon = ft.Icon(
                            icon=ft.Icons.ARROW_DROP_UP,
                            color="white")

        else:
            self.dropdown_arrow.icon = ft.Icon(
                            icon=ft.Icons.ARROW_DROP_DOWN,
                            color="white")
            self.height = None
            self.info_column.visible = False


    def on_submit_trash(self, e):
        self.state.remove_book(self.book)

    def checkbox_change(self, e):
        self.state.set_book_available(self.book, self.checkbox_available.value)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
