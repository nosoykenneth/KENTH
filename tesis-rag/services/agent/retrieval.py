import os
import re

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from models.schemas import EstadoAgente
from services.agent.routing import (
    LOOKUP_STOPWORDS,
    TECHNICAL_CONCEPT_PATTERNS,
    _es_pregunta_ambigua,
    _es_pregunta_conceptual_directa,
    _es_pregunta_lookup,
    _conceptos_en_texto,
    _resolver_referente_ambiguo,
    _respuesta_aclaracion_ambigua,
    _tiene_termino_tecnico_curso,
    _tokens_lookup,
    _eje_fuerte_pregunta,
    _normalizar_texto,
    _axis_id_meta,
)

EMBEDDING_MODEL_NAME = "nomic-embed-text"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "bd_vectorial")
RETRIEVAL_K = 8
MIN_RELEVANCE_SCORE = 0.35
SPECIFIC_UNSUPPORTED_TERMS = [
    "serum", "sintesis", "synthesis", "fm", "wavetable", "granular",
    "ableton", "logic", "fl studio", "cubase", "pro tools", "reaper",
    "massive", "sylenth", "vital", "kontakt", "oversampling"
]
CURRENT_AXIS_BOOST = 0.35
PREVIOUS_AXIS_SUPPORT_BOOST = 0.16
FUTURE_AXIS_DEFAULT_PENALTY = -0.30
FUTURE_AXIS_REQUESTED_BOOST = 0.24

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)


def _get_vector_store():
    return Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)


def _reescribir_query_contextual(pregunta: str, historial: list, contexto_leccion: str = ""):
    if not _es_pregunta_ambigua(pregunta):
        return pregunta, ""

    referente, aclaracion = _resolver_referente_ambiguo(pregunta, historial)
    if not referente:
        return "", aclaracion

    return f"{referente}. Pregunta de seguimiento: {pregunta}"[:300], ""


def _contiene_frase(texto: str, frase: str):
    texto_norm = _normalizar_texto(texto)
    frase_norm = _normalizar_texto(frase)
    return frase_norm in texto_norm


def _texto_evidencia(evidencias: list):
    partes = []
    for item in evidencias:
        doc = item["document"]
        meta = doc.metadata or {}
        partes.append(doc.page_content or "")
        partes.extend(str(valor) for valor in meta.values() if valor)
    return "\n".join(partes)


def _terminos_especificos_no_soportados(pregunta: str, evidencias: list):
    evidencia = _texto_evidencia(evidencias)
    no_soportados = []
    for termino in SPECIFIC_UNSUPPORTED_TERMS:
        if _contiene_frase(pregunta, termino) and not _contiene_frase(evidencia, termino):
            no_soportados.append(termino)

    pregunta_norm = _normalizar_texto(pregunta)
    evidencia_norm = _normalizar_texto(evidencia)
    pregunta_pide_fm = "fm" in pregunta_norm.split() and ("sintesis" in pregunta_norm or "synthesis" in pregunta_norm)
    evidencia_soporta_fm = "fm" in evidencia_norm.split() and ("sintesis" in evidencia_norm or "synthesis" in evidencia_norm)
    if pregunta_pide_fm and not evidencia_soporta_fm and "sintesis fm" not in no_soportados:
        no_soportados.append("sintesis fm")

    return no_soportados


def _respuesta_fuera_de_material(terminos: list):
    tema = ", ".join(terminos[:3]) if terminos else "ese tema"
    return (
        f"No tengo respaldo suficiente en el material cargado del curso para explicar {tema}. "
        "Para evitar inventar, no voy a desarrollarlo. Si existe una clase o recurso del curso sobre eso, indicame cual."
    )



def _resumen_metadata_debug(meta: dict):
    return {
        "filename": meta.get("filename") or os.path.basename(meta.get("source", "")),
        "doc_type": meta.get("doc_type"),
        "axis": meta.get("axis") or meta.get("eje") or meta.get("module") or meta.get("modulo"),
        "layer": meta.get("layer") or meta.get("capa"),
        "topic": meta.get("topic") or meta.get("tema"),
        "resource_title": meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso"),
        "page": meta.get("page"),
        "start_time": meta.get("start_time"),
        "url": meta.get("url") or meta.get("url_video")
    }


def _axis_number_from_value(value):
    if value in ("", None):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value)
    match = re.search(r"(\d+)", text)
    if not match:
        return None
    try:
        return int(match.group(1))
    except Exception:
        return None


def _axis_number_from_meta(meta: dict):
    axis = (
        meta.get("axis")
        or meta.get("eje")
        or meta.get("axis_id")
        or meta.get("axis_number")
        or meta.get("module")
        or meta.get("modulo")
        or meta.get("module_id")
    )
    number = _axis_number_from_value(axis)
    if number is not None:
        return number

    source = " ".join([
        str(meta.get("source", "")),
        str(meta.get("filename", "")),
    ])
    return _axis_number_from_value(source)


def _axis_label(axis_number):
    return f"Eje {axis_number}" if axis_number is not None else ""


