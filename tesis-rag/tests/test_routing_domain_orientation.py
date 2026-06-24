"""Regresiones de los fixes H1 (dominio dentro de leccion) y H2 (orientacion).

Sintomas reportados en la leccion SEC2-R55:
  - H1: "quien gano el ultimo mundial" NO se bloqueaba (caia a RAG y filtraba el
    id interno). Causa: el routing decidia dominio sobre pregunta+contexto, y el
    contexto de la leccion (lleno de terminos del curso) hacia pasar cualquier
    pregunta. Fix: la senal de dominio se decide sobre la PREGUNTA; el contexto
    solo rescata continuaciones.
  - H2: "en que leccion estoy" caia a RAG y el modelo narraba el bloque de
    contexto (ids, tiempos, delegados). Fix: ruta deterministica 'ubicacion' ->
    nodo_orientacion responde desde el envelope sin LLM ni internos.

Deterministas, sin Ollama/Chroma. El LLM del supervisor se stubbea con FakeLLM:
para las preguntas fuera de dominio el stub responde 'teoria' a proposito, de
modo que un PASS prueba que el BLOQUEO es deterministico y no depende del LLM.

Correr: python -m pytest tests/test_routing_domain_orientation.py -q
"""

import os
import sys
from types import SimpleNamespace

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent import routing


class _FakeLLM:
    def __init__(self, reply):
        self._reply = reply

    def invoke(self, _prompt):
        return SimpleNamespace(content=self._reply)


def _env(lesson=None, block=None):
    return SimpleNamespace(active_lesson=lesson, active_block=block)


# Contexto de leccion RICO EN TERMINOS DEL CURSO: reproduce la contaminacion que
# causaba el bug (cualquier pregunta "parecia" del dominio por culpa del contexto).
CONTEXTO_DOMINIO = (
    "Leccion de mezcla y masterizacion. El instructor Kenneth corrige problemas de "
    "mezcla real aplicando el ciclo de decision: escuchar, diagnosticar, decidir y "
    "verificar. Se trabaja ecualizacion, compresion, paneo, fase, estereo y el DAW."
)

# Leccion activa de dominio, con metadata que NO menciona los temas ajenos de abajo
# (para que el override por cobertura no los rescate).
LECCION_DOMINIO = {
    "lesson_id": "SEC2-R55",
    "lesson_title": "Ciclo de decision en la mezcla",
    "learning_goal": "Aplicar el ciclo escuchar-diagnosticar-decidir-verificar",
    "suggested_prompts": ["como diagnostico un problema de mezcla"],
}


def _state(pregunta, lesson=LECCION_DOMINIO, contexto=CONTEXTO_DOMINIO, historial=None):
    return {
        "pregunta": pregunta,
        "contexto_leccion": contexto,
        "historial": historial or [],
        "tutor_envelope": _env(lesson=lesson),
    }


# ==========================================================================
# H1 — preguntas FUERA DE DOMINIO dentro de una leccion -> bloqueo
# ==========================================================================
# El FakeLLM responde 'teoria': si el test pasa es porque el bloqueo NO depende
# del LLM (es deterministico, pese al contexto rico en dominio).

FUERA_DE_DOMINIO = [
    "quien gano el ultimo mundial",
    "quien gano el mundial de futbol",
    "recomiendame una buena pelicula de terror",
    "cuentame un chiste",
    "cual es la capital de francia",
    "como preparo una pizza",
    "dame la receta del ceviche",
    "quien es el presidente de ecuador",
    "cuanto cuesta un iphone",
    "traduceme esta frase al ingles",
    "cuando es el proximo feriado",
    "que opinas de bitcoin",
    "como esta el clima hoy",
]


@pytest.mark.parametrize("pregunta", FUERA_DE_DOMINIO)
def test_h1_fuera_de_dominio_se_bloquea_pese_al_contexto(monkeypatch, pregunta):
    # El juez semantico (zona incierta) responde 'no' -> bloqueo. Un PASS prueba
    # que la pregunta llega al juez y se bloquea pese al contexto rico en dominio.
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("no"))
    out = routing.nodo_supervisor(_state(pregunta))
    assert out["ruta"] == "bloqueo", f"deberia bloquear: {pregunta!r} -> {out['ruta']}"
    assert out.get("blocked_by"), f"sin blocked_by: {pregunta!r}"


