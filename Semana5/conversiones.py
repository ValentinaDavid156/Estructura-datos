# Código base — Semana 05
# Fuente: 01-Momento-1-Contrato-y-secuencia/05-Semana-05-Memoria-dinamica-y-nodos/02-guia-de-laboratorio.html

def desde_lista(valores):
    """Construye una cadena de nodos a partir de una lista de Python.
    Devuelve la cabeza, o None si la lista está vacía."""
    pass


def a_lista(cabeza):
    """Convierte una cadena de nodos en una lista de Python."""
    pass


# --- pruebas ---
def test_ida_y_vuelta():
    original = [1, 2, 3, 4, 5]
    assert a_lista(desde_lista(original)) == original


def test_cadena_vacia():
    assert desde_lista([]) is None
    assert a_lista(None) == []


def test_insertar_al_inicio():
    cabeza = desde_lista(["B", "C"])
    cabeza = insertar_al_inicio(cabeza, "A")
    assert a_lista(cabeza) == ["A", "B", "C"]


def test_insertar_despues():
    cabeza = desde_lista(["A", "C"])
    insertar_despues(cabeza, "B")
    assert a_lista(cabeza) == ["A", "B", "C"]


def test_eliminar_siguiente():
    cabeza = desde_lista(["A", "B", "C"])
    eliminar_siguiente(cabeza)
    assert a_lista(cabeza) == ["A", "C"]
