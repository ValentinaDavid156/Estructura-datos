# Recorridos del árbol de carpetas — por niveles (cola) vs. con pila

## Árbol de prueba

Entre corchetes, las entregas que hay directamente en cada materia (las demás carpetas tienen 0).

```
Universidad Cooperativa de Colombia                        (nivel 0)
├── Facultad de Ingeniería                                 (nivel 1)
│   ├── Ingeniería de Software                             (nivel 2)
│   │   ├── Estructuras de Datos        [12 entregas]      (nivel 3)
│   │   └── Física                      [ 9 entregas]
│   ├── Ingeniería Mecánica
│   │   └── Termodinámica               [ 7 entregas]
│   └── Ingeniería Civil
│       └── Estática                    [ 6 entregas]
├── Facultad de Medicina
│   ├── Medicina
│   │   └── Anatomía                    [10 entregas]
│   ├── Enfermería
│   │   └── Fundamentos de Enfermería   [ 8 entregas]
│   └── Psicología
│       └── Psicología General          [ 5 entregas]
├── Facultad de Derecho
│   └── Derecho
│       └── Derecho Constitucional      [ 4 entregas]
└── Facultad de Odontología
    └── Odontología
        └── Anatomía Dental             [ 3 entregas]
```

Verificación a mano de las otras dos consultas:

- **Total bajo la UCC:** 12 + 9 + 7 + 6 + 10 + 8 + 5 + 4 + 3 = **64**.
  Bajo `Facultad de Ingeniería`: 34. Bajo `Ingeniería de Software`: 21. Bajo `Facultad de Medicina`: 23.
- **Profundidad máxima:** 3 (la raíz es el nivel 0). Todas las materias están en el nivel 3, así que hay empate;
  gana la primera rama, y la ruta es
  `Universidad Cooperativa de Colombia / Facultad de Ingeniería / Ingeniería de Software / Estructuras de Datos`.

## Salida por niveles (con la cola propia `ColaEnlazada`)

```
Nivel 0: ['Universidad Cooperativa de Colombia']
Nivel 1: ['Facultad de Ingeniería', 'Facultad de Medicina', 'Facultad de Derecho', 'Facultad de Odontología']
Nivel 2: ['Ingeniería de Software', 'Ingeniería Mecánica', 'Ingeniería Civil', 'Medicina', 'Enfermería', 'Psicología', 'Derecho', 'Odontología']
Nivel 3: ['Estructuras de Datos', 'Física', 'Termodinámica', 'Estática', 'Anatomía', 'Fundamentos de Enfermería', 'Psicología General', 'Derecho Constitucional', 'Anatomía Dental']
```

## El mismo recorrido con pila (solo cambia el contenedor)

```
Universidad Cooperativa de Colombia, Facultad de Odontología, Odontología, Anatomía Dental,
Facultad de Derecho, Derecho, Derecho Constitucional,
Facultad de Medicina, Psicología, Psicología General, Enfermería, Fundamentos de Enfermería, Medicina, Anatomía,
Facultad de Ingeniería, Ingeniería Civil, Estática, Ingeniería Mecánica, Termodinámica,
Ingeniería de Software, Física, Estructuras de Datos
```

Las dos versiones visitan las mismas 22 carpetas; solo cambia el orden.

## Por qué difieren

El algoritmo es idéntico en las dos versiones: sacar un nodo, visitarlo y meter sus hijos de izquierda a
derecha. Lo único que cambia es **qué nodo sale primero**.

- **Cola (FIFO):** sale el que lleva más tiempo esperando. Las cuatro facultades entran antes que cualquier
  programa, así que salen antes; los programas entran antes que cualquier materia, y así sucesivamente.
  Todo el nivel *k* entra a la cola antes que cualquier nodo del nivel *k+1*, por lo que sale antes: eso es
  exactamente el recorrido por niveles.
- **Pila (LIFO):** sale el último que entró. Tras visitar la UCC entran las cuatro facultades y sale
  `Facultad de Odontología` (la última). Sus hijos entran encima y salen antes de que `Facultad de Derecho`
  vuelva a ser el tope. La pila se hunde por una rama hasta el fondo (`Odontología → Anatomía Dental`) antes de
  volver a la siguiente: es un recorrido en profundidad. Como los hijos se meten de izquierda a derecha, el
  último hijo sale primero, lo que da un preorden con los hijos en orden inverso (derecha a izquierda).

La **causa** es la disciplina de salida del contenedor (FIFO frente a LIFO), no el código del recorrido.