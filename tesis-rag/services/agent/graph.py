from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
import concurrent.futures

from models.schemas import EstadoAgente
from config import TEXT_MODEL, VISION_MODEL
from services.domain import get_domain_pack
from services.agent.prompts import _campos_pedagogicos, _prompt_por_intent
from services.agent.routing import (
    _conceptos_relevantes_pregunta,
    _es_pregunta_ambigua,
    _es_pregunta_lookup,
    _formatear_historial,
    _normalizar_texto,
    _respuesta_aclaracion_ambigua,
    _warning,
    configure_routing,
    nodo_supervisor,
)
from services.agent.retrieval import (
    _buscar_evidencia,
    _buscar_evidencia_lookup,
    _chunks_desde_evidencias,
    _concepto_definicion_directa,
    _construir_contexto_evidencia,
    _current_axis_number,
    _debe_incluir_historial_en_prompt,
    _es_pregunta_comparativa_multiconcepto,
    _formatear_fuente,
    _intent_efectivo_para_prompt,
    _is_future_axis_question,
    _question_axis_number,
    _ordenar_para_respuesta_directa,
    _preparar_retrieval,
    _respuesta_fuera_de_material,
    _respuesta_lookup,
    _respuesta_sin_evidencia,
    _terminos_especificos_no_soportados,
)
from services.agent.vision import (
    _imagen_parece_audio,
    _limpiar_imagen_base64,
    _responder_imagen_audio_sin_evidencia,
)
from services.agent.verification import (
    _bloquear_localizacion_no_validada,
    _limpiar_citas_internas_rag,
    _limitar_anticipo_eje_posterior,
    _recortar_relleno_sin_evidencia,
    _respuesta_conceptual_controlada,
    _verificar_respuesta,
)

# ==========================================
# 1. INICIALIZACION DE MODELOS
# ==========================================
llm_logico = ChatOllama(model=TEXT_MODEL, temperature=0.2)
llm_vision = ChatOllama(model=VISION_MODEL, temperature=0.1)
buscador_web = DuckDuckGoSearchRun()


# ==========================================
# PROMPTS DE NODO (DOMINIO) — Fase 0
# ==========================================
# La persona y los prompts de nodo viven en el Domain Pack (datos en
# domain_packs/<course_id>.json), no aqui. _PACK resuelve el curso por defecto
# para el piloto mono-curso; la resolucion por course_id en runtime es Fase 1.
_PACK = get_domain_pack()

RAG_SYSTEM_PROMPT = _PACK.node_prompt("rag_system")
VISION_RAG_INTRO = _PACK.node_prompt("vision_rag_intro")
VISION_RAG_RULES = _PACK.node_prompt("vision_rag_rules")
LOST_INTRO = _PACK.node_prompt("lost_intro")
LOST_RULES = _PACK.node_prompt("lost_rules")
WEB_QUERY_SUFFIX = _PACK.node_prompt("web_query_suffix")
WEB_INTRO = _PACK.node_prompt("web_intro")
WEB_RULES = _PACK.node_prompt("web_rules")
GUARD_REPLY = _PACK.node_prompt("guard_reply")
GREETINGS = _PACK.greetings()


def _bool_fuente(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "si", "sí"}
    return bool(value)


def _fuente_titulo(fuente: dict):
    return (
        fuente.get("title")
        or fuente.get("resource_title")
        or fuente.get("filename")
        or "recurso"
    )


def _fuente_descripcion(fuente: dict):
    return (
        fuente.get("description")
        or fuente.get("topic")
        or fuente.get("lesson_title")
        or ""
    )


def _fuente_contextual_suficiente(fuente: dict):
    if not isinstance(fuente, dict):
        return False
    relation = fuente.get("context_relation")
    if relation not in {"same_lesson", "same_section", "same_axis"}:
        return False
    return bool(
        _fuente_titulo(fuente)
        and (
            _fuente_descripcion(fuente)
            or fuente.get("resource_type")
            or fuente.get("media_type")
        )
    )


def _fuente_es_recurso_descargable(fuente: dict):
    return (fuente.get("media_type") or "") in {"audio", "template", "file"} or bool(fuente.get("source", "").startswith("resource:"))


