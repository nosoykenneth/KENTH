#!/usr/bin/env bash
# ============================================================================
#  Backup de TIC KENTH (BD Moodle + moodledata). Sin sudo.
#  Programar via crontab del usuario, p.ej. diario 3am:
#    0 3 * * * /srv/kenneth/tic-kenth/deploy/backup.sh >> /srv/kenneth/backups/backup.log 2>&1
#  Restaurar BD:  zcat moodle-db-XXXX.sql.gz | docker exec -i tic-mariadb mariadb -uroot -p<PASS> moodle
# ============================================================================
PROJECT_DIR="/srv/kenneth/tic-kenth"
DEST="/srv/kenneth/backups"
KEEP=7                      # cuantas copias retener de cada tipo
TS="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$DEST"
# Cargar secretos del .env (MARIADB_ROOT_PASSWORD)
set -a; . "$PROJECT_DIR/.env"; set +a

echo "[$(date)] backup start ($TS)"
TMP="$DEST/.moodle-db-$TS.sql"

# 1) Dump de la BD a temporal, con reintentos. El cron de Moodle puede reconstruir
#    tablas (p.ej. tag_correlation) y disparar Error 1412 con --single-transaction;
#    un reintento a los segundos suele bastar. Solo movemos a definitivo si OK.
dump_ok=0
for attempt in 1 2 3; do
  if docker exec tic-mariadb sh -c \
      "mariadb-dump -uroot -p\"$MARIADB_ROOT_PASSWORD\" --single-transaction --quick --no-tablespaces --skip-lock-tables --routines --triggers --events moodle" \
      > "$TMP" 2>"$DEST/.dumperr"; then
    dump_ok=1; break
  fi
  echo "  dump intento $attempt fallo: $(tail -1 "$DEST/.dumperr" 2>/dev/null); reintento en 12s..."
  sleep 12
done

if [ "$dump_ok" = "1" ]; then
  gzip -f "$TMP" && mv -f "$TMP.gz" "$DEST/moodle-db-$TS.sql.gz"
  echo "  db   -> $(du -h "$DEST/moodle-db-$TS.sql.gz" | cut -f1)"
else
  rm -f "$TMP"
  echo "  ERROR: dump de BD fallo tras 3 intentos (ver arriba)"
fi
rm -f "$DEST/.dumperr"

# 2) moodledata: solo lo NO regenerable (archivos reales + originales de perfil)
if tar -cf "$DEST/moodledata-$TS.tar" \
      -C "$PROJECT_DIR/runtime/moodledata" filedir tesis_profile_originals 2>/dev/null; then
  echo "  data -> $(du -h "$DEST/moodledata-$TS.tar" | cut -f1)"
else
  echo "  aviso: tar de moodledata con incidencias (continua)"
fi

# 3) Rotacion: conservar las KEEP mas recientes de cada tipo
ls -1t "$DEST"/moodle-db-*.sql.gz 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm -f
ls -1t "$DEST"/moodledata-*.tar  2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm -f

echo "[$(date)] backup done"
