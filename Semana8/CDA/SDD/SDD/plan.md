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
