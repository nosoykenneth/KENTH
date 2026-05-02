from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
import concurrent.futures

from models.schemas import EstadoAgente

# ==========================================
# 1. INICIALIZACIÓN DE HERRAMIENTAS Y MODELOS
# ==========================================
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# Como este archivo está en 'services/', la BD Chroma está una carpeta arriba
vector_store = Chroma(persist_directory="./bd_vectorial", embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) 
buscador_web = DuckDuckGoSearchRun()

# El cerebro lógico (llama3.2 de 3b es ideal aquí para que no se equivoque clasificando)
llm_logico = ChatOllama(model="llama3.2:3b", temperature=0.2) 
# El cerebro con ojos
llm_vision = ChatOllama(model="qwen3-vl:4b-instruct", temperature=0.1) 

# ==========================================
# 3. LOS AGENTES (Nodos del Grafo)
# ==========================================

def nodo_supervisor(state: EstadoAgente):
    """Evalúa la pregunta y decide a qué especialista enviarla."""
    if state.get("ruta") == "internet":
        print("👔 [SUPERVISOR]: Ruta forzada a 'internet'. Saltando clasificación.")
        return {"ruta": "internet"}
        
    pregunta_limpia = state["pregunta"].strip().lower()
    for char in ["!", "¡", "?", "¿", ".", ","]:
        pregunta_limpia = pregunta_limpia.replace(char, "")
    pregunta_limpia = pregunta_limpia.strip()
    
    textos_rapidos = ["hola", "holaa", "buenas", "buenas tardes", "buenos dias", "buenas noches", "saludos", "hey", "que tal", "como estas", "gracias", "muchas gracias", "ok", "vale", "perfecto", "listo", "entendido", "adios", "chao", "hasta luego"]
    if pregunta_limpia in textos_rapidos:
        print("👔 [SUPERVISOR]: Charla básica detectada. Ruta rápida -> 'saludo'")
        return {"ruta": "saludo"}

    print("👔 [SUPERVISOR]: Analizando la solicitud con IA...")
    
    # 1. Formatear el historial para que el Supervisor tenga contexto
    historial_formateado = ""
    if state.get("historial"):
        historial_formateado = "--- HISTORIAL RECIENTE ---\n"
        ultimos_mensajes = state["historial"][-4:] # Últimos 4
        for msg in ultimos_mensajes:
            rol = "Alumno" if msg.get("role") == "user" else "KENTH"
            historial_formateado += f"{rol}: {msg.get('content')}\n"
        historial_formateado += "--------------------------\n"
    
    prompt = (
        "Eres un clasificador inteligente para un curso de Mezcla y Masterización.\n"
        "Clasifica la siguiente pregunta en UNA de estas tres categorías:\n"
        "1. 'internet': Si el usuario pide descargar algo, un link, un plugin externo (ej. Voxengo SPAN), o noticias actuales.\n"
        "2. 'teoria': Si el usuario pregunta sobre audio, ecualización, compresores, DAWs, o si dice 'qué es esto en la imagen'.\n"
        "3. 'bloqueo': Si el usuario habla de cocina, videojuegos, política, o cualquier tema no musical.\n\n"
        "INSTRUCCIÓN CRÍTICA DE CONTEXTO: Antes de clasificar la pregunta como fuera de dominio ('bloqueo'), revisa el HISTORIAL RECIENTE. "
        "Si la pregunta es corta o ambigua (ej. '¿y cómo uso eso?', '¿dónde está?'), asume que se refiere al tema musical que se está discutiendo en los mensajes anteriores y mándala a 'teoria'.\n\n"
        f"{historial_formateado}"
        "RESPONDE ÚNICA Y EXCLUSIVAMENTE CON UNA DE LAS TRES PALABRAS (internet, teoria, o bloqueo). No digas nada más.\n"
        f"Pregunta a clasificar: {state['pregunta']}"
    )
    
    respuesta = llm_logico.invoke(prompt).content.strip().lower()
    
    # Limpieza por si el modelo responde con punto o caracteres extra
    if "internet" in respuesta: ruta = "internet"
    elif "bloqueo" in respuesta: ruta = "bloqueo"
    else: ruta = "teoria" # Por defecto, asumimos que es una duda del curso
    
    print(f"👔 [SUPERVISOR]: Decisión tomada -> Enviar a la ruta '{ruta}'")
    return {"ruta": ruta}


def nodo_rag(state: EstadoAgente):
    """Busca en los PDFs y responde (Soporta imágenes)"""
    print("📚 [AGENTE RAG]: Paso 1 - Activando base de datos vectorial (Nomic)...")
    
    # 1. Búsqueda
    docs = retriever.invoke(state["pregunta"])
    print("✅ [AGENTE RAG]: Paso 2 - Documentos encontrados. Preparando texto con metadatos...")
    
    # Formatear el contexto inyectando metadatos (si los hay)
    texto_crudo = ""
    for doc in docs:
        meta = doc.metadata
        # Extraer campos JSON si existen
        if "modulo" in meta or "tema" in meta:
            texto_crudo += f"[Módulo: {meta.get('modulo', 'N/A')} - Tema: {meta.get('tema', 'N/A')}]\n"
            
        texto_crudo += f"{doc.page_content}\n"
        
        recurso = meta.get("recurso_recomendado")
        video = meta.get("url_video")
        if recurso or video:
            texto_crudo += f"-> RECURSOS EDUCATIVOS ASOCIADOS: "
            if recurso: texto_crudo += f"[{recurso}] "
            if video: texto_crudo += f"(Video: {video}) "
        texto_crudo += "\n\n"

    if not docs:
        texto_crudo = "No hay contexto exacto, usa tu conocimiento."
        
    teoria = texto_crudo[:2000] + "..." if len(texto_crudo) > 2000 else texto_crudo
    
    # 2. Formatear el historial reciente
    historial_formateado = ""
    if state.get("historial"):
        historial_formateado = "--- HISTORIAL RECIENTE ---\n"
        ultimos_mensajes = state["historial"][-4:] # Últimos 4 intercambios
        for msg in ultimos_mensajes:
            rol = "Alumno" if msg.get("role") == "user" else "KENTH (Tú)"
            historial_formateado += f"{rol}: {msg.get('content')}\n"
        historial_formateado += "--------------------------\n"

    instrucciones = (
        "Eres KENTH, ingeniero de mezcla profesional y un TUTOR MENTOR.\n"
        "Tu objetivo es enseñar, guiar y fomentar el pensamiento crítico, sin frustrar al alumno con puras preguntas.\n\n"
        "REGLAS ESTRICTAS:\n"
        "1. DIFERENCIAR TEORÍA DE PRÁCTICA:\n"
        "   - Si la pregunta es TEÓRICA o el alumno pide un concepto (ej. '¿Qué es ecualización?', 'No entiendo'): DEBES EXPLICAR la teoría de forma clara y directa basándote en el material del curso. PROHIBIDO responder a una duda teórica con otra pregunta. Primero dale la base.\n"
        "   - Si la pregunta es de APLICACIÓN PRÁCTICA (ej. '¿Cómo corto graves aquí?'): Usa el método Socrático. NO des la solución exacta (ej. 'corta en 200Hz'). Da una pista teórica y formula una pregunta que lo obligue a deducir la respuesta.\n"
        "2. REGLA DEL 80/20: Tu respuesta debe ser 80% enseñanza/diagnóstico y 20% preguntas. NUNCA respondas únicamente con una pregunta suelta.\n"
        "3. RECURSOS EDUCATIVOS: Si la Teoría del Curso incluye 'RECURSOS EDUCATIVOS ASOCIADOS' (videos o actividades), DEBES incluirlos de forma natural al final de tu respuesta (ej. 'Para profundizar en esto, te recomiendo revisar el recurso: [Nombre] o ver este video: [URL]'). NUNCA inventes URLs ni recursos que no estén en el contexto.\n"
        "4. TONO DEL TUTOR: Mantén un tono alentador, profesional y analítico.\n"
        "5. SÉ CONCISO: Evita largos discursos académicos.\n\n"
        f"--- TEORÍA DEL CURSO ---\n{teoria}\n------------------------\n"
        f"{historial_formateado}"
    )

    if state["imagen"]:
        print("👀 [AGENTE RAG]: Paso 3 - Analizando imagen (Invocando a Qwen-Vision)...")
        
        # LIMPIEZA: Si la imagen viene con el prefijo "data:image/...;base64,", se lo quitamos
        # porque Ollama/LangChain esperan el string base64 puro.
        imagen_limpia = state["imagen"]
        if "," in imagen_limpia:
            imagen_limpia = imagen_limpia.split(",")[1]

        # PROMPT BLINDADO SOCRÁTICO
        instrucciones_vision = (
            "Eres KENTH, ingeniero de mezcla profesional y Tutor.\n"
            "El alumno ha adjuntado una imagen. Analízala cuidadosamente.\n\n"
            "REGLAS ESTRICTAS:\n"
            "1. REGLA DEL 80/20: Tu respuesta debe ser 80% diagnóstico de lo que observas en la imagen y 20% pregunta guía.\n"
            "2. NO des la solución exacta (ej. 'baja los 500Hz'). Explica tu observación técnica y haz una pregunta (ej. 'Veo una acumulación en medios-bajos, ¿qué pasaría con la claridad si atenuamos ahí?').\n"
            "3. TONO DEL TUTOR: Sé alentador, profesional y analítico.\n"
            "4. SALIDA DE EMERGENCIA: Si la imagen NO es de mezcla o plugin, di: 'Esta imagen no parece de tu DAW o plugin. Sube una captura de tu mezcla para poder guiarte'.\n\n"
            f"--- TEORÍA DEL CURSO ---\n{teoria}\n------------------------\n"
            f"{historial_formateado}\n"
            f"Pregunta del alumno: {state['pregunta']}"
        )
        
        mensaje = [HumanMessage(content=[
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagen_limpia}"}},
            {"type": "text", "text": instrucciones_vision}
        ])]
        
        # Penalizamos repeticiones usando el parámetro nativo de Ollama (NO es OpenAI)
        respuesta = llm_vision.bind(options={"repeat_penalty": 1.5}).invoke(mensaje).content
    else:
        print("🧠 [AGENTE RAG]: Paso 3 - Generando respuesta de texto (Invocando a Llama 3.2, leyendo teoría...)")
        respuesta = llm_logico.invoke(instrucciones + "\nPregunta del alumno: " + state["pregunta"]).content
        
    print("🚀 [AGENTE RAG]: ¡Respuesta generada con éxito!")
    return {"respuesta_final": respuesta}


