# Sistema de Gestión de Atención — CDA

Se requiere un sistema que gestione la atención de **pacientes** y **vehículos** (ambulancias u otros vehículos de emergencia) mediante una **cola de prioridad (CDA)**, expuesta como un **API**. El orden de atención no depende de la llegada, sino de un **nivel de prioridad de 1 a 5**, donde 1 es lo más urgente.

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


## 3. Reglas de priorización (CDA)

| Prioridad | Categoría | Espera | Criterio clínico |
| --- | --- | --- | --- |
| 1 | Crítica / riesgo de vida inminente | **No puede esperar** (atención inmediata) | Riesgo vital inminente. Paro cardiorrespiratorio, shock o trauma severo. |
| 2 | Muy urgente | **No puede esperar** (máximo 10 - 15 min) | Alto riesgo de deterioro rápido o dolor severo. Inestabilidad hemodinámica. |
| 3 | Urgente | Puede esperar (atención prioritaria 30 - 40 min) | Requiere múltiples exámenes/recursos. Signos vitales estables, pero requiere intervención médica. |
| 4 | Poco urgente | Puede esperar (espera media 60 - 120 min) | Condiciones de baja complejidad o lesiones leves (ej. esguinces leves, suturas simples). |
| 5 | No urgente, puede esperar | Puede esperar (atención sujeta a disponibilidad / demanda, o consulta externa) | Cuadro leve o crónico sin signos de alarma (ej. resfriado leve, renovación de fórmulas). |


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

## 5. Requisitos Funcionales (RF)

| ***RF*** | ***DESCRIPCIÓN*** |
| --- | --- |
| RF1 | El sistema debe permitir registrar un turno con tipo, prioridad, nombre, motivo, ID, estado, hora de registro y teléfono. |
| RF2 | El sistema debe validar que la prioridad esté entre 1 y 5, rechazando valores fuera de rango, asimismo que el tipo sea PACIENTE o VEHÍCULO. |
| RF3 | El sistema debe permitir consultar el siguiente turno sin modificar su estado. |
| RF4 | El sistema debe permitir atender (sacar del frente) al siguiente elemento según prioridad y desempate FIFO. |
| RF5 | El sistema debe permitir marcar un turno EN_ATENCIÓN como ATENDIDO. |
| RF6 | El sistema debe permitir retirar de la cola a un elemento si está EN_ESPERA. |
| RF7 | El sistema debe permitir consultar cuántos turnos hay en cada estado. |
| RF8 | El sistema debe permitir listar todos los elementos en espera, ordenados por prioridad y orden de llegada. |
| RF9 | El sistema debe rechazar cualquier transición de estado no permitida (Principio 7) con un error explícito. |
| RF10 | El sistema debe validar que NOMBRE, MOTIVO, PRIORIDAD no esté vacío al registrar un turno. |
| RF11 | El sistema debe **acelerar la prioridad** de los turnos que superen el tiempo máximo de espera garantizado. |

## 6. Requisitos No Funcionales (RNF)

| RNF | **DESCRIPCIÓN** |
| --- | --- |
| RNF1 | Las operaciones de registrar, consultar siguiente y atender deben ejecutarse en tiempo logarítmico (O(n)) respecto al tamaño de la cola. |
| RNF2 | El API debe responder en formato JSON. |
| RNF3 | **Cuando un método mueve más de un "puntero" a la vez** (por ejemplo, al sacar un turno de en medio de la cola), hay que explicar en `plan.md` en qué orden se hacen esos cambios y qué pasaría mal si se hicieran en otro orden |
| RNF4 | El resumen de la cola es anónimo**.** El endpoint que muestra cuántos turnos hay en cada estado (HU-06) nunca muestra nombres ni teléfonos, solo números. |
| RNF5 | Mirar no es lo mismo que tocar. Los endpoints que solo consultan información (ver el siguiente turno, ver el resumen) nunca cambian el estado de ningún turno. |
| RNF6 | Los datos de cada elemento (id, tipo, nombre, prioridad, estado) deben mantenerse consistentes durante todo su ciclo de vida (sin pérdida de información entre operaciones). |

## 7. Criterios de aceptación.

- Dado un tipo (`PACIENTE` o `VEHICULO`), un nombre y una prioridad entre 1 y 5, el sistema crea el registro y lo pone en estado `EN_ESPERA`. (RF1 - RF10)
- Si la prioridad está fuera del rango 1-5, el sistema rechaza el registro con un mensaje de error claro. (RF2 - HU01)
- El sistema asigna automáticamente un `id` único y la `hora_registro`. (RF1)
- Si la cola está vacía, el sistema responde indicando que no hay elementos en espera (no lanza un error genérico). (HU-02)
- Al atender, el elemento cambia de `EN_ESPERA` a `EN_ATENCION` y sale del frente de la cola. (RF3 - RF4)
- El sistema indica si el elemento atendido es un `PACIENTE` o un `VEHICULO`. (RF1)
- Existe una acción para marcar la atención como finalizada (`ATENDIDO`). (RF5 - RF9)
- El sistema expone la cantidad de elementos actualmente `EN_ESPERA`. (HU-04, RF7)
- El sistema expone la cantidad total de elementos `ATENDIDO`. (RF7)
- El sistema devuelve la lista de elementos `EN_ESPERA`, ordenada primero por prioridad y luego por orden de llegada. (RF8)

