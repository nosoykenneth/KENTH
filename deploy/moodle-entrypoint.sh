#!/bin/sh
# Corre como root al inicio: ajusta permisos de moodledata (bind mount del host,
# propiedad de otro uid) y arranca Apache. www-data necesita escribir moodledata.
set -e

mkdir -p /var/moodledata
# Solo cambia dueno si hace falta (evita recursion costosa en cada arranque).
if [ "$(stat -c '%U' /var/moodledata 2>/dev/null)" != "www-data" ]; then
  echo "[moodle-entrypoint] chown moodledata -> www-data ..."
  chown -R www-data:www-data /var/moodledata || true
fi

exec apache2-foreground
