# Plan del Proyecto — CDA

## 1. Fases del proyecto

```text
  FASE 1              FASE 2               FASE 3          FASE 4
  cola.py     →    main.py (API)    →     Pruebas    →    Entrega
  (dominio         (expone cola.py
  puro, sin         por HTTP)
  internet)
```

- **Fase 1** se prueba en la terminal, sin servidor, sin internet, sin Postman. Es la prioridad real del proyecto.
- **Fase 2** no reescribe nada de la lógica: solo abre una "puerta" HTTP hacia lo que ya existe en `cola.py`.
- No se empieza el API (Fase 2) sin que `cola.py` esté terminado y probado (Fase 1).

## 2. Arquitectura general

```text
        ┌────────────────────┐
        │      Cliente       │
        └─────────┬──────────┘
                  │  HTTP / JSON          ← Fase 2
        ┌─────────▼──────────────┐
        │    main.py (API)       │   Solo recibe y responde.
        │                        │   Traduce peticiones en llamadas
        │                        │   a ColaAtencion.
        └─────────┬──────────────┘
                  │  llama a métodos
        ┌─────────▼──────────────────────┐
        │    cola.py (dominio)           │   ← Fase 1
        │    clase ColaAtencion          │
        │    lista ordenada por prioridad│
        │    + motor de aceleración      │
        └────────────────────────────────┘
```
## 3. Modelo de datos del turno.

| Campo | Tipo | De dónde sale |
| --- | --- | --- |
| `id` | entero | Lo asigna el sistema automáticamente |
| `tipo` | `PACIENTE` / `VEHICULO` | RF1, RF2 |
| `nombre` | texto | RF1, RF10 |
| `motivo` | texto | RF1, RF10 |
| `prioridad` | entero 1-5 (puede subir sola con el tiempo) | RF1, RF2, RF11 |
| `hora_registro` | fecha/hora | Lo asigna el sistema automáticamente |
| `orden_llegada` | entero interno, para el desempate | Lo asigna el sistema automáticamente |
| `estado` | `EN_ESPERA` / `EN_ATENCION` / `ATENDIDO` / `RETIRADO` | RF1 |
| `telefono` | texto | RF1 |

## 4. Estructura de datos elegida: lista ordenada.

**Regla de orden de la lista:** un turno A va antes que un turno B si:

1. `A.prioridad < B.prioridad`, o
2. `A.prioridad == B.prioridad` y `A.orden_llegada < B.orden_llegada`

**Cómo se comporta cada operación:**

| Operación | Cómo se hace | Costo aproximado |
| --- | --- | --- |
| Registrar un turno | Buscar la posición correcta e insertarlo ahí (`insertar_ordenado`) | Proporcional al tamaño de la cola (recorre hasta encontrar su lugar) |
| Consultar quién sigue | Leer `self._lista[0]` | Inmediato |
| Atender al siguiente | Sacar `self._lista[0]` | Inmediato (solo mueve el resto de la lista una posición) |
| Retirar un turno por id | Buscarlo por id y marcarlo `RETIRADO` (no se saca físicamente) | Proporcional al tamaño de la cola |

## 5. Máquina de estados (RF9)

EN_ESPERA ──atender──▶ EN_ATENCION ──finalizar──▶ ATENDIDO
    │
    └──retirar──▶ RETIRADO

**Transiciones permitidas (las únicas tres que existen):**

1. `EN_ESPERA → EN_ATENCION` (acción: atender)
2. `EN_ATENCION → ATENDIDO` (acción: finalizar)
3. `EN_ESPERA → RETIRADO` (acción: retirar)

**Cualquier otro intento se rechaza explícitamente (RF9)**, por ejemplo:

- Finalizar un turno que no está `EN_ATENCION`.
- Retirar un turno que ya fue `ATENDIDO`.
- Atender un turno que ya está `RETIRADO`.


## 6. TIEMPOS MÁXIMOS DE ESPERA

| Prioridad | Tiempo máximo de espera garantizado |
| --- | --- |
| 1 | 0 min — atención inmediata, no aplica aceleración |
| 2 | 15 min |
| 3 | 40 min |
| 4 | 120 min |
| 5 | Sin máximo fijo (sujeto a disponibilidad) |

*(Tomados directamente de la columna "Espera" de la tabla de reglas de priorización del spec oficial.)*

---

## 7. Mecanismo de aceleración de prioridad

**Qué hace:** si un turno lleva esperando más del tiempo máximo de su prioridad actual, el sistema le **sube un nivel de prioridad** (nunca baja de 1), para que no se quede esperando indefinidamente.

**Cuándo se evalúa:** internamente, dentro de `ColaAtencion`, justo antes de responder a cualquier consulta sobre la cola (ver el siguiente, listar, pedir el resumen). No es un endpoint aparte ni un proceso en segundo plano separado.

### Orden exacto de las operaciones (obligatorio por RNF3)

Con una lista ordenada, este mecanismo mueve dos cosas a la vez: el campo `prioridad` del turno y la **posición** de ese turno dentro de la lista (que depende de la prioridad con la que fue insertado). El orden correcto es:

1. Recorrer **todos** los turnos `EN_ESPERA` y calcular si alguno debe subir de prioridad (sin reordenar la lista todavía).
2. Actualizar el campo `prioridad` de cada turno que lo necesite.
3. **Solo después** de actualizar todos, volver a ordenar la lista completa una sola vez, con el mismo criterio de la sección 4 (`sorted()` o reinsertar todos).

### Qué pasaría mal si se hiciera en otro orden

- Si se reordenara la lista turno por turno, en medio de la revisión, la lista quedaría en un estado a medias (unos turnos ya con su prioridad nueva reflejada en su posición, otros no), y `consultar_siguiente()` podría devolver temporalmente al turno equivocado.

