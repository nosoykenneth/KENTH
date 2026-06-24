# Full Docker Server

Este runbook deja TIC KENTH listo para servidor con Moodle y MariaDB dentro de Docker, manteniendo Ollama nativo en el host para usar GPU sin complicar el runtime NVIDIA del compose.

## Arquitectura

Servicios en `docker-compose.full.yml`:

- `gateway`: nginx publico en `80` y futuro `443`.
- `frontend`: build estatico React servido por el gateway.
- `fastapi`: backend RAG en red interna, sin puerto publico.
- `moodle`: contenedor Moodle en red interna, sin puerto publico directo.
- `mariadb`: base de datos Moodle en red interna, sin puerto publico.
- `loki`, `promtail`, `grafana`: observabilidad interna, sin publicar `3000`.
- Ollama: nativo en el host, accesible desde contenedores por `host.docker.internal:11434`.

Puertos publicos previstos: solo `80` y luego `443` cuando haya TLS.

## Requisitos del servidor

- Ubuntu Server actualizado.
- Driver NVIDIA funcional si se usara GPU: `nvidia-smi` debe responder.
- Docker Engine con plugin `docker compose`.
- Ollama instalado nativo y escuchando en `0.0.0.0:11434`.
- Acceso SSH con usuario sudo.
- Secretos rotados: no reutilizar secretos que estuvieron en Git.

## Instalacion rapida del host

Desde el repo clonado o desde un paquete copiado al servidor:

```bash
bash scripts/setup-full-docker-server.sh
```

El script instala Docker si falta, instala Ollama si falta, configura `OLLAMA_HOST=0.0.0.0:11434`, descarga modelos y crea carpetas `runtime/`. No escribe credenciales reales.

## Instalacion manual equivalente

```bash
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg ufw
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"

curl -fsSL https://ollama.com/install.sh | sh
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf >/dev/null <<'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl restart ollama

ollama pull llama3.1:8b
ollama pull qwen3-vl:4b-instruct
ollama pull nomic-embed-text
```

## Clonar y preparar `.env`

```bash
git clone https://github.com/nosoykenneth/KENTH.git tic-kenth
cd tic-kenth
cp .env.server.example .env
openssl rand -hex 32
nano .env
```

Rellena todos los `CAMBIAR_*`. No copies `.env` de la laptop. Cualquier secreto anterior debe considerarse comprometido.

Variables criticas:

- `MARIADB_ROOT_PASSWORD`
- `MOODLE_DB_NAME`
- `MOODLE_DB_USER`
- `MOODLE_DB_PASSWORD`
- `MOODLE_ADMIN_USER`
- `MOODLE_ADMIN_PASSWORD`
- `MOODLE_ADMIN_EMAIL`
- `MOODLE_SITE_NAME`
- `MOODLE_WS_TOKEN`
- `KENTH_COURSE_ID_SECRET`
- `GRAFANA_ADMIN_PASSWORD`

## Carpetas persistentes

```bash
mkdir -p runtime/mariadb runtime/moodle runtime/moodledata runtime/chroma runtime/fastapi-chat
```

Volumenes bind-mounted:

- `./runtime/mariadb:/var/lib/mysql`
- `./runtime/moodle:/bitnami/moodle`
- `./runtime/moodledata:/bitnami/moodledata`
- `./runtime/chroma:/app/bd_vectorial`
- `./runtime/fastapi-chat:/app/bd_chat`

Si el servidor usa Linux y la imagen Moodle no puede escribir en `runtime/moodle*`, ajustar permisos segun el UID del contenedor Bitnami:

```bash
sudo chown -R 1001:1001 runtime/moodle runtime/moodledata
```

## Plugin Moodle local_tesisai

El repo actual no contiene una carpeta versionada `local/tesisai` ni `local_tesisai`; solo conserva migraciones schema-only en `tesis-rag/migrations/moodle/*.sql`.

Si tienes el plugin fuera del repo, copialo al servidor y luego elige una de estas opciones:

```bash
# Opcion A: copiar al volumen persistente tras el primer arranque de Moodle
mkdir -p runtime/moodle/local
cp -a /ruta/segura/tesisai runtime/moodle/local/tesisai

# Opcion B: montar una ruta real descomentando en docker-compose.full.yml
# ./moodle/local/tesisai:/bitnami/moodle/local/tesisai:ro
```

