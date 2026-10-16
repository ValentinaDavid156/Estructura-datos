"""Cola de prioridad de tres niveles con envejecimiento (sin heapq).

Diseño
------
Una cola FIFO (ColaEnlazada) por nivel: ALTA, MEDIA y BAJA. Dentro de cada
nivel el orden es de llegada, así que el elemento más viejo de cada nivel
siempre está al frente. Para decidir quién sigue solo hay que comparar los
TRES frentes: O(1) por operación (3 comparaciones), encolar O(1).

Mecanismo contra la espera indefinida: ENVEJECIMIENTO
-----------------------------------------------------
Cada `intervalo_envejecimiento` minutos de espera, un elemento sube un nivel
de prioridad efectiva (BAJA -> MEDIA -> ALTA). Se atiende primero a quien
tenga menor nivel efectivo; en empate gana quien llegó antes.

    nivel_efectivo = max(ALTA, nivel - espera // intervalo)

Por qué acota la espera: un elemento BAJA que llegó en t0 es ALTA efectivo
desde t0 + 2*intervalo. A partir de ahí, cualquier ALTA que llegue después
tiene la misma prioridad efectiva pero llegó más tarde, así que pierde el
desempate. Lo único que puede estar delante son elementos que ya estaban
en la cola antes de t0, que son una cantidad finita. Sin envejecimiento
(intervalo=None) una ráfaga continua de ALTA deja a BAJA esperando para siempre.

Por qué basta mirar los tres frentes: dentro de un nivel el frente es el de
llegada más antigua, o sea el de más espera y mejor nivel efectivo. Ningún
otro elemento del mismo nivel puede ganarle. Requiere que `ahora` no
retroceda entre llamadas (se valida).

Complejidad: encolar O(1), desencolar O(1) (3 niveles fijos), frente O(1).
"""

from cola import ColaEnlazada, ColaVaciaError

ALTA, MEDIA, BAJA = 0, 1, 2
NOMBRES_NIVEL = {ALTA: "alta", MEDIA: "media", BAJA: "baja"}


class _Entrada:
    """Un elemento con su nivel original, su hora de llegada y su orden global."""

    __slots__ = ("dato", "nivel", "llegada", "orden")

    def __init__(self, dato, nivel, llegada, orden):
        self.dato = dato
        self.nivel = nivel
        self.llegada = llegada
        self.orden = orden


class ColaPrioridad:
    """Cola de prioridad de tres niveles con envejecimiento opcional.

    El tiempo lo aporta quien llama (`ahora`, en minutos): así el
    comportamiento es determinista y se puede probar y simular.
    """

    def __init__(self, intervalo_envejecimiento=None):
        if intervalo_envejecimiento is not None and intervalo_envejecimiento <= 0:
            raise ValueError("el intervalo de envejecimiento debe ser > 0")
        self._intervalo = intervalo_envejecimiento
        self._colas = [ColaEnlazada(), ColaEnlazada(), ColaEnlazada()]
        self._orden = 0
        self._tamaño = 0
        self._ultimo_tiempo = None

    # ---------- consulta ----------
    def esta_vacia(self):
        return self._tamaño == 0

    def tamaño(self):
        return self._tamaño

    def __len__(self):
        return self._tamaño

    def nivel_efectivo(self, entrada, ahora):
        """Nivel de prioridad tras aplicar el envejecimiento."""
        if self._intervalo is None:
            return entrada.nivel
        subidas = (ahora - entrada.llegada) // self._intervalo
        return max(ALTA, entrada.nivel - int(subidas))

    # ---------- operaciones ----------
    def encolar(self, dato, nivel, ahora=0):
        if nivel not in (ALTA, MEDIA, BAJA):
            raise ValueError(f"nivel inválido: {nivel!r}")
        self._avanzar_reloj(ahora)
        self._colas[nivel].encolar(_Entrada(dato, nivel, ahora, self._orden))
        self._orden += 1
        self._tamaño += 1

    def desencolar(self, ahora=0):
        if self.esta_vacia():
            raise ColaVaciaError("desencolar sobre cola prioridad vacía")
        self._avanzar_reloj(ahora)
        cola = self._cola_del_siguiente(ahora)
        self._tamaño -= 1
        return cola.desencolar().dato

    def frente(self, ahora=0):
        if self.esta_vacia():
            raise ColaVaciaError("frente sobre cola prioridad vacía")
        self._avanzar_reloj(ahora)
        return self._cola_del_siguiente(ahora).frente().dato

    # ---------- internos ----------
    def _avanzar_reloj(self, ahora):
        if self._ultimo_tiempo is not None and ahora < self._ultimo_tiempo:
            raise ValueError("el tiempo no puede retroceder")
        self._ultimo_tiempo = ahora

    def _cola_del_siguiente(self, ahora):
        """Cola cuyo frente se atiende primero: menor (nivel efectivo, llegada, orden)."""
        mejor_cola = None
        mejor_clave = None
        for cola in self._colas:
            if cola.esta_vacia():
                continue
            e = cola.frente()
            clave = (self.nivel_efectivo(e, ahora), e.llegada, e.orden)
            if mejor_clave is None or clave < mejor_clave:
                mejor_clave = clave
                mejor_cola = cola
        return mejor_cola