def _current_axis_number(state: dict):
    if not state:
        return None

    envelope = state.get("tutor_envelope")
    ctx = getattr(envelope, "activity_context", None) if envelope else None
    if ctx:
        number = _axis_number_from_value(getattr(ctx, "current_axis", ""))
        if number is not None:
            return number

    activity_context = state.get("activity_context")
    if isinstance(activity_context, dict):
        number = _axis_number_from_value(activity_context.get("current_axis"))
        if number is not None:
            return number

    return _axis_number_from_value(state.get("course_module", ""))


def _question_axis_number(pregunta: str):
    axis = _eje_fuerte_pregunta(pregunta)
    return _axis_number_from_value(axis)


def _is_future_axis_question(state: dict, pregunta: str):
    current = _current_axis_number(state)
    requested = _question_axis_number(pregunta)
    return (
        current is not None
        and requested is not None
        and requested > current
    )


def _curriculum_relation(state: dict, axis_number):
    current = _current_axis_number(state)
    if current is None or axis_number is None:
        return "unknown"
    if axis_number < current:
        return "previous"
    if axis_number == current:
        return "current"
    return "future"


def _curriculum_priority_adjustment(item: dict, pregunta: str, state: dict = None):
    current = _current_axis_number(state or {})
    if current is None:
        return 0.0

    axis_number = _axis_number_from_meta(item["document"].metadata or {})
    if axis_number is None:
        return 0.0

    requested = _question_axis_number(pregunta)

    if requested is not None and requested > current:
        if axis_number == requested:
            return FUTURE_AXIS_REQUESTED_BOOST
        if axis_number == current:
            return 0.14
        if axis_number < current:
            return 0.08
        return -0.18

    if axis_number == current:
        return CURRENT_AXIS_BOOST
    if axis_number < current:
        return PREVIOUS_AXIS_SUPPORT_BOOST
    return FUTURE_AXIS_DEFAULT_PENALTY


def _debug_resultados_retrieval(resultados: list, etiqueta: str):
    print(f"[RETRIEVAL DEBUG] {etiqueta}: top_chunks={len(resultados)}")
    for index, item in enumerate(resultados[:8], start=1):
        if isinstance(item, tuple):
            doc, score = item
        else:
            doc = item.get("document")
            score = item.get("score")
        meta = doc.metadata or {}
        print(
            f"[RETRIEVAL DEBUG] #{index} score={float(score or 0):.4f} "
            f"meta={_resumen_metadata_debug(meta)}"
        )


def _concepto_aparece_en_texto(concepto: str, texto_norm: str):
    for concepto_base, aliases in TECHNICAL_CONCEPT_PATTERNS:
        if concepto_base != concepto:
            continue
        for alias in aliases:
            alias_norm = _normalizar_texto(alias).strip()
            if not alias_norm:
                continue
            if len(alias_norm) <= 2:
                if f" {alias_norm} " in f" {texto_norm} ":
                    return True
            elif alias_norm in texto_norm:
                return True
        return False
    return concepto in texto_norm


def _conceptos_relevantes_pregunta(pregunta: str):
    conceptos = _conceptos_en_texto(pregunta)
    pregunta_norm = _normalizar_texto(pregunta)

    # "frecuencia de corte" activa tambien el alias generico "filtro".
    # Si el alumno no escribio filtro/filtros literalmente, quitamos ese
    # concepto amplio para no contaminar comparaciones especificas.
    if (
        "frecuencia de corte" in conceptos
        and "filtro" in conceptos
        and "filtro" not in pregunta_norm
        and "filtros" not in pregunta_norm
    ):
        conceptos.remove("filtro")

    unicos = []
    for concepto in conceptos:
        if concepto not in unicos:
            unicos.append(concepto)
    return unicos


def _es_pregunta_comparativa_multiconcepto(pregunta: str):
    pregunta_norm = _normalizar_texto(pregunta)
    marcadores = [
        "diferencia entre",
        "explicame la diferencia",
        "explica la diferencia",
        "compara",
        "comparame",
        "comparar",
        "es lo mismo",
    ]
    return (
        any(marcador in pregunta_norm for marcador in marcadores)
        and len(_conceptos_relevantes_pregunta(pregunta)) >= 2
    )


