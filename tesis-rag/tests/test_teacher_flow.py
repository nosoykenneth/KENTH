"""Flujo docente RAG (teacher-driven). Fases 3, 4, 5 y 6.

Fija el contrato del flujo por el que el PROFESOR alimenta el RAG desde la interfaz
(sin Markdown/YAML):

- Fase 3: la transcripción CRUDA de Whisper no se indexa hasta que se aprueba
  (feature flag INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL). approved/edited sí indexan.
- Fase 4: separación comportamiento (inyectado) vs conocimiento (indexado): el
  teacher_approved_context NO contiene tono/nivel/reglas/must_not_do/prompts.
- Fase 5: build_teacher_approved_context_document materializa el perfil aprobado.
- Fase 6: publish borra chunks previos de la misma lección/source y reindexa solo
  esa fuente (sin rebuild global), devolviendo estado.
"""
import os
import sqlite3
import sys
from contextlib import contextmanager
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from services import db_service, pedagogy_profile, teacher_context, transcription_service
from scripts import teacher_flow_section0 as driver


def _reset_sqlite(monkeypatch):
    monkeypatch.setenv("TESISAI_FORCE_SQLITE", "1")
    monkeypatch.setenv("TESISAI_ALLOW_SQLITE_FALLBACK", "1")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    @contextmanager
    def fake_connection():
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    monkeypatch.setattr(db_service, "get_connection", fake_connection)
    db_service._INITIALIZED = False
    db_service._BACKEND = None


def _seed_full_profile(lesson_id="SEC2-R55", course_id="2", section="2"):
    """Lección con perfil pedagógico COMPLETO (comportamiento + conocimiento)."""
    db_service.upsert_lesson(lesson_id=lesson_id, course_id=course_id,
                             moodle_section_id=section, title="Mezclar es decidir: el ciclo")
    pedagogy_profile.apply_profile(lesson_id, course_id, "teacher", {
        "learning_goal": "Adoptar el ciclo de decisión al mezclar",
        "lesson_summary": "Escuchar, diagnosticar, decidir, actuar y verificar.",
        "key_concepts": ["diagnóstico", "verificación con volumen igualado"],
        "common_mistakes": ["Confundir movimiento con progreso"],
        "probable_questions": ["¿Qué es un diagnóstico?"],
        # --- comportamiento (NO debe materializarse como evidencia) ---
        "tutor_tone": "socratico",
        "help_level": "orientar",
        "lesson_rules": ["Guiar con preguntas, no dar recetas"],
        "tutor_must_not_do": ["No revelar la respuesta del ejercicio"],
        "proactive_message": "Bienvenido; empecemos por escuchar.",
        "suggested_prompts": ["¿Por dónde empiezo?"],
        "moments": [
            {"start_time": 0, "end_time": 60, "title": "Mezclar es decidir",
             "summary": "La mezcla mejora por buenas decisiones.",
             "pedagogical_intent": "Instalar la idea rectora"},
        ],
    }, mode="replace", apply_moments=True)


# ==========================================
# FASE 5 — build_teacher_approved_context_document
# ==========================================

