# DEPLOY_PRODUCCION.md — Despliegue del sistema TIC KENTH

Guía operativa para reconstruir y desplegar el sistema completo (tutor IA + Moodle
+ gateway + observabilidad) con `docker-compose.deploy.yml`. Es la referencia de
reproducibilidad que exige la auditoría (`AUDITORIA_TIC_READYNESS.md`).

> **Servidor real de la tesis:** `kenneth@100.97.90.86` (host `bodyguard26`, Ubuntu),
> repo en `/srv/kenneth/tic-kenth`, rama desplegada `main`. Ollama es **nativo** en
> el host (GPU); el resto corre en Docker.

---

## 1. Arquitectura de despliegue

```
Navegador (SPA React)
        │  (mismo origen)
        ▼
 ┌──────────────────────────┐
 │ tic-gateway (nginx:alpine)│  publica 8090→80
 │ rate-limit + timeouts     │
 └───┬───────────────┬──────┘
     │ /api/ai/*     │ /api/lms/  /moodle/  /moodle_api/
     ▼               ▼
 ┌────────────────┐   ┌──────────────────────┐
 │ tic-fastapi    │   │ tic-moodle (PHP 5.0)  │ 8091→8080
 │ LangGraph/RAG  │◄WS┤ local_tesisai +       │
 │ :8000          │   │ api_persistente       │
 └──┬────────┬────┘   └──────────┬────────────┘
Chroma│    Ollama(host)          │ SQL
(bind)│  host.docker.internal    ▼
      │  :11434 (NATIVO GPU)  tic-mariadb :3306 (bind)
      │                       + tic-moodle-cron (cron 60s)
      ▼
 llama3.1:8b (chat) · nomic-embed-text (embed) · qwen3:14b (ai-prepare)
 qwen3-vl:4b (visión) · deepseek-r1:32b (quality=max)

Observabilidad: nginx JSON logs → tic-promtail → tic-loki → tic-grafana (127.0.0.1:3000)
```

**Principio de paridad:** el frontend sólo llama dos prefijos, mapeados igual en
dev (proxy Vite) y prod (nginx): `/api/ai/*` → FastAPI, `/api/lms/*` → Moodle.

---

## 2. Servicios Docker (`docker-compose.deploy.yml`)

| Servicio | Contenedor | Imagen | Puerto host | Depende de | Rol |
|---|---|---|---|---|---|
| mariadb | tic-mariadb | mariadb:11.4 | — (3306 interno) | — | Persistencia (Moodle + `mdl_local_tesisai_*`) |
| moodle | tic-moodle | tic-kenth/moodle:5.0-real | 8091→8080 | mariadb (healthy) | LMS + plugin + WS + api_persistente |
| moodle-cron | tic-moodle-cron | tic-kenth/moodle:5.0-real | — | moodle | `admin/cli/cron.php` cada 60 s |
| frontend | tic-frontend | tic-kenth/frontend:latest | — (volumen) | — | Build estático de la SPA → `frontend_build` |
| fastapi | tic-fastapi | tic-kenth/fastapi:latest | — (8000 interno) | mariadb, moodle | Tutor RAG / autoría / proxy Moodle |
| gateway | tic-gateway | nginx:alpine | **8090→80** | fastapi, frontend, moodle | Entrada pública única |
| loki | tic-loki | grafana/loki:2.9.0 | — | — | Almacén de logs |
| promtail | tic-promtail | grafana/promtail:2.9.0 | — | loki | Colector de logs de contenedores |
| grafana | tic-grafana | grafana/grafana:10.4.0 | 127.0.0.1:3000 | loki | Dashboards |

### Ruteo del gateway (`nginx/nginx.full.conf`)

| Location | Upstream | Timeout | Rate-limit |
|---|---|---|---|
| `/api/ai/chat` | `fastapi:8000/chat` | 300 s | `ai_zone` 20 r/m (por `Authorization`), burst 5 |
| `/api/ai/authoring/` | `fastapi:8000/authoring/` | **600 s** (ai-prepare quality=max) | `anon_zone` 60 r/m, burst 20 |
| `/api/ai/` | `fastapi:8000/` | 120 s | `anon_zone` 60 r/m, burst 20 |
| `/api/lms/`, `/moodle/`, `/moodle_api/` | `moodle:8080/` | 120 s | sin límite (H5P carga muchos assets) |
| `/` | SPA (`try_files … /index.html`) | — | — |

