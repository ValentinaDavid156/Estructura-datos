# Código base — Semana 04
# Fuente: 01-Momento-1-Contrato-y-secuencia/04-Semana-04-Arreglos-y-estructuras-estaticas/02-guia-de-laboratorio.html

import csv
import statistics
import timeit

from lista_arreglo import ListaArreglo

TAMANOS = [1_000, 10_000, 80_000, 200_000]
REPETICIONES = 7  # la actividad pide mínimo 5


def construir(n):
    lista = ListaArreglo()
    for i in range(n):
        lista.insertar(lista.tamaño(), 2 * i)  # solo pares, ya ordenada
    return lista


def medir(operacion, veces, deshacer=None):
    """Mediana de UNA llamada. Repite REPETICIONES veces con timeit."""
    tiempos = []
    for _ in range(REPETICIONES):
        total = timeit.timeit(operacion, number=veces)
        if deshacer:
            deshacer(veces)  # deja la lista en tamaño n (fuera del cronómetro)
        tiempos.append(total / veces)
    return statistics.median(tiempos)


def medir_tamano(n):
    lista = construir(n)
    medio = 2 * (n // 2) + 1  # impar: cae en el medio

    def quitar_inicio(v):
        for _ in range(v):
            lista.eliminar(0)

    def quitar_final(v):
        for _ in range(v):
            lista.eliminar(lista.tamaño() - 1)

    def quitar_medio(v):
        lista.eliminar(n // 2 + 1)

    return {
        "insertar_inicio": medir(lambda: lista.insertar(0, -1), 1, quitar_inicio),
        "insertar_final": medir(
            lambda: lista.insertar(lista.tamaño(), 2 * n + 1), 100, quitar_final),
        "insertar_ordenado": medir(
            lambda: lista.insertar_ordenado(medio), 1, quitar_medio),
        "obtener": medir(lambda: lista.obtener(n // 2), 10_000),
        "buscar_lineal": medir(lambda: lista.buscar_lineal(-1), 1),
        "buscar_binaria": medir(lambda: lista.buscar_binaria(-1), 10_000),
    }


def graficar(filas):
    import matplotlib.pyplot as plt

    ops = []
    for o, _, _ in filas:
        if o not in ops:
            ops.append(o)

    def serie(op):
        pares = [(n, t) for o, n, t in filas if o == op]
        return [p[0] for p in pares], [p[1] for p in pares]

    plt.figure(figsize=(8, 5))
    for op in ops:
        xs, ys = serie(op)
        plt.plot(xs, ys, marker="o", label=op)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n (registros) [escala logarítmica]")
    plt.ylabel("tiempo por llamada (s) [escala logarítmica]")
    plt.title("ListaArreglo: tiempo de cada operación según n")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafica_superpuesta.png", dpi=150)


def main():
    filas = []
    for n in TAMANOS:
        for op, t in medir_tamano(n).items():
            filas.append((op, n, t))
            print(f"{op:<18}{n:>10,}{t:>16.9f}")
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["operacion", "n", "mediana_segundos"])
        for op, n, t in filas:
            w.writerow([op, n, f"{t:.9f}"])
    graficar(filas)
    print("Listo: resultados.csv y grafica_superpuesta.png")

if __name__ == "__main__":
    main()