def _prioridad_evidencia(item: dict, pregunta: str, state: dict = None):
    doc = item["document"]
    meta = doc.metadata or {}
    pregunta_norm = _normalizar_texto(pregunta)
    texto = _normalizar_texto(" ".join([
        doc.page_content or "",
        meta.get("filename", ""),
        meta.get("doc_type", ""),
        meta.get("topic", "") or meta.get("tema", ""),
        meta.get("lesson_title", ""),
        meta.get("resource_title", ""),
    ]))
    tokens = _tokens_lookup(pregunta)
    token_matches = sum(1 for token in tokens if token in texto)
    prioridad = float(item.get("score") or 0) + min(0.30, token_matches * 0.06)

    # Prioridad por Eje
    axis_meta = _axis_id_meta(meta)
    axis_fuerte = _eje_fuerte_pregunta(pregunta)
    if axis_fuerte and axis_meta == axis_fuerte:
        prioridad += 0.70
    elif axis_fuerte and axis_meta:
        prioridad -= 0.20

    prioridad += _curriculum_priority_adjustment(item, pregunta, state)

    filename = (meta.get("filename") or "").lower()

    # Prioridad por Capa/Layer
    layer = (meta.get("layer") or meta.get("capa") or "general").lower()
    
    es_conceptual = _es_pregunta_conceptual_directa(pregunta) or bool(_concepto_definicion_directa(pregunta)) or "diferencia" in pregunta_norm
    es_operativa = any(word in pregunta_norm for word in ["error", "falla", "matriz", "heuristica", "criterio", "operativo", "saturacion", "clip", "que hago si", "como corrijo", "falla probable", "que error"])

    # Boost a chunks definicionales si es conceptual
    if es_conceptual:
        patrones_def = [" se define como ", " es un ", " es una ", " diferencia entre ", " definicion", " concepto tecnico ", " tabla ", " criterio "]
        if any(p in texto for p in patrones_def) or filename.endswith("_glosario.json"):
            prioridad += 0.18

    # Sesgo suave por Capa (no exclusion)
    if es_conceptual:
        if layer == "canonico":
            prioridad += 0.12
        elif layer == "limpio":
            prioridad += 0.08
    elif es_operativa:
        if layer == "limpio":
            prioridad += 0.12
        elif layer == "canonico":
            prioridad += 0.08

    if filename.endswith(("_faq.json", "_glosario.json", "_guia_canonica.md", "_paquete_limpio.md")):
        prioridad += 0.06

    if (
        "diferencia" in pregunta_norm
        and "filtro" in pregunta_norm
        and "ecualizacion" in pregunta_norm
        and ("guia_canonica" in filename or "canonico" in filename)
    ):
        prioridad += 0.45
    if "frecuencia de corte" in pregunta_norm and "frecuencia de corte" in texto:
        prioridad += 0.25
    if "pendiente" in pregunta_norm and " q " in f" {pregunta_norm} " and "pendiente" in texto and (" q " in f" {texto} " or "factor q" in texto):
        prioridad += 0.30
    if "fase lineal" in pregunta_norm and "fase lineal" in texto:
        prioridad += 0.25
    if "ecualizacion dinamica" in pregunta_norm and "ecualizacion dinamica" in texto:
        prioridad += 0.25
    if "capa" in pregunta_norm and ("perdio cuerpo" in pregunta_norm or "perdido cuerpo" in pregunta_norm) and ("layering" in texto or "capa" in texto):
        prioridad += 0.25

    if _es_pregunta_comparativa_multiconcepto(pregunta):
        conceptos = _conceptos_relevantes_pregunta(pregunta)
        cobertura = sum(1 for concepto in conceptos if _concepto_aparece_en_texto(concepto, texto))
        prioridad += min(0.50, cobertura * 0.16)
        if cobertura >= 2:
            prioridad += 0.20
        if conceptos and cobertura == len(conceptos):
            prioridad += 0.25

    return prioridad


def _concepto_definicion_directa(pregunta: str):
    pregunta_norm = _normalizar_texto(pregunta)
    patrones = [
        "que es", "que significa", "cual es", "define", "definicion de"
    ]
    if not any(pregunta_norm.startswith(patron) for patron in patrones):
        return ""

    concepto = pregunta_norm
    for patron in patrones:
        if concepto.startswith(patron):
            concepto = concepto[len(patron):].strip()
            break

    for stop in ["?", "en mezcla", "en el curso", "del curso"]:
        concepto = concepto.replace(stop, "").strip()
    if concepto == "q":
        return "factor q"
    return concepto


