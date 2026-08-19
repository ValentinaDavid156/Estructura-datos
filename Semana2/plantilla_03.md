# Plan Técnico — ADT Bolsa

**Especificación de referencia:** spec.md v1.0

## 1. Implementaciones construidas
- BolsaLista: lista con un elemento por aparición
- BolsaDict: diccionario elemento -> cantidad

## 2. Comparación de complejidad
| Operación | BolsaLista | BolsaDict | Comentario |
|-----------|-----------|-----------|------------|
| agregar   | O(1)      | O(1)      | En lista se usa `.append()` al final; en dict es asignación por clave directa.|
| sacar     | O(n)      | O(1)      |En lista requiere buscar/recorrer o hacer `.remove()`; en dict es eliminación directa por clave. |
| cuantos   | O(n)      | O(1)      |En lista requiere contar recorriendo con `.count()`; en dict la cantidad se consulta por clave.|
| tamaño    | O(1)      | O(1)      |Ambos mantienen un contador o usan `len()` de la estructura interna. |

## 3. ¿Cuál conviene?
- BolsaDict: Es la mejor para casi cualquier caso real. Como sacar y cuantos tardan tiempo constante O(1), la aplicación no se frena si la bolsa llega a tener miles de elementos.
- BolsaLista: Solo valdría la pena si son muy poquitos datos (donde la diferencia de rendimiento ni se nota) o si necesitas guardar objetos que no son hashables en Python (como listas o diccionarios), los cuales no se pueden usar como claves en un diccionario sin que saque error.

## 4. Invariantes de representación
- BolsaLista: Cada elemento guardado en la lista representa una unidad (los duplicados se guardan tal cual). El tamaño total de la bolsa siempre coincide con la cantidad de elementos en la lista.

- BolsaDict: ninguna cantidad almacenada puede ser 0 (se elimina la clave)