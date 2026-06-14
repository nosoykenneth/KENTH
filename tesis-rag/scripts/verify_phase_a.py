"""Verificación de la Fase A del Editor de Lección.

Roundtrip completo sin tocar la API HTTP (misma capa que usan las rutas):
  1. upsert_lesson con TODOS los campos (incluidas las listas nuevas multi-ítem).
  2. prompts + bloques (con modo criterio_operativo) + transcripción.
  3. Reload vía lesson_service.load_lesson: nada se pierde ni se pisa.
  4. metadata_json se preserva con el merge que hace la ruta de autoría.
  5. course_id denormalizado presente en bloques/prompts/transcript.
  6. render_context_block: el prompt contiene todos los campos exigidos.
  7. Limpieza (delete_lesson).

Uso:  python scripts/verify_phase_a.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("TESISAI_ALLOW_SQLITE_FALLBACK", "1")

from models.context import ActivityContext, InteractionMode, TutorContextEnvelope
from services import db_service
from services.context_service import render_context_block
from services.lesson_service import find_block_at_timestamp, load_lesson

COURSE = "2"
LESSON = "TESTFA-L1"

FAILS = []


def check(cond, label):
    print(("  OK   " if cond else "  FAIL ") + label)
    if not cond:
        FAILS.append(label)


def main():
    # --- 1. Lección completa (la ruta /authoring hace exactamente este upsert) ---
    db_service.upsert_lesson(
        lesson_id=LESSON,
        course_id=COURSE,
        moodle_section_id="99",
        title="Lección de prueba Fase A",
        order=7,
        learning_goal="Entender el gain staging antes de mezclar",
        expected_action="Ajustar los faders a -18 dBFS promedio",
        learning_goals=[
            "Identifica el headroom disponible en el master",
            "Calibra cada pista a nivel nominal",
        ],
        resources=[],
        prerequisites=["TESTFA-L0", "E1-L02"],
        delegated_to_tutor=[
            "Resolver dudas de routing del DAW",
            "Repasar el criterio de gain staging con ejemplos propios",
        ],
        attribution_constraints=[
            "Cita siempre el minuto del video al referir la demo",
            "No recomendar plugins de pago",
        ],
        notes="NOTA INTERNA: revisar el ejemplo del minuto 3 antes del piloto",
        metadata={"foo": "bar"},
    )
    db_service.set_lesson_prompts(
        LESSON,
        proactive_message="¿Viste cómo quedó el medidor? Pregúntame si algo no cuadra.",
        suggested_prompts=["¿Qué es headroom?", "¿Por qué -18 dBFS?"],
    )
    db_service.replace_lesson_blocks(LESSON, [
        {
            "block_id": f"{LESSON}-B1",
            "start_time": 0, "end_time": 60,
            "block_title": "Intro al gain staging",
            "summary": "Se muestra el mixer con todas las pistas en 0",
            "interaction_mode": "navegacion_de_recurso",
            "tutor_focus": "Orientar sin adelantar el criterio",
            "concepts": ["gain staging", "headroom"],
            "preguntas_probables": ["¿Por qué bajar los faders?"],
        },
        {
            "block_id": f"{LESSON}-B2",
            "start_time": 60, "end_time": 120,
            "block_title": "Criterio de -18 dBFS",
            "summary": "Se calibra la pista de bombo al nivel nominal",
            "interaction_mode": "criterio_operativo",
            "tutor_focus": "Reforzar el criterio operativo del nivel nominal",
            "concepts": ["dBFS", "nivel nominal"],
            "preguntas_probables": ["¿Sirve para todos los géneros?"],
        },
    ])
    db_service.replace_transcript(LESSON, [
        {"seq": 0, "start_time": 0.0, "end_time": 4.2, "text": "Bienvenidos al gain staging.", "speaker": ""},
        {"seq": 1, "start_time": 4.2, "end_time": 9.8, "text": "Bajemos todos los faders.", "speaker": ""},
    ])

    # --- 2. Reload: nada se pierde ---
    print("\n[roundtrip] load_lesson tras guardar:")
    data = load_lesson(LESSON, COURSE)
    check(data is not None, "la lección existe tras guardar")
    check(data["lesson_title"] == "Lección de prueba Fase A", "titulo")
    check(data["order"] == 7, "orden")
    check(data["prerequisites"] == ["TESTFA-L0", "E1-L02"], "prerequisites")
    check(data["learning_goal"].startswith("Entender"), "learning_goal")
    check(len(data["learning_goals"]) == 2, "learning_goals (criterios de logro, 2 items)")
    check(data["expected_action"].startswith("Ajustar"), "expected_action")
    check(data["delegated_to_tutor"] == [
        "Resolver dudas de routing del DAW",
        "Repasar el criterio de gain staging con ejemplos propios",
    ], "delegated_to_tutor (lista multi-item)")
    check(data["attribution_constraints"] == [
        "Cita siempre el minuto del video al referir la demo",
        "No recomendar plugins de pago",
    ], "attribution_constraints (lista multi-item)")
    check(data["proactive_message"].startswith("¿Viste"), "proactive_message")
    check(data["suggested_prompts"] == ["¿Qué es headroom?", "¿Por qué -18 dBFS?"], "suggested_prompts")
    check(data["notes"].startswith("NOTA INTERNA"), "notes persiste")
    check("expected_actions" not in data and "source_script_file" not in data, "campos deprecados fuera del shape")
    check(len(data["blocks"]) == 2, "2 bloques")
    b2 = data["blocks"][1]
    check(b2["interaction_mode"] == "criterio_operativo", "bloque 2 con modo criterio_operativo")
    check(b2["concepts"] == ["dBFS", "nivel nominal"], "concepts por bloque")
    check(InteractionMode("criterio_operativo") is not None, "criterio_operativo en el enum")

    # --- 3. metadata no se pisa (merge de la ruta de autoría) ---
    row = db_service.get_lesson(LESSON, COURSE)
    merged = {**(row.get("metadata") or {}), "edited_by": "profe-1"}
    db_service.upsert_lesson(
        lesson_id=LESSON, course_id=COURSE, moodle_section_id="99",
        title=row["title"], order=row["order"],
        learning_goal=row["learning_goal"], expected_action=row["expected_action"],
        learning_goals=row["learning_goals"], resources=row["resources"],
        prerequisites=row["prerequisites"],
        delegated_to_tutor=row["delegated_to_tutor"],
        attribution_constraints=row["attribution_constraints"],
        notes=row["notes"], metadata=merged,
    )
    row2 = db_service.get_lesson(LESSON, COURSE)
    print("\n[metadata] tras re-guardar desde el editor:")
    check(row2["metadata"].get("foo") == "bar", "contenido ajeno de metadata_json sobrevive")
    check(row2["metadata"].get("edited_by") == "profe-1", "edited_by presente")

    # --- 4. course_id en tablas hijas ---
    print("\n[course_id] denormalizado en tablas hijas:")
    blocks = db_service.list_lesson_blocks(LESSON)
    check(all(b.get("course_id") == COURSE for b in blocks), "lesson_blocks.course_id = " + COURSE)
    with db_service.get_connection() as conn:
        q = db_service._q()
        prow = db_service._fetchone(
            conn, f"SELECT course_id FROM {db_service.table_name('lesson_prompts')} WHERE lesson_id={q}", (LESSON,))
        trow = db_service._fetchone(
            conn, f"SELECT course_id FROM {db_service.table_name('transcript_segments')} WHERE lesson_id={q}", (LESSON,))
    check(prow and str(prow.get("course_id")) == COURSE, "lesson_prompts.course_id")
    check(trow and str(trow.get("course_id")) == COURSE, "transcript_segments.course_id")

    # --- 5. Prompt renderizado ---
    lesson_data = load_lesson(LESSON, COURSE)
    block = find_block_at_timestamp(lesson_data, 75.0)  # cae en B2
    envelope = TutorContextEnvelope(
        question="¿Por qué -18?",
        activity_context=ActivityContext(current_lesson_id=LESSON, current_timestamp=75.0),
        interaction_mode=InteractionMode.CRITERIO_OPERATIVO,
        active_lesson=lesson_data,
        active_block=block,
    )
    rendered = render_context_block(envelope)
    print("\n[prompt] render_context_block:\n")
    print(rendered)
    print()
    esperados = {
        "learning_goal": "Objetivo de la leccion: Entender el gain staging",
        "learning_goals": "Criterios de logro de la leccion:",
        "prerequisites": "Prerrequisitos de la leccion",
        "expected_action": "Accion esperada de la leccion: Ajustar",
        "delegated_to_tutor": "Delegado al tutor en esta leccion",
        "attribution_constraints": "RESTRICCIONES Y ATRIBUCIONES (OBLIGATORIAS)",
        "proactive_message": "Mensaje proactivo de la leccion:",
        "suggested_prompts": "Prompts sugeridos de la leccion:",
        "bloque activo": "BLOQUE ACTIVO DEL VIDEO",
        "bloque summary": "Que esta pasando en pantalla: Se calibra la pista",
        "bloque modo": "Modo pedagogico del bloque: criterio_operativo",
        "bloque foco": "Foco del tutor en este bloque:",
        "bloque conceptos": "Conceptos del bloque: dBFS, nivel nominal",
        "bloque preguntas": "Preguntas probables del alumno aqui:",
    }
    for label, needle in esperados.items():
        check(needle in rendered, f"prompt contiene {label}")
    check("NOTA INTERNA" not in rendered, "notes NO se inyecta al tutor")

    # --- 6. Limpieza ---
    db_service.delete_lesson(LESSON)
    check(db_service.get_lesson(LESSON, COURSE) is None, "limpieza: lección de prueba eliminada")

    print("\n" + ("TODO OK" if not FAILS else f"FALLARON {len(FAILS)}: {FAILS}"))
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
