# Estado inicial:  [A, B, C, _, _]   tamaño=3
# Queremos:        [A, X, B, C, _]   tamaño=4

# INCORRECTO (de izquierda a derecha):
#   datos[2] = datos[1]  ->  [A, B, B, _, _]   ¡perdiste C!
#   datos[3] = datos[2]  ->  [A, B, B, B, _]   ¡desastre!

# CORRECTO (de derecha a izquierda):
#   datos[3] = datos[2]  ->  [A, B, C, C, _]
#   datos[2] = datos[1]  ->  [A, B, B, C, _]
#   datos[1] = X         ->  [A, X, B, C, _]   ✓

# En Python, el rango descendente se escribe así:
for i in range(self._tamaño, posicion, -1):
    self._datos[i] = self._datos[i - 1]