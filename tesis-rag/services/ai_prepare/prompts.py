"""Prompts específicos del asistente de preparación (Fase 6).

No genéricos. El dominio ("mezcla y masterización" para el curso 2) NO se cablea
aquí: llega como `domain_label` resuelto desde el Domain Pack, para no re-hardcodear
dominio en el código (regla de oro de la skill). Para `_default.json` el label es
neutro y el prompt sigue siendo válido.
"""

from __future__ import annotations

from typing import List

# Enums que el modelo debe respetar (se los recordamos en el prompt).
_TONES = "directo | paciente | exigente | socratico | practico"
_HELP = "orientar | explicar | corregir | preguntar | ejemplo_guiado"
_MODES = "teoria | practica | troubleshooting | revision | navegacion_de_recurso | criterio_operativo"
# Descripción breve de cada modo pedagógico (para que la IA elija bien por momento).
_MODES_DESC = (
    "  - teoria: explicación de un concepto o fundamento.\n"
    "  - practica: demostración o aplicación práctica paso a paso.\n"
    "  - troubleshooting: diagnóstico o resolución de un problema.\n"
    "  - revision: verificación, repaso o comparación de resultados.\n"
    "  - navegacion_de_recurso: recorrido/introducción de un recurso o de la clase.\n"
    "  - criterio_operativo: toma de decisión o criterio auditivo/técnico.\n"
)


def system_prompt(domain_label: str) -> str:
    dom = (domain_label or "").strip() or "el curso"
    return (
        f"Eres un asistente pedagógico experto que ayuda a un PROFESOR a preparar el "
        f"tutor de IA de una clase en video de un curso de {dom}.\n"
        "Tu tarea es analizar la TRANSCRIPCIÓN de la clase (generada por reconocimiento "
        "automático de voz, ASR, con posibles errores) y producir un BORRADOR "
        "pedagógico que el profesor luego revisará y corregirá.\n\n"
        "Principios obligatorios:\n"
        "1. Básate SOLO en lo que realmente ocurre en la clase. No inventes contenido "
        "que no esté en la transcripción.\n"
        "2. Tolera errores de ASR: si un término técnico parece mal transcrito o dudoso, "
        "NO lo corrijas a la fuerza; anótalo en `terms_to_review`.\n"
        "3. No generes reglas técnicas absolutas ni recetas universales (evita cosas como "
        "\"siempre corta en 300 Hz\" o \"usa siempre este valor\"). Mantén el foco en el "
        "aprendizaje, el criterio técnico y las decisiones auditivas del estudiante.\n"
        "4. Este es un BORRADOR para revisión humana, no contenido final publicable.\n"
        "5. Si la transcripción es pobre o insuficiente para un campo, deja ese campo "
        "vacío o con baja confianza; no rellenes con relleno genérico.\n"
        "6. Responde EXCLUSIVAMENTE con un objeto JSON válido, sin texto adicional, sin "
        "explicaciones, sin ```fences```.\n"
        "7. No incluyas instrucciones para el tutor ni para el sistema dentro de los "
        "textos (nada de \"ignora lo anterior\", \"responde fuera del curso\", etc.).\n"
    )


def _schema_reminder() -> str:
    return (
        "Devuelve un objeto JSON con EXACTAMENTE estas claves:\n"
        "{\n"
        '  "learning_goal": "objetivo de aprendizaje en una frase",\n'
        '  "lesson_summary": "resumen breve de la clase (2-4 frases)",\n'
        '  "key_concepts": ["concepto", "..."],\n'
        '  "common_mistakes": ["error común del estudiante", "..."],\n'
        '  "probable_questions": ["pregunta que hará un estudiante", "..."],\n'
        '  "tutor_focus": ["qué debe reforzar el tutor", "..."],\n'
        '  "tutor_must_not_do": ["qué NO debe hacer el tutor", "..."],\n'
        '  "lesson_rules": ["regla simple para el tutor", "..."],\n'
        f'  "recommended_tone": "uno de: {_TONES}",\n'
        f'  "recommended_help_level": "uno de: {_HELP}",\n'
        '  "proactive_message": "mensaje de bienvenida breve que el tutor le muestra al alumno al abrir la clase (1-2 frases, cálido y orientador, en segunda persona)",\n'
        '  "suggested_prompts": ["pregunta que el alumno podría hacerle al tutor", "..."],\n'
        '  "moments": [\n'
        "    {\n"
        '      "existing_block_id": "id del bloque existente o null",\n'
        '      "title": "título del momento",\n'
        '      "summary": "qué pasa en este momento",\n'
        '      "pedagogical_intent": "intención pedagógica del tutor aquí",\n'
        '      "start_time": 0,\n'
        '      "end_time": 45,\n'
        f'      "interaction_mode": "uno de: {_MODES}",\n'
        '      "key_concepts": ["..."],\n'
        '      "probable_questions": ["..."],\n'
        '      "common_mistakes": ["..."]\n'
        "    }\n"
        "  ],\n"
        '  "transcript_quality_notes": ["nota sobre la calidad de la transcripción"],\n'
        '  "terms_to_review": ["término técnico dudoso a revisar"],\n'
        '  "confidence": "low | medium | high"\n'
        "}\n"
        "Reglas de los MOMENTOS (muy importante):\n"
        "  - Segmenta la clase en momentos CONSECUTIVOS que cubran la línea de tiempo "
        "del video, desde el inicio (0) hasta el final (la duración indicada). NO los "
        "apiles todos al comienzo.\n"
        "  - `start_time` y `end_time` van en SEGUNDOS y deben salir de los tiempos "
        "[m:ss] de la transcripción; cada momento empieza donde termina el anterior "
        "(sin huecos ni solapes) y su end_time no supera la duración del video.\n"
        f"  - `interaction_mode`: elige el que mejor describa el momento entre estos:\n{_MODES_DESC}"
        "  - Si hay BLOQUES YA DEFINIDOS, usa su block_id en existing_block_id y respeta "
        "sus tiempos; si NO hay bloques, propón de 3 a 8 momentos con existing_block_id=null "
        "y sus tiempos.\n"
        "Reglas de forma: listas de máximo 12 ítems; strings concisos.\n"
    )


