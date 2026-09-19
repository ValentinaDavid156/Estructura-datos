# Arreglo frente a lista enlazada

## Tabla de complejidad
| Operación          | ListaArreglo | ListaEnlazada | ¿Quién gana? |
|--------------------|--------------|---------------|--------------|
| obtener(i)         | O(1)         | O(n)          | Arreglo      |
| insertar al inicio | O(n)         | O(1)          | Enlazada     |
| insertar al final  | O(1) amort.  | O(1)          | Empate       |
| insertar en medio  | O(n)         | O(n)          | ?            |
| eliminar al inicio | O(n)         | O(1)          | Enlazada     |
| eliminar al final  | O(1)         | O(n)          | Arreglo      |
| buscar             | O(n)         | O(n)          | Empate       |
| memoria por elem.  | ?            | ?             | ?            |

## Medición
<Cronometra 20.000 inserciones al inicio en cada una. Pega los números.>

## ¿Cuál usarías para...?
1. Un historial de navegación donde solo agregas y quitas del final: <justifica>
2. Una cola de impresión donde agregas al final y quitas del inicio: <justifica>
3. Un catálogo que se consulta mucho por índice y casi nunca cambia: <justifica>
4. Una lista de tareas donde insertas prioridades al principio: <justifica>

## Conclusión
<No hay ganador absoluto. Hay perfiles de costo distintos.
Explica en tres líneas cuál es el criterio para elegir.>