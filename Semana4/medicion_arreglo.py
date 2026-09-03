# Código base — Semana 04
# Fuente: 01-Momento-1-Contrato-y-secuencia/04-Semana-04-Arreglos-y-estructuras-estaticas/02-guia-de-laboratorio.html

import time
from lista_arreglo import ListaArreglo

N = 20_000

# Insertar SIEMPRE al final
lista = ListaArreglo()
inicio = time.perf_counter()
for i in range(N):
    lista.insertar(lista.tamaño(), i)
al_final = time.perf_counter() - inicio

# Insertar SIEMPRE al inicio
lista = ListaArreglo()
inicio = time.perf_counter()
for i in range(N):
    lista.insertar(0, i)
al_inicio = time.perf_counter() - inicio

print(f"{N:,} inserciones al final:  {al_final:7.3f} s")
print(f"{N:,} inserciones al inicio: {al_inicio:7.3f} s")
print(f"Al inicio es {al_inicio / al_final:.0f} veces más lento")

# Pregunta: si duplicas N, ¿cuánto esperas que crezca cada uno?
# Compruébalo.