def _regla_resource_type(fuente: dict):
    resource_type = (fuente.get("resource_type") or "").strip().lower()
    media_type = (fuente.get("media_type") or "").strip().lower()
    visible = fuente.get("visible_to_student") is True or _bool_fuente(fuente.get("visible_to_student"))
    titulo = _fuente_titulo(fuente)
    descripcion = _fuente_descripcion(fuente)

    lineas = [
        f"- Fuente {fuente.get('index')}: {titulo}",
        f"  scope={fuente.get('scope') or ''}; relation={fuente.get('context_relation') or ''}; "
        f"resource_type={resource_type or ''}; media_type={media_type or ''}; "
        f"lesson_id={fuente.get('lesson_id') or ''}; moodle_section_id={fuente.get('moodle_section_id') or ''}; "
        f"axis_id={fuente.get('axis_id') or ''}.",
    ]
    if descripcion:
        lineas.append(f"  descripcion usable: {descripcion}")

    if resource_type == "daw_template" or media_type == "template":
        lineas.append(
            "  regla: tratalo como plantilla/proyecto DAW descargable para practicar; "
            "no intentes leer ni interpretar el archivo binario. Usa titulo, descripcion y contexto de leccion."
        )
    elif resource_type == "audio_practice" or media_type == "audio":
        lineas.append(
            "  regla: explica para que practica auditiva sirve segun su descripcion; no finjas que escuchaste el audio."
        )
    elif resource_type in {"pdf_reading", "theory"} or media_type == "document":
        lineas.append("  regla: usalo como apoyo conceptual o lectura de teoria.")
    elif resource_type == "exercise":
        lineas.append("  regla: explica que debe hacer el alumno y cual es el siguiente paso practico.")
    elif resource_type in {"solution", "rubric"}:
        lineas.append("  regla: usalo con cuidado como criterio interno; no reveles literalmente si no es visible.")

    if _fuente_es_recurso_descargable(fuente):
        if visible:
            lineas.append("  visibilidad: puedes decir que el alumno puede abrirlo o descargarlo.")
        else:
            lineas.append("  visibilidad: NO ofrezcas descarga ni enlace; usalo solo como conocimiento textual.")
    return "\n".join(lineas)


def _bloque_uso_evidencia(fuentes: list, state: EstadoAgente):
    fuentes = [f for f in fuentes or [] if isinstance(f, dict)]
    top = fuentes[:4]
    if not top:
        return "", {
            "downloadable_resource_rule": False,
            "context_jump_rule": False,
            "contextual_resource_sufficient": False,
            "missing_evidence_rule": True,
        }

    contextual_sufficient = any(_fuente_contextual_suficiente(f) for f in top)
    downloadable = any(_fuente_es_recurso_descargable(f) for f in top)
    context_jump = any(f.get("context_relation") in {"other_section", "other_axis"} for f in top)
    weak_generic = not contextual_sufficient and all(
        f.get("context_relation") in {"global", "unknown", ""} for f in top
    )

    lineas = [
        "--- POLITICA DE USO DE EVIDENCIA CONTEXTUAL ---",
        f"Curso actual: {state.get('course_id') or ''}.",
        f"Seccion/Tema actual: {state.get('current_section_name') or state.get('moodle_section_id') or ''}.",
        f"Leccion actual: {state.get('current_lesson_id') or ''}.",
        "Usa esta politica para decidir el tono de certeza y el tipo de respuesta.",
    ]

    if contextual_sufficient:
        lineas.append(
            "Hay evidencia contextual suficiente de la leccion/seccion actual. "
            "NO abras con 'no hay suficiente contexto/evidencia'. Responde directamente con lo que si se sabe; "
            "si falta un detalle, cierra con una pregunta especifica."
        )
    elif weak_generic:
        lineas.append(
            "La evidencia es generica o debil. Si no alcanza, di que no ves ese recurso/concepto en la leccion o seccion actual "
            "y pide el nombre exacto o una coordenada concreta."
        )

    if context_jump:
        lineas.append(
            "Si usas una fuente marcada other_section/other_axis, indica brevemente el salto: pertenece mas a otra seccion/tema que a la seccion actual, "
            "y responde como anticipo corto sin hacerlo pasar como parte de la leccion actual."
        )

    lineas.append("Reglas por fuente:")
    lineas.extend(_regla_resource_type(f) for f in top)
    lineas.append("------------------------\n")

    flags = {
        "downloadable_resource_rule": downloadable,
        "context_jump_rule": context_jump,
        "contextual_resource_sufficient": contextual_sufficient,
        "missing_evidence_rule": weak_generic,
    }
    return "\n".join(lineas), flags


