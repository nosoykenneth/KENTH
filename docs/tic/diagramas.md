# Diagramas — TIC KENTH

Diagramas en Mermaid (renderizables en GitHub/VS Code). Reflejan el sistema
desplegado (`AUDITORIA_TIC_READYNESS.md`, commit `6b25712`).

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
