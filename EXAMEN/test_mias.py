"""Tus pruebas: mínimo 2 por función, sobre casos que el contrato NO cubre
(un solo elemento, todos iguales, árbol degenerado, k negativo, ...).
Cada prueba lleva un comentario de una línea: qué caso cubre y por qué importa.
"""
from estructuras import ListaDoble, ABB
from solucion import quitar_repetidos, posicion_en_ranking

# ---------- quitar_repetidos ----------
 
def test_un_solo_elemento():
    # Un solo nodo: no hay con qué compararlo, no se elimina nada y cabeza/cola siguen siendo el mismo nodo.
    lista = ListaDoble([9])
    assert quitar_repetidos(lista) == 0
    assert list(lista) == [9]
    assert lista.cabeza is lista.cola
 
def test_todos_iguales():
    # Todos repetidos: solo queda uno, y cabeza y cola deben apuntar a ese nodo con enlaces None.
    lista = ListaDoble([4, 4, 4, 4])
    assert quitar_repetidos(lista) == 3
    assert list(lista) == [4]
    assert len(lista) == 1
    assert lista.cabeza is lista.cola
    assert lista.cabeza.anterior is None and lista.cabeza.siguiente is None
 
def test_sin_repetidos_no_cambia():
    # Sin repetidos: devuelve 0 y la lista queda igual en ambos sentidos.
    lista = ListaDoble([1, 2, 3])
    assert quitar_repetidos(lista) == 0
    assert list(lista) == [1, 2, 3]
    assert list(reversed(lista)) == [3, 2, 1]
 
def test_repetidos_en_los_extremos():
    # Repetido en cabeza y cola: se elimina la cabeza vieja y los extremos quedan bien enlazados.
    lista = ListaDoble([1, 2, 3, 1])
    assert quitar_repetidos(lista) == 1
    assert list(lista) == [2, 3, 1]
    assert lista.cabeza.anterior is None
    assert lista.cola.siguiente is None
    assert list(reversed(lista)) == [1, 3, 2]
 
 
# ---------- posicion_en_ranking ----------
 
def test_ranking_arbol_vacio():
    # Árbol vacío: no hay puestos, devuelve None en vez de fallar.
    assert posicion_en_ranking(ABB(), 1) is None
 
def test_ranking_un_solo_puntaje():
    # Un solo nodo: el puesto 1 es ese puntaje y el 2 no existe.
    arbol = ABB([42])
    assert posicion_en_ranking(arbol, 1) == 42
    assert posicion_en_ranking(arbol, 2) is None
 
def test_ranking_k_negativo():
    # k negativo: puesto inválido, debe devolver None (no indexar al revés).
    assert posicion_en_ranking(ABB([5, 3, 8]), -1) is None
 
def test_ranking_arbol_degenerado():
    # Árbol en forma de lista (insertado en orden): llega al último puesto recorriendo toda la rama derecha.
    arbol = ABB(range(1, 201))
    assert arbol.altura() == 199
    assert posicion_en_ranking(arbol, 1) == 200
    assert posicion_en_ranking(arbol, 200) == 1
 
def test_ranking_ultimo_puesto_y_duplicados():
    # Puntajes repetidos se guardan una sola vez: el puesto len(arbol) es el menor y len+1 no existe.
    arbol = ABB([50, 30, 70, 30, 50])
    assert len(arbol) == 3
    assert posicion_en_ranking(arbol, 3) == 30
    assert posicion_en_ranking(arbol, 4) is None