def _respuesta_recurso_contextual_desde_metadata(pregunta: str, fuentes: list, state: EstadoAgente):
    fuente = next((f for f in fuentes or [] if _fuente_contextual_suficiente(f)), None)
    if not fuente:
        return ""

    resource_type = (fuente.get("resource_type") or "").strip().lower()
    media_type = (fuente.get("media_type") or "").strip().lower()
    titulo = _fuente_titulo(fuente)
    descripcion = _fuente_descripcion(fuente)
    relation = fuente.get("context_relation") or ""
    visible = fuente.get("visible_to_student") is True or _bool_fuente(fuente.get("visible_to_student"))
    lesson_id = fuente.get("lesson_id") or state.get("current_lesson_id") or "esta leccion"

    if relation in {"other_section", "other_axis"}:
        axis = fuente.get("current_section_name") or fuente.get("moodle_section_id") or fuente.get("axis_id") or "otra seccion"
        current_axis = state.get("current_section_name") or state.get("moodle_section_id") or state.get("current_axis_id") or "la seccion actual"
        return (
            f"Eso pertenece mas a {axis}; ahora estas en {current_axis}. "
            f"Con esa salvedad: {titulo} se debe leer segun su descripcion disponible: {descripcion or 'material recuperado del curso'}."
        )

    if resource_type == "daw_template" or media_type == "template":
        base = (
            f"{titulo} es una plantilla/proyecto DAW de {lesson_id}. "
            "Te sirve como base de practica para trabajar sin armar la sesion desde cero. "
            "No interpreto el archivo binario directamente; me baso en su descripcion y en el contexto de la leccion"
        )
        if descripcion:
            base += f": {descripcion}."
        else:
            base += "."
        if visible:
            base += " Como esta visible para el alumno, puedes abrirla o descargarla desde el recurso."
        return base

    if resource_type == "audio_practice" or media_type == "audio":
        base = (
            f"{titulo} es un recurso de practica auditiva de {lesson_id}. "
            "No puedo fingir que lo escuche; lo explico por su descripcion"
        )
        base += f": {descripcion}." if descripcion else "."
        if visible:
            base += " Si esta disponible en la interfaz, puedes abrirlo para escucharlo y comparar tus decisiones."
        return base

    if resource_type in {"solution", "rubric"} and not visible:
        return (
            f"Puedo usar {titulo} como criterio interno de apoyo, pero no debo revelarlo literalmente ni ofrecer descarga. "
            f"Con lo recuperado, orienta la respuesta segun esta descripcion: {descripcion or 'criterio indexado del curso'}."
        )

    return (
        f"{titulo} es material de apoyo de {lesson_id}. "
        f"Segun la evidencia recuperada, sirve para: {descripcion or 'orientar la practica o el concepto consultado'}."
    )


def _respuesta_menciona_falta_evidencia(respuesta: str):
    norm = _normalizar_texto(respuesta or "")
    marcas = [
        "no hay suficiente contexto",
        "no tengo suficiente contexto",
        "no hay suficiente evidencia",
        "no tengo suficiente evidencia",
        "no tengo evidencia suficiente",
        "no hay respaldo suficiente",
    ]
    return any(marca in norm for marca in marcas)


def _reparar_incertidumbre_recurso_contextual(respuesta: str, pregunta: str, fuentes: list, state: EstadoAgente):
    if not _respuesta_menciona_falta_evidencia(respuesta):
        return respuesta
    reparada = _respuesta_recurso_contextual_desde_metadata(pregunta, fuentes, state)
    if reparada:
        print("[AGENTE RAG]: Reparando incertidumbre generica con metadata contextual suficiente.")
        return reparada
    return respuesta


def _respuesta_sin_evidencia_contextual(state: EstadoAgente):
    lesson = state.get("current_lesson_id") or ""
    axis = state.get("current_section_name") or state.get("current_axis_id") or ""
    if lesson or axis:
        scope = f" en {lesson}" if lesson else ""
        if axis:
            scope += f" del {axis}" if scope else f" en {axis}"
        return (
            f"No veo una fuente relevante{scope} para responder eso con seguridad. "
            "Dame el nombre exacto del recurso o dime si quieres que busque fuera de la leccion actual."
        )
    return _respuesta_sin_evidencia(state)


