from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from langchain_community.tools import DuckDuckGoSearchRun
import concurrent.futures
import os
import unicodedata

from models.schemas import EstadoAgente

# ==========================================
# 1. INICIALIZACION DE HERRAMIENTAS Y MODELOS
# ==========================================
EMBEDDING_MODEL_NAME = "nomic-embed-text"
TEXT_MODEL_NAME = "llama3.2:3b"
VISION_MODEL_NAME = "qwen3-vl:4b-instruct"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTOR_STORE_DIR = os.path.join(BASE_DIR, "bd_vectorial")

embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
buscador_web = DuckDuckGoSearchRun()

RETRIEVAL_K = 8
MIN_RELEVANCE_SCORE = 0.35
AMBIGUOUS_MAX_WORDS = 8
SPECIFIC_UNSUPPORTED_TERMS = [
    "serum", "sintesis", "synthesis", "fm", "wavetable", "granular",
    "ableton", "logic", "fl studio", "cubase", "pro tools", "reaper",
    "massive", "sylenth", "vital", "kontakt"
]
LOOKUP_STOPWORDS = {
    "que", "qué", "para", "por", "con", "del", "de", "la", "el", "lo", "los",
    "las", "un", "una", "unos", "unas", "reviso", "revisar", "entender",
    "explica", "explican", "explica", "mejor", "donde", "en", "que", "clase",
    "minuto", "pdf", "pagina", "página", "recurso", "tengo", "volver", "leer",
    "esto", "eso", "ahi", "allí", "alli"
}
TECHNICAL_CONCEPT_PATTERNS = [
    ("compresion multibanda", ["compresion multibanda", "multibanda"]),
    ("compresion paralela", ["compresion paralela"]),
    ("makeup gain", ["makeup gain", "ganancia de compensacion"]),
    ("reduccion de ganancia", ["reduccion de ganancia", "gain reduction"]),
    ("headroom", ["headroom"]),
    ("threshold", ["threshold", "umbral"]),
    ("lufs", ["lufs"]),
    ("limitador", ["limitador", "limiter"]),
    ("frecuencia de corte", ["frecuencia de corte"]),
    ("pendiente", ["pendiente", "pendientes", "pendiente abrupta", "pendientes abruptas", "slope"]),
    ("factor q", ["factor q", " q ", " q?", "q que", "que pendiente"]),
    ("fase lineal", ["fase lineal"]),
    ("ecualizacion dinamica", ["ecualizacion dinamica", "eq dinamica"]),
    ("eq correctiva", ["eq correctiva", "ecualizacion correctiva"]),
    ("eq tonal", ["eq tonal", "ecualizacion tonal"]),
    ("ecualizacion", ["ecualizacion", "ecualizador", "eq"]),
    ("compresion", ["compresion", "compresor"]),
    ("filtro", ["filtro", "frecuencia de corte"]),
    ("saturacion", ["saturacion"]),
    ("reverb", ["reverb", "reverberacion"]),
    ("delay", ["delay"]),
]
LOOKUP_STOPWORDS.update({
    "cual", "cuÃ¡l", "significa", "cuando", "cuÃ¡ndo", "usar",
    "siempre", "mismo", "misma", "entre"
})

COURSE_MODULES = [
    {
        "id": "fundamentos_acustica_medicion",
        "evaluation_category": "mezcla_general_ruteo",
        "keywords": ["frecuencia", "amplitud", "acustica", "medicion", "analizador", "escucha"]
    },
    {
        "id": "gain_staging_flujo_senal",
        "evaluation_category": "estructura_ganancia",
        "keywords": ["gain staging", "headroom", "nivel", "niveles", "entrada", "salida", "ruteo", "flujo de senal", "db"]
    },
    {
        "id": "polaridad_fase_monocompatibilidad",
        "evaluation_category": "fase_imagen_estereo",
        "keywords": ["polaridad", "fase", "mono", "monocompatibilidad", "correlacion", "cancelacion", "estereo"]
    },
    {
        "id": "filtros_ecualizacion",
        "evaluation_category": "ecualizacion_modificacion_espectral",
        "keywords": ["eq", "ecualizacion", "ecualizador", "filtro", "frecuencia", "q", "balance tonal", "espectral"]
    },
    {
        "id": "procesadores_dinamicos",
        "evaluation_category": "dinamica",
        "keywords": ["compresion", "compresor", "dinamica", "threshold", "ataque", "release", "ratio", "limitador", "multibanda"]
    },
    {
        "id": "espacialidad_profundidad_ambiencia",
        "evaluation_category": "fase_imagen_estereo",
        "keywords": ["espacialidad", "profundidad", "ambiencia", "reverb", "delay", "paneo", "imagen"]
    },
    {
        "id": "practica_integradora_mezcla",
        "evaluation_category": "mezcla_general_ruteo",
        "keywords": ["mezcla", "balance", "integrar", "practica", "sesion", "bus", "buses", "ruteo"]
    },
    {
        "id": "masterizacion_optimizacion_comercial",
        "evaluation_category": "mastering",
        "keywords": ["mastering", "masterizacion", "lufs", "limitador", "comercial", "optimizacion", "entrega", "streaming"]
    },
]


