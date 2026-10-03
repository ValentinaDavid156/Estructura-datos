# CONSTITUCIÓN

## Constitución del Proyecto — CDA (Centro Diagnóstico de Atención médica)

Principios no negociables para este proyecto. Toda decisión de diseño tomada en `spec.md`, `plan.md` o `tasks.md` debe poder justificarse contra estos principios; si algo los contradice, se corrige el código o el plan, no la constitución.

---

## Principio 1: La prioridad es la única ley del orden.

El orden de atención se determina exclusivamente por el nivel de prioridad (1 a 5), donde 1 es la máxima urgencia. Ninguna funcionalidad, endpoint o regla de negocio puede alterar este orden, salvo la regla de desempate definida en el Principio 2.

- Menor número de prioridad = mayor urgencia = se atiende primero.
- No existen "atajos" ni excepciones manuales para saltarse el orden de prioridad.

---

## Principio 2: Desempate por orden de llegada (FIFO)

Cuando dos o más elementos tienen la misma prioridad, se atiende primero al que llegó antes.

- Este criterio es un supuesto adoptado ante la falta de especificación explícita del requerimiento original.
- Cualquier cambio a esta regla debe documentarse en `spec.md` (sección de supuestos) y en la bitácora de IA antes de modificar el código.

---

## Principio 3: Los casos extremos son parte del contrato, no un extra.

Los siguientes casos deben estar probados explícitamente y deben pasar:

- Cola vacía (consultar, desencolar y sacar deben fallar de forma controlada).
- Cola de un solo turno.
- Sacar el turno que está al frente de la cola.
- Sacar el turno que está al final de la cola.
- Sacar un turno que está en medio de la cola.
- Un turno que cruza el umbral de anti-inanición y sube de nivel efectivo mientras está en espera.