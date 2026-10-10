"""Parte D — Calcula la decisión a partir de resultados.csv y escribe decision.md.

Costo de una "ronda" (1 inserción + b búsquedas):
    ordenado    = t(insertar_ordenado) + b * t(buscar_binaria)
    desordenado = t(insertar_final)    + b * t(buscar_lineal)

Punto de equilibrio (se igualan los dos costos y se despeja b):
    t_io + b*t_bin = t_if + b*t_lin
    b* = (t_io - t_if) / (t_lin - t_bin)

Uso:  python calcular_decision.py      (lee resultados.csv, escribe decision.md)
"""
import csv

TAMANOS = [80_000, 200_000]
ESCENARIOS = [("Vacaciones", 5), ("Normal", 50), ("Exámenes", 300)]


def leer(ruta="resultados.csv"):
    t = {}
    with open(ruta, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            t[(fila["operacion"], int(fila["n"]))] = float(fila["mediana_segundos"])
    return t


def fmt(segundos):
    """Formatea un tiempo con la unidad que corresponda (coma decimal)."""
    if segundos >= 1:
        texto = f"{segundos:.3f} s"
    elif segundos >= 1e-3:
        texto = f"{segundos * 1e3:.3f} ms"
    else:
        texto = f"{segundos * 1e6:.2f} µs"
    return texto.replace(".", ",")


def num(x, dec=2):
    return f"{x:.{dec}f}".replace(".", ",")


def miles(n):
    """80000 -> '80.000'"""
    return f"{n:,}".replace(",", ".")


def main():
    t = leer()
    L = []
    L.append("# Decisión — ¿conviene mantener el catálogo ordenado?\n")
    L.append("Uso mis propias mediciones (`resultados.csv`, mediana de varias "
             "repeticiones). Comparo dos formas de llevar el catálogo:\n")
    L.append("- **Ordenado:** cada libro nuevo se inserta en su sitio "
             "(`insertar_ordenado`) y se busca con `buscar_binaria`.")
    L.append("- **Desordenado:** cada libro nuevo se agrega al final "
             "(`insertar` al final) y se busca con `buscar_lineal`.\n")
    L.append("Para las búsquedas usé el peor caso (elemento ausente) y para "
             "`insertar_ordenado` un valor que cae en el medio del catálogo.\n")

    L.append("## 1. Tiempos medidos\n")
    L.append("| Operación | n = 80.000 | n = 200.000 |")
    L.append("|---|---|---|")
    for op in ["insertar_ordenado", "buscar_binaria", "insertar_final",
               "buscar_lineal"]:
        fila = " | ".join(fmt(t[(op, n)]) for n in TAMANOS)
        L.append(f"| `{op}` | {fila} |")
    L.append("")

    L.append("## 2. Costo total de 1 inserción + b búsquedas\n")
    L.append("Fórmulas: `ordenado = t_insertar_ordenado + b · t_buscar_binaria` "
             "y `desordenado = t_insertar_final + b · t_buscar_lineal`.\n")
    L.append("| n | Época | b | Ordenado | Desordenado | Conviene |")
    L.append("|---|---|---|---|---|---|")
    veredictos = {}
    for n in TAMANOS:
        for nombre, b in ESCENARIOS:
            ord_ = t[("insertar_ordenado", n)] + b * t[("buscar_binaria", n)]
            des = t[("insertar_final", n)] + b * t[("buscar_lineal", n)]
            if ord_ < des:
                gana, veces = "ordenado", des / ord_
            else:
                gana, veces = "desordenado", ord_ / des
            veredictos[(n, nombre)] = gana
            L.append(f"| {miles(n)} | {nombre} | {b} | {fmt(ord_)} | "
                     f"{fmt(des)} | **{gana}** ({num(veces, 1)}× más rápido) |")
    L.append("")

    L.append("## 3. Punto de equilibrio\n")
    L.append("Igualo los dos costos y despejo b:\n")
    L.append("`t_io + b·t_bin = t_if + b·t_lin`  →  "
             "`b* = (t_io − t_if) / (t_lin − t_bin)`\n")
    equilibrios = {}
    for n in TAMANOS:
        t_io = t[("insertar_ordenado", n)]
        t_if = t[("insertar_final", n)]
        t_lin = t[("buscar_lineal", n)]
        t_bin = t[("buscar_binaria", n)]
        b_eq = (t_io - t_if) / (t_lin - t_bin)
        equilibrios[n] = b_eq
        L.append(f"- n = {miles(n)}: b* = ({fmt(t_io)} − {fmt(t_if)}) / "
                 f"({fmt(t_lin)} − {fmt(t_bin)}) = **{num(b_eq)} búsquedas "
                 f"por inserción**")
    L.append("")
    L.append("Si hay más búsquedas que b* por cada libro nuevo, conviene "
             "ordenado; si hay menos, conviene desordenado.\n")

    L.append("## 4. Recomendación a la biblioteca\n")
    b_max = max(equilibrios.values())
    todos_ordenado = all(v == "ordenado" for v in veredictos.values())
    todos_desordenado = all(v == "desordenado" for v in veredictos.values())
    if todos_ordenado:
        L.append(f"**Conviene mantener el catálogo ordenado**, y la respuesta "
                 f"no cambia con la época: en vacaciones (5 búsquedas por "
                 f"inserción), en un mes normal (50) y en exámenes (300) "
                 f"ordenado sale más rápido, con 80.000 y con 200.000 "
                 f"registros. Solo dejaría de convenir si hubiera menos de "
                 f"unas {num(b_max)} búsquedas por cada libro nuevo, y el "
                 f"caso más bajo que describe la biblioteca ya es 5.\n")
        L.append("Esto tiene sentido porque insertar ordenado cuesta "
                 "desplazar, en promedio, la mitad de los elementos (O(n)), "
                 "pero cada búsqueda lineal recorre todo el catálogo "
                 "(también O(n)) y la binaria casi nada (O(log n)). Como los "
                 "dos costos grandes son del mismo orden, con muy pocas "
                 "búsquedas por inserción ya se paga el mantener el orden.\n")
    elif todos_desordenado:
        L.append(f"**No conviene mantener el catálogo ordenado** en ninguna "
                 f"de las tres épocas: el punto de equilibrio está en "
                 f"b* ≈ {num(b_max)} búsquedas por inserción y los tres "
                 f"escenarios quedan por debajo.\n")
    else:
        L.append("**La respuesta cambia según la época.**\n")
        for n in TAMANOS:
            for nombre, b in ESCENARIOS:
                L.append(f"- {nombre} (b = {b}), n = {miles(n)}: "
                         f"{veredictos[(n, nombre)]}")
        L.append("")
        L.append(f"El cambio ocurre en b* ≈ {num(b_max)} búsquedas por "
                 f"inserción: por encima conviene ordenado, por debajo "
                 f"desordenado.\n")
    L.append("## 5. Límites de este cálculo\n")
    L.append("- Medí en mi computador y en Python puro; los números "
             "absolutos cambian de máquina a máquina, pero la forma de las "
             "curvas y el punto de equilibrio deberían ser parecidos.")
    L.append("- Usé el peor caso en las búsquedas. En promedio una búsqueda "
             "lineal recorre la mitad, así que el punto de equilibrio real "
             "sería aproximadamente el doble de b*.")
    L.append("- Supuse que los libros nuevos llegan en posiciones al azar "
             "(en promedio el medio). Si siempre llegaran al final del "
             "orden, ordenar sería todavía más barato.")

    with open("decision.md", "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("decision.md generado")


if __name__ == "__main__":
    main()