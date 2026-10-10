# Predicción de complejidad — ListaArreglo

> Escrito **antes** de ejecutar `medicion.py`. Este archivo va en un commit
> aparte, anterior al de las mediciones.

Notación: **n** es el tamaño de la lista (`_tamaño`). Para justificar cada
complejidad cuento operaciones sencillas de mi código (comparaciones,
asignaciones, sumas y restas). No me importa el valor exacto de cada
constante, solo cómo crece el total cuando n crece.

## Resumen

| Operación | Mejor caso | Peor caso | Big-O |
|---|---|---|---|
| `obtener(pos)` | O(1) | O(1) | **O(1)** |
| `insertar(pos, x)` | O(1) (al final) | O(n) (al inicio) | **O(n)** |
| `insertar_ordenado(x)` | O(log n) (va al final) | O(n) (va al inicio) | **O(n)** |
| `buscar_lineal(x)` | O(1) (está primero) | O(n) (no está) | **O(n)** |
| `buscar_binaria(x)` | O(1) (está en el medio) | O(log n) | **O(log n)** |

## 1. `obtener(pos)`

- `_validar` calcula el límite (1 operación) y hace 2 comparaciones
  (`0 <= pos` y `pos <= limite`).
- Después hace **1** acceso a `_datos[pos]`.

Total: unas 4 operaciones, **sin importar cuánto valga n**.
T(n) = 4 → **O(1)**.

## 2. `insertar(pos, x)`

El `while` desplaza los elementos desde `_tamaño` hasta `pos + 1`, o sea
**n − pos** vueltas. Cada vuelta hace 1 asignación (`datos[i] = datos[i-1]`)
y 1 resta (`i = i - 1`), así que son 2 operaciones por vuelta:

T(n, pos) = 2 · (n − pos) + c        (c = validar + asignar + `_tamaño += 1`)

- Al inicio (pos = 0): T = 2n + c → **O(n)**.
- En el medio (pos = n/2): T = n + c → O(n).
- Al final (pos = n): T = c → **O(1)**.

**Redimensionar.** Cuando la lista se llena (`_tamaño == _capacidad`) hay que
copiar los n elementos a un arreglo del doble de tamaño. Eso es O(n), pero
pasa pocas veces porque la capacidad se duplica: 4, 8, 16, 32, …

Si hago n inserciones al final, las copias totales son
4 + 8 + 16 + … + 2^k, con 2^k ≤ n. Esa suma da menos de 2 · 2^k ≤ 2n.
Ejemplo con n = 1000: se redimensiona en 4, 8, …, 512 y las copias son
4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 = 1020 ≈ n.

Costo por inserción = 2n / n = 2 copias en promedio → **O(1) amortizado**.
Por eso insertar al final sale barato aunque a veces haya una copia grande.

## 3. `insertar_ordenado(x)`

Tiene dos pasos:

1. `_posicion_ordenada` hace una búsqueda binaria: el intervalo pasa de
   n a n/2, n/4, … hasta quedar vacío, o sea ⌊log₂ n⌋ + 1 pasos.
2. `insertar(pos, x)`: 2 · (n − pos) + c operaciones, como en el punto 2.

T(n, pos) = (⌊log₂ n⌋ + 1) · c₁ + 2 · (n − pos) + c

- Si x es el más grande (pos = n): solo queda la búsqueda → O(log n).
- Si x cae en el medio (pos = n/2): T ≈ n + log₂ n → O(n).
- Si x es el más pequeño (pos = 0): T ≈ 2n + log₂ n → O(n).

La búsqueda binaria encuentra el sitio rápido, pero no ayuda con lo caro, que
son los desplazamientos. Por eso la complejidad es **O(n)**.

## 4. `buscar_lineal(x)`

Cada vuelta del `while` hace 3 operaciones: la condición `i < _tamaño`, la
comparación `datos[i] == x` y `i = i + 1`.

- Peor caso (x no está): n vueltas → T = 3n + c → **O(n)**.
- Mejor caso (x está primero): 1 vuelta → O(1).
- Caso promedio (x está): n/2 vueltas → 1,5n + c, que sigue siendo O(n).

## 5. `buscar_binaria(x)`

Cada paso hace unas 5 operaciones (calcular `medio`, 1 o 2 comparaciones y
actualizar `izq` o `der`) y deja la mitad del intervalo:

n → n/2 → n/4 → … → 1

El número de pasos k cumple n / 2^k < 1, o sea **k = ⌊log₂ n⌋ + 1**.

| n | log₂ n | pasos (peor caso) |
|---|---|---|
| 1.000 | 9,97 | 10 |
| 10.000 | 13,29 | 14 |
| 80.000 | 16,29 | 17 |
| 200.000 | 17,61 | 18 |

T(n) = 5 · k + c → **O(log n)**. Mejor caso: x está justo en el medio y se
encuentra en el primer paso → O(1).

## Qué espero ver al medir

Voy a medir: `insertar` al inicio (peor caso), `insertar` al final (mejor
caso), `insertar_ordenado` con un valor que cae en el medio, `obtener` en el
medio, `buscar_lineal` con un elemento ausente (peor caso) y `buscar_binaria`
con un elemento ausente (peor caso).

Cuánto debería crecer el tiempo al pasar de n = 80.000 a n = 200.000
(un factor de 200.000 / 80.000 = 2,5):

| Operación | Pasos 80.000 → 200.000 | Crecimiento esperado |
|---|---|---|
| `insertar` al inicio | n → 2,5 n | ≈ ×2,5 |
| `insertar_ordenado` (medio) | ≈ n/2 → 2,5 · n/2 | ≈ ×2,5 |
| `buscar_lineal` (ausente) | n → 2,5 n | ≈ ×2,5 |
| `buscar_binaria` (ausente) | 17 → 18 pasos | ≈ ×1,06 (casi plana) |
| `obtener` | 4 → 4 | ×1 (plana) |
| `insertar` al final | 2 copias → 2 copias | ×1 (plana) |

En la gráfica log-log, las tres curvas O(n) deberían verse como rectas con
pendiente 1, y las otras tres casi horizontales (la binaria sube un poquito).

**Cosas que podrían no coincidir (para revisar después de medir):**

- En Python, una vuelta de desplazar (`insertar`) hace más trabajo que una
  vuelta de comparar (`buscar_lineal`), así que `insertar` al inicio puede
  salir más lento o parecido a `buscar_lineal` aunque ambos sean O(n).
- Con n = 1.000, `obtener` y `buscar_binaria` tardan microsegundos, y el
  ruido del sistema puede tapar la forma de la curva.
- `insertar` al final puede tener algún pico cuando justo toca redimensionar.