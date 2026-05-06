from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

VISION_MODEL_NAME = "qwen3-vl:4b-instruct"
llm_vision = ChatOllama(model=VISION_MODEL_NAME, temperature=0.1)


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
