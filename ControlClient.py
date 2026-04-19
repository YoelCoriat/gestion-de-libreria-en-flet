from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ControlClientList import ControlClientList

import flet as ft
from Client import Client

"""
Control visual de un cliente individual dentro de una lista.

Funcionalidades:
- Muestra nombre completo y cedula siempre visibles en la vista compacta.
- Se puede expandir con una flecha para ver nombre, apellido, cedula y el boton de eliminar.
- El boton de eliminar se deshabilita visualmente si el cliente tiene un prestamo activo,
  y AppState valida esto nuevamente como segunda capa de proteccion.
- El estado de expansión (dropped) se guarda en el objeto Client para que la UI
  recuerde si la tarjeta estaba abierta o cerrada al sincronizarse con force_sync.
"""


@ft.control
class ControlClient(ft.Container):
    def __init__(self, client: Client, state, *args, **kwargs):
        super().__init__()
        self.client = client
        self.state = state

        self.dropdown_arrow = ft.IconButton(
            icon=ft.Icon(icon=ft.Icons.ARROW_DROP_DOWN, color="white"),
            on_click=self.on_submit_dropdown_arrow,
        )

        # Consulta al AppState si el cliente tiene un prestamo activo.
        # Esto determina si el boton de eliminar debe estar habilitado o no.
        is_on_loan = self.state.client_has_active_loan(self.client)

        self.button_trash = ft.IconButton(
            icon=ft.Icon(
                icon=ft.Icons.DELETE,
                color=ft.Colors.WHITE if not is_on_loan else ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
                size=25,
            ),
            on_click=self.on_submit_trash,
            disabled=is_on_loan,
            tooltip="No se puede eliminar un cliente con préstamo activo" if is_on_loan else "Eliminar cliente",
        )

        # Panel de detalles, visible solo cuando el cliente esta expandido completamente
        self.info_column = ft.Column(
            controls=[
                ft.Row(controls=[ft.Text(f"Nombre: {self.client.name}", expand=True, size=18)]),
                ft.Row(controls=[ft.Text(f"Apellido: {self.client.last_name}", expand=True, size=18)]),
                ft.Row(controls=[ft.Text(f"Cedula: {self.client.cedula}", expand=True, size=18)]),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Tiene préstamo activo" if is_on_loan else "",
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

        # Vista compacta - siempre visible
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.PERSON, color=ft.Colors.WHITE, size=25),
                        ft.Text(self.client.full_name, expand=True, size=22),
                        ft.Text(
                            f"CI: {self.client.cedula}",
                            size=14,
                            color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                        ),
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
        self.client.dropped = not self.client.dropped
        self.update_dropdown()
        self.state.notify()

    def update_dropdown(self):
        """Actualiza la UI según si el panel está expandido o no."""
        if self.client.dropped:
            self.height = 210
            self.info_column.visible = True
            self.dropdown_arrow.icon = ft.Icon(icon=ft.Icons.ARROW_DROP_UP, color="white")
        else:
            self.dropdown_arrow.icon = ft.Icon(icon=ft.Icons.ARROW_DROP_DOWN, color="white")
            self.height = None
            self.info_column.visible = False

    def on_submit_trash(self, e):
        """
        Solicita al AppState eliminar el cliente.
        AppState verifica internamente que no tenga prestamo activo antes de eliminarlo.
        """
        self.state.remove_client(self.client)
