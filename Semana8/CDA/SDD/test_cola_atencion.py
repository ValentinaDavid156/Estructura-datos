"""Pruebas del dominio CDA (Fase 1, T01.24 - T01.28).

Cubre los casos extremos del Principio 3 de la constitución y RF1-RF11.
"""
from datetime import datetime, timedelta

import pytest

from cola import (
    ColaAtencion,
    ColaVaciaError,
    CampoObligatorioError,
    PrioridadInvalidaError,
    TipoInvalidoError,
    TransicionInvalidaError,
    TurnoNoEncontradoError,
)

@pytest.fixture
def cola():
    return ColaAtencion()


def reg(cola, nombre="Ana", prioridad=3, tipo="PACIENTE", motivo="dolor"):
    return cola.registrar(tipo, nombre, motivo, prioridad, "3001112233")


# ---------- T01.24: registro válido e inválido (RF1, RF2, RF10) ----------

def test_registro_valido_queda_en_espera(cola):
    t = reg(cola, prioridad=2)
    assert t.estado == "EN_ESPERA"
    assert t.id is not None
    assert isinstance(t.hora_registro, datetime)


def test_ids_unicos(cola):
    assert reg(cola, "A").id != reg(cola, "B").id


@pytest.mark.parametrize("prioridad", [0, 6, -1, 99])
def test_prioridad_fuera_de_rango(cola, prioridad):
    with pytest.raises(PrioridadInvalidaError):
        reg(cola, prioridad=prioridad)


def test_tipo_invalido(cola):
    with pytest.raises(TipoInvalidoError):
        reg(cola, tipo="ROBOT")


@pytest.mark.parametrize("campo", ["nombre", "motivo", "prioridad"])
def test_campos_obligatorios_vacios(cola, campo):
    datos = dict(tipo="PACIENTE", nombre="Ana", motivo="dolor", prioridad=3)
    datos[campo] = "" if campo != "prioridad" else None
    with pytest.raises(CampoObligatorioError):
        cola.registrar(datos["tipo"], datos["nombre"], datos["motivo"],
                       datos["prioridad"], "300")


# ---------- T01.25: orden por prioridad y desempate FIFO (Principios 1 y 2) ----------

def test_orden_por_prioridad(cola):
    reg(cola, "normal", 4)
    reg(cola, "critico", 1)
    reg(cola, "urgente", 3)
    assert [t.nombre for t in cola.mostrar_cola()] == ["critico", "urgente", "normal"]


def test_empate_es_fifo(cola):
    reg(cola, "primero", 3)
    reg(cola, "segundo", 3)
    reg(cola, "tercero", 3)
    assert cola.atender_siguiente().nombre == "primero"
    assert cola.atender_siguiente().nombre == "segundo"
    assert cola.atender_siguiente().nombre == "tercero"


def test_llegada_tardia_con_mayor_prioridad_pasa_adelante(cola):
    reg(cola, "viejo", 5)
    reg(cola, "nuevo", 1)
    assert cola.consultar_siguiente().nombre == "nuevo"


# ---------- Principio 4: una sola cola, el tipo no ordena ----------

def test_tipo_no_afecta_el_orden(cola):
    reg(cola, "paciente", 3, tipo="PACIENTE")
    reg(cola, "ambulancia", 3, tipo="VEHICULO")
    assert [t.nombre for t in cola.mostrar_cola()] == ["paciente", "ambulancia"]


def test_vehiculo_prioridad_mayor_atiende_primero(cola):
    reg(cola, "paciente", 4, tipo="PACIENTE")
    reg(cola, "ambulancia", 2, tipo="VEHICULO")
    sig = cola.atender_siguiente()
    assert sig.nombre == "ambulancia" and sig.tipo == "VEHICULO"


# ---------- Principio 3: casos extremos ----------

def test_cola_vacia_consultar_y_atender(cola):
    with pytest.raises(ColaVaciaError):
        cola.consultar_siguiente()
    with pytest.raises(ColaVaciaError):
        cola.atender_siguiente()


def test_cola_vacia_retirar(cola):
    with pytest.raises(TurnoNoEncontradoError):
        cola.retirar(1)


