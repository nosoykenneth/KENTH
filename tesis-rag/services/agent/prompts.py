TEXT_MODEL_NAME = "llama3.2:3b"

PROMPT_COMMON_RULES = (
    "--- REGLAS COMUNES DEL TUTOR ---\n"
    "- Usa fuente del curso como evidencia principal cuando answer_type no sea web_answer.\n"
    "- Prioriza 'Contenido Canonico' para definiciones y conceptos fundamentales.\n"
    "- Prioriza 'Paquete Limpio' para matrices de error, heuristica y criterio operativo.\n"
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


def _campos_pedagogicos(state: dict, **overrides):
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