def nodo_rag(state: EstadoAgente):

    pregunta = state["pregunta"].strip()

    if state.get("imagen"):
        print("[VISION GATE]: Clasificando si la imagen pertenece al dominio de audio...")
        if not _imagen_parece_audio(state["imagen"]):
            print("[VISION GATE]: NO_AUDIO -> bloqueo limpio.")
            return {
                "respuesta_final": "La imagen no parece una captura de audio, DAW, plugin, medidor o forma de onda. Sube una captura relacionada con el curso y dime que quieres revisar.",
                "evidencias": [],
                "evidence_level": "bajo",
                **_campos_pedagogicos(
                    state,
                    answer_type="image_feedback",
                    requires_course_evidence=False,
                    warnings=[
                        _warning("NO_AUDIO_IMAGE", "La imagen no parece relacionada con audio o el curso.")
                    ],
                    retrieved_chunks=[],
                    model_used=VISION_MODEL
                )
            }
        imagen_limpia = _limpiar_imagen_base64(state["imagen"])

        # Hacer retrieval con la pregunta o contexto de leccion para conectar imagen con curso
        query_imagen = pregunta or state.get("contexto_leccion", "").strip() or "captura DAW plugin mezcla masterizacion"
        evidencias_imagen = _buscar_evidencia(query_imagen, state=state)

        if evidencias_imagen:
            print(f"[VISION+RAG]: Imagen AUDIO con {len(evidencias_imagen)} evidencias del curso.")
            teoria, fuentes = _construir_contexto_evidencia(evidencias_imagen)
            best_score = evidencias_imagen[0].get("final_score", evidencias_imagen[0]["score"])
            evidence_level = "alto" if best_score >= 0.65 else "medio"

            instrucciones_vision = (
                VISION_RAG_INTRO
                + f"{_prompt_por_intent('retroalimentacion_visual')}"
                + VISION_RAG_RULES
                + f"--- EVIDENCIA DEL CURSO ---\n{teoria}\n------------------------\n"
                + f"Pregunta del alumno: {pregunta}"
            )
            mensaje = [HumanMessage(content=[
                {"type": "text", "text": instrucciones_vision},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{imagen_limpia}"}
            ])]
            respuesta = llm_vision.bind(options={"repeat_penalty": 1.5}).invoke(mensaje).content
            return {
                "respuesta_final": respuesta,
                "evidencias": fuentes,
                "evidence_level": evidence_level,
                **_campos_pedagogicos(
                    state,
                    answer_type="image_feedback",
                    retrieved_chunks=_chunks_desde_evidencias(evidencias_imagen),
                    model_used=VISION_MODEL
                )
            }
        else:
            print("[VISION+RAG]: Imagen AUDIO sin evidencia suficiente. Respuesta visual limitada.")
            return {
                "respuesta_final": _responder_imagen_audio_sin_evidencia(imagen_limpia, pregunta),
                "evidencias": [],
                "evidence_level": "bajo",
                **_campos_pedagogicos(
                    state,
                    answer_type="image_feedback",
                    warnings=[
                        _warning("LOW_EVIDENCE", "La imagen parece de audio, pero no se recupero evidencia suficiente del curso.")
                    ],
                    retrieved_chunks=[],
                    model_used=VISION_MODEL
                )
            }

    query_retrieval, necesita_aclaracion, aclaracion = _preparar_retrieval(state)
    es_query_seguimiento = ". Pregunta de seguimiento:" in query_retrieval
    referente_ambiguo_resuelto = bool(_es_pregunta_ambigua(pregunta) and query_retrieval and es_query_seguimiento)
    intent_original = state.get("intent") or "aclaracion_concepto"
    intent_efectivo = _intent_efectivo_para_prompt(state, pregunta, referente_ambiguo_resuelto)
    comparacion_multiconcepto = _es_pregunta_comparativa_multiconcepto(pregunta)
    usar_historial_prompt = _debe_incluir_historial_en_prompt(pregunta, query_retrieval)
    print(
        "[CONVERSATION DEBUG]",
        {
            "historial_en_prompt": usar_historial_prompt,
            "referente_ambiguo_resuelto": referente_ambiguo_resuelto,
            "intent_original": intent_original,
            "intent_efectivo": intent_efectivo,
            "comparacion_multiconcepto": comparacion_multiconcepto,
            "query_retrieval": query_retrieval
        }
    )

    if necesita_aclaracion:
        print("[AGENTE RAG]: Pregunta ambigua sin contexto suficiente.")
        return {
            "respuesta_final": aclaracion or _respuesta_aclaracion_ambigua(),
            "evidencias": [],
            "evidence_level": "bajo",
            **_campos_pedagogicos(
                state,
                intent="ambigua",
                answer_type="clarification",
                requires_course_evidence=False,
                warnings=[
                    _warning("AMBIGUOUS_REFERENCE", "La pregunta depende de un referente no claro.")
                ],
                retrieved_chunks=[],
                model_used="none"
            )
        }

    if _es_pregunta_lookup(pregunta):
        print("[AGENTE RAG]: Intencion lookup detectada. Priorizando metadatos concretos.")
        evidencias_lookup = _buscar_evidencia_lookup(query_retrieval, state=state)
        fuentes_lookup = [
            _formatear_fuente(item["document"].metadata or {}, item["score"], index, item)
            for index, item in enumerate(evidencias_lookup, start=1)
        ]
        return {
            "respuesta_final": _respuesta_lookup(pregunta, evidencias_lookup),
            "evidencias": fuentes_lookup,
            "evidence_level": "metadata" if evidencias_lookup else "bajo",
            **_campos_pedagogicos(
                state,
                intent="busqueda_fuente",
                answer_type="source_lookup",
                retrieved_chunks=fuentes_lookup,
                warnings=[] if evidencias_lookup else [
                    _warning("NO_COURSE_SOURCE", "No se encontro una fuente concreta en los metadatos indexados.")
                ],
                model_used="none"
            )
        }

    evidencias = _buscar_evidencia(query_retrieval, state=state)

    if not evidencias:
        print("[AGENTE RAG]: Evidencia insuficiente. Respuesta segura sin invencion.")
        return {
            "respuesta_final": _respuesta_sin_evidencia_contextual(state),
            "evidencias": [],
            "evidence_level": "bajo",
            **_campos_pedagogicos(
                state,
                intent=intent_efectivo,
                answer_type="needs_more_context",
                warnings=[
                    _warning("NO_COURSE_SOURCE", "No se encontro respaldo suficiente en el material cargado.")
                ],
                retrieved_chunks=[],
                model_used="none"
            )
        }

    terminos_no_soportados = _terminos_especificos_no_soportados(pregunta, evidencias)
    if terminos_no_soportados and not state.get("imagen"):
        print(f"[AGENTE RAG]: Terminos especificos sin respaldo: {terminos_no_soportados}")
        return {
            "respuesta_final": _respuesta_fuera_de_material(terminos_no_soportados),
            "evidencias": [],
            "evidence_level": "bajo",
            **_campos_pedagogicos(
                state,
                intent="fuera_dominio",
                answer_type="out_of_domain",
                requires_course_evidence=False,
                warnings=[
                    _warning("NO_COURSE_SOURCE", "La consulta contiene terminos especificos no respaldados por el curso.")
                ],
                retrieved_chunks=[],
                model_used="none"
            )
        }

    print(f"[AGENTE RAG]: Evidencias aceptadas: {len(evidencias)}")

    evidencias_para_respuesta = _ordenar_para_respuesta_directa(evidencias, pregunta, state)
    teoria, fuentes = _construir_contexto_evidencia(evidencias_para_respuesta)
    politica_evidencia, evidence_policy_flags = _bloque_uso_evidencia(fuentes, state)
    print("[EVIDENCE POLICY DEBUG]", evidence_policy_flags)
    best_score = evidencias[0].get("final_score", evidencias[0]["score"])
    evidence_level = "alto" if best_score >= 0.65 else "medio"

    respuesta_controlada = _respuesta_conceptual_controlada(pregunta)
    if respuesta_controlada:
        print("[AGENTE RAG]: Respuesta conceptual controlada aplicada.")
        return {
            "respuesta_final": respuesta_controlada,
            "evidencias": fuentes,
            "evidence_level": evidence_level,
            **_campos_pedagogicos(
                state,
                intent="aclaracion_concepto",
                answer_type="rag_answer",
                retrieved_chunks=_chunks_desde_evidencias(evidencias_para_respuesta),
                warnings=[] if evidence_level == "alto" else [
                    _warning("LOW_EVIDENCE", "La evidencia recuperada tiene relevancia moderada.")
                ],
                model_used="none"
            )
        }

    historial_formateado = (
        _formatear_historial(state.get("historial", []))
        if usar_historial_prompt else ""
    )
    contexto_leccion = state.get("contexto_leccion", "").strip()
    # Dedupe (B4): si ya existe el bloque de contexto estructurado del backend
    # (activity_context_block, mas rico y exacto), no inyectamos ademas el string
    # de contexto del frontend — evita la doble inyeccion del mismo contexto.
    # Fuera de leccion (sin bloque estructurado) se mantiene como fallback.
    contexto_actual = (
        "--- CONTEXTO ACTUAL DE LA LECCION (NO ES EVIDENCIA RAG) ---\n"
        f"{contexto_leccion}\n"
        "------------------------\n"
        if contexto_leccion and not state.get("activity_context_block") else ""
    )
    # Capa 2/3 del tutor contextual: bloque pre-renderizado por
    # services.context_service. No contamina retrieval, solo orienta.
    activity_context_block = state.get("activity_context_block", "")
    contexto_actividad = f"{activity_context_block}\n" if activity_context_block else ""
    referencia_inferida = (
        f"Referencia contextual inferida para buscar: {query_retrieval}\n"
        if es_query_seguimiento else (
            f"Consulta expandida para busqueda: {query_retrieval}\n"
            if query_retrieval != pregunta else ""
        )
    )
    referencia_resuelta = (
        query_retrieval.split(". Pregunta de seguimiento:", 1)[0].strip()
        if es_query_seguimiento else ""
    )
    regla_referencia_resuelta = (
        "--- REFERENCIA CONTEXTUAL VALIDADA ---\n"
        f"La pregunta corta se refiere solo a: {referencia_resuelta}.\n"
        "No cambies a otro concepto del historial. No mezcles con otros temas mencionados antes.\n"
        "Si la evidencia recuperada no respalda esa referencia, pide aclaracion en una frase.\n"
        "------------------------\n"
        if referencia_resuelta else ""
    )
    restriccion_terminos = (
        "Terminos de la pregunta sin respaldo directo en evidencia: "
        f"{', '.join(terminos_no_soportados)}. No los expliques; limitate a describir lo observable o pide aclaracion.\n"
        if terminos_no_soportados else ""
    )
    concepto_directo = _concepto_definicion_directa(pregunta)
    regla_definicion_directa = (
        "--- DEFINICION DIRECTA ---\n"
        f"El alumno pregunta que es: {concepto_directo}.\n"
        "Responde primero con la definicion directa de ese concepto usando la evidencia mas relevante. "
        "No empieces con conceptos vecinos como EQ correctiva/tonal salvo que el alumno los pregunte.\n"
        "Mantenerlo breve: definicion directa y una nota practica corta, sin repetir la misma idea.\n"
        "------------------------\n"
        if concepto_directo else ""
    )
    conceptos_comparacion = _conceptos_relevantes_pregunta(pregunta) if comparacion_multiconcepto else []
    regla_comparacion = (
        "--- COMPARACION MULTI-CONCEPTO ---\n"
        f"El alumno pide comparar: {', '.join(conceptos_comparacion)}.\n"
        "Responde en formato breve y ordenado: una linea por concepto y una frase final con la diferencia principal. "
        "No te quedes desarrollando solo uno de los conceptos ni arrastres el subtema anterior del historial.\n"
        "------------------------\n"
        if conceptos_comparacion else ""
    )
    current_axis = _current_axis_number(state)
    requested_axis = _question_axis_number(pregunta)
    future_axis_question = _is_future_axis_question(state, pregunta)
    # La politica de fuentes/grounding/ubicaciones vive ahora en RAG_SYSTEM_PROMPT
    # (Domain Pack, reglas 12-13). Aqui solo va lo DINAMICO de este turno: en que
    # seccion esta el alumno y el gate de no-adelantar secciones posteriores.
    regla_curricular = ""
    if current_axis is not None:
        regla_curricular += f"Seccion actual del alumno: Seccion {current_axis} (numerada por orden).\n"
    if future_axis_question:
        regla_curricular += (
            f"La pregunta apunta a Seccion {requested_axis}, que es posterior a la seccion actual. "
            "Responde solo como anticipo controlado: una orientacion breve, sin clase exhaustiva, "
            "y di explicitamente que se vera mas adelante. No desarrolles procedimientos completos de esa seccion. "
            "Maximo 4 frases. No menciones ids internos de bloque/leccion ni digas 'leccion piloto'.\n"
        )
    if regla_curricular:
        regla_curricular = "--- UBICACION CURRICULAR (este turno) ---\n" + regla_curricular + "------------------------\n"

    if evidence_level == "alto":
        regla_evidence_gate = ""
    else:
        regla_evidence_gate = (
            "--- ALERTA DE EVIDENCIA ---\n"
            "La evidencia recuperada tiene relevancia MODERADA (score < 0.65).\n"
            "Esto significa que los fragmentos pueden no ser exactamente sobre lo que pregunta el alumno.\n"
            "REGLAS ADICIONALES para evidencia moderada:\n"
            "- Cinete estrictamente a lo que dice la evidencia. No extrapoles.\n"
            "- Si la evidencia no alcanza para una afirmacion especifica, dilo en una frase.\n"
            "- Prefiere respuestas cortas y cautelosas a explicaciones largas con poca base.\n"
            "- No inventes ejemplos, parametros ni valores que no aparezcan literalmente.\n"
            "------------------------\n"
        )

    # Si llego un bloque activo del video, el orden de prioridad cambia.
    # Primero el bloque (que esta viendo el alumno ahora), luego la
    # metadata de la leccion, luego la evidencia RAG del eje. Esto evita
    # que el RAG general opaque el bloque actual.
    envelope_actual = state.get("tutor_envelope")
    tiene_bloque_activo = bool(getattr(envelope_actual, "active_block", None))

    regla_prioridad_piloto = (
        "--- ORDEN DE PRIORIDAD (BLOQUE ACTIVO) ---\n"
        "1. BLOQUE ACTIVO DEL VIDEO como punto de partida (lo que el alumno esta viendo justo ahora).\n"
        "2. Metadata de la leccion (learning_goal, expected_action).\n"
        "3. EVIDENCIA DEL CURSO (RAG del eje actual y ejes previos) para profundizar conceptos.\n"
        "4. Historial reciente y resto del contexto solo para resolver referencias.\n"
        "Si la pregunta encaja en una de las preguntas probables del bloque, ancla la respuesta a ese bloque. "
        "Puedes apoyarte en otros bloques, la leccion o ejes previos si la pregunta lo exige, "
        "pero senala el puente y no reemplaces el punto actual por una clase lateral.\n"
        "------------------------\n"
        if tiene_bloque_activo else ""
    )

    instrucciones = (
        RAG_SYSTEM_PROMPT
        + f"{_prompt_por_intent(intent_efectivo)}"
        f"{regla_curricular}"
        f"{regla_prioridad_piloto}"
        f"{contexto_actividad}"
        f"{regla_evidence_gate}"
        f"{politica_evidencia}"
        f"--- EVIDENCIA DEL CURSO ---\n{teoria}\n------------------------\n"
        f"{contexto_actual}"
        f"{historial_formateado}"
        f"{referencia_inferida}"
        f"{regla_referencia_resuelta}"
        f"{regla_definicion_directa}"
        f"{regla_comparacion}"
        f"{restriccion_terminos}"
    )

    print("[AGENTE RAG]: Generando respuesta de texto con evidencia del curso...")
    respuesta = llm_logico.invoke(instrucciones + "\nPregunta del alumno: " + pregunta).content

    respuesta = _reparar_incertidumbre_recurso_contextual(respuesta, pregunta, fuentes, state)
    respuesta = _verificar_respuesta(respuesta, fuentes, evidencias)
    respuesta = _bloquear_localizacion_no_validada(respuesta, fuentes)
    respuesta = _recortar_relleno_sin_evidencia(respuesta)
    respuesta = _limpiar_citas_internas_rag(respuesta)
    if future_axis_question:
        respuesta = _limitar_anticipo_eje_posterior(respuesta, requested_axis)

    print("[AGENTE RAG]: Respuesta generada y verificada.")
    policy_warnings = []
    if evidence_policy_flags.get("context_jump_rule"):
        policy_warnings.append(_warning("CONTEXT_JUMP", "La evidencia principal pertenece a otro eje."))
    if evidence_policy_flags.get("downloadable_resource_rule"):
        policy_warnings.append(_warning("DOWNLOADABLE_RESOURCE_POLICY", "Se activo politica de recurso descargable/media."))
    if evidence_policy_flags.get("contextual_resource_sufficient"):
        policy_warnings.append(_warning("CONTEXTUAL_RESOURCE_EVIDENCE", "Hay evidencia contextual suficiente de leccion/eje."))
    return {
        "respuesta_final": respuesta,
        "evidencias": fuentes,
        "evidence_level": evidence_level,
        **_campos_pedagogicos(
            state,
            intent=intent_efectivo,
            answer_type="rag_answer",
            retrieved_chunks=_chunks_desde_evidencias(evidencias_para_respuesta),
            warnings=(
                ([_warning("FUTURE_AXIS_PREVIEW", f"La consulta apunta a Eje {requested_axis}, posterior al eje actual.")]
                 if future_axis_question else [])
                + policy_warnings
                + ([] if evidence_level == "alto" else [
                    _warning("LOW_EVIDENCE", "La evidencia recuperada tiene relevancia moderada.")
                ])
            ),
            model_used=TEXT_MODEL
        )
    }


