"""Estructuras del curso (semanas 7 y 11), ya completas. NO modifiques este archivo."""


class PosicionInvalidaError(IndexError):
    """La posición está fuera del rango válido."""


class NodoDoble:
    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente


class ListaDoble:
    """Lista doblemente enlazada. Posiciones desde 0.
    cabeza es el primer nodo y cola el último; cabeza.anterior y cola.siguiente son None.
    Lista vacía: cabeza is None y cola is None."""

    def __init__(self, datos=()):
        self.cabeza = None
        self.cola = None
        self._tamaño = 0
        for d in datos:
            self.insertar_al_final(d)

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_al_inicio(self, dato):
        nuevo = NodoDoble(dato, None, self.cabeza)
        if self.cabeza is None:
            self.cola = nuevo
        else:
            self.cabeza.anterior = nuevo
        self.cabeza = nuevo
        self._tamaño += 1
        return nuevo

    def insertar_al_final(self, dato):
        nuevo = NodoDoble(dato, self.cola, None)
        if self.cola is None:
            self.cabeza = nuevo
        else:
            self.cola.siguiente = nuevo
        self.cola = nuevo
        self._tamaño += 1
        return nuevo

    def insertar(self, posicion, dato):
        self._validar(posicion, incluir_final=True)
        if posicion == 0:
            return self.insertar_al_inicio(dato)
        if posicion == self._tamaño:
            return self.insertar_al_final(dato)
        siguiente = self._nodo_en(posicion)
        nuevo = NodoDoble(dato, siguiente.anterior, siguiente)
        siguiente.anterior.siguiente = nuevo
        siguiente.anterior = nuevo
        self._tamaño += 1
        return nuevo

    def eliminar_nodo(self, nodo):
        """Desenlaza un nodo en O(1) y devuelve su dato."""
        if nodo.anterior is None:
            self.cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente
        if nodo.siguiente is None:
            self.cola = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior
        self._tamaño -= 1
        return nodo.dato

    def eliminar(self, posicion):
        self._validar(posicion, incluir_final=False)
        return self.eliminar_nodo(self._nodo_en(posicion))

    def _nodo_en(self, posicion):
        """Recorre desde el extremo más cercano."""
        if posicion <= self._tamaño // 2:
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
        else:
            actual = self.cola
            for _ in range(self._tamaño - posicion - 1):
                actual = actual.anterior
        return actual

    def obtener(self, posicion):
        self._validar(posicion, incluir_final=False)
        return self._nodo_en(posicion).dato

    def _validar(self, posicion, incluir_final):
        limite = self._tamaño if incluir_final else self._tamaño - 1
        if not 0 <= posicion <= limite:
            raise PosicionInvalidaError(f"posicion {posicion} fuera de [0, {limite}]")

    def __len__(self):
        return self._tamaño

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __reversed__(self):
        actual = self.cola
        while actual is not None:
            yield actual.dato
            actual = actual.anterior

    def __repr__(self):
        return f"ListaDoble({list(self)!r})"


class NodoArbol:
    def __init__(self, dato, izquierdo=None, derecho=None):
        self.dato = dato
        self.izquierdo = izquierdo
        self.derecho = derecho


class ABB:
    """Árbol binario de búsqueda. No admite duplicados: insertar una clave
    existente no hace nada. Altura: vacío = -1, un solo nodo = 0."""

    def __init__(self, claves=()):
        self.raiz = None
        self._tamaño = 0
        for c in claves:
            self.insertar(c)

    def __len__(self):
        return self._tamaño

    def insertar(self, clave):
        self.raiz = self._insertar(self.raiz, clave)

    def _insertar(self, nodo, clave):
        if nodo is None:
            self._tamaño += 1
            return NodoArbol(clave)
        if clave < nodo.dato:
            nodo.izquierdo = self._insertar(nodo.izquierdo, clave)
        elif clave > nodo.dato:
            nodo.derecho = self._insertar(nodo.derecho, clave)
        return nodo

    def altura(self):
        def h(n):
            return -1 if n is None else 1 + max(h(n.izquierdo), h(n.derecho))
        return h(self.raiz)

    def inorden(self):
        resultado = []
        def rec(n):
            if n:
                rec(n.izquierdo); resultado.append(n.dato); rec(n.derecho)
        rec(self.raiz)
        return resultado
