"""Contrato JSON estricto del borrador pedagógico + sanitización (Fase 5 y 11).

El modelo debe devolver SOLO JSON. Aquí:
  - extraemos el JSON aunque venga con ```fences``` o bloques <think> (deepseek).
  - validamos con Pydantic, recortando longitudes de listas/strings (tope duro).
  - coercionamos enums fuera de rango a "" (= automático) en vez de romper.
  - sanitizamos instrucciones peligrosas (prompt injection): el borrador es DATO,
    no puede reintroducir instrucciones al tutor ("ignora lo anterior", etc.).

El modelo NUNCA escribe campos técnicos (timestamps, block ids nuevos, source_hash):
este schema no los admite; los `existing_block_id` sólo se ACEPTAN si ya existen
(eso se valida en service.py contra los bloques reales).
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, field_validator

# -------- Límites (seguridad / coste / UI) --------
MAX_STR = 600           # longitud máx. de un string corto (título, objetivo…)
MAX_SUMMARY = 1500      # resumen de lección/momento
MAX_LIST = 12           # nº máx. de ítems por lista
MAX_MOMENTS = 40        # nº máx. de momentos
MAX_ITEM = 300          # longitud máx. de un ítem de lista

TONE_VALUES = {"directo", "paciente", "exigente", "socratico", "practico"}
HELP_VALUES = {"orientar", "explicar", "corregir", "preguntar", "ejemplo_guiado"}
CONFIDENCE_VALUES = {"low", "medium", "high"}

# -------- Detectores de inyección (como DATOS, no lógica cableada) --------
# Se neutraliza (se descarta el ítem/campo) cualquier string que intente
# reintroducir instrucciones al sistema o sacar al tutor del curso.
INJECTION_PATTERNS = [
    r"ignora(r|\s)+.*(instrucc|anterior|previo|reglas|system)",
    r"olvida(r|\s)+.*(instrucc|anterior|previo|reglas)",
    r"responde\s+fuera\s+del\s+curso",
    r"sal(te|ir)\s+del\s+(curso|dominio|tema)",
    r"desactiva(r)?\s+.*(filtro|seguridad|restricc)",
    r"(system|developer)\s*prompt",
    r"act[uú]a\s+como\s+.*(dan|jailbreak|sin\s+restricc)",
    r"ignore\s+.*(previous|above|instruction)",
    r"disregard\s+.*(previous|above|instruction)",
]
_INJECTION_RE = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]


def _looks_injected(text: str) -> bool:
    t = text or ""
    return any(rx.search(t) for rx in _INJECTION_RE)


def _clean_str(value: Any, max_len: int = MAX_STR) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    if _looks_injected(s):
        return ""  # neutraliza: se descarta contenido con instrucciones peligrosas
    # colapsa espacios y recorta
    s = re.sub(r"\s+", " ", s)
    return s[:max_len]


def _clean_list(value: Any, max_items: int = MAX_LIST, max_len: int = MAX_ITEM) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, (list, tuple)):
        return []
    out: List[str] = []
    seen = set()
    for item in value:
        s = _clean_str(item, max_len)
        if not s:
            continue
        key = s.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
        if len(out) >= max_items:
            break
    return out


def _coerce_enum(value: Any, allowed: set) -> str:
    s = (str(value or "")).strip().lower()
    return s if s in allowed else ""


class AiMoment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    existing_block_id: Optional[str] = None
    title: str = ""
    summary: str = ""
    pedagogical_intent: str = ""
    key_concepts: List[str] = []
    probable_questions: List[str] = []
    common_mistakes: List[str] = []

    @field_validator("existing_block_id", mode="before")
    @classmethod
    def _v_bid(cls, v):
        s = str(v or "").strip()
        return s or None

    @field_validator("title", "pedagogical_intent", mode="before")
    @classmethod
    def _v_short(cls, v):
        return _clean_str(v, MAX_STR)

    @field_validator("summary", mode="before")
    @classmethod
    def _v_sum(cls, v):
        return _clean_str(v, MAX_SUMMARY)

    @field_validator("key_concepts", "probable_questions", "common_mistakes", mode="before")
    @classmethod
    def _v_list(cls, v):
        return _clean_list(v)


class AiPrepareDraft(BaseModel):
    model_config = ConfigDict(extra="ignore")
    learning_goal: str = ""
    lesson_summary: str = ""
    key_concepts: List[str] = []
    common_mistakes: List[str] = []
    probable_questions: List[str] = []
    tutor_focus: List[str] = []
    tutor_must_not_do: List[str] = []
    lesson_rules: List[str] = []
    recommended_tone: str = ""
    recommended_help_level: str = ""
    moments: List[AiMoment] = []
    transcript_quality_notes: List[str] = []
    terms_to_review: List[str] = []
    confidence: str = "low"

    @field_validator("learning_goal", mode="before")
    @classmethod
    def _v_goal(cls, v):
        return _clean_str(v, MAX_STR)

    @field_validator("lesson_summary", mode="before")
    @classmethod
    def _v_summary(cls, v):
        return _clean_str(v, MAX_SUMMARY)

    @field_validator(
        "key_concepts", "common_mistakes", "probable_questions",
        "tutor_focus", "tutor_must_not_do", "lesson_rules",
        "transcript_quality_notes", "terms_to_review",
        mode="before",
    )
    @classmethod
    def _v_lists(cls, v):
        return _clean_list(v)

    @field_validator("recommended_tone", mode="before")
    @classmethod
    def _v_tone(cls, v):
        return _coerce_enum(v, TONE_VALUES)

    @field_validator("recommended_help_level", mode="before")
    @classmethod
    def _v_help(cls, v):
        return _coerce_enum(v, HELP_VALUES)

    @field_validator("confidence", mode="before")
    @classmethod
    def _v_conf(cls, v):
        s = _coerce_enum(v, CONFIDENCE_VALUES)
        return s or "low"

    @field_validator("moments", mode="before")
    @classmethod
    def _v_moments(cls, v):
        if not isinstance(v, (list, tuple)):
            return []
        return list(v)[:MAX_MOMENTS]


def extract_json_block(text: str) -> Optional[str]:
    """Extrae el primer objeto JSON balanceado de un texto ruidoso.

    Tolera ```json fences```, prefijos, y bloques <think>...</think> de deepseek-r1.
    """
    if not text:
        return None
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # quita fences de código
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, flags=re.DOTALL)
    if fence:
        return fence.group(1)
    # busca el primer { y recorre balanceando llaves (respeta strings)
    start = cleaned.find("{")
    if start == -1:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return cleaned[start:i + 1]
    return None


def parse_and_validate(raw_text: str) -> Tuple[Optional[AiPrepareDraft], List[str]]:
    """Parsea + valida el texto crudo del modelo.

    Devuelve (draft|None, errores). Si no hay JSON parseable, draft=None y el
    caller decide reparar (una vez) o fallar de forma controlada.
    """
    errors: List[str] = []
    block = extract_json_block(raw_text)
    if not block:
        return None, ["No se encontró un objeto JSON en la respuesta del modelo."]
    try:
        data = json.loads(block)
    except json.JSONDecodeError as exc:
        return None, [f"JSON inválido: {exc}"]
    if not isinstance(data, dict):
        return None, ["El JSON raíz no es un objeto."]
    try:
        draft = AiPrepareDraft.model_validate(data)
    except Exception as exc:  # pydantic ValidationError u otros
        return None, [f"El JSON no cumple el schema: {exc}"]
    return draft, errors


def validate_dict(data: Any) -> Tuple[Optional[AiPrepareDraft], List[str]]:
    """Valida un borrador que ya es dict (p. ej. editado por el profesor al aceptar).

    Reaplica TODA la sanitización/recorte del schema, así una edición manual tampoco
    puede colar strings peligrosos ni listas gigantes.
    """
    if not isinstance(data, dict):
        return None, ["El borrador no es un objeto JSON."]
    try:
        draft = AiPrepareDraft.model_validate(data)
    except Exception as exc:
        return None, [f"El borrador no cumple el schema: {exc}"]
    return draft, []


def draft_to_public(draft: AiPrepareDraft) -> Dict[str, Any]:
    """Serializa el borrador validado a dict limpio (para persistir/mostrar)."""
    return draft.model_dump()
