import flet as ft
from clients.ControlClient import ControlClient

"""
ControlClientList: Control que muestra una lista de clientes.

Clase base análoga a ControlBookList. Hereda de ft.Container y mantiene
internamente un ListView que se sincroniza con AppState a traves del
metodo force_sync (registrado via state.subscribe en main.py).

Las subclases pueden sobrescribir get_allowed_clients() para filtrar
la lista segun criterios especificos (busqueda, estado, etc.).
"""


@ft.control
class ControlClientList(ft.Container):
    def __init__(self, state):
        super().__init__()
        self.width = 700
        self.padding = 10
        self.border_radius = 10
        self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)

        self.state = state

        self.empty_text = ft.Text(
            value="Sin clientes",
            size=45,
            text_align=ft.TextAlign.CENTER,
            opacity=0.2)

        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        self.content = self.list_view

    def get_allowed_clients(self):
        """
        Retorna la lista de clientes a mostrar.
        Las subclases pueden sobrescribir este metodo para filtrar.
        """
        return self.state.clients

    def force_sync(self):
        """
        Sincroniza la vista con el AppState.
        Se llama automaticamente cuando AppState llama a .notify().
        """
        self.list_view.controls.clear()

        clients = self.get_allowed_clients()

        if not clients:
            self.list_view.controls.append(
                ft.Container(
                    content=self.empty_text,
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                )
            )
        else:
            for client in clients:
                self.list_view.controls.append(
                    ControlClient(
                        client=client,
                        state=self.state,
                    )
                )

        self.list_view.update()