def _ordenar_para_respuesta_directa(evidencias: list, pregunta: str):
    axis_fuerte = _eje_fuerte_pregunta(pregunta)
    pregunta_norm = _normalizar_texto(pregunta)
    if "bus" in pregunta_norm and "auxiliar" in pregunta_norm:
        def prioridad_bus_auxiliar(item):
            doc = item["document"]
            meta = doc.metadata or {}
            texto = _normalizar_texto(doc.page_content or "")
            filename = (meta.get("filename") or "").lower()
            topic = _normalizar_texto(meta.get("topic", "") or meta.get("tema", ""))
            score = float(item.get("score") or 0)
            if "faq" in filename and "ruteo" in topic:
                score += 30
            if "glosario" in filename and "ruteo" in topic:
                score += 25
            if "canonico" in filename and "bus" in texto and "auxiliar" in texto:
                score += 20
            return score

        return sorted(evidencias, key=prioridad_bus_auxiliar, reverse=True)[:5]

    if _es_pregunta_comparativa_multiconcepto(pregunta):
        conceptos = _conceptos_relevantes_pregunta(pregunta)

        def prioridad_comparacion(item):
            doc = item["document"]
            meta = doc.metadata or {}
            texto = _normalizar_texto(" ".join([
                doc.page_content or "",
                meta.get("topic", "") or meta.get("tema", ""),
                meta.get("filename", ""),
            ]))
            filename = (meta.get("filename") or "").lower()
            cobertura = sum(1 for concepto in conceptos if _concepto_aparece_en_texto(concepto, texto))
            score = _prioridad_evidencia(item, pregunta) + (cobertura * 10)
            if axis_fuerte and _axis_id_meta(meta) == axis_fuerte:
                score += 12
            if "canonico" in filename or "guia_canonica" in filename:
                score += 4
            if "faq" in filename:
                score += 3
            if "glosario" in filename:
                score += 3
            return score

        return sorted(evidencias, key=prioridad_comparacion, reverse=True)[:5]

    concepto = _concepto_definicion_directa(pregunta)
    if not concepto:
        return evidencias

    def prioridad(item):
        doc = item["document"]
        meta = doc.metadata or {}
        texto = _normalizar_texto(" ".join([
            doc.page_content or "",
            meta.get("topic", "") or meta.get("tema", ""),
            meta.get("resource_title", ""),
            meta.get("filename", ""),
        ]))
        filename = (meta.get("filename") or "").lower()
        score = _prioridad_evidencia(item, pregunta)
        if concepto and concepto in texto:
            score += 10
        if axis_fuerte and _axis_id_meta(meta) == axis_fuerte:
            score += 12
        if "glosario" in filename:
            score += 4
        if "faq" in filename:
            score += 3
        if "canonico" in filename:
            score += 1
        return score

    ordenadas = sorted(evidencias, key=prioridad, reverse=True)
    return ordenadas[:4]


def _buscar_evidencia(pregunta: str, modo_lookup: bool = False, state: dict = None):
    """Recupera documentos con score y filtra evidencia debil."""
    try:
        db = _get_vector_store()
        resultados = db.similarity_search_with_relevance_scores(
            pregunta,
            k=12 if modo_lookup else RETRIEVAL_K
        )
    except Exception as e:
        print(f"[AGENTE RAG]: Error recuperando evidencia con score: {e}")
        return []

    _debug_resultados_retrieval(resultados, f"semantic query='{pregunta}'")

    evidencias = []
    min_score = 0.05 if modo_lookup else MIN_RELEVANCE_SCORE
    for doc, score in resultados:
        score = float(score or 0)
        if score < min_score:
            continue
        evidencias.append({
            "document": doc,
            "score": score
        })

    if not modo_lookup:
        evidencias.extend(_buscar_evidencia_lexica_lookup(pregunta)[:6])

    vistos = set()
    unicas = []
    for item in evidencias:
        meta = item["document"].metadata or {}
        clave = meta.get("chunk_id") or f"{meta.get('source')}::{meta.get('chunk_index')}"
        if clave in vistos:
            continue
        vistos.add(clave)
        unicas.append(item)

    unicas.sort(key=lambda item: _prioridad_evidencia(item, pregunta, state), reverse=True)
    for item in unicas:
        axis_number = _axis_number_from_meta(item["document"].metadata or {})
        item["axis_relation"] = _curriculum_relation(state or {}, axis_number)
    _debug_resultados_retrieval(unicas, "semantic+lexical merged")
    return unicas


def _extraer_frases_lookup(pregunta: str):
    """Extrae frases compuestas significativas de la pregunta para busqueda lexica."""
    texto = _normalizar_texto(pregunta)
    for sw in ["que recurso reviso para entender", "que recurso reviso para",
               "que recurso reviso", "que recurso debo", "que debo revisar",
               "donde explican", "donde se explica", "en que clase se explica mejor lo del",
               "en que clase se explica mejor", "en que clase se explica", "en que clase",
               "en que minuto reviso el", "en que minuto reviso", "en que minuto",
               "que pdf tengo que volver a leer para", "que pdf tengo que leer",
               "que pdf", "en que pagina", "que pagina reviso",
               "donde puedo repasar", "en que parte", "en que documento",
               "que video", "que material", "donde esta", "donde encuentro",
               "que revisar para", "que revisar", "donde se habla de", "donde se habla",
               "en que modulo", "que archivo", "donde veo", "donde aparece"]:
        if texto.startswith(sw):
            texto = texto[len(sw):].strip()
            break

    palabras = [w for w in texto.split() if w not in LOOKUP_STOPWORDS and len(w) > 2]
    if not palabras:
        return [], []

    frase_completa = " ".join(palabras)
    frases = [frase_completa]

    if len(palabras) >= 3:
        for i in range(len(palabras) - 1):
            frases.append(f"{palabras[i]} {palabras[i+1]}")

    return frases, palabras


