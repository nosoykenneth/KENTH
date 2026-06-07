from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from services.domain import get_domain_pack

VISION_MODEL_NAME = "qwen3-vl:4b-instruct"
llm_vision = ChatOllama(model=VISION_MODEL_NAME, temperature=0.1)

# Fase 0: los prompts de vision viven en el Domain Pack (datos), no aqui.
# _PACK resuelve el curso por defecto para el piloto mono-curso.
_PACK = get_domain_pack()
VISION_CLASSIFY_PROMPT = _PACK.node_prompt("vision_classify")
VISION_CAPTION_PROMPT = _PACK.node_prompt("vision_caption")
VISION_NO_EVIDENCE_PROMPT = _PACK.node_prompt("vision_no_evidence")


def _limpiar_imagen_base64(imagen: str):
    if "," in imagen:
        return imagen.split(",", 1)[1]
    return imagen


def _imagen_parece_audio(imagen: str):
    imagen_limpia = _limpiar_imagen_base64(imagen)
    print(f"[VISION GATE]: Imagen recibida. base64_len={len(imagen_limpia)}")
    prompt = VISION_CLASSIFY_PROMPT
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


def describir_imagen_para_conocimiento(imagen_b64: str) -> str:
    """Genera un borrador de descripción de una imagen (captura de plugin/DAW) para
    usar como conocimiento del tutor. Lo usa el botón 'sugerir con IA' al subir."""
    img = _limpiar_imagen_base64(imagen_b64)
    prompt = VISION_CAPTION_PROMPT
    mensaje = [HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img}"},
    ])]
    try:
        return (llm_vision.invoke(mensaje).content or "").strip()
    except Exception as e:
        print(f"[VISION CAPTION]: error {e}")
        return ""


def _responder_imagen_audio_sin_evidencia(imagen_limpia: str, pregunta: str):
    print("[VISION NODE]: Nodo visual activo. Descripcion visual solamente.")
    prompt = VISION_NO_EVIDENCE_PROMPT + f"Pregunta del alumno: {pregunta}"
    mensaje = [HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{imagen_limpia}"}
    ])]
    respuesta = llm_vision.bind(options={"repeat_penalty": 1.5}).invoke(mensaje).content
    print(f"[VISION NODE]: Respuesta vision_len={len(respuesta or '')}")
    return respuesta
