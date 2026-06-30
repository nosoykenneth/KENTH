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

# Taxonomia por SECCION del curso (la taxonomia "eje" quedo deprecada; el
# conocimiento se ancla a la seccion Moodle). Cada entrada lleva section_number
# (1..N, base Moodle de las secciones pedagogicas) para hablar el mismo numero
# que el retrieval por seccion.
COURSE_SECTIONS = _PACK.course_sections()

STRONG_SECTION_TERMS = _PACK.strong_section_terms()

# Fase 0: el vocabulario de dominio vive en el Domain Pack (datos), no en codigo.
TECHNICAL_WORD_LIST = _PACK.technical_word_list()
DOMAIN_HINT_TERMS = _PACK.domain_hint_terms()
# Seleccion de intent por keyword (ORDENADA: primer match gana).
INTENT_SELECTION_KEYWORDS = _PACK.intent_selection_keywords()
# Etiqueta del dominio desde el Domain Pack (datos), no cableada en el agente.
# El clasificador LLM la usa en vez de nombrar el curso a mano.
DOMAIN_LABEL = _PACK.domain_label("este curso")


def _normalizar_texto(texto: str):
    texto = (texto or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    for char in ["!", "¡", "Â¡", "?", "¿", "Â¿", ".", ",", ":", ";"]:
        texto = texto.replace(char, "")
    return texto.strip()


def _seccion_fuerte_pregunta(texto: str):
    """Etiqueta "Seccion N" cuyos terminos fuertes mejor casan, o "" si ninguno."""
    texto_norm = _normalizar_texto(texto)
    mejor_seccion = ""
    mejor_score = 0
    for seccion, terminos in STRONG_SECTION_TERMS.items():
        score = 0
        for termino in terminos:
            termino_norm = _normalizar_texto(termino)
            if termino_norm and termino_norm in texto_norm:
                score += 2 if " " in termino_norm else 1
        if score > mejor_score:
            mejor_seccion = seccion
            mejor_score = score
    return mejor_seccion


def _warning(code: str, message: str):
    return {"code": code, "message": message}


def _numero_de_etiqueta_seccion(etiqueta: str):
    """Numero de seccion (int) embebido en una etiqueta tipo "Seccion 4", o None."""
    match = re.search(r"(\d+)", etiqueta or "")
    return int(match.group(1)) if match else None


def _seccion_por_numero(numero):
    """Entrada de COURSE_SECTIONS cuyo section_number == numero, o None."""
    if numero is None:
        return None
    for seccion in COURSE_SECTIONS:
        sn = seccion.get("section_number")
        try:
            if sn is not None and int(sn) == numero:
                return seccion
        except (TypeError, ValueError):
            continue
    return None


def _inferir_seccion_categoria(pregunta: str, contexto_leccion: str = ""):
    """(section_id, evaluation_category) de la seccion que mejor cubre la pregunta.

    Primero por terminos fuertes ("Seccion N" -> esa seccion por section_number);
    si no, por solapamiento de keywords sobre COURSE_SECTIONS. Devuelve ("", "")
    si nada casa. Antes esto inferia el "eje"; ahora habla de secciones Moodle.
    """
    texto = _normalizar_texto(f"{pregunta} {contexto_leccion}")
    seccion_fuerte = _seccion_fuerte_pregunta(texto)
    if seccion_fuerte:
        seccion = _seccion_por_numero(_numero_de_etiqueta_seccion(seccion_fuerte))
        if seccion:
            return seccion["id"], seccion["evaluation_category"]

    mejor = None
    mejor_score = 0
    for seccion in COURSE_SECTIONS:
        score = 0
        for keyword in seccion["keywords"]:
            keyword_norm = _normalizar_texto(keyword)
            if not keyword_norm:
                continue
            if len(keyword_norm) <= 2:
                if keyword_norm in texto.split():
                    score += 1
            elif keyword_norm in texto:
                score += 1
        if score > mejor_score:
            mejor = seccion
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
    course_module, evaluation_category = _inferir_seccion_categoria(pregunta, contexto_leccion)

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


# Señales inequivocas de bloqueo/frustracion: disparan "perdido" siempre.
FRASES_PERDIDO_FUERTE = [
    "me perdi", "me rindo", "estoy perdido", "estoy perdida",
    "todo me suena igual", "no se que hacer", "no se por donde empezar",
    "explicame desde cero",
]
# Señales debiles: "no entiendo X" es muy comun en preguntas conceptuales
# normales del curso ("no entiendo la compresion paralela"). Solo cuentan como
# "perdido" cuando NO son una consulta conceptual directa sobre un concepto del
# curso (jerarquia concepts.md: una pregunta del dominio no se degrada a perdido).
FRASES_PERDIDO_DEBIL = ["no entiendo", "no entendi"]


def _es_estudiante_perdido(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    if any(frase in pregunta_limpia for frase in FRASES_PERDIDO_FUERTE):
        return True
    if any(frase in pregunta_limpia for frase in FRASES_PERDIDO_DEBIL):
        # "no entiendo <concepto del curso>" es una consulta conceptual normal,
        # no frustracion: no la marcamos como estudiante perdido.
        if _es_pregunta_conceptual_directa(pregunta) or _tiene_termino_tecnico_curso(pregunta):
            return False
        return True
    return False


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
    if _seccion_fuerte_pregunta(pregunta) and not any(ref in palabras for ref in referencias):
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


# ==========================================
# POLITICA DE LA LECCION ACTIVA (Capas 3/4)
# ==========================================
# El supervisor recibe el `state` completo (incluye `tutor_envelope`), pero
# historicamente solo miraba la pregunta cruda + un string de contexto. Estas
# capas (leccion/bloque) son las que AUTORIZAN al tutor (delegacion, conceptos de
# la leccion) y deben consultarse ANTES de bloquear por dominio (concepts.md §1).

def _envelope_leccion_bloque(state: dict):
    """Lección y bloque activos del envelope, o (None, None) en modo general."""
    envelope = (state or {}).get("tutor_envelope")
    lesson = getattr(envelope, "active_lesson", None) if envelope else None
    block = getattr(envelope, "active_block", None) if envelope else None
    return (
        lesson if isinstance(lesson, dict) else None,
        block if isinstance(block, dict) else None,
    )


def _terminos_significativos(texto: str):
    """Palabras de contenido (len>3, sin stopwords) para solapamiento determinista."""
    return {
        t for t in _normalizar_texto(texto).split()
        if len(t) > 3 and t not in LOOKUP_STOPWORDS
    }


def _pregunta_delegada_a_tutor(pregunta: str, lesson: dict):
    """Item de `delegated_to_tutor` que cubre la pregunta, o "".

    Jerarquia (concepts.md §1, regla 3): una regla global de dominio NO puede
    vetar algo que la leccion delego explicitamente al tutor. Heuristica
    determinista: la pregunta comparte una palabra significativa con un delegado.
    """
    if not lesson:
        return ""
    # Solo terminos de CONTENIDO: si no, una palabra-funcion como 'como' (presente
    # en un delegado tipo 'Como construir habitos de escucha...') hace match con
    # 'como preparo una pizza' y autoriza por error una pregunta ajena.
    q_terms = _terminos_contenido(pregunta)
    if not q_terms:
        return ""
    for item in lesson.get("delegated_to_tutor") or []:
        if q_terms & _terminos_significativos(item):
            return item
    return ""


def _pregunta_cubierta_por_leccion(pregunta: str, lesson: dict, block: dict = None):
    """True si la pregunta pertenece al dominio segun la metadata de leccion/bloque.

    Implementa "ausencia de evidencia != fuera de dominio" (concepts.md §5,
    regla 4): una leccion con titulo generico ("Clase 3") pero conceptos del
    dominio mantiene la pregunta dentro del dominio. Mira titulo, objetivo,
    criterios, prompts sugeridos, delegados y, si hay bloque activo, sus
    conceptos/foco/resumen. Solo se usa para EVITAR bloquear (sesgo seguro: a lo
    sumo deja pasar al RAG, que tiene sus propias compuertas de evidencia).
    """
    if not lesson:
        return False
    # Solo terminos de CONTENIDO: evita que 'como'/'cuanto' hagan match con un
    # prompt de la leccion ('como diagnostico...') y la den por cubierta.
    q_terms = _terminos_contenido(pregunta)
    if not q_terms:
        return False
    partes = [
        lesson.get("lesson_title") or lesson.get("title") or "",
        lesson.get("learning_goal") or "",
        " ".join(lesson.get("learning_goals") or []),
        " ".join(lesson.get("suggested_prompts") or []),
        " ".join(lesson.get("delegated_to_tutor") or []),
    ]
    if block:
        partes.append(" ".join(block.get("concepts") or []))
        partes.append(block.get("tutor_focus") or "")
        partes.append(block.get("summary") or "")
        partes.append(block.get("block_title") or "")
    return bool(q_terms & _terminos_significativos(" ".join(partes)))


# ==========================================
# PREGUNTAS DE UBICACION / ORIENTACION (modo navegacion del curso)
# ==========================================
# "en que leccion estoy", "donde estoy", "que estoy viendo" son preguntas META
# sobre la posicion del alumno. NO deben ir al RAG: alli el modelo termina
# narrando el bloque de CONTEXTO ACTIVO inyectado y filtra ids, rangos de tiempo
# y la lista de temas delegados (Finding H2). Se responden de forma determinista
# desde el envelope (nodo_orientacion). Frases de navegacion = vocabulario neutro,
# no de dominio, por eso viven en el agente y no en el Domain Pack.
PATRONES_UBICACION = [
    # Leccion / curso (los patrones cortos como 'que leccion es' capturan tambien
    # las variantes 'estamos'/'estoy' por substring).
    "en que leccion estoy", "en que clase estoy", "en que modulo estoy",
    "en que parte del curso estoy", "en que parte estoy", "en que tema estoy",
    "en que video estoy", "donde estoy", "que leccion es", "que clase es esta",
    "cual es esta leccion", "cual leccion es esta",
    "que estoy viendo", "que estoy aprendiendo", "que leccion estoy viendo",
    "como se llama esta leccion", "como se llama esta clase",
    # Bloque (identidad/posicion, NO contenido: 'de que trata este bloque' NO
    # debe matchear porque es una pregunta de contenido, no de ubicacion).
    "en que bloque", "que bloque es", "de que bloque",
    # Seccion ('que seccion es' captura 'en que seccion estoy/estamos' por
    # substring; no usamos 'en que seccion' pelado para no atrapar lookups tipo
    # 'en que seccion encuentro los ejercicios').
    "que seccion es", "a que seccion pertenece", "a que seccion corresponde",
    "de que seccion es este",
]


def _es_pregunta_de_ubicacion(pregunta: str):
    """True si la pregunta es navegacional ('donde/que leccion estoy')."""
    texto = _normalizar_texto(pregunta)
    if not texto:
        return False
    # 'en que parte de la cadena va el compresor' es tecnica, no navegacion.
    if _tiene_termino_tecnico_curso(pregunta):
        return False
    return any(patron in texto for patron in PATRONES_UBICACION)


# Preguntas por el CONTENIDO del bloque actual ('de que trata este bloque'). NO
# es navegacion (eso es ubicacion) ni tecnica: se responde desde el RESUMEN del
# bloque (Capa 2), sin narrar transcripciones de otros bloques (Finding: el RAG
# volcaba 'transcripcion del bloque 3/4/5').
PATRONES_RESUMEN_BLOQUE = [
    "de que trata este bloque", "de que va este bloque", "que trata este bloque",
    "de que habla este bloque", "que dice este bloque", "que pasa en este bloque",
    "que se ve en este bloque", "que muestran en este bloque", "resume este bloque",
    "resumen de este bloque", "que explican en este bloque", "que explican aqui",
    "que se ve aqui", "de que trata este video", "de que trata esta parte",
]


def _es_pregunta_sobre_bloque_actual(pregunta: str):
    """True si la pregunta pide el CONTENIDO del bloque actual (no su ubicacion)."""
    texto = _normalizar_texto(pregunta)
    if not texto:
        return False
    if _tiene_termino_tecnico_curso(pregunta):
        return False
    return any(patron in texto for patron in PATRONES_RESUMEN_BLOQUE)


# ==========================================
# CONTINUACION SIN CONTENIDO NUEVO
# ==========================================
# 'explicame mejor', 'dame un ejemplo', 'y el resto?' no introducen un tema
# propio: continuan la leccion. NO se bloquean por dominio aunque no traigan un
# termino del curso (dependen del contexto/historial). Esto separa la
# continuacion de una pregunta con contenido ajeno propio ('quien gano el
# mundial'), que si debe bloquearse. Vocabulario conversacional neutro.
# Muletillas conversacionales (verbos de peticion, comprension, cuantificadores).
# Deliberadamente GENEROSO: si una pregunta ajena se cuela como "continuacion",
# el clasificador LLM es el respaldo y la bloquea; en cambio bloquear una
# continuacion legitima es un falso-bloqueo duro. NUNCA incluye sustantivos-tema,
# por lo que una pregunta fuera de dominio conserva su sustantivo propio (mundial,
# pelicula, chiste...) y NO se considera continuacion. Vocabulario neutro.
PALABRAS_META_GENERICAS = {
    # peticiones / continuacion
    "explicame", "explica", "explicar", "explicacion", "detalla", "detallar",
    "amplia", "ampliar", "ejemplo", "ejemplos", "resume", "resumen", "continua",
    "continuar", "sigue", "seguir", "aclara", "aclarame", "aclaracion", "repite",
    "repiteme", "profundiza", "profundizar", "desarrolla", "desarrollar",
    # verbos de peticion genericos
    "dame", "darme", "ponme", "ponerme", "poner", "pones", "muestrame", "mostrarme",
    "dime", "decirme", "cuentame", "puedes", "puede", "podrias", "podria", "quiero",
    "quisiera", "quieres", "necesito", "ayuda", "ayudame", "ayudarme", "gustaria",
    "saber", "hablame", "comenta", "comentame",
    # verbos de estudio / navegacion (no introducen tema propio)
    "puedo", "podemos", "repasar", "repaso", "revisar", "reviso", "ver", "veo",
    "leer", "leo", "estudiar", "practicar", "encontrar", "encuentro", "buscar",
    "busco", "mirar", "miro", "conocer", "aprender", "aprendo", "recordar",
    # comprension / muletillas
    "entiendo", "entendi", "comprendo", "comprendi", "claro", "clara", "queda",
    "quedo", "sentido", "mejor", "duda", "dudas",
    # cuantificadores / referencias vagas
    "detalle", "detalles", "mas", "menos", "resto", "otro", "otra", "otros",
    "otras", "punto", "puntos", "parte", "partes", "tema", "temas", "eso",
    "esto", "info", "informacion", "sobre", "acerca",
}

# Palabras-funcion (interrogativos, demostrativos, cerrados). No son contenido:
# que una compuerta haga match sobre 'como' o 'cuanto' es un falso positivo (por
# eso 'como esta el clima' parecia 'cubierta' por un prompt 'como diagnostico...').
PALABRAS_FUNCION = {
    "como", "cuanto", "cuanta", "cuantos", "cuantas", "cuando", "donde", "cual",
    "cuales", "quien", "quienes", "porque", "esta", "este", "estos", "estas",
    "esos", "esas", "aqui", "alli", "ahora", "antes", "ademas", "tambien",
    "curso", "leccion", "clase", "seccion", "modulo",
    # conectores discursivos (un 'entonces?' suelto es continuacion, no tema)
    "entonces", "pero", "bueno", "luego", "despues", "asi", "pues",
}


def _terminos_contenido(texto: str):
    """Terminos de CONTENIDO real: sin stopwords, sin muletillas, sin funcion.

    Aisla el sustantivo/tema propio de la pregunta. 'como esta el clima' -> {clima};
    'puedes darme mas detalle' -> {} (solo muletillas); 'quien gano el mundial' ->
    {gano, mundial}. Base de la deteccion de continuacion y de fuera-de-dominio.
    """
    return {
        t for t in _terminos_significativos(texto)
        if t not in PALABRAS_META_GENERICAS and t not in PALABRAS_FUNCION
    }


def _es_continuacion_sin_contenido_nuevo(pregunta: str):
    """True si la pregunta no aporta un tema propio (continuacion del dialogo).

    Se decide SOLO por contenido: 'explicame mejor' / 'y el resto?' no tienen tema
    propio (continuacion -> no bloquear); 'quien gano el mundial' o 'entonces los
    tutoriales no sirven' si lo tienen (van al juez de dominio). Antes habia un
    atajo 'empieza con conector' que dejaba pasar 'entonces quien gano el mundial'.
    """
    return not _terminos_contenido(pregunta)


def _hint_dominio_en_pregunta(pregunta: str):
    """Hint de dominio por PALABRA COMPLETA (no substring).

    `_parece_consulta_del_dominio_curso` hace match de substring, asi hints cortos
    como 'eco' matchean dentro de 'r-eco-miendame' (falso positivo). Para decidir
    si la PREGUNTA es del dominio exigimos coincidencia de token (o de frase, para
    hints multipalabra).
    """
    norm = _normalizar_texto(pregunta)
    tokens = set(norm.split())
    for pista in DOMAIN_HINT_TERMS:
        p = _normalizar_texto(pista)
        if not p:
            continue
        if " " in p:
            if p in norm:
                return True
        elif p in tokens:
            return True
    return False


def _pregunta_tiene_senal_dominio_propia(pregunta: str):
    """True si la PREGUNTA (sin el string de contexto) toca el dominio del curso.

    El `contexto_leccion` que envia el front esta lleno de terminos del curso;
    usarlo para decidir dominio hace pasar cualquier cosa ('quien gano el mundial'
    dentro de una leccion). El dominio se decide sobre la PREGUNTA; el contexto
    solo sirve para resolver referencias y rescatar continuaciones (Finding H1).
    """
    modulo, _ = _inferir_seccion_categoria(pregunta, "")
    return (
        bool(modulo)
        or _tiene_termino_tecnico_curso(pregunta)
        or _hint_dominio_en_pregunta(pregunta)
    )


def _relacionada_con_dominio_llm(pregunta: str, lesson: dict):
    """Juez semantico para la ZONA INCIERTA (contenido propio, sin cobertura lexica).

    Unico punto del routing donde decide un LLM, y SOLO porque la relacion tematica
    con vocabulario arbitrario es semantica, no resoluble con reglas: 'los
    tutoriales de youtube no sirven' es del tema de una leccion sobre 'recetas',
    pero 'quien gano el mundial' no, y lexicamente ambas son "contenido ajeno".
    Devuelve True (-> teoria) si esta relacionada, False (-> bloqueo) si es ajena.
    Ante fallo o respuesta ambigua, conserva el BLOQUEO (garantia fuera-de-dominio).
    """
    if llm_logico is None:
        return False
    titulo = ""
    objetivo = ""
    if lesson:
        titulo = (lesson.get("lesson_title") or lesson.get("title") or "").strip()
        objetivo = (lesson.get("learning_goal") or "").strip()
    contexto = ""
    if titulo:
        contexto += f'Leccion actual: "{titulo}".\n'
    if objetivo:
        contexto += f"Objetivo de la leccion: {objetivo}.\n"
    prompt = (
        f"Eres un filtro de relevancia para el tutor de un curso de {DOMAIN_LABEL}.\n"
        f"{contexto}"
        "Di si la PREGUNTA se relaciona con APRENDER ese tema (SI) o es de un tema "
        "totalmente ajeno (NO).\n"
        "Cuenta como SI, aunque no use palabras tecnicas: cuestionar si sirven los "
        "tutoriales/videos/recetas/metodos para aprender el tema; dudas sobre por que o "
        "como aprender, practicar o tomar el curso; herramientas o software del tema.\n"
        "Cuenta como NO: deportes, politica, comida, clima, entretenimiento, matematicas "
        "o cualquier cosa sin relacion con el tema del curso.\n"
        "Ejemplos:\n"
        "Pregunta: quien gano el mundial -> NO\n"
        "Pregunta: los tutoriales de youtube no sirven -> SI\n"
        "Pregunta: cuentame un chiste -> NO\n"
        "Pregunta: para que tomar el curso si hay videos gratis -> SI\n"
        "Pregunta: como esta el clima -> NO\n"
        "Pregunta: las recetas que copio de internet no me funcionan -> SI\n"
        "Responde EXACTAMENTE una palabra, SI o NO.\n"
        f"Pregunta: {pregunta} ->"
    )
    try:
        resp = _normalizar_texto(llm_logico.invoke(prompt).content)
    except Exception:
        return False
    tokens = resp.split()
    return bool(tokens) and tokens[0] == "si"


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

    # Pregunta de ubicacion/orientacion: se responde de forma determinista desde
    # el envelope, sin pasar por el RAG (evita que el modelo narre el andamiaje).
    if _es_pregunta_de_ubicacion(pregunta_original):
        print("[SUPERVISOR]: Pregunta de ubicacion/orientacion detectada. Ruta -> ubicacion.")
        return {
            "ruta": "ubicacion",
            **clasificacion,
            "intent": "orientacion",
            "answer_type": "orientation",
            "requires_course_evidence": False,
        }

    # Pregunta por el CONTENIDO del bloque actual ('de que trata este bloque'):
    # es claramente del curso (sobre la posicion actual). Va a teoria de forma
    # deterministica; el nodo RAG la ancla al resumen del bloque (Capa 2).
    if _es_pregunta_sobre_bloque_actual(pregunta_original):
        print("[SUPERVISOR]: Pregunta por el contenido del bloque actual. Ruta -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if _es_estudiante_perdido(pregunta_original):
        print("[SUPERVISOR]: Frustracion o bloqueo de aprendizaje detectado. Ruta -> perdido.")
        return {"ruta": "perdido", **clasificacion}

    # Capas 3/4 y senal de dominio se calculan UNA vez para gobernar las
    # compuertas siguientes. La senal de dominio se decide sobre la PREGUNTA, no
    # sobre el string de contexto (que esta lleno de terminos del curso y hacia
    # pasar a teoria cualquier cosa, incluso 'quien gano el mundial' — Finding H1).
    lesson_activa, bloque_activo = _envelope_leccion_bloque(state)
    item_delegado = _pregunta_delegada_a_tutor(pregunta_original, lesson_activa)
    tiene_senal_dominio = _pregunta_tiene_senal_dominio_propia(pregunta_original)
    cubierta_por_leccion = _pregunta_cubierta_por_leccion(pregunta_original, lesson_activa, bloque_activo)

    # BLOQUEO DETERMINISTICO TEMPRANO de fuera-de-dominio. Va ANTES de lookup y
    # ambigua para que 'cuanto cuesta un iphone' o 'como esta el clima hoy' no se
    # cuelen como pregunta del curso (esas compuertas hacian match sobre 'cuanto'/
    # 'como'). Solo dispara con contenido ajeno REAL: sin senal de dominio, sin
    # delegacion, sin cobertura de la leccion y que NO sea una continuacion (esto
    # ultimo garantiza que existe un sustantivo-tema propio ajeno al curso).
    if (
        not tiene_senal_dominio
        and not item_delegado
        and not cubierta_por_leccion
        and not _es_continuacion_sin_contenido_nuevo(pregunta_original)
    ):
        # ZONA INCIERTA: la pregunta trae contenido propio pero sin senal/cobertura/
        # delegacion lexica. Distinguir 'tematico pero con otras palabras' (->
        # responder) de 'ajeno' (-> bloquear) es SEMANTICO, no lexico, asi que aqui
        # —y solo aqui— decide un juez LLM enfocado con el titulo/objetivo de la
        # leccion. Bloquea 'quien gano el mundial' y deja pasar 'los tutoriales de
        # youtube no sirven' en una leccion sobre 'la mentira de las recetas'.
        if _relacionada_con_dominio_llm(pregunta_original, lesson_activa):
            print("[SUPERVISOR]: Zona incierta juzgada RELACIONADA por el juez semantico. Ruta -> teoria.")
            return {"ruta": "teoria", **clasificacion, "applied_policies": ["semantic_domain_override"]}
        print("[SUPERVISOR]: Zona incierta juzgada AJENA por el juez semantico. Ruta -> bloqueo.")
        return {
            "ruta": "bloqueo",
            **clasificacion,
            "intent": "fuera_dominio",
            "answer_type": "out_of_domain",
            "requires_course_evidence": False,
            "blocked_by": "out_of_domain:semantic",
        }

    # Delegacion: la leccion AUTORIZA el tema al tutor (vence el bloqueo de dominio).
    if item_delegado:
        print(f"[SUPERVISOR]: Tema delegado por la leccion al tutor ('{item_delegado}'). Ruta -> teoria.")
        return {"ruta": "teoria", **clasificacion, "applied_policies": ["lesson_delegation_override"]}

    if _es_pregunta_lookup(pregunta_original):
        print("[SUPERVISOR]: Pregunta de ubicacion/recurso detectada. Ruta -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if _es_pregunta_ambigua(pregunta_original):
        print("[SUPERVISOR]: Pregunta ambigua corta detectada. Ruta deterministica -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    if tiene_senal_dominio:
        print("[SUPERVISOR]: Senal de dominio en la pregunta. Ruta deterministica -> teoria.")
        return {"ruta": "teoria", **clasificacion}

    # Sin senal propia pero la leccion la cubre por su metadata -> dominio.
    if cubierta_por_leccion:
        print("[SUPERVISOR]: Cubierta por la metadata de la leccion activa. Ruta -> teoria.")
        return {"ruta": "teoria", **clasificacion, "applied_policies": ["lesson_domain_override"]}

    # Lo unico que llega aqui es una CONTINUACION sin tema propio ('explicame
    # mejor', 'y el resto?'). No es fuera de dominio (ya filtrado arriba) ni
    # frustracion (perdido ya se evaluo): depende del contexto/historial, asi que
    # se enruta a teoria para CONTINUAR la leccion (el RAG la resuelve con el
    # contexto). Antes esto lo decidia un clasificador LLM 3b, que mandaba
    # 'explicame mejor' a 'perdido'; un gate critico no debe depender de un LLM
    # pequeno (concepts.md: determinismo en compuertas criticas).
    print("[SUPERVISOR]: Continuacion sin tema propio. Ruta deterministica -> teoria.")
    return {"ruta": "teoria", **clasificacion}