llm_logico = ChatOllama(model=TEXT_MODEL_NAME, temperature=0.2)
llm_vision = ChatOllama(model=VISION_MODEL_NAME, temperature=0.1)


def _get_vector_store():
    # Chroma puede quedar con una instancia vieja despues de rebuild. Abrirlo
    # por consulta mantiene al agente sincronizado con la base persistida.
    return Chroma(persist_directory=VECTOR_STORE_DIR, embedding_function=embeddings)


def _normalizar_texto(texto: str):
    texto = (texto or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    for char in ["!", "¡", "?", "¿", ".", ",", ":", ";"]:
        texto = texto.replace(char, "")
    return texto.strip()


def _warning(code: str, message: str):
    return {"code": code, "message": message}


def _inferir_modulo_categoria(pregunta: str, contexto_leccion: str = ""):
    texto = _normalizar_texto(f"{pregunta} {contexto_leccion}")
    mejor = None
    mejor_score = 0

    for modulo in COURSE_MODULES:
        score = 0
        for keyword in modulo["keywords"]:
            if _normalizar_texto(keyword) in texto:
                score += 1
        if score > mejor_score:
            mejor = modulo
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
        if any(word in texto for word in ["master", "mastering", "masterizacion", "comercial", "lufs"]):
            clasificacion["intent"] = "optimizacion_mastering_comercial"
        elif any(word in texto for word in ["suena", "porque", "problema", "reviso", "corrijo", "pierde", "satura"]):
            clasificacion["intent"] = "diagnostico_tecnico"
        elif any(word in texto for word in ["espacio", "profundidad", "reverb", "delay", "estereo", "ambiencia", "paneo"]):
            clasificacion["intent"] = "consejo_estetico_espacialidad"

    return clasificacion


PROMPT_COMMON_RULES = (
    "--- REGLAS COMUNES DEL TUTOR ---\n"
    "- Usa fuente del curso como evidencia principal cuando answer_type no sea web_answer.\n"
    "- Distingue explicitamente fuente del curso de fuente externa.\n"
    "- No inventes recursos, clases, paginas, minutos, URLs, plugins, DAWs, presets, parametros ni valores en dB.\n"
    "- Si falta contexto o evidencia, pide una aclaracion breve o declara que no hay respaldo suficiente.\n"
    "- Si la consulta esta fuera del dominio del curso, bloquea limpio y no des una mini clase general.\n"
    "-------------------------------\n"
)

PROMPTS_BY_INTENT = {
    "aclaracion_concepto": {
        "id": "aclaracion_concepto_v1",
        "text": (
            "INTENCION PEDAGOGICA: aclaracion de concepto.\n"
            "Objetivo: explicar un concepto del curso de forma clara y verificable.\n"
            "Estructura: definicion breve, importancia practica y orientacion concreta respaldada por evidencia.\n"
            "No agregues ejemplos o recursos que no esten en la evidencia o en la pregunta.\n"
        )
    },
    "diagnostico_tecnico": {
        "id": "diagnostico_tecnico_v1",
        "text": (
            "INTENCION PEDAGOGICA: diagnostico tecnico.\n"
            "Objetivo: ayudar a razonar posibles causas sin fingir que escuchaste el audio.\n"
            "Estructura: hipotesis cautelosa, comprobacion practica y siguiente paso.\n"
            "No afirmes diagnosticos definitivos ni valores exactos sin evidencia.\n"
        )
    },
    "consejo_estetico_espacialidad": {
        "id": "consejo_estetico_espacialidad_v1",
        "text": (
            "INTENCION PEDAGOGICA: consejo estetico/espacialidad.\n"
            "Objetivo: orientar decisiones de profundidad, paneo, ambiente o imagen estereo.\n"
            "Distingue decision tecnica de decision estetica. Evita recetas universales.\n"
            "Conecta con fase, mono o balance solo si la evidencia lo respalda.\n"
        )
    },
    "optimizacion_mastering_comercial": {
        "id": "optimizacion_mastering_comercial_v1",
        "text": (
            "INTENCION PEDAGOGICA: mastering u optimizacion comercial.\n"
            "Objetivo: orientar decisiones de acabado, traduccion y preparacion final.\n"
            "No inventes LUFS, dBTP, plataformas, estandares comerciales ni cadenas de mastering si no aparecen en la evidencia.\n"
        )
    },
    "busqueda_fuente": {
        "id": "busqueda_fuente_v1",
        "text": (
            "INTENCION PEDAGOGICA: busqueda de fuente.\n"
            "Objetivo: responder primero donde revisar, no desarrollar teoria larga.\n"
            "Estructura: recurso concreto, modulo/clase/minuto/pagina si existe, y explicacion minima de relevancia.\n"
            "Si no hay metadatos suficientes, dilo y pide el concepto exacto.\n"
        )
    },
    "fuera_dominio": {
        "id": "fuera_dominio_v1",
        "text": (
            "INTENCION PEDAGOGICA: fuera de dominio.\n"
            "Objetivo: bloquear breve, limpio y util.\n"
            "No expliques el tema externo. Redirige solo al dominio del curso de mezcla y masterizacion.\n"
        )
    },
    "ambigua": {
        "id": "ambigua_v1",
        "text": (
            "INTENCION PEDAGOGICA: pregunta ambigua.\n"
            "Objetivo: pedir aclaracion minima en una sola frase cuando el referente no sea unico.\n"
            "No desarrolles teoria ni adivines el referente.\n"
        )
    },
    "estudiante_perdido": {
        "id": "estudiante_perdido_v1",
        "text": (
            "INTENCION PEDAGOGICA: estudiante perdido.\n"
            "Objetivo: guiar paso a paso, con lenguaje simple y una pregunta corta de calibracion.\n"
        )
    },
    "consulta_externa": {
        "id": "consulta_externa_v1",
        "text": (
            "INTENCION PEDAGOGICA: respuesta con fuente externa.\n"
            "Objetivo: separar informacion web de evidencia del curso y advertir que no reemplaza el material cargado.\n"
        )
    },
    "retroalimentacion_visual": {
        "id": "retroalimentacion_visual_v1",
        "text": (
            "INTENCION PEDAGOGICA: retroalimentacion visual.\n"
            "Objetivo: describir solo lo observable en la imagen y no inferir sonido real.\n"
        )
    },
    "saludo": {
        "id": "saludo_v1",
        "text": "INTENCION PEDAGOGICA: saludo o cortesia. Responder breve y redirigir al curso.\n"
    },
}


def _prompt_info_por_intent(intent: str):
    return PROMPTS_BY_INTENT.get(intent, PROMPTS_BY_INTENT["aclaracion_concepto"])


def _prompt_por_intent(intent: str):
    info = _prompt_info_por_intent(intent)
    return PROMPT_COMMON_RULES + info["text"]


def _prompt_id_por_intent(intent: str):
    return _prompt_info_por_intent(intent)["id"]


def _campos_pedagogicos(state: EstadoAgente, **overrides):
    data = {
        "intent": state.get("intent", "aclaracion_concepto"),
        "answer_type": state.get("answer_type", "rag_answer"),
        "course_module": state.get("course_module", ""),
        "evaluation_category": state.get("evaluation_category", ""),
        "requires_course_evidence": state.get("requires_course_evidence", True),
        "warnings": list(state.get("warnings", []) or []),
        "retrieved_chunks": list(state.get("retrieved_chunks", []) or []),
        "model_used": state.get("model_used", TEXT_MODEL_NAME),
        "prompt_id": state.get("prompt_id", "")
    }
    data.update(overrides)
    if not data.get("prompt_id"):
        data["prompt_id"] = _prompt_id_por_intent(data.get("intent", "aclaracion_concepto"))
    return data


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

    palabras_tecnicas = [
        "filtro", "filtros", "ecualizacion", "ecualizador", "eq",
        "frecuencia de corte", "pendiente", "pendientes", "pendiente abrupta",
        "pendientes abruptas", "factor q", "fase lineal",
        "shelving", "campana", "notch", "hpf", "lpf", "layering",
        "capa", "capas", "headroom", "ganancia", "mezcla", "masterizacion"
    ]
    return any(f" {_normalizar_texto(palabra)} " in texto_limpio for palabra in palabras_tecnicas)


def _es_pregunta_conceptual_directa(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    patrones = [
        "que es", "que significa", "cual es la diferencia", "diferencia entre",
        "es lo mismo", "cuando usar", "cuando se usa", "cuando conviene",
        "conviene usar", "que reviso primero", "que revisar primero",
        "explicame", "hablame de", "cuentame sobre", "cuentame de"
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
    indicadores_directos = [
        "y eso", "eso cuando", "cuando si conviene", "cuando conviene",
        "conviene usarlo", "usarlo", "donde dice eso", "donde dice",
        "donde aparece", "a cuantos db", "cuantos db", "para esto",
        "sobre esto", "esto"
    ]
    if any(ind in pregunta_limpia for ind in indicadores_directos):
        return True

    indicadores = [
        "cuantos db", "a cuantos db", "cuanto", "donde", "cual",
        "eso", "ahi", "esa", "ese", "como asi"
    ]
    return len(palabras) <= AMBIGUOUS_MAX_WORDS and any(ind in pregunta_limpia for ind in indicadores)


def _es_pregunta_lookup(pregunta: str):
    pregunta_limpia = _normalizar_texto(pregunta)
    patrones = [
        "que recurso", "recurso reviso", "recurso debo", "que debo revisar",
        "donde explican", "donde se explica", "en que clase", "que clase",
        "en que minuto", "que minuto", "minuto reviso", "que pdf",
        "cual pdf", "pdf tengo", "que pagina", "en que pagina", "pagina reviso",
        "donde puedo repasar", "en que parte", "en que documento", "que documento",
        "que video", "que material", "donde esta", "donde encuentro",
        "que revisar", "que tengo que leer", "que tengo que ver",
        "donde se habla", "en que modulo", "que archivo",
        "donde veo", "donde lo veo", "donde aparece",
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


def _resolver_referente_ambiguo(pregunta: str, historial: list):
    pregunta_limpia = _normalizar_texto(pregunta)

    if "db" in pregunta_limpia:
        return "", "De que parametro en dB hablas: nivel, threshold, reduccion de ganancia, LUFS u otro?"
    if "donde dice" in pregunta_limpia or "donde aparece" in pregunta_limpia:
        return "", "Sobre que afirmacion o concepto quieres que busque la fuente?"

    ultimo_asistente = _ultimo_mensaje_asistente(historial)
    ultimo_usuario = _ultimo_mensaje_usuario(historial)
    conceptos_asistente = _conceptos_relevantes_pregunta(ultimo_asistente)
    conceptos_usuario = _conceptos_relevantes_pregunta(ultimo_usuario)

    conceptos_comunes = [
        concepto for concepto in conceptos_usuario
        if concepto in conceptos_asistente
    ]
    if len(conceptos_comunes) == 1:
        return conceptos_comunes[0], ""

    # Si el turno anterior del alumno dejo un unico concepto tecnico claro,
    # "eso" se resuelve a ese concepto. Antes se pedia aclaracion aunque el
    # ultimo usuario hubiera preguntado exactamente por un solo referente.
    if len(conceptos_usuario) == 1:
        return conceptos_usuario[0], ""

    if conceptos_usuario:
        return "", ""

    if len(conceptos_asistente) == 1:
        return conceptos_asistente[0], ""

    return "", ""


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


def _limpiar_imagen_base64(imagen: str):
    if "," in imagen:
        return imagen.split(",", 1)[1]
    return imagen


def _imagen_parece_audio(imagen: str):
    imagen_limpia = _limpiar_imagen_base64(imagen)
    print(f"[VISION GATE]: Imagen recibida. base64_len={len(imagen_limpia)}")
    prompt = (
        "Clasifica la imagen. Responde solo una palabra:\n"
        "AUDIO si parece una interfaz de DAW, plugin, medidor, forma de onda, mezclador, ecualizador, compresor o sesion de audio.\n"
        "NO_AUDIO si parece cualquier otra cosa: personas, fuego, paisajes, documentos, comida, objetos generales, etc.\n"
        "No expliques."
    )
    mensaje = [HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{imagen_limpia}"}
    ])]
    try:
        respuesta = llm_vision.bind(options={"repeat_penalty": 1.2}).invoke(mensaje).content.strip().upper()
    except Exception as e:
        print(f"[VISION GATE]: Error clasificando imagen: {e}")
        return False
    es_audio = "AUDIO" in respuesta and "NO_AUDIO" not in respuesta
    print(f"[VISION GATE]: Resultado={respuesta} -> es_audio={es_audio}")
    return es_audio


def _responder_imagen_audio_sin_evidencia(imagen_limpia: str, pregunta: str):
    print("[VISION NODE]: Nodo visual activo. Descripcion visual solamente.")
    prompt = (
        "Eres KENTH, tutor de mezcla y masterizacion.\n"
        "La imagen fue clasificada como relacionada con audio.\n"
        "Responde mirando la imagen. No uses teoria del curso salvo que sea estrictamente visible.\n\n"
        "Reglas:\n"
        "1. Describe solo lo observable en la captura: interfaz, controles, medidores, pistas, forma de onda o plugin.\n"
        "2. No infieras como suena. No inventes problemas de mezcla.\n"
        "3. No menciones recursos, clases, DAWs, plugins o tecnicas que no se vean en la imagen o no esten en la pregunta.\n"
        "4. Cierra con una pregunta breve para que el alumno precise que quiere revisar.\n\n"
        f"Pregunta del alumno: {pregunta}"
    )
    mensaje = [HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{imagen_limpia}"}
    ])]
    respuesta = llm_vision.bind(options={"repeat_penalty": 1.5}).invoke(mensaje).content
    print(f"[VISION NODE]: Respuesta vision_len={len(respuesta or '')}")
    return respuesta


