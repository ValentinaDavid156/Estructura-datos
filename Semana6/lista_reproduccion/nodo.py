# Dependencia: definido en la semana 05.
# Si ya lo tienes implementado, usa tu propia versión.

# Código base — Semana 05
# Fuente: 01-Momento-1-Contrato-y-secuencia/05-Semana-05-Memoria-dinamica-y-nodos/02-guia-de-laboratorio.html

class Nodo:
    """Un eslabón de una cadena: un dato y una referencia al siguiente.

    `siguiente` es None cuando este nodo es el último de la cadena.
    """

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente

    def __repr__(self):
        return f"Nodo({self.dato!r})"


