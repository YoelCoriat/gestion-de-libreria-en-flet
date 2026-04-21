import flet as ft

# Esta clase representa el control de la interfaz para realizar préstamos de libros
# Hereda de ft.Column, significa que los elementos se organizarán verticalmente en la pantalla

@ft.control
class ControlLoanBook(ft.Container):
    def __init__(self, state):
        super().__init__()
        self.width = 700
        self.padding = 10
        self.border_radius = 10
        self.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.state = state

        @ft.control
        class _DropdownLoan(ft.Dropdown):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.editable = True
                self.width = 300
                self.border_color = "grey"
                self.filled = True
                self.fill_color = ft.Colors.with_opacity(0.2, ft.Colors.BLACK)
                self.disabled = True
                self.options = []

            def set_options(self, options):
                self.options = options
                if options:
                    self.disabled = False
                else:
                    self.disabled = True

        class _ButtonLoan(ft.Button):
            def __init__(self, on_submit_callback, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.content = ft.Text("Prestar Libro")
                self.on_click = on_submit_callback
                self.disabled = True


        self.book_dropdown = _DropdownLoan(
            label="Seleccionar Libro",
            on_text_change=self.on_change_dropdown,
            on_select=self.on_change_dropdown,
            on_focus=self.on_change_dropdown,
            on_blur=self.on_change_dropdown,
            )

        self.client_dropdown = _DropdownLoan(
            label="Seleccionar Cliente",
            on_text_change=self.on_change_dropdown,
            on_select=self.on_change_dropdown,
            on_focus=self.on_change_dropdown,
            on_blur=self.on_change_dropdown,
            )

        self.loan_button = _ButtonLoan(
            content=ft.Text("Prestar Libro"),
            on_submit_callback=self.on_submit
        )

        self.content = ft.Column(
            controls=[
                self.book_dropdown,
                self.client_dropdown,
                self.loan_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def on_submit(self, e):
        self.state.create_loan(
            self.state.get_book_by_uuid(self.book_dropdown.value),
            self.state.get_client_by_uuid(self.client_dropdown.value)
        )

    def check_valid(self):
        valid_book = any(
            option.key == self.book_dropdown.value
            for option in self.book_dropdown.options
        )

        valid_client = any(
            option.key == self.client_dropdown.value
            for option in self.client_dropdown.options
        )

        self.loan_button.disabled = not (valid_book and valid_client)
        self.loan_button.update()


    def on_change_dropdown(self, e):
        self.check_valid()

    def force_sync(self):
        self.book_dropdown.set_options([ft.DropdownOption(text=book.title, key=book.uuid) for book in self.state.books if book.available])
        self.book_dropdown.update()

        self.client_dropdown.set_options([ft.DropdownOption(text=client.full_name, key=client.uuid) for client in self.state.clients])
        self.client_dropdown.update()

        self.check_valid()

