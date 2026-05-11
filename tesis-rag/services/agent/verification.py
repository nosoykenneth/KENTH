import re
import os

from services.agent.routing import _normalizar_texto


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
    """Respuestas cortas para preguntas observadas con alto riesgo de desanclaje."""
    q = _normalizar_texto(pregunta)

    if "frecuencia" in q and "tono" in q and ("diferencia" in q or "diferencia hay" in q):
        return (
            "La frecuencia es una magnitud fisica medible: cuantas veces vibra una senal por segundo. "
            "El tono es la percepcion auditiva asociada a esa frecuencia: como sentimos si algo es mas grave o mas agudo. "
            "No son lo mismo: una es medicion fisica y la otra es percepcion."
        )

    if "espuma" in q and ("grave" in q or "graves" in q):
        return (
            "No necesariamente. En el marco de acustica del curso, la espuma puede ayudar con reflexiones o contenido medio-agudo, "
            "pero no conviene tratarla como solucion automatica para graves inflados. Para graves suele hacer falta diagnosticar sala, "
            "modos/resonancias y tratamiento adecuado, no solo pegar espuma."
        )

    if "serie" in q and "paralelo" in q and ("diferencia" in q or "diferencia hay" in q):
        return (
            "En serie, la senal pasa por un proceso y luego por el siguiente: el orden cambia el resultado. "
            "En paralelo, una copia o envio se procesa por otra ruta y luego se mezcla con la senal original. "
            "La diferencia practica es flujo: cadena unica versus rutas simultaneas que se recombinan."
        )

    if "frecuencia de corte" in q and any(patron in q for patron in ["que es", "explicame", "defineme", "define"]):
        return (
            "La frecuencia de corte es un punto de referencia tecnico dentro del comportamiento de un filtro. "
            "Sirve para ubicar desde donde se entiende o se mide la transicion del filtro, pero no debe pensarse como un muro instantaneo. "
            "Algunas definiciones usan referencias numericas segun el tipo de filtro o contexto, pero no conviene fijarlas como doctrina universal cerrada sin matiz."
        )

    if "compresor" in q and any(patron in q for patron in ["que hace", "que es", "para que sirve"]):
        return (
            "Un compresor controla la dinamica: reduce o contiene el excedente de una senal cuando supera un umbral, "
            "segun parametros como ratio, ataque y release. En la practica no es un boton de mejora automatica; sirve para ordenar, sostener o moldear movimiento dinamico segun el problema."
        )

    if (
        ("comprimir" in q or "comprimo" in q or "compresion" in q)
        and ("ecualizador" in q or "ecualizacion" in q or " eq " in f" {q} ")
    ):
        return (
            "Tecnicamente no se comprime un ecualizador: se comprime una senal con un compresor y se ecualiza con un EQ. "
            "Si te refieres a controlar una frecuencia solo cuando se dispara, eso se parece mas a ecualizacion dinamica o compresion multibanda. "
            "Primero identifica el problema: balance tonal, resonancia puntual o exceso dinamico en una banda."
        )

    if "master" in q and ("clipea" in q or "clip" in q) and "bien" in q:
        return (
            "No. Que el master no clipee solo indica que no esta superando ese limite de pico. "
            "No demuestra por si solo que el flujo de nivel, el margen, la dinamica, el balance o la traduccion esten bien. "
            "Es una condicion tecnica basica, no una validacion completa."
        )

    if "revisar en mono" in q or ("por que" in q and "mono" in q):
        return (
            "Porque al cerrar a mono aparecen problemas de suma que en estereo pueden quedar disimulados. "
            "Si elementos importantes como voz, bombo, caja o bajo pierden solidez, hay un problema real de compatibilidad. "
            "La revision en mono no busca que todo sea estrecho, sino comprobar que la mezcla no se desarme fuera del punto ideal de escucha."
        )

    if "polaridad" in q and ("invierto" in q or "invertir" in q or "inversion" in q):
        return (
            "No necesariamente. Invertir polaridad puede resolver casos donde dos senales estan opuestas de forma binaria, "
            "pero no corrige cualquier problema de fase o de tiempo. Si el conflicto viene de retraso, alineacion o filtrado peine, "
            "hay que diagnosticar la relacion temporal, no solo apretar el boton de polaridad."
        )

    if "mezclar bien" in q and ("plugin" in q or "plugins" in q or "aplicar" in q):
        return (
            "No. Mezclar bien no es aplicar plugins a todo. Desde la practica integradora, primero se diagnostica que problema existe, "
            "que jerarquia tiene cada elemento, que pasa en contexto y cual es el costo de intervenir. Si una fuente ya cumple su funcion, procesarla por reflejo puede empeorar la mezcla."
        )

    if "correlacion" in q or "correlaci" in q or "correlator" in q or "correlometro" in q:
        return (
            "En este curso, correlacion se entiende como una lectura de relacion entre canales o senales para estimar como suman "
            "y que tan compatibles son al revisar mono. Sirve como orientacion: valores muy positivos suelen indicar suma mas estable, "
            "y valores negativos advierten posible cancelacion. No es una verdad absoluta; hay que leerla por contexto, por bandas y por rol musical."
        )

    return ""
