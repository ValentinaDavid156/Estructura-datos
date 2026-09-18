# Código base — Semana 06
# Fuente: 01-Momento-1-Contrato-y-secuencia/06-Semana-06-Listas-enlazadas-simples/02-guia-de-laboratorio.html

from nodo import Nodo


class PosicionInvalidaError(IndexError):
    """La posición solicitada está fuera del rango válido."""


class ListaEnlazada:
    """Lista implementada sobre nodos enlazados.

    Atributos internos:
        _cabeza  primer nodo, o None si la lista está vacía
        _cola    último nodo, o None si la lista está vacía
        _tamaño  cantidad de nodos

    Invariantes de representación:
        IR-01: _cabeza is None  <=>  _tamaño == 0  <=>  _cola is None
        IR-02: _cola.siguiente is None siempre
        IR-03: recorrer desde _cabeza llega a _cola en exactamente _tamaño pasos

    Complejidad:
        insertar(0)       -> O(1)
        insertar(tamaño)  -> O(1)   gracias a _cola
        insertar(i)       -> O(n)
        obtener(i)        -> O(n)   ¡no hay acceso directo!
        eliminar(0)       -> O(1)
        eliminar(tamaño-1)-> O(n)   hay que llegar al penúltimo
        buscar            -> O(n)
    """

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamaño = 0

    def tamaño(self):
        return self._tamaño

    def obtener(self, posicion):
        self._validar(posicion, incluir_final=False)
        return self._nodo_en(posicion).dato

    def insertar(self, posicion, elemento):
        self._validar(posicion, incluir_final=True)
        if posicion == 0:
            self._insertar_al_inicio(elemento)
        elif posicion == self._tamaño:
            self._insertar_al_final(elemento)
        else:
            self._insertar_en_medio(posicion, elemento)
        self._tamaño += 1

    def eliminar(self, posicion):
        self._validar(posicion, incluir_final=False)
        if posicion == 0:
            dato = self._eliminar_primero()
        else:
            dato = self._eliminar_no_primero(posicion)
        self._tamaño -= 1
        return dato

    def buscar(self, elemento):
        actual, i = self._cabeza, 0
        while actual is not None:
            if actual.dato == elemento:
                return i
            actual, i = actual.siguiente, i + 1
        return -1

    # ---------- CASO 1: insertar al inicio ----------
    def _insertar_al_inicio(self, elemento):
        """O(1). Cuidado: si la lista estaba vacía, también hay que fijar _cola."""
        nuevo = Nodo(elemento, self._cabeza)
        self._cabeza = nuevo
        if self._cola is None:          # la lista estaba vacía
            self._cola = nuevo
        # ¿Por qué esta comprobación? Si no la haces, IR-01 se rompe.

    # ---------- CASO 2: insertar al final ----------
    def _insertar_al_final(self, elemento):
        """O(1) gracias a _cola."""
        nuevo = Nodo(elemento)
        if self._cola is None:          # lista vacía: es también la cabeza
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo

    # ---------- CASO 3: insertar en el medio ----------
    def _insertar_en_medio(self, posicion, elemento):
        """O(n). Hay que llegar al nodo ANTERIOR a la posición."""
        anterior = self._nodo_en(posicion - 1)
        # Orden correcto: primero apunta el nuevo al que sigue,
        # después reengancha el anterior.
        nuevo = Nodo(elemento,anterior.siguiente) #El nuevo le apunta al lo que sigue
        anterior.siguiente = nuevo     # El anterior le apunta al nuevo

    # ---------- CASO 4: eliminar el primero ----------
    def _eliminar_primero(self):
        """O(1). Cuidado: si era el único elemento, _cola queda colgando."""
        nodo = self._cabeza
        self._cabeza = nodo.siguiente
        if self._cabeza is None:        # era el único
            self._cola = None
        return nodo.dato

    # ---------- CASO 5: eliminar cualquier otro ----------
    def _eliminar_no_primero(self, posicion):
        """O(n). Si es el último, hay que actualizar _cola."""
        anterior = self._nodo_en(posicion - 1)
        objetivo = anterior.siguiente
        anterior.siguiente = objetivo.siguiente
        if objetivo is self._cola:      # era el último entonces la cola cambia
            self._cola = anterior
        return objetivo.dato

    def _nodo_en(self, posicion):
        """Devuelve el nodo en `posicion`. O(n)."""
        actual = self._cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        return actual

    def _validar(self, posicion, incluir_final):
        limite = self._tamaño if incluir_final else self._tamaño - 1
        if not 0 <= posicion <= limite:
            raise PosicionInvalidaError(
                f"posicion {posicion} fuera de rango [0, {limite}]"
            )

    def __len__(self):
        return self._tamaño

    def __getitem__(self, i):
        return self.obtener(i)

    def __iter__(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self):
        return f"ListaEnlazada({list(self)!r})"
