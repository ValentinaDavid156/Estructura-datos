# Código base — Semana 02
# Fuente: 01-Momento-1-Contrato-y-secuencia/02-Semana-02-ADT-y-Spec-Driven-Development/02-guia-de-laboratorio.html

import pytest
from carrito_lista import BolsaLista
from carrito_dict import BolsaDict, ElementoNoEncontradoError


# Las MISMAS pruebas corren contra las DOS implementaciones
@pytest.fixture(params=[BolsaLista, BolsaDict])
def Bolsa(request):
    return request.param


def test_bolsa_vacia(Bolsa):
    """CA-01: una bolsa recién creada tiene tamaño 0."""
    b = Bolsa()
    assert b.tamaño() == 0
    assert not b.contiene("x")


def test_duplicados(Bolsa):
    """CA-02: agregar el mismo elemento dos veces da cuantos() == 2."""
    b = Bolsa()
    b.agregar("manzana")
    b.agregar("manzana")
    assert b.cuantos("manzana") == 2
    assert b.tamaño() == 2


def test_sacar_inexistente(Bolsa):
    """CA-03: sacar un elemento inexistente lanza excepción."""
    b = Bolsa()
    with pytest.raises(ElementoNoEncontradoError):
        b.sacar("fantasma")


def test_sacar_reduce_cantidad(Bolsa):
    """CA-04: sacar reduce en 1 la cantidad y el tamaño."""
    b = Bolsa()
    b.agregar("a")
    b.agregar("a")
    b.sacar("a")
    assert b.cuantos("a") == 1
    assert b.tamaño() == 1


def test_invariante_tamaño(Bolsa):
    """INV-02: el tamaño es la suma de las cantidades."""
    b = Bolsa()
    for e in ["a", "b", "a", "c", "a"]:
        b.agregar(e)
    assert b.tamaño() == b.cuantos("a") + b.cuantos("b") + b.cuantos("c")

def test_sacar_ultimo_elemento(Bolsa):
    """CA-04: sacar el último ejemplar de un elemento lo purga de la estructura."""
    b = Bolsa()
    b.agregar("pera")
    b.sacar("pera")
    assert b.cuantos("pera") == 0
    with pytest.raises(ElementoNoEncontradoError):
        b.sacar("pera")


def test_contiene_post_eliminacion(Bolsa):
    """CA-05: contiene() devuelve False para elementos cuyo conteo bajó a 0."""
    b = Bolsa()
    b.agregar("uva")
    assert b.contiene("uva")
    b.sacar("uva")
    assert not b.contiene("uva")

def test_cantidad_cero_para_elemento_nunca_agregado(Bolsa):
    """CA-06: consultar cuantos() de algo nunca agregado devuelve 0, sin error."""
    b = Bolsa()
    assert b.cuantos("fantasma") == 0
