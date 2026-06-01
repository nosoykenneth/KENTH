from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
import concurrent.futures

from models.schemas import EstadoAgente
from config import TEXT_MODEL, VISION_MODEL
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
            best_score = evidencias_imagen[0]["score"]
            evidence_level = "alto" if best_score >= 0.65 else "medio"

            instrucciones_vision = (
                "Eres KENTH, ingeniero de mezcla profesional y tutor.\n"
                "El alumno adjunto una imagen. Analizala cuidadosamente.\n\n"
                f"{_prompt_por_intent('retroalimentacion_visual')}"
                "REGLAS ESTRICTAS:\n"
                "1. La imagen ya fue clasificada como relacionada con audio. Describe solo lo visible: interfaz, controles, medidores, forma de onda o plugin.\n"
                "2. No infieras como suena. Una captura no permite saber si algo suena bien o mal.\n"
                "3. Usa EVIDENCIA DEL CURSO solo si conecta claramente con lo visible. Si no conecta, no fuerces teoria.\n"
                "4. NO des parametros exactos, valores en dB, presets ni diagnosticos auditivos sin audio.\n"
                "5. Recomienda recursos, software o plugins solo si aparecen en la evidencia o en la pregunta.\n"
                "6. Prohibido mencionar Ableton, Logic, Serum u otros nombres propios si no aparecen en evidencia o pregunta.\n"
                "7. Si no estas seguro de lo que se ve, pide una aclaracion breve.\n\n"
                f"--- EVIDENCIA DEL CURSO ---\n{teoria}\n------------------------\n"
                f"Pregunta del alumno: {pregunta}"
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
            _formatear_fuente(item["document"].metadata or {}, item["score"], index)
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
            "respuesta_final": _respuesta_sin_evidencia(state),
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

    evidencias_para_respuesta = _ordenar_para_respuesta_directa(evidencias, pregunta)
    teoria, fuentes = _construir_contexto_evidencia(evidencias_para_respuesta)
    best_score = evidencias[0]["score"]
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
    contexto_actual = (
        "--- CONTEXTO ACTUAL DE LA LECCION (NO ES EVIDENCIA RAG) ---\n"
        f"{contexto_leccion}\n"
        "------------------------\n"
        if contexto_leccion else ""
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
    regla_sin_localizacion = (
        "--- LOCALIZACION OFICIAL ---\n"
        "La capa oficial de localizacion (Ejes 0-7) no tiene recursos ni ubicaciones aprobadas por defecto. "
        "Los nombres Fuente/archivo solo indican evidencia recuperada, NO clase, pagina, minuto ni recurso recomendado. "
        "No presentes ubicaciones oficiales si la evidencia no trae pagina, minuto, URL o recurso validado.\n"
        "------------------------\n"
    )

    current_axis = _current_axis_number(state)
    requested_axis = _question_axis_number(pregunta)
    future_axis_question = _is_future_axis_question(state, pregunta)
    regla_curricular = (
        "--- POLITICA CURRICULAR Y FUENTES ---\n"
        "Todo lo que uses para responder debe venir de una de estas categorias: "
        "A) EVIDENCIA DEL CURSO recuperada por RAG; "
        "B) CONTEXTO RUNTIME inyectado en este turno; "
        "C) reglas del sistema/prompt/routing.\n"
        "Jerarquia pedagogica: bloque activo = punto de partida; leccion actual = contexto inmediato; "
        "ejes previos = soporte permitido; eje actual completo = expansion natural.\n"
        "El contexto runtime orienta donde esta el alumno, pero no convierte por si solo una afirmacion tecnica "
        "en evidencia documental del curso.\n"
        "Puedes salir del bloque activo cuando la pregunta lo necesite, siempre anclando la respuesta al punto actual "
        "y usando evidencia RAG o contexto runtime explicito.\n"
    )
    if current_axis is not None:
        regla_curricular += f"Eje actual del alumno: Eje {current_axis}.\n"
    if future_axis_question:
        regla_curricular += (
            f"La pregunta apunta a Eje {requested_axis}, que es posterior al eje actual. "
            "Responde solo como anticipo controlado: una orientacion breve, sin clase exhaustiva, "
            "y di explicitamente que se vera mas adelante. No desarrolles procedimientos completos de ese eje. "
            "Maximo 4 frases. No menciones ids internos de bloque/leccion ni digas 'leccion piloto'.\n"
        )
    regla_curricular += "------------------------\n"

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
        "Eres KENTH, tutor experto del curso de mezcla y masterizacion.\n"
        "Tu respuesta debe estar basada principalmente en la EVIDENCIA DEL CURSO.\n"
        "Si la evidencia no alcanza para una afirmacion especifica, dilo claramente y no inventes.\n\n"
        "REGLAS ESTRICTAS:\n"
        "1. Dominio cerrado: solo mezcla, masterizacion, audio, DAWs, plugins y material del curso.\n"
        "2. Prioriza la EVIDENCIA DEL CURSO sobre conocimiento general.\n"
        "3. El HISTORIAL ayuda a entender referencias, pero NO justifica hechos tecnicos.\n"
        "4. Si respondes teoria, explica claro y directo.\n"
        "5. Si respondes practica, guia el razonamiento. Evita recetas rigidas sin diagnostico.\n"
        "6. Recomienda recursos, videos, herramientas, software, plugins o tecnicas especificas SOLO si aparecen "
        "literalmente en la evidencia o en la pregunta del alumno.\n"
        "7. Prohibido mencionar Ableton, Logic, Serum u otros nombres propios si no aparecen en evidencia o pregunta.\n"
        "8. Nunca inventes URLs, modulos, ejes, recursos, DAWs, plugins, parametros ni valores en dB.\n"
        "9. Si hay incertidumbre, pide una aclaracion breve.\n"
        "10. Mantente conciso, profesional y pedagogico.\n\n"
        "11. No menciones en la respuesta nombres internos como Fuente 1, score, chunk, archivo, tema o eje "
        "salvo que el alumno pregunte explicitamente donde revisar o pida fuentes. Esos datos ya viajan en el JSON.\n\n"
        f"{_prompt_por_intent(intent_efectivo)}"
        f"{regla_curricular}"
        f"{regla_prioridad_piloto}"
        f"{contexto_actividad}"
        f"{regla_evidence_gate}"
        f"--- EVIDENCIA DEL CURSO ---\n{teoria}\n------------------------\n"
        f"{contexto_actual}"
        f"{historial_formateado}"
        f"{referencia_inferida}"
        f"{regla_referencia_resuelta}"
        f"{regla_definicion_directa}"
        f"{regla_comparacion}"
        f"{regla_sin_localizacion}"
        f"{restriccion_terminos}"
    )

    print("[AGENTE RAG]: Generando respuesta de texto con evidencia del curso...")
    respuesta = llm_logico.invoke(instrucciones + "\nPregunta del alumno: " + pregunta).content

    respuesta = _verificar_respuesta(respuesta, fuentes, evidencias)
    respuesta = _bloquear_localizacion_no_validada(respuesta, fuentes)
    respuesta = _recortar_relleno_sin_evidencia(respuesta)
    respuesta = _limpiar_citas_internas_rag(respuesta)
    if future_axis_question:
        respuesta = _limitar_anticipo_eje_posterior(respuesta, requested_axis)

    print("[AGENTE RAG]: Respuesta generada y verificada.")
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
        evidence_level = "alto" if evidencias[0]["score"] >= 0.65 else "medio"
    else:
        fuentes = []
        evidencia_bloque = (
            "--- EVIDENCIA DEL CURSO ---\n"
            "No hay evidencia suficiente para recomendar una clase, recurso o tecnica especifica.\n"
            "------------------------\n"
        )
        evidence_level = "bajo"

    prompt = (
        "Eres KENTH, tutor del curso de mezcla y masterizacion.\n"
        "El alumno esta confundido o frustrado. Responde como guia pedagogico, no como enciclopedia.\n\n"
        f"{_prompt_por_intent('estudiante_perdido')}"
        "REGLAS:\n"
        "1. Usa exactamente 4 bloques con estos titulos: Validacion, Explicacion simple, Siguiente paso, Pregunta de calibracion.\n"
        "2. Se breve: 1 o 2 frases por bloque.\n"
        "3. Recomienda recursos, software, plugins, DAWs o tecnicas especificas SOLO si aparecen literalmente en la evidencia o pregunta.\n"
        "4. No menciones Ableton, Logic, Serum ni nombres propios si no aparecen en evidencia o pregunta.\n"
        "5. Si no hay evidencia suficiente, guia el proceso sin inventar clase, recurso, timestamp ni parametro.\n\n"
        f"{evidencia_bloque}"
        f"Pregunta/frustracion del alumno: {pregunta}"
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

    query_optimizada = state["pregunta"] + " plugins audio VST mezcla masterizacion"
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
        "Eres el asistente experto del curso de KENTH.\n"
        "Estas en MODO INTERNET: la informacion externa NO reemplaza el material del curso.\n"
        f"{_prompt_por_intent('consulta_externa')}"
        "Usala solo para links, descargas, plugins o informacion externa solicitada.\n"
        "No inventes enlaces y aclara cuando algo viene de informacion externa.\n"
        "No sugieras software, plugins o recursos que no aparezcan en la pregunta o en la informacion web.\n\n"
        f"--- INFO WEB ---\n{info_web}\n----------------\n"
        f"Pregunta original del alumno: {state['pregunta']}"
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
        "respuesta_final": (
            "Solo puedo ayudarte con mezcla, masterizacion, audio, DAWs, plugins y contenido del curso. "
            "Si tu duda esta relacionada con el curso, dime el eje, clase o concepto que quieres revisar."
        ),
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
        respuesta = "De nada. Estoy aqui para ayudarte con mezcla, mastering y el material del curso. Que duda seguimos puliendo?"
    elif "ok" in pregunta or "vale" in pregunta or "perfecto" in pregunta or "entendido" in pregunta:
        respuesta = "Excelente. Sigamos con el curso. Tienes alguna duda puntual de mezcla o masterizacion?"
    elif "adios" in pregunta or "chao" in pregunta or "luego" in pregunta:
        respuesta = "Hasta luego. Cuando vuelvas, puedo ayudarte a revisar conceptos, plugins o ejercicios del curso."
    else:
        respuesta = "Hola. Soy KENTH, tu tutor de mezcla y masterizacion. En que parte del curso necesitas ayuda?"

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
