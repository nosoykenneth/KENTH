# `moodle/` — Componentes Moodle versionados (fuente de verdad)

Estos son los componentes que viven **dentro de Moodle** (fuera del webroot de este
repo) pero de los que dependen el backend FastAPI y el frontend. Hasta ahora vivían
sólo en el servidor (`runtime/moodle/…`, gitignored), lo que era un riesgo de
reproducibilidad (bug **B4** de `AUDITORIA_TIC_READYNESS.md`). Aquí quedan
versionados **sin secretos** para poder reconstruir el entorno.

> ⚠️ Esta carpeta es **fuente/documentación**, no se despliega automáticamente. La
> copia viva en el servidor está en `runtime/moodle/` (montada en el contenedor
> `tic-moodle`). Ver `docs/deploy/DEPLOY_PRODUCCION.md` para sincronizar.

## Contenido

| Ruta | Qué es | Ubicación real en Moodle |
|---|---|---|
| `local_tesisai/` | Plugin Moodle `local_tesisai`: esquema operativo (`db/install.xml`), upgrades, Web Services (`db/services.php`, `externallib.php`), idioma. **Es el dueño de las tablas `mdl_local_tesisai_*` y de la WS `local_tesisai_get_permissions`.** | `moodle/local/tesisai/` |
| `api_persistente/` | Endpoints PHP nativos de auth/login, onboarding, pagos (PayPal/PayPhone) y el microservicio de roles `tesis_role.php`. | `moodle/proyecto_curso/api_persistente/` |

## Política de secretos aplicada al versionar

Auditado antes de copiar (ver `AUDITORIA_TIC_READYNESS.md` §11 B4). **No** se incluyó:

- `.env` reales (contienen tokens PayPhone/PayPal) → sólo `api_persistente/.env.example`.
- Logs con PII: `log_*.txt`, `*.log`.
- Registros de transacciones: `payments/*.json`, `*.json` de datos, `db_user_columns.json`.
- Backups `*.bak*`, binarios (`logo-main.png`) y utilidades destructivas/debug
  (`purge_all.php`, `clear_*.php`, `debug_*.php`, `check_*.php`, `test_upload.php`).
- **Secreto hardcodeado**: `tesis_lib.php` tenía `$KENTH_SECRET` en claro; se
  **redactó** a `getenv('KENTH_COURSE_ID_SECRET')` con placeholder.

`.gitignore` de la raíz refuerza esto (`.env`, `*.bak`, `*.log`, `*.sql`).

## Instalación / sincronización (resumen)

1. **Plugin**: copiar `local_tesisai/` → `<moodle>/local/tesisai/` y visitar
   *Administración del sitio → Notificaciones* para correr las upgrades del
   esquema. La WS `local_tesisai_get_permissions` debe estar adjunta al servicio
   externo `api_tesis` (id=2) y habilitada.
2. **api_persistente**: copiar `api_persistente/` → `<moodle>/proyecto_curso/api_persistente/`,
   crear el `.env` real a partir de `.env.example` y confirmar que el `.htaccess`
   bloquea el acceso directo a archivos sensibles.
3. **Secreto compartido**: `KENTH_COURSE_ID_SECRET` (backend FastAPI) debe ser
   idéntico al `$KENTH_SECRET` que resuelve `tesis_lib.php`, o las firmas de
   `course_id` no validarán.

Detalle completo en [`../docs/deploy/DEPLOY_PRODUCCION.md`](../docs/deploy/DEPLOY_PRODUCCION.md).
