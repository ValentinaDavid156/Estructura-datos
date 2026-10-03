# CDA API: Sistema de Atención Médica

> **Orden de trabajo:** no se empieza una fase sin terminar y probar la anterior. La Fase 1 (dominio, `cola.py`) es la prioridad real del proyecto; el API solo la expone.

---

## Fase 0 — Documentación SDD

- [x] **T00.1:** Analizar el requerimiento
- [x] **T00.2:** Definir el sistema de atención y la tabla de reglas de priorización (con tiempos de espera)
- [x] **T00.3:** Redactar HU-01 a HU-07 con criterios de aceptación
- [x] **T00.4:** Definir RF1-RF11 y RNF1-RNF6
- [x] **T00.5:** Redactar la constitución del proyecto
- [x] **T00.6:** Redactar el plan
- [ ] **T00.7:** Mantener actualizada la bitácora de interacción con la IA en cada sesión

---

## Fase 1 — Dominio (`cola.py`) — SIN pensar en API todavía

### 1.1 Modelo de datos

- [ ] **T01.1** — Definir/ampliar la clase `ElementoAtencion` con: `id`, `tipo`, `nombre`, `motivo`, `prioridad`, `hora_registro`, `orden_llegada`, `estado`, `telefono` — RF1
- [ ] **T01.2** — Definir los valores posibles de `tipo` (`PACIENTE`, `VEHICULO`) y de `estado` (`EN_ESPERA`, `EN_ATENCION`, `ATENDIDO`, `RETIRADO`)

### 1.2 Registro de turnos

- [ ] **T01.3** — Implementar `registrar()` que reciba tipo, nombre, motivo, prioridad y teléfono
- [ ] **T01.4** — Validar que `prioridad` esté entre 1 y 5 (si no, lanzar `PrioridadInvalidaError`) — RF2
- [ ] **T01.5** — Validar que `tipo` sea `PACIENTE` o `VEHICULO` (si no, lanzar `TipoInvalidoError`) — RF2
- [ ] **T01.6** — Validar que `nombre`, `motivo` y `prioridad` no estén vacíos (si falta alguno, lanzar `CampoObligatorioError`) — RF10
- [ ] **T01.7** — Asignar automáticamente `id` único, `hora_registro` y `orden_llegada` al crear el turno — RF1

### 1.3 Cola de prioridad con lista ordenada (el corazón del sistema)

- [ ] **T01.8:** Mantener una lista de Python (`self._lista`) siempre ordenada por `prioridad` y, en caso de empate, por `orden_llegada`
- [ ] **T01.9:** Implementar la función de comparación "es más urgente o igual" (prioridad menor, o misma prioridad con `orden_llegada` menor)
- [ ] **T01.10:** Implementar la inserción ordenada al registrar un turno (misma lógica que `insertar_ordenado` de la Actividad 2)
- [ ] **T01.11:** Implementar `consultar_siguiente()` que devuelva `self._lista[0]` sin sacarlo de la lista ni cambiar su `estado` — RF3, RNF5
- [ ] **T01.12:** Implementar `atender_siguiente()` que saque `self._lista[0]` y lo pase a `EN_ATENCION` — RF4

### 1.4 Máquina de estados

- [ ] **T01.13:** Crear una tabla interna de transiciones válidas: `EN_ESPERA→EN_ATENCION`, `EN_ATENCION→ATENDIDO`, `EN_ESPERA→RETIRADO`
- [ ] **T01.14:** Crear la excepción `TransicionInvalidaError` para cualquier otro intento de cambio de estado
- [ ] **T01.15:** Implementar `finalizar_atencion()` que solo acepte turnos `EN_ATENCION`
- [ ] **T01.16:** Implementar `retirar()` que solo acepte turnos `EN_ESPERA` (se marca `RETIRADO`, no se borra físicamente)

### 1.5 Aceleración de prioridad (envejecimiento)

- [ ] **T01.17:** Crear la tabla de tiempos máximos de espera por prioridad
- [ ] **T01.18:** Implementar el método interno que calcule, para cada turno `EN_ESPERA`, si superó su tiempo máximo
- [ ] **T01.19:** Aplicar el orden exacto descrito en `plan.md` sección 7: (1) calcular todo → (2) actualizar prioridades → (3) reordenar la lista una sola vez — RNF3