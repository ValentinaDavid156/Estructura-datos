# Comparación — ListaArreglo vs ListaEnlazada para el reproductor

Medición hecha sobre listas de N = 5.000 canciones, 5 repeticiones por
operación, tomando la mediana. Cada mutación (insertar, eliminar) se
mide sobre una lista reconstruida justo antes, para no mezclar el
costo de construir la lista con el de la operación.

## Tabla de costos medidos (segundos, mediana de 5 repeticiones)

| Operación | Frecuencia/día | ListaArreglo | ListaEnlazada |
|---|---|---|---|
| Insertar al principio | 40 | 0.00023782 | 0.00000251 |
| Recorrer toda la lista | 3 | 0.00013773 | 0.00011069 |
| Ir a la canción N (medio) | 200 | 0.00000053 | 0.00003995 |
| Borrar la actual (medio) | 15 | 0.00015397 | 0.00004310 |

Esto confirma lo que predice la teoría:
- **Insertar al principio**: `ListaEnlazada` es ~95 veces más rápida.
  Solo reacomoda `_cabeza` (O(1)); `ListaArreglo` tiene que desplazar
  los 5.000 elementos (O(n)).
- **Ir a la canción N**: `ListaArreglo` es ~75 veces más rápida. Accede
  directo por índice (O(1)); `ListaEnlazada` tiene que recorrer nodo
  por nodo desde la cabeza hasta llegar a la posición (O(n)).
- **Recorrer** y **borrar**: tiempos del mismo orden en ambas, porque
  las dos son O(n) para estas operaciones.

## Costo de un día de emisión

Costo total = Σ (tiempo de la operación × frecuencia diaria)

**ListaArreglo:**
(0.00023782 × 40) + (0.00013773 × 3) + (0.00000053 × 200) + (0.00015397 × 15)
= 0.0095128 + 0.0004132 + 0.0001060 + 0.0023096
= 0.0123416 s


**ListaEnlazada:**
(0.00000251 × 40) + (0.00011069 × 3) + (0.00003995 × 200) + (0.00004310 × 15)
= 0.0001004 + 0.0003321 + 0.0079900 + 0.0006465
= 0.0090690 s


## Tabla resumen: costo teórico vs. costo medido

| Operación | Big-O ListaArreglo | Medido ListaArreglo (s) | Big-O ListaEnlazada | Medido ListaEnlazada (s) |
|---|---|---|---|---|
| Insertar al principio | O(n) | 0.00023782 | O(1) | 0.00000251 |
| Recorrer toda la lista | O(n) | 0.00013773 | O(n) | 0.00011069 |
| Obtener (posición N) | O(1) | 0.00000053 | O(n) | 0.00003995 |
| Eliminar (posición N) | O(n) | 0.00015397 | O(n) | 0.00004310 |

**¿Coincide la teoría con la medición?** Sí. Donde la teoría dice O(1)
(insertar al principio en la enlazada, obtener en el arreglo), el
tiempo medido es el más bajo de toda la tabla. Donde la teoría dice
O(n) en ambas (recorrer, eliminar), los tiempos medidos son del mismo
orden de magnitud entre sí, a diferencia de los casos O(1) vs O(n)
donde la brecha es de uno o dos órdenes de magnitud (insertar al
principio: la enlazada es ~95 veces más rápida; obtener: el arreglo es
~75 veces más rápido).

## Recomendación

Con las frecuencias reales que dio la emisora, **`ListaEnlazada` le
cuesta menos al reproductor por día** (0.00907 s frente a 0.01234 s de
`ListaArreglo`, aproximadamente un 27% menos).

Aunque `obtener` (ir a la canción N) es mucho más lenta en la lista
enlazada, esa operación es barata en términos absolutos incluso
multiplicada por 200 veces al día. Lo que de verdad pesa en
`ListaArreglo` es **insertar al principio**: aunque solo ocurre 40
veces al día, cada una desplaza los 5.000 elementos, y ese costo
domina su total (0.0095 s de los 0.0123 s totales, un 77%).

### Qué tendría que cambiar en las frecuencias para que cambiara la recomendación

`obtener` es la operación donde `ListaArreglo` gana por mucho margen
(O(1) contra O(n)). Si la frecuencia de "ir a la canción N" subiera lo
suficiente, en algún punto ese costo dominaría también en la lista
enlazada y volcaría la balanza.

Dejando las demás frecuencias fijas (40, 3, 15), el punto de
equilibrio para "ir a la canción N" es aproximadamente: