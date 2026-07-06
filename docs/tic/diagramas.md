# Diagramas — TIC KENTH

Diagramas en Mermaid (renderizables en GitHub/VS Code). Actualizados al cierre
funcional de julio 2026 (Sección 0 teacher-driven + H5P learning_signals +
tutor adaptativo). Diagramas 1–6: base del sistema; 7–11: flujo docente RAG,
señales H5P, contexto del tutor, estados de la guía y secuencia de defensa.

---

## 1. Arquitectura general (SOA tras API Gateway)

```mermaid
flowchart TD
  Browser["Navegador — SPA React (Vite)"]
  GW["tic-gateway — nginx :8090→80<br/>rate-limit + timeouts"]
  FA["tic-fastapi — LangGraph/RAG :8000"]
  MO["tic-moodle — PHP 5.0 :8091→8080<br/>local_tesisai + api_persistente"]
  DB[("tic-mariadb :3306<br/>Moodle + mdl_local_tesisai_*")]
  CH[("Chroma — bd_vectorial")]
  OL["Ollama NATIVO host :11434 (GPU)"]
  OBS["Loki / Promtail / Grafana"]

  Browser -->|/api/ai/*| GW
  Browser -->|/api/lms/*| GW
  GW -->|/api/ai/*| FA
  GW -->|/api/lms/ /moodle/| MO
  FA -->|Web Services| MO
  FA --> CH
  FA -->|chat / embed / visión| OL
  MO --> DB
  FA -->|auth + mdl_local_tesisai_*| DB
  GW -. logs JSON .-> OBS
```

---

## 2. Componentes

```mermaid
flowchart LR
  subgraph Cliente
    SPA["SPA React<br/>estudiante + editor docente/admin"]
  end
  subgraph Gateway
    NGX["nginx.full.conf<br/>/api/ai → FastAPI<br/>/api/lms → Moodle"]
  end
  subgraph Backend_IA["FastAPI / IA"]
    API["api/routes/*"]
    AG["services/agent (supervisor→rag/web/guardia/saludo/perdido)"]
    RET["retrieval + verification"]
    CTX["context_service (Capas 2/3)"]
    DP["domain_packs/<course>.json"]
    DBS["db_service (Moodle-first)"]
  end
  subgraph Moodle
    PLG["local_tesisai (WS + esquema)"]
    APIP["api_persistente (auth/pagos/roles)"]
  end
  SPA --> NGX --> API
  API --> AG --> RET
  AG --> CTX
  AG --> DP
  API --> DBS
  DBS --> PLG
  API -->|WS get_permissions| PLG
  SPA -->|roles| APIP
```

---

## 3. Secuencia — Estudiante → Tutor → RAG → Ollama → Respuesta

```mermaid
sequenceDiagram
  autonumber
  participant U as Estudiante (SPA)
  participant G as Gateway (nginx)
  participant F as FastAPI /chat
  participant A as Auth (mdl_external_tokens)
  participant S as Supervisor (LangGraph)
  participant R as Retrieval (Chroma)
  participant O as Ollama
  participant D as MariaDB (traces)

  U->>G: POST /api/ai/chat (Bearer token)
  G->>F: proxy /chat (rate-limit ai_zone)
  F->>A: validar token
  A-->>F: user_id (o 401)
  F->>S: enrutar intención (determinista)
  alt en dominio
    S->>R: recuperar evidencia (pre-filtro por curso, scope-aware)
    R-->>S: chunks + metadata
    S->>O: generar respuesta (llama3.1:8b)
    O-->>S: texto
    S->>S: verificación post-generación (anti-alucinación)
  else fuera de dominio
    S-->>F: bloqueo (out_of_domain)
  end
  S-->>F: respuesta + fuentes + trace_id
  F->>D: persistir interaction_trace
  F-->>G: 200 (respuesta)
  G-->>U: respuesta + retrieval_scope
```

---

## 4. Secuencia — Profesor → ai-prepare → metadata → tutor