Despues visita `/moodle/admin` o ejecuta el upgrade CLI dentro del contenedor para que Moodle aplique cambios del plugin.

## Levantar stack full Docker

```bash
docker compose -f docker-compose.full.yml --env-file .env config
docker compose -f docker-compose.full.yml --env-file .env up -d --build
docker compose -f docker-compose.full.yml --env-file .env ps
```

## Verificaciones

```bash
docker compose -f docker-compose.full.yml --env-file .env logs --tail=100 fastapi
docker compose -f docker-compose.full.yml --env-file .env logs --tail=100 moodle
docker compose -f docker-compose.full.yml --env-file .env exec fastapi curl -s http://localhost:8000/openapi.json | head -c 100
docker compose -f docker-compose.full.yml --env-file .env exec fastapi curl -s http://host.docker.internal:11434/api/tags
docker compose -f docker-compose.full.yml --env-file .env exec fastapi sh -c "python -m pytest -q"
```

Smoke tests por navegador:

- `http://IP/` carga el frontend.
- `http://IP/api/ai/openapi.json` responde desde FastAPI.
- `http://IP/api/lms/` llega a Moodle via gateway.
- `http://IP/moodle/` puede servir para administracion inicial, pero Moodle bajo subruta suele requerir `wwwroot` coherente. Para produccion estable, preferir subdominio futuro `moodle.DOMINIO`.

## Reindex RAG

El indice Chroma ya no vive en Git. Si `runtime/chroma` esta vacio, copia un indice valido o reindexa desde corpus oficial:

```bash
docker compose -f docker-compose.full.yml --env-file .env exec fastapi sh -c "python scripts/reindex_rag_clean.py"
```

Usa el mismo `KENTH_EMBED_MODEL` con el que se construyo el indice. Cambiar embeddings invalida el espacio vectorial.

## Evaluacion del tutor

```bash
docker compose -f docker-compose.full.yml --env-file .env exec fastapi sh -c "python evaluation/run_rag_eval.py"
docker compose -f docker-compose.full.yml --env-file .env exec fastapi sh -c "python evaluation/run_tutor_eval.py"
```

## Firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH || sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 172.16.0.0/12 to any port 11434 proto tcp
sudo ufw deny 3306/tcp
sudo ufw deny 8000/tcp
sudo ufw deny 8080/tcp
sudo ufw deny 11434/tcp
sudo ufw deny 3000/tcp
sudo ufw --force enable
sudo ufw status numbered
```

Docker puede saltarse `ufw` para puertos publicados; por eso el compose full solo publica `80` y deja los servicios sensibles sin `ports:`.

## Rollback basico

```bash
docker compose -f docker-compose.full.yml --env-file .env down
# Backup antes de borrar runtime si hay datos reales.
tar czf runtime-backup-$(date +%Y%m%d-%H%M%S).tgz runtime
```

Para reiniciar desde cero, solo despues de backup:

```bash
sudo rm -rf runtime/mariadb runtime/moodle runtime/moodledata runtime/chroma runtime/fastapi-chat
mkdir -p runtime/mariadb runtime/moodle runtime/moodledata runtime/chroma runtime/fastapi-chat
docker compose -f docker-compose.full.yml --env-file .env up -d --build
```

## Docker Hub opcional futuro

No se publica nada ahora. Si mas adelante quieres evitar builds en servidor, usar repos privados si el frontend incluye variables de pago:

- `kacortez/tic-kenth-frontend`
- `kacortez/tic-kenth-fastapi`
- `kacortez/tic-kenth-gateway`

Comandos futuros, no ejecutar todavia:

```bash
docker tag tic-kenth/frontend:latest kacortez/tic-kenth-frontend:latest
docker tag tic-kenth/fastapi:latest kacortez/tic-kenth-fastapi:latest
# docker login
# docker push kacortez/tic-kenth-frontend:latest
# docker push kacortez/tic-kenth-fastapi:latest
```

## Seguridad pendiente

Despues de reescribir historial, publicar con:

```bash
git push --force-with-lease origin main
```

Nunca usar `git push --force` normal. Rota Moodle token, passwords MariaDB/Moodle/Grafana, `KENTH_COURSE_ID_SECRET` y tokens de pago que estuvieron en Git.