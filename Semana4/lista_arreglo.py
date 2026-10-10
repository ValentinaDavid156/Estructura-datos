# Código base — Semana 04
# Fuente: 01-Momento-1-Contrato-y-secuencia/04-Semana-04-Arreglos-y-estructuras-estaticas/02-guia-de-laboratorio.html

from array import array


class PosicionInvalidaError(IndexError):
    """La posición solicitada está fuera del rango válido."""


class ListaArreglo:
    """Lista implementada sobre un arreglo de tamaño fijo con redimensionamiento.

    Atributos internos:
        _datos      arreglo subyacente (capacidad fija en cada momento)
        _capacidad  cuántas posiciones tiene el arreglo
        _tamaño     cuántas posiciones están realmente ocupadas

    Invariante de representación: 0 <= _tamaño <= _capacidad

    Complejidad (n = tamaño de la lista):
        obtener            -> O(1)
        insertar(final)    -> O(1) amortizado
        insertar(inicio)   -> O(n)
        insertar_ordenado  -> O(n)
        eliminar           -> O(n)
        buscar_lineal      -> O(n)
        buscar_binaria     -> O(log n)   (solo si la lista está ordenada)
    """

    CAPACIDAD_INICIAL = 4

    def __init__(self):
        self._capacidad = self.CAPACIDAD_INICIAL
        self._datos = [None] * self._capacidad
        self._tamaño = 0

    # ---------- operaciones públicas ----------

    def tamaño(self):
        return self._tamaño

    def obtener(self, posicion):
        """Devuelve el elemento en `posicion`. O(1)."""
        self._validar(posicion, incluir_final=False)
        return self._datos[posicion]

    def insertar(self, posicion, elemento):
        """Inserta desplazando los elementos siguientes hacia la derecha."""
        self._validar(posicion, incluir_final=True)
        if self._tamaño == self._capacidad:
            self._redimensionar(self._capacidad * 2)
        # Desplaza desde el FINAL hacia atrás. ¿Por qué desde el final?
        # Si lo haces desde el principio, sobrescribes los datos.
        i = self._tamaño
        while i > posicion:
            self._datos[i] = self._datos[i - 1]
            i = i - 1
        self._datos[posicion] = elemento
        self._tamaño += 1

    def insertar_ordenado(self, elemento):
        """Inserta `elemento` en su sitio. Supone que la lista ya está ordenada
        de menor a mayor. Busca la posición con búsqueda binaria y luego
        inserta (los desplazamientos siguen siendo O(n))."""
        posicion = self._posicion_ordenada(elemento)
        self.insertar(posicion, elemento)

    def eliminar(self, posicion):
        """Elimina y devuelve el elemento, desplazando los siguientes."""
        self._validar(posicion, incluir_final=False)
        elemento = self._datos[posicion]

        i = posicion
        while i < self._tamaño - 1:
            self._datos[i] = self._datos[i + 1]
            i = i + 1

        self._tamaño -= 1
        self._datos[self._tamaño] = None
        return elemento

    def buscar_lineal(self, elemento):
        """Devuelve la posición de la primera aparición, o -1. O(n)."""
        i = 0
        while i < self._tamaño:
            if self._datos[i] == elemento:
                return i
            i = i + 1
        return -1

    def buscar(self, elemento):
        """Igual que buscar_lineal (la usan los tests del contrato)."""
        return self.buscar_lineal(elemento)

    def buscar_binaria(self, elemento):
        """Devuelve la posición de `elemento`, o -1. Supone lista ordenada.
        O(log n): en cada paso descarta la mitad del intervalo."""
        izq = 0
        der = self._tamaño - 1
        while izq <= der:
            medio = (izq + der) // 2
            if self._datos[medio] == elemento:
                return medio
            if self._datos[medio] < elemento:
                izq = medio + 1
            else:
                der = medio - 1
        return -1

    # ---------- auxiliares ----------

    def _validar(self, posicion, incluir_final):
        limite = self._tamaño if incluir_final else self._tamaño - 1
        if not 0 <= posicion <= limite:
            raise PosicionInvalidaError(
                f"posicion {posicion} fuera de rango [0, {limite}]"
            )

    def _posicion_ordenada(self, elemento):
        """Primera posición donde `elemento` cabe sin romper el orden
        (después de los iguales). Búsqueda binaria."""
        izq = 0
        der = self._tamaño
        while izq < der:
            medio = (izq + der) // 2
            if self._datos[medio] <= elemento:
                izq = medio + 1
            else:
                der = medio
        return izq

    def _redimensionar(self, nueva_capacidad):
        """Crea un arreglo mayor y copia los elementos. O(n)."""
        nuevo = [None] * nueva_capacidad
        i = 0
        while i < self._tamaño:
            nuevo[i] = self._datos[i]
            i = i + 1
        self._datos = nuevo
        self._capacidad = nueva_capacidad

    # ---------- protocolo de Python ----------

    def __len__(self):
        return self._tamaño

    def __getitem__(self, i):
        return self.obtener(i)

    def __iter__(self):
        for i in range(self._tamaño):
            yield self._datos[i]

    def __repr__(self):
        return f"ListaArreglo({list(self)!r})"