# Tareas 

Desglose de `plan.md` en tareas concretas.

## Parte A — La cadena a mano
- [x] Construir 3 nodos sueltos sin usar `ListaEnlazada`.
- [x] Encadenarlos manualmente y recorrerlos con un bucle.
- [x] Documentar, con diagramas, qué pasa si se reasigna el enlace del
      primer nodo antes de guardar el segundo (pérdida de referencia).
- [x] Documentar el caso complementario: un nodo sigue vivo mientras
      alguna variable lo referencie, aunque salga de la cadena
      principal.
- **Entregable:** `nodos_a_mano.md`

## Parte B — La lista enlazada
- [x] Definir `Nodo` en `nodo.py` (dato + siguiente).
- [x] Implementar `ListaEnlazada` con el mismo contrato que
      `ListaArreglo`: `tamaño`, `obtener`, `insertar`, `eliminar`,
      `buscar`.
- [x] Implementar los 5 casos internos: insertar al inicio, insertar
      al final, insertar en el medio, eliminar el primero, eliminar
      cualquier otro.
- [x] Verificar que pasa `test_lista.py` sin modificarlo.
- **Entregables:** `lista_enlazada.py`, `nodo.py`

## Parte C — Los cuatro extremos
- [x] Prueba: lista vacía.
- [x] Prueba: lista de un elemento.
- [x] Prueba: borrar el primero.
- [x] Prueba: borrar el último (verificando que `_cola` se actualiza).
- **Entregable:** `test_extremos.py`

## Parte D — La decisión del reproductor
- [x] Medir las 4 operaciones (insertar al principio, recorrer,
      obtener, eliminar) en ambas estructuras, con 5.000 canciones.
- [x] Calcular el costo total de un día de emisión con cada
      estructura, usando las frecuencias reales dadas.
- [x] Recomendar una estructura, citando los números medidos.
- [x] Explicar qué tendría que cambiar en las frecuencias para que
      cambiara la recomendación.
- **Entregables:** `comparacion.py`, `comparacion.md`


## Verificación final
- [x] `pytest -v` corre sin errores (20/20 pruebas).