def nodo_perdido(state: EstadoAgente):
    """Modo guia para estudiantes confundidos o frustrados."""
    print("[MODO GUIA]: Activando respuesta pedagogica para estudiante perdido...")

    pregunta = state["pregunta"].strip()
    query_retrieval = (
        state.get("contexto_leccion", "").strip()
        or pregunta
        or "orientacion estudiante perdido mezcla masterizacion escucha critica"
    )
    evidencias = _buscar_evidencia(query_retrieval, state=state)

    if evidencias:
        teoria, fuentes = _construir_contexto_evidencia(evidencias)
        evidencia_bloque = f"--- EVIDENCIA DEL CURSO ---\n{teoria}\n------------------------\n"
        evidence_level = "alto" if evidencias[0].get("final_score", evidencias[0]["score"]) >= 0.65 else "medio"
    else:
        fuentes = []
        evidencia_bloque = (
            "--- EVIDENCIA DEL CURSO ---\n"
            "No hay evidencia suficiente para recomendar una clase, recurso o tecnica especifica.\n"
            "------------------------\n"
        )
        evidence_level = "bajo"

    prompt = (
        LOST_INTRO
        + f"{_prompt_por_intent('estudiante_perdido')}"
        + LOST_RULES
        + f"{evidencia_bloque}"
        + f"Pregunta/frustracion del alumno: {pregunta}"
    )

    respuesta = llm_logico.invoke(prompt).content
    return {
        "respuesta_final": respuesta,
        "evidencias": fuentes,
        "evidence_level": evidence_level,
        **_campos_pedagogicos(
            state,
            intent="estudiante_perdido",
            answer_type="rag_answer" if fuentes else "needs_more_context",
            retrieved_chunks=_chunks_desde_evidencias(evidencias),
            warnings=[] if fuentes else [
                _warning("LOW_EVIDENCE", "Modo guia activo sin evidencia suficiente para recomendar recurso concreto.")
            ],
            model_used=TEXT_MODEL
        )
    }


