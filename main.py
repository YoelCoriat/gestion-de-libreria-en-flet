import flet as ft

from ControlBookList import ControlBookList
from ControlAddBook import ControlAddBook
from AppState import AppState
from ControlAvailableBookList import ControlAvailableBookList
from ControlUnavailableBooklist import ControlUnavailableBookList
from ControlFormSearchBooks import ControlFormSearchBooks

"""
La forma que funciona el codigo en su esencia es que todos los datos importantes se almacenan en AppState.py y sus atributos.
Al inicializar a cada clase de control se pasa una instancia de "AppState" donde todos los datos se encuentran.
Cada vez que se realiza un cambio que haria alguna diferencia en las listas, o en los datos de informacion,
se notifica al AppState para que ajuste y sincronize todos los cambios.
Cada clase de control tiene la instancia de AppState en sus atributos, y puede referirla para acceder a los datos del programa.

La logica es bastante simple, pero el alineamiento y el ajuste de los controles es lo que toma la mayoria del codigo.
Un ejemplo de este comportamiento puede ser en el caso de AddBook:
        
        self.state.add_book(Book(
            title=self.title.text_field.value,
        author=self.author.text_field.value,
        isbn=self.isbn.text_field.value))

Al querer añadir un libro, se va a el AppState que se pasó al inicializar la clase y se acceden sus metodos diseñados
para cada funcion

Estos datos se comparten entre todos los diferentes controles, y cada vez que se hace un cambio se notifica a la clase
de AppState con .notify().
Es preferible no llamar a .notify() fuera de la clase, si no que intentar realizar todos los .notify() dentro de la clase,
ya que es un proceso que es un poco "expensive" ya que refrezca todos los datos en los controles

La forma que AppState sincroniza los cambios con las clases, es a traves de state.subscribe.
Se pasa un metodo en callback que corre cada vez que se llama .notify(), y de esta forma se sincronizan los cambios
Toda la logica se realiza dentro de estos programas, y main es solamente posicionamiento de UI de los controles (y la
inicializacion del AppState y sincronizacion con las clases control)
"""

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

    # Aqui es donde se sincronizan todas las clases de control y el AppState
    # Los metodos de sincronizacion generalmente se llaman .force_sync
    state = AppState()

    control_book_list = ControlBookList(state)
    state.subscribe(control_book_list.force_sync)

    available_control_book_list = ControlAvailableBookList(state)
    state.subscribe(available_control_book_list.force_sync)

    unavailable_control_book_list = ControlUnavailableBookList(state)
    state.subscribe(unavailable_control_book_list.force_sync)

    form_search = ControlFormSearchBooks(state)
    add_book = ControlAddBook(state)

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
                                    ft.Column(
                                        controls=[

                                            ft.Row(
                                                controls=[form_search
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,
                                            ),

                                            ft.Row(
                                                controls=[

                                                    ft.Column(
                                                        controls=[
                                                            ft.Text("Libros disponibles", size=25),
                                                            ft.Container(
                                                                content=available_control_book_list,
                                                                expand=True
                                                            )
                                                        ],
                                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    ),

                                                    ft.Column(
                                                        controls=[
                                                            ft.Text("Libros no disponibles", size=25),
                                                            ft.Container(
                                                                content=unavailable_control_book_list,
                                                                expand=True
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
