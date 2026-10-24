# Prueba individual · Estructuras de Datos

**Universidad Cooperativa de Colombia · Momento 2 (semanas 7–12) · 12 % del curso · 90 minutos**

Nombre:Valentina David Passos
Documento: 1025885882

## Instrucciones

- La prueba tiene dos partes. **Parte I** (35 min, 40 puntos): respondes en este mismo archivo, debajo de cada pregunta, y lo subes a D2L. **Parte II** (55 min, 60 puntos): se publica en D2L cuando cierra la Parte I.
- Sin internet, sin IA y sin ejecutar código en la Parte I.
- Todas las estructuras son **las que construimos en clase con nodos**: `Nodo(dato, siguiente)`, `NodoDoble(dato, anterior, siguiente)` y `NodoArbol(dato, izquierdo, derecho)`. Responde con lo que hacen **nuestros nodos**, no con listas de Python ni con lo que dice un libro.
- Cada pregunta pide una **justificación**. Sin ella, la respuesta vale la mitad.
- Si una expresión no se puede evaluar, escribe qué error produce y por qué.
- Si una pregunta trata un tema que **no vimos en clase**, escribe **«No lo vimos en clase»**. Es una respuesta válida y no te resta puntos.

---

# Parte I · Seguir los nodos (40 puntos)

## 1. Nodos de la lista doble (8 pts)

Se tienen cuatro `NodoDoble` enlazados en los dos sentidos:

```
cabeza                                cola
  [10] ⇄ [20] ⇄ [30] ⇄ [40]
```

`cabeza.anterior` es `None` y `cola.siguiente` es `None`. Alguien escribe este código para insertar el 55:

```python
n = cabeza.siguiente
nuevo = NodoDoble(55, n, n.siguiente)
n.siguiente = nuevo
```

a) ¿Qué dato tiene el nodo `n`?
b) Escribe el recorrido que se obtiene empezando en `cabeza` y avanzando por `siguiente` hasta `None`. Luego escribe el que se obtiene empezando en `cola` y retrocediendo por `anterior` hasta `None`.
c) ¿Cuánto vale `cola.anterior.anterior.dato`?
d) ¿Qué línea le falta al código para que la inserción quede correcta? Escríbela.

Justificación: explica por qué en b) los dos recorridos no muestran lo mismo.

**Respuesta:**
a): El nodo "n" tiene como dato el número 20.

b): El recorrido que se obtiene empezando en 'cabeza' y avanzando por siguiente es 10, 20, 55, 30, 40. Y retrocediendo desde cola por anterior es 40, 30, 20, 10.

Justificación: hacia adelante el 20 ya apunta al 55 que se insertó y el 55 al 30, por eso el recorrido lo demuestra. Hacia atrás, el 30 sigue apuntando al 20 porque nadie le cambió anterior, así que el recorrido se salta el 55. La inserción solo actualizó los enlaces en un sentido. En una lista doble hay que actualizar 4 enlaces (nuevo.anterior, nuevo.siguiente, n.siguiente y siguiente.anterior) y el código solo hizo 3.

c): cola.anterior.anterior.dato es 20

d): La linea que hace falta para que la inserción quede correcta es nuevo.siguiente.anterior = nuevo


---

## 2. Nodos de la pila (6 pts)

En una `PilaEnlazada` del curso vacía se ejecuta:

`push(1)` · `push(2)` · `push(3)` · `pop()` · `push(9)` · `push(4)`

Sea `t = pila._tope`.

a) ¿Qué devolvió el `pop()`?
b) ¿Cuánto vale `t.dato`? ¿Y `t.siguiente.dato`? ¿Y `t.siguiente.siguiente.siguiente.dato`?
c) ¿Qué es `t.siguiente.siguiente.siguiente.siguiente`?

Justificación: dibuja la cadena de nodos con sus flechas `siguiente` y explica hacia dónde apuntan.

**Respuesta:**
a): El pop devolvió 3 ya que fue el último dato que ingresó 

b): t.dato = 4, t.siguiente.dato = 9, t.siguiente.siguiente.siguiente.dato = 1

c): t.siguiente.siguiente.siguiente.siguiente = none


---

## 3. Nodos de la cola (6 pts)

En una `ColaEnlazada` del curso vacía se ejecuta:

`encolar(5)` · `encolar(6)` · `desencolar()` · `encolar(7)` · `desencolar()` · `desencolar()`

a) ¿Qué devolvió cada `desencolar()`?
b) Al terminar, ¿a qué apuntan `_cabeza` y `_cola`?
c) Ahora se ejecuta `encolar(8)`. ¿Cuánto vale `_cabeza.dato`? ¿`_cabeza is _cola` da `True` o `False`?
d) Repite c) suponiendo que en `desencolar` alguien **borró** la línea `self._cola = None`. ¿Qué pasa con el 8?

Justificación de d).

**Respuesta:**
a): Desencolar 1 = 5, ya que fue el número que primero entró, por lo tanto es el primero en salir, en desencolar 2 = 6, en el desencolar 3 = 7.

b): Al finalizar cabeza y cola estan vacíos por lo tanto apuntan a none

c): _cabeza.dato = a 8. Y `_cabeza is _cola = True, porque es la unica en la cola, por lo tanto es cabeza y cola al mismo tiempo.

d) Sin esa línea, _cola sigue apuntando al nodo del 7. Al encolar el 8, encolar cree que la cola no está vacía y hace _cola.siguiente = nuevo. Pero _cabeza es None, así que el 8 queda enlazado a un nodo que ya no pertenece a la cola. La cola parece vacía y _cabeza.dato da error

---

## 4. Nodos del ABB (10 pts)

En un `ABB` del curso vacío se insertan, en este orden:

`50, 30, 70, 25, 40, 60, 80, 40, 30, 45`

Sea `r = arbol.raiz`.

a) Dibuja el árbol (en texto, como en clase).
b) ¿Cuánto valen `len(arbol)` y `arbol.altura()`? ¿Cuál es la altura de un `ABB` vacío?
c) ¿Cuánto valen `r.izquierdo.derecho.derecho.dato` y `r.izquierdo.derecho.izquierdo.dato`?
d) Escribe el recorrido inorden.
e) Se elimina el 30. ¿Cuánto vale ahora `r.izquierdo.dato`? Escribe el preorden.

Justificación: explica tu respuesta a `len(arbol)`.

**Respuesta:**
a):   
```python

        50
      /    \
    30      70
   /  \    /  \
  25  40  60  80
        \
         45
```

b): len(arbol) = 8 y arbol.altura() = 3, un ABB vacío tiene una altura de 0.
Justificación len(arbol) = 8: Es la cantidad total de numeros que posee el arbol sin repetir. 

c): r.izquierdo.derecho.derecho.dato = 45 y r.izquierdo.derecho.izquierdo.dato = 0 o none.

d): El recorrido inorden es: 25, 30, 40, 45, 50, 60, 70, 80.

e): r.izquierdo.dato = 40, El 30 tiene dos hijos (25 y 40), así que se reemplaza por su sucesor que es el menor del lado derecho, que es el 40, este pasa a ocupar el lugar del 30 y el 45 pasa a ocupar el lugar del 40.

```python

        50
      /    \
    40      70
   /  \    /  \
  25  45  60  80

```


---

## 5. Nodos de la lista circular (6 pts)

Cinco `Nodo` forman una lista **circular** simple: `1 → 2 → 3 → 4 → 5 → 1` (el `siguiente` del 5 es el 1). La variable `inicio` apunta al nodo del 1. Se ejecuta:

```python
actual = inicio
while actual.siguiente is not actual:
    victima = actual.siguiente
    actual.siguiente = victima.siguiente
    actual = actual.siguiente
```

a) ¿En qué orden salen de la lista los nodos (`victima.dato` en cada vuelta)?
b) Al terminar, ¿cuánto vale `actual.dato`?
c) Al terminar, ¿`actual.siguiente is actual` da `True` o `False`? ¿Por qué?
d) Si la condición del ciclo fuera `while actual is not None:`, ¿qué pasaría?

Justificación: dibuja el círculo de nodos después de la segunda vuelta.

**Respuesta:**
a): victima.dato = 2, 4, 1, 5. por ejemplo: si el nodo que le sigue al actual no es el actual, lo tomaremos como victima y se eliminará, en este caso el actual = 1, y como 2 no es el actual se elimina, y el actual pasa a ser el siguiente, quiere decir, el 3, y como el siguiente del actual no es el actual, se elimina, y asi consecutivamente hasta dejar 1 nodo que se apunte a si mismo.

b): actual.dato = 3

c): actual.siguiente is actual = True, ya que al finalizar queda un solo número que es el 3 y se apunta a si mismo.

d) Es un ciclo infinito. En una lista circular ningún siguiente es None. Cuando queda un nodo, victima es él mismo y se “elimina” una y otra vez.

justificación: lista circular despues de la segunda vuelta
```python
      ┌──────────────────────┐
      ↓                      │
     [1] ───→ [3] ───→ [5] ──┘
                        ↑
                     actual
