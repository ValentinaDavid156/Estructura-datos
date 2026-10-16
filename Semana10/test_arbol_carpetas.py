from arbol_carpetas import (
    Carpeta, construir_arbol_prueba, total_entregas, profundidad_maxima,
    ruta_mas_profunda, listado_por_niveles, recorrido_con_cola, recorrido_con_pila,
)


def buscar(raiz, nombre):
    """Auxiliar de prueba: busca una carpeta por nombre (nombres únicos)."""
    if raiz.nombre == nombre:
        return raiz
    for h in raiz.hijos:
        r = buscar(h, nombre)
        if r:
            return r
    return None


# ---- casos límite ----
def test_arbol_vacio():
    assert total_entregas(None) == 0
    assert profundidad_maxima(None) == -1
    assert ruta_mas_profunda(None) == []
    assert listado_por_niveles(None) == []


def test_un_solo_nodo():
    solo = Carpeta("solo", 3)
    assert total_entregas(solo) == 3
    assert profundidad_maxima(solo) == 0
    assert ruta_mas_profunda(solo) == ["solo"]
    assert listado_por_niveles(solo) == [["solo"]]


# ---- árbol de prueba (verificable a mano con el dibujo de recorridos.md) ----
def test_conteo():
    raiz = construir_arbol_prueba()
    assert total_entregas(raiz) == 64
    assert total_entregas(buscar(raiz, "Facultad de Ingeniería")) == 34
    assert total_entregas(buscar(raiz, "Ingeniería de Software")) == 21
    assert total_entregas(buscar(raiz, "Facultad de Medicina")) == 23
    assert total_entregas(buscar(raiz, "Facultad de Derecho")) == 4


def test_profundidad_y_ruta():
    raiz = construir_arbol_prueba()
    assert profundidad_maxima(raiz) == 3
    assert ruta_mas_profunda(raiz) == [
        "Universidad Cooperativa de Colombia", "Facultad de Ingeniería",
        "Ingeniería de Software", "Estructuras de Datos"]
    assert profundidad_maxima(buscar(raiz, "Facultad de Derecho")) == 2


def test_listado_por_niveles():
    assert listado_por_niveles(construir_arbol_prueba()) == [
        ["Universidad Cooperativa de Colombia"],
        ["Facultad de Ingeniería", "Facultad de Medicina",
         "Facultad de Derecho", "Facultad de Odontología"],
        ["Ingeniería de Software", "Ingeniería Mecánica", "Ingeniería Civil",
         "Medicina", "Enfermería", "Psicología", "Derecho", "Odontología"],
        ["Estructuras de Datos", "Física", "Termodinámica", "Estática", "Anatomía",
         "Fundamentos de Enfermería", "Psicología General",
         "Derecho Constitucional", "Anatomía Dental"],
    ]


# ---- parte D ----
def test_cola_equivale_a_niveles_aplanados():
    raiz = construir_arbol_prueba()
    aplanado = [n for nivel in listado_por_niveles(raiz) for n in nivel]
    assert recorrido_con_cola(raiz) == aplanado


def test_pila_da_un_orden_distinto_pero_visita_lo_mismo():
    raiz = construir_arbol_prueba()
    con_cola, con_pila = recorrido_con_cola(raiz), recorrido_con_pila(raiz)
    assert con_pila != con_cola
    assert sorted(con_pila) == sorted(con_cola)
    assert con_pila[:4] == [
        "Universidad Cooperativa de Colombia", "Facultad de Odontología",
        "Odontología", "Anatomía Dental"]