def _buscar_evidencia_lexica_lookup(pregunta: str):
    frases, tokens = _extraer_frases_lookup(pregunta)
    if not tokens:
        return []

    pregunta_limpia = _normalizar_texto(pregunta)
    pide_minuto = "minuto" in pregunta_limpia
    pide_pagina = "pagina" in pregunta_limpia or "pdf" in pregunta_limpia

    try:
        db = _get_vector_store()
        data = db._collection.get(include=["documents", "metadatas"])
    except Exception as e:
        print(f"[LOOKUP DEBUG] No se pudo escanear Chroma lexicalmente: {e}")
        return []

    documentos = data.get("documents") or []
    metadatas = data.get("metadatas") or []
    candidatos = []

    for doc_text, meta in zip(documentos, metadatas):
        meta = meta or {}
        texto = " ".join([
            doc_text or "",
            " ".join(str(valor) for valor in meta.values() if valor not in ("", None))
        ])
        texto_limpio = _normalizar_texto(texto)

        frase_matches = sum(1 for frase in frases if frase in texto_limpio)
        token_matches = sum(1 for token in tokens if token in texto_limpio)

        if frase_matches == 0 and token_matches == 0:
            continue

        score = 0.30 + (frase_matches * 0.18) + (token_matches * 0.05)

        recurso = _normalizar_texto(meta.get("resource_title") or meta.get("recurso_recomendado") or "")
        tema = _normalizar_texto(meta.get("topic") or meta.get("tema") or "")
        clase = _normalizar_texto(meta.get("lesson_title") or "")

        for frase in frases:
            if frase in recurso:
                score += 0.20
            if frase in tema or frase in clase:
                score += 0.15

        if pide_minuto and meta.get("start_time") not in ("", None):
            score += 0.20
        if pide_pagina and meta.get("page") not in ("", None):
            score += 0.10

        score = min(0.99, score)
        candidatos.append({
            "document": Document(page_content=doc_text or "", metadata=meta),
            "score": score,
            "phrase_hits": frase_matches
        })

    candidatos.sort(key=lambda item: item["score"], reverse=True)
    _debug_resultados_retrieval(candidatos, f"lexical lookup frases={frases} tokens={tokens}")
    return candidatos[:12]


def _prioridad_lookup(item: dict, pregunta: str):
    meta = item["document"].metadata or {}
    pregunta_limpia = _normalizar_texto(pregunta)
    texto_meta = _normalizar_texto(" ".join(str(valor) for valor in meta.values() if valor not in ("", None)))
    prioridad = float(item.get("score") or 0)

    if meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso"):
        prioridad += 0.25
    if meta.get("start_time") not in ("", None):
        prioridad += 0.25
    if meta.get("doc_type") == "video_transcript":
        prioridad += 0.15
    if "pdf" in pregunta_limpia and meta.get("doc_type") == "pdf":
        prioridad += 0.35
    if "pagina" in pregunta_limpia and meta.get("page") not in ("", None):
        prioridad += 0.25
    if "minuto" in pregunta_limpia and meta.get("start_time") not in ("", None):
        prioridad += 0.35

    for token in _tokens_lookup(pregunta):
        if token in texto_meta:
            prioridad += 0.05

    return prioridad


def _buscar_evidencia_lookup(pregunta: str, state: dict = None):
    semanticas = _buscar_evidencia(pregunta, modo_lookup=True, state=state)
    lexicas = _buscar_evidencia_lexica_lookup(pregunta)

    for item in lexicas:
        phrase_hits = item.pop("phrase_hits", 0)
        if phrase_hits >= 1:
            item["score"] = min(0.99, item["score"] + 0.10)

    evidencias = []
    evidencias.extend(semanticas)
    evidencias.extend(lexicas)

    vistos = set()
    unicas = []
    for item in evidencias:
        meta = item["document"].metadata or {}
        clave = meta.get("chunk_id") or f"{meta.get('source')}::{meta.get('chunk_index')}"
        if clave in vistos:
            continue
        vistos.add(clave)
        unicas.append(item)

    unicas.sort(key=lambda item: _prioridad_lookup(item, pregunta), reverse=True)
    for item in unicas:
        axis_number = _axis_number_from_meta(item["document"].metadata or {})
        item["axis_relation"] = _curriculum_relation(state or {}, axis_number)
    _debug_resultados_retrieval(unicas, "lookup merged")
    return unicas[:6]


def _formatear_fuente(meta: dict, score: float, index: int):
    filename = meta.get("filename") or os.path.basename(meta.get("source", "")) or "archivo sin nombre"
    fuente = {
        "origin": "course",
        "index": index,
        "filename": filename,
        "doc_type": meta.get("doc_type") or "",
        "chunk_id": meta.get("chunk_id") or "",
        "page": meta.get("page") if meta.get("page") not in ("", None) else None,
        "start_time": meta.get("start_time") if meta.get("start_time") not in ("", None) else None,
        "end_time": meta.get("end_time") if meta.get("end_time") not in ("", None) else None,
        "axis": meta.get("axis") or meta.get("eje") or meta.get("axis_id") or meta.get("module") or meta.get("modulo") or "",
        "axis_relation": "",
        "layer": meta.get("layer") or meta.get("capa") or "",
        "submodule": meta.get("submodule") or meta.get("submodulo") or "",
        "lesson_title": meta.get("lesson_title") or "",
        "topic": meta.get("topic") or meta.get("tema") or "",
        "resource_title": meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso") or "",
        "url": meta.get("url") or meta.get("url_video") or "",
        "score": round(float(score or 0), 4)
    }
    return fuente


