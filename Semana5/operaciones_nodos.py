# Código base — Semana 05
# Fuente: 01-Momento-1-Contrato-y-secuencia/05-Semana-05-Memoria-dinamica-y-nodos/02-guia-de-laboratorio.html

def insertar_al_inicio(cabeza, dato):
    """Devuelve la nueva cabeza de la cadena. O(1).

    Diagrama:
        antes:   cabeza -> [B] -> [C] -> None
        después: cabeza -> [A] -> [B] -> [C] -> None
    """
    pass


def insertar_despues(nodo, dato):
    """Inserta un nodo nuevo justo después de `nodo`. O(1).

    Diagrama:
        antes:   ... -> [nodo] -> [X] -> ...
        después: ... -> [nodo] -> [nuevo] -> [X] -> ...

    CUIDADO con el orden. Si haces primero
        nodo.siguiente = nuevo
    pierdes la referencia a [X] para siempre.
    """
    pass


def eliminar_siguiente(nodo):
    """Elimina el nodo que sigue a `nodo`. O(1).

    Diagrama:
        antes:   ... -> [nodo] -> [X] -> [Y] -> ...
        después: ... -> [nodo] -> [Y] -> ...

    ¿Qué pasa con [X]? Python lo recolecta automáticamente
    cuando nadie lo referencia. En C tendrías que hacer free().
    """
    pass
