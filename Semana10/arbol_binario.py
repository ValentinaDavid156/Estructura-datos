# Código base — Semana 10
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/10-Semana-10-Arboles-binarios-y-recorridos/02-guia-de-laboratorio.html
from cola import ColaEnlazada
class NodoArbol:
    """Un nodo con hasta dos hijos."""

    def __init__(self, dato, izquierdo=None, derecho=None):
        self.dato = dato
        self.izquierdo = izquierdo
        self.derecho = derecho

    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

    def __repr__(self):
        return f"NodoArbol({self.dato!r})"


class ArbolBinario:
    """Árbol binario genérico, sin propiedad de orden.

    En la semana 11 le impondremos la propiedad de orden y se
    convertirá en un BST. Hoy solo lo recorremos.
    """

    def __init__(self, raiz=None):
        self.raiz = raiz

    def esta_vacio(self):
        return self.raiz is None

    # ---------- PREORDEN: raíz, izquierdo, derecho ----------
    def preorden(self):
        """Visita la raíz ANTES de los subárboles.

        Uso típico: copiar o serializar un árbol (reconstruyes desde la raíz).
        Complejidad: O(n) en tiempo, O(h) en espacio por la pila de llamadas.
        """
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado

    def _preorden(self, nodo, acumulador):
        if nodo is None:            # CASO BASE — nunca lo omitas
            return
        acumulador.append(nodo.dato)          # visita
        self._preorden(nodo.izquierdo, acumulador)
        self._preorden(nodo.derecho, acumulador)

    # ---------- INORDEN: izquierdo, raíz, derecho ----------
    def inorden(self):
        """Visita la raíz ENTRE los subárboles.

        Uso típico: en un BST devuelve los elementos ORDENADOS.
        Es el recorrido más importante del curso.
        """
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo, acumulador):
        if nodo is None:                           # completa: mueve la línea de la visita al medio
            return
        self._inorden(nodo.izquierdo, acumulador)
        acumulador.append(nodo.dato)
        self._inorden(nodo.derecho, acumulador)    

    # ---------- POSTORDEN: izquierdo, derecho, raíz ----------
    def postorden(self):
        """Visita la raíz DESPUÉS de los subárboles.

        Uso típico: liberar memoria o borrar un árbol (borras los hijos
        antes que el padre; si lo hicieras al revés, perderías las
        referencias a los hijos).
        """
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado

    def _postorden(self, nodo, acumulador):
        if nodo is None:                        # completa: mueve la línea de la visita al final
            return
        self._postorden(nodo.izquierdo, acumulador)
        self._postorden(nodo.derecho, acumulador)
        acumulador.append(nodo.dato)   

    def por_niveles(self):
        """Visita los nodos nivel por nivel, de izquierda a derecha.

        En el árbol del paso 1 devuelve: [A, B, C, D, E, F, G]

        Algoritmo:
            1. Encola la raíz
            2. Mientras la cola no esté vacía:
               a. Desencola un nodo y visítalo
               b. Encola sus hijos no nulos (izquierdo primero)

        Complejidad: O(n) en tiempo, O(w) en espacio donde w es la
        anchura máxima del árbol.

        PRUEBA ESTO: cambia la cola por una pila. ¿Qué recorrido obtienes?
        (Pista: se parece mucho al preorden, pero con los hijos invertidos.)
        """
        from cola import ColaEnlazada

        if self.esta_vacio():
            return []

        resultado = []
        cola = ColaEnlazada()
        cola.encolar(self.raiz)
        while not cola.esta_vacia():
            nodo = cola.desencolar()
            resultado.append(nodo.dato)
            if nodo.izquierdo is not None:
                cola.encolar(nodo.izquierdo)
            if nodo.derecho is not None:
                cola.encolar(nodo.derecho)
        return resultado


    def por_niveles_agrupado(self):
        """Como por_niveles, pero devuelve una lista de listas, una por nivel.

        En el árbol del paso 1: [[A], [B, C], [D, E, F], [G]]

        Truco: antes de procesar, mira cuántos elementos hay en la cola.
        Esos son exactamente los del nivel actual.
        """
        niveles = []
        if self.esta_vacio():
            return niveles
        cola = ColaEnlazada()
        cola.encolar(self.raiz)
        while not cola.esta_vacia():
            nivel = []
            for _ in range(cola.tamaño()):      # solo los del nivel actual
                nodo = cola.desencolar()
                nivel.append(nodo.dato)
                if nodo.izquierdo is not None:
                    cola.encolar(nodo.izquierdo)
                if nodo.derecho is not None:
                    cola.encolar(nodo.derecho)
            niveles.append(nivel)
        return niveles

    def altura(self):
        """Altura del árbol. Vacío = -1, hoja = 0.

        Complejidad: O(n)
        """
        return self._altura(self.raiz)

    def _altura(self, nodo):
        if nodo is None:
            return -1               # ¡NO 0! Si pones 0, una hoja daría altura 1
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))

    def contar_nodos(self):
        """Cantidad total de nodos. O(n)."""
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):
        if nodo is None:                             # patrón: 0 si es None, si no 1 + los de cada subárbol
            return 0
        return 1 + self._contar_nodos(nodo.izquierdo) + self._contar_nodos(nodo.derecho)   
    def contar_hojas(self):
        """Cantidad de nodos sin hijos. O(n)."""
        return self._contar_hojas(self.raiz)

    def _contar_hojas(self, nodo):       # cuidado: un nodo con UN hijo NO es hoja
        if nodo is None:
            return 0
        if nodo.es_hoja():
            return 1
        return self._contar_hojas(nodo.izquierdo) + self._contar_hojas(nodo.derecho)   

    def profundidad_de(self, dato):
        """Profundidad del nodo que contiene `dato`, o -1 si no está. O(n)."""
        return self._profundidad_de(self.raiz, dato, 0)

    def _profundidad_de(self, nodo, dato, nivel):
        if nodo is None:
            return -1
        if nodo.dato == dato:
            return nivel
        izquierda = self._profundidad_de(nodo.izquierdo, dato, nivel + 1)
        if izquierda != -1:
            return izquierda
        return self._profundidad_de(nodo.derecho, dato, nivel + 1)

    def es_perfecto(self):
        """Un árbol es perfecto si todas las hojas están al mismo nivel
        y todos los nodos internos tienen dos hijos.

        Pista: un árbol perfecto de altura h tiene exactamente
        2^(h+1) - 1 nodos.
        """
        return self.contar_nodos() == 2 ** (self.altura() + 1) - 1
