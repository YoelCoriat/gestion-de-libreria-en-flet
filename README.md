
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

La Parte B o segunda parte se  agrega la gestión de clientes siguiendo el mismo patrón de arquitectura de la Parte A.

Se creó la clase Client para almacenar nombre, apellido, cédula y uuid de cada cliente.

El formulario ControlAddClient valida que los campos no estén vacíos y que la cédula
no esté duplicada antes de registrar. ControlClient es la tarjeta visual de cada cliente,
expandible para ver el detalle completo y con botón para eliminar.

ControlClientList muestra la lista sincronizada con AppState mediante force_sync y
state.subscribe(). ControlFilteredClientList hereda de esta y filtra por nombre o cédula
según lo que escriba el usuario en ControlFormSearchClients.

Se modificaron AppState.py y main.py para integrar los métodos y controles de clientes
en el Tab correspondiente.
