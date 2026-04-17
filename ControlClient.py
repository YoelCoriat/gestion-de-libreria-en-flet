from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ControlClientList import ControlClientList

import flet as ft
from Client import Client

"""
ControlClient: Control visual para mostrar un cliente individual dentro de una lista.

Diseñado de forma analoga a ControlBook, con las siguientes funcionalidades:
- Muestra nombre completo y cedula siempre visibles
- Se puede expandir (dropdown) para ver detalles: nombre, apellido, cedula
- Boton de eliminar cliente
- Indicador de color para identificacion rapida

El estado de expansion (dropped) se almacena en el objeto Client para que
la UI recuerde si el control estaba abierto o cerrado al sincronizarse.
"""


@ft.control
class ControlClient(ft.Container):
    def __init__(self, client: Client, state, *args, **kwargs):
        super().__init__()
        self.client = client
        self.state = state

        self.dropdown_arrow = ft.IconButton(
            icon=ft.Icon(
                icon=ft.Icons.ARROW_DROP_DOWN,
                color="white"),
            on_click=self.on_submit_dropdown_arrow)

        self.button_trash = ft.IconButton(
            icon=ft.Icon(
                icon=ft.Icons.DELETE,
                color=ft.Colors.WHITE,
                size=25),
            on_click=self.on_submit_trash)

        # Detalle expandido del cliente
        self.info_column = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(f"Nombre: {self.client.name}", expand=True, size=18),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"Apellido: {self.client.last_name}", expand=True, size=18),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text(f"Cedula: {self.client.cedula}", expand=True, size=18),
                    ],
                ),
                ft.Row(
                    controls=[self.button_trash],
                    alignment=ft.MainAxisAlignment.END,
                )
            ],
            visible=False
        )

        # Vista compacta (siempre visible)
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.Icons.PERSON,
                            color=ft.Colors.WHITE,
                            size=25),
                        ft.Text(
                            self.client.full_name,
                            expand=True,
                            size=22),
                        ft.Text(
                            f"CI: {self.client.cedula}",
                            size=14,
                            color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
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
        """Alterna la expansion del panel de detalles."""
        self.client.dropped = not self.client.dropped
        self.update_dropdown()
        self.state.notify()

    def update_dropdown(self):
        """Actualiza la UI segun si el panel esta expandido o no."""
        if self.client.dropped:
            self.height = 210
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
        """Elimina el cliente a traves del AppState."""
        self.state.remove_client(self.client)
