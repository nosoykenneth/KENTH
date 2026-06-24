"""Regresiones de los fixes pedagogicos del tutor (skill pedagogical-rag-tutor).

Deterministas y sin Ollama/Chroma. Cubren:
  - FIX A: la leccion activa (delegated_to_tutor / conceptos) puede anular el
    bloqueo de dominio del supervisor (concepts.md, reglas 3-4).
  - FIX C: "no entiendo <concepto del curso>" no se marca como estudiante perdido.
  - FIX D: el objetivo/accion de la leccion no se inyecta dos veces.
  - FIX E: las compuertas de bloqueo exponen blocked_by.
  - FIX G: verificacion post-generacion de attribution_constraints (regla 10):
    capa determinista (datos en el Domain Pack) que detecta y repara suave la
    violacion + gap semantico observable + capa LLM opcional (flag) mockeada.

Correr: python -m pytest tests/test_tutor_pedagogical_fixes.py -q
"""

import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.agent import routing
from services.agent.verification import verificar_attribution_constraints
from services.context_service import render_context_block
from models.context import ActivityContext, TutorContextEnvelope


class _FakeLLM:
    """Stub determinista: el supervisor no debe tocar Ollama en estos tests."""

    def __init__(self, reply):
        self._reply = reply

    def invoke(self, _prompt):
        return SimpleNamespace(content=self._reply)


def _env(lesson=None, block=None):
    return SimpleNamespace(active_lesson=lesson, active_block=block)


# --------------------------------------------------------------------------
# FIX C — estudiante perdido
# --------------------------------------------------------------------------

def test_perdido_senal_fuerte_sigue_disparando():
    assert routing._es_estudiante_perdido("me rindo, esto es imposible") is True
    assert routing._es_estudiante_perdido("explicame desde cero") is True


def test_perdido_no_dispara_con_concepto_del_curso():
    # Precondicion: "compresion" es un termino tecnico del curso.
    assert routing._tiene_termino_tecnico_curso("no entiendo la compresion")
    assert routing._es_estudiante_perdido("no entiendo la compresion") is False


def test_perdido_si_dispara_sin_concepto():
    assert routing._es_estudiante_perdido("no entiendo nada de esto") is True


# --------------------------------------------------------------------------
# FIX A — delegacion y cobertura de la leccion (helpers puros)
# --------------------------------------------------------------------------

def test_delegacion_detecta_solapamiento():
    lesson = {"delegated_to_tutor": ["si el alumno menciona examenes, dale animo"]}
    assert routing._pregunta_delegada_a_tutor("tengo examenes y estoy agobiado", lesson)


def test_delegacion_vacia_sin_solapamiento():
    lesson = {"delegated_to_tutor": ["dar animo cuando hay examenes"]}
    assert routing._pregunta_delegada_a_tutor("quien gano el mundial", lesson) == ""


def test_cobertura_por_leccion_con_titulo_generico():
    # Titulo generico ("Clase 3") pero conceptos del dominio => sigue en dominio.
    lesson = {"title": "Clase 3", "learning_goals": ["repaso de fisica ondulatoria"]}
    assert routing._pregunta_cubierta_por_leccion("dudas de fisica ondulatoria", lesson, None) is True


def test_cobertura_falsa_si_no_relacionado():
    lesson = {"title": "Clase 3", "learning_goals": ["fisica ondulatoria"]}
    assert routing._pregunta_cubierta_por_leccion("quien gano el mundial", lesson, None) is False


# --------------------------------------------------------------------------
# FIX A + E — supervisor (determinista, LLM stubbeado)
# --------------------------------------------------------------------------

def test_supervisor_bloquea_fuera_dominio_con_motivo(monkeypatch):
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("bloqueo"))
    out = routing.nodo_supervisor({"pregunta": "quien es napoleon", "tutor_envelope": _env()})
    assert out["ruta"] == "bloqueo"
    assert out.get("blocked_by")  # la compuerta explica por que bloqueo


def test_supervisor_delegacion_anula_bloqueo(monkeypatch):
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("bloqueo"))
    lesson = {"delegated_to_tutor": ["si el alumno menciona examenes, dale animo"]}
    out = routing.nodo_supervisor({
        "pregunta": "tengo examenes manana y estoy agobiado",
        "tutor_envelope": _env(lesson=lesson),
    })
    assert out["ruta"] == "teoria"
    assert "lesson_delegation_override" in (out.get("applied_policies") or [])


