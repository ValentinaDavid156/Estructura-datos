# Registro de ambigüedades — spec del equipo <Valentina David/Jose Miguel Alvarez>

| # | Qué no estaba claro | Qué tuve que asumir |
|---|---------------------|---------------------|
| 1 | ¿sacar() devuelve algo o no devuelve nada? | Asumí que no devuelve nada |
| 2 | ¿Qué devuelve `cuantos()` si el elemento nunca se agregó a la bolsa?| Asumí que devuelve `0`, en vez de lanzar un error — a diferencia de `sacar()`, consultar la cantidad de algo que no está no es un error, solo significa "cero".|
| 3 | Cuando `sacar()` quita la última unidad de un elemento, ¿queda un conteo en `0` o se elimina la entrada por completo?| Asumí que se elimina la entrada por completo. Así `contiene()` devuelve `False` inmediatamente, y no queda "basura" (claves con conteo `0`) rondando en el diccionario interno.|