def nodo_web(state: EstadoAgente):
    """Busca en DuckDuckGo solo cuando el usuario fuerza modo internet."""
    print("[AGENTE WEB]: Conectando a internet...")

    query_optimizada = state["pregunta"] + WEB_QUERY_SUFFIX
    print(f"[AGENTE WEB]: Buscando en DuckDuckGo: {query_optimizada}")

    info_web = "No se pudo obtener informacion de internet a tiempo o hubo un error de red."
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(buscador_web.invoke, query_optimizada)
            info_web = future.result(timeout=15)
    except concurrent.futures.TimeoutError:
        print("[AGENTE WEB]: Tiempo de espera agotado en DuckDuckGo Search.")
    except Exception as e:
        print(f"[AGENTE WEB]: Error al conectar a internet: {e}")

    prompt = (
        WEB_INTRO
        + f"{_prompt_por_intent('consulta_externa')}"
        + WEB_RULES
        + f"--- INFO WEB ---\n{info_web}\n----------------\n"
        + f"Pregunta original del alumno: {state['pregunta']}"
    )
    respuesta = llm_logico.invoke(prompt).content
    fuente_externa = [{
        "origin": "external",
        "index": 1,
        "filename": "DuckDuckGo Search",
        "doc_type": "web",
        "chunk_id": "",
        "page": None,
        "start_time": None,
        "end_time": None,
        "module": "",
        "submodule": "",
        "lesson_title": "",
        "topic": "busqueda externa",
        "resource_title": "Busqueda web solicitada por el estudiante",
        "url": "",
        "score": None
    }]
    return {
        "respuesta_final": respuesta,
        "evidencias": fuente_externa,
        "evidence_level": "externo",
        **_campos_pedagogicos(
            state,
            intent="consulta_externa",
            answer_type="web_answer",
            requires_course_evidence=False,
            warnings=[
                _warning("EXTERNAL_SOURCE_USED", "Esta respuesta usa busqueda externa y no cuenta como evidencia del curso.")
            ],
            retrieved_chunks=[],
            model_used=TEXT_MODEL
        )
    }


