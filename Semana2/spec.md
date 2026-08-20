# Especificación — ADT Bolsa

## 1. Propósito
Una bolsa almacena elementos permitiendo repeticiones, sin orden definido.

## 2. Fuera de alcance
- Sin orden de inserción: La secuencia en que se agregan los productos no influye en las operaciones.
- Sin acceso posicional: No se permite acceso mediante índices (ej. `bolsa[0]`).
- Restricción de librerías: Prohibido el uso de `collections.Counter`; la lógica debe ser implementada con tipos primitivos (`list` y `dict`).

## 3. Operaciones

### agregar(elemento)
- Precondiciones: ninguna
- Postcondiciones: la cantidad de `elemento` aumenta en 1; el tamaño aumenta en 1
- Errores: ninguno

### sacar(elemento)
- Precondiciones:  El `elemento` debe existir previamente en la bolsa (`cuantos(elemento) > 0`)
- Postcondiciones:  Disminuye en 1 la cantidad de `elemento` y el tamaño total. Si la cantidad de un elemento llega a 0 en la implementación de diccionario, la clave es purgada.
- Errores:  Lanza `ElementoNoEncontradoError` si el elemento no se encuentra en la bolsa.

### cuantos(elemento)
-  Retorna la cantidad exacta (entero) del `elemento` especificado. Retorna 0 si no existe.

### tamaño()
-  Retorna la suma total de elementos guardados en la bolsa (entero) 

### contiene(elemento)
-  Retorna `True` si `cuantos(elemento) > 0`; de lo contrario, `False`

## 4. Invariantes
- INV-01: tamaño >= 0
- INV-02: tamaño == suma de cuantos(e) para todo e distinto en la bolsa
- INV-03: 'cuantos(e) >= 0` para cualquier objeto `e`

## 5. Criterios de aceptación
| ID | Criterio | Prueba que lo verifica |
|----|----------|------------------------|
| CA-01 | Una bolsa recién creada tiene tamaño 0 | test_bolsa_vacia |
| CA-02 | Agregar el mismo elemento dos veces hace que cuantos() devuelva 2 | test_duplicados |
| CA-03 | Sacar un elemento inexistente lanza ElementoNoEncontradoError | test_sacar_inexistente |
| CA-04 | Sacar el último ejemplar de un elemento lo purga de la estructura |test_sacar_ultimo_elemento |
| CA-05 | `contiene()` devuelve `False` para elementos cuyo conteo bajó a 0 |test_contiene_post_eliminacion |
| CA-06 | Consultar cuantos() de un elemento nunca agregado devuelve 0, sin error | test_cantidad_cero_para_elemento_nunca_agregado |

## 6. Casos extremos considerados
- Bolsa vacía
- Un solo elemento
- Elemento repetido muchas veces
- Sacar el último ejemplar de un elemento

## 7. Decisiones sobre Ambigüedades (Parte A)
- Sacar elementos inexistentes: Se considera una violación de precondición. Debe lanzar la excepción `ElementoNoEncontradoError´
- Purga de memoria: En `carrito_dict.py`, cuando un elemento llega a cantidad 0 tras llamar a `sacar()`, la clave se elimina con `del`.
- Manejo de cantidades: `agregar()` solo incrementa de 1 en 1 por llamada. No se procesan parámetros con valores negativos o nulos.
- Consultas en vacuidad: Si el carrito está vacío, `cuantos(elemento)` y `tamaño()` retornan `0` de forma segura sin arrojar excepciones.

## 8. Registro de ambigüedades — spec del equipo
 
| # | Qué no estaba claro | Qué tuve que asumir |
|---|---|---|
| 1 | ¿`sacar()` devuelve algo o no devuelve nada? | Asumí que no devuelve nada. |
| 2 | ¿Qué devuelve `cuantos()` si el elemento nunca se agregó a la bolsa? | Asumí que devuelve `0`, en vez de lanzar un error — a diferencia de `sacar()`, consultar la cantidad de algo que no está no es un error, solo significa "cero". |
| 3 | Cuando `sacar()` quita la última unidad de un elemento, ¿queda un conteo en `0` o se elimina la entrada? | Asumí que se elimina la entrada por completo. Así `contiene()` devuelve `False` inmediatamente, y no queda "basura" (claves con conteo `0`) rondando en el diccionario interno. |
