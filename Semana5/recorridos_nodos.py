# Código base — Semana 05
# Fuente: 01-Momento-1-Contrato-y-secuencia/05-Semana-05-Memoria-dinamica-y-nodos/02-guia-de-laboratorio.html

def recorrer(cabeza):
    """Imprime todos los datos de la cadena."""
    actual = cabeza          # NUNCA muevas `cabeza`: la perderías
    while actual is not None:
        print(actual.dato, end=" -> ")
        actual = actual.siguiente
    print("None")


def contar(cabeza):
    """Devuelve cuántos nodos hay en la cadena. O(n)."""
    pass


def buscar(cabeza, valor):
    """Devuelve el nodo que contiene `valor`, o None si no está."""
    pass


def ultimo(cabeza):
    """Devuelve el último nodo de la cadena, o None si está vacía."""
    pass


def obtener_en(cabeza, indice):
    """Devuelve el dato en la posición `indice`, contando desde 0.
    Lanza IndexError si el índice no existe.

    Nota la diferencia con el arreglo: aquí NO puedes saltar
    directamente a la posición. Tienes que recorrer. Por eso es O(n)
    y no O(1)."""
    pass
