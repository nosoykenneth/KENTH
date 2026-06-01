# Runbook: migracion de Moodle al servidor del tutor

Objetivo: trasladar la instalacion actual de Moodle 5.0.4 que vive en
`C:\Moodle\server` (XAMPP) al stack Docker Compose del servidor, preservando:

- Curso "Mezcla y Masterización" (ID 2).
- Usuarios, enrolamientos, calificaciones, intentos H5P.
- Plugin custom `local_tesisai` (tablas `mdl_local_tesisai_*`).
- Suite PHP `proyecto_curso/api_persistente/` (login, profile, commercial, etc.).
- Archivos en `moodledata/`.

Tiempo estimado: 60-90 min, dependiendo del tamano de `moodledata`.

---

## Fase A. Backup en la maquina local (Windows)

Ejecutar desde PowerShell en `C:\Moodle\server`.

```powershell
# 1. Backup de la base de datos
& "C:\Moodle\server\mariadb\bin\mysqldump.exe" `
    -h 127.0.0.1 -P 3307 -u root -p123 `
    --default-character-set=utf8mb4 `
    --single-transaction --routines --triggers --events `
    moodle > moodle_dump.sql

# 2. Empaquetar codigo Moodle (incluye plugins custom)
Compress-Archive -Path "C:\Moodle\server\moodle\*" -DestinationPath moodle_code.zip

# 3. Empaquetar moodledata
Compress-Archive -Path "C:\Moodle\server\moodledata\*" -DestinationPath moodledata.zip
```

Verificar tamanos antes de copiar al servidor:

```powershell
Get-Item moodle_dump.sql, moodle_code.zip, moodledata.zip | Select-Object Name, Length
```

## Fase B. Transferencia al servidor

Con `scp` (Linux server) o `pscp` (desde Windows). Ajustar usuario y host.

```bash
scp moodle_dump.sql moodle_code.zip moodledata.zip user@servidor:/tmp/migration/
```

## Fase C. Preparar volumenes en el servidor

```bash
cd /opt/tic-kenth   # carpeta donde vive el repo + docker-compose.yml

# Levantar SOLO mariadb (el resto aun no, para evitar que Moodle escriba algo).
docker compose up -d mariadb

# Esperar a que MariaDB este listo (verificar healthcheck).
docker compose logs --tail=20 mariadb
```

## Fase D. Restaurar la base de datos

```bash
# Recrear el schema vacio
docker compose exec mariadb mysql -uroot -p"${MOODLE_ROOT_PASS}" \
    -e "DROP DATABASE IF EXISTS moodle; CREATE DATABASE moodle CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Cargar el dump
docker compose exec -T mariadb mysql -uroot -p"${MOODLE_ROOT_PASS}" moodle \
    < /tmp/migration/moodle_dump.sql

# Verificar curso ID 2
docker compose exec mariadb mysql -uroot -p"${MOODLE_ROOT_PASS}" moodle \
    -e "SELECT id, fullname, shortname FROM mdl_course WHERE id = 2;"
```

## Fase E. Inyectar codigo Moodle y moodledata

El contenedor `bitnami/moodle:5` mantiene Moodle en `/bitnami/moodle` y los
datos en `/bitnami/moodledata`, ambos volumenes nombrados (`moodle_data` y
`moodledata_data`).

```bash
# 1. Hacer que el contenedor escriba sus volumenes la primera vez
docker compose up -d moodle
# Esperar a que termine la inicializacion bitnami (mira logs).
docker compose logs --tail=50 -f moodle
docker compose stop moodle

# 2. Reemplazar /bitnami/moodle con el codigo del repo (que incluye los plugins).
# Esto es delicado: queremos preservar SOLO los plugins custom + proyecto_curso/.
# El nucleo de Moodle ya esta en el contenedor; sobrescribir podria romper la version.
docker compose run --rm --no-deps moodle bash -c '
    mkdir -p /bitnami/moodle/local/tesisai
    mkdir -p /bitnami/moodle/proyecto_curso
'

# Copiar SOLO el plugin custom y la suite PHP propia.
# Asumimos que el zip del codigo ya esta descomprimido en /tmp/migration/moodle_src/
docker cp /tmp/migration/moodle_src/local/tesisai tic-moodle:/bitnami/moodle/local/
docker cp /tmp/migration/moodle_src/proyecto_curso tic-moodle:/bitnami/moodle/

# 3. Copiar moodledata (archivos subidos por estudiantes, sesiones, cache).
docker cp /tmp/migration/moodledata/. tic-moodle:/bitnami/moodledata/

# Ajustar permisos (bitnami corre como uid 1001).
docker compose run --rm --no-deps --user root moodle bash -c '
    chown -R 1001:1001 /bitnami/moodle/local/tesisai /bitnami/moodle/proyecto_curso /bitnami/moodledata
'
```

## Fase F. Ajustes de configuracion Moodle

```bash
docker compose up -d moodle

# Ejecutar el upgrade UI si la imagen viene con version superior.
curl -i "http://localhost/admin/index.php?confirmupgrade=1&confirmrelease=1"

# Re-emitir token para FastAPI:
#   1. Admin -> Server -> Webservices -> Habilitar protocolo REST.
#   2. External services -> "tesisai_service" -> Functions.
#   3. Manage tokens -> Create token vinculado al servicio.
# Copiar el token a .env (MOODLE_WS_TOKEN) y reiniciar fastapi.
docker compose restart fastapi
```

## Fase G. Verificacion

```bash
# 1. Login funciona
curl -X POST "http://localhost/api/lms/proyecto_curso/api_persistente/tesis_login.php" \
     -d "username=admin&password=${MOODLE_PASSWORD}"

# 2. WS responde para FastAPI
curl "http://localhost/api/lms/webservice/rest/server.php?wstoken=${MOODLE_WS_TOKEN}&wsfunction=core_user_get_users_by_field&field=id&values[0]=2&moodlewsrestformat=json"

# 3. Tutor IA puede leer el perfil del estudiante
curl -H "Authorization: Bearer ${TOKEN_DE_LOGIN}" \
     "http://localhost/api/ai/moodle/me"

# 4. Curso ID 2 sigue visible
curl -H "Authorization: Bearer ${TOKEN_DE_LOGIN}" \
     "http://localhost/api/ai/moodle/courses/2/contents"
```

## Fase H. Rollback

Si algo sale mal, todo es reversible:

```bash
docker compose down
docker volume rm tic-kenth_moodle_data tic-kenth_moodledata_data tic-kenth_mariadb_data
# Restaurar el zip de moodledata y el dump SQL, repetir desde Fase C.
```

La instalacion original en `C:\Moodle\server` no se toca hasta que la migracion
quede verificada en el servidor.

## Backups periodicos

Anadir a cron del servidor (Linux):

```cron
# Diario a las 02:00
0 2 * * * cd /opt/tic-kenth && docker compose exec -T mariadb mysqldump -uroot -p"$(cat .env | grep MOODLE_ROOT_PASS | cut -d= -f2)" moodle | gzip > /var/backups/moodle/moodle_$(date +\%Y\%m\%d).sql.gz
```

Retener 14 dias (alineado con la retencion de Loki). Cambiar el path segun
politicas del servidor del tutor.
