# Código base — Semana 06
# Fuente: 01-Momento-1-Contrato-y-secuencia/06-Semana-06-Listas-enlazadas-simples/02-guia-de-laboratorio.html
import pytest
from Semana6.lista_reproduccion.lista_arreglo import ListaArreglo
from Semana6.lista_reproduccion.lista_enlazada import ListaEnlazada

# ANTES:  IMPLEMENTACIONES = [ListaArreglo]
IMPLEMENTACIONES = [ListaArreglo, ListaEnlazada]

@pytest.fixture(params=IMPLEMENTACIONES)
def Lista(request):
    return request.param


def test_lista_vacia(Lista):
    """CA-01: una lista nueva tiene tamaño 0."""
    assert Lista().tamaño() == 0


def test_insertar_en_vacia(Lista):
    """CA-02: insertar en posición 0 en lista vacía."""
    lista = Lista()
    lista.insertar(0, "a")
    assert lista.tamaño() == 1
    assert lista.obtener(0) == "a"


def test_insertar_inicio(Lista):
    """CA-03: insertar al inicio desplaza sin perder elementos."""
    lista = Lista()
    for i, v in enumerate(["b", "c"]):
        lista.insertar(i, v)
    lista.insertar(0, "a")
    assert [lista.obtener(i) for i in range(3)] == ["a", "b", "c"]


def test_eliminar(Lista):
    """CA-04: eliminar reduce el tamaño y devuelve el elemento."""
    lista = Lista()
    lista.insertar(0, "x")
    assert lista.eliminar(0) == "x"
    assert lista.tamaño() == 0


def test_posicion_invalida(Lista):
    """CA-05: posición fuera de rango lanza excepción."""
    lista = Lista()
    with pytest.raises(Exception):
        lista.obtener(0)
    with pytest.raises(Exception):
        lista.insertar(5, "x")


def test_buscar_ausente(Lista):
    """CA-06: buscar devuelve -1 si no está."""
    assert Lista().buscar("fantasma") == -1


def test_redimensionamiento(Lista):
    """El crecimiento más allá de la capacidad inicial no pierde datos."""
    lista = Lista()
    for i in range(100):
        lista.insertar(i, i)
    assert lista.tamaño() == 100
    assert [lista.obtener(i) for i in range(100)] == list(range(100))
# No cambies NADA más. Ejecuta:
#     pytest -v
# Deberías ver cada prueba corriendo dos veces, una por implementación.