- Si se actualizara el campo `prioridad` sin nunca reordenar la lista, la lista seguiría ordenada según los valores **viejos** (el cambio del dato no reacomoda la lista solo), rompiendo la regla de que "la prioridad es la única ley del orden" (Artículo I de la constitución).
- Por eso: **primero calcular todo, luego actualizar todo, y al final reordenar una sola vez.**

> **Nota importante (RNF5):** esto modifica solo el campo `prioridad`, nunca el campo `estado`. Por eso no contradice la regla de que "mirar no es lo mismo que tocar": los endpoints de solo consulta siguen sin cambiar el `estado` de ningún turno.

## 8. Diseño del API (Fase 2 — después de que cola.py esté listo)

| Método | Ruta | Función | RF / HU |
| --- | --- | --- | --- |
| `POST` | `/turnos` | Registrar un turno nuevo | RF1, RF2, RF10, HU-01 |
| `GET` | `/turnos/siguiente` | Ver quién sigue, sin sacarlo de la cola | RF3, RNF5, HU-02 |
| `POST` | `/turnos/atender` | Atender al siguiente turno | RF4, HU-02 |
| `POST` | `/turnos/{id}/finalizar` | Marcar un turno `EN_ATENCION` como `ATENDIDO` | RF5, RF9, HU-07 |
| `DELETE` | `/turnos/{id}` | Retirar un turno `EN_ESPERA` | RF6, HU-03 |
| `GET` | `/turnos/resumen` | Conteo de turnos por estado (anónimo) | RF7, RNF4, HU-04 |
| `GET` | `/turnos` | Listar turnos en espera, ordenados por prioridad | RF8 |
| `GET` | `/turnos/{id}` | Ver el detalle completo de un turno | HU-06 |


## 9. Cronograma, dependencias, ruta crítica y holgura (Semana 9)

Taller formativo. Pone el proyecto contra el calendario usando los
bloques de trabajo ya definidos en `tasks.md`.

### 9.1 Descomposición en tareas (≤ 8h cada una)

| ID | Tarea | Horas | Depende de |
|---|---|---|---|
| F0 | Documentación SDD (constitución, spec, plan) | 6h | — |
| T1.1 | Modelo de datos + validaciones (RF2, RF10) | 3h | F0 |
| T1.2 | Lista ordenada + inserción + consultar/atender | 4h | T1.1 |
| T1.3 | Máquina de estados (transiciones válidas, RF9) | 2h | T1.1 |
| T1.4 | Aceleración de prioridad (RNF3) | 3h | T1.2 |
| T1.5 | Consultas (resumen, detalle, mostrar_cola) | 2h | T1.2, T1.3 |
| T1.6 | Pruebas del dominio (T01.24–29) | 3h | T1.4, T1.5 |
| T2.1 | Setup FastAPI + modelos Pydantic | 2h | T1.6 |
| T2.2 | Endpoints de escritura (registrar, atender, finalizar, retirar) | 4h | T2.1 |
| T2.3 | Endpoints de lectura (siguiente, resumen, listar, detalle) | 3h | T2.1 |
| T3 | Pruebas E2E del API | 4h | T2.2, T2.3 |
| T4 | Revisión de consistencia + bitácora final | 2h | T3 |

### 9.2 Dependencias reales vs. dependencias inventadas

- **T1.3 no depende de T1.2.** Ambas solo necesitan T1.1 (el modelo de
  datos). Son paralelizables; si en la práctica se hacen en secuencia es
  por ser la misma persona la que programa (límite de recurso), no
  porque T1.3 necesite algo que produzca T1.2.
- **T2.3 no depende de T2.2.** Ambas solo necesitan T2.1 (la instancia
  compartida de `ColaAtencion` y los modelos Pydantic). Igual que el
  caso anterior, es paralelizable en principio.
- Todas las demás dependencias de la tabla son reales: cada tarea
  produce algo que la siguiente necesita para existir (no se puede
  probar lo que no se ha implementado; no se empieza el API sin que el
  dominio esté probado, por regla explícita de este `plan.md`).

### 9.3 Ruta crítica

La cadena más larga es:

`F0 → T1.1 → T1.2 → T1.4 → T1.6 → T2.1 → T2.2 → T3 → T4`

Suma: 6 + 3 + 4 + 3 + 3 + 2 + 4 + 4 + 2 = **31 horas**. Esta es la ruta
crítica: cualquier retraso en una de estas tareas mueve la fecha final
en la misma cantidad. Sus tareas tienen **holgura cero**.

### 9.4 Holgura

| Rama paralela | Suma hasta reencontrarse con la ruta crítica | Holgura |
|---|---|---|
| T1.3 (en vez de T1.2, para llegar a T1.5) | 28h | 3h |
| T2.3 (en vez de T2.2, para llegar a T3) | 30h | 1h |

### 9.5 Prueba del retraso

- Sumar 4h a **T1.4** (ruta crítica) → el hito final se mueve de 31h a
  **35h**.
- Sumar 3h a **T1.3** (3h de holgura) → el hito final **no se mueve**:
  la holgura absorbe el retraso completo.
- Sumar 4h a **T1.3** (una más de su holgura) → el hito final se mueve,
  pero solo **1h** (el excedente sobre la holgura), no las 4h completas.

Conclusión: el mismo retraso cuesta distinto según en qué tarea ocurra.

### 9.6 Diagrama de Gantt

Ver `evidencias/gantt-cda.png`. Barras en naranja: ruta crítica (holgura
cero). Barras en azul: tareas con holgura (T1.3, T2.3).