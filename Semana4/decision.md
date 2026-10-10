# Decisión — ¿conviene mantener el catálogo ordenado?

Uso mis propias mediciones (`resultados.csv`, mediana de varias repeticiones). Comparo dos formas de llevar el catálogo:

- **Ordenado:** cada libro nuevo se inserta en su sitio (`insertar_ordenado`) y se busca con `buscar_binaria`.
- **Desordenado:** cada libro nuevo se agrega al final (`insertar` al final) y se busca con `buscar_lineal`.

Para las búsquedas usé el peor caso (elemento ausente) y para `insertar_ordenado` un valor que cae en el medio del catálogo.

## 1. Tiempos medidos

| Operación | n = 80.000 | n = 200.000 |
|---|---|---|
| `insertar_ordenado` | 3,018 ms | 13,093 ms |
| `buscar_binaria` | 1,44 µs | 1,53 µs |
| `insertar_final` | 0,30 µs | 0,32 µs |
| `buscar_lineal` | 6,553 ms | 9,448 ms |

## 2. Costo total de 1 inserción + b búsquedas

Fórmulas: `ordenado = t_insertar_ordenado + b · t_buscar_binaria` y `desordenado = t_insertar_final + b · t_buscar_lineal`.

| n | Época | b | Ordenado | Desordenado | Conviene |
|---|---|---|---|---|---|
| 80.000 | Vacaciones | 5 | 3,025 ms | 32,763 ms | **ordenado** (10,8× más rápido) |
| 80.000 | Normal | 50 | 3,090 ms | 327,628 ms | **ordenado** (106,0× más rápido) |
| 80.000 | Exámenes | 300 | 3,450 ms | 1,966 s | **ordenado** (569,8× más rápido) |
| 200.000 | Vacaciones | 5 | 13,100 ms | 47,239 ms | **ordenado** (3,6× más rápido) |
| 200.000 | Normal | 50 | 13,169 ms | 472,388 ms | **ordenado** (35,9× más rápido) |
| 200.000 | Exámenes | 300 | 13,552 ms | 2,834 s | **ordenado** (209,1× más rápido) |

## 3. Punto de equilibrio

Igualo los dos costos y despejo b:

`t_io + b·t_bin = t_if + b·t_lin`  →  `b* = (t_io − t_if) / (t_lin − t_bin)`

- n = 80.000: b* = (3,018 ms − 0,30 µs) / (6,553 ms − 1,44 µs) = **0,46 búsquedas por inserción**
- n = 200.000: b* = (13,093 ms − 0,32 µs) / (9,448 ms − 1,53 µs) = **1,39 búsquedas por inserción**

Si hay más búsquedas que b* por cada libro nuevo, conviene ordenado; si hay menos, conviene desordenado.

## 4. Recomendación a la biblioteca

**Conviene mantener el catálogo ordenado**, y la respuesta no cambia con la época: en vacaciones (5 búsquedas por inserción), en un mes normal (50) y en exámenes (300) ordenado sale más rápido, con 80.000 y con 200.000 registros. Solo dejaría de convenir si hubiera menos de unas 1,39 búsquedas por cada libro nuevo, y el caso más bajo que describe la biblioteca ya es 5.

Esto tiene sentido porque insertar ordenado cuesta desplazar, en promedio, la mitad de los elementos (O(n)), pero cada búsqueda lineal recorre todo el catálogo (también O(n)) y la binaria casi nada (O(log n)). Como los dos costos grandes son del mismo orden, con muy pocas búsquedas por inserción ya se paga el mantener el orden.

## 5. Límites de este cálculo

- Medí en mi computador y en Python puro; los números absolutos cambian de máquina a máquina, pero la forma de las curvas y el punto de equilibrio deberían ser parecidos.
- Usé el peor caso en las búsquedas. En promedio una búsqueda lineal recorre la mitad, así que el punto de equilibrio real sería aproximadamente el doble de b*.
- Supuse que los libros nuevos llegan en posiciones al azar (en promedio el medio). Si siempre llegaran al final del orden, ordenar sería todavía más barato.
