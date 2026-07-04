# Seguridad — TIC KENTH

Modelo de seguridad del sistema, verificado en la auditoría del servidor
(`AUDITORIA_TIC_READYNESS.md` §8) y fijado por pruebas
(`tests/test_operational_endpoints.py`, `test_authoring_role_separation.py`,
`test_moodle_permissions.py`).

---

## 1. Autenticación por token Moodle

- **Contrato:** `Authorization: Bearer <moodle_token>`. El token se valida contra
  `mdl_external_tokens` (join con `mdl_external_services`): debe existir, el servicio
  estar habilitado (`enabled=1`) y no estar expirado (`validuntil`).
- **Fuente:** `api/dependencies.py::get_current_user_id` →
  `db_service.get_user_id_from_token`.
- **Producción:** con la BD Moodle activa, el token es **obligatorio**. Sin token →
  **401**.
- **Lectura permitida de core Moodle:** por contrato SOA sólo se leen directamente
  `mdl_external_tokens` (auth) y `mdl_local_tesisai_*` (del proyecto); el resto va por
  Web Services.

## 2. Bypass `X-User-Id` cerrado

- La cabecera `X-User-Id` **sólo** se acepta en desarrollo aislado (SQLite, sin
  Moodle). Con Moodle activo se **ignora**: `POST /chat` con `X-User-Id` y sin token →
  **401** (verificado, §8).
- Prueba: `test_me_exige_token_cuando_moodle_activo`.

## 3. Autorización por capabilities (no por nombre de rol)

- **Fuente de verdad:** WS `local_tesisai_get_permissions` (en el plugin
  `local_tesisai`), que deriva flags de `has_capability` en el contexto del curso.
  Server-to-server con `MOODLE_WS_TOKEN` + `userid` explícito.
- **Fallback:** si la WS no está disponible, los guards caen al fallback por nombre de
  rol de `db_service` (mismo contrato).
- **Flags:** `puede_ver_curso`, `es_profesor`, `puede_administrar_curso`,
  `puede_revisar`, `es_tecnico_rag`, `es_invitado`.

### Guards y qué protegen

| Guard | Capability | Protege |
|---|---|---|
| `require_course_view` | `puede_ver_curso` | Lecturas de estructura/recursos del alumno. |
| `require_teacher` | `es_profesor` (editing) | Autoría pedagógica (momentos, pedagogy, recursos, transcripción, ai-prepare). |
| `require_course_reviewer` | `puede_revisar` | Revisión/analítica (incluye profesor sin edición). |
| `require_course_admin` | `puede_administrar_curso` | Estructura técnica (blocks, reorder, reindex por curso). |
| `require_rag_admin` | `es_tecnico_rag` (site) | Índice global (`/documents/index`, `/documents/rebuild`). |

- **Profesor sin edición** (non-editing teacher) **no** edita: revisa pero no toca
  pedagogía ni estructura → 403 (verificado; `test_require_teacher_bloquea_non_editing`).
- **Resolución segura de curso:** `require_course_view` acepta el curso por
  `X-Course-Id` o por query `course_id`; la capability se valida **siempre** sobre el
  curso resuelto — aceptar el query **no** debilita la autorización
  (`test_course_view_query_fallback_sigue_validando_capability`).

## 4. Endpoints protegidos (resumen)

- **Autoría (`/authoring/*`):** `require_teacher` (pedagogía) y `require_course_admin`
  (estructura: `/lessons-reorder`, `/documents/reindex`). Estudiante/anónimo → 401/403.
- **Reindex del índice:** `/documents/index` y `/documents/rebuild` → `require_rag_admin`
  (site admin). Destructivo; el profesor editor **no** reindexa (verificado, §8).
- **Chat / sesiones / perfil:** requieren token. Un usuario no accede a sesiones de
  otro.
- **Salud (`/health`):** público a propósito (readiness), **sin** datos sensibles.

## 5. Perfil `/moodle/me` sin fuga de datos

- Devuelve **lista blanca** de campos del perfil (id, nombre, email propio, etc.); los
  campos no reconocidos que devuelva el WS **no** se propagan
  (`test_me_ok_con_perfil_y_capabilities`).
- Si el Moodle WS falla, degrada de forma **controlada** (200 con `moodle_ws:"error"`,
  sin 500) — corrige el bug B1 (KeyError de logging).

## 6. `/health` sin secretos

- Sólo expone estados (`ok`/`degraded`/`error`), nombres de modelos (configuración no
  secreta) y conteos. **Nunca** tokens, contraseñas ni URLs con credenciales.
- Prueba: `test_health_no_expone_secretos` (verifica ausencia de token/DBpass y de las
  palabras `wstoken`/`password`/`bearer` en el body).

## 7. Secretos fuera del repo

- `.gitignore` bloquea `.env`, `.env.*` (salvo `*.example`), `*.bak`, `*.log`, `*.sql`,
  `_migration/`, `runtime/`, dumps y binarios.
- Al **versionar** los componentes Moodle (`moodle/`), se auditó y **excluyó**: `.env`
  reales (tokens PayPal/PayPhone), logs con PII, `payments/*.json` (transacciones),
  backups y binarios; y se **redactó** el único secreto hardcodeado
  (`tesis_lib.php::$KENTH_SECRET` → `getenv('KENTH_COURSE_ID_SECRET')`).
- `.htaccess` de `api_persistente` niega el acceso directo por URL a
  `.env/.log/.txt/.json/.bak/.sql`.
- **Firma de `course_id`:** HMAC-SHA256 con `KENTH_COURSE_ID_SECRET` (compartido
  backend↔Moodle) evita manipular/adivinar ids de curso.

## 8. Observabilidad / trazabilidad

- Log JSON por request (`request_id`, ruta, estado, latencia, `user_id`) →
  Promtail → Loki → Grafana (Grafana sólo en `127.0.0.1:3000`).
- Traza por interacción en `mdl_local_tesisai_interaction_traces`.
- Rate-limit en el gateway: `ai_zone` 20 r/m por `Authorization` (chat), `anon_zone`
  60 r/m por IP (resto de `/api/ai`).

---

## 9. Riesgos pendientes (no cerrados en esta rama)

| Riesgo | Severidad | Nota / mitigación futura |
|---|---|---|
| Rutas legacy `/documents/` (list/upload/delete) **sin guard de rol**. | 🟠 Media | Son de desarrollo; las destructivas (`index`/`rebuild`) sí exigen `require_rag_admin`. Recomendado: gatearlas o retirarlas antes de producción. |
| **Sin HTTPS/dominio** (HTTP plano en el gateway). | 🟠 Media | Post-tesis: TLS + dominio; el token viaja en claro en HTTP. |
| **Sin pruebas de carga / hardening** (p95, límites de recursos). | 🟡 Baja-Media | Post-tesis. |
| **Backups no restaurados-verificados** y no siempre frescos. | 🟠 Media | Probar restauración; automatizar frescura (ver `DEPLOY_PRODUCCION.md` §8). |
| `pytest` ausente en la imagen de producción. | ⚪ Info | La suite corre en dev; no afecta runtime. |
| Gestión de secretos manual (`.env` en el servidor). | 🟡 Baja-Media | Post-tesis: gestor de secretos / variables del orquestador. |
| Grafana con credenciales de entorno. | 🟡 Baja | Sólo escucha en loopback; cambiar `GRAFANA_ADMIN_PASSWORD`. |

> **Veredicto de seguridad (auditoría):** enforcement por rol **correcto** en todos
> los casos probados, sin bypass. Los pendientes son de **hardening** para producción,
> no fallos de autorización.
