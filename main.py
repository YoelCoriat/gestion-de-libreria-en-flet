import flet as ft

from BookList import BookList
from Book import Book
from AddBook import AddBook

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

    class AppState:
        def __init__(self):
            self.books = []
            self.clients = []

            self._listeners = []

        def subscribe(self, callback):
            self._listeners.append(callback)

        def notify(self):
            for callback in self._listeners:
                callback()
            print("update all")

    state = AppState()
    book_list = BookList(state)
    state.subscribe(book_list.force_sync)
    add_book = AddBook(book_list)

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
                                        controls=[book_list,
                                        add_book],
                                        vertical_alignment=ft.CrossAxisAlignment.START,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),
                            ),
                            ft.Container(
                                content=(
                                    ft.Row(
                                        controls=[
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