def _fuente_a_texto(fuente: dict):
    partes = [
        f"Fuente {fuente.get('index')}",
        f"origen: {fuente.get('origin')}",
        f"archivo: {fuente.get('filename')}",
        f"score: {float(fuente.get('score') or 0):.2f}"
    ]
    for key, label in [
        ("doc_type", "tipo"),
        ("page", "pagina"),
        ("start_time", "inicio"),
        ("end_time", "fin"),
        ("url", "url"),
    ]:
        value = fuente.get(key)
        if value not in ("", None):
            suffix = "s" if key in ("start_time", "end_time") else ""
            partes.append(f"{label}: {value}{suffix}")
    return " | ".join(partes)


def _chunks_desde_evidencias(evidencias: list):
    chunks = []
    for index, item in enumerate(evidencias or [], start=1):
        meta = item["document"].metadata or {}
        fuente = _formatear_fuente(meta, item.get("score", 0), index)
        fuente["axis_relation"] = item.get("axis_relation", "")
        chunks.append(fuente)
    return chunks


def _construir_contexto_evidencia(evidencias: list):
    texto_crudo = ""
    fuentes = []

    for index, item in enumerate(evidencias, start=1):
        doc = item["document"]
        score = item["score"]
        meta = doc.metadata or {}
        fuente = _formatear_fuente(meta, score, index)
        fuente["axis_relation"] = item.get("axis_relation", "")
        fuentes.append(fuente)

        texto_crudo += f"[{_fuente_a_texto(fuente)}]\n"
        texto_crudo += f"{doc.page_content}\n"

        objetivo = meta.get("learning_objective")
        recurso = meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso")
        recurso_tipo = meta.get("resource_type")
        video = meta.get("url") or meta.get("url_video")
        start_time = meta.get("start_time")
        end_time = meta.get("end_time")
        page = meta.get("page")

        if objetivo:
            texto_crudo += f"OBJETIVO DE APRENDIZAJE: {objetivo}\n"

        tiene_ubicacion_validable = (
            page not in ("", None)
            or start_time not in ("", None)
            or video not in ("", None)
        )
        if tiene_ubicacion_validable:
            texto_crudo += "UBICACION DOCUMENTAL VALIDADA: "
            if recurso and not _recurso_es_generico(meta):
                texto_crudo += f"{recurso} "
            if recurso_tipo:
                texto_crudo += f"(tipo: {recurso_tipo}) "
            if page not in ("", None):
                texto_crudo += f"(pagina: {page}) "
            if start_time not in ("", None):
                texto_crudo += f"(inicio: {start_time}s) "
            if end_time not in ("", None):
                texto_crudo += f"(fin: {end_time}s) "
            if video:
                texto_crudo += f"(Video: {video}) "
        texto_crudo += "\n\n"

    teoria = texto_crudo[:4500] + "..." if len(texto_crudo) > 4500 else texto_crudo
    return teoria, fuentes


def _formatear_segundos(segundos):
    if segundos in ("", None):
        return ""
    try:
        segundos = int(segundos)
    except Exception:
        return str(segundos)
    minutos = segundos // 60
    resto = segundos % 60
    return f"{minutos}:{resto:02d}"


