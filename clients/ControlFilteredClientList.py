from clients.ControlClientList import ControlClientList
import flet as ft

"""
ControlFilteredClientList: Subclase de ControlClientList que filtra los clientes
segun el termino de busqueda en AppState.

Hereda de ControlClientList y sobreescribe get_allowed_clients() para retornar
solo los clientes cuyo nombre completo o cedula coincida con el filtro.

Este patron es identico al utilizado en ControlAvailableBookList y
ControlUnavailableBookList, para mantener consistencia con la Parte A.
"""


@ft.control
class ControlFilteredClientList(ControlClientList):
    def __init__(self, state):
        super().__init__(state)
        self.width = 700

    def get_allowed_clients(self):
        """
        Retorna los clientes filtrados por el termino de busqueda.
        Filtra por nombre completo (nombre + apellido) o por cedula.
        """
        result = []
        search = self.state.search_filter_clients.lower().strip()

        for client in self.state.clients:
            name_match = search in client.full_name.lower()
            cedula_match = search in client.cedula.lower()
            if name_match or cedula_match:
                result.append(client)

        return result
