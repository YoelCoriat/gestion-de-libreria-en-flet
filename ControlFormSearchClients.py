import flet as ft

"""
ControlFormSearchClients: Campo de busqueda para filtrar la lista de clientes.

Analogo a ControlFormSearchBooks. Al modificar el texto, notifica al AppState
para que actualice el filtro de busqueda y sincronice la UI.

Busca por nombre completo (nombre + apellido) o por cedula.
"""


@ft.control
class ControlFormSearchClients(ft.Container):
    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state

        self.text_field = ft.TextField(
            on_change=self.on_change,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            label="Buscar por nombre o cedula",
        )

        self.content = self.text_field
        self.padding = 10
        self.spacing = 2

        self.text_field.label_style = ft.TextStyle(color=ft.Colors.GREY)
        self.text_field.border_color = "grey"
        self.text_field.counter_style = ft.TextStyle(color=None)

    def on_change(self, e):
        """Actualiza el filtro de busqueda en AppState cada vez que cambia el texto."""
        self.state.update_search_filter_clients(self.text_field.value.strip())
