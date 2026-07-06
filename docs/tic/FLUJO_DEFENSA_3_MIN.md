# Flujo de defensa — video de 3 minutos

> Guion técnico + checklist de grabación. Secuencia visual: `diagramas.md` §11.
> Objetivo: demostrar el ciclo completo *login → curso → lección → H5P →
> orientación automática del tutor* sin tiempos muertos.

## 1. Guion técnico (3:00)

| t | Escena | Acción exacta | Narración sugerida |
|---|---|---|---|
| 0:00–0:15 | Login | Abrir la SPA, iniciar sesión con el usuario estudiante de demo | "Esta es la plataforma del curso de mezcla y masterización, integrada con Moodle y con un tutor de IA local." |
| 0:15–0:35 | Estructura | Dashboard → curso 2 → mostrar secciones; abrir **Sección 0 — El sistema de decisión** (7 lecciones) | "El curso se organiza en secciones y lecciones; toda la Sección 0 está poblada por el flujo docente: el profesor sube recursos y aprueba transcripciones desde la interfaz." |
| 0:35–0:55 | Lección + recursos | Abrir una lección (recomendada: **Lección 5 — Gain Staging**, SEC2-R59); mostrar el panel de recursos de la lección | "Cada lección tiene su video interactivo y recursos reales: bitácoras, plantillas del DAW, audios de referencia." |
| 0:55–1:30 | Video H5P | Reproducir unos segundos; responder 2–3 interacciones **fallando al menos 2 a propósito** | "El video incluye evaluación formativa H5P. Las respuestas quedan en Moodle y se transforman en señales de aprendizaje." |
| 1:30–1:50 | Orientación automática | Con el chat cerrado: aparece el badge **"Conviene reforzar · el tutor tiene una guía"** + flecha con contador (+sonido). Clic en **"Ver guía del tutor"** | "El tutor detecta los conceptos débiles y me avisa. La guía no se pierde: puedo recuperarla cuando quiera." |
| 1:50–2:20 | Guía del tutor | Se abre el chat con la orientación: conceptos priorizados, **minuto exacto del video, recurso de la lección y micro-práctica** | "La orientación es determinística y verificable: minuto exacto, recurso real de la lección y una práctica corta. Nunca es punitiva." |
| 2:20–2:45 | Pregunta al tutor | Escribir una pregunta de seguimiento (p. ej. *"¿por qué mi mezcla clipea si bajé el master?"*); mostrar la respuesta con fuentes | "El tutor responde anclado a la evidencia del curso —RAG con modelos locales— y con el tono y nivel de ayuda que configuró el profesor." |
| 2:45–3:00 | Cierre | Volver al curso; opcional: 3 s de la Vista Profesor (timeline de momentos) | "Todo el conocimiento del tutor lo gobierna el docente desde la interfaz. Gracias." |

## 2. Checklist para grabar

**Antes (preparación):**
- [ ] Usuario estudiante de demo matriculado en el curso 2, sin intentos previos
      en la lección elegida (o limpiar su intento para que la guía sea fresca).
- [ ] Verificar `GET /api/ai/health` → todo `ok`.
- [ ] Probar el flujo completo UNA vez fuera de cámara (calienta Ollama: la
      primera respuesta del chat es más lenta).
- [ ] Cerrar el panel del tutor antes de responder el H5P (para que se vea el
      badge + flecha + sonido).
- [ ] Audio del sistema activado (el aviso sonoro es sutil).
- [ ] Ventana en resolución 1920×1080, zoom 100%, tema consistente.

**Qué mostrar:**
- [ ] Badge "Conviene reforzar · el tutor tiene una guía" con el botón "Ver guía".
- [ ] La guía con ≥2 conceptos numerados (fallar 2+ interacciones lo garantiza).
- [ ] El minuto y el nombre del recurso dentro del mensaje.
- [ ] Las fuentes de la respuesta del chat (grounding visible).

**Qué NO mostrar:**
- [ ] Vistas de admin técnico (editor avanzado, ids internos, JSON).
- [ ] Grafana/logs, terminal, docker.
- [ ] Tokens, URLs internas, credenciales.
- [ ] El chat general para la parte de señales (la personalización es POR lección).

**Plan B (si algo falla en vivo):**
- Si la guía no aparece en ~10 s: el sync corre en polling 30 s; repetir la
  última interacción del video o reabrir la lección (la guía persistida
  reaparece por el badge).
- Si el chat tarda: el timeout muestra fallback con reintento — narrar
  "los modelos son locales" y reintentar.

## 3. Métricas listas para citar en la defensa

- 7 lecciones H5P InteractiveVideo, 29 interacciones calificables.
- Chroma: 241 chunks del curso, canonical_md Sección 0 = 0 (teacher-driven).
- Batería de retrieval 21/21; suite backend 263 tests verdes; contratos
  frontend 3/3.
- Guidance multi-concepto priorizada (máx. 3) + recuperable (persistencia local
  7 días, dedupe por intento).
