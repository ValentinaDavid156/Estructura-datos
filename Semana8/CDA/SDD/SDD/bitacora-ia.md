# Bitácora de interacción con la IA — CDA API

> Registro exigido por el Principio 6 de la constitución: prompt textual, síntesis de la respuesta y decisión del estudiante.
> Cada sesión incluye el **prompt textual** (lo que se escribió realmente, sin editar) y una **versión reformulada** de ese prompt, solo para claridad. La reformulación no reemplaza al original.
> Herramienta: Claude (Anthropic). Fecha de las sesiones: 2026-10-03.

---

## Sesión 1 — Completar `ColaPrioridad` y crear `test_cola_atencion.py`

**Prompt (textual):**
> Tengo el siguiente código en Python que aún está incompleto. Necesito que me ayudes a completar la lógica respetando la estructura existente y siguiendo buenas prácticas [código base de `ColaPrioridad`, Semana 09]
> y adicionalmente el `test_Cola_atención`
> Analiza si la documentación del SDD de la Semana 8 (constitución, spec, plan y tasks) es consistente entre sí y confirma si el plan de pruebas cubre adecuadamente todas las reglas y casos extremos especificados


**Síntesis de la respuesta:**
- Se completó `ColaPrioridad`: `encolar` guarda `(prioridad, orden, dato)`; `desencolar` y `frente` usan un helper `_indice_minimo()` por búsqueda lineal (O(n)) que compara solo `(prioridad, orden)`, así el empate sale FIFO.
- Se definió `ColaVaciaError`, que faltaba.
- Se escribió `test_cola_atencion.py` con 42 pruebas que cubren T01.24 a T01.28 y los casos extremos del Principio 3 (cola vacía, un solo turno, retirar frente/medio/final, transiciones de estado, aceleración, resumen anónimo).
- Para validar los tests se usó una `ColaAtencion` de referencia escrita según el SDD (no forma parte del repo). Resultado: 44 pruebas pasaron (42 + 2 de `ColaPrioridad`).
- Una prueba de aceleración falló en el primer intento por un error en la expectativa del propio test (el turno vencido P3→P2 empata con el P2 y gana por FIFO); se corrigió la expectativa.

**Revisión del SDD (hallazgos de la IA):**
1. RNF1 dice "logarítmico (O(n))": O(n) es lineal.
2. `retirar()` marca `RETIRADO` sin sacar de la lista, pero `mostrar_cola()` debe devolver solo `EN_ESPERA`; además `resumen()` y `obtener_detalle()` necesitan un registro por id que el plan no define.
3. La aceleración no aclara si el tiempo se mide desde `hora_registro` o desde la última subida.
4. Los criterios de aceptación no cubren HU-03, HU-05 ni HU-06.
5. Referencias cruzadas erradas: RNF4 cita HU-06 (es HU-04); `plan.md` dice "Artículo I" (es Principio 1); T04.1 nombra `task.md`/`constitucion.md` (son `tasks.md`/`constitution.md`); ruta del Gantt distinta de la real.
6. `VEHÍCULO` con tilde en RF2 vs. `VEHICULO` en el resto.
7. Esta bitácora estaba vacía.

**Decisión del estudiante:** _(completar: qué hallazgos corregirá y cuáles no)_

1. Se corrige RNF1 por O(n)
4. Se corrigen los criterios de aceptación que cubren las HU
7. Se completa la bitácora

## Sesión 2 — Para qué sirve el test

**Prompt (textual):**
> Explica para qué sirve y en qué consiste la prueba de cola de atención

**Síntesis de la respuesta:** El test verifica que `ColaAtencion` cumple las reglas del SDD antes de pasar al API (tarea T01.29). Se usa escribiendo `cola.py`, corriendo `pytest -v` y leyendo el nombre del test que falla para saber qué regla se incumple. En el repo todavía no existe `cola.py`.

**Decisión del estudiante:** Entender el rol del test dentro de la Fase 1.

Se comprendió

## Sesión 3 — Cómo ejecutar las pruebas de `ColaPrioridad`

**Prompt (textual):**
> Revisa este test en Python, necesito llamar explícitamente a index o acceder al elemento por su índice para que la prueba pase correctamente, o la como se encuentra actualmente ya es suficiente?

**Síntesis de la respuesta:**
- No hay que "llamar a un index": las pruebas las ejecuta `pytest` (`pip install pytest`, luego `pytest cola_prioridad.py -v`; debe salir `2 passed`).
- Pytest solo descubre archivos `test_*.py`; por eso se indica el nombre del archivo o se mueven las pruebas a `test_cola_prioridad.py`.
- El código estaba completo. Se sugirieron dos pruebas opcionales: `test_desencolar_vacia` y `test_frente_no_modifica` (requieren `import pytest`).

**Decisión del estudiante:** Ejecutar con `pytest cola_prioridad.py -v`. Pruebas opcionales: _(completar si las agregó)_

No se agregaron las pruebas opcionales

## Sesión 4 — Revisión de la versión propia de `cola_prioridad.py`

**Prompt (textual):**
> Verifica este código, le hace falta algo? [versión del estudiante de `ColaPrioridad`]
> Analiza los cambios [segunda versión]


**Síntesis de la respuesta:**
- Primera versión: faltaban `_indice_minimo()` y `ColaVaciaError`, y `__len__` estaba duplicado.
- Segunda versión: `_indice_minimo()` quedó correcto, se eliminó el `__len__` duplicado y se agregó `import pytest`. Solo faltaba `ColaVaciaError` (sin ella, `desencolar()` y `frente()` dan `NameError` con la cola vacía).

**Decisión del estudiante:** Escribió `_indice_minimo()` por su cuenta (con la variable `menor`), eliminó el `__len__` repetido y agregó `import pytest`. Pendiente al cierre de la sesión: definir `ColaVaciaError` antes de la clase.

Se definió la clase ColaVaciaError

## Sesión 5 — Revisión de `test_cola_atencion.py`

**Prompt (textual):**
> Revisa esta prueba [`test_cola_atencion.py`], hazme saber si esta correcta


**Síntesis de la respuesta:** El archivo es correcto (equivale al entregado, con una línea en blanco menos). Para que corra se necesita un `cola.py` con `ColaAtencion` y 6 excepciones (`ColaVaciaError`, `CampoObligatorioError`, `PrioridadInvalidaError`, `TipoInvalidoError`, `TransicionInvalidaError`, `TurnoNoEncontradoError`), que los turnos tengan `hora_registro` modificable y que la aceleración se calcule con ese campo. Se advirtió que `TurnoNoEncontradoError` no está en `tasks.md` (Principio 5) y que el `test_cola.py` de la semana 9 ya importa de `cola`, por lo que conviene decidir si `ColaAtencion` va en `cola.py` o en `cola_atencion.py`.

**Decisión del estudiante:** Conservar `test_cola_atencion.py`. Pendiente: crear `ColaAtencion`, documentar `TurnoNoEncontradoError` en `tasks.md` y decidir el nombre del archivo.

Se implementaron las 6 excepciones.

## Pendientes generales

- [x] Definir `ColaVaciaError` en `cola_prioridad.py`.
- [ ] Implementar `ColaAtencion` (Fase 1) y correr `pytest` (T01.29).
- [x] Corregir las inconsistencias del SDD listadas en la Sesión 1.
- [x] Agregar `TurnoNoEncontradoError` a `tasks.md` / `spec.md`.
- [x] Completar las decisiones marcadas como _(completar)_.