def test_h1_fuera_de_dominio_tambien_en_modo_general(monkeypatch):
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("no"))
    out = routing.nodo_supervisor({"pregunta": "quien gano el mundial", "tutor_envelope": _env()})
    assert out["ruta"] == "bloqueo"


LECCION_RECETAS = {
    "lesson_id": "SEC2-R55",
    "lesson_title": "La mentira de las recetas",
    "learning_goal": "Entender que mezclar es decidir, no seguir recetas",
}


@pytest.mark.parametrize("pregunta", [
    "entonces los tutoriales de youtube no sirven",
    "las recetas de internet no funcionan",
    "para que tomar el curso si hay videos gratis",
    "los tutoriales de youtube no sirven",
])
def test_h1_tematico_pero_lexico_ajeno_no_se_bloquea(monkeypatch, pregunta):
    # Preguntas del TEMA de la leccion ('la mentira de las recetas') con vocabulario
    # fuera de la metadata. El juez semantico (si lo alcanzan) responde 'si'. Lo que
    # importa: NO se bloquean (lleguen a teoria por cobertura, senal o juez).
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("si, esta relacionada"))
    out = routing.nodo_supervisor(_state(pregunta, lesson=LECCION_RECETAS))
    assert out["ruta"] == "teoria", f"{pregunta!r} -> {out['ruta']}"


def test_h1_juez_semantico_admite_tematico_y_bloquea_ajeno(monkeypatch):
    # Caso que SOLO el juez resuelve (sin cobertura/senal lexica).
    pregunta = "los tutoriales de youtube no sirven"
    assert not routing._pregunta_tiene_senal_dominio_propia(pregunta)
    assert not routing._pregunta_cubierta_por_leccion(pregunta, LECCION_RECETAS, None)

    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("si"))
    out = routing.nodo_supervisor(_state(pregunta, lesson=LECCION_RECETAS))
    assert out["ruta"] == "teoria"
    assert "semantic_domain_override" in (out.get("applied_policies") or [])

    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("no"))
    out = routing.nodo_supervisor(_state(pregunta, lesson=LECCION_RECETAS))
    assert out["ruta"] == "bloqueo"


def test_h1_conector_no_es_loophole_para_ajeno(monkeypatch):
    # 'entonces quien gano el mundial': empezar con conector NO debe dar paso libre.
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("no"))
    out = routing.nodo_supervisor(_state("entonces quien gano el mundial"))
    assert out["ruta"] == "bloqueo"


# ==========================================================================
# H1 — preguntas DE DOMINIO siguen yendo a teoria (sin regresion)
# ==========================================================================

DE_DOMINIO = [
    "que es la compresion paralela",
    "para que sirve la ecualizacion",
    "como funciona el paneo",
    "explicame la masterizacion",
    "que es la mezcla en mono",
    "cuando conviene usar compresion",
]


@pytest.mark.parametrize("pregunta", DE_DOMINIO)
def test_h1_dominio_va_a_teoria(monkeypatch, pregunta):
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("bloqueo"))  # no debe usarse
    assert routing._pregunta_tiene_senal_dominio_propia(pregunta), (
        f"precondicion: {pregunta!r} deberia tener senal de dominio propia"
    )
    out = routing.nodo_supervisor(_state(pregunta))
    assert out["ruta"] == "teoria", f"{pregunta!r} -> {out['ruta']}"


# ==========================================================================
# H1 — continuaciones sin tema propio NO se bloquean (caen al clasificador)
# ==========================================================================
# No tienen senal de dominio propia, pero dependen del contexto. El FakeLLM
# (clasificador) responde 'teoria'; el test exige que NO se bloqueen antes.

CONTINUACIONES = [
    "explicame mejor",
    "dame un ejemplo",
    "y el resto?",
    "puedes darme mas detalle",
    "no me quedo claro, amplia",
    "profundiza en eso",
    "continua",
    "y eso?",
    "puedes ampliar",
]


@pytest.mark.parametrize("pregunta", CONTINUACIONES)
def test_h1_continuacion_va_a_teoria(pregunta):
    # Routing deterministico: una continuacion CONTINUA la leccion (teoria),
    # ya no la decide el LLM (que mandaba 'explicame mejor' a 'perdido').
    out = routing.nodo_supervisor(_state(pregunta))
    assert out["ruta"] == "teoria", f"continuacion debia ir a teoria: {pregunta!r} -> {out['ruta']}"


