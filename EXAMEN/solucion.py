"""Prueba individual · Estructuras de Datos · Parte II

Nombre: Valentina David Passos  Documento: 1025885882

Metodología del curso (SDD): la especificación manda. El contrato exacto de
cada función está en test_contrato.py. Léelo ANTES de programar: lo que no
diga el enunciado, lo dicen esas pruebas.

Reglas: recorre los nodos (cabeza, cola, siguiente, anterior, raiz, izquierdo,
derecho). No conviertas la estructura completa a una lista de Python.
Escribe en un comentario la complejidad Big-O de cada función y por qué.
"""
from estructuras import ListaDoble, ABB


def quitar_repetidos(lista: ListaDoble) -> int:
    """Quita los datos repetidos: al terminar, cada dato aparece una sola vez en la lista.
    Devuelve cuántos nodos se eliminaron.
    """

    #Se conserva la ÚLTIMA aparición de cada dato (contrato).
    #Recorre desde la cola hacia atrás: la primera vez que ve un dato es su
    #última aparición (se queda); las siguientes son copias viejas y se eliminan.

    #Complejidad: O(n) tiempo, porque visita cada nodo una vez, el set consulta
    #en O(1) y eliminar_nodo es O(1). O(n) espacio extra por el set.
    

    vistos = set()
    eliminados = 0
    actual = lista.cola
    while actual is not None:
        anterior = actual.anterior  # guardar antes de que eliminar_nodo desenlace el nodo
        if actual.dato in vistos:
            lista.eliminar_nodo(actual)
            eliminados += 1
        else:
            vistos.add(actual.dato)
        actual = anterior
    return eliminados


def posicion_en_ranking(arbol: ABB, k: int):
    """El árbol guarda los puntajes de una competencia.
    Devuelve el puntaje que ocupa el puesto k del ranking.
    """
    #Puesto 1 = el mayor. Si k < 1 o k > cantidad de puntajes, devuelve None.
    #Recorrido inorden invertido (derecho, raíz, izquierdo): visita de mayor a
    #menor y corta al llegar al k-ésimo. Es iterativo con pila de nodos.

    #Complejidad: O(h + k) tiempo, porque baja por la derecha (h pasos) y
    #visita solo k nodos, sin recorrer todo el árbol. O(h) espacio por la pila.

    if k < 1:
        return None
    pila = []
    actual = arbol.raiz
    contador = 0
    while actual is not None or pila:
        while actual is not None:
            pila.append(actual)
            actual = actual.derecho
        actual = pila.pop()
        contador += 1
        if contador == k:
            return actual.dato
        actual = actual.izquierdo
    return None  # k mayor que la cantidad de puntajes (o árbol vacío)
