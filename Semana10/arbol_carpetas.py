"""El árbol de carpetas de la sala de cómputo (Actividad 5, partes C y D).

Modelo: cada `Carpeta` tiene un nombre, las entregas que contiene directamente
y una lista de subcarpetas. Un árbol de carpetas puede tener cualquier cantidad
de hijos por nodo, así que `hijos` es una lista usada como soporte interno
(permitido por el README del curso); la estructura que se recorre sigue siendo
el árbol de nodos `Carpeta`.

Convención del curso: altura/profundidad de árbol vacío = -1, de un solo nodo = 0.

Las tres consultas:
    total_entregas(c)      recursiva, O(n)
    profundidad_maxima(c)  recursiva, O(n)  (+ ruta_mas_profunda)
    listado_por_niveles(c) iterativa con ColaEnlazada propia, O(n)
"""

from cola import ColaEnlazada
from pila import PilaEnlazada


class Carpeta:
    def __init__(self, nombre, entregas=0, hijos=None):
        self.nombre = nombre
        self.entregas = entregas            # entregas directamente en esta carpeta
        self.hijos = list(hijos) if hijos else []

    def agregar(self, hijo):
        self.hijos.append(hijo)
        return hijo

    def __repr__(self):
        return f"Carpeta({self.nombre!r})"


# ---------- Consulta 1: total de entregas bajo un nodo (recursión) ----------
def total_entregas(carpeta):
    """Entregas de esta carpeta + las de todo lo que cuelga de ella."""
    if carpeta is None:                     # CASO BASE: árbol vacío
        return 0
    total = carpeta.entregas
    for hijo in carpeta.hijos:              # un nodo sin hijos no entra al for: hoja
        total += total_entregas(hijo)
    return total


# ---------- Consulta 2: ruta más profunda (recursión) ----------
def profundidad_maxima(carpeta):
    """Aristas desde `carpeta` hasta su descendiente más lejano.
    Vacío = -1, un solo nodo = 0."""
    if carpeta is None:                     # CASO BASE
        return -1
    mayor = -1                              # sin hijos: 1 + (-1) = 0
    for hijo in carpeta.hijos:
        mayor = max(mayor, profundidad_maxima(hijo))
    return 1 + mayor


def ruta_mas_profunda(carpeta):
    """Lista de nombres desde `carpeta` hasta el nodo más profundo.
    En empate gana la primera rama (la de más a la izquierda)."""
    if carpeta is None:                     # CASO BASE
        return []
    mejor = []
    for hijo in carpeta.hijos:
        ruta = ruta_mas_profunda(hijo)
        if len(ruta) > len(mejor):          # estrictamente mayor: la primera gana empates
            mejor = ruta
    return [carpeta.nombre] + mejor


# ---------- Consulta 3: listado por niveles (cola propia, sin recursión) ----------
def listado_por_niveles(raiz):
    """Lista de listas de nombres, una por nivel, de izquierda a derecha."""
    niveles = []
    if raiz is None:
        return niveles
    cola = ColaEnlazada()
    cola.encolar(raiz)
    while not cola.esta_vacia():
        nivel = []
        for _ in range(cola.tamaño()):      # exactamente los nodos del nivel actual
            carpeta = cola.desencolar()
            nivel.append(carpeta.nombre)
            for hijo in carpeta.hijos:
                cola.encolar(hijo)
        niveles.append(nivel)
    return niveles


# ---------- Parte D: el MISMO código con cola o con pila ----------
def _recorrer(raiz, contenedor, meter, sacar):
    """Saca un nodo, lo visita y mete sus hijos. Lo único que cambia entre las
    dos versiones es el contenedor: eso es lo que provoca el orden distinto."""
    orden = []
    if raiz is None:
        return orden
    meter(contenedor, raiz)
    while not contenedor.esta_vacia():
        carpeta = sacar(contenedor)
        orden.append(carpeta.nombre)
        for hijo in carpeta.hijos:
            meter(contenedor, hijo)
    return orden


def recorrido_con_cola(raiz):
    return _recorrer(raiz, ColaEnlazada(), ColaEnlazada.encolar, ColaEnlazada.desencolar)


def recorrido_con_pila(raiz):
    return _recorrer(raiz, PilaEnlazada(), PilaEnlazada.apilar, PilaEnlazada.desapilar)


# ---------- Árbol de prueba ----------
def construir_arbol_prueba():
    """
    Universidad Cooperativa de Colombia                        (nivel 0)
    ├── Facultad de Ingeniería                                 (nivel 1)
    │   ├── Ingeniería de Software                             (nivel 2)
    │   │   ├── Estructuras de Datos        [12 entregas]      (nivel 3)
    │   │   └── Física                      [ 9 entregas]
    │   ├── Ingeniería Mecánica
    │   │   └── Termodinámica               [ 7 entregas]
    │   └── Ingeniería Civil
    │       └── Estática                    [ 6 entregas]
    ├── Facultad de Medicina
    │   ├── Medicina
    │   │   └── Anatomía                    [10 entregas]
    │   ├── Enfermería
    │   │   └── Fundamentos de Enfermería   [ 8 entregas]
    │   └── Psicología
    │       └── Psicología General          [ 5 entregas]
    ├── Facultad de Derecho
    │   └── Derecho
    │       └── Derecho Constitucional      [ 4 entregas]
    └── Facultad de Odontología
        └── Odontología
            └── Anatomía Dental             [ 3 entregas]
    """
    ucc = Carpeta("Universidad Cooperativa de Colombia")

    ing = ucc.agregar(Carpeta("Facultad de Ingeniería"))
    soft = ing.agregar(Carpeta("Ingeniería de Software"))
    soft.agregar(Carpeta("Estructuras de Datos", 12))
    soft.agregar(Carpeta("Física", 9))
    ing.agregar(Carpeta("Ingeniería Mecánica")).agregar(Carpeta("Termodinámica", 7))
    ing.agregar(Carpeta("Ingeniería Civil")).agregar(Carpeta("Estática", 6))

    med = ucc.agregar(Carpeta("Facultad de Medicina"))
    med.agregar(Carpeta("Medicina")).agregar(Carpeta("Anatomía", 10))
    med.agregar(Carpeta("Enfermería")).agregar(Carpeta("Fundamentos de Enfermería", 8))
    med.agregar(Carpeta("Psicología")).agregar(Carpeta("Psicología General", 5))

    der = ucc.agregar(Carpeta("Facultad de Derecho"))
    der.agregar(Carpeta("Derecho")).agregar(Carpeta("Derecho Constitucional", 4))

    odo = ucc.agregar(Carpeta("Facultad de Odontología"))
    odo.agregar(Carpeta("Odontología")).agregar(Carpeta("Anatomía Dental", 3))
    return ucc


if __name__ == "__main__":
    raiz = construir_arbol_prueba()
    print("Total de entregas:", total_entregas(raiz))
    print("Profundidad máxima:", profundidad_maxima(raiz))
    print("Ruta más profunda:", " / ".join(ruta_mas_profunda(raiz)))
    for i, nivel in enumerate(listado_por_niveles(raiz)):
        print(f"Nivel {i}:", nivel)
    print("Con cola:", recorrido_con_cola(raiz))
    print("Con pila:", recorrido_con_pila(raiz))