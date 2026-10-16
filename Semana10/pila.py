from nodo import Nodo


class PilaVaciaError(IndexError):
    """Se intentó operar sobre una pila vacía."""


class PilaEnlazada:
    """Pila LIFO sobre nodos: apila y desapila por la cabeza. Todo O(1)."""

    def __init__(self):
        self._cabeza = None
        self._tamaño = 0

    def esta_vacia(self):
        return self._cabeza is None

    def tamaño(self):
        return self._tamaño

    def apilar(self, elemento):
        self._cabeza = Nodo(elemento, self._cabeza)
        self._tamaño += 1

    def desapilar(self):
        if self.esta_vacia():
            raise PilaVaciaError("desapilar sobre pila vacía")
        nodo = self._cabeza
        self._cabeza = nodo.siguiente
        self._tamaño -= 1
        return nodo.dato

    def tope(self):
        if self.esta_vacia():
            raise PilaVaciaError("tope sobre pila vacía")
        return self._cabeza.dato

    def __len__(self):
        return self._tamaño