def nodo_guardia(state: EstadoAgente):
    """Rechaza preguntas fuera del dominio del curso sin improvisar."""
    print("[GUARDIA]: Bloqueando pregunta fuera de dominio...")
    return {
        "respuesta_final": GUARD_REPLY,
        "evidencias": [],
        "evidence_level": "bajo",
        **_campos_pedagogicos(
            state,
            intent="fuera_dominio",
            answer_type="out_of_domain",
            requires_course_evidence=False,
            warnings=[
                _warning("OUT_OF_DOMAIN", "La consulta fue clasificada fuera del dominio del curso.")
            ],
            retrieved_chunks=[],
            model_used="none"
        )
    }


def nodo_saludo(state: EstadoAgente):
    """Ruta rapida para saludos y cortesias sin usar LLM."""
    print("[AGENTE SALUDO]: Respondiendo al instante...")
    pregunta = state["pregunta"].lower()

    if "gracias" in pregunta:
        respuesta = GREETINGS["thanks"]
    elif "ok" in pregunta or "vale" in pregunta or "perfecto" in pregunta or "entendido" in pregunta:
        respuesta = GREETINGS["ok"]
    elif "adios" in pregunta or "chao" in pregunta or "luego" in pregunta:
        respuesta = GREETINGS["bye"]
    else:
        respuesta = GREETINGS["default"]

    return {
        "respuesta_final": respuesta,
        "evidencias": [],
        "evidence_level": "bajo",
        **_campos_pedagogicos(
            state,
            intent="saludo",
            answer_type="needs_more_context",
            requires_course_evidence=False,
            retrieved_chunks=[],
            model_used="none"
        )
    }


# ==========================================
# 3. CONSTRUCCION DEL GRAFO
# ==========================================
configure_routing(llm_logico)

flujo = StateGraph(EstadoAgente)

flujo.add_node("supervisor", nodo_supervisor)
flujo.add_node("agente_rag", nodo_rag)
flujo.add_node("agente_web", nodo_web)
flujo.add_node("guardia", nodo_guardia)
flujo.add_node("saludo", nodo_saludo)
flujo.add_node("perdido", nodo_perdido)

flujo.set_entry_point("supervisor")


def enrutador(state: EstadoAgente):
    if state["ruta"] == "internet":
        return "internet"
    return state["ruta"]


flujo.add_conditional_edges(
    "supervisor",
    enrutador,
    {
        "teoria": "agente_rag",
        "internet": "agente_web",
        "bloqueo": "guardia",
        "saludo": "saludo",
        "perdido": "perdido"
    }
)

flujo.add_edge("agente_rag", END)
flujo.add_edge("agente_web", END)
flujo.add_edge("guardia", END)
flujo.add_edge("saludo", END)
flujo.add_edge("perdido", END)

super_agente = flujo.compile()
