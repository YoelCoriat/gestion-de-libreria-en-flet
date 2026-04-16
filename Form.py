import flet as ft

@ft.control
class Form(ft.Column):
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
        if color is None:
            self.text_field.label_style = ft.TextStyle(color=ft.Colors.GREY)
            self.text_field.border_color = "grey"
            self.text_field.counter_style = ft.TextStyle(color=color)

        else:
            self.text_field.label_style = ft.TextStyle(color=color)
            self.text_field.border_color = color
            self.text_field.counter_style = ft.TextStyle(color=color)

    def wrong(self, error_text):
        self.change_color("red")
        self.error_text.value = error_text

    def valid(self):
        self.change_color()
        self.error_text.value = ""

    def on_focus(self):
        self.change_color()

    def on_submit(self, e):
        if self.on_submit_callback:
            self.on_submit_callback(e)