# Especificación — Lista de reproducción con dos estructuras

## 1. Contexto y objetivo

El reproductor de una emisora universitaria necesita mantener una
lista de canciones. Ya existe una implementación (`ListaArreglo`, de
la actividad anterior). El objetivo de este trabajo es construir una
segunda implementación (`ListaEnlazada`) con exactamente el mismo
comportamiento observable desde afuera, y decidir — con datos medidos,
no con intuición — cuál de las dos estructuras le conviene al
reproductor, dado el patrón real de uso de una semana de emisión.

## 2. Requisitos funcionales

**RF-01 — Tamaño consultable.**
CUANDO se consulte el tamaño de la lista, EL SISTEMA DEBE devolver la
cantidad de canciones almacenadas actualmente.

**RF-02 — Acceso por posición.**
CUANDO se pida la canción en una posición válida, EL SISTEMA DEBE
devolver esa canción sin alterar el resto de la lista.

**RF-03 — Inserción en cualquier posición.**
CUANDO se inserte una canción en una posición válida, EL SISTEMA DEBE
agregarla ahí, aumentar el tamaño en uno, y conservar el orden
relativo de las demás canciones.

**RF-04 — Eliminación por posición.**
CUANDO se elimine la canción en una posición válida, EL SISTEMA DEBE
quitarla, devolver la canción eliminada, y disminuir el tamaño en uno.

**RF-05 — Búsqueda por contenido.**
CUANDO se busque una canción por su valor, EL SISTEMA DEBE devolver su
posición si existe, o un indicador de "no encontrada" si no existe.

**RF-06 — Rechazo de posiciones inválidas.**
SI se pide acceder, insertar o eliminar en una posición fuera del
rango permitido, ENTONCES EL SISTEMA DEBE rechazar la operación con un
error, sin modificar el estado de la lista.

**RF-07 — Contrato equivalente entre implementaciones.**
DONDE existan dos implementaciones de la lista de reproducción, EL
SISTEMA DEBE comportarse de forma indistinguible entre ellas desde el
punto de vista de quien las usa (mismas entradas producen las mismas
salidas y los mismos errores).

**RF-08 — Decisión basada en evidencia.**
CUANDO se deba recomendar una estructura para el reproductor, EL
SISTEMA DEBE apoyar la recomendación en mediciones de tiempo reales
sobre las operaciones de uso frecuente, no en supuestos generales
sobre qué estructura "debería" ser más rápida.

## 3. Requisitos no funcionales

- **RNF-01 — Trazabilidad de la memoria.** El comportamiento de la
  lista ante la pérdida de referencias entre elementos debe quedar
  documentado con ejemplos concretos, no solo mencionado.
- **RNF-02 — Reproducibilidad de las mediciones.** Cualquier medición
  de tiempo debe poder repetirse y dar resultados del mismo orden de
  magnitud, no una sola lectura aislada.
- **RNF-03 — Escala del caso de uso.** Las mediciones deben reflejar
  el tamaño real esperado del catálogo del reproductor (miles de
  canciones), no un puñado de elementos de prueba.

## 4. Casos límite

- Lista vacía (consultar, buscar o eliminar sobre ella).
- Lista con un solo elemento.
- Eliminar el primer elemento de la lista.
- Eliminar el último elemento de la lista.
- Insertar en el extremo inicial y en el extremo final.
- Buscar un elemento que no existe.

## 5. Fuera de alcance

- Persistencia de la lista en disco o base de datos.
- Concurrencia (varios procesos modificando la lista al mismo tiempo).
- Ordenar la lista de reproducción automáticamente.
- Cualquier interfaz de usuario del reproductor.


## 6. Criterios de aceptación 
 
| ID | Criterio | Prueba | ListaArreglo | ListaEnlazada |
|---|---|---|---|---|
| CA-01 | Una lista nueva tiene tamaño 0 | `test_lista_vacia` | Sí | Sí |
| CA-02 | Insertar en posición 0 en lista vacía deja el elemento accesible | `test_insertar_en_vacia` | Sí | Sí |
| CA-03 | Insertar al inicio desplaza los existentes sin perder ninguno | `test_insertar_inicio` | Sí | Sí |
| CA-04 | Eliminar reduce el tamaño en 1 y devuelve el elemento | `test_eliminar` | Sí | Sí |
| CA-05 | Posición fuera de rango lanza `PosicionInvalidaError` | `test_posicion_invalida` | Sí | Sí |
| CA-06 | `buscar` devuelve -1 si el elemento no está | `test_buscar_ausente` | Sí | Sí |

## 7. Criterios de finalización

- Los 7 criterios de aceptación heredados del contrato de la Actividad
  2 pasan para ambas implementaciones.
- Los 6 casos límite adicionales de esta actividad pasan.
- Existe una recomendación explícita (una de las dos estructuras),
  respaldada por una tabla de costos medidos y por el cálculo del
  costo de un día completo de emisión.
- Se explica qué tendría que cambiar en las frecuencias de uso para
  que la recomendación cambiara.

## 8. Dudas abiertas

- [NECESITA ACLARACIÓN] "Ir a la canción número N": ¿se refiere
  siempre a una posición fija, o a una posición que varía según qué
  tan avanzada esté la emisión? Se asumió una posición representativa
  fija (el medio de la lista) por simplicidad de medición.
- [NECESITA ACLARACIÓN] ¿El reproductor necesita alguna vez insertar o
  eliminar en una posición intermedia (no al inicio ni al final), o
  esas operaciones son exclusivas del catálogo y no del flujo normal
  de la emisora? Se asumió que sí pueden ocurrir, por eso el contrato
  las exige, aunque no tengan una frecuencia diaria asignada en el
  caso de uso.