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

class Nodo:
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente

# Construye la cadena
c = Nodo("C")
b = Nodo("B", c)
a = Nodo("A", b)

# Ahora observa: ¿cuántas flechas apuntan a cada nodo?
otro = b            # dos nombres apuntan al mismo nodo

# Desconecta B de la cadena
a.siguiente = c     # la cadena ahora es A -> C

# ¿Se destruyó el nodo B?
print(otro.dato)    # sigue existiendo: `otro` lo mantiene vivo

otro = None         # ahora sí: nadie referencia a B, Python lo recolecta
