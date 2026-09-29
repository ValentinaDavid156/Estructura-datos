# Código base — Semana 09
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/09-Semana-09-Colas/02-guia-de-laboratorio.html

import pytest
from cola import ColaCircular, ColaEnlazada, ColaVaciaError


@pytest.fixture(params=[ColaCircular, ColaEnlazada])
def Cola(request):
    return request.param


def test_cola_nueva_vacia(Cola):
    """CA-01: una cola nueva está vacía."""
    c = Cola()
    assert c.esta_vacia()
    assert c.tamaño() == 0


def test_orden_fifo(Cola):
    """CA-02: los elementos salen en el mismo orden en que entraron."""
    c = Cola()
    for v in [1, 2, 3]:
        c.encolar(v)
    assert [c.desencolar(), c.desencolar(), c.desencolar()] == [1, 2, 3]


def test_desencolar_vacia(Cola):
    """CA-03: desencolar sobre cola vacía lanza ColaVaciaError."""
    with pytest.raises(ColaVaciaError):
        Cola().desencolar()


def test_frente_no_modifica(Cola):
    """CA-04: frente devuelve sin quitar."""
    c = Cola()
    c.encolar("a")
    assert c.frente() == "a"
    assert c.tamaño() == 1


def test_vaciar_y_reutilizar(Cola):
    """CA-05: la cola queda consistente después de vaciarse."""
    c = Cola()
    for v in range(5):
        c.encolar(v)
    for _ in range(5):
        c.desencolar()
    assert c.esta_vacia()
    c.encolar("nuevo")            # debe funcionar
    assert c.frente() == "nuevo"


def test_dar_la_vuelta():
    """Específico de la circular: el uso intercalado hace que los índices
    den la vuelta. Aquí es donde falla una implementación mal hecha."""
    c = ColaCircular()
    for ciclo in range(3):
        for i in range(6):
            c.encolar((ciclo, i))
        for i in range(6):
            assert c.desencolar() == (ciclo, i)
    assert c.esta_vacia()


def test_crecer_dando_la_vuelta():
    """Redimensionar cuando los elementos están dados la vuelta."""
    c = ColaCircular()
    for i in range(6):
        c.encolar(i)
    for _ in range(4):
        c.desencolar()            # frente queda avanzado
    for i in range(100, 120):
        c.encolar(i)              # fuerza redimensionamiento
    esperado = [4, 5] + list(range(100, 120))
    assert [c.desencolar() for _ in range(len(esperado))] == esperado
