import flet as ft

from books.ControlBookList import ControlBookList
from books.ControlAddBook import ControlAddBook
from AppState import AppState
from books.ControlAvailableBookList import ControlAvailableBookList
from loans.ControlLoanBook import ControlLoanBook
from loans.ControlLoanList import ControlLoanList
from books.ControlUnavailableBooklist import ControlUnavailableBookList
from books.ControlFormSearchBooks import ControlFormSearchBooks
from clients.ControlFilteredClientList import ControlFilteredClientList
from clients.ControlFormSearchClients import ControlFormSearchClients
from clients.ControlAddClient import ControlAddClient

"""
Punto de entrada del programa. Se encarga unicamente del posicionamiento
de la UI y de la inicializacion y suscripcion de los controles al AppState.

Toda la logica de datos de nuestro programavive en AppState.py.
Cada control recibe una referencia al AppState al inicializarse, y se
suscribe con state.subscribe(force_sync) para actualizarse automaticamente
cada vez que AppState llama a notify().

Estructura de tabs:
  Tab 1 - Agregar Libros : formulario + lista general de libros
  Tab 2 - Libros         : libros disponibles vs no disponibles con busqueda
  Tab 3 - Clientes       : registro y busqueda de clientes
  Tab 4 - Prestamos      : formulario de prestamo + lista de prestamos activos
"""

#Todo gran programa empezo siendo un “Hola Mundo” lleno de bugs.
#si continuamos compilando, el proximo commit puede ser legendario.


def main(page: ft.Page):
    page.title = "Gestion de Libros"
    main_column = ft.Column(controls=[])
    page.add(
        ft.SafeArea(
            content=ft.Container(content=main_column),
            expand=True,
        )
    )

    state = AppState()

    #  Libros 
    control_book_list = ControlBookList(state)
    state.subscribe(control_book_list.force_sync)

    available_control_book_list = ControlAvailableBookList(state)
    state.subscribe(available_control_book_list.force_sync)

    unavailable_control_book_list = ControlUnavailableBookList(state)
    state.subscribe(unavailable_control_book_list.force_sync)

    form_search = ControlFormSearchBooks(state)
    add_book = ControlAddBook(state)

    #  Clientes 
    # Se instancian los controles de clientes y se suscriben al AppState
    # para sincronizarse automaticamente con cada cambio en state.clients.
    filtered_client_list = ControlFilteredClientList(state)
    state.subscribe(filtered_client_list.force_sync)
    form_search_clients = ControlFormSearchClients(state)
    add_client = ControlAddClient(state)

    #  Prestamos 
    # ControlLoanBook: formulario para seleccionar libro y cliente y crear el prestamo.
    # ControlLoanList: lista de prestamos activos con boton de devolucion por cada uno.
    # Ambos se suscriben al AppState para reflejarse ante cualquier cambio.
    control_loan_book = ControlLoanBook(state)
    state.subscribe(control_loan_book.force_sync)

    control_loan_list = ControlLoanList(state)
    state.subscribe(control_loan_list.force_sync)

    main_column.controls.append(
        ft.Tabs(
            selected_index=0,
            length=4,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Agregar Libros", icon=ft.Icons.ADD),
                            ft.Tab(label="Libros", icon=ft.Icons.BOOK),
                            ft.Tab(label="Clientes", icon=ft.Icons.PERSON),
                            ft.Tab(label="Prestamos", icon=ft.Icons.SWAP_HORIZ),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[

                            # Tab 1 - Agregar Libros
                            ft.Container(
                                content=ft.Row(
                                    controls=[control_book_list, add_book],
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ),

                            # Tab 2 - Libros (disponibles y no disponibles)
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[form_search],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Libros disponibles", size=25),
                                                        ft.Container(
                                                            content=available_control_book_list,
                                                            expand=True,
                                                        )
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                ),
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Libros no disponibles", size=25),
                                                        ft.Container(
                                                            content=unavailable_control_book_list,
                                                            expand=True,
                                                        )
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                ),
                                            ],
                                            vertical_alignment=ft.CrossAxisAlignment.START,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            expand=True,
                                        ),
                                    ]
                                ),
                            ),

                            # Tab 3 - Clientes
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[form_search_clients],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Clientes registrados", size=25),
                                                        ft.Container(
                                                            content=filtered_client_list,
                                                            expand=True,
                                                        ),
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                ),
                                                add_client,
                                            ],
                                            vertical_alignment=ft.CrossAxisAlignment.START,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            expand=True,
                                        ),
                                    ]
                                )
                            ),

                            # Tab 4 - Prestamos
                            # Arriba: formulario para crear prestamo (ControlLoanBook)
                            # Abajo: lista de prestamos activos con opcion de devolucion (ControlLoanList)
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[control_loan_book],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("Préstamos activos", size=25),
                                                        ft.Container(
                                                            content=control_loan_list,
                                                            expand=True,
                                                        ),
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                ),
                                            ],
                                            vertical_alignment=ft.CrossAxisAlignment.START,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            expand=True,
                                        ),
                                    ]
                                ),
                            ),

                        ],
                    ),
                ],
            ),
        ),
    )


ft.run(main)
