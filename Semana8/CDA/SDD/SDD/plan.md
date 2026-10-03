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