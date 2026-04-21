import flet as ft
from loans.Loan import Loan

"""
Módulo de visualizacin de prestamos activos. Parte C.

Contiene dos clases:

ControlLoanItem: Tarjeta visual de un prestamo individual. Muestra el titulo del
libro y el nombre del cliente que lo tiene. Incluye un boton de devolucion que
llama a state.return_loan(), lo que marca el libro como disponible y elimina
el prestamo de la lista en AppState.

ControlLoanList: Lista de todos los prestamos activos. Se sincroniza con AppState
a traves de force_sync, registrado con state.subscribe() en main.py, siguiendo
el mismo patron que ControlBookList y ControlClientList. Si no hay prestamos,
muestra un mensaje de estado vacio.
"""


@ft.control
class ControlLoanItem(ft.Container):
    """Tarjeta visual de un prestamo individual."""

    def __init__(self, loan: Loan, state):
        super().__init__()
        self.loan = loan
        self.state = state

        # Boton de devolucion: llama a return_loan en AppState,
        # que marca el libro como disponible y elimina el prestamo.
        self.button_return = ft.IconButton(
            icon=ft.Icon(icon=ft.Icons.ASSIGNMENT_RETURN, color=ft.Colors.WHITE, size=22),
            tooltip="Devolver libro",
            on_click=self.on_return,
        )

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(icon=ft.Icons.SWAP_HORIZ, color=ft.Colors.WHITE, size=22),
                        ft.Column(
                            controls=[
                                ft.Text(self.loan.book.title, size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    f"Prestado a: {self.loan.client.full_name}  |  CI: {self.loan.client.cedula}",
                                    size=13,
                                    color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE),
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        self.button_return,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
            ]
        )

        self.padding = 10
        self.border_radius = 6
        self.bgcolor = ft.Colors.with_opacity(0.08, ft.Colors.WHITE)

    def on_return(self, e):
        """Procesa la devolucion del libro a traves del AppState."""
        self.state.return_loan(self.loan)


@ft.control
class ControlLoanList(ft.Container):
    """
    Lista de todos los prestamos activos.

    Se suscribe al AppState mediante state.subscribe(force_sync) en main.py.
    Cada vez que se crea o devuelve un prestamo, AppState llama a notify(),
    que dispara force_sync() y reconstruye la lista automaticamente.
    """

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.width = 700
        self.padding = 10
        self.border_radius = 10
        self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)

        self.empty_text = ft.Text(
            value="Sin préstamos activos",
            size=35,
            text_align=ft.TextAlign.CENTER,
            opacity=0.2,
        )

        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        self.content = self.list_view

    def force_sync(self):
        """
        Reconstruye la lista de prestamos desde AppState.
        Se llama automaticamente cada vez que AppState ejecuta notify().
        """
        self.list_view.controls.clear()

        if not self.state.loans:
            self.list_view.controls.append(
                ft.Container(
                    content=self.empty_text,
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                )
            )
        else:
            for loan in self.state.loans:
                self.list_view.controls.append(
                    ControlLoanItem(loan=loan, state=self.state)
                )

        self.list_view.update()
