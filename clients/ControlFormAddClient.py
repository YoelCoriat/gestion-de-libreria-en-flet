import flet as ft

"""
ControlFormAddClient: Subclase de formulario para agregar clientes.

Esta clase es análoga a ControlFormAdd utilizada en la gestión de libros.
Reutiliza el mismo patron visual (TextField con validacion de error en rojo)
para mantener consistencia en la interfaz.

Se puede heredar directamente de ControlFormAdd si se desea, pero se reimplementa
aqui para mayor claridad y para evitar acoplamientos innecesarios.
"""


@ft.control
class ControlFormAddClient(ft.Column):
    def __init__(self, on_submit_callback=None, *args, **kwargs):
        super().__init__()

        self.on_submit_callback = on_submit_callback

        self.text_field = ft.TextField(
            *args,
            **kwargs,
            on_focus=self.on_focus,
            on_submit=self.on_submit,
            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
        )

        self.error_text = ft.Text(
            value=" ",
            color="red",
            size=12
        )

        self.change_color()

        self.controls = [
            self.error_text,
            self.text_field
        ]

        self.spacing = 2

    def change_color(self, color=None):
        """Cambia el color del borde y la etiqueta del campo."""
        if color is None:
            self.text_field.label_style = ft.TextStyle(color=ft.Colors.GREY)
            self.text_field.border_color = "grey"
            self.text_field.counter_style = ft.TextStyle(color=color)
        else:
            self.text_field.label_style = ft.TextStyle(color=color)
            self.text_field.border_color = color
            self.text_field.counter_style = ft.TextStyle(color=color)

    def wrong(self, error_text):
        """Marca el campo como invalido con un mensaje de error."""
        self.change_color("red")
        self.error_text.value = error_text

    def valid(self):
        """Marca el campo como valido y limpia el mensaje de error."""
        self.change_color()
        self.error_text.value = ""

    def on_focus(self, e):
        """Al hacer foco, se resetea el color del campo."""
        self.change_color()

    def on_submit(self, e):
        """Dispara el callback si fue provisto."""
        if self.on_submit_callback:
            self.on_submit_callback(e)
