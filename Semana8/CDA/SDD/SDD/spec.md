# Sistema de Gestión de Atención — CDA

Se requiere un sistema que gestione la atención de **pacientes** y **vehículos** (ambulancias u otros vehículos de emergencia) mediante una **cola de prioridad (CDA)**, expuesta como un **API**. El orden de atención no depende de la llegada, sino de un **nivel de prioridad de 1 a 5**, donde 1 es lo más urgente.

---

## 2. Definición del sistema de atención

El sistema recibe solicitudes de atención de dos tipos de elemento:

| Tipo | Descripción |
| --- | --- |
| `PACIENTE` | Persona que requiere atención médica directa. |
| `VEHICULO` | Ambulancia u otro vehículo de emergencia que transporta un caso. |

Cada elemento registrado tiene:

- **ID**: identificador único, asignado por el sistema.
- **Tipo**: `PACIENTE` o `VEHICULO`.
- **nombre**: nombre completo del paciente.
- **Motivo**: descripción corta del por qué ingresa.
- **prioridad**: entero entre 1 y 5.
- **hora_registro**: fecha/hora de ingreso a la cola.
- **estado**: `EN_ESPERA`, `EN_ATENCION`, `ATENDIDO` o `RETIRADO`.
- **Número de teléfono**: familiar o personal.

---

## 3. Reglas de priorización (CDA)

| Prioridad | Categoría | Espera | Criterio clínico |
| --- | --- | --- | --- |
| 1 | Crítica / riesgo de vida inminente | **No puede esperar** (atención inmediata) | Riesgo vital inminente. Paro cardiorrespiratorio, shock o trauma severo. |
| 2 | Muy urgente | **No puede esperar** (máximo 10 - 15 min) | Alto riesgo de deterioro rápido o dolor severo. Inestabilidad hemodinámica. |
| 3 | Urgente | Puede esperar (atención prioritaria 30 - 40 min) | Requiere múltiples exámenes/recursos. Signos vitales estables, pero requiere intervención médica. |
| 4 | Poco urgente | Puede esperar (espera media 60 - 120 min) | Condiciones de baja complejidad o lesiones leves (ej. esguinces leves, suturas simples). |
| 5 | No urgente, puede esperar | Puede esperar (atención sujeta a disponibilidad / demanda, o consulta externa) | Cuadro leve o crónico sin signos de alarma (ej. resfriado leve, renovación de fórmulas). |

---

## 4. Historias de usuario

### HU-01 — Registrar un elemento en la cola

**Como** personal médico del sistema de atención, **quiero** registrar un paciente o un vehículo con su nivel de prioridad, **para** que quede en la cola de espera correspondiente.

### HU-02 — Consultar quién es el siguiente

**Como** médico, **quiero** consultar quién es el siguiente elemento a atender, **para** prepararme para atenderlo sin sacarlo aún de la cola.

### HU-03 — Retirar un elemento de la cola

**Como** personal médico, **quiero** retirar de la cola a un elemento que ya no requiere esperar, **para** mantener la cola actualizada (por ejemplo, se fue o fue trasladado).

### HU-04 — Monitorear la carga del sistema

**Como** personal médico o supervisor, **quiero** ver cuántos elementos están en espera y cuántos han sido atendidos, **para** monitorear la carga del sistema de atención.

### HU-05 — Aceleración de prioridad

**Como** paciente con prioridad baja, **quiero** que mi prioridad suba si espero más del tiempo garantizado para mi nivel.

### HU-06 — Consultar el detalle de un elemento específico

**Como** operador, **quiero** consultar el estado y los datos de un elemento por su id, **para** dar seguimiento puntual a un caso.

### HU-07 — Finalizar la atención *(RF5, RF9)*

**Como** personal médico, **quiero** marcar un turno `EN_ATENCION` como `ATENDIDO`.

- Solo un turno `EN_ATENCION` puede pasar a `ATENDIDO`.
- Cualquier otro origen (`EN_ESPERA`, `RETIRADO`, `ATENDIDO`) se rechaza con un error explícito (RF9).