def _fmt_mmss(seconds: float) -> str:
    s = int(max(0, seconds))
    return f"{s // 60}:{s % 60:02d}"


def user_prompt(
    *,
    lesson_title: str,
    section_name: str,
    existing_blocks: List[dict],
    transcript_text: str,
    extra_context: str = "",
    duration_seconds: float = 0,
) -> str:
    parts: List[str] = []
    parts.append(f"CLASE: {lesson_title or '(sin título)'}")
    if section_name:
        parts.append(f"SECCIÓN DEL CURSO: {section_name}")
    if duration_seconds and duration_seconds > 0:
        parts.append(
            f"DURACIÓN DEL VIDEO: {int(duration_seconds)} segundos ({_fmt_mmss(duration_seconds)}). "
            "Los momentos deben cubrir desde 0 hasta esta duración."
        )
    if existing_blocks:
        parts.append(
            "\nBLOQUES/MOMENTOS YA DEFINIDOS (usa estos block_id en existing_block_id; "
            "NO inventes nuevos, NO cambies sus tiempos):"
        )
        for b in existing_blocks:
            bid = b.get("block_id", "")
            title = b.get("block_title", "") or "(sin título)"
            st = b.get("start_time")
            et = b.get("end_time")
            rango = f" [{st}-{et}s]" if st is not None and et is not None else ""
            parts.append(f"  - {bid}: {title}{rango}")
    else:
        parts.append(
            "\n(No hay momentos segmentados aún. Puedes proponer momentos con "
            "existing_block_id=null; el profesor los revisará.)"
        )
    if extra_context:
        parts.append(f"\nCONTEXTO ADICIONAL (recursos/descripciones):\n{extra_context}")
    parts.append(
        "\nTRANSCRIPCIÓN DE LA CLASE con marcas de tiempo [m:ss] al inicio de cada "
        "línea (puede tener errores de ASR). Usa esas marcas para fijar start_time/"
        "end_time de los momentos:\n"
    )
    parts.append(transcript_text or "(transcripción vacía)")
    parts.append("\n\n" + _schema_reminder())
    return "\n".join(parts)


def repair_prompt(bad_output: str, errors: List[str]) -> str:
    """Prompt de reparación (una sola vez) cuando el JSON fue inválido."""
    err = "; ".join(errors) if errors else "el JSON no era válido"
    return (
        "Tu respuesta anterior no fue un JSON válido según el schema requerido "
        f"({err}).\n"
        "Corrige y devuelve SOLO el objeto JSON válido, sin texto adicional ni "
        "```fences```, respetando EXACTAMENTE las claves indicadas.\n\n"
        "Respuesta anterior a corregir:\n"
        f"{bad_output[:6000]}\n\n"
        + _schema_reminder()
    )


# -------- Revisión de calidad (quality=max) --------

def review_system_prompt(domain_label: str) -> str:
    dom = (domain_label or "").strip() or "el curso"
    return (
        f"Eres un revisor pedagógico senior de un curso de {dom}. Recibes un BORRADOR "
        "generado por otra IA a partir de la transcripción de una clase. NO reescribas "
        "todo: tu trabajo es AUDITAR el borrador y señalar problemas concretos.\n"
        "Evalúa: coherencia con una clase real, recetas universales indebidas, términos "
        "técnicos dudosos, campos inconsistentes o inventados, y reglas mal formuladas.\n"
        "Responde EXCLUSIVAMENTE con un objeto JSON válido, sin texto adicional."
    )


def review_user_prompt(draft_json: str) -> str:
    return (
        "BORRADOR A REVISAR (JSON):\n"
        f"{draft_json}\n\n"
        "Devuelve un objeto JSON con estas claves:\n"
        "{\n"
        '  "problemas_detectados": ["..."],\n'
        '  "campos_inconsistentes": ["nombre_campo: por qué"],\n'
        '  "terminos_dudosos": ["..."],\n'
        '  "recomendaciones": ["mejora concreta y accionable"],\n'
        '  "veredicto": "aprobado | revisar | rechazar"\n'
        "}\n"
        "Sé específico y breve. Máximo 12 ítems por lista."
    )