```mermaid
sequenceDiagram
  autonumber
  participant P as Profesor (SPA)
  participant G as Gateway
  participant F as FastAPI /authoring
  participant Perm as WS get_permissions
  participant O as Ollama (qwen3:14b / deepseek-r1:32b)
  participant D as MariaDB

  P->>G: POST /api/ai/authoring/lessons/{id}/ai-prepare
  G->>F: proxy (timeout 600s)
  F->>Perm: es_profesor(user, course)?
  Perm-->>F: true (o 403)
  F->>D: leer transcripción + recursos
  F->>O: generar borrador pedagógico (momentos+tiempos+tipo)
  O-->>F: JSON estricto (validado, anti-inyección)
  F->>D: guardar en metadata.ai_prepare (borrador aislado)
  F-->>P: borrador (líneas de tiempo editables)
  P->>G: POST .../ai-prepare/accept (draft editado)
  G->>F: proxy
  F->>D: promover (pedagogy/momentos) a campos vivos
  F-->>P: 200 (requires_reindex=false)
  Note over F,D: El tutor ya inyecta el nuevo perfil en el prompt (sin reindex).
```

---

## 5. Autorización por roles / capabilities

```mermaid
flowchart TD
  REQ["Request al backend"] --> TOK{"¿Bearer token válido?<br/>(mdl_external_tokens)"}
  TOK -- no --> R401["401 — no autenticado"]
  TOK -- sí --> GUARD{"Guard del endpoint"}
  GUARD --> WS["WS local_tesisai_get_permissions<br/>(has_capability por curso)"]
  WS -->|WS caída| FB["fallback por nombre de rol (db_service)"]
  WS --> FLAGS["flags: puede_ver_curso / es_profesor /<br/>puede_administrar_curso / puede_revisar / es_tecnico_rag"]
  FB --> FLAGS
  FLAGS --> DEC{"¿cumple la capability del guard?"}
  DEC -- no --> R403["403 — prohibido"]
  DEC -- sí --> OK["ejecuta acción (scoping por course_id canónico)"]

  subgraph Guards
    V["require_course_view → puede_ver_curso"]
    T["require_teacher → es_profesor (editing)"]
    Rv["require_course_reviewer → puede_revisar"]
    Ad["require_course_admin → puede_administrar_curso"]
    Rag["require_rag_admin → es_tecnico_rag (site)"]
  end
```

---

## 6. ERD simplificado — tablas `mdl_local_tesisai_*`

```mermaid
erDiagram
  LESSONS ||--o{ LESSON_BLOCKS : "tiene bloques"
  LESSONS ||--o{ LESSON_PROMPTS : "prompts proactivos/sugeridos"
  LESSONS ||--o{ TRANSCRIPT_SEGMENTS : "segmentos de transcripción"
  LESSONS ||--o{ RESOURCE_LESSON_LINKS : "recursos enlazados"
  COURSE_RESOURCES ||--o{ RESOURCE_LESSON_LINKS : "vínculo recurso↔lección"
  TUTOR_SESSIONS ||--o{ TUTOR_MESSAGES : "mensajes"
  TUTOR_MESSAGES ||--o{ MESSAGE_TRACES : "traza por mensaje"
  TUTOR_SESSIONS ||--o{ SESSION_CONTEXT : "contexto runtime"
  TUTOR_SESSIONS ||--o{ INTERACTION_TRACES : "traza por interacción"
  DOCUMENTS ||--o{ COURSE_RESOURCES : "conocimiento RAG"

  LESSONS {
    string lesson_id PK "anclado al cmid"
    string course_id
    string moodle_section_id
    string title
    json   metadata "pedagogy, ai_prepare"
  }
  LESSON_BLOCKS {
    string block_id PK
    int    start_time
    int    end_time
    string tutor_focus
    string interaction_mode
  }
  COURSE_RESOURCES {
    string doc_id PK
    bool   allowed_for_indexing
    bool   visible_to_student
    string resource_type
  }
  DOCUMENTS {
    string id PK
    string scope "global/course/section/lesson/block"
    string index_status
  }
  TRANSCRIPT_SEGMENTS {
    string id PK
    string lesson_id FK
    int    start_ms
    string text
  }
  INTERACTION_TRACES {
    string trace_id PK
    string course_id
    string retrieval_scope
    string model_used
  }
```

