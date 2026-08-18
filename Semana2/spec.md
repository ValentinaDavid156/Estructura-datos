# Especificación — ADT Bolsa

## 1. Propósito
Una bolsa almacena elementos permitiendo repeticiones, sin orden definido.

## 2. Fuera de alcance
<¿Qué NO hace? Por ejemplo: no mantiene orden de inserción, no permite indexar>

## 3. Operaciones

### agregar(elemento)
- Precondiciones: ninguna
- Postcondiciones: la cantidad de `elemento` aumenta en 1; el tamaño aumenta en 1
- Errores: ninguno

### sacar(elemento)
- Precondiciones: <completa>
- Postcondiciones: <completa>
- Errores: <completa>

### cuantos(elemento)
- <completa>

### tamaño()
- <completa>

### contiene(elemento)
- <completa>

## 4. Invariantes
- INV-01: tamaño >= 0
- INV-02: tamaño == suma de cuantos(e) para todo e distinto en la bolsa
- INV-03: <completa>

## 5. Criterios de aceptación
| ID | Criterio | Prueba que lo verifica |
|----|----------|------------------------|
| CA-01 | Una bolsa recién creada tiene tamaño 0 | test_bolsa_vacia |
| CA-02 | Agregar el mismo elemento dos veces hace que cuantos() devuelva 2 | test_duplicados |
| CA-03 | Sacar un elemento inexistente lanza ElementoNoEncontradoError | test_sacar_inexistente |
| CA-04 | <completa> | |
| CA-05 | <completa> | |

## 6. Casos extremos considerados
- Bolsa vacía
- Un solo elemento
- Elemento repetido muchas veces
- Sacar el último ejemplar de un elemento