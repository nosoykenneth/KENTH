from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
import concurrent.futures

app = FastAPI()

# ==========================================
# 1. INICIALIZACIÓN DE HERRAMIENTAS Y MODELOS
# ==========================================
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma(persist_directory="./bd_vectorial", embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) 
buscador_web = DuckDuckGoSearchRun()

# El cerebro lógico (llama3.2 de 3b es ideal aquí para que no se equivoque clasificando)
llm_logico = ChatOllama(model="qwen3-vl:4b-instruct", temperature=0.2) 
# El cerebro con ojos
llm_vision = ChatOllama(model="qwen3-vl:4b-instruct", temperature=0.1) 

# ==========================================
# 2. EL ESTADO DEL GRAFO (La memoria compartida)
# ==========================================
class EstadoAgente(TypedDict):
    pregunta: str
    imagen: str
    ruta: str # Aquí el supervisor guardará su decisión
    respuesta_final: str

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
    
    prompt = (
        "Eres un clasificador estricto para un curso de Mezcla y Masterización.\n"
        "Clasifica la siguiente pregunta en UNA de estas tres categorías:\n"
        "1. 'internet': Si el usuario pide descargar algo, un link, un plugin externo (ej. Voxengo SPAN), o noticias actuales.\n"
        "2. 'teoria': Si el usuario pregunta sobre audio, ecualización, compresores, DAWs, o si dice 'qué es esto en la imagen'.\n"
        "3. 'bloqueo': Si el usuario habla de cocina, videojuegos (Geometry Dash), política, o cualquier tema no musical.\n\n"
        "RESPONDE ÚNICA Y EXCLUSIVAMENTE CON UNA DE LAS TRES PALABRAS (internet, teoria, o bloqueo). No digas nada más.\n"
        f"Pregunta: {state['pregunta']}"
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
    print("✅ [AGENTE RAG]: Paso 2 - Documentos encontrados. Preparando texto...")
    
    # TRUCO DE OPTIMIZACIÓN: Si el PDF te devuelve 3 páginas, el modelo se ahoga. 
    # Limitamos el contexto a los primeros 1500 caracteres para que sea un "snare" rápido y no un pad eterno.
    texto_crudo = "\n\n".join(doc.page_content for doc in docs) if docs else "No hay contexto exacto, usa tu conocimiento."
    teoria = texto_crudo[:1500] + "..." if len(texto_crudo) > 1500 else texto_crudo
    
    instrucciones = (
        "Eres KENTH, ingeniero de mezcla profesional.\n"
        "REGLA DE VOCABULARIO: Di 'Ecualizador', 'Filtro Paso Alto/Bajo'. Nunca uses malas traducciones.\n"
        "REGLA DE ORO: Sé extremadamente CONCISO y DIRECTO. Responde en MÁXIMO 1 PÁRRAFO CORTO. Evita largas explicaciones.\n"
        f"--- TEORÍA DEL CURSO ---\n{teoria}\n------------------------\n"
    )

    if state["imagen"]:
        print("👀 [AGENTE RAG]: Paso 3 - Analizando imagen (Invocando a Qwen-Vision)...")
        # PROMPT BLINDADO: Le damos permiso para rechazar la imagen si no es un plugin
        instrucciones_vision = (
            "Eres KENTH, un ingeniero de mezcla profesional.\n"
            "El alumno ha adjuntado una imagen. Analízala cuidadosamente.\n\n"
            "REGLA DE ORO: Si la imagen muestra una interfaz de un DAW, un plugin (Ecualizador, Compresor, etc.) o parámetros de mezcla, descríbelos y da retroalimentación técnica. SE EXTREMADAMENTE CONCISO Y DIRECTO. DA TU DIAGNÓSTICO EN MÁXIMO 1 PÁRRAFO CORTO y ve al grano.\n"
            "SALIDA DE EMERGENCIA: Si la imagen es un micrófono, una guitarra, un paisaje, o CUALQUIER COSA que no sea un plugin de audio, simplemente responde: 'Esta imagen no parece ser de un software de mezcla. Por favor, sube una captura de tu DAW o plugin para poder ayudarte'. No inventes problemas ni repitas frases.\n\n"
            f"--- TEORÍA DEL CURSO ---\n{teoria}\n------------------------\n"
            f"Pregunta del alumno: {state['pregunta']}"
        )
        
        mensaje = [HumanMessage(content=[
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{state['imagen']}"}},
            {"type": "text", "text": instrucciones_vision}
        ])]
        
        # Penalizamos repeticiones usando el parámetro nativo de Ollama (NO es OpenAI)
        respuesta = llm_vision.bind(options={"repeat_penalty": 1.5}).invoke(mensaje).content
    else:
        print("🧠 [AGENTE RAG]: Paso 3 - Generando respuesta de texto (Invocando a Qwen, leyendo teoría...)")
        respuesta = llm_logico.invoke(instrucciones + "\nPregunta: " + state["pregunta"]).content
        
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


# ==========================================
# 5. ENDPOINT DE FASTAPI
# ==========================================
class Consulta(BaseModel):
    pregunta: str
    contexto_leccion: str = ""
    imagen: str = ""
    usar_internet: bool = False # <--- AQUI ESTA TU NUEVO BOTÓN

@app.post("/chat")
def chat_endpoint(consulta: Consulta):
    
    # Si el botón de React está encendido, bypasseamos al supervisor y forzamos la ruta
    ruta_forzada = "internet" if consulta.usar_internet else ""

    estado_inicial = {
        "pregunta": consulta.pregunta,
        "imagen": consulta.imagen,
        "ruta": ruta_forzada, 
        "respuesta_final": ""
    }
    
    # Si forzamos la ruta, el LangGraph saltará directo a donde le dijimos
    resultado = super_agente.invoke(estado_inicial)
    
    return {"respuesta": resultado["respuesta_final"]}
