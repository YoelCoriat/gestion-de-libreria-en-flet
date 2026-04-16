import flet as ft

from ControlBookList import ControlBookList
from AddBook import AddBook
from AppState import AppState
from AvailableControlBookList import AvailableControlBookList
from UnavailableControlBooklist import UnavailableControlBookList

def main(page: ft.Page):
    page.title = "Gestion de Libros"
    main_column = ft.Column(
        controls=[],
    )
    page.add(
        ft.SafeArea(
            content=ft.Container(
                content=main_column),
            expand=True,

        )
    )

    state = AppState()

    control_book_list = ControlBookList(state)
    state.subscribe(control_book_list.force_sync)

    available_control_book_list = AvailableControlBookList(state)
    state.subscribe(available_control_book_list.force_sync)

    unavailable_control_book_list = UnavailableControlBookList(state)
    state.subscribe(unavailable_control_book_list.force_sync)

    add_book = AddBook(state)

    main_column.controls.append(
        ft.Tabs(
            selected_index=0,
            length=3,
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
                            ft.Container(
                                content=(
                                    ft.Row(
                                        controls=[control_book_list,
                                        add_book],
                                        vertical_alignment=ft.CrossAxisAlignment.START,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),
                            ),
                            ft.Container(
                                content=(
                                    ft.Row(
                                        controls=[available_control_book_list,
                                                  unavailable_control_book_list
                                                  ],
                                        vertical_alignment=ft.CrossAxisAlignment.START,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),
                            ),
                            ft.Container(
                                content=ft.Text("This is Tab 3"),

                            ),
                            ft.Container(
                                content=ft.Text("This is Tab 4"),

                            ),
                        ],
                    ),
                ],
            ),
        ),
    )

    """
    main_column.controls.append(form_agregar_libros)
    main_column.controls.append(lista_libros)
    """

ft.run(main)
