"""Fase 4 - verificacion de comportamiento contextual del agente.

No llama al LLM ni toca Chroma. Valida los bloques de prompt/politica y el
reparador de incertidumbre usando fuentes dummy con metadata realista.

Uso:
  python scripts/verify_phase4_prompt_behavior.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.context import ActivityContext, TutorContextEnvelope  # noqa: E402
from services.context_service import render_context_block  # noqa: E402
from services.agent.graph import (  # noqa: E402
    _bloque_uso_evidencia,
    _reparar_incertidumbre_recurso_contextual,
    _respuesta_sin_evidencia_contextual,
)


COURSE = "2"
AXIS = "Eje 2"
LESSON = "E2-L01"

_passes = []
_fails = []


def check(name, cond, detail=""):
    (_passes if cond else _fails).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" -> {detail}" if detail and not cond else ""))


def state():
    return {
        "course_id": COURSE,
        "current_axis_id": AXIS,
        "current_lesson_id": LESSON,
    }


def fuente(**overrides):
    data = {
        "index": 1,
        "title": "Another trap",
        "resource_title": "Another trap",
        "description": "Plantilla FL Studio de RnB trap para practicar decisiones de filtros en la leccion.",
        "scope": "lesson",
        "context_relation": "same_lesson",
        "resource_type": "daw_template",
        "media_type": "template",
        "visible_to_student": True,
        "allowed_for_indexing": True,
        "lesson_id": LESSON,
        "axis_id": AXIS,
        "source": "resource:test-doc",
        "score": 1.2,
    }
    data.update(overrides)
    return data


def case_a_template_prompt_and_repair():
    print("\n== A) Another trap como plantilla DAW contextual ==")
    fuentes = [fuente()]
    block, flags = _bloque_uso_evidencia(fuentes, state())
    repaired = _reparar_incertidumbre_recurso_contextual(
        "No hay suficiente contexto o evidencia para responder.",
        "Para que sirve Another trap?",
        fuentes,
        state(),
    )
    norm = repaired.lower()
    check("activa regla de recurso descargable", flags["downloadable_resource_rule"])
    check("activa evidencia contextual suficiente", flags["contextual_resource_sufficient"])
    check("prompt prohibe abrir con falta de contexto", "no abras con" in block.lower(), block)
    check("prompt trata template como plantilla/proyecto DAW", "plantilla/proyecto daw" in block.lower(), block)
    check("respuesta reparada no conserva incertidumbre generica", "no hay suficiente" not in norm, repaired)
    check("respuesta reparada explica plantilla/proyecto DAW", "plantilla/proyecto daw" in norm, repaired)
    check("respuesta reparada no finge leer el .flp", "no interpreto el archivo binario" in norm, repaired)


def case_b_audio_practice():
    print("\n== B) Audio practice no finge escucha ==")
    block, flags = _bloque_uso_evidencia([
        fuente(
            title="Audio corte filtros",
            resource_title="Audio corte filtros",
            description="Audio para comparar cortes HPF y LPF en solo versus mezcla.",
            resource_type="audio_practice",
            media_type="audio",
        )
    ], state())
    check("activa regla descargable/audio", flags["downloadable_resource_rule"])
    check("instruye no fingir escucha", "no finjas que escuchaste el audio" in block.lower(), block)


def case_c_other_axis():
    print("\n== C) Evidencia other_axis marca salto de contexto ==")
    block, flags = _bloque_uso_evidencia([
        fuente(
            title="Compresion paralela",
            resource_title="Compresion paralela",
            description="Material del Eje 4 sobre compresion paralela.",
            resource_type="theory",
            media_type="document",
            context_relation="other_axis",
            scope="axis",
            axis_id="Eje 4",
            lesson_id="",
        )
    ], state())
    check("activa regla salto de contexto", flags["context_jump_rule"])
    check("prompt pide indicar salto de eje", "indica brevemente el salto" in block.lower(), block)


def case_d_hidden_indexed_resource():
    print("\n== D) Recurso oculto indexado no ofrece descarga ==")
    fuentes = [
        fuente(
            title="Rubrica interna",
            resource_title="Rubrica interna",
            description="Criterio interno para evaluar la practica.",
            resource_type="rubric",
            media_type="file",
            visible_to_student=False,
        )
    ]
    block, _ = _bloque_uso_evidencia(fuentes, state())
    repaired = _reparar_incertidumbre_recurso_contextual(
        "No tengo suficiente evidencia.",
        "Que hago con la rubrica?",
        fuentes,
        state(),
    )
    check("prompt prohibe descarga/link", "no ofrezcas descarga ni enlace" in block.lower(), block)
    check("respuesta reparada no ofrece descarga", "descargar" not in repaired.lower(), repaired)


def case_e_missing_resource():
    print("\n== E) Sin fuente relevante usa falta contextual especifica ==")
    resp = _respuesta_sin_evidencia_contextual(state())
    check("menciona leccion actual", LESSON in resp, resp)
    check("no usa frase generica inicial", "no veo una fuente relevante" in resp.lower(), resp)


def case_f_runtime_state_injection():
    print("\n== F) Estado de leccion/bloque se inyecta como runtime ==")
    envelope = TutorContextEnvelope(
        question="Que hago aqui?",
        activity_context=ActivityContext(
            current_axis=AXIS,
            current_lesson_id=LESSON,
            current_timestamp=42.0,
            learning_goal="Aplicar filtros con criterio.",
            expected_action="Comparar solo versus mezcla.",
        ),
        active_lesson={
            "lesson_id": LESSON,
            "axis_id": AXIS,
            "lesson_title": "Filtros HPF/LPF",
            "learning_goal": "Aplicar filtros con criterio.",
            "expected_action": "Comparar solo versus mezcla.",
            "proactive_message": "Recuerda escuchar antes de cortar.",
            "suggested_prompts": ["Cuando corto en solo?", "Cuando corto en mezcla?"],
            "metadata": {"tutor_constraints": "No dar recetas fijas de dB."},
        },
        active_block={
            "block_id": "B1",
            "block_title": "Corte inicial",
            "start_time": 10,
            "end_time": 80,
            "tutor_focus": "Distinguir limpieza de perdida de cuerpo.",
            "interaction_mode": "criterio_operativo",
            "preguntas_probables": ["Estoy quitando demasiado?"],
        },
    )
    rendered = render_context_block(envelope)
    check("inyecta titulo leccion", "Filtros HPF/LPF" in rendered, rendered)
    check("inyecta proactive_message", "Recuerda escuchar antes de cortar" in rendered, rendered)
    check("inyecta suggested_prompts", "Cuando corto en solo?" in rendered, rendered)
    check("inyecta tutor_constraints", "No dar recetas fijas de dB" in rendered, rendered)
    check("inyecta tutor_focus del bloque", "Distinguir limpieza" in rendered, rendered)


def main():
    case_a_template_prompt_and_repair()
    case_b_audio_practice()
    case_c_other_axis()
    case_d_hidden_indexed_resource()
    case_e_missing_resource()
    case_f_runtime_state_injection()
    print(f"\n=== RESULTADO FASE 4 PROMPT: {len(_passes)} PASS, {len(_fails)} FAIL ===")
    if _fails:
        print("Fallaron: " + ", ".join(_fails))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
