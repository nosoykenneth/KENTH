import os
import unicodedata
import re

from models.schemas import EstadoAgente
from services.agent.prompts import _campos_pedagogicos
from services.domain import get_domain_pack

# Fase 0: el conocimiento de dominio se carga del Domain Pack (datos en
# domain_packs/<course_id>.json), no se cablea aqui. _PACK resuelve el curso por
# defecto (KENTH_DEFAULT_COURSE_ID) para el piloto mono-curso; la resolucion por
# course_id en runtime es Fase 1.
_PACK = get_domain_pack()

TEXT_MODEL_NAME = "llama3.2:3b"
llm_logico = None


def configure_routing(model):
    global llm_logico
    llm_logico = model
AMBIGUOUS_MAX_WORDS = 8
SPECIFIC_UNSUPPORTED_TERMS = _PACK.unsupported_terms()
LOOKUP_STOPWORDS = _PACK.lookup_stopwords()
TECHNICAL_CONCEPT_PATTERNS = _PACK.concept_patterns()

COURSE_AXES = _PACK.course_axes()

STRONG_AXIS_TERMS = _PACK.strong_axis_terms()

# Fase 0: el vocabulario de dominio vive en el Domain Pack (datos), no en codigo.
TECHNICAL_WORD_LIST = _PACK.technical_word_list()
DOMAIN_HINT_TERMS = _PACK.domain_hint_terms()
# Seleccion de intent por keyword (ORDENADA: primer match gana).
INTENT_SELECTION_KEYWORDS = _PACK.intent_selection_keywords()


