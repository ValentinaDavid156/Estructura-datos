# CONSTITUCIÓN

## Constitución del Proyecto — CDA (Centro Diagnóstico de Atención médica)

Principios no negociables para este proyecto. Toda decisión de diseño tomada en `spec.md`, `plan.md` o `tasks.md` debe poder justificarse contra estos principios; si algo los contradice, se corrige el código o el plan, no la constitución.

---

## Principio 1: La prioridad es la única ley del orden.

El orden de atención se determina exclusivamente por el nivel de prioridad (1 a 5), donde 1 es la máxima urgencia. Ninguna funcionalidad, endpoint o regla de negocio puede alterar este orden, salvo la regla de desempate definida en el Principio 2.

- Menor número de prioridad = mayor urgencia = se atiende primero.
- No existen "atajos" ni excepciones manuales para saltarse el orden de prioridad.

## Principio 2: Desempate por orden de llegada (FIFO)

Cuando dos o más elementos tienen la misma prioridad, se atiende primero al que llegó antes.

- Este criterio es un supuesto adoptado ante la falta de especificación explícita del requerimiento original.
- Cualquier cambio a esta regla debe documentarse en `spec.md` (sección de supuestos) y en la bitácora de IA antes de modificar el código.

## Principio 3: Los casos extremos son parte del contrato, no un extra.

Los siguientes casos deben estar probados explícitamente y deben pasar:

- Cola vacía (consultar, desencolar y sacar deben fallar de forma controlada).
- Cola de un solo turno.
- Sacar el turno que está al frente de la cola.
- Sacar el turno que está al final de la cola.
- Sacar un turno que está en medio de la cola.
- Un turno que cruza el umbral de anti-inanición y sube de nivel efectivo mientras está en espera.

## Principio 4: Una sola cola, sin discriminación por tipo.

Pacientes y vehículos comparten **la misma cola de prioridad**. El campo `tipo` (`PACIENTE` / `VEHICULO`) es un dato informativo, nunca un criterio de orden.

- Está prohibido crear colas separadas por tipo de elemento en esta versión del sistema.
- Cualquier lógica que trate a un tipo como automáticamente más urgente que otro viola este artículo, a menos que se exprese como un nivel de prioridad explícito.

## Principio 5: Todo requisito nace de una necesidad documentada.

Ninguna funcionalidad se implementa sin estar respaldada por un Requisito Funcional (RF) o una Historia de Usuario (HU) en `spec.md`.

- Antes de programar un endpoint o método nuevo, debe existir su HU o su RF correspondiente.
- Si durante la implementación surge una necesidad no documentada, se detiene el desarrollo, se documenta en `spec.md`, y luego se continúa.

## Principio 6: Trazabilidad del proceso.

Todo el proceso de construcción del proyecto, incluida la interacción con la IA, debe quedar registrado.

- Cada decisión de diseño no explícita en el enunciado original se documenta como supuesto en `spec.md`.
- Cada sesión de trabajo con la IA se registra en `bitacora-ia-cda-api.md`, con el prompt textual, la síntesis de la respuesta y la decisión tomada por el estudiante.

## Principio 7: Transiciones de estado controladas

Todo el proceso de registro de pacientes debe estar 100% controlado por medio del API configurada para mostrar el estado en el que se encuentra una persona de la siguiente manera:

- `EN_ESPERA → EN_ATENCION`
- `EN_ATENCION → ATENDIDO`
- `EN_ESPERA → RETIRADO`