def _recurso_es_generico(meta: dict):
    recurso = _normalizar_texto(meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso") or "")
    filename = _normalizar_texto(os.path.splitext(meta.get("filename") or os.path.basename(meta.get("source", "")))[0])
    return not recurso or recurso == filename


def _meta_tiene_ubicacion_validada(meta: dict):
    if meta.get("page") not in ("", None):
        return True
    if meta.get("start_time") not in ("", None):
        return True
    if meta.get("url") not in ("", None) or meta.get("url_video") not in ("", None):
        return True
    return False


def _formatear_fuente_lookup(meta: dict):
    """Formatea una fuente para respuesta lookup: solo datos concretos, cero relleno."""
    lineas = []
    recurso = meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso") or ""
    clase = meta.get("lesson_title") or meta.get("topic") or meta.get("tema") or ""
    axis = meta.get("axis") or meta.get("eje") or meta.get("module") or meta.get("modulo") or ""
    submodulo = meta.get("submodule") or meta.get("submodulo") or ""
    page = meta.get("page")
    start_time = meta.get("start_time")
    end_time = meta.get("end_time")
    url = meta.get("url") or meta.get("url_video") or ""
    filename = meta.get("filename") or os.path.basename(meta.get("source", "")) or ""
    doc_type = meta.get("doc_type") or "documento"

    if recurso and not _recurso_es_generico(meta):
        lineas.append(f"  - Recurso: {recurso}")
    if clase:
        lineas.append(f"  - Clase/tema: {clase}")
    if axis:
        detalle = f"Eje {axis}"
        if submodulo:
            detalle += f", submodulo {submodulo}"
        lineas.append(f"  - Ubicacion: {detalle}")
    if start_time not in ("", None):
        tiempo = _formatear_segundos(start_time)
        cierre = f"  - Minuto: {tiempo}"
        if end_time not in ("", None):
            cierre += f" a {_formatear_segundos(end_time)}"
        lineas.append(cierre)
    if page not in ("", None):
        lineas.append(f"  - Pagina: {page}")
    lineas.append(f"  - Archivo: {filename} ({doc_type})")
    if url:
        lineas.append(f"  - Enlace: {url}")
    return lineas


def _formatear_documento_oficial_lookup(meta: dict):
    filename = meta.get("filename") or os.path.basename(meta.get("source", "")) or "archivo sin nombre"
    doc_type = meta.get("doc_type") or "documento"
    topic = meta.get("topic") or meta.get("tema") or ""
    axis = meta.get("axis") or meta.get("eje") or meta.get("module") or meta.get("modulo") or ""

    lineas = [f"  - Documento: {filename} ({doc_type})"]
    if axis:
        lineas.append(f"  - Eje: {axis}")
    if topic:
        lineas.append(f"  - Contenido asociado: {topic}")
    return lineas


def _respuesta_lookup(pregunta: str, evidencias: list):
    if not evidencias:
        return (
            "No encontre ubicaciones oficiales validadas ni documentos oficiales indexados para esa consulta. "
            "Prueba indicando el concepto exacto o eje."
        )

    pregunta_limpia = _normalizar_texto(pregunta)
    _, tokens_concepto = _extraer_frases_lookup(pregunta)
    if not tokens_concepto and ("esto" in pregunta_limpia or "eso" in pregunta_limpia):
        return "Necesito una precision minima: sobre que concepto quieres que busque recurso, clase, minuto o PDF?"

    preferir_pdf = "pdf" in pregunta_limpia or "pagina" in pregunta_limpia
    preferir_minuto = "minuto" in pregunta_limpia
    preferir_recurso = "recurso" in pregunta_limpia

    ubicaciones_validadas = [
        item for item in evidencias
        if _meta_tiene_ubicacion_validada(item["document"].metadata or {})
    ]
    usando_ubicaciones = bool(ubicaciones_validadas)

    candidatos = ubicaciones_validadas if usando_ubicaciones else evidencias
    if preferir_pdf:
        pdfs = [item for item in candidatos if (item["document"].metadata or {}).get("doc_type") == "pdf"]
        if pdfs:
            candidatos = pdfs
    elif preferir_minuto:
        videos = [
            item for item in candidatos
            if (item["document"].metadata or {}).get("start_time") not in ("", None)
        ]
        if videos:
            candidatos = videos
    elif preferir_recurso and usando_ubicaciones:
        recursos = [
            item for item in candidatos
            if not _recurso_es_generico(item["document"].metadata or {})
        ]
        if recursos:
            candidatos = recursos

    vistos_files = set()
    fuentes_unicas = []
    for item in candidatos:
        meta = item["document"].metadata or {}
        fn = meta.get("filename") or os.path.basename(meta.get("source", ""))
        clave = f"{fn}::{meta.get('page', '')}::{meta.get('start_time', '')}"
        if clave in vistos_files:
            continue
        vistos_files.add(clave)
        fuentes_unicas.append(item)
        if len(fuentes_unicas) >= 3:
            break

    if usando_ubicaciones:
        if len(fuentes_unicas) == 1:
            lineas = ["Encontre esta ubicacion validada en el material del curso:"]
            lineas.extend(_formatear_fuente_lookup(fuentes_unicas[0]["document"].metadata or {}))
        else:
            lineas = [f"Encontre {len(fuentes_unicas)} ubicaciones validadas en el material del curso:"]
            for idx, item in enumerate(fuentes_unicas, 1):
                meta = item["document"].metadata or {}
                lineas.append(f"")
                lineas.append(f"**Ubicacion {idx}:**")
                lineas.extend(_formatear_fuente_lookup(meta))
    else:
        lineas = [
            "No hay ubicaciones oficiales validadas para esta consulta: no tengo pagina, minuto, URL ni recurso aprobado.",
            "Lo que si hay son documentos oficiales indexados que puedes revisar:"
        ]
        for idx, item in enumerate(fuentes_unicas, 1):
            meta = item["document"].metadata or {}
            lineas.append("")
            lineas.append(f"**Documento {idx}:**")
            lineas.extend(_formatear_documento_oficial_lookup(meta))

    return "\n".join(lineas)


def _respuesta_sin_evidencia(state: EstadoAgente):
    if state.get("imagen"):
        detalle = "La captura ayuda, pero necesito que precises el eje, clase, recurso o la parte concreta del DAW/plugin que quieres analizar."
    else:
        detalle = "Puedes precisar el eje, clase, recurso o subir una captura relacionada para buscar mejor en la base del curso."

    return (
        "No tengo suficiente respaldo en el material cargado del curso para responder eso con seguridad. "
        "Prefiero no inventar una explicacion que pueda confundirte. "
        f"{detalle}"
    )


def _query_retrieval_con_aliases(pregunta: str):
    pregunta_norm = _normalizar_texto(pregunta)
    concepto_directo = _concepto_definicion_directa(pregunta)

    if concepto_directo == "factor q" or (
        "factor q" not in pregunta_norm
        and f" q " in f" {pregunta_norm} "
        and any(patron in pregunta_norm for patron in ["que es", "que significa", "define"])
    ):
        return f"factor q. Pregunta original: {pregunta}"

    if (
        ("comprim" in pregunta_norm or "compres" in pregunta_norm)
        and (
            "ecualizador" in pregunta_norm
            or "ecualizacion" in pregunta_norm
            or " eq " in f" {pregunta_norm} "
        )
    ):
        return (
            "compresion multibanda ecualizacion dinamica compresor ecualizador "
            f"Pregunta original: {pregunta}"
        )

    return pregunta


def _preparar_retrieval(state: EstadoAgente):
    pregunta = state["pregunta"].strip()
    contexto_leccion = state.get("contexto_leccion", "").strip()
    historial = state.get("historial", [])
    pregunta_limpia = _normalizar_texto(pregunta)

    # Vertical slice piloto: si hay un bloque activo, el referente
    # ambiguo ("eso", "esto", "aqui") ya esta resuelto por el bloque.
    # Expandimos la query con el titulo del bloque y saltamos los gates
    # de aclaracion para no perder el contexto que ya viaja en el envelope.
    envelope = state.get("tutor_envelope")
    pilot_block = getattr(envelope, "pilot_block", None) if envelope else None
    if pilot_block:
        if not _es_pregunta_ambigua(pregunta):
            return _query_retrieval_con_aliases(pregunta), False, ""
        lesson = getattr(envelope, "pilot_lesson", None) or {}
        concepts = ", ".join(pilot_block.get("concepts") or [])
        referente = ". ".join([
            lesson.get("lesson_title", ""),
            pilot_block.get("block_title", ""),
            concepts,
            pilot_block.get("summary", ""),
        ]).strip(". ")
        if referente:
            return f"{pregunta}. Contexto activo: {referente}"[:500], False, ""

    if "espuma" in pregunta_limpia and "interfaz" in pregunta_limpia:
        return (
            "",
            True,
            "Necesito una aclaracion breve para no inventar: cuando dices interfaz, te refieres a interfaz de audio, interfaz del software o a otro contexto?"
        )

    if (
        "audio" in pregunta_limpia
        and "procesad" in pregunta_limpia
        and ("ecualiz" in pregunta_limpia or " eq " in f" {pregunta_limpia} ")
    ):
        return (
            "",
            True,
            "Cuando dices audios ya procesados, te refieres a una mezcla/master terminado, stems exportados o pistas con efectos impresos? Con eso te digo si conviene ecualizar y con que cautela."
        )

    if _es_pregunta_lookup(pregunta):
        _, tokens_concepto = _extraer_frases_lookup(pregunta)
        if not tokens_concepto and ("esto" in pregunta_limpia or "eso" in pregunta_limpia):
            return "", True, "Sobre que concepto quieres que busque documentos oficiales, recurso, pagina o minuto?"
        return _query_retrieval_con_aliases(pregunta), False, ""

    if _es_pregunta_ambigua(pregunta):
        query_contextual, aclaracion = _reescribir_query_contextual(pregunta, historial, contexto_leccion)
        if not query_contextual:
            return "", True, aclaracion
        return query_contextual, False, ""

    if not pregunta and state.get("imagen"):
        return (
            contexto_leccion
            or "captura DAW plugin mezcla masterizacion ecualizacion compresion niveles medidores"
        ), False, ""

    return _query_retrieval_con_aliases(pregunta), False, ""


def _debe_incluir_historial_en_prompt(pregunta: str, query_retrieval: str):
    if query_retrieval != pregunta:
        return False

    if not _es_pregunta_ambigua(pregunta) and (
        _tiene_termino_tecnico_curso(pregunta)
        or _es_pregunta_conceptual_directa(pregunta)
        or _es_pregunta_comparativa_multiconcepto(pregunta)
    ):
        return False

    return True


def _intent_efectivo_para_prompt(state: EstadoAgente, pregunta: str, referente_resuelto: bool):
    intent_original = state.get("intent") or "aclaracion_concepto"
    if intent_original != "ambigua" or not referente_resuelto:
        return intent_original

    pregunta_norm = _normalizar_texto(pregunta)
    claves_diagnostico = [
        "problema", "reviso", "corrijo", "pierde", "perdio", "satura",
        "aplica igual", "cualquier plugin", "por que", "porque"
    ]
    if any(clave in pregunta_norm for clave in claves_diagnostico):
        return "diagnostico_tecnico"
    return "aclaracion_concepto"