def test_supervisor_cobertura_leccion_anula_bloqueo(monkeypatch):
    monkeypatch.setattr(routing, "llm_logico", _FakeLLM("bloqueo"))
    lesson = {"title": "Clase 3", "learning_goals": ["repaso de fisica ondulatoria"]}
    out = routing.nodo_supervisor({
        "pregunta": "tengo dudas de fisica ondulatoria",
        "tutor_envelope": _env(lesson=lesson),
    })
    assert out["ruta"] == "teoria"
    assert "lesson_domain_override" in (out.get("applied_policies") or [])


# --------------------------------------------------------------------------
# FIX D — sin doble inyeccion de objetivo/accion
# --------------------------------------------------------------------------

def test_render_no_duplica_objetivo_cuando_coincide():
    ctx = ActivityContext(
        current_lesson_id="L1",
        learning_goal="Dominar la compresion paralela",
        expected_action="Practica con un bus",
    )
    env = TutorContextEnvelope(
        question="x",
        activity_context=ctx,
        active_lesson={
            "lesson_id": "L1",
            "lesson_title": "T",
            "learning_goal": "Dominar la compresion paralela",
            "expected_action": "Practica con un bus",
        },
    )
    out = render_context_block(env)
    assert out.count("Dominar la compresion paralela") == 1
    assert "Objetivo de aprendizaje:" not in out
    assert out.count("Practica con un bus") == 1


def test_render_inyecta_objetivo_distinto_de_ctx():
    ctx = ActivityContext(current_lesson_id="L1", learning_goal="Objetivo runtime distinto")
    env = TutorContextEnvelope(
        question="x",
        activity_context=ctx,
        active_lesson={"lesson_id": "L1", "learning_goal": "Objetivo de la leccion"},
    )
    out = render_context_block(env)
    assert "Objetivo de la leccion: Objetivo de la leccion" in out
    assert "Objetivo de aprendizaje: Objetivo runtime distinto" in out


# --------------------------------------------------------------------------
# FIX G — verificacion post-generacion de attribution_constraints
# --------------------------------------------------------------------------
# Capa determinista: detectores como DATOS en el Domain Pack. Accion elegida:
# observar (applied_policies + warnings) + reparar suave el fragmento infractor.
# Sin Ollama: la capa LLM esta apagada por defecto (ATTR_LLM_JUDGE != "1").

def _codes(warnings):
    return [w["code"] for w in warnings]


def test_g_promesa_se_repara_y_registra_politica():
    respuesta = "Con esto siempre vas a lograr una mezcla profesional y te garantizo el resultado."
    out, policies, warnings = verificar_attribution_constraints(
        respuesta, ["No prometas resultados garantizados"], course_id="2"
    )
    assert "attribution_no_promise" in policies
    assert "ATTRIBUTION_NO_PROMISE" in _codes(warnings)
    # reparacion suave: el lenguaje de promesa fue neutralizado
    low = out.lower()
    assert "siempre vas a lograr" not in low
    assert "te garantizo" not in low


def test_g_receta_universal_se_relativiza():
    out, policies, warnings = verificar_attribution_constraints(
        "La formula es simple: siempre debes comprimir a 4:1.",
        ["No des una receta universal"], course_id="2"
    )
    assert "attribution_no_universal_recipe" in policies
    assert "siempre debes" not in out.lower()
    assert "la formula es" not in out.lower()


def test_g_respuesta_limpia_no_genera_politica():
    out, policies, warnings = verificar_attribution_constraints(
        "Depende del contexto; podrias probar distintos ajustes segun la cancion.",
        ["No prometas resultados"], course_id="2"
    )
    assert policies == []
    assert _codes(warnings) == []
    assert out  # texto intacto


def test_g_negacion_no_es_falso_positivo():
    # "No puedo garantizarte" CUMPLE la restriccion: no debe marcarse violacion.
    out, policies, warnings = verificar_attribution_constraints(
        "No puedo garantizarte un resultado; depende de tu criterio.",
        ["No prometas resultados"], course_id="2"
    )
    assert policies == []
    assert "ATTRIBUTION_NO_PROMISE" not in _codes(warnings)


def test_g_sin_constraints_es_noop():
    texto = "cualquier respuesta del tutor"
    out, policies, warnings = verificar_attribution_constraints(texto, [], course_id="2")
    assert (out, policies, warnings) == (texto, [], [])


def test_g_constraint_semantica_es_observable_con_juez_apagado():
    # Una restriccion que ninguna regla determinista cubre (atribucion al autor)
    # no se finge cumplida: se declara como gap observable.
    out, policies, warnings = verificar_attribution_constraints(
        "X es asi.", ["Atribuye siempre al criterio del autor"], course_id="2"
    )
    assert "ATTRIBUTION_UNVERIFIED_SEMANTIC" in _codes(warnings)
    assert policies == []


