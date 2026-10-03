# Código base — Semana 09
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/09-Semana-09-Colas/02-guia-de-laboratorio.html
class ColaVaciaError(Exception):
    """Se lanza al consultar o desencolar sobre una cola vacía."""
class ColaPrioridad:
    """Cola donde sale primero el elemento de MENOR prioridad numérica.

    Implementación por búsqueda lineal del mínimo: simple pero O(n)
    al desencolar. En la semana 14, cuando la uses para A*, verás
    que un montículo binario la baja a O(log n).

    Empates: se resuelven por orden de llegada (FIFO entre iguales).
    Este comportamiento DEBE estar en el spec.md: no es obvio.

    Complejidad: encolar O(1), desencolar O(n), frente O(n)
    """

    def __init__(self):
        self._elementos = []      # lista de tuplas (prioridad, orden, dato)
        self._contador = 0        # desempata por llegada

    def esta_vacia(self):
        return len(self._elementos) == 0

    def encolar(self, dato, prioridad):
        self._elementos.append((prioridad, self._contador, dato))
        self._contador += 1

    def _indice_minimo(self):
        """Índice del elemento con menor (prioridad, orden). O(n)."""
        menor = 0
        for i in range(1, len(self._elementos)):
            if self._elementos[i][:2] < self._elementos[menor][:2]:
                menor = i
        return menor

    def desencolar(self):
        """Devuelve el dato de menor prioridad. O(n)."""
        if self.esta_vacia():
            raise ColaVaciaError("desencolar sobre cola vacía")
        return self._elementos.pop(self._indice_minimo())[2]

    def frente(self):
        """Devuelve (sin quitar) el dato de menor prioridad. O(n)."""
        if self.esta_vacia():
            raise ColaVaciaError("frente sobre cola vacía")
        return self._elementos[self._indice_minimo()][2]
 
    def __len__(self):
        return len(self._elementos)

# --- pruebas ---

import pytest

def test_orden_por_prioridad():
    cp = ColaPrioridad()
    cp.encolar("urgente", 1)
    cp.encolar("normal", 5)
    cp.encolar("critico", 0)
    assert cp.desencolar() == "critico"
    assert cp.desencolar() == "urgente"
    assert cp.desencolar() == "normal"


def test_empate_es_fifo():
    """Documentado en el spec: los empates salen por orden de llegada."""
    cp = ColaPrioridad()
    cp.encolar("primero", 3)
    cp.encolar("segundo", 3)
    assert cp.desencolar() == "primero"
    assert cp.desencolar() == "segundo"

def test_cola_vacia_lanza_error():
    cp = ColaPrioridad()
    with pytest.raises(ColaVaciaError):
        cp.desencolar()
    with pytest.raises(ColaVaciaError):
        cp.frente()

def test_frente_no_modifica_la_cola():
    cp = ColaPrioridad()
    cp.encolar("a", 2)
    assert cp.frente() == "a"
    assert len(cp) == 1

def test_un_solo_elemento():
    cp = ColaPrioridad()
    cp.encolar("unico", 4)
    assert cp.desencolar() == "unico"
    assert cp.esta_vacia()
