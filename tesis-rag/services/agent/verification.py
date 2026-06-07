import re
import os

from services.agent.routing import _normalizar_texto
from services.domain import get_domain_pack

# Fase 0: las respuestas conceptuales controladas (antes hardcodeadas aqui) viven
# como datos en el Domain Pack (controlled_answers). _PACK resuelve el curso por
# defecto para el piloto mono-curso.
_PACK = get_domain_pack()


def _verificar_respuesta(respuesta: str, fuentes: list, evidencias: list):
    """Ultima linea de defensa: detecta alucinaciones obvias en la respuesta."""
    respuesta_norm = _normalizar_texto(respuesta)
    problemas = []

    # 1. Detectar URLs inventadas (no deben existir salvo que esten en evidencia)
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

    # 2. Detectar mencion de ejes no presentes en evidencia
    ejes_evidencia = set()
    for item in evidencias:
        meta = item["document"].metadata or {}
        eje = meta.get("axis") or meta.get("eje") or meta.get("module") or meta.get("modulo")
        if eje:
            # Normalizar para comparar (ej: "Eje 4" -> "4")
            val = str(eje).lower().replace("eje", "").replace("axis", "").strip()
            if val:
                ejes_evidencia.add(val)
    
    ejes_mencionados = set(re.findall(r'(?:[Ee]je|[Aa]xis)\s*(\d+)', respuesta))
    ejes_inventados = {e for e in ejes_mencionados if e not in ejes_evidencia}
    if ejes_inventados:
        problemas.append(f"Ejes mencionados sin evidencia: {ejes_inventados}")

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
        filename = os.path.splitext(fuente.get("filename") or "")[0]
        recurso_norm = _normalizar_texto(recurso)
        filename_norm = _normalizar_texto(filename)
        recurso_generico = (
            not recurso_norm
            or recurso_norm == filename_norm
            or recurso_norm in {"01_contenido_canonico", "02_paquete_limpio"}
            or any(f"eje{i}" in recurso_norm for i in range(8))
        )
        if recurso and not recurso_generico:
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
            and any(token in norm for token in ["clase", "modulo", "eje", "axis", "recurso", "guia", "seccion"])
        )
        if recomienda_ubicacion:
            continue
        oraciones = []
        for oracion in parrafo.split(". "):
            oracion_norm = _normalizar_texto(oracion)
            cita_ubicacion_interna = (
                "eje" in oracion_norm
                or "axis" in oracion_norm
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


def _recortar_relleno_sin_evidencia(respuesta: str):
    norm = _normalizar_texto(respuesta)
    marcas_sin_evidencia = [
        "no hay evidencia",
        "no tengo evidencia",
        "no tengo suficiente evidencia",
        "no hay suficiente informacion",
        "no menciona explicitamente",
        "no menciona directamente",
        "evidencia proporcionada no menciona",
    ]
    if not any(marca in norm for marca in marcas_sin_evidencia):
        return respuesta

    conectores_relleno = ["sin embargo", "aunque", "en general", "podria", "puede entenderse"]
    if len(respuesta) < 450 and not any(conector in norm for conector in conectores_relleno):
        return respuesta

    return (
        "No tengo evidencia suficiente en el material del curso para responder eso con seguridad. "
        "Para no inventar, dame una aclaracion breve sobre el concepto o contexto exacto."
    )


def _limpiar_citas_internas_rag(respuesta: str):
    limpia = re.sub(r"\s*\([^)]*Fuente\s+\d+[^)]*\)", "", respuesta, flags=re.IGNORECASE)
    limpia = re.sub(r"\bFuente\s+\d+\s*\|[^.\n]*(?:\.|$)", "", limpia, flags=re.IGNORECASE)
    limpia = re.sub(r"\bFuente\s+\d+\b[:\-]?\s*", "", limpia, flags=re.IGNORECASE)
    limpia = re.sub(r"\bE\d+-L\d{2}-B\d+\b\s*[-–—:]?\s*", "", limpia, flags=re.IGNORECASE)
    limpia = re.sub(r"\bE\d+-L\d{2}\b\s*[-–—:]?\s*", "", limpia, flags=re.IGNORECASE)
    limpia = re.sub(r"\bleccion piloto\b", "leccion actual", limpia, flags=re.IGNORECASE)
    limpia = re.sub(r"\blección piloto\b", "leccion actual", limpia, flags=re.IGNORECASE)
    limpia = re.sub(r"[ \t]{2,}", " ", limpia)
    limpia = re.sub(r"\n{3,}", "\n\n", limpia)
    return limpia.strip()


def _limitar_anticipo_eje_posterior(respuesta: str, requested_axis: int):
    """Reduce respuestas de ejes posteriores a un anticipo breve."""
    if not respuesta:
        return respuesta

    norm = _normalizar_texto(respuesta)
    prefijo = (
        f"Eso pertenece al Eje {requested_axis}, que veras mas adelante. "
        if requested_axis is not None and "mas adelante" not in norm
        else ""
    )

    texto = re.sub(r"\s+", " ", respuesta).strip()
    oraciones = re.split(r"(?<=[.!?])\s+", texto)
    recortada = " ".join(oraciones[:4]).strip()
    return (prefijo + recortada).strip()


def _respuesta_conceptual_controlada(pregunta: str):
    """Respuestas cortas para preguntas con alto riesgo de desanclaje.

    Fase 0: las reglas (terminos disparadores) y los textos viven en el Domain
    Pack (controlled_answers), no en codigo. Una regla casa si TODOS sus grupos
    casan, y un grupo casa si ALGUNO de sus terminos esta en la pregunta. El match
    usa la pregunta normalizada y PADEADA con espacios, para que terminos como
    " eq " casen como palabra. Orden = primer match gana (igual que el if/elif
    original). Devuelve "" si ninguna regla casa.
    """
    q = _normalizar_texto(pregunta)
    padded = f" {q} "
    for rule in _PACK.controlled_answers():
        grupos = rule.get("all_of") or []
        if grupos and all(any(term in padded for term in grupo) for grupo in grupos):
            return rule.get("answer", "")
    return ""
