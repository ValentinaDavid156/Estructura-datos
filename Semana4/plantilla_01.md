# Especificación — ADT Lista

## 1. Propósito
Colección ordenada de elementos, accesibles por posición, que admite
inserción y eliminación en cualquier punto.

## 2. Operaciones
### insertar(posicion, elemento)
- Precondiciones: 0 <= posicion <= tamaño
- Postcondiciones: el elemento queda en `posicion`; tamaño aumenta en 1;
  el orden relativo de los demás elementos se conserva
- Errores: PosicionInvalidaError

### eliminar(posicion) -> elemento
### obtener(posicion) -> elemento
### buscar(elemento) -> posicion o -1
### tamaño() -> entero

## 3. Invariantes
- INV-01: tamaño >= 0
- INV-02: recorrer la lista visita exactamente `tamaño` elementos
- INV-03: obtener(i) devuelve el elemento insertado en la posición i,
  si no hubo inserciones ni eliminaciones antes de i

## 4. Criterios de aceptación
| ID | Criterio | Prueba |
|----|----------|--------|
| CA-01 | Una lista nueva tiene tamaño 0 | test_lista_vacia |
| CA-02 | Insertar en posición 0 en lista vacía deja el elemento accesible | test_insertar_en_vacia |
| CA-03 | Insertar al inicio desplaza los existentes sin perder ninguno | test_insertar_inicio |
| CA-04 | Eliminar reduce el tamaño en 1 y devuelve el elemento | test_eliminar |
| CA-05 | Posición fuera de rango lanza PosicionInvalidaError | test_posicion_invalida |
| CA-06 | buscar devuelve -1 si el elemento no está | test_buscar_ausente |