# CHAT_VALIDATION — Sección 0 (curso 2)

Validación del tutor por **invocación directa del agente** (sin HTTP/token), con el
flujo docente aplicado. Modelo de chat local: `llama3.2:3b` (KENTH_TEXT_MODEL).
Script reproducible: `scripts/chat_validate_section0.py`. Datos: `chat_validation.json`.

> Alcance local: sólo SEC2-R55 y SEC2-R56 existen en la BD local. R57–R61 se validan
> en el servidor con el mismo script tras el runbook.

## Resultado por lección

### SEC2-R55 — 0.1 "Mezclar es decidir: el ciclo de trabajo"

| Pregunta | ruta | scope | evidencia | Veredicto |
|---|---|---|---|---|
| ¿De qué trata esta lección? | teoria | lesson | alto | ✅ nombra la lección + Sección 0, describe el ciclo |
| ¿Cuáles son los pasos del ciclo de trabajo? | teoria | lesson | alto | ✅ Escuchar, Diagnosticar, Decidir, Actuar, Verificar (de la transcripción nueva) |
| ¿Cómo verifico honestamente si un cambio mejoró? | teoria | lesson | alto | ✅ "comparar con el volumen igualado" (de la transcripción nueva) |

### SEC2-R56 — 0.2 "Tu oído miente: percepción y nivel de escucha"

| Pregunta | ruta | scope | evidencia | Veredicto |
|---|---|---|---|---|
| ¿De qué trata esta lección? | teoria | lesson | alto | ✅ percepción, volumen, fenómenos de escucha |
| ¿Por qué se dice que el oído miente? | teoria | lesson | alto | ✅ "no es un instrumento neutral, distorsiona la percepción" |
| ¿Qué hacer con el nivel de escucha? | teoria | lesson | alto | ✅ "moderado y constante" |

## Casos borde

| Caso | Esperado | ruta | Resultado |
|---|---|---|---|
| Fuera de dominio ("¿capital de Francia?") | rechazar | `bloqueo` (`blocked_by=out_of_domain:semantic`) | ✅ "Solo puedo ayudarte con mezcla, masterización…" |

## Criterios de respuesta (Fase 11)

| Criterio | Resultado |
|---|---|
| Usa la lección correcta (sin cruces) | ✅ `scope=lesson`, sin herencia de otra lección |
| No expone IDs técnicos (`SEC2-R…`) en la respuesta | ✅ (título humano, no id) |
| No inventa si no hay fuente | ✅ (out-of-domain rechazado) |
| `retrieval_scope` coherente | ✅ `lesson` en todas |
| Fuera de dominio rechazado | ✅ |
| No usar "según la evidencia" como muletilla | ⚠️ **hallazgo** (ver abajo) |

## Hallazgo (no oculto)

El modelo local `llama3.2:3b` antepone con frecuencia **"Según la evidencia del
curso…"**. Es una muletilla del modelo, **no** proviene del prompt ni del Domain
Pack (verificado por grep), y **no** la introduce el flujo docente. En producción el
tutor usa `llama3.1:8b`, cuya redacción difiere. Se documenta como observación
pre-existente y de-riesgo bajo; una corrección segura (sin tocar los prompts
baselined en phase0) sería un *soft-strip* del prefijo en `verification.py`, dejado
como follow-up para no arriesgar el gate phase0 en este cambio.

**Conclusión:** el flujo docente entrega respuestas **grounded por lección**, con
scope correcto, sin fuga de IDs ni de otra lección, y con rechazo fuera de dominio.
