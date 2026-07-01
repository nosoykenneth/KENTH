"""Selección de modelos por TAREA para el asistente de preparación (Fase 2).

Capa fina sobre `langchain_ollama.ChatOllama` que:
  - elige el modelo según la tarea (borrador / revisión / contexto largo), leyendo
    la configuración de `config.py` (env vars); nada hardcodeado.
  - construye un cliente ROBUSTO: base_url explícito (OLLAMA_BASE_URL, que el chat
    en vivo ignora hoy), timeout, num_ctx y reintentos.
  - fuerza salida JSON cuando la tarea lo requiere (`format="json"`).

Es AISLADA del grafo del tutor: no importa ni modifica services/agent/*. Así el
chat en vivo, su payload y sus tests no cambian.
"""

from __future__ import annotations

from typing import Optional

import config

# Nombres de tarea (evita strings sueltos por el código).
TASK_DRAFT = "draft"            # generar el JSON pedagógico estructurado
TASK_REVIEW = "review"          # revisión de calidad opcional (quality=max)
TASK_LONG_CONTEXT = "long"      # resumen jerárquico de transcripciones largas
TASK_VISION = "vision"          # análisis de slides/frames (si se habilita)
TASK_CHAT = "chat"              # (informativo; el chat en vivo NO usa esta capa)


def get_model_name(task: str) -> str:
    """Modelo Ollama configurado para una tarea. Default seguro por tarea."""
    return {
        TASK_DRAFT: config.AI_PREP_MODEL,
        TASK_REVIEW: config.AI_PREP_REVIEW_MODEL,
        TASK_LONG_CONTEXT: config.AI_PREP_LONG_CONTEXT_MODEL,
        TASK_VISION: config.AI_VISION_MODEL,
        TASK_CHAT: config.AI_CHAT_MODEL,
    }.get(task, config.AI_PREP_MODEL)


def build_chat(
    task: str,
    *,
    force_json: bool = False,
    temperature: float = 0.2,
    num_ctx: Optional[int] = None,
    model: Optional[str] = None,
):
    """Devuelve un Runnable ChatOllama configurado y con reintentos.

    `model` permite forzar un modelo concreto (p. ej. quality=max explícito); si no,
    se resuelve por `task`. Lanza RuntimeError si langchain_ollama no está instalado.
    """
    try:
        from langchain_ollama import ChatOllama
    except Exception as exc:  # pragma: no cover - depende del entorno
        raise RuntimeError(
            "langchain_ollama no está instalado. Ejecuta: pip install langchain-ollama"
        ) from exc

    model_name = model or get_model_name(task)
    kwargs = {
        "model": model_name,
        "base_url": config.OLLAMA_BASE_URL,
        "temperature": temperature,
        "num_ctx": int(num_ctx or config.AI_PREP_NUM_CTX),
        # client_kwargs -> ollama.Client(timeout=...): corta el cuelgue de un 14B/32B.
        "client_kwargs": {"timeout": config.AI_PREP_TIMEOUT},
    }
    if force_json:
        kwargs["format"] = "json"

    llm = ChatOllama(**kwargs)
    # Reintenta ante errores transitorios (modelo cargando, timeout puntual).
    retries = max(0, int(config.AI_PREP_MAX_RETRIES))
    if retries:
        llm = llm.with_retry(stop_after_attempt=retries + 1)
    return llm


def invoke_text(
    task: str,
    system_prompt: str,
    user_prompt: str,
    *,
    force_json: bool = False,
    temperature: float = 0.2,
    num_ctx: Optional[int] = None,
    model: Optional[str] = None,
) -> str:
    """Ejecuta una llamada de texto simple (system + user) y devuelve el string crudo."""
    from langchain_core.messages import SystemMessage, HumanMessage

    llm = build_chat(
        task,
        force_json=force_json,
        temperature=temperature,
        num_ctx=num_ctx,
        model=model,
    )
    resp = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)])
    content = getattr(resp, "content", resp)
    return content if isinstance(content, str) else str(content)


def describe_selection(quality: str) -> dict:
    """Modelos que se usarán para una calidad dada (para logging/telemetría/UI).

    quality: fast|balanced|max. 'max' añade el modelo revisor.
    """
    info = {
        "draft_model": get_model_name(TASK_DRAFT),
        "long_context_model": get_model_name(TASK_LONG_CONTEXT),
        "review_model": None,
    }
    if quality == "max":
        info["review_model"] = get_model_name(TASK_REVIEW)
    return info
