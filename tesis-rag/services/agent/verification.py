import re
import os

from services.agent.routing import _normalizar_texto, _warning
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

    # 2. Detectar mencion de secciones no presentes en evidencia
    secciones_evidencia = set()
    for item in evidencias:
        meta = item["document"].metadata or {}
        seccion = (
            meta.get("section_number")
            or meta.get("section_title")
            or meta.get("moodle_section_id")
        )
        if seccion not in (None, ""):
            # Normalizar a solo digitos (ej: "Seccion 4" / "4" -> "4")
            digitos = re.sub(r"\D", "", str(seccion))
            if digitos:
                secciones_evidencia.add(digitos)

    secciones_mencionadas = set(re.findall(r'(?:[Ss]ecci[oó]n)\s*(\d+)', respuesta))
    secciones_inventadas = {s for s in secciones_mencionadas if s not in secciones_evidencia}
    if secciones_inventadas:
        problemas.append(f"Secciones mencionadas sin evidencia: {secciones_inventadas}")

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
            or recurso_norm in {"01_contenido_canonico", "02_paquete_limpio", "contenido_canonico"}
            or "contenido canonico" in recurso_norm
            or re.search(r"\bseccion[ _]?\d", recurso_norm) is not None
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
            and any(token in norm for token in ["clase", "modulo", "recurso", "guia", "seccion"])
        )
        if recomienda_ubicacion:
            continue
        oraciones = []
        for oracion in parrafo.split(". "):
            oracion_norm = _normalizar_texto(oracion)
            cita_ubicacion_interna = (
                "seccion" in oracion_norm
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


def _limitar_anticipo_seccion_posterior(respuesta: str, requested_section: int):
    """Reduce respuestas de secciones posteriores a un anticipo breve.

    La proteccion ACTIVA contra adelantar secciones posteriores vive en el prompt
    curricular de graph.py y en la penalizacion de retrieval por seccion futura;
    este helper queda disponible para recortes deterministas puntuales (migrado de
    la antigua taxonomia por eje, conserva la proteccion en lenguaje de seccion).
    """
    if not respuesta:
        return respuesta

    norm = _normalizar_texto(respuesta)
    prefijo = (
        f"Eso pertenece a la Seccion {requested_section}, que veras mas adelante. "
        if requested_section is not None and "mas adelante" not in norm
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


# ==========================================================================
# FIX G — Verificacion POST-generacion de attribution_constraints (regla 10)
# ==========================================================================
# Las `attribution_constraints` de la leccion entran al prompt como normas
# obligatorias (context_service), pero hasta aqui nadie comprobaba que la salida
# las cumpliera => cumplimiento no observable. Enfoque elegido (hibrido):
#   1) Capa DETERMINISTA siempre activa: reglas/patrones que viven como DATOS en
#      el Domain Pack (`attribution_verifiers`), no en el codigo. Mapean el texto
#      libre de la restriccion a un patron de violacion en la respuesta y una
#      reparacion suave. Rapida, sin LLM, 100% testeable.
#   2) Capa LLM-juez OPCIONAL (flag ATTR_LLM_JUDGE=1): para restricciones que
#      ninguna regla cubre (p. ej. "atribuye al criterio del autor"). Apagada por
#      defecto => comportamiento determinista y suite estable.
# Accion ante incumplimiento: OBSERVAR (applied_policies + warnings) + REPARAR
# SUAVE el fragmento infractor cuando es localizable. Nunca re-genera.

# Negaciones que invalidan un "match" de violacion: si el marcador viene negado
# ("no garantizo", "sin prometer"...) la respuesta en realidad CUMPLE.
_NEGADORES_ATRIBUCION = (" no ", " nunca ", " sin ", " jamas ", " tampoco ", " ni ")


def _violacion_negada(texto_norm: str, inicio: int, ventana: int = 18) -> bool:
    """True si el marcador en `inicio` viene precedido por una negacion cercana."""
    fragmento = " " + texto_norm[max(0, inicio - ventana):inicio] + " "
    return any(neg in fragmento for neg in _NEGADORES_ATRIBUCION)


def _constraint_casa_detector(constraint_norm: str, detector: dict) -> bool:
    return any(m in constraint_norm for m in (detector.get("constraint_markers") or []))


def _detectar_violacion_atribucion(respuesta_norm: str, detector: dict) -> str:
    """Primer marcador de violacion presente (no negado), o "" si no hay."""
    for marcador in detector.get("violation_markers") or []:
        if not marcador:
            continue
        idx = respuesta_norm.find(marcador)
        while idx != -1:
            if not _violacion_negada(respuesta_norm, idx):
                return marcador
            idx = respuesta_norm.find(marcador, idx + 1)
    return ""


def _reparar_atribucion_suave(respuesta: str, detector: dict) -> str:
    """Sustituye los fragmentos infractores localizables por equivalentes suaves.

    Opera sobre el texto CRUDO (case-insensitive). Si la violacion se detecto por
    una variante no listada en `repairs`, no se toca el texto: igual se registra
    la politica/warning (cumplimiento observable aunque la reparacion no aplique).
    """
    reparada = respuesta
    for par in detector.get("repairs") or []:
        if not isinstance(par, (list, tuple)) or len(par) != 2:
            continue
        patron, reemplazo = par
        reparada = re.sub(re.escape(patron), reemplazo, reparada, flags=re.IGNORECASE)
    return reparada


def verificar_attribution_constraints(respuesta, constraints, *, course_id=None, judge=None):
    """Impone las attribution_constraints en la salida (FIX G).

    Devuelve `(respuesta_ajustada, applied_policies, warnings)`. No muta estado;
    el nodo del grafo decide como anexar las politicas/warnings a su retorno.
    """
    constraints = [c for c in (constraints or []) if isinstance(c, str) and c.strip()]
    if not constraints or not respuesta:
        return respuesta, [], []

    pack = get_domain_pack(course_id) if course_id else _PACK
    detectores = pack.attribution_verifiers()
    applied_policies: list = []
    warnings: list = []

    constraints_norm = [(c, _normalizar_texto(c)) for c in constraints]
    cubiertas: set = set()  # indices de restricciones que cubre la capa determinista

    for det in detectores:
        casa_idx = [i for i, (_, cn) in enumerate(constraints_norm) if _constraint_casa_detector(cn, det)]
        if not casa_idx:
            continue
        cubiertas.update(casa_idx)
        marcador = _detectar_violacion_atribucion(_normalizar_texto(respuesta), det)
        if not marcador:
            continue
        respuesta = _reparar_atribucion_suave(respuesta, det)
        policy = det.get("policy") or det.get("id") or "attribution_violation"
        if policy not in applied_policies:
            applied_policies.append(policy)
        warnings.append(_warning(
            det.get("warning_code") or "ATTRIBUTION_VIOLATED",
            det.get("message") or "Restriccion de conducta de la leccion incumplida; salida ajustada.",
        ))

    # Restricciones que ninguna regla determinista cubre (semanticas).
    no_cubiertas = [c for i, (c, _) in enumerate(constraints_norm) if i not in cubiertas]
    if no_cubiertas:
        usar_juez = judge is not None and os.getenv("ATTR_LLM_JUDGE", "0") == "1"
        if usar_juez:
            try:
                veredicto = judge(respuesta, no_cubiertas) or {}
            except Exception as e:  # el juez nunca debe tumbar la respuesta
                print(f"[VERIFICADOR ATRIBUCION]: juez LLM fallo, se omite: {e}")
                veredicto = {}
            violaciones = [v for v in (veredicto.get("violaciones") or []) if v]
            corregida = veredicto.get("respuesta_corregida")
            if violaciones:
                if "attribution_llm_violation" not in applied_policies:
                    applied_policies.append("attribution_llm_violation")
                for v in violaciones:
                    warnings.append(_warning("ATTRIBUTION_LLM_VIOLATION", f"Juez semantico marco incumplimiento: {v}"))
                if isinstance(corregida, str) and corregida.strip():
                    respuesta = corregida.strip()  # reparacion suave del juez
        else:
            # Gap OBSERVABLE: hay restricciones solo verificables semanticamente y
            # la capa LLM esta apagada. No se finge cumplimiento; se declara.
            warnings.append(_warning(
                "ATTRIBUTION_UNVERIFIED_SEMANTIC",
                f"{len(no_cubiertas)} restriccion(es) de la leccion solo son verificables "
                "semanticamente; capa LLM (ATTR_LLM_JUDGE) desactivada.",
            ))

    if applied_policies or warnings:
        print(f"[VERIFICADOR ATRIBUCION]: policies={applied_policies} "
              f"warnings={[w['code'] for w in warnings]}")
    return respuesta, applied_policies, warnings
