# Código base — Semana 06
# Fuente: 01-Momento-1-Contrato-y-secuencia/06-Semana-06-Listas-enlazadas-simples/02-guia-de-laboratorio.html

import pytest
from Semana6.lista_reproduccion.lista_enlazada import ListaEnlazada, PosicionInvalidaError


def test_insertar_en_vacia_fija_cabeza_y_cola():
    """Insertar el primer elemento debe dejar cabeza y cola apuntando al mismo nodo."""
    lista = ListaEnlazada()
    lista.insertar(0, "único")
    assert lista._cabeza is lista._cola
    assert lista.tamaño() == 1


def test_eliminar_unico_deja_lista_consistente():
    """Eliminar el único elemento debe dejar cabeza Y cola en None."""
    lista = ListaEnlazada()
    lista.insertar(0, "único")
    lista.eliminar(0)
    assert lista._cabeza is None
    assert lista._cola is None       # el error más común: olvidar esta línea
    assert lista.tamaño() == 0


def test_eliminar_ultimo_actualiza_cola():
    """Al eliminar el último, _cola debe pasar al penúltimo."""
    lista = ListaEnlazada()
    for i, v in enumerate(["a", "b", "c"]):
        lista.insertar(i, v)
    lista.eliminar(2)
    assert lista._cola.dato == "b"
    assert lista._cola.siguiente is None


def test_eliminar_cabeza_con_varios():
    lista = ListaEnlazada()
    for i, v in enumerate(["a", "b", "c"]):
        lista.insertar(i, v)
    assert lista.eliminar(0) == "a"
    assert list(lista) == ["b", "c"]
    assert lista._cabeza.dato == "b"


def test_eliminar_de_vacia_lanza():
    with pytest.raises(PosicionInvalidaError):
        ListaEnlazada().eliminar(0)


def test_insertar_y_eliminar_alternado():
    """Estrés: la lista debe quedar consistente tras muchas operaciones."""
    lista = ListaEnlazada()
    for i in range(50):
        lista.insertar(0, i)
    for _ in range(25):
        lista.eliminar(0)
    assert lista.tamaño() == 25
    assert lista._cola.siguiente is None