> Otras tablas del esquema: `local_tesisai_axes` (residual de la migración
> eje→sección, deuda técnica diferida). El ERD anterior muestra las 13 entidades
> operativas principales; el detalle de campos vive en
> `moodle/local_tesisai/db/install.xml`.

---

## 7. Teacher-driven RAG — el profesor alimenta el conocimiento sin tocar Markdown

```mermaid
flowchart TD
  P["Profesor (Vista Profesor, SPA)"] -->|sube recursos<br/>PDF/imagen/audio/plantilla| UP["/authoring/lessons/{id}/resources"]
  P -->|video de la lección| WH["Transcripción Whisper<br/>(generated_pending_review)"]
  WH -->|revisa y aprueba| APR["Transcripción APROBADA"]
  APR --> AIP["Preparar tutor con IA<br/>(/ai-prepare → borrador)"]
  AIP -->|acepta| ACC["teacher_approved_context<br/>(source=authoring_profile)"]
  P -->|"Publicar cambios del tutor"| PUB["/publish — indexación incremental<br/>delete-then-add teacher_context:&lt;lesson&gt;"]
  ACC --> PUB
  UP --> IDX["index_resource_text /<br/>index_resource_description"]
  IDX --> CH[("Chroma (colección única,<br/>metadata course/section/lesson)")]
  PUB --> CH
  CH --> TUT["Tutor por lección<br/>(retrieval scope-aware)"]

  style CH fill:#1a4a3a,stroke:#2e8b57,color:#eee
  classDef inj fill:#4a3a1a,stroke:#b8860b,color:#eee
  ACC2["Perfil pedagógico (tono, nivel de ayuda,<br/>momentos, reglas) — metadata"]:::inj
  P --> ACC2
  ACC2 -->|se INYECTA al prompt,<br/>NO se indexa| TUT
```

Principio **inject-vs-index**: el *conocimiento* (transcripción aprobada,
resource_text, resource_description, teacher_context) se **indexa** en Chroma;
el *comportamiento* (tono, nivel de ayuda, momentos, reglas, mensaje proactivo)
se **inyecta** en el prompt por lección. Sección 0: `canonical_md = 0` activo
(los 208 chunks canónicos fueron superseded por 35 recursos docentes reales).

---

## 8. H5P + learning signals — de la respuesta del estudiante a la guía del tutor

```mermaid
flowchart TD
  E["Estudiante responde<br/>InteractiveVideo (29 interacciones,<br/>7 lecciones mod_hvp)"] --> XR[("mdl_hvp_xapi_results<br/>+ gradebook")]
  XR --> SY["POST /learning-signals/sync/lesson/{id}<br/>(idempotente, solo SU snapshot)"]
  MAN["Manifest data/learning_signals/<br/>course_2_interactions.json<br/>(concepto + minuto + recurso + micro-práctica)"] --> SIG
  SY --> SIG["get_lesson_signals:<br/>score %, nivel, weak_concepts<br/>PRIORIZADOS (menor acierto primero)"]
  SIG --> GU["POST /lesson/{id}/guidance<br/>build_guidance_message DETERMINÍSTICO<br/>(1/2/3+ conceptos, help_level)"]
  SIG --> CTX["signals_block_for → Capa 3<br/>(inyección runtime al chat)"]
  GU --> UI{"¿chat abierto?"}
  UI -- sí --> INS["insertar en historial<br/>(dedupe por attempt_id)"]
  UI -- no --> BDG["badge + flecha + sonido<br/>pending_guidance persistido<br/>(localStorage por curso+lección)"]
  BDG -->|clic badge 'Ver guía' /<br/>abrir tutor / recarga| INS
  CTX --> CH8["Chat del tutor (agente RAG)"]

  NOTE["NUNCA a Chroma: las señales son<br/>estado runtime del alumno, no evidencia"]
  SIG -.- NOTE
```

