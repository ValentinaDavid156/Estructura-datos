# Código base — Semana 09
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/09-Semana-09-Colas/02-guia-de-laboratorio.html

class ColaVaciaError(IndexError):
    """Se intentó operar sobre una cola vacía."""


class ColaCircular:
    """Cola FIFO sobre arreglo circular con redimensionamiento.

    Invariantes de representación:
        IR-01: 0 <= _tamaño <= _capacidad
        IR-02: los elementos ocupan las posiciones
               (_frente + i) % _capacidad  para i en [0, _tamaño)
        IR-03: _frente siempre está en [0, _capacidad)

    Complejidad: encolar O(1) amortizado, desencolar O(1), frente O(1)
    """

    CAPACIDAD_INICIAL = 8

    def __init__(self):
        self._capacidad = self.CAPACIDAD_INICIAL
        self._datos = [None] * self._capacidad
        self._frente = 0
        self._tamaño = 0

    def esta_vacia(self):
        return self._tamaño == 0

    def tamaño(self):
        return self._tamaño

    def encolar(self, elemento):
        if self._tamaño == self._capacidad:
            self._redimensionar(self._capacidad * 2)
        posicion = (self._frente + self._tamaño) % self._capacidad
        pass    # coloca el elemento y actualiza el tamaño

    def desencolar(self):
        if self.esta_vacia():
            raise ColaVaciaError("desencolar sobre cola vacía")
        elemento = self._datos[self._frente]
        self._datos[self._frente] = None        # libera la referencia
        pass    # avanza _frente circularmente y decrementa el tamaño
        return elemento

    def frente(self):
        if self.esta_vacia():
            raise ColaVaciaError("frente sobre cola vacía")
        return self._datos[self._frente]

    def _redimensionar(self, nueva_capacidad):
        """Copia los elementos EN ORDEN a un arreglo nuevo y resetea _frente a 0.

        Ojo: no puedes copiar el arreglo tal cual, porque los elementos
        pueden estar «dados la vuelta».
        """
        nuevos = [None] * nueva_capacidad
        for i in range(self._tamaño):
            nuevos[i] = self._datos[(self._frente + i) % self._capacidad]
        self._datos = nuevos
        self._capacidad = nueva_capacidad
        self._frente = 0

    def __len__(self):
        return self._tamaño

    def __iter__(self):
        for i in range(self._tamaño):
            yield self._datos[(self._frente + i) % self._capacidad]

from nodo import Nodo


class ColaEnlazada:
    """Cola FIFO sobre nodos. Desencola por la cabeza, encola por la cola.

    Invariantes de representación:
        IR-01: _cabeza is None  <=>  _cola is None  <=>  _tamaño == 0
        IR-02: _cola.siguiente is None siempre

    Complejidad: encolar O(1), desencolar O(1), frente O(1)
    """

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamaño = 0

    def esta_vacia(self):
        return self._cabeza is None

    def tamaño(self):
        return self._tamaño

    def encolar(self, elemento):
        nuevo = Nodo(elemento)
        if self._cola is None:
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo
        self._tamaño += 1

    def desencolar(self):
        if self.esta_vacia():
            raise ColaVaciaError("desencolar sobre cola vacía")
        nodo = self._cabeza
        self._cabeza = nodo.siguiente
        if self._cabeza is None:        # era el último
            self._cola = None           # ¡no olvides esta línea!
        self._tamaño -= 1
        return nodo.dato

    def frente(self):
        if self.esta_vacia():
            raise ColaVaciaError("frente sobre cola vacía")
        return self._cabeza.dato

    def __len__(self):
        return self._tamaño
