# Código base — Semana 10
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/10-Semana-10-Arboles-binarios-y-recorridos/02-guia-de-laboratorio.html

from arbol_binario import NodoArbol, ArbolBinario


def arbol_ejemplo():
    """Construye el árbol del paso 1:
                  A
                /   \
               B     C
              / \     \
             D   E     F
                /
               G
    """
    g = NodoArbol("G")
    d = NodoArbol("D")
    e = NodoArbol("E", g)
    b = NodoArbol("B", d, e)
    f = NodoArbol("F")
    c = NodoArbol("C", None, f)
    return ArbolBinario(NodoArbol("A", b, c))


def test_preorden():
    assert arbol_ejemplo().preorden() == ["A", "B", "D", "E", "G", "C", "F"]


def test_inorden():
    assert arbol_ejemplo().inorden() == ["D", "B", "G", "E", "A", "C", "F"]


def test_postorden():
    assert arbol_ejemplo().postorden() == ["D", "G", "E", "B", "F", "C", "A"]


def test_por_niveles():
    assert arbol_ejemplo().por_niveles() == ["A", "B", "C", "D", "E", "F", "G"]


def test_por_niveles_agrupado():
    assert arbol_ejemplo().por_niveles_agrupado() == [
        ["A"], ["B", "C"], ["D", "E", "F"], ["G"]
    ]


def test_altura():
    assert arbol_ejemplo().altura() == 3
    assert ArbolBinario().altura() == -1            # vacío
    assert ArbolBinario(NodoArbol("solo")).altura() == 0   # una hoja


def test_conteos():
    arbol = arbol_ejemplo()
    assert arbol.contar_nodos() == 7
    assert arbol.contar_hojas() == 3               # D, G, F


def test_profundidad():
    arbol = arbol_ejemplo()
    assert arbol.profundidad_de("A") == 0
    assert arbol.profundidad_de("G") == 3
    assert arbol.profundidad_de("Z") == -1


def test_es_perfecto():
    #     X
    #   /   \
    #  Y     Z
    perfecto = ArbolBinario(NodoArbol("X", NodoArbol("Y"), NodoArbol("Z")))
    assert perfecto.es_perfecto()
    assert not arbol_ejemplo().es_perfecto()


def test_arbol_degenerado():
    """Un árbol donde cada nodo tiene un solo hijo: es una lista disfrazada.
    Esto anticipa el problema de la semana 11."""
    nodo = NodoArbol(5)
    for v in [4, 3, 2, 1]:
        nodo = NodoArbol(v, nodo)
    arbol = ArbolBinario(nodo)
    assert arbol.altura() == 4                     # tantos niveles como nodos - 1
    assert arbol.contar_hojas() == 1
    # Un árbol así pierde toda la ventaja de ser árbol.