> `GET /api/ai/health` → `fastapi:8000/health`. `GET /api/ai/moodle/me` → `fastapi:8000/moodle/me`.

---

## 3. Volúmenes y persistencia

**Bind-mounts en `./runtime/`** (NO versionados; viven sólo en el servidor):

| Bind | Contenido |
|---|---|
| `runtime/mariadb` | Datadir de MariaDB (Moodle + tablas del proyecto) |
| `runtime/moodle` | Webroot de Moodle **incluye** `local/tesisai` y `proyecto_curso/api_persistente` |
| `runtime/moodledata` | Media de Moodle (H5P/vídeos). FastAPI lo monta **solo lectura** para transcribir |
| `runtime/chroma` | Índice vectorial (`/app/bd_vectorial` en FastAPI) |
| `runtime/fastapi-chat` | SQLite dev-fallback del backend |
| `runtime/whisper-cache` | Modelo faster-whisper (~480 MB, se descarga una vez) |

**Volúmenes nombrados:** `frontend_build` (compartido frontend→gateway),
`loki_data`, `grafana_data`.

**Import inicial de Moodle:** `_migration/moodle_dump.sql` se importa **solo** en el
primer arranque de MariaDB (datadir vacío). No versionado.

---

## 4. Variables de entorno requeridas (`.env`)

Copiar `.env.server.example` → `.env` y rellenar los `CAMBIAR_*`. **El `.env` real
nunca se versiona** (está en `.gitignore`). Claves clave:

```
# Acceso / Ollama nativo
PUBLIC_HOST=<ip-o-dominio>        PUBLIC_SCHEME=http
OLLAMA_BASE_URL=http://host.docker.internal:11434
KENTH_TEXT_MODEL=llama3.1:8b     KENTH_EMBED_MODEL=nomic-embed-text
KENTH_VISION_MODEL=qwen3-vl:4b-instruct
AI_PREP_MODEL=qwen3:14b          CHROMA_DIR=/app/bd_vectorial

# MariaDB / Moodle
MARIADB_ROOT_PASSWORD=…   MOODLE_DB_NAME=moodle   MOODLE_DB_USER=moodleuser
MOODLE_DB_PASSWORD=…      MOODLE_DB_PREFIX=mdl_
MOODLE_DB_HOST=mariadb    MOODLE_DB_PORT=3306
MOODLE_WS_BASE=http://moodle:8080/webservice/rest/server.php
MOODLE_WS_TOKEN=…                 # token del servicio api_tesis

# Backend
KENTH_COURSE_ID_SECRET=…          # DEBE coincidir con $KENTH_SECRET de tesis_lib.php
TESISAI_ALLOW_SQLITE_FALLBACK=0   # 0 en prod: exige MariaDB, sin fallback silencioso

# Grafana
GRAFANA_ADMIN_USER=admin  GRAFANA_ADMIN_PASSWORD=…
```

> ⚠️ **Secreto compartido**: `KENTH_COURSE_ID_SECRET` (FastAPI) debe ser idéntico a
> `$KENTH_SECRET` que resuelve `tesis_lib.php` (ahora `getenv('KENTH_COURSE_ID_SECRET')`),
> o la verificación de `course_id` firmado falla.

---

## 5. Ollama nativo y modelos necesarios

Ollama corre en el **host** (no en Docker) para usar la GPU; FastAPI lo alcanza por
`host.docker.internal:11434` (declarado con `extra_hosts` en el compose).

Modelos que deben existir (`ollama list` en el host):

```bash
ollama pull llama3.1:8b          # KENTH_TEXT_MODEL (chat del tutor)
ollama pull nomic-embed-text     # KENTH_EMBED_MODEL (embeddings RAG)
ollama pull qwen3:14b            # AI_PREP_MODEL (Preparar tutor con IA)
ollama pull qwen3-vl:4b-instruct # visión (captions)
ollama pull deepseek-r1:32b      # solo ai-prepare quality=max (opcional)
```

> **Gotcha (memoria de proyecto):** si el modelo configurado no está en Ollama, la
> llamada devuelve 404 → el tutor cae en 500 y ai-prepare en 500. Verificar SIEMPRE
> que los 3 primeros existen antes de anunciar “desplegado”.

---

## 6. Comandos de build y deploy