def test_cola_de_un_solo_turno(cola):
    t = reg(cola, "unico", 2)
    assert cola.consultar_siguiente() is t
    assert cola.atender_siguiente() is t
    assert cola.mostrar_cola() == []
    with pytest.raises(ColaVaciaError):
        cola.atender_siguiente()


def test_retirar_el_del_frente(cola):
    a, b, c = reg(cola, "a", 1), reg(cola, "b", 2), reg(cola, "c", 3)
    cola.retirar(a.id)
    assert [t.nombre for t in cola.mostrar_cola()] == ["b", "c"]
    assert cola.consultar_siguiente() is b


def test_retirar_el_del_final(cola):
    a, b, c = reg(cola, "a", 1), reg(cola, "b", 2), reg(cola, "c", 3)
    cola.retirar(c.id)
    assert [t.nombre for t in cola.mostrar_cola()] == ["a", "b"]


def test_retirar_el_del_medio(cola):
    a, b, c = reg(cola, "a", 1), reg(cola, "b", 2), reg(cola, "c", 3)
    cola.retirar(b.id)
    assert [t.nombre for t in cola.mostrar_cola()] == ["a", "c"]
    assert cola.atender_siguiente() is a
    assert cola.atender_siguiente() is c


# ---------- T01.26: máquina de estados (Principio 7, RF9) ----------

def test_flujo_completo_valido(cola):
    t = reg(cola)
    assert cola.atender_siguiente().estado == "EN_ATENCION"
    assert cola.finalizar_atencion(t.id).estado == "ATENDIDO"


def test_retirar_en_espera_es_valido(cola):
    t = reg(cola)
    assert cola.retirar(t.id).estado == "RETIRADO"


def test_finalizar_desde_en_espera_es_invalido(cola):
    t = reg(cola)
    with pytest.raises(TransicionInvalidaError):
        cola.finalizar_atencion(t.id)


def test_retirar_desde_en_atencion_es_invalido(cola):
    t = reg(cola)
    cola.atender_siguiente()
    with pytest.raises(TransicionInvalidaError):
        cola.retirar(t.id)


def test_retirar_ya_atendido_es_invalido(cola):
    t = reg(cola)
    cola.atender_siguiente()
    cola.finalizar_atencion(t.id)
    with pytest.raises(TransicionInvalidaError):
        cola.retirar(t.id)


def test_finalizar_dos_veces_es_invalido(cola):
    t = reg(cola)
    cola.atender_siguiente()
    cola.finalizar_atencion(t.id)
    with pytest.raises(TransicionInvalidaError):
        cola.finalizar_atencion(t.id)


def test_retirado_no_puede_atenderse(cola):
    t = reg(cola)
    cola.retirar(t.id)
    with pytest.raises(ColaVaciaError):
        cola.atender_siguiente()
    with pytest.raises(TransicionInvalidaError):
        cola.finalizar_atencion(t.id)


# ---------- T01.27: aceleración de prioridad (RF11, RNF3) ----------

def test_turno_vencido_sube_un_nivel_y_cambia_de_posicion(cola):
    esperando = reg(cola, "esperando", 3)
    reg(cola, "reciente", 2)
    assert cola.mostrar_cola()[0].nombre == "reciente"
    esperando.hora_registro = datetime.now() - timedelta(minutes=45)  # > 40 min
    # P3 vencido sube a P2; empata con 'reciente' pero llegó antes (FIFO)
    assert cola.consultar_siguiente().nombre == "esperando"
    assert esperando.prioridad == 2
    assert esperando.estado == "EN_ESPERA"        # solo cambia prioridad (RNF5)


def test_aceleracion_sube_solo_un_nivel_y_no_salta_a_quien_sigue_mas_urgente(cola):
    viejo = reg(cola, "viejo", 4)
    reg(cola, "urgente", 2)
    viejo.hora_registro = datetime.now() - timedelta(minutes=130)
    assert cola.consultar_siguiente().nombre == "urgente"
    assert viejo.prioridad == 3


def test_turno_no_vencido_no_sube(cola):
    t = reg(cola, "t", 3)
    t.hora_registro = datetime.now() - timedelta(minutes=10)  # < 40 min
    cola.consultar_siguiente()
    assert t.prioridad == 3