```

---

## 6. Recorrer nodos (4 pts)

Una `ListaDoble` del curso tiene 1000 elementos. ¿Cuántas veces se pasa de un nodo a otro (`actual = actual.siguiente` o `actual = actual.anterior`) para ejecutar:

a) `obtener(993)`
b) `obtener(12)`

Justificación: ¿desde qué nodo arranca cada recorrido y por qué?

**Respuesta:**
a): obtener (993) Desde cabeza (índice 0) serían 993 pasos, Desde cola (índice 999) son 999 - 993 = 6 pasos por anterior, Está más cerca de la cola, así que arranca en cola: 6 pasos.

b): obtener (12) Desde la cabeza (indice 0) serían 12 pasos, desde la cola (indice 999) son 999 - 12 = 987 pasos, está más cerca de la cabeza: 12 pasos.

---

## 7. Lista doble con nodo centinela

Una `ListaDoble` también se puede implementar con un **nodo centinela**.

a) ¿Qué es el nodo centinela y qué dato guarda?
b) ¿Qué ventaja tiene frente a manejar `cabeza` y `cola` por separado?
c) Escribe cómo quedaría `insertar_al_final(dato)` usando el centinela.

**Respuesta:**
Tema visto: 0%. Creatividad para inventar: 100%, pero prefiero ahorrarle la lectura :)


---

## 8. Lista de saltos (skip list)

Una lista de saltos guarda `10, 20, 30, 40, 50, 60, 70` en el nivel 0. En el nivel 1 están `20, 40, 60` y en el nivel 2 está solo `40`. Cada nodo tiene una referencia `adelante[i]` por cada nivel en el que aparece.

a) Describe, nodo por nodo, cómo se busca el 50 empezando por el nivel más alto.
b) ¿Qué complejidad promedio tiene la búsqueda y por qué?
c) ¿Cómo se decide en cuántos niveles queda un nodo nuevo al insertarlo?

**Respuesta:**
No profe, yo vine a ser evaluada, no sorprendida :c



# Parte II · Implementación con nodos (60 puntos)

Descarga `Parte_II.zip` de D2L. Contiene:

- `estructuras.py`: `ListaDoble` (con `cabeza` y `cola`) y `ABB`, ya completas. **No lo modifiques.**
- `solucion.py`: las dos funciones que implementas.
- `test_contrato.py`: **el contrato**. Léelo antes de programar: lo que el enunciado no diga, lo dicen esas pruebas. No se modifica.
- `test_mias.py`: tus pruebas.

### Ejercicio 1 · `quitar_repetidos(lista)` (30 pts)
Quita los datos repetidos de una `ListaDoble`: al terminar, cada dato aparece una sola vez. Devuelve cuántos nodos eliminó.

### Ejercicio 2 · `posicion_en_ranking(arbol, k)` (30 pts)
El `ABB` guarda los puntajes de una competencia. Devuelve el puntaje que ocupa el puesto `k` del ranking.

### Reglas
- Recorre los nodos (`cabeza`, `cola`, `siguiente`, `anterior`, `raiz`, `izquierdo`, `derecho`). **No conviertas la estructura completa a una lista de Python.**
- Escribe en un comentario la complejidad Big-O de cada función y por qué.
- En `test_mias.py` escribe mínimo 2 pruebas por función sobre casos que el contrato **no** cubre, cada una con un comentario de qué caso cubre.
- Ejecuta `python -m pytest -v` hasta que todo pase.
- Sube a D2L `solucion.py` y `test_mias.py`.

| Criterio (por ejercicio) | Peso |
|---|---|
| Cumple el contrato y la estructura queda bien | 45 % |
| Casos extremos y tus pruebas | 25 % |
| Complejidad adecuada y declarada | 20 % |
| Claridad | 10 % |
