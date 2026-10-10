# Código base — Semana 04
# Fuente: 01-Momento-1-Contrato-y-secuencia/04-Semana-04-Arreglos-y-estructuras-estaticas/02-guia-de-laboratorio.html

import pytest
from lista_arreglo import ListaArreglo, PosicionInvalidaError

# En la semana 6 agregarás ListaEnlazada a esta lista de parámetros
IMPLEMENTACIONES = [ListaArreglo]


@pytest.fixture(params=IMPLEMENTACIONES)
def Lista(request):
    return request.param


def llenar(lista, valores):
    """Auxiliar: inserta los valores uno tras otro, al final."""
    for v in valores:
        lista.insertar(lista.tamaño(), v)
    return lista


def contenido(lista):
    return [lista.obtener(i) for i in range(lista.tamaño())]


# ---------- contrato general (sirve para cualquier implementación) ----------

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
    with pytest.raises(PosicionInvalidaError):
        lista.obtener(0)
    with pytest.raises(PosicionInvalidaError):
        lista.insertar(5, "x")


def test_buscar_ausente(Lista):
    """CA-06: buscar devuelve -1 si el elemento no está."""
    assert Lista().buscar("fantasma") == -1


def test_redimensionamiento(Lista):
    """El crecimiento más allá de la capacidad inicial no pierde datos."""
    lista = Lista()
    for i in range(100):
        lista.insertar(i, i)
    assert lista.tamaño() == 100
    assert [lista.obtener(i) for i in range(100)] == list(range(100))


# ---------- casos extremos que pide la actividad ----------

def test_vacia_eliminar_y_obtener_fallan(Lista):
    """Lista vacía: no hay nada que obtener ni eliminar."""
    lista = Lista()
    with pytest.raises(PosicionInvalidaError):
        lista.eliminar(0)
    with pytest.raises(PosicionInvalidaError):
        lista.obtener(0)


def test_un_elemento(Lista):
    """Lista de un solo elemento: obtener, buscar y eliminar."""
    lista = Lista()
    lista.insertar(0, "solo")
    assert lista.tamaño() == 1
    assert lista.obtener(0) == "solo"
    assert lista.buscar("solo") == 0
    assert lista.eliminar(0) == "solo"
    assert lista.tamaño() == 0
    assert lista.buscar("solo") == -1


def test_insertar_final(Lista):
    """Insertar al final no toca los elementos que ya estaban."""
    lista = llenar(Lista(), ["a", "b", "c"])
    lista.insertar(3, "d")
    assert contenido(lista) == ["a", "b", "c", "d"]


def test_insertar_medio(Lista):
    """Insertar en el medio desplaza solo lo que viene después."""
    lista = llenar(Lista(), ["a", "c", "d"])
    lista.insertar(1, "b")
    assert contenido(lista) == ["a", "b", "c", "d"]


def test_eliminar_en_medio_y_final(Lista):
    lista = llenar(Lista(), ["a", "b", "c", "d"])
    assert lista.eliminar(1) == "b"
    assert contenido(lista) == ["a", "c", "d"]
    assert lista.eliminar(2) == "d"
    assert contenido(lista) == ["a", "c"]


def test_insertar_posicion_mayor_que_tamaño(Lista):
    lista = llenar(Lista(), ["a", "b"])
    with pytest.raises(PosicionInvalidaError):
        lista.insertar(3, "x")
    with pytest.raises(PosicionInvalidaError):
        lista.insertar(-1, "x")


# ---------- operaciones propias de ListaArreglo (actividad 2) ----------

def test_buscar_lineal_primero_ultimo_ausente():
    lista = llenar(ListaArreglo(), [5, 7, 9])
    assert lista.buscar_lineal(5) == 0
    assert lista.buscar_lineal(9) == 2
    assert lista.buscar_lineal(8) == -1


def test_buscar_lineal_devuelve_primera_aparicion():
    lista = llenar(ListaArreglo(), [4, 2, 4])
    assert lista.buscar_lineal(4) == 0


def test_buscar_binaria_vacia_y_un_elemento():
    assert ListaArreglo().buscar_binaria(3) == -1
    lista = llenar(ListaArreglo(), [3])
    assert lista.buscar_binaria(3) == 0
    assert lista.buscar_binaria(1) == -1
    assert lista.buscar_binaria(9) == -1


@pytest.mark.parametrize("n", [2, 4, 6, 10, 100])  # tamaños pares
def test_buscar_binaria_tamaño_par(n):
    lista = llenar(ListaArreglo(), [2 * i for i in range(n)])
    for i in range(n):
        assert lista.buscar_binaria(2 * i) == i


@pytest.mark.parametrize("n", [1, 3, 5, 7, 101])  # tamaños impares
def test_buscar_binaria_tamaño_impar(n):
    lista = llenar(ListaArreglo(), [2 * i for i in range(n)])
    for i in range(n):
        assert lista.buscar_binaria(2 * i) == i


def test_buscar_binaria_bordes_y_ausentes():
    lista = llenar(ListaArreglo(), [10, 20, 30, 40, 50, 60])
    assert lista.buscar_binaria(10) == 0   # primer elemento
    assert lista.buscar_binaria(60) == 5   # último elemento
    assert lista.buscar_binaria(5) == -1   # menor que todos
    assert lista.buscar_binaria(99) == -1  # mayor que todos
    assert lista.buscar_binaria(35) == -1  # entre dos elementos


def test_insertar_ordenado_en_vacia():
    lista = ListaArreglo()
    lista.insertar_ordenado(7)
    assert contenido(lista) == [7]


def test_insertar_ordenado_inicio_medio_final():
    lista = llenar(ListaArreglo(), [10, 20, 30, 40])
    lista.insertar_ordenado(5)    # inicio
    lista.insertar_ordenado(25)   # medio
    lista.insertar_ordenado(99)   # final
    assert contenido(lista) == [5, 10, 20, 25, 30, 40, 99]


def test_insertar_ordenado_con_repetidos():
    lista = llenar(ListaArreglo(), [1, 3, 3, 5])
    lista.insertar_ordenado(3)
    assert contenido(lista) == [1, 3, 3, 3, 5]


def test_insertar_ordenado_desordenado_queda_ordenado():
    lista = ListaArreglo()
    for v in [8, 3, 9, 1, 7, 2, 6, 4, 5, 0]:
        lista.insertar_ordenado(v)
    assert contenido(lista) == list(range(10))


def test_binaria_despues_de_insertar_ordenado():
    lista = ListaArreglo()
    for v in [50, 10, 40, 20, 30]:
        lista.insertar_ordenado(v)
    assert lista.buscar_binaria(40) == 3
    assert lista.buscar_binaria(35) == -1