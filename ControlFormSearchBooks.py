import flet as ft

"""
Form de busqueda de libros. Esta enlazado con AppState al cambiar el texto
"""
@ft.control
class ControlFormSearchBooks(ft.Container):
    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state
        self.text_field = ft.TextField(
            *args,
            **kwargs,
            on_change=self.on_change,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            label="Buscar Titulo",
            )

        self.content = self.text_field

        self.padding=10

        self.spacing = 2

        self.text_field.label_style = ft.TextStyle(color=ft.Colors.GREY)
        self.text_field.border_color = "grey"
        self.text_field.counter_style = ft.TextStyle(color=None)

    def on_change(self, e):
        self.state.update_search_filter_books(self.text_field.value.strip())