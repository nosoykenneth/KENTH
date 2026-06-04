"""
Servicio de transcripcion automatica (faster-whisper, local).

Corre en la misma maquina que Moodle/Ollama: ninguna llamada externa, el audio
no sale del servidor. El motor (faster-whisper) se importa de forma perezosa para
que el backend arranque aunque la dependencia aun no este instalada; en ese caso
el job termina con un error claro.

La transcripcion de un video largo tarda, asi que cada peticion arranca un job en
un hilo en segundo plano. El estado se consulta por leccion y, al terminar, los
segmentos quedan persistidos en BD via db_service.replace_transcript.
"""

from __future__ import annotations

import os
import threading
import time
from typing import Any, Dict, List, Optional

from services import db_service

# Tamano del modelo Whisper. tiny/base/small/medium/large-v3.
# 'small' es un buen balance calidad/velocidad en CPU para espanol.
_MODEL_SIZE = os.getenv("KENTH_WHISPER_MODEL", "small")
_DEVICE = os.getenv("KENTH_WHISPER_DEVICE", "cpu")
_COMPUTE_TYPE = os.getenv("KENTH_WHISPER_COMPUTE", "int8")

_model = None
_model_lock = threading.Lock()

# Registro de jobs por lesson_id. Estructura:
#   { status: 'running'|'done'|'error', progress: 0..1, error: str|'',
#     segments: int, started_at: float, finished_at: float|None }
_jobs: Dict[str, Dict[str, Any]] = {}
_jobs_lock = threading.Lock()


def _load_model():
    """Carga (y cachea) el modelo faster-whisper. Lanza si no esta instalado."""
    global _model
    if _model is not None:
        return _model
    with _model_lock:
        if _model is not None:
            return _model
        try:
            from faster_whisper import WhisperModel  # import perezoso
        except Exception as exc:  # pragma: no cover - depende del entorno
            raise RuntimeError(
                "faster-whisper no esta instalado. Ejecuta: pip install faster-whisper"
            ) from exc
        _model = WhisperModel(_MODEL_SIZE, device=_DEVICE, compute_type=_COMPUTE_TYPE)
        return _model


def get_status(lesson_id: str) -> Optional[Dict[str, Any]]:
    with _jobs_lock:
        job = _jobs.get(lesson_id)
        return dict(job) if job else None


def _set(lesson_id: str, **fields: Any) -> None:
    with _jobs_lock:
        job = _jobs.setdefault(lesson_id, {})
        job.update(fields)


def _run(lesson_id: str, video_path: str, language: str) -> None:
    try:
        _set(lesson_id, status="running", progress=0.0, error="", segments=0)
        model = _load_model()

        segments_iter, info = model.transcribe(
            video_path,
            language=(language or None),
            vad_filter=True,
            beam_size=5,
            word_timestamps=True,
        )
        total = float(getattr(info, "duration", 0) or 0)

        collected: List[Dict[str, Any]] = []
        for idx, seg in enumerate(segments_iter):
            text = (seg.text or "").strip()
            if not text:
                continue
            # Anclar el inicio/fin a la primera/ultima palabra real: los
            # timestamps a nivel de segmento de Whisper suelen llegar un pelin
            # tarde al comienzo de la frase. Los de palabra son mas precisos.
            words = getattr(seg, "words", None) or []
            start = words[0].start if words and words[0].start is not None else seg.start
            end = words[-1].end if words and words[-1].end is not None else seg.end
            collected.append({
                "seq": len(collected),
                "start_time": round(float(start or 0), 3),
                "end_time": round(float(end or 0), 3),
                "text": text,
                "speaker": "",
            })
            if total > 0:
                progress = min(0.99, float(seg.end or 0) / total)
                _set(lesson_id, progress=progress, segments=len(collected))

        db_service.replace_transcript(lesson_id, collected)
        _set(
            lesson_id,
            status="done",
            progress=1.0,
            segments=len(collected),
            finished_at=time.time(),
        )
    except Exception as exc:  # pragma: no cover - depende del entorno
        _set(lesson_id, status="error", error=str(exc), finished_at=time.time())


def start_transcription(lesson_id: str, video_path: str, language: str = "es") -> Dict[str, Any]:
    """Arranca (o reusa) un job de transcripcion para una leccion."""
    with _jobs_lock:
        existing = _jobs.get(lesson_id)
        if existing and existing.get("status") == "running":
            return dict(existing)
        _jobs[lesson_id] = {
            "status": "running",
            "progress": 0.0,
            "error": "",
            "segments": 0,
            "started_at": time.time(),
            "finished_at": None,
        }

    thread = threading.Thread(
        target=_run,
        args=(lesson_id, video_path, language),
        name=f"whisper-{lesson_id}",
        daemon=True,
    )
    thread.start()
    return get_status(lesson_id) or {"status": "running"}
