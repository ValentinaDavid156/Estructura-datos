"""CONTRATO de la Parte II. Estas pruebas NO se modifican: tu solución debe pasarlas.
Ejecuta:  python -m pytest -v
"""
from estructuras import ListaDoble, ABB
from solucion import quitar_repetidos, posicion_en_ranking


# ---------- quitar_repetidos ----------

def test_quitar_repetidos_conserva_la_ultima_aparicion():
    lista = ListaDoble([3, 1, 3, 2, 1])
    assert quitar_repetidos(lista) == 2
    assert list(lista) == [3, 2, 1]

def test_quitar_repetidos_enlaces_hacia_atras():
    lista = ListaDoble([5, 7, 5])
    quitar_repetidos(lista)
    assert list(reversed(lista)) == [5, 7]
    assert len(lista) == 2

def test_quitar_repetidos_vacia():
    assert quitar_repetidos(ListaDoble()) == 0


# ---------- posicion_en_ranking ----------

PUNTAJES = [50, 30, 70, 20, 40, 60, 80]

def test_ranking_puesto_1_es_el_mejor_puntaje():
    assert posicion_en_ranking(ABB(PUNTAJES), 1) == 80

def test_ranking_puesto_3():
    assert posicion_en_ranking(ABB(PUNTAJES), 3) == 60

def test_ranking_puesto_inexistente():
    assert posicion_en_ranking(ABB(PUNTAJES), 0) is None
    assert posicion_en_ranking(ABB(PUNTAJES), 8) is None
