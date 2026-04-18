import flet as ft

# Esta clase representa el control de la interfaz para realizar préstamos de libros
# Hereda de ft.Column, significa que los elementos se organizarán verticalmente en la pantalla
class ControlLoanBook(ft.Column):

    # Se ejecuta cuando se crea el control dentro de la aplicación
    def __init__(self, state):
        super().__init__()

        # permite acceder a la lista de libros, clientes y métodos como create_loan()
        self.state = state

        # Puede elegir qué libro desea prestar via el dropdown
        self.book_dropdown = ft.Dropdown(label="Seleccionar Libro")

        # Permite elegir qué cliente tomará el libro prestado con el menu
        self.client_dropdown = ft.Dropdown(label="Seleccionar Cliente")

        # Crea un botón que ejecuta la acción de préstamo
        # Cuando el usuario haga clic, se ejecutará el método loan_book
        self.loan_button = ft.ElevatedButton(
            text="Prestar Libro",
            on_click=self.loan_book
        )

        # Define los controles visuales que se mostrarán en la interfaz
        # Como esta clase hereda de Column, se mostrarán uno debajo del otro
        self.controls = [
            self.book_dropdown,
            self.client_dropdown,
            self.loan_button
        ]

    # Método que se ejecuta cuando el usuario presiona el botón "Prestar Libro"
    def loan_book(self, e):

        # Obtiene el UUID del libro seleccionado en el menú tipo dropdown
        book_uuid = self.book_dropdown.value

        # Obtiene la cédula del cliente seleccionado
        client_cedula = self.client_dropdown.value

        # Llama al método create_loan del AppState
        # Este método se encarga de verificar disponibilidad,
        # crear el objeto Loan y actualizar el estado del libro
        self.state.create_loan(book_uuid, client_cedula)
