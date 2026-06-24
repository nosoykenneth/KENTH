# Migración al servidor del tutor — runbook

> Objetivo: pasar TIC KENTH de la laptop a un servidor **Ubuntu** (Intel Ultra,
> 64 GB RAM, **RTX 5070 Ti** 16 GB) con el mínimo de errores. Despliegue
> **híbrido**: Ollama y Moodle **nativos**; FastAPI + frontend + gateway +
> observabilidad en **Docker Compose**.
>
> Decidido: **Moodle se mueve completo al servidor** (piloto independiente de la laptop).

## Arquitectura objetivo

```
                    Internet / LAN
                          │
                    [ gateway nginx ]  :80   (contenedor)
                    /      |        \
        /api/ai/* │   /api/lms/*    │  /  (SPA estático)
                  │        │
        [ fastapi RAG ]    └──► [ Moodle Apache ]  127.0.0.1:8081  (NATIVO)
         (contenedor)                   │
              │                   [ MariaDB ]      127.0.0.1:3306  (NATIVO)
              ▼
        [ Ollama ]  0.0.0.0:11434  (NATIVO, GPU)
```

- El **gateway** ocupa el `:80` público → por eso **Moodle/Apache se mueve al `:8081`** (local).
- `fastapi` alcanza Ollama, MariaDB y Moodle-WS del host vía `host.docker.internal`.
- Observabilidad (Loki/Promtail/Grafana) en compose; Grafana en `:3000`.

---

## PASO 0 — Lo que NO está en git (cópialo a mano o NADA funciona)

Clonar el repo en el server **no** trae esto. Llévalo en USB / `scp` / `rsync`:

- [ ] **Corpus oficial** → `tesis-rag/documentos/oficial/` (temario, `ejes/`, `global/`, `guiones/`). Sin él no hay reindex.
- [ ] **Índice vectorial ya construido** → `tesis-rag/bd_vectorial/` (evita reindexar; embed = `nomic-embed-text`).
- [ ] **Secretos del frontend** → `frontend-tesis/.env` (tokens Payphone/PayPal). Se **hornean en el build**.
- [ ] **`api_persistente`** (PHP auth/login/pagos) → de `C:\Moodle\server\moodle\proyecto_curso\api_persistente` al webroot de Moodle del server.
- [ ] **Dump de la BD de Moodle** → `mysqldump` (incluye las tablas `mdl_local_tesisai_*` que SON tu base operativa).
- [ ] **`moodledata`** → la carpeta de datos de Moodle (`$CFG->dataroot`).
- [ ] **`.env` del backend** → no copies el de la laptop; usa `.env.server.example` (rutas/hosts distintos).

> Tip: en la laptop, `git status --porcelain` + esta lista = todo lo que viaja.

---

## PASO 1 — Provisionar el host (Ollama nativo + Docker)

En el server, con el repo ya clonado:

```bash
# 1. Driver NVIDIA para Blackwell (5070 Ti): driver >= 570, CUDA 12.8+
nvidia-smi   # si falla: sudo ubuntu-drivers install   (o el .run oficial), luego reinicia

# 2. Script de provisión (instala Ollama nativo, lo deja en 0.0.0.0:11434,
#    baja modelos, instala Docker). NO instala Moodle.
bash scripts/setup-server.sh
```

El script deja Ollama escuchando en `0.0.0.0:11434` (necesario para que el contenedor
lo alcance) y descarga `llama3.1:8b`, el modelo de visión y `nomic-embed-text`.

> **GPU Blackwell:** si `ollama ps` no muestra GPU, el problema es driver/CUDA, no el script.
> Verifica `nvidia-smi` y que Ollama sea reciente. En CPU funciona pero lento.

---

## PASO 2 — Moodle nativo (LAMP) en el servidor

```bash
sudo apt update
sudo apt install -y apache2 mariadb-server php php-{mysqli,xml,curl,gd,intl,zip,mbstring,soap} libapache2-mod-php
```

1. **Apache al puerto 8081** (el `:80` es del gateway). Edita `/etc/apache2/ports.conf`
   → `Listen 8081`, y el `<VirtualHost *:80>` del site → `<VirtualHost *:8081>`. `sudo systemctl reload apache2`.
2. **MariaDB**: crea la BD y el usuario, e **importa el dump**:
   ```bash
   sudo mysql -e "CREATE DATABASE moodle CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   sudo mysql -e "CREATE USER 'tic_kenth'@'%' IDENTIFIED BY 'TU_PASS'; GRANT ALL ON moodle.* TO 'tic_kenth'@'%'; FLUSH PRIVILEGES;"
   mysql -u tic_kenth -p moodle < moodle_dump.sql
   ```
   > El `'%'` permite que el contenedor fastapi conecte vía `host.docker.internal`. Si prefieres
   > restringir, usa la IP del bridge docker en vez de `%`.
3. **Webroot**: copia el código de Moodle + `proyecto_curso/api_persistente` a `/var/www/moodle`.
4. **`moodledata`**: copia la carpeta a una ruta fuera del webroot (ej. `/var/moodledata`), `chown -R www-data`.
5. **`config.php`** de Moodle: ajusta
   - `$CFG->dbhost='127.0.0.1'`, `$CFG->dbname='moodle'`, `$CFG->dbuser='tic_kenth'`, `$CFG->dbpass=...`
   - `$CFG->dataroot='/var/moodledata'`
   - `$CFG->wwwroot='http://IP_O_DOMINIO'` ⟵ **importante** (ver PASO 5: rompe los file links si no se ajusta el frontend).
