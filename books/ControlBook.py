from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ControlBookList import ControlBookList

"""
Control visual de un libro individual dentro de una lista.

Funcionalidades:
- Muestra el título del libro y su estado (Disponible y No disponible) siempre visibles.
- Se puede expandir con una flecha para ver autor, ISBN y el boton de eliminar.
- El checkbox de disponibilidad está deshabilitado en la UI: el estado lo maneja
  automaticamente el sistema de prestamos a traves de AppState.
- El boton de eliminar se deshabilita visualmente si el libro tiene un prestamo activo,
  y AppState valida esto nuevamente como segunda capa de proteccion.
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
            icon=ft.Icon(icon=ft.Icons.ARROW_DROP_DOWN, color="white"),
            on_click=self.on_submit_dropdown_arrow,
        )

        # Consulta al AppState si el libro tiene un prestamo activo.
        # Esto determina si el boton de eliminar debe estar habilitado o no.
        is_on_loan = self.state.book_has_active_loan(self.book)

        self.button_trash = ft.IconButton(
            icon=ft.Icon(
                icon=ft.Icons.DELETE,
                color=ft.Colors.WHITE if not is_on_loan else ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                size=25,
            ),
            on_click=self.on_submit_trash,
            disabled=is_on_loan,
            tooltip="No se puede eliminar un libro prestado" if is_on_loan else "Eliminar libro",
        )

        # El checkbox está deshabilitado: el estado lo controla el sistema de prestamos.
        self.checkbox_available = ft.Checkbox(
            label="Disponible",
            value=self.book.available,
            on_change=self.checkbox_change,
            disabled=True,
        )

        # Panel de detalles, visible solo cuando el libro está expandido
        self.info_column = ft.Column(
            controls=[
                ft.Row(controls=[ft.Text(f"Escrito por: {self.book.author}", expand=True, size=20)]),
                ft.Row(controls=[ft.Text(f"ISBN: {self.book.isbn}", expand=True, size=20)]),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Prestado actualmente" if is_on_loan else "",
                            size=13,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                            italic=True,
                        ),
                        self.button_trash,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                )
            ],
            visible=False,
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.BOOK, color=ft.Colors.WHITE, size=25),
                        ft.Text(self.book.title, expand=True, size=25),
                        self.checkbox_available,
                        self.dropdown_arrow,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                self.info_column,
            ]
        )

        self.padding = 10
        self.border_radius = 6
        self.bgcolor = ft.Colors.with_opacity(0.08, ft.Colors.WHITE)
        self.update_dropdown()

    def on_submit_dropdown_arrow(self, e):
        """Alterna la expansión del panel de detalles y notifica al AppState."""
        self.book.dropped = not self.book.dropped
        self.update_dropdown()
        self.state.notify()

    def update_dropdown(self):
        """Actualiza la UI según si el panel está expandido o no."""
        if self.book.dropped:
            self.height = 200
            self.info_column.visible = True
            self.dropdown_arrow.icon = ft.Icon(icon=ft.Icons.ARROW_DROP_UP, color="white")
        else:
            self.dropdown_arrow.icon = ft.Icon(icon=ft.Icons.ARROW_DROP_DOWN, color="white")
            self.height = None
            self.info_column.visible = False

    def on_submit_trash(self, e):
        """
        Solicita al AppState eliminar el libro.
        AppState verifica internamente que no tenga préstamo activo antes de eliminarlo.
        """
        self.state.remove_book(self.book)

    def checkbox_change(self, e):
        self.state.set_book_available(self.book, self.checkbox_available.value)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
