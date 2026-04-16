from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ControlBookList import ControlBookList

import flet as ft
"""
TODO:
SUBSCRIBE EN BOOK.PY Y REEMPLAZAR BOOKLIST

"""
@ft.control
class ControlBook(ft.Container):
    def __init__(self, title, author, isbn, state, *args, **kwargs):
        super().__init__()
        self.state = state
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

        self.dropped = False
        self.dropdown_arrow = ft.IconButton(
            icon=ft.Icon(
                icon=ft.Icons.ARROW_DROP_DOWN,
                color="white"),
            on_click=self.on_submit_dropdown)

        self.button_trash = ft.IconButton(
            icon=ft.Icon(icon=ft.Icons.DELETE,
                         color=ft.Colors.RED,
                         size=25),
            on_click=self.on_submit_trash)

        self.checkbox_available = ft.Checkbox(
            label="Disponible",
            value=True,
            on_change=self.checkbox_change)

        self.info_column = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(f"Escrito por: {self.author}", expand=True, size=20)
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"ISBN: {self.isbn}", expand=True, size=20)
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
                            self.title,
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

    def on_submit_dropdown(self, e):
        if not self.dropped:
            self.dropped = True

            self.height = 200
            self.info_column.visible = True
            self.dropdown_arrow.icon = ft.Icon(
                            icon=ft.Icons.ARROW_DROP_UP,
                            color="white")
        else:
            self.dropped = False
            self.dropdown_arrow.icon = ft.Icon(
                            icon=ft.Icons.ARROW_DROP_DOWN,
                            color="white")

            self.height = None
            self.info_column.visible = False

    def on_submit_trash(self, e):
        self.state.books.remove(self)
        self.state.notify()

    def checkbox_change(self, e):
        self.available = self.checkbox_available.value

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
