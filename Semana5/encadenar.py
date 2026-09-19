# Código base — Semana 05
# Fuente: 01-Momento-1-Contrato-y-secuencia/05-Semana-05-Memoria-dinamica-y-nodos/02-guia-de-laboratorio.html

from nodo import Nodo

# Forma A: de atrás hacia adelante
d = Nodo("D")
c = Nodo("C", d)
b = Nodo("B", c)
cabeza_a = Nodo("A", b)

# Forma B: de adelante hacia atrás, asignando después
cabeza_b = Nodo("A")
cabeza_b.siguiente = Nodo("B")
cabeza_b.siguiente.siguiente = Nodo("C")
cabeza_b.siguiente.siguiente.siguiente = Nodo("D")

# Forma C: con un ciclo y una referencia al último
cabeza_c = None
ultimo = None
for letra in ["A", "B", "C", "D"]:
    nuevo = Nodo(letra)
    if cabeza_c is None:
        cabeza_c = nuevo
    else:
        ultimo.siguiente = nuevo
    ultimo = nuevo

# ¿Por qué la forma C necesita la variable `ultimo`?
# ¿Qué pasaría si no la tuvieras?
