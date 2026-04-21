from __future__ import annotations

import flet as ft
from clients.ControlFormAddClient import ControlFormAddClient
from clients.Client import Client

"""
ControlAddClient: Panel para registrar nuevos clientes en el sistema.

Analogo a ControlAddBook . Provee un formulario con los campos:
  - Nombre
  - Apellido
  - Cedula/ID (identificador unico)

Valida que todos los campos esten completos y que la cedula sea unica
(no exista otro cliente con la misma cedula). Al confirmar, crea un objeto
Client y lo agrega al AppState.

Incluye una subclase interna _ButtonAddClient para manejar el boton de submit,
siguiendo el mismo patron que ControlAddBook._ButtonAddBook.
"""


@ft.control
class ControlAddClient(ft.Container):

    @ft.control
    class _ButtonAddClient(ft.OutlinedButton):
        def __init__(self, on_submit_callback, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.content = "Registrar Cliente"
            self.on_submit_callback = on_submit_callback
            self.on_click = self.on_submit
            self.style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=4),
                bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
            )
            self.height = 35

        def on_submit(self, e):
            self.on_submit_callback(e)

    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
        self.width = 550
        self.height = 320
        self.border_radius = 13

        self.state = state

        self.name_field = ControlFormAddClient(
            label="Nombre",
            width=500,
            max_length=50,
            on_submit_callback=self.event_add_client,
        )

        self.last_name_field = ControlFormAddClient(
            label="Apellido",
            width=500,
            max_length=50,
            on_submit_callback=self.event_add_client,
        )

        self.cedula_field = ControlFormAddClient(
            label="Cedula / ID",
            width=350,
            max_length=20,
            hint_text="Ej: 8-123-4567",
            on_submit_callback=self.event_add_client,
        )

        self.button_add_client = self._ButtonAddClient(
            on_submit_callback=self.event_add_client
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.name_field],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[self.last_name_field],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        self.cedula_field,
                        ft.Container(
                            content=self.button_add_client,
                            padding=ft.Padding.only(top=25, right=1),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )

    def _cedula_exists(self, cedula: str) -> bool:
        """Verifica si ya existe un cliente con la misma cedula en el AppState."""
        return self.state.get_client_by_cedula(cedula) is not None

    def event_add_client(self, e):
        """
        Valida los campos y agrega el cliente al AppState si todo es correcto.
        Retorna True si el cliente fue agregado, False en caso de error.
        """
        error = False

        if self.name_field.text_field.value.strip() == "":
            error = True
            self.name_field.wrong("El nombre no puede estar vacio")
        else:
            self.name_field.valid()

        if self.last_name_field.text_field.value.strip() == "":
            error = True
            self.last_name_field.wrong("El apellido no puede estar vacio")
        else:
            self.last_name_field.valid()

        cedula_value = self.cedula_field.text_field.value.strip()

        if cedula_value == "":
            error = True
            self.cedula_field.wrong("La cedula no puede estar vacia")
        elif self._cedula_exists(cedula_value):
            error = True
            self.cedula_field.wrong("Ya existe un cliente con esa cedula")
        else:
            self.cedula_field.valid()

        if error:
            return False

        # Todo correcto: crear cliente y agregar al estado
        self.state.add_client(
            Client(
                name=self.name_field.text_field.value.strip(),
                last_name=self.last_name_field.text_field.value.strip(),
                cedula=cedula_value,
            )
        )

        # Limpiar los campos despues de agregar exitosamente
        self.name_field.text_field.value = ""
        self.last_name_field.text_field.value = ""
        self.cedula_field.text_field.value = ""
        self.name_field.text_field.update()
        self.last_name_field.text_field.update()
        self.cedula_field.text_field.update()

        return True
