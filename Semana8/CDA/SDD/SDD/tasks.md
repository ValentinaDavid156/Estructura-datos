# CDA API: Sistema de Atención Médica.

> **Orden de trabajo:** no se empieza una fase sin terminar y probar la anterior. La Fase 1 (dominio, `cola.py`) es la prioridad real del proyecto; el API solo la expone.

---

## Fase 0: Documentación SDD

**T00.1:** Analizar el requerimiento

**T00.2:** Definir el sistema de atención y la tabla de reglas de priorización (con tiempos de espera)

**T00.3:** Redactar HU-01 a HU-07 con criterios de aceptación

**T00.4:** Definir RF1-RF11 y RNF1-RNF6

**T00.5:** Redactar la constitución del proyecto

**T00.6:** Redactar el plan

**T00.7:** Mantener actualizada la bitácora de interacción con la IA en cada sesión

---

## Fase 1: Dominio (`cola.py`) — SIN pensar en API todavía

### 1.1 Modelo de datos

**T01.1** — Definir/ampliar la clase `ElementoAtencion` con: `id`, `tipo`, `nombre`, `motivo`, `prioridad`, `hora_registro`, `orden_llegada`, `estado`, `telefono` — RF1

**T01.2** — Definir los valores posibles de `tipo` (`PACIENTE`, `VEHICULO`) y de `estado` (`EN_ESPERA`, `EN_ATENCION`, `ATENDIDO`, `RETIRADO`)

### 1.2 Registro de turnos

**T01.3** — Implementar `registrar()` que reciba tipo, nombre, motivo, prioridad y teléfono

**T01.4** — Validar que `prioridad` esté entre 1 y 5 (si no, lanzar `PrioridadInvalidaError`) — RF2

**T01.5** — Validar que `tipo` sea `PACIENTE` o `VEHICULO` (si no, lanzar `TipoInvalidoError`) — RF2

**T01.6** — Validar que `nombre`, `motivo` y `prioridad` no estén vacíos (si falta alguno, lanzar `CampoObligatorioError`) — RF10

**T01.7** — Asignar automáticamente `id` único, `hora_registro` y `orden_llegada` al crear el turno — RF1

### 1.3 Cola de prioridad con lista ordenada (el corazón del sistema)

**T01.8:** Mantener una lista de Python (`self._lista`) siempre ordenada por `prioridad` y, en caso de empate, por `orden_llegada`

**T01.9:** Implementar la función de comparación "es más urgente o igual" (prioridad menor, o misma prioridad con `orden_llegada` menor)

**T01.10:** Implementar la inserción ordenada al registrar un turno (misma lógica que `insertar_ordenado` de la Actividad 2)

**T01.11:** Implementar `consultar_siguiente()` que devuelva `self._lista[0]` sin sacarlo de la lista ni cambiar su `estado` — RF3, RNF5

**T01.12:** Implementar `atender_siguiente()` que saque `self._lista[0]` y lo pase a `EN_ATENCION` — RF4

### 1.4 Máquina de estados

**T01.13:** Crear una tabla interna de transiciones válidas: `EN_ESPERA→EN_ATENCION`, `EN_ATENCION→ATENDIDO`, `EN_ESPERA→RETIRADO`

**T01.14:** Crear la excepción `TransicionInvalidaError` para cualquier otro intento de cambio de estado

**T01.15:** Implementar `finalizar_atencion()` que solo acepte turnos `EN_ATENCION`

**T01.16:** Implementar `retirar()` que solo acepte turnos `EN_ESPERA` (se marca `RETIRADO`, no se borra físicamente)

### 1.5 Aceleración de prioridad (envejecimiento)

T01.17: Crear la tabla de tiempos máximos de espera por prioridad.

T01.18: Implementar el método interno que calcule, para cada turno `EN_ESPERA`, si superó su tiempo máximo.

T01.19: Aplicar el orden exacto descrito en plan.md sección 7: **(1) calcular todo → (2) actualizar prioridades → (3) reordenar la lista una sola vez** — RNF3

T01.20: Verificar que esta evaluación corre automáticamente antes de `consultar_siguiente()`, `atender_siguiente()`, listar y resumen.

### 1.6 Consultas

T01.21:  Implementar `mostrar_cola()` que devuelva los turnos `EN_ESPERA` ya ordenados (es directamente `self._lista`)

T01.22: Implementar `resumen()` que devuelva **solo conteos por estado** (sin nombre, motivo ni teléfono)

T01.23 : Implementar `obtener_detalle(id)` para consultar todos los datos de un turno específico.

### 1.7 Pruebas del dominio (antes de pasar a la Fase 2)

T01.24: Probar registro válido y con datos inválidos.

T01.25: Probar que la lista queda bien ordenada por prioridad, incluido el desempate.

T01.26: Probar cada transición de estado válida y cada una inválida.

T01.27: Probar la aceleración de prioridad simulando un turno con `hora_registro` vencida y verificar su nueva posición en la lista.

T01.28: Probar que `resumen()` nunca expone datos personales.

T01.29: Correr `python3 cola.py` y `pytest` y confirmar que todo pasa **antes de tocar el API.**

## Fase 2: API (solo después de que la Fase 1 esté 100% probada)

T02.1: Instalar FastAPI y uvicorn, configurar `main.py`

T02.2: Crear una única instancia de `ColaAtencion` compartida por todo el API

T02.3: Modelos Pydantic: `TurnoIn`, `TurnoOut`, `ResumenOut`

T02.4: Endpoint `POST /turnos` → llama a `registrar()` — RF1, RF2, RF10

T02.5: Endpoint `GET /turnos/siguiente` → llama a `consultar_siguiente()` — RF3, RNF5

T02.6: Endpoint `POST /turnos/atender` → llama a `atender_siguiente()` — RF4

T02.7: Endpoint `POST /turnos/{id}/finalizar` → llama a `finalizar_atencion()` — RF5, RF9

T02.8: Endpoint `DELETE /turnos/{id}` → llama a `retirar()` — RF6

T02.9: Endpoint `GET /turnos/resumen` → llama a `resumen()` — RF7, RNF4

T02.10: Endpoint `GET /turnos` → llama a `mostrar_cola()` — RF8

T02.11: Endpoint `GET /turnos/{id}` → llama a `obtener_detalle()` — HU-06

## Fase 3: Pruebas del API

T03.1: Probar cada endpoint con datos válidos e inválidos.

T03.2: Probar que un intento de transición inválida responde 409.

T03.3: Probar que `/turnos/resumen` nunca incluye nombre, motivo ni teléfono.

T03.4: Probar que los endpoints de solo lectura (`GET`) nunca cambian el `estado` de ningún turno — RNF5

T03.5: Probar un escenario completo de principio a fin: registrar, consultar, atender, finalizar, retirar y ver resumen.

## Fase 4: Entrega

T04.1: Revisar que `spec.md`, `plan.md`, `task.md` y `constitucion.md` sean consistentes entre sí.

T04.2: Completar la bitácora de interacción con la IA con todas las sesiones de trabajo.