def test_g_juez_no_se_invoca_con_flag_apagado(monkeypatch):
    monkeypatch.delenv("ATTR_LLM_JUDGE", raising=False)

    def juez_que_explota(_resp, _cons):
        raise AssertionError("el juez LLM no debe invocarse con el flag apagado")

    # No debe lanzar: el juez nunca se llama.
    out, policies, warnings = verificar_attribution_constraints(
        "X es asi.", ["Atribuye al criterio del autor"], course_id="2", judge=juez_que_explota
    )
    assert "ATTRIBUTION_UNVERIFIED_SEMANTIC" in _codes(warnings)


def test_g_juez_on_observa_y_repara(monkeypatch):
    monkeypatch.setenv("ATTR_LLM_JUDGE", "1")

    def fake_judge(_resp, _cons):
        return {"violaciones": ["no atribuye al autor"],
                "respuesta_corregida": "Segun el criterio del autor, X."}

    out, policies, warnings = verificar_attribution_constraints(
        "X es asi.", ["Atribuye al criterio del autor"], course_id="2", judge=fake_judge
    )
    assert "attribution_llm_violation" in policies
    assert "ATTRIBUTION_LLM_VIOLATION" in _codes(warnings)
    assert out == "Segun el criterio del autor, X."


def test_g_es_agnostico_al_curso_via_default_pack():
    # Un curso sin pack propio cae a _default, que tambien trae los detectores
    # genericos de conducta => la verificacion no depende del dominio de mezcla.
    out, policies, warnings = verificar_attribution_constraints(
        "Te garantizo resultados garantizados.",
        ["No prometas resultados"], course_id="curso_inexistente_999"
    )
    assert "attribution_no_promise" in policies


# --------------------------------------------------------------------------
# FIX D (live) — la delegacion vence la compuerta de "sin evidencia"
# --------------------------------------------------------------------------
# Sintoma reportado en el e2e: una pregunta que la leccion delego al tutor
# (delegated_to_tutor) pero que NO recupera evidencia RAG caia en la respuesta
# generica "no veo una fuente relevante". Causa raiz: la compuerta `if not
# evidencias` corria ANTES de calcular item_delegado. Estos tests fijan el
# ordenamiento: la delegacion se evalua primero y responde como adaptacion
# operativa. Deterministas: retrieval y LLM mockeados (sin Chroma/Ollama).

def _state_delegado(pregunta, delegados, course_id="2"):
    return {
        "pregunta": pregunta,
        "tutor_envelope": _env(lesson={"lesson_id": "L1", "delegated_to_tutor": delegados}),
        "course_id": course_id,
    }


def test_delegacion_sin_evidencia_responde_como_adaptacion(monkeypatch):
    from services.agent import graph

    monkeypatch.setattr(graph, "_preparar_retrieval", lambda s: ("como hago esto en fl studio", False, ""))
    monkeypatch.setattr(graph, "_es_pregunta_lookup", lambda _p: False)
    monkeypatch.setattr(graph, "_buscar_evidencia", lambda *a, **k: [])
    monkeypatch.setattr(graph, "llm_logico", _FakeLLM("Como orientacion del tutor en FL Studio, puedes mapear el paso asi."))

    out = graph.nodo_rag(_state_delegado(
        "como hago esto en FL Studio",
        ["si el alumno pregunta por FL Studio, orientalo como adaptacion"],
    ))

    # No degrada: responde con la adaptacion operativa, no con "sin fuente".
    assert out["evidence_level"] == "delegado"
    assert out["answer_type"] == "delegated_adaptation"
    assert "lesson_delegation_no_evidence" in (out.get("applied_policies") or [])
    assert "no veo una fuente relevante" not in out["respuesta_final"].lower()
    assert "FL Studio" in out["respuesta_final"]


def test_sin_evidencia_y_sin_delegacion_sigue_pidiendo_fuente(monkeypatch):
    from services.agent import graph

    monkeypatch.setattr(graph, "_preparar_retrieval", lambda s: ("como hago esto", False, ""))
    monkeypatch.setattr(graph, "_es_pregunta_lookup", lambda _p: False)
    monkeypatch.setattr(graph, "_buscar_evidencia", lambda *a, **k: [])

    class _LLMQueExplota:
        def invoke(self, _prompt):
            raise AssertionError("el LLM no debe invocarse sin evidencia ni delegacion")

    monkeypatch.setattr(graph, "llm_logico", _LLMQueExplota())

    out = graph.nodo_rag(_state_delegado("como hago esto en herramienta_x", []))

    assert out["evidence_level"] == "bajo"
    assert out["answer_type"] == "needs_more_context"
    assert "lesson_delegation_no_evidence" not in (out.get("applied_policies") or [])