def _normalizar_texto(texto: str):
    texto = (texto or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    for char in ["!", "Â¡", "?", "Â¿", ".", ",", ":", ";"]:
        texto = texto.replace(char, "")
    return texto.strip()


def _eje_fuerte_pregunta(texto: str):
    texto_norm = _normalizar_texto(texto)
    mejor_eje = ""
    mejor_score = 0
    for eje, terminos in STRONG_AXIS_TERMS.items():
        score = 0
        for termino in terminos:
            termino_norm = _normalizar_texto(termino)
            if termino_norm and termino_norm in texto_norm:
                score += 2 if " " in termino_norm else 1
        if score > mejor_score:
            mejor_eje = eje
            mejor_score = score
    return mejor_eje


def _axis_id_meta(meta: dict):
    axis = str(
        meta.get("axis")
        or meta.get("eje")
        or meta.get("axis_id")
        or meta.get("axis_number")
        or meta.get("module_id")
        or ""
    )
    if axis.upper().startswith("EJE"):
        return axis.title()
    if axis.isdigit():
        return f"Eje {axis}"
    source_hint = " ".join([
        meta.get("filename", ""),
        meta.get("source", ""),
    ]).upper()
    filename = (source_hint or os.path.basename(meta.get("source", "")) or "").upper()
    match = re.search(r"EJE\s*(\d+)", filename)
    if not match:
        match = re.search(r"EJE[_\s-]*(\d+)", filename)
    if match:
        return f"Eje {match.group(1)}"
    return ""


def _warning(code: str, message: str):
    return {"code": code, "message": message}


def _inferir_modulo_categoria(pregunta: str, contexto_leccion: str = ""):
    texto = _normalizar_texto(f"{pregunta} {contexto_leccion}")
    eje_fuerte = _eje_fuerte_pregunta(texto)
    if eje_fuerte:
        for eje in COURSE_AXES:
            if eje_fuerte == "Eje 0" and eje["id"] == "eje0_identidad_acustica":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 1" and eje["id"] == "eje1_estructura_flujo":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 2" and eje["id"] == "eje2_espacio_fase":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 3" and eje["id"] == "eje3_identidad_espectral":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 4" and eje["id"] == "eje4_control_dinamico":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 5" and eje["id"] == "eje5_dimension_ambiencia":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 6" and eje["id"] == "eje6_criterio_integracion":
                return eje["id"], eje["evaluation_category"]
            if eje_fuerte == "Eje 7" and eje["id"] == "eje7_optimizacion_entrega":
                return eje["id"], eje["evaluation_category"]

    mejor = None
    mejor_score = 0
    for eje in COURSE_AXES:
        score = 0
        for keyword in eje["keywords"]:
            keyword_norm = _normalizar_texto(keyword)
            if not keyword_norm:
                continue
            if len(keyword_norm) <= 2:
                if keyword_norm in texto.split():
                    score += 1
            elif keyword_norm in texto:
                score += 1
        if score > mejor_score:
            mejor = eje
            mejor_score = score

    if not mejor:
        return "", ""
    return mejor["id"], mejor["evaluation_category"]


def _clasificacion_pedagogica(
    pregunta: str,
    contexto_leccion: str = "",
    tiene_imagen: bool = False,
    ruta_forzada: str = ""
):
    course_module, evaluation_category = _inferir_modulo_categoria(pregunta, contexto_leccion)

    clasificacion = {
        "intent": "aclaracion_concepto",
        "answer_type": "rag_answer",
        "course_module": course_module,
        "evaluation_category": evaluation_category,
        "requires_course_evidence": True
    }

    if ruta_forzada == "internet":
        clasificacion.update({
            "intent": "consulta_externa",
            "answer_type": "web_answer",
            "requires_course_evidence": False
        })
    elif tiene_imagen:
        clasificacion.update({
            "intent": "retroalimentacion_visual",
            "answer_type": "image_feedback",
            "requires_course_evidence": True
        })
    elif _es_estudiante_perdido(pregunta):
        clasificacion.update({
            "intent": "estudiante_perdido",
            "answer_type": "rag_answer",
            "requires_course_evidence": True
        })
    elif _es_pregunta_lookup(pregunta):
        clasificacion.update({
            "intent": "busqueda_fuente",
            "answer_type": "source_lookup",
            "requires_course_evidence": True
        })
    elif _es_pregunta_ambigua(pregunta):
        clasificacion.update({
            "intent": "ambigua",
            "answer_type": "clarification",
            "requires_course_evidence": False
        })
    else:
        texto = _normalizar_texto(pregunta)
        for intent_name, keywords in INTENT_SELECTION_KEYWORDS:
            if any(word in texto for word in keywords):
                clasificacion["intent"] = intent_name
                break

    return clasificacion



def _formatear_historial(historial: list):
    if not historial:
        return ""

    historial_formateado = "--- HISTORIAL RECIENTE (NO ES EVIDENCIA DEL CURSO) ---\n"
    for msg in historial[-4:]:
        rol = "Alumno" if msg.get("role") == "user" else "KENTH"
        contenido = (msg.get("content") or "").strip()
        if contenido:
            historial_formateado += f"{rol}: {contenido}\n"
    historial_formateado += "--------------------------\n"
    return historial_formateado


def _es_estudiante_perdido(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    frases = [
        "no entiendo", "no entendi", "me perdi", "me rindo",
        "estoy perdido", "estoy perdida", "todo me suena igual",
        "no se que hacer", "no se por donde empezar", "explicame desde cero"
    ]
    return any(frase in pregunta_limpia for frase in frases)


def _tiene_termino_tecnico_curso(texto: str):
    texto_limpio = f" {_normalizar_texto(texto)} "
    for _, aliases in TECHNICAL_CONCEPT_PATTERNS:
        for alias in aliases:
            alias_norm = f" {_normalizar_texto(alias)} "
            if alias_norm.strip() and alias_norm in texto_limpio:
                return True

    return any(f" {_normalizar_texto(palabra)} " in texto_limpio for palabra in TECHNICAL_WORD_LIST)


def _es_pregunta_conceptual_directa(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    patrones = [
        "que es", "que significa", "cual es la diferencia", "diferencia entre",
        "es lo mismo", "cuando usar", "cuando se usa", "cuando conviene",
        "conviene usar", "que reviso primero", "que revisar primero",
        "explicame", "hablame de", "cuentame sobre", "cuentame de",
        "por que", "porque", "para que sirve", "sirve", "arregla",
        "revisar en mono", "ya esta bien", "que hace", "que hacen",
        "si ", "debo ", "puedo "
    ]
    return (
        any(pregunta_limpia.startswith(patron) or patron in pregunta_limpia for patron in patrones)
        and _tiene_termino_tecnico_curso(pregunta)
    )


def _es_pregunta_ambigua(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    if not pregunta_limpia:
        return False

    if _es_pregunta_conceptual_directa(pregunta):
        return False

    palabras = pregunta_limpia.split()
    referencias = ["eso", "esto", "ahi", "esa", "ese", "donde", "cual", "cuanto"]
    if _eje_fuerte_pregunta(pregunta) and not any(ref in palabras for ref in referencias):
        return False

    indicadores_directos = [
        "y eso", "eso cuando", "cuando si conviene", "cuando conviene",
        "conviene usarlo", "usarlo", "donde dice eso", "donde dice",
        "donde aparece", "a cuantos db", "cuantos db", "para esto",
        "sobre esto", "esto"
    ]
    pronombres_referenciales = {"eso", "esto", "esa", "ese"}
    if any(ind in pregunta_limpia for ind in indicadores_directos if ind not in pronombres_referenciales):
        return True
    if any(ind in palabras for ind in pronombres_referenciales):
        return True

    indicadores = [
        "cuantos db", "a cuantos db", "cuanto", "donde", "cual",
        "eso", "ahi", "esa", "ese", "como asi"
    ]
    indicadores_frase = {"cuantos db", "a cuantos db", "como asi"}
    indicadores_token = {"cuanto", "donde", "cual"}
    return len(palabras) <= AMBIGUOUS_MAX_WORDS and (
        any(ind in pregunta_limpia for ind in indicadores_frase)
        or any(ind in palabras for ind in indicadores_token)
        or any(ind in palabras for ind in pronombres_referenciales)
    )


def _es_pregunta_lookup(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    if _es_pregunta_conceptual_directa(pregunta):
        return False

    if any(patron in pregunta_limpia for patron in [
        "que es", "por que", "para que", "cuando conviene",
        "diferencia entre", "revisar en mono", "colapsar a mono"
    ]):
        return False

    if any(token in pregunta_limpia.split() for token in ["minuto", "pagina", "pdf"]):
        return True

    patrones = [
        "que recurso", "recurso reviso", "recurso debo",
        "donde explican", "donde se explica", "donde sale", "en que clase", "que clase",
        "en que minuto", "que minuto", "minuto reviso", "que pdf",
        "cual pdf", "pdf tengo", "que pagina", "en que pagina", "pagina reviso",
        "donde puedo repasar", "en que parte", "en que documento", "que documento",
        "cual documento", "muestrame el documento", "muestreme el documento",
        "que video", "que material", "donde esta", "donde encuentro",
        "que tengo que leer", "que tengo que ver", "pasame la fuente",
        "donde se habla", "en que modulo", "que archivo",
        "donde veo", "donde lo veo", "donde aparece", "donde esta eso en el curso",
    ]
    return any(patron in pregunta_limpia for patron in patrones)


def _tokens_lookup(texto: str):
    texto_limpio = _normalizar_texto(texto)
    tokens = []
    for token in texto_limpio.split():
        if token in LOOKUP_STOPWORDS:
            continue
        if len(token) <= 2 and token != "q":
            continue
        tokens.append(token)
    return tokens


def _respuesta_aclaracion_ambigua(referente: str = ""):
    if referente:
        return f"Te refieres a {referente} o a otra parte?"
    return (
        "Necesito una precision minima para no inventar: a que parametro, herramienta o parte de la clase te refieres?"
    )


def _ultimo_mensaje_usuario(historial: list):
    for msg in reversed(historial or []):
        if msg.get("role") == "user":
            contenido = (msg.get("content") or "").strip()
            if contenido:
                return contenido
    return ""


def _ultimo_mensaje_asistente(historial: list):
    for msg in reversed(historial or []):
        if msg.get("role") == "assistant":
            contenido = (msg.get("content") or "").strip()
            if contenido:
                return contenido
    return ""


def _conceptos_en_texto(texto: str):
    texto_limpio = f" {_normalizar_texto(texto)} "
    conceptos = []
    for concepto, aliases in TECHNICAL_CONCEPT_PATTERNS:
        for alias in aliases:
            alias_norm = _normalizar_texto(alias).strip()
            if not alias_norm:
                continue
            if len(alias_norm) <= 2:
                aparece = f" {alias_norm} " in texto_limpio
            else:
                aparece = alias_norm in texto_limpio.strip()
            if aparece:
                conceptos.append(concepto)
                break

    if "compresion multibanda" in conceptos and "compresion" in conceptos:
        conceptos.remove("compresion")
    if "compresion paralela" in conceptos and "compresion" in conceptos:
        conceptos.remove("compresion")

    return conceptos


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


def _resolver_referente_ambiguo(pregunta: str, historial: list):
    pregunta_limpia = _normalizar_texto(pregunta)
    palabras = pregunta_limpia.split()
    usa_referente_eso = any(ref in palabras for ref in ["eso", "esto", "esa", "ese"]) or pregunta_limpia.startswith("y eso")
    pide_uso_del_referente = any(frase in pregunta_limpia for frase in [
        "cuando conviene", "cuando usar", "usarlo", "usarla", "eso cuando", "eso como"
    ])

    if "db" in pregunta_limpia:
        return "", "De que parametro en dB hablas: nivel, threshold, reduccion de ganancia, LUFS u otro?"
    if "donde dice" in pregunta_limpia or "donde aparece" in pregunta_limpia:
        return "", "Sobre que afirmacion o concepto quieres que busque la fuente?"

    ultimo_asistente = _ultimo_mensaje_asistente(historial)
    ultimo_usuario = _ultimo_mensaje_usuario(historial)
    conceptos_asistente = _conceptos_relevantes_pregunta(ultimo_asistente)
    conceptos_usuario = _conceptos_relevantes_pregunta(ultimo_usuario)

    if usa_referente_eso and pide_uso_del_referente:
        if any(concepto in conceptos_usuario for concepto in ["clip", "headroom", "flujo de senal"]):
            return "", "Necesito una precision minima: te refieres al clipping del master, a la estructura de ganancia o a otra parte?"
        if len(conceptos_usuario) != 1:
            return "", "Necesito una precision minima: a que parte te refieres exactamente?"

    conceptos_comunes = [
        concepto for concepto in conceptos_usuario
        if concepto in conceptos_asistente
    ]
    if len(conceptos_comunes) == 1:
        return conceptos_comunes[0], ""

    # Si el turno anterior del alumno dejo un unico concepto tecnico claro,
    # "eso" se resuelve a ese concepto. No usamos solo el ultimo mensaje del
    # asistente: puede arrastrar un concepto vecino que el usuario no nombro.
    if len(conceptos_usuario) == 1:
        return conceptos_usuario[0], ""

    if conceptos_usuario:
        return "", ""

    return "", ""

def _parece_consulta_del_dominio_curso(pregunta: str, contexto_leccion: str = ""):
    texto = _normalizar_texto(f"{pregunta} {contexto_leccion}")
    return any(pista in texto for pista in DOMAIN_HINT_TERMS)

def nodo_supervisor(state: EstadoAgente):
    """Evalua la pregunta limpia y decide a que especialista enviarla."""
    clasificacion = _clasificacion_pedagogica(
        state.get("pregunta", ""),
        state.get("contexto_leccion", ""),
        bool(state.get("imagen")),
        state.get("ruta", "")
    )

    if state.get("ruta") == "internet":
        print("[SUPERVISOR]: Ruta forzada a internet.")
        return {"ruta": "internet", **clasificacion}

    pregunta_original = state["pregunta"].strip()
    pregunta_limpia = _normalizar_texto(pregunta_original)

    textos_rapidos = [
        "hola", "holaa", "buenas", "buenas tardes", "buenos dias",
        "buenas noches", "saludos", "hey", "que tal", "como estas",
        "gracias", "muchas gracias", "ok", "vale", "perfecto",
        "listo", "entendido", "adios", "chao", "hasta luego"
    ]
    if pregunta_limpia in textos_rapidos:
        print("[SUPERVISOR]: Charla basica detectada.")
        return {
            "ruta": "saludo",
            **clasificacion,
            "intent": "saludo",
            "answer_type": "needs_more_context",
            "requires_course_evidence": False
        }

    if state.get("imagen") and not pregunta_limpia:
        print("[SUPERVISOR]: Imagen sin texto detectada. Ruta -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if state.get("imagen"):
        print("[SUPERVISOR]: Imagen detectada. Prioridad visual -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if _es_estudiante_perdido(pregunta_original):
        print("[SUPERVISOR]: Frustracion o bloqueo de aprendizaje detectado. Ruta -> perdido.")
        return {"ruta": "perdido", **clasificacion}

    if _es_pregunta_lookup(pregunta_original):
        print("[SUPERVISOR]: Pregunta de ubicacion/recurso detectada. Ruta -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if _es_pregunta_ambigua(pregunta_original):
        print("[SUPERVISOR]: Pregunta ambigua corta detectada. Ruta deterministica -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if clasificacion.get("course_module") or _tiene_termino_tecnico_curso(pregunta_original):
        print("[SUPERVISOR]: Consulta tecnica del curso detectada. Ruta deterministica -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if not _parece_consulta_del_dominio_curso(pregunta_original, state.get("contexto_leccion", "")):
        print("[SUPERVISOR]: Consulta fuera de dominio detectada por compuerta deterministica. Ruta -> bloqueo.")
        return {
            "ruta": "bloqueo",
            **clasificacion,
            "intent": "fuera_dominio",
            "answer_type": "out_of_domain",
            "requires_course_evidence": False
        }

    historial_formateado = _formatear_historial(state.get("historial", []))
    contexto_leccion = state.get("contexto_leccion", "").strip()

    prompt = (
        "Eres un clasificador para un tutor de un curso de mezcla y masterizacion.\n"
        "Clasifica la pregunta en UNA categoria:\n"
        "1. internet: si pide links externos, descargas, plugins externos o informacion actual.\n"
        "2. teoria: si pregunta sobre audio, mezcla, masterizacion, DAWs, plugins, ejercicios o material del curso.\n"
        "3. perdido: si el alumno dice que no entiende, se perdio, se rinde o todo le suena igual.\n"
        "4. bloqueo: si habla de temas fuera de audio, mezcla, masterizacion o produccion musical.\n\n"
        "Regla de contexto: si la pregunta es corta o ambigua, usa el historial y el contexto de leccion "
        "solo para entender a que se refiere. No los uses como evidencia factual.\n\n"
        f"{historial_formateado}"
        f"Contexto de leccion actual: {contexto_leccion}\n"
        "Responde unica y exclusivamente con una palabra: internet, teoria, perdido o bloqueo.\n"
        f"Pregunta a clasificar: {pregunta_original}"
    )

    respuesta = llm_logico.invoke(prompt).content.strip().lower()

    if "internet" in respuesta:
        ruta = "internet"
        clasificacion.update({
            "intent": "consulta_externa",
            "answer_type": "web_answer",
            "requires_course_evidence": False
        })
    elif "perdido" in respuesta:
        ruta = "perdido"
        clasificacion.update({"intent": "estudiante_perdido", "answer_type": "rag_answer"})
    elif "bloqueo" in respuesta:
        ruta = "bloqueo"
        clasificacion.update({
            "intent": "fuera_dominio",
            "answer_type": "out_of_domain",
            "requires_course_evidence": False
        })
    else:
        ruta = "teoria"

    print(f"[SUPERVISOR]: Decision tomada -> {ruta}")
    print(f"[PEDAGOGIA]: {clasificacion}")
    return {"ruta": ruta, **clasificacion}