# Regresion live: un delegado que empieza por 'Como ...' no debe AUTORIZAR una
# pregunta ajena que tambien empieza por 'como' (match por palabra-funcion).
LECCION_DELEGADO_COMO = {
    "lesson_id": "SEC2-R55",
    "lesson_title": "Ciclo de decision en la mezcla",
    "delegated_to_tutor": [
        "Como construir habitos de escucha critica y rutinas de sesion",
        "Traduccion de cualquier paso de la demo al DAW del alumno (FL Studio, Pro Tools)",
    ],
}


@pytest.mark.parametrize("pregunta", [
    "como preparo una pizza",
    "como esta el clima hoy",
    "como llego al estadio",
])
def test_h1_delegado_con_palabra_funcion_no_autoriza_ajena(monkeypatch, pregunta):
    # No hay delegacion lexica real; el juez semantico (zona incierta) dice 'no'.
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("no"))
    assert routing._pregunta_delegada_a_tutor(pregunta, LECCION_DELEGADO_COMO) == ""
    out = routing.nodo_supervisor(_state(pregunta, lesson=LECCION_DELEGADO_COMO))
    assert out["ruta"] == "bloqueo", f"{pregunta!r} -> {out['ruta']}"


def test_h1_delegacion_legitima_sigue_funcionando():
    # Una pregunta que SI toca el tema delegado (contenido real) se autoriza.
    item = routing._pregunta_delegada_a_tutor(
        "como traduzco este paso a fl studio", LECCION_DELEGADO_COMO
    )
    assert "Traduccion" in item


def test_h1_continuacion_es_detectada_como_tal():
    assert routing._es_continuacion_sin_contenido_nuevo("explicame mejor")
    assert routing._es_continuacion_sin_contenido_nuevo("puedes darme mas detalle")
    assert routing._es_continuacion_sin_contenido_nuevo("y el resto?")
    # con sustantivo-tema propio NO es continuacion:
    assert not routing._es_continuacion_sin_contenido_nuevo("quien gano el mundial")
    assert not routing._es_continuacion_sin_contenido_nuevo("recomiendame una pelicula")


# ==========================================================================
# H2 — preguntas de UBICACION -> ruta 'ubicacion'
# ==========================================================================

UBICACION = [
    "en que leccion estoy",
    "en que leccion estoy?",
    "en que leccion estamos",
    "donde estoy",
    "que leccion es esta",
    "que estoy viendo",
    "en que seccion estoy",
    "en que seccion estamos",
    "en que parte del curso estoy",
    "como se llama esta leccion",
    "que leccion estoy viendo",
    "en que modulo estoy",
    # nivel bloque / seccion del bloque (Finding H2 ampliado)
    "en que bloque estamos",
    "en que bloque estoy",
    "que bloque es este",
    "a que seccion pertenece este bloque",
    "a que seccion corresponde este bloque",
]


@pytest.mark.parametrize("pregunta", UBICACION)
def test_h2_ubicacion_enruta_a_orientacion(monkeypatch, pregunta):
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("teoria"))  # no debe usarse
    out = routing.nodo_supervisor(_state(pregunta))
    assert out["ruta"] == "ubicacion", f"{pregunta!r} -> {out['ruta']}"
    assert out["intent"] == "orientacion"


def test_h2_pregunta_tecnica_de_ubicacion_no_es_navegacion():
    # "en que parte de la cadena va el compresor" es tecnica, no navegacion.
    assert routing._es_pregunta_de_ubicacion("en que parte de la cadena va el compresor") is False


@pytest.mark.parametrize("pregunta", [
    "de que trata este bloque",
    "que se ve en este bloque",
    "explicame este bloque",
])
def test_h2_contenido_del_bloque_no_es_navegacion(pregunta):
    # Preguntar el CONTENIDO del bloque no es navegacion: debe seguir a RAG, no
    # al nodo de orientacion (que solo dice 'donde estas').
    assert routing._es_pregunta_de_ubicacion(pregunta) is False


# ==========================================================================
# H2 — nodo_orientacion responde desde el envelope SIN filtrar internos
# ==========================================================================