6. **Plugin** `local_tesisai`: ya viene en el dump (tablas) y en el webroot (código). Visita
   `http://IP:8081/admin` para correr upgrades pendientes.
7. **Token de Web Services**: en Moodle admin, genera/copia el token del servicio y ponlo en `.env`
   (`MOODLE_WS_TOKEN`). Sin él, la sincronización Python↔Moodle falla.

---

## PASO 3 — Sembrar datos del RAG y secretos del frontend

```bash
# Índice vectorial ya construido (del PASO 0). El compose lo bind-montea.
#   tesis-rag/bd_vectorial/   <-- pegar aquí lo copiado

# Corpus oficial (por si necesitas reindexar):
#   tesis-rag/documentos/oficial/

# Secretos del frontend (se usan en el build de Docker):
#   frontend-tesis/.env       <-- pegar aquí lo copiado
```

> Si NO copiaste `bd_vectorial`, reindexa en el server (necesita Ollama arriba):
> `cd tesis-rag && python scripts/reindex_rag_clean.py` — **destructivo**, reconstruye el índice.
> Requiere el corpus oficial presente y `KENTH_EMBED_MODEL=nomic-embed-text`.

---

## PASO 4 — Configurar `.env` y levantar el app tier

```bash
cp .env.server.example .env
nano .env        # rellena todos los CAMBIAR_*  (PUBLIC_HOST, pass DB, WS token, secret, grafana)
openssl rand -hex 32   # para KENTH_COURSE_ID_SECRET

docker compose -f docker-compose.server.yml up -d --build
docker compose -f docker-compose.server.yml ps
```

`OLLAMA_BASE_URL`, `MOODLE_DBHOST` y `MOODLE_WS_BASE` ya apuntan a `host.docker.internal`
(Ollama:11434, MariaDB:3306, Moodle:8081). No los cambies salvo que muevas esos servicios.

---

## PASO 5 — Fix obligatorio: `http://localhost` hardcodeado en el frontend

`frontend-tesis/src/shared/components/ui/MoodleRenderer.jsx` (líneas **24, 204, 282**) hace:

```js
contentObj.fileurl.replace('http://localhost/', '/api/lms/')
```

En la laptop el `wwwroot` de Moodle es `http://localhost`, así que matchea. **En el server,
`wwwroot` = `http://IP_O_DOMINIO`**, así que el `replace` NO matchea y **los archivos de
Moodle no cargan**. Dos opciones:

- **Rápida**: reemplaza las 3 ocurrencias de `'http://localhost/'` por el `wwwroot` real del
  server (ej. `'http://IP_O_DOMINIO/'`). Rebuild del frontend.
- **Robusta** (recomendada): derivar el prefijo del `wwwroot` en vez de hardcodearlo.

> Dime el `wwwroot` final (IP o dominio) y te dejo el parche de las 3 líneas listo.

---

## PASO 6 — Verificación end-to-end (smoke test)

- [ ] `curl http://localhost:11434/api/version` → Ollama responde.
- [ ] `ollama ps` → muestra GPU.
- [ ] `docker compose -f docker-compose.server.yml ps` → todos `Up`.
- [ ] `http://IP/` → carga el SPA.
- [ ] Login de un alumno (pasa por `api_persistente`) → token válido.
- [ ] Abrir una lección → carga recursos de Moodle (valida el PASO 5).
- [ ] Preguntar al tutor dentro de una lección → responde con evidencia del curso.
- [ ] Probar el **fix D**: una pregunta `delegated_to_tutor` sin evidencia → responde como
      adaptación operativa (`evidence_level: "delegado"`), no "no veo una fuente".
- [ ] Grafana `http://IP:3000` → llegan logs del gateway/fastapi.

---

## Rollback

El app tier es desechable: `docker compose -f docker-compose.server.yml down` y vuelves a
`up`. Los datos persistentes viven fuera del compose (MariaDB nativa, `moodledata`,
`bd_vectorial` bind-monteado), así que un `down` no los borra. Haz **backup del dump y de
`moodledata`** antes de tocar Moodle.

---

## Notas y pendientes

- **TLS**: con dominio, usa certbot y descomenta el server `:443` en `nginx/nginx.server.conf`.
- **Modelo más fuerte / LLM-juez**: con la 5070 Ti puedes `ollama pull qwen2.5:14b-instruct`
  y subirlo en `KENTH_TEXT_MODEL`. Es lo que vuelve confiable el juez de atribución (hoy apagado
  por el 3b débil).
- **Selector de modelo en la UI**: pendiente (lo ofrecí antes). Una vez en el server, el cambio
  de modelo es editar `.env` y `restart`; el selector lo hace sin tocar archivos.
- **Transcripción (faster-whisper)**: corre en CPU dentro del contenedor (no GPU passthrough).
  Es autoría, no la ruta del alumno; aceptable, pero lento para videos largos.
- **Python**: la laptop usa 3.14; la imagen del server usa 3.11-slim con versiones **pineadas**
  (`requirements.txt`) → mismo comportamiento. Snapshot completo en `requirements.lock.txt`.
