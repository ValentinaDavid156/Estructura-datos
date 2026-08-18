# Plan Técnico — ADT Bolsa

**Especificación de referencia:** spec.md v1.0

## 1. Implementaciones construidas
- BolsaLista: lista con un elemento por aparición
- BolsaDict: diccionario elemento -> cantidad

## 2. Comparación de complejidad
| Operación | BolsaLista | BolsaDict | Comentario |
|-----------|-----------|-----------|------------|
| agregar   | O(1)      | O(1)      | |
| sacar     | O(n)      | O(1)      | |
| cuantos   | O(n)      | O(1)      | |
| tamaño    | O(1)      | O(1)      | |

## 3. ¿Cuál conviene?
<Argumenta: ¿en qué caso de uso preferirías cada una? ¿Hay algún escenario
donde BolsaLista sea mejor a pesar de sus complejidades peores?>

## 4. Invariantes de representación
- BolsaLista: <completa>
- BolsaDict: ninguna cantidad almacenada puede ser 0 (se elimina la clave)