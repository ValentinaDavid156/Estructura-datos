# Autopsia del error.

### 1. El código con el bug
 
```python
class Carrito:
    def __init__(self, items=[]):        # <- el problema está aquí
        self.items = items
 
    def meter(self, producto):
        self.items.append(producto)
```
 
### 2. Síntoma observado
 
```python
carro_ana = Carrito()
carro_luis = Carrito()
 
carro_ana.meter("manzana")
 
print("Carrito de Ana: ", carro_ana.items)
print("Carrito de Luis:", carro_luis.items)
```
 
Salida real (verificada ejecutando el código):
 
```
Carrito de Ana:  ['manzana']
Carrito de Luis: ['manzana']
```
 
`carro_luis` nunca llamó a `meter()`, pero igual tiene "manzana" adentro.
Los dos carritos "ven" el mismo contenido.
 
### 3. Diagnóstico
 
En Python, el valor por defecto de un parámetro (`items=[]`) se evalúa
**una sola vez**: cuando el intérprete lee la definición de `__init__`,
no cada vez que se crea un `Carrito()` nuevo. Esa lista queda guardada
en un único lugar de memoria, colgada de la función `__init__` misma
— no de cada instancia.
 
Cada vez que se llama `Carrito()` sin pasarle `items` explícitamente,
Python no crea una lista nueva: reutiliza esa misma lista por defecto y
se la asigna a `self.items`. El resultado es que **todas las instancias
que no reciben `items` explícito terminan apuntando al mismo objeto
lista**, aunque cada `Carrito` "cree" tener el suyo propio.
 
Prueba definitiva, ejecutada sobre el código con el bug:
 
```python
print(id(carro_ana.items) == id(carro_luis.items))
# True  <- son literalmente el mismo objeto en memoria
```
 
### 4. Diagrama de memoria — ANTES (con el bug)
 
```
                    Carrito.__init__
                    (la función, en memoria una sola vez)
                            |
                            |  su parámetro "items" tiene
                            |  un valor por defecto ya creado:
                            v
                    +----------------+
                    |  lista @0x100  |  <-- UNA sola lista, compartida
                    |  ['manzana']   |      por todo el que no pase
                    +----------------+      su propio items
                       ^            ^
                       |            |
            .items ----+            +---- .items
                       |            |
                  +---------+  +---------+
                  |carro_ana|  |carro_luis|
                  +---------+  +---------+
 
carro_ana.meter("manzana")
   -> hace self.items.append("manzana")
   -> modifica la lista @0x100 directamente
   -> como carro_luis.items TAMBIÉN apunta a @0x100,
      "ve" el cambio sin que nadie lo haya tocado
```

### 5. La corrección
 
```python
class Carrito:
    def __init__(self, items=None):
        self.items = items if items is not None else []
 
    def meter(self, producto):
        self.items.append(producto)
```
 
El cambio clave: usar `None` como valor por defecto (un valor inmutable,
sin problema en compartirlo) y crear la lista real **dentro del cuerpo**
de `__init__`, con `[]`. Esa línea `items if items is not None else []`
sí se ejecuta cada vez que se llama `Carrito()` — no una sola vez al
definir la función — así que cada instancia recibe su propia lista nueva.
 
Verificación ejecutando el código corregido:
 
```
Carrito de Ana:  ['manzana']
Carrito de Luis: []
```
 
```python
print(id(carro_ana.items) == id(carro_luis.items))
# False  <- ahora sí son objetos distintos
```
 
### 6. Diagrama de memoria — DESPUÉS (corregido)
 
```
                    Carrito.__init__
                    (la función, en memoria una sola vez)
                            |
                            |  su parámetro "items" tiene
                            |  como valor por defecto None
                            |  (un valor inmutable, no una lista)
                            v
                         None
 
     Cada llamada a Carrito() SIN argumento entra al
     "else: []" y crea una lista NUEVA en ese momento:
 
        +-------------+                +-------------+
        | lista @0x200|                | lista @0x300|
        | ['manzana'] |                |     []      |
        +-------------+                +-------------+
               ^                              ^
               |                              |
     .items ---+                              +--- .items
               |                              |
        +---------+                    +----------+
        |carro_ana|                    |carro_luis|
        +---------+                    +----------+
```
 
### 7. Por qué la corrección funciona.

El bug no está en que Python "haga algo raro" con las listas — está en
**cuándo se evalúa el valor por defecto de un parámetro**. Python lo
evalúa una única vez, al leer el `def`, no en cada llamada. Cualquier
objeto **mutable** (lista, diccionario, set) usado como valor por
defecto se convierte en una trampa: como es un solo objeto compartido,
mutarlo desde una instancia lo muta para todas.
 
La corrección funciona porque mueve la creación del objeto mutable
**del encabezado de la función al cuerpo de la función**. El encabezado
(`def __init__(self, items=None)`) se lee una vez, y `None` es
inmutable — compartirlo no genera ningún problema, porque no se puede
"mutar" `None`. El cuerpo (`items if items is not None else []`), en
cambio, se ejecuta en cada llamada — así que el `[]` que aparece ahí se
crea de cero cada vez, generando un objeto distinto por instancia.

### 8. Por qué las implementaciones del carrito ya evitan este bug
 
Tanto `carrito_lista.py` como `carrito_dict.py` inicializan su
estado así:
 
```python
def __init__(self):
    self._elementos = []   # o self._conteos = {}
```
 
No hay ningún parámetro con valor por defecto mutable — la lista o el
diccionario se crea directamente en el cuerpo de `__init__`, sin pasar
por un parámetro. Por diseño, cada instancia ya recibe su propia
estructura desde el principio, así que este bug específico no puede
aparecer en ninguna de las dos implementaciones actuales.
