"""Simulación de la sala de cómputo: FIFO vs cola de prioridad (Actividad 5, parte B).

Modelo
------
- Un técnico atiende una solicitud a la vez (sin interrupciones).
- Jornada de 480 min. Las solicitudes llegan con tiempos entre llegadas
  exponenciales (media 4,4 min) y el servicio dura entre 2 y 6 min (media 4).
  Utilización ≈ 4 / 4,4 ≈ 91 %: la sala se llena, pero no colapsa.
- Niveles: ALTA 15 % (entrega o examen inminente), MEDIA 50 % (clase),
  BAJA 35 % (práctica libre).
- Las tres estrategias reciben EXACTAMENTE las mismas solicitudes (misma semilla),
  así que la diferencia se debe solo a la estrategia.
- Se repite con muchas semillas y se promedia, para no depender de un día con suerte.

Estrategias: FIFO, prioridad sin envejecimiento y prioridad con envejecimiento.
"""

import random

from cola import ColaEnlazada
from cola_prioridad import ColaPrioridad, ALTA, MEDIA, BAJA, NOMBRES_NIVEL

JORNADA = 480.0
LLEGADA_MEDIA = 4.4
SERVICIO_MIN, SERVICIO_MAX = 2.0, 6.0
PROBABILIDADES = ((ALTA, 0.15), (MEDIA, 0.50), (BAJA, 0.35))
INTERVALO = 15.0            # minutos de espera por cada nivel que sube
SEMILLAS = range(300)


class Solicitud:
    __slots__ = ("nivel", "llegada", "servicio")

    def __init__(self, nivel, llegada, servicio):
        self.nivel = nivel
        self.llegada = llegada
        self.servicio = servicio


class ColaFIFO:
    """Adaptador: una sola ColaEnlazada con la misma interfaz que ColaPrioridad."""

    def __init__(self):
        self._cola = ColaEnlazada()

    def encolar(self, dato, nivel, ahora):
        self._cola.encolar(dato)

    def desencolar(self, ahora):
        return self._cola.desencolar()

    def esta_vacia(self):
        return self._cola.esta_vacia()


def _nivel_aleatorio(azar):
    x = azar.random()
    acumulado = 0.0
    for nivel, p in PROBABILIDADES:
        acumulado += p
        if x < acumulado:
            return nivel
    return BAJA


def generar_solicitudes(semilla):
    azar = random.Random(semilla)
    solicitudes = []
    t = azar.expovariate(1 / LLEGADA_MEDIA)
    while t < JORNADA:
        solicitudes.append(
            Solicitud(_nivel_aleatorio(azar), t, azar.uniform(SERVICIO_MIN, SERVICIO_MAX))
        )
        t += azar.expovariate(1 / LLEGADA_MEDIA)
    return solicitudes


def simular(solicitudes, cola):
    """Atiende todas las solicitudes (la cola se vacía después de la jornada).
    Devuelve [(nivel, espera)] con la espera = inicio de atención - llegada."""
    esperas = []
    t = 0.0
    i = 0
    n = len(solicitudes)
    while i < n or not cola.esta_vacia():
        while i < n and solicitudes[i].llegada <= t:
            s = solicitudes[i]
            cola.encolar(s, s.nivel, s.llegada)
            i += 1
        if cola.esta_vacia():
            t = solicitudes[i].llegada          # el técnico espera a la próxima llegada
            continue
        s = cola.desencolar(t)
        esperas.append((s.nivel, t - s.llegada))
        t += s.servicio
    return esperas


ESTRATEGIAS = {
    "FIFO": lambda: ColaFIFO(),
    "Prioridad sin envejecimiento": lambda: ColaPrioridad(None),
    f"Prioridad con envejecimiento ({INTERVALO:g} min)": lambda: ColaPrioridad(INTERVALO),
}


def evaluar(fabrica_cola, semillas=SEMILLAS):
    """Promedia entre semillas: media, peor caso (promedio y máximo) y por nivel."""
    medias, peores = [], []
    por_nivel = {n: ([], []) for n in (ALTA, MEDIA, BAJA)}      # (medias, peores)
    for semilla in semillas:
        esperas = simular(generar_solicitudes(semilla), fabrica_cola())
        medias.append(sum(e for _, e in esperas) / len(esperas))
        peores.append(max(e for _, e in esperas))
        for nivel in por_nivel:
            xs = [e for n, e in esperas if n == nivel]
            if xs:
                por_nivel[nivel][0].append(sum(xs) / len(xs))
                por_nivel[nivel][1].append(max(xs))
    prom = lambda xs: sum(xs) / len(xs)
    return {
        "media": prom(medias),
        "peor_promedio": prom(peores),
        "peor_maximo": max(peores),
        "nivel": {n: (prom(m), prom(p)) for n, (m, p) in por_nivel.items()},
    }


def tabla_markdown(resultados):
    filas = ["| Estrategia | Espera media (min) | Peor espera, promedio (min) | Peor espera, máximo (min) |",
             "|---|---|---|---|"]
    for nombre, r in resultados.items():
        filas.append(f"| {nombre} | {r['media']:.1f} | {r['peor_promedio']:.1f} | {r['peor_maximo']:.1f} |")
    filas += ["", "| Estrategia | Nivel | Espera media (min) | Peor espera, promedio (min) |", "|---|---|---|---|"]
    for nombre, r in resultados.items():
        for nivel in (ALTA, MEDIA, BAJA):
            m, p = r["nivel"][nivel]
            filas.append(f"| {nombre} | {NOMBRES_NIVEL[nivel]} | {m:.1f} | {p:.1f} |")
    return "\n".join(filas)


def barrido_intervalo(intervalos=(5, 10, 15, 30, 60)):
    filas = ["| Intervalo (min) | Espera media | Peor espera (promedio) | Peor espera BAJA (promedio) |", "|---|---|---|---|"]
    for t in intervalos:
        r = evaluar(lambda t=t: ColaPrioridad(t))
        filas.append(f"| {t} | {r['media']:.1f} | {r['peor_promedio']:.1f} | {r['nivel'][BAJA][1]:.1f} |")
    return "\n".join(filas)


if __name__ == "__main__":
    resultados = {nombre: evaluar(f) for nombre, f in ESTRATEGIAS.items()}
    n = len(generar_solicitudes(0))
    print(f"{len(SEMILLAS)} jornadas simuladas (≈{n} solicitudes por jornada).\n")
    print(tabla_markdown(resultados))
    print("\nSensibilidad al intervalo de envejecimiento:\n")
    print(barrido_intervalo())