def nodo_web(state: EstadoAgente):
    """Busca en DuckDuckGo links reales con contexto forzado"""
    print("🌐 [AGENTE WEB]: Conectando a internet...")
    
    # TRUCO NINJA: Le inyectamos contexto a la búsqueda sin que el usuario lo vea
    query_optimizada = state["pregunta"] + " plugins audio VST mezcla masterizacion"
    print(f"🔍 Buscando en DuckDuckGo: {query_optimizada}")
    
    info_web = "No se pudo obtener información de internet a tiempo o hubo un error de red."
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(buscador_web.invoke, query_optimizada)
            info_web = future.result(timeout=15)
    except concurrent.futures.TimeoutError:
        print("⚠️ [AGENTE WEB]: Tiempo de espera agotado en DuckDuckGo Search.")
    except Exception as e:
        print(f"⚠️ [AGENTE WEB]: Error al conectar a internet: {e}")
        
    prompt = (
        "Eres el asistente experto del curso de KENTH. El alumno pidió información externa o recomendaciones.\n"
        "Usa esta información de internet combinada con tu conocimiento para darle una respuesta estelar y precisa:\n"
        f"--- INFO WEB ---\n{info_web}\n----------------\n"
        f"Pregunta original del alumno: {state['pregunta']}"
    )
    respuesta = llm_logico.invoke(prompt).content
    return {"respuesta_final": respuesta}


def nodo_guardia(state: EstadoAgente):
    """Rechaza preguntas fuera de lugar con estilo"""
    print("🛡️ [GUARDIA]: Bloqueando pregunta fuera de dominio...")
    prompt = (
        "Eres KENTH. Un alumno te acaba de preguntar algo que NO tiene nada que ver con producción musical, mezcla o masterización.\n"
        "Rechaza su pregunta de forma educada, usando una metáfora o humor relacionado con el audio o el estudio de grabación para devolverlo al tema principal.\n"
        f"Pregunta del alumno: {state['pregunta']}"
    )
    respuesta = llm_logico.invoke(prompt).content
    return {"respuesta_final": respuesta}


def nodo_saludo(state: EstadoAgente):
    """Ruta rápida para saludos y cortesías sin usar LLM para ahorrar hardware"""
    print("👋 [AGENTE SALUDO]: Respondiendo al instante...")
    pregunta = state["pregunta"].lower()
    
    if "gracias" in pregunta:
        respuesta = "¡De nada! Aquí estoy para ayudarte a sonar como un profesional. ¿Tienes alguna otra duda?"
    elif "ok" in pregunta or "vale" in pregunta or "perfecto" in pregunta or "entendido" in pregunta:
        respuesta = "¡Excelente! Sigamos dándole duro a esas mezclas. 💪"
    elif "adios" in pregunta or "chao" in pregunta or "luego" in pregunta:
        respuesta = "¡Hasta luego! Recuerda confiar en tus oídos. 🎶"
    else:
        respuesta = "¡Hola! Soy KENTH, tu ingeniero de mezcla virtual. ¿En qué te puedo ayudar hoy con tus producciones?"
        
    return {"respuesta_final": respuesta}

# ==========================================
# 4. CONSTRUCCIÓN DEL GRAFO
# ==========================================
flujo = StateGraph(EstadoAgente)

# Añadir los nodos al flujo
flujo.add_node("supervisor", nodo_supervisor)
flujo.add_node("agente_rag", nodo_rag)
flujo.add_node("agente_web", nodo_web)
flujo.add_node("guardia", nodo_guardia)
flujo.add_node("saludo", nodo_saludo)

# Establecer el punto de entrada
flujo.set_entry_point("supervisor")

# Función de enrutamiento condicional
def enrutador(state: EstadoAgente):
    # Si el botón de frontend forzó la ruta a "internet", nos saltamos al supervisor
    if state["ruta"] == "internet":
        return "internet"
    return state["ruta"]

# Crear las rutas
flujo.add_conditional_edges(
    "supervisor",
    enrutador,
    {
        "teoria": "agente_rag",
        "internet": "agente_web",
        "bloqueo": "guardia",
        "saludo": "saludo"
    }
)

# Todos los especialistas terminan el proceso
flujo.add_edge("agente_rag", END)
flujo.add_edge("agente_web", END)
flujo.add_edge("guardia", END)
flujo.add_edge("saludo", END)

# Compilar el Súper-Agente
super_agente = flujo.compile()