```bash
ssh kenneth@100.97.90.86
cd /srv/kenneth/tic-kenth

# 1) Traer la rama a validar/desplegar
git fetch origin
git checkout <rama>
git reset --hard origin/<rama>

# 2) Build + up (todo el stack)
docker compose -f docker-compose.deploy.yml --env-file .env up -d --build

# 2b) Solo lo que cambió (iteración típica de esta rama):
docker compose -f docker-compose.deploy.yml build frontend fastapi
docker compose -f docker-compose.deploy.yml up -d frontend fastapi
```

> **Gotcha del gateway (memoria de proyecto):** `nginx.full.conf` es un bind-mount de
> **un solo archivo**. Un `git pull` que cambia ese archivo cambia el inode, y un
> `nginx -s reload` NO basta: hay que **recrear** el contenedor del gateway:
> ```bash
> docker compose -f docker-compose.deploy.yml up -d --force-recreate gateway
> ```

---

## 7. Comandos de validación (no destructivos)

```bash
# Estado y commit desplegado
docker compose -f docker-compose.deploy.yml ps
git rev-parse HEAD && git status -sb

# Salud de la app (nuevo endpoint)
curl -s http://localhost:8090/api/ai/health | tee /dev/stderr | grep -q '"status"'

# Smoke completo (sin secretos). Con token opcional:
BASE_URL=http://localhost:8090 bash scripts/smoke_produccion.sh
MOODLE_TOKEN=<token> BASE_URL=http://localhost:8090 bash scripts/smoke_produccion.sh

# Validadores del índice RAG (lectura; NO reindexan)
docker exec tic-fastapi python scripts/validate_rag_index.py
docker exec tic-fastapi python scripts/verify_rag_index_clean.py
```

> `pytest` **no** está instalado en la imagen de producción (bug B5). La suite se
> corre en entorno de desarrollo (`tesis-rag/.venv`), no en el contenedor.

---

## 8. Backups y restauración

Existen en `/srv/kenneth/backups/`:

- `moodle-db-YYYYMMDD.sql.gz` — dump de la BD de Moodle.
- `moodledata-YYYYMMDD.tar` — media de Moodle.
- `rag-migration-*/`, `tesis_role.php.bak.*`, `backup.log`.
- `tic-kenth-backups/pre-align-*/`.

> ⚠️ **La restauración NO está probada** y el último snapshot puede no ser fresco.
> Antes de un piloto real: (1) verificar la frescura del dump, (2) **probar** una
> restauración en un entorno aparte, (3) automatizar la frecuencia. Restaurar sobre
> `runtime/mariadb`/`runtime/moodledata` con el stack **detenido**.

---

## 9. Sincronizar los componentes Moodle versionados

Los componentes Moodle ahora están versionados en [`../../moodle/`](../../moodle/)
(fuente sin secretos). Para llevarlos al servidor:

```bash
# Plugin (esquema + WS). Tras copiar, correr upgrades desde Notificaciones.
cp -r moodle/local_tesisai/*        runtime/moodle/local/tesisai/

# Endpoints PHP (auth/pagos/roles). Mantener el .env real del servidor.
cp -r moodle/api_persistente/*.php  runtime/moodle/proyecto_curso/api_persistente/
#  ⚠️ NO sobrescribir el .env real ni tesis_lib.php si el server usa secreto local.
docker compose -f docker-compose.deploy.yml exec moodle \
  php admin/cli/upgrade.php --non-interactive   # aplica upgrades del plugin
```

> La copia viva del plugin está bajo `runtime/moodle/` (gitignored). `moodle/` en el
> repo es la **fuente de verdad** para reconstruir; no se despliega automáticamente.

---

## 10. Checklist de despliegue

- [ ] `.env` creado desde `.env.server.example`, sin `CAMBIAR_*`.
- [ ] `KENTH_COURSE_ID_SECRET` == `$KENTH_SECRET` de Moodle.
- [ ] Ollama nativo con los 3 modelos base (`llama3.1:8b`, `nomic-embed-text`, `qwen3:14b`).
- [ ] `docker compose … up -d --build` sin errores; 9 contenedores arriba.
- [ ] Gateway **recreado** si cambió `nginx.full.conf`.
- [ ] `curl /api/ai/health` → `status: ok|degraded`.
- [ ] `scripts/smoke_produccion.sh` → 0 FAIL.
- [ ] `git rev-parse HEAD` == commit esperado, árbol limpio.
