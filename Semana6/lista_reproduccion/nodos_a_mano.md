# Nodos a mano — la cadena manual

## Construcción de 3 nodos sin usar la clase ListaEnlazada

​```python
class Nodo:
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente

nodo1 = Nodo("Canción A")
nodo2 = Nodo("Canción B")
nodo3 = Nodo("Canción C")

nodo1.siguiente = nodo2
nodo2.siguiente = nodo3
​```

## Recorrido con un bucle

​```python
actual = nodo1
while actual is not None:
    print(actual.dato)
    actual = actual.siguiente
​```

Salida: `Canción A`, `Canción B`, `Canción C`

## Qué pasa si reasignas el enlace del primer nodo antes de guardar el segundo

### Diagrama - estado inicial

​```
nodo1 --> nodo2 --> nodo3 --> None
​```

### Caso incorrecto: reasignar antes de guardar

Paso 1: `nodo1.siguiente = nodo_nuevo`

​```
nodo1 --> nodo_nuevo         nodo2 --> nodo3 --> None
                              (huérfanos: ya nada apunta a ellos)
​```

En este punto ya perdimos la referencia a `nodo2` y `nodo3`. No existe
ninguna otra flecha en el programa que apunte hacia ellos.

Paso 2: `nodo_nuevo.siguiente = nodo1.siguiente`

​```
nodo1 --> nodo_nuevo --> nodo_nuevo   (se apunta a sí mismo: bucle infinito)
​```

Como en el paso 1 ya sobrescribimos `nodo1.siguiente`, cuando el paso 2
lee `nodo1.siguiente` ya no obtiene `nodo2`: obtiene el propio
`nodo_nuevo`. El nodo termina apuntándose a sí mismo.

### Caso correcto: guardar antes de reasignar

Paso 1: `nodo_nuevo.siguiente = nodo1.siguiente`

​```
nodo_nuevo --> nodo2   (nodo_nuevo ya guarda hacia dónde iba nodo1)
nodo1 --> nodo2 --> nodo3 --> None   (la cadena original sigue intacta)
​```

Paso 2: `nodo1.siguiente = nodo_nuevo`

​```
nodo1 --> nodo_nuevo --> nodo2 --> nodo3 --> None
​```

## Conclusión del primer caso

El orden de las dos líneas importa porque no existe una "copia de
seguridad" automática del enlace: en el momento en que reasignas
`nodo1.siguiente`, el valor anterior se pierde para siempre, a menos
que ya lo hayas guardado en otra variable o nodo antes de sobrescribirlo.

## Un nodo sigue vivo mientras algo lo referencie

### Código

​```python
c = Nodo("C")
b = Nodo("B", c)
a = Nodo("A", b)
# En este punto: a --> b --> c --> None

otro = b            # una segunda variable apunta al mismo nodo B

a.siguiente = c      # desconectamos B de la cadena principal
# Ahora la cadena principal es: a --> c --> None

print(otro.dato)     # imprime "B"
​```

### Diagrama - antes de desconectar

​```
a --> b --> c --> None
      ^
otro -┘
​```

Dos flechas distintas apuntan al nodo B: la de `a.siguiente` (porque
es el siguiente de A) y la de la variable `otro`.

### Diagrama - después de `a.siguiente = c`

​```
a ------------> c --> None

otro --> b (sigue existiendo, aparte de la cadena principal)
​```

La cadena principal (la que empieza en `a`) ya no pasa por B: se saltó
directo a C. Pero B **no desaparece**, porque `otro` todavía tiene una
flecha apuntándole.

### ¿Por qué `print(otro.dato)` sigue funcionando?

Porque "estar en la cadena principal" y "existir en memoria" son cosas
distintas. Un nodo existe mientras **al menos una** referencia (una
variable, u otro nodo `.siguiente`) apunte a él. Sacar a B de la
cadena de A solo elimina *una* de sus referencias (la de
`a.siguiente`), pero `otro` sigue siendo otra referencia válida.

### ¿Cuándo se destruye B de verdad?

Solo cuando la última referencia que le queda desaparece:

​```python
otro = None   # ahora ninguna variable apunta a B
​```

En este momento, Python detecta que ningún nombre en el programa
puede alcanzar a B (ni `a`, ni `otro`, ni el `.siguiente` de ningún
otro nodo), y el recolector de basura libera esa memoria.

### Conexión con el caso anterior

Este ejemplo es el reverso del anterior: antes vimos que **perder la
única referencia por accidente** (al reasignar en mal orden) te deja
sin forma de llegar al resto de la cadena. Aquí vemos que **mientras
quede al menos una referencia**, el nodo sigue accesible y vivo, sin
importar si sigue conectado a la cadena principal o no.