def test_build_materializa_solo_conocimiento(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_full_profile()
    doc = teacher_context.build_teacher_approved_context_document("SEC2-R55", "2")
    assert doc is not None and doc["has_content"] is True
    text = doc["text"]
    # Conocimiento SÍ presente:
    assert "Objetivo de aprendizaje" in text
    assert "Adoptar el ciclo de decisión al mezclar" in text
    assert "Conceptos clave" in text and "diagnóstico" in text
    assert "Errores comunes" in text and "Confundir movimiento con progreso" in text
    assert "Preguntas probables" in text and "¿Qué es un diagnóstico?" in text
    assert "Momentos de la clase" in text and "Mezclar es decidir" in text


def test_build_excluye_comportamiento(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_full_profile()
    text = teacher_context.build_teacher_approved_context_document("SEC2-R55", "2")["text"].lower()
    # Comportamiento / directrices privadas NO deben materializarse como evidencia:
    assert "socratico" not in text
    assert "no revelar la respuesta" not in text
    assert "guiar con preguntas" not in text
    assert "orientar" not in text
    # Mensajes al alumno tampoco son evidencia:
    assert "bienvenido; empecemos" not in text
    assert "¿por dónde empiezo?" not in text
    # Sin IDs técnicos visibles (block_id):
    assert "-b1" not in text and "block_id" not in text


def test_build_metadata_contrato(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_full_profile()
    md = teacher_context.build_teacher_approved_context_document("SEC2-R55", "2")["metadata"]
    assert md["source_type"] == "teacher_approved_context"
    assert md["source"] == "authoring_profile"
    assert md["visible_to_student"] is True
    assert md["allowed_for_indexing"] is True
    assert md["internal_context"] is False
    assert md["generated_from"] == "ai_prepare_acceptance"
    assert md["status"] == "teacher_approved"
    assert md["corpus_version"] == "teacher_flow_v1"
    assert md["lesson_id"] == "SEC2-R55"
    assert md["moodle_section_id"] == "2"
    assert md["lesson_title"] and md["lesson_title"] != "SEC2-R55"  # humano, no id
    assert md["source_hash"]


def test_build_sin_perfil_no_tiene_contenido(monkeypatch):
    _reset_sqlite(monkeypatch)
    db_service.upsert_lesson(lesson_id="SEC2-R56", course_id="2", moodle_section_id="2", title="Tu oído miente")
    doc = teacher_context.build_teacher_approved_context_document("SEC2-R56", "2")
    assert doc is not None and doc["has_content"] is False and doc["chunks"] == []


def test_build_leccion_inexistente_devuelve_none(monkeypatch):
    _reset_sqlite(monkeypatch)
    assert teacher_context.build_teacher_approved_context_document("NOPE", "2") is None


# ==========================================
# FASE 6 — publish (índice incremental, sin rebuild global)
# ==========================================

class _FakeIngest:
    """Registra las llamadas de indexación sin tocar embeddings/Chroma."""
    def __init__(self):
        self.indexed = []
        self.deleted = []

    def index_teacher_approved_context(self, course_id, lesson_id, chunks, **kw):
        self.indexed.append({"course_id": course_id, "lesson_id": lesson_id,
                             "chunks": list(chunks), **kw})
        return {"success": True, "chunks": len(chunks), "source_path": f"teacher_context:{lesson_id}"}

    def delete_teacher_approved_context(self, lesson_id):
        self.deleted.append(lesson_id)
        return {"success": True}


def test_publish_indexa_incremental_y_devuelve_estado(monkeypatch):
    _reset_sqlite(monkeypatch)
    _seed_full_profile()
    db_service.merge_lesson_metadata("SEC2-R55", "2", {"transcript_status": "approved"})
    fake = _FakeIngest()
    monkeypatch.setitem(sys.modules, "ingest", fake)

    res = teacher_context.publish_lesson_teacher_context("SEC2-R55", "2", "teacher")
    assert res["ok"] is True and res["tutor_updated"] is True
    assert res["index_status"] == "indexed"
    assert res["requires_reindex"] is False
    assert res["transcript_status"] == "approved"
    assert res["source_type"] == "teacher_approved_context"
    assert res["indexed_at"]
    # Se indexó exactamente esta lección (una sola fuente, incremental).
    assert len(fake.indexed) == 1 and fake.indexed[0]["lesson_id"] == "SEC2-R55"
    assert fake.indexed[0]["chunks"]  # hubo contenido


def test_publish_sin_contenido_limpia_indice(monkeypatch):
    _reset_sqlite(monkeypatch)
    db_service.upsert_lesson(lesson_id="SEC2-R56", course_id="2", moodle_section_id="2", title="Tu oído miente")
    fake = _FakeIngest()
    monkeypatch.setitem(sys.modules, "ingest", fake)
    res = teacher_context.publish_lesson_teacher_context("SEC2-R56", "2", "teacher")
    # Sin perfil aprobado: no se indexa nada, se limpia cualquier chunk previo.
    assert fake.indexed == [] and fake.deleted == ["SEC2-R56"]


# ==========================================
# FASE 3 — la transcripción cruda de Whisper no se indexa hasta aprobar
# ==========================================

class _FakeWhisperModel:
    def transcribe(self, *a, **k):
        info = SimpleNamespace(duration=60.0)
        seg = SimpleNamespace(text="hola", start=0.0, end=2.0, words=[])
        return iter([seg]), info


def _run_whisper(monkeypatch, flag_value):
    _reset_sqlite(monkeypatch)
    db_service.upsert_lesson(lesson_id="SEC2-R55", course_id="2", moodle_section_id="2", title="L")
    monkeypatch.setattr(config, "INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL", flag_value)
    monkeypatch.setattr(transcription_service, "_load_model", lambda: _FakeWhisperModel())
    calls = []
    fake = SimpleNamespace(index_lesson_transcript=lambda *a, **k: calls.append(a))
    monkeypatch.setitem(sys.modules, "ingest", fake)
    transcription_service._run("SEC2-R55", "video.mp4", "es", course_id="2", moodle_section_id="2")
    lesson = db_service.get_lesson("SEC2-R55", "2")
    return calls, (lesson.get("metadata") or {}).get("transcript_status")


def test_whisper_crudo_no_indexa_con_flag_on(monkeypatch):
    calls, status = _run_whisper(monkeypatch, True)
    assert calls == []  # NO se indexó la transcripción cruda
    assert status == config.TRANSCRIPT_STATUS_PENDING


def test_whisper_indexa_con_flag_off(monkeypatch):
    calls, status = _run_whisper(monkeypatch, False)
    assert len(calls) == 1  # con flag off (dev/test) sí indexa de inmediato
    assert status == config.TRANSCRIPT_STATUS_EDITED


def test_config_transcript_is_approved():
    assert config.transcript_is_approved("approved") is True
    assert config.transcript_is_approved("edited") is True
    assert config.transcript_is_approved("generated_pending_review") is False
    assert config.transcript_is_approved("") is False


# ==========================================
# Driver Sección 0 — parser de transcripción VTT (preserva timestamps)
# ==========================================

def test_parser_ts_to_seconds():
    assert driver._ts_to_seconds("00:06.977") == 6.977
    assert driver._ts_to_seconds("01:05.236") == 65.236
    assert driver._ts_to_seconds("1:02:03.500") == 3723.5


def test_parser_transcript_real():
    path = os.path.join(driver.TRANSCRIPT_DIR, "leccion_0_1_transcripcion.txt")
    segs = driver.parse_transcript_file(path)
    assert len(segs) > 50
    assert segs[0]["start_time"] == 0.0
    assert segs[0]["seq"] == 0
    assert "mezclar" in segs[0]["text"].lower() or "bienvenidos" in segs[0]["text"].lower()
    # timestamps monótonos crecientes y texto no vacío
    for s in segs:
        assert s["text"].strip()
        assert s["end_time"] >= s["start_time"]


def test_seccion0_manifest_mapea_1a1():
    nums = [s["num"] for s in driver.SECTION0]
    assert nums == ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7"]
    # lesson_id SEC2-R{cmid}, cmid = 54 + índice; sin duplicados
    ids = [s["lesson_id"] for s in driver.SECTION0]
    assert ids == [f"SEC2-R{54 + i}" for i in range(1, 8)]
    assert len(set(ids)) == 7
    # 0.5 es Gain Staging y 0.6 es Nativos (no cruzados)
    by_num = {s["num"]: s for s in driver.SECTION0}
    assert "Gain Staging" in by_num["0.5"]["title"]
    assert "Nativos" in by_num["0.6"]["title"]
