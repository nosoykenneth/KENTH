"""Domain Pack — conocimiento de dominio de un curso cargado desde datos.

Objetivo (Fase 0): sacar TODO el conocimiento de dominio (ejes, conceptos,
listas permitidas/bloqueadas, prompts de persona, respuestas controladas) del
codigo Python hacia domain_packs/<course_id>.json. El backend se vuelve un
lienzo en blanco que procesa el dominio inyectado.

- get_domain_pack(course_id) resuelve el pack del curso; si no existe el archivo,
  cae a domain_packs/_default.json (neutro). El resultado se cachea.
- DomainPack expone accesores que RECONSTRUYEN los tipos exactos que el agente
  usaba como constantes (lista de tuplas, set, dict), para que el cableado sea
  drop-in y behavior-preserving (verificado por el gate determinista de Fase 0).

course_id == id numerico del curso Moodle (convencion del proyecto). El default
sigue KENTH_DEFAULT_COURSE_ID (igual que ingest.py) para el piloto mono-curso.
"""

from __future__ import annotations

import json
import os
import threading
from typing import Any, Dict, List, Optional, Tuple

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACK_DIR = os.path.join(_BASE_DIR, "domain_packs")
DEFAULT_COURSE_ID = os.getenv("KENTH_DEFAULT_COURSE_ID", "2")
DEFAULT_PACK_NAME = "_default"

_CACHE: Dict[str, "DomainPack"] = {}
_LOCK = threading.Lock()


class DomainPack:
    """Wrapper tipado sobre el JSON del pack. Los accesores devuelven los tipos
    que el agente espera (no el dict crudo)."""

    def __init__(self, data: dict, *, pack_id: str, source_path: str):
        self._data = data or {}
        self.pack_id = pack_id
        self.source_path = source_path

    # ---- meta ----
    @property
    def persona(self) -> Dict[str, str]:
        return dict(self._data.get("persona") or {})

    @property
    def description(self) -> str:
        return str(self._data.get("description") or "")

    def domain_label(self, default: str = "") -> str:
        """Etiqueta corta del dominio del curso (p. ej. 'mezcla y masterizacion').

        Fuente de verdad para textos que antes cableaban el nombre del curso en el
        codigo del agente (clasificador, etc.). Cae al default si el pack no la
        define, para que un curso sin pack degrade sin romper.
        """
        return str(self.persona.get("domain_label") or default)

    @property
    def node_prompts(self) -> Dict[str, Any]:
        return dict(self._data.get("node_prompts") or {})

    # ---- taxonomy ----
    def course_axes(self) -> List[dict]:
        return list((self._data.get("taxonomy") or {}).get("course_axes") or [])

    def strong_axis_terms(self) -> Dict[str, List[str]]:
        return dict((self._data.get("taxonomy") or {}).get("strong_axis_terms") or {})

    # ---- lexicon ----
    def concept_patterns(self) -> List[Tuple[str, List[str]]]:
        raw = (self._data.get("lexicon") or {}).get("concept_patterns") or []
        return [(item[0], list(item[1])) for item in raw]

    def technical_word_list(self) -> List[str]:
        return list((self._data.get("lexicon") or {}).get("technical_word_list") or [])

    def domain_hint_terms(self) -> List[str]:
        return list((self._data.get("lexicon") or {}).get("domain_hint_terms") or [])

    def lookup_stopwords(self) -> set:
        return set((self._data.get("lexicon") or {}).get("lookup_stopwords") or [])

    # ---- blocklist ----
    def unsupported_terms(self) -> List[str]:
        return list((self._data.get("blocklist") or {}).get("unsupported_terms") or [])

    # ---- intents ----
    def prompt_common_rules(self) -> str:
        return (self._data.get("intents") or {}).get("common_rules", "")

    def prompts_by_intent(self) -> Dict[str, dict]:
        return dict((self._data.get("intents") or {}).get("by_intent") or {})

    def intent_selection_keywords(self) -> List[Tuple[str, List[str]]]:
        raw = (self._data.get("intents") or {}).get("selection_keywords") or []
        return [(item[0], list(item[1])) for item in raw]

    # ---- node prompt helpers ----
    def node_prompt(self, key: str, default: str = "") -> str:
        return self.node_prompts.get(key, default)

    def greetings(self) -> Dict[str, str]:
        return dict(self.node_prompts.get("greetings") or {})

    # ---- controlled answers (FAQ extraido del codigo a datos) ----
    def controlled_answers(self) -> List[dict]:
        return list(self._data.get("controlled_answers") or [])

    # ---- attribution verifiers (FIX G: verificacion post-gen de
    # attribution_constraints como datos, no codigo) ----
    def attribution_verifiers(self) -> List[dict]:
        """Detectores deterministas de cumplimiento de restricciones de conducta.

        Cada detector mapea el texto libre de una `attribution_constraint` del
        profesor (via `constraint_markers`) a un patron de violacion en la salida
        (`violation_markers`) y una reparacion suave (`repairs`). Son reglas de
        conducta agnosticas al curso (no prometer resultados, no recetas
        universales); por eso viven tambien en `_default.json`. Lista vacia => la
        verificacion post-gen no impone nada deterministicamente (igual que antes
        del FIX G) y todo queda para la capa LLM opcional."""
        return list(self._data.get("attribution_verifiers") or [])


def _load_pack_file(name: str) -> Optional[Tuple[dict, str]]:
    path = os.path.join(PACK_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f), path


def _resolve_course_id(course_id: Optional[str]) -> str:
    cid = str(course_id or "").strip()
    return cid or DEFAULT_COURSE_ID


def get_domain_pack(course_id: Optional[str] = None) -> DomainPack:
    """Devuelve el DomainPack del curso (cacheado). Fallback a _default si no hay
    archivo para ese course_id."""
    cid = _resolve_course_id(course_id)
    cached = _CACHE.get(cid)
    if cached is not None:
        return cached

    with _LOCK:
        cached = _CACHE.get(cid)
        if cached is not None:
            return cached
        loaded = _load_pack_file(cid)
        if loaded is None:
            loaded = _load_pack_file(DEFAULT_PACK_NAME)
            if loaded is None:
                raise FileNotFoundError(
                    f"No se encontro domain pack para course_id={cid!r} ni _default en {PACK_DIR}"
                )
            data, path = loaded
            pack = DomainPack(data, pack_id=f"{DEFAULT_PACK_NAME}(for {cid})", source_path=path)
        else:
            data, path = loaded
            pack = DomainPack(data, pack_id=cid, source_path=path)
        _CACHE[cid] = pack
        return pack


def clear_cache() -> None:
    """Util para tests/recarga tras editar un pack."""
    with _LOCK:
        _CACHE.clear()