def test_prioridad_1_nunca_baja_de_uno(cola):
    t = reg(cola, "critico", 1)
    t.hora_registro = datetime.now() - timedelta(hours=5)
    cola.consultar_siguiente()
    assert t.prioridad == 1


def test_prioridad_5_no_tiene_maximo(cola):
    t = reg(cola, "leve", 5)
    t.hora_registro = datetime.now() - timedelta(hours=10)
    cola.consultar_siguiente()
    assert t.prioridad == 5


def test_aceleracion_ocurre_tambien_en_atender_listar_y_resumen(cola):
    for metodo in ("atender_siguiente", "mostrar_cola", "resumen"):
        c = ColaAtencion()
        t = reg(c, "t", 4)
        reg(c, "otro", 4)
        t.hora_registro = datetime.now() - timedelta(minutes=130)
        getattr(c, metodo)()
        assert t.prioridad < 4, metodo


def test_aceleracion_actualiza_todos_y_reordena_una_vez(cola):
    a = reg(cola, "a", 4)
    b = reg(cola, "b", 3)
    c = reg(cola, "c", 4)
    a.hora_registro = datetime.now() - timedelta(minutes=130)
    c.hora_registro = datetime.now() - timedelta(minutes=130)
    prioridades = [t.prioridad for t in cola.mostrar_cola()]
    assert prioridades == sorted(prioridades)       # lista consistente
    assert b.prioridad == 3 and a.prioridad == 3 and c.prioridad == 3


# ---------- RF3 / RNF5: mirar no es tocar ----------

def test_consultar_siguiente_no_cambia_estado_ni_cola(cola):
    t = reg(cola)
    assert cola.consultar_siguiente() is t
    assert cola.consultar_siguiente() is t
    assert t.estado == "EN_ESPERA"
    assert len(cola.mostrar_cola()) == 1


def test_resumen_y_listado_no_cambian_estados(cola):
    a, b = reg(cola, "a", 1), reg(cola, "b", 2)
    cola.resumen()
    cola.mostrar_cola()
    assert a.estado == b.estado == "EN_ESPERA"


# ---------- T01.28: resumen anónimo (RF7, RNF4) ----------

def test_resumen_cuenta_por_estado(cola):
    a, b, c, d = (reg(cola, n, p) for n, p in
                  [("a", 1), ("b", 2), ("c", 3), ("d", 4)])
    cola.atender_siguiente()                 # a -> EN_ATENCION
    cola.finalizar_atencion(a.id)            # a -> ATENDIDO
    cola.atender_siguiente()                 # b -> EN_ATENCION
    cola.retirar(d.id)                       # d -> RETIRADO
    r = cola.resumen()
    assert r["ATENDIDO"] == 1
    assert r["EN_ATENCION"] == 1
    assert r["EN_ESPERA"] == 1
    assert r["RETIRADO"] == 1


def test_resumen_nunca_expone_datos_personales(cola):
    reg(cola, "Ana Pérez", 1)
    texto = str(cola.resumen())
    assert "Ana" not in texto
    assert "3001112233" not in texto
    assert "dolor" not in texto
    assert all(isinstance(v, int) for v in cola.resumen().values())


# ---------- HU-06: detalle ----------

def test_detalle_por_id_en_cualquier_estado(cola):
    t = reg(cola, "Ana", 2)
    cola.atender_siguiente()
    d = cola.obtener_detalle(t.id)
    assert (d.nombre, d.tipo, d.prioridad, d.estado) == ("Ana", "PACIENTE", 2, "EN_ATENCION")


def test_detalle_id_inexistente(cola):
    with pytest.raises(TurnoNoEncontradoError):
        cola.obtener_detalle(999)


# ---------- RNF6: consistencia de datos ----------

def test_datos_se_conservan_durante_el_ciclo_de_vida(cola):
    t = cola.registrar("VEHICULO", "Ambulancia 7", "trauma", 1, "3009998877")
    cola.atender_siguiente()
    cola.finalizar_atencion(t.id)
    d = cola.obtener_detalle(t.id)
    assert (d.id, d.tipo, d.nombre, d.motivo, d.telefono) == \
           (t.id, "VEHICULO", "Ambulancia 7", "trauma", "3009998877")