def _resumen_metadata_debug(meta: dict):
    return {
        "filename": meta.get("filename") or os.path.basename(meta.get("source", "")),
        "doc_type": meta.get("doc_type"),
        "module": meta.get("module") or meta.get("modulo"),
        "topic": meta.get("topic") or meta.get("tema"),
        "resource_title": meta.get("resource_title") or meta.get("recurso_recomendado") or meta.get("recurso"),
        "page": meta.get("page"),
        "start_time": meta.get("start_time"),
        "url": meta.get("url") or meta.get("url_video")
    }


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


def _prioridad_evidencia(item: dict, pregunta: str):
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

    # Para preguntas conceptuales, FAQ, glosario y guia canonica son las
    # fuentes autorales principales del Modulo 4.
    filename = (meta.get("filename") or "").lower()
    if filename in {"m04_faq.json", "m04_glosario.json", "m04_guia_canonica.md"}:
        prioridad += 0.08

    if (
        "diferencia" in pregunta_norm
        and "filtro" in pregunta_norm
        and "ecualizacion" in pregunta_norm
        and filename == "m04_guia_canonica.md"
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
            score = cobertura * 10
            if filename == "m04_guia_canonica.md":
                score += 4
            if filename == "m04_faq.json":
                score += 3
            if filename == "m04_glosario.json":
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
        score = 0
        if concepto and concepto in texto:
            score += 10
        if filename == "m04_glosario.json":
            score += 4
        if filename == "m04_faq.json":
            score += 3
        if filename == "m04_guia_canonica.md":
            score += 1
        return score

    ordenadas = sorted(evidencias, key=prioridad, reverse=True)
    # Evita que chunks amplios de la guia contaminen definiciones directas
    # con contenido vecino como EQ correctiva/tonal.
    return ordenadas[:4]


def _buscar_evidencia(pregunta: str, modo_lookup: bool = False):
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

    unicas.sort(key=lambda item: _prioridad_evidencia(item, pregunta), reverse=True)
    _debug_resultados_retrieval(unicas, "semantic+lexical merged")
    return unicas


def _extraer_frases_lookup(pregunta: str):
    """Extrae frases compuestas significativas de la pregunta para busqueda lexica."""
    texto = _normalizar_texto(pregunta)
    # Eliminar las palabras de intención de lookup para quedarnos con el concepto
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

    # Eliminar stopwords sueltas restantes
    palabras = [w for w in texto.split() if w not in LOOKUP_STOPWORDS and len(w) > 2]
    if not palabras:
        return [], []

    # La frase completa como concepto principal
    frase_completa = " ".join(palabras)
    frases = [frase_completa]

    # Si la frase tiene 3+ palabras, generar bigramas
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

        # Coincidencia por frases compuestas (más preciso que tokens sueltos)
        frase_matches = sum(1 for frase in frases if frase in texto_limpio)
        token_matches = sum(1 for token in tokens if token in texto_limpio)

        if frase_matches == 0 and token_matches == 0:
            continue

        # Score base: las frases valen mucho más que tokens sueltos
        score = 0.30 + (frase_matches * 0.18) + (token_matches * 0.05)

        # Bonus por metadatos estructurados
        recurso = _normalizar_texto(meta.get("resource_title") or meta.get("recurso_recomendado") or "")
        tema = _normalizar_texto(meta.get("topic") or meta.get("tema") or "")
        clase = _normalizar_texto(meta.get("lesson_title") or "")

        for frase in frases:
            if frase in recurso:
                score += 0.20
            if frase in tema or frase in clase:
                score += 0.15

        # Bonus contextual: si pide minuto y el chunk tiene start_time
        if pide_minuto and meta.get("start_time") not in ("", None):
            score += 0.20
        # Bonus contextual: si pide página/pdf y el chunk tiene page
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


def _buscar_evidencia_lookup(pregunta: str):
    semanticas = _buscar_evidencia(pregunta, modo_lookup=True)
    lexicas = _buscar_evidencia_lexica_lookup(pregunta)

    # Si el léxico encontró matches con frases compuestas, darles boost en el merge
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
        "module": meta.get("module") or meta.get("modulo") or "",
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
    modulo = meta.get("module") or meta.get("modulo") or ""
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
    if modulo:
        detalle = f"Modulo {modulo}"
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
    modulo = meta.get("module") or meta.get("modulo") or ""

    lineas = [f"  - Documento: {filename} ({doc_type})"]
    if modulo:
        lineas.append(f"  - Modulo: {modulo}")
    if topic:
        lineas.append(f"  - Contenido asociado: {topic}")
    return lineas


def _respuesta_lookup(pregunta: str, evidencias: list):
    if not evidencias:
        return (
            "No encontre ubicaciones oficiales validadas ni documentos oficiales indexados para esa consulta. "
            "Prueba indicando el concepto exacto o modulo."
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

    # Deduplicar por filename para no repetir el mismo archivo
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
            "No hay ubicaciones oficiales validadas para esta consulta en M04: no tengo pagina, minuto, URL ni recurso aprobado.",
            "Lo que si hay son documentos oficiales indexados del modulo que puedes revisar:"
        ]
        for idx, item in enumerate(fuentes_unicas, 1):
            meta = item["document"].metadata or {}
            lineas.append("")
            lineas.append(f"**Documento {idx}:**")
            lineas.extend(_formatear_documento_oficial_lookup(meta))

    return "\n".join(lineas)


def _respuesta_sin_evidencia(state: EstadoAgente):
    if state.get("imagen"):
        detalle = "La captura ayuda, pero necesito que precises el modulo, clase, recurso o la parte concreta del DAW/plugin que quieres analizar."
    else:
        detalle = "Puedes precisar el modulo, clase, recurso o subir una captura relacionada para buscar mejor en la base del curso."

    return (
        "No tengo suficiente respaldo en el material cargado del curso para responder eso con seguridad. "
        "Prefiero no inventar una explicacion que pueda confundirte. "
        f"{detalle}"
    )


def _query_retrieval_con_aliases(pregunta: str):
    pregunta_norm = _normalizar_texto(pregunta)
    concepto_directo = _concepto_definicion_directa(pregunta)

    # Alias corto: en M04, "Q" se usa como factor Q. Para retrieval,
    # expandimos la consulta porque "q" sola es demasiado corta para Chroma
    # y para la busqueda lexica.
    if concepto_directo == "factor q" or (
        "factor q" not in pregunta_norm
        and f" q " in f" {pregunta_norm} "
        and any(patron in pregunta_norm for patron in ["que es", "que significa", "define"])
    ):
        return f"factor q. Pregunta original: {pregunta}"

    return pregunta


def _preparar_retrieval(state: EstadoAgente):
    pregunta = state["pregunta"].strip()
    contexto_leccion = state.get("contexto_leccion", "").strip()
    historial = state.get("historial", [])

    if _es_pregunta_lookup(pregunta):
        pregunta_limpia = _normalizar_texto(pregunta)
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
    # Regla anti-contaminacion conversacional:
    # 1. Si una pregunta ambigua ya fue resuelta, la query_retrieval contiene
    #    el referente validado; no volvemos a meter el historial completo.
    # 2. Si la pregunta actual NO es ambigua y ya trae terminos tecnicos,
    #    es conceptual directa o compara varios conceptos, se responde con
    #    la evidencia recuperada para esa pregunta, no con el subtema anterior.
    # 3. Solo conservamos historial para preguntas realmente dependientes de
    #    contexto que no hayan quedado resueltas antes del prompt final.
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


# ==========================================
# 2. NODOS DEL GRAFO
# ==========================================
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


# AUDIT FIX #6: Verificador post-generacion ligero.
# Detecta URLs inventadas y recursos/modulos no respaldados por la evidencia.
def _verificar_respuesta(respuesta: str, fuentes: list, evidencias: list):
    """Ultima linea de defensa: detecta alucinaciones obvias en la respuesta."""
    respuesta_norm = _normalizar_texto(respuesta)
    problemas = []

    # 1. Detectar URLs inventadas (no deben existir salvo que esten en evidencia)
    import re
    urls_respuesta = set(re.findall(r'https?://[^\s)>"]+', respuesta))
    urls_evidencia = set()
    for item in evidencias:
        meta = item["document"].metadata or {}
        for key in ("url", "url_video"):
            val = meta.get(key)
            if val:
                urls_evidencia.add(val)
    urls_inventadas = urls_respuesta - urls_evidencia
    if urls_inventadas:
        problemas.append(f"URLs no respaldadas eliminadas: {urls_inventadas}")
        for url in urls_inventadas:
            respuesta = respuesta.replace(url, "[enlace no verificado - consulta el material del curso]")

    # 2. Detectar mencion de modulos no presentes en evidencia
    modulos_evidencia = set()
    for item in evidencias:
        meta = item["document"].metadata or {}
        mod = meta.get("module") or meta.get("modulo")
        if mod:
            modulos_evidencia.add(str(mod))
    modulos_mencionados = set(re.findall(r'[Mm]odulo\s+(\d+)', respuesta))
    modulos_inventados = modulos_mencionados - modulos_evidencia
    if modulos_inventados:
        problemas.append(f"Modulos mencionados sin evidencia: {modulos_inventados}")

    if problemas:
        print(f"[VERIFICADOR]: Problemas detectados: {problemas}")
    else:
        print("[VERIFICADOR]: Respuesta limpia, sin alucinaciones detectadas.")

    return respuesta


def _fuentes_tienen_ubicacion_validada(fuentes: list):
    for fuente in fuentes or []:
        if fuente.get("page") not in ("", None):
            return True
        if fuente.get("start_time") not in ("", None):
            return True
        if fuente.get("url") not in ("", None):
            return True
        recurso = fuente.get("resource_title") or ""
        if recurso and not _normalizar_texto(recurso).startswith("m04_"):
            return True
    return False


def _bloquear_localizacion_no_validada(respuesta: str, fuentes: list):
    if _fuentes_tienen_ubicacion_validada(fuentes):
        return respuesta

    parrafos = respuesta.split("\n\n")
    filtrados = []
    for parrafo in parrafos:
        norm = _normalizar_texto(parrafo)
        recomienda_ubicacion = (
            ("recomiendo revisar" in norm or "puedes revisar" in norm or "revisa el recurso" in norm)
            and any(token in norm for token in ["clase", "modulo", "recurso", "guia", "seccion"])
        )
        if recomienda_ubicacion:
            continue
        oraciones = []
        for oracion in parrafo.split(". "):
            oracion_norm = _normalizar_texto(oracion)
            cita_ubicacion_interna = (
                "m04_" in oracion_norm
                or "fuente " in oracion_norm
                or "score" in oracion_norm
                or "archivo" in oracion_norm
                or "del recurso" in oracion_norm
                or "en el recurso" in oracion_norm
            )
            if cita_ubicacion_interna:
                continue
            oraciones.append(oracion)
        limpio = ". ".join(oraciones).strip()
        if limpio:
            filtrados.append(limpio)

    return "\n\n".join(filtrados).strip()


def nodo_rag(state: EstadoAgente):
    """Busca evidencia del curso y responde solo si hay respaldo suficiente."""
    print("[AGENTE RAG]: Buscando evidencia con Chroma + scores...")

    pregunta = state["pregunta"].strip()

    # AUDIT FIX #3: Imagen AUDIO ahora hace retrieval ANTES de responder.
    # La captura del alumno se conecta con material del curso si existe.
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
                    model_used=VISION_MODEL_NAME
                )
            }
        imagen_limpia = _limpiar_imagen_base64(state["imagen"])

        # Hacer retrieval con la pregunta o contexto de leccion para conectar imagen con curso
        query_imagen = pregunta or state.get("contexto_leccion", "").strip() or "captura DAW plugin mezcla masterizacion"
        evidencias_imagen = _buscar_evidencia(query_imagen)

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
                    model_used=VISION_MODEL_NAME
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
                    model_used=VISION_MODEL_NAME
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
        evidencias_lookup = _buscar_evidencia_lookup(query_retrieval)
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

    evidencias = _buscar_evidencia(query_retrieval)

    # AUDIT FIX #4: Eliminado codigo muerto con imagen_limpia fuera de scope.
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
        "La capa oficial de localizacion de M04 no tiene recursos ni ubicaciones aprobadas. "
        "Los nombres Fuente/archivo solo indican evidencia recuperada, NO clase, pagina, minuto ni recurso recomendado. "
        "No presentes ubicaciones oficiales si la evidencia no trae pagina, minuto, URL o recurso validado.\n"
        "------------------------\n"
    )

    # AUDIT FIX #2: Evidence gate REAL.
    # Si evidence_level es medio, endurece el prompt para que el LLM sea mas cauteloso.
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
        "8. Nunca inventes URLs, modulos, recursos, DAWs, plugins, parametros ni valores en dB.\n"
        "9. Si hay incertidumbre, pide una aclaracion breve.\n"
        "10. Mantente conciso, profesional y pedagogico.\n\n"
        "11. No menciones en la respuesta nombres internos como Fuente 1, score, chunk, archivo, tema o modulo "
        "salvo que el alumno pregunte explicitamente donde revisar o pida fuentes. Esos datos ya viajan en el JSON.\n\n"
        f"{_prompt_por_intent(intent_efectivo)}"
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

    # AUDIT FIX #6: Verificador post-generacion
    respuesta = _verificar_respuesta(respuesta, fuentes, evidencias)
    respuesta = _bloquear_localizacion_no_validada(respuesta, fuentes)

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
            warnings=[] if evidence_level == "alto" else [
                _warning("LOW_EVIDENCE", "La evidencia recuperada tiene relevancia moderada.")
            ],
            model_used=TEXT_MODEL_NAME
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
    evidencias = _buscar_evidencia(query_retrieval)

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
            model_used=TEXT_MODEL_NAME
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
            model_used=TEXT_MODEL_NAME
        )
    }


def nodo_guardia(state: EstadoAgente):
    """Rechaza preguntas fuera del dominio del curso sin improvisar."""
    print("[GUARDIA]: Bloqueando pregunta fuera de dominio...")
    return {
        "respuesta_final": (
            "Solo puedo ayudarte con mezcla, masterizacion, audio, DAWs, plugins y contenido del curso. "
            "Si tu duda esta relacionada con el curso, dime el modulo, clase o concepto que quieres revisar."
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
