# Plan — Lista de reproducción con dos estructuras

Este documento traduce `spec.md` (el QUÉ y el POR QUÉ) en decisiones
técnicas concretas (el CÓMO).

## 1. Estructura de datos elegida para `ListaEnlazada`

Nodos simples (`Nodo`, definido en `nodo.py`) con dos campos: `dato` y
`siguiente`. La lista mantiene tres atributos:
- `_cabeza`: primer nodo, o `None` si está vacía.
- `_cola`: último nodo, o `None` si está vacía.
- `_tamaño`: cantidad de nodos, mantenido como contador en vez de
  recalcularse recorriendo la lista.

**Por qué mantener `_cola` aparte de `_cabeza`:** sin ella, insertar al
final requeriría recorrer toda la lista para encontrar el último nodo
(O(n)). Con `_cola`, insertar al final es O(1): se accede directo al
último nodo sin recorrer nada.

## 2. Orden de reconexión de nodos

Al insertar o eliminar en el medio de la lista, los enlaces se
reasignan en un orden específico para no perder referencias:

- **Insertar:** primero se hace que el nodo nuevo apunte a lo que
  seguía después del nodo anterior; solo después se hace que el nodo
  anterior apunte al nuevo. Si se hiciera al revés, en el momento de
  reasignar `anterior.siguiente` ya se perdería el único camino hacia
  el resto de la cadena.
- **Eliminar:** el nodo anterior se reconecta directamente con el
  siguiente del nodo que se está sacando, saltándoselo. Si el nodo
  eliminado era la cola, `_cola` se actualiza para apuntar al nodo
  anterior; si no se hace esta actualización, `_cola` queda apuntando
  a un nodo ya inalcanzable desde `_cabeza`.

Esta decisión está documentada con diagramas paso a paso en
`nodos_a_mano.md`.

## 3. Manejo de errores

Se reutiliza `PosicionInvalidaError` (subclase de `IndexError`) tal
como está definida en el contrato de `ListaArreglo`, para que el
comportamiento ante errores sea idéntico entre ambas implementaciones
(RF-06 y RF-07 de `spec.md`).

## 4. Complejidad esperada por operación

| Operación | ListaArreglo | ListaEnlazada |
|---|---|---|
| obtener(i) | O(1) | O(n) — sin acceso directo, hay que recorrer |
| insertar(0) | O(n) — desplaza todo | O(1) — solo reacomoda `_cabeza` |
| insertar(final) | O(1) amortizado | O(1) gracias a `_cola` |
| insertar(medio) | O(n) | O(n) |
| eliminar(0) | O(n) | O(1) |
| eliminar(final) | O(1) | O(n) — hay que llegar al penúltimo |
| buscar | O(n) | O(n) |

## 5. Estrategia de medición (Parte D)

- Construcción de la lista (5.000 elementos) **fuera** del bloque
  cronometrado, para que el tiempo medido corresponda solo a la
  operación de interés.
- 5 repeticiones por operación, se reporta la mediana (no el
  promedio), para amortiguar picos de ruido del sistema operativo.
- Las operaciones mutantes (insertar al principio, eliminar) se miden
  reconstruyendo la lista completa antes de cada repetición, para que
  cada medición parta del mismo estado inicial.

## 6. Archivos que implementan este plan

| Archivo | Contenido |
|---|---|
| `nodo.py` | Clase `Nodo` |
| `lista_enlazada.py` | Clase `ListaEnlazada` |
| `nodos_a_mano.md` | Ejercicio manual de construcción y pérdida de referencias (Parte A) |
| `test_extremos.py` | Pruebas de los 4 casos límite (Parte C) |
| `comparacion.py` | Script de medición (Parte D) |
| `comparacion.md` | Tabla de costos, cálculo del día de emisión y recomendación (Parte D) |