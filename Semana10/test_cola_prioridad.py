import pytest

from cola import ColaVaciaError
from cola_prioridad import ColaPrioridad, ALTA, MEDIA, BAJA


def test_vacia_lanza_error():
    cola = ColaPrioridad()
    assert cola.esta_vacia()
    with pytest.raises(ColaVaciaError):
        cola.desencolar()


def test_atiende_por_nivel():
    cola = ColaPrioridad()
    cola.encolar("b", BAJA, 0)
    cola.encolar("m", MEDIA, 0)
    cola.encolar("a", ALTA, 0)
    assert [cola.desencolar(0) for _ in range(3)] == ["a", "m", "b"]


def test_fifo_dentro_del_mismo_nivel():
    cola = ColaPrioridad()
    for i, nombre in enumerate(["m1", "m2", "m3"]):
        cola.encolar(nombre, MEDIA, i)
    assert [cola.desencolar(10) for _ in range(3)] == ["m1", "m2", "m3"]


def test_nivel_invalido_y_tiempo_que_retrocede():
    cola = ColaPrioridad()
    with pytest.raises(ValueError):
        cola.encolar("x", 7, 0)
    cola.encolar("x", ALTA, 5)
    with pytest.raises(ValueError):
        cola.encolar("y", ALTA, 4)


def _ráfaga_de_altas(cola, paso=5, limite=200):
    """Una BAJA espera mientras llega una ALTA nueva cada `paso` minutos.
    Devuelve el instante en que se atiende a la BAJA, o None si nunca."""
    cola.encolar("baja", BAJA, 0)
    t = 0
    while t <= limite:
        cola.encolar(f"alta@{t}", ALTA, t)
        if cola.desencolar(t) == "baja":
            return t
        t += paso
    return None


def test_sin_envejecimiento_la_baja_espera_indefinidamente():
    assert _ráfaga_de_altas(ColaPrioridad(None)) is None


def test_con_envejecimiento_la_baja_se_atiende_en_2_intervalos():
    # intervalo 10: a los 20 min la BAJA es ALTA efectiva y gana el desempate por llegada
    assert _ráfaga_de_altas(ColaPrioridad(10)) == 20


def test_envejecimiento_no_altera_el_orden_de_quien_no_espero():
    cola = ColaPrioridad(10)
    cola.encolar("m", MEDIA, 0)
    cola.encolar("a", ALTA, 1)
    assert cola.desencolar(2) == "a"
    assert cola.desencolar(2) == "m"