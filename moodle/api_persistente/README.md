# `api_persistente/` — Endpoints PHP nativos de Moodle (auth / onboarding / pagos / roles)

Capa PHP que corre **dentro de Moodle** (webroot), servida por Apache. El frontend
la consume vía el gateway bajo `/api/lms/…` (alias legacy `/moodle_api/…`). No la
importa FastAPI; coopera por contrato HTTP.

Ubicación real: `<moodle>/proyecto_curso/api_persistente/`.

## Archivos versionados (fuente, sin secretos)

- **Roles/permisos**: `tesis_role.php` (microservicio que el frontend usa para
  resolver el rol por curso; espeja la WS `local_tesisai_get_permissions`),
  `tesis_lib.php` (firma/verificación HMAC de `course_id`).
- **Auth/perfil**: `tesis_login.php`, `api_request_password_reset.php`,
  `api_confirm_password_reset.php`, `tesis_profile.php`, `api_onboarding_process.php`.
- **Curso/contenido**: `tesis_view.php`, `tesis_course_settings.php`,
  `tesis_enrolments.php`, `tesis_actions.php`, `tesis_studio.php`, `tesis_image.php`,
  `sec_contenidos.php`, `secure_data.php`, `secure_lista.php`,
  `api_check_guest_enrollment.php`.
- **Pagos**: `api_register_intent.php`, `api_prepare_payphone.php`,
  `api_webhook_pagos.php`, `api_capture_paypal_order.php`,
  `api_register_paypal_payment.php`, `tesis_commercial.php`.
- **Seguridad**: `.htaccess` (bloquea acceso directo a `.env/.log/.txt/.json/.bak/.sql`).
- **Config**: `.env.example` (plantilla; el `.env` real va sólo en el servidor).

## NO versionado (por seguridad/privacidad)

`.env` real, `log_*.txt`, `*.log`, `payments/*.json` (transacciones con PII),
`db_user_columns.json`, `*.json` de datos, `*.bak*`, `logo-main.png`, y utilidades
de debug/destructivas (`purge_all.php`, `clear_*.php`, `debug_*.php`, `check_*.php`,
`test_upload.php`).

## Puesta en marcha

1. Copiar estos archivos al webroot de Moodle en `proyecto_curso/api_persistente/`.
2. `cp .env.example .env` y rellenar con los valores reales (tokens PayPhone/PayPal,
   `KENTH_COURSE_ID_SECRET`). El `.env` **no** debe subirse al repo.
3. Verificar que Apache tiene `AllowOverride` para que el `.htaccess` aplique.
4. `KENTH_COURSE_ID_SECRET` debe coincidir con el del backend FastAPI
   (`tesis-rag/.env`), o las firmas de `course_id` fallarán.