---

## 9. Contexto del tutor — qué ve el modelo al responder

```mermaid
flowchart LR
  subgraph Entrada["Prompt final del tutor (por mensaje)"]
    direction TB
    A["A. EVIDENCIA RAG (indexada)<br/>chunks Chroma del curso/sección/lección:<br/>transcripciones aprobadas, recursos,<br/>teacher_context"]
    B["B. CONTEXTO ACTIVO (inyectado)<br/>lección/bloque actual, objetivo, momentos,<br/>tono + nivel de ayuda (directivas operativas),<br/>reglas del profesor"]
    C["C. SEÑALES DE APRENDIZAJE (runtime)<br/>desempeño H5P del alumno:<br/>conceptos débiles priorizados,<br/>minuto/recurso/micro-práctica"]
    D["D. PREGUNTA + HISTORIAL del alumno"]
  end
  A --> LLM["Ollama llama3.1:8b"]
  B --> LLM
  C --> LLM
  D --> LLM
  LLM --> V["Verificación post-generación<br/>(citas inventadas, fugas, atribuciones)"]
  V --> R["Respuesta del tutor<br/>+ fuentes visibles al alumno"]
```

Separación estricta: A es **conocimiento verificable** (con fuentes); B y C son
**comportamiento/estado** — jamás entran a la query vectorial ni a Chroma.

---

## 10. Estados de la actividad H5P y de la guía del tutor

```mermaid
stateDiagram-v2
  [*] --> not_attempted : lección abierta,<br/>video sin responder
  not_attempted --> available : estudiante responde<br/>el InteractiveVideo
  state available {
    [*] --> needs_reinforcement : < 60%
    [*] --> partial : 60–79%
    [*] --> ready : >= 80%
  }
  available --> guidance_pending : nivel débil/parcial<br/>(should_notify) — badge+flecha+sonido
  guidance_pending --> guidance_seen : abre el chat /<br/>clic en "Ver guía del tutor"
  guidance_seen --> guidance_pending : NUEVO intento<br/>(attempt_id distinto)
  guidance_seen --> guidance_recuperable : el mensaje queda<br/>recuperable desde el badge
  note right of guidance_pending
    persistido en localStorage por curso+lección;
    sobrevive recargas; el sonido no se repite;
    expira a los 7 días
  end note
```

---

## 11. Secuencia de defensa (video 3 min) — login → lección → H5P → tutor orienta

```mermaid
sequenceDiagram
  autonumber
  actor Est as Estudiante
  participant SPA as SPA React
  participant M as Moodle (LMS)
  participant F as FastAPI (IA)
  participant O as Ollama

  Est->>SPA: login (credenciales)
  SPA->>M: token (api_persistente)
  M-->>SPA: sesión + cursos
  Est->>SPA: abre curso 2 → Sección 0 → Lección (video H5P)
  SPA->>M: render mod_hvp (InteractiveVideo)
  Est->>M: responde las interacciones (MC/TF/Summary)
  M-->>M: guarda mdl_hvp_xapi_results + gradebook
  SPA->>F: sync + guidance (learning-signals)
  F-->>SPA: guía determinística (conceptos débiles,<br/>minuto, recurso, micro-práctica)
  SPA-->>Est: badge "Conviene reforzar · el tutor tiene una guía" 🔔
  Est->>SPA: clic en "Ver guía del tutor"
  SPA-->>Est: chat abre con la orientación (recuperable, sin duplicar)
  Est->>SPA: pregunta de seguimiento al tutor
  SPA->>F: POST /chat (contexto lección + señales)
  F->>O: RAG + generación (evidencia del curso)
  O-->>F: respuesta
  F-->>SPA: respuesta con tono/nivel de ayuda del profesor + fuentes
```