def test_h2_orientacion_responde_con_titulo_sin_internos():
    from services.agent import graph

    state = {
        "pregunta": "en que leccion estoy",
        "current_section_name": "Seccion 2 - Espacio y fase",
        "tutor_envelope": _env(lesson={
            "lesson_id": "SEC2-R55",
            "lesson_title": "Ciclo de decision en la mezcla",
            "delegated_to_tutor": ["traducir pasos a otros DAWs"],
        }),
    }
    out = graph.nodo_orientacion(state)
    resp = out["respuesta_final"]

    assert "Ciclo de decision en la mezcla" in resp           # usa el titulo legible
    assert "Seccion 2 - Espacio y fase" in resp               # y la seccion
    assert "SEC2-R55" not in resp                             # NO filtra el id interno
    assert "delegated" not in resp.lower()                    # NO filtra delegados
    assert "DAWs" not in resp
    assert out["model_used"] == "none"                        # sin LLM
    assert out["answer_type"] == "orientation"


def test_h2_orientacion_sin_leccion_no_filtra_y_no_inventa():
    from services.agent import graph

    out = graph.nodo_orientacion({"pregunta": "donde estoy", "tutor_envelope": _env()})
    resp = out["respuesta_final"].lower()
    assert "curso" in resp
    assert "sec2" not in resp
    assert out["model_used"] == "none"


def test_h2_detector_resumen_bloque_distingue_de_navegacion():
    assert routing._es_pregunta_sobre_bloque_actual("de que trata este bloque")
    assert routing._es_pregunta_sobre_bloque_actual("que se ve en este bloque")
    # navegacion (donde) y tecnica NO son "resumen del bloque":
    assert not routing._es_pregunta_sobre_bloque_actual("en que bloque estoy")
    assert not routing._es_pregunta_sobre_bloque_actual("que es la compresion en este bloque")


def test_h2_supervisor_resumen_bloque_va_a_teoria_sin_juez(monkeypatch):
    # No debe consultar al juez LLM: es contenido del curso, ruta deterministica.
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("no"))
    out = routing.nodo_supervisor(_state("de que trata este bloque"))
    assert out["ruta"] == "teoria"


def test_h2_rag_resumen_bloque_usa_summary_sin_retrieval(monkeypatch):
    from services.agent import graph

    def _no_retrieval(*a, **k):
        raise AssertionError("no debe hacer retrieval cruzado: ancla al resumen del bloque")

    monkeypatch.setattr(graph, "_buscar_evidencia", _no_retrieval)
    monkeypatch.setattr(graph, "llm_logico", _FakeLLM("Aqui se desmonta la cultura de recetas."))

    state = {
        "pregunta": "de que trata este bloque",
        "tutor_envelope": _env(
            lesson={"lesson_id": "SEC2-R55", "lesson_title": "T"},
            block={
                "block_id": "S0-L01-B1",
                "block_title": "La mentira de las recetas",
                "summary": "Kenneth desmonta la cultura de recetas y plantea que mezclar es decidir.",
                "concepts": ["recetas vs criterio"],
            },
        ),
    }
    out = graph.nodo_rag(state)
    assert out["answer_type"] == "block_summary"
    assert "active_block_summary" in (out.get("applied_policies") or [])
    # no filtra ids internos ni numeros de bloque (el prompt lo prohibe; aqui el
    # FakeLLM no los emite, validamos el contrato de la respuesta):
    assert "S0-L01-B1" not in out["respuesta_final"]


def test_h2_orientacion_con_bloque_reporta_titulo_sin_internos():
    from services.agent import graph

    state = {
        "pregunta": "en que bloque estamos",
        "current_section_name": "Seccion 0: El sistema de decision",
        "tutor_envelope": _env(
            lesson={"lesson_id": "SEC2-R55", "lesson_title": "1 - Mezclar es decidir"},
            block={
                "block_id": "S0-L01-B1",
                "block_title": "La mentira de las recetas",
                "start_time": 0, "end_time": 70,
            },
        ),
    }
    out = graph.nodo_orientacion(state)
    resp = out["respuesta_final"]

    assert "La mentira de las recetas" in resp        # reporta el bloque por titulo
    assert "1 - Mezclar es decidir" in resp           # y la leccion
    # NUNCA filtra ids internos, recurso ni timestamp:
    assert "S0-L01-B1" not in resp
    assert "SEC2-R55" not in resp
    assert "55" not in resp
    assert "70" not in resp
    assert "timestamp" not in resp.lower()
    assert out["model_used"] == "none"
