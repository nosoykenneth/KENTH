#!/usr/bin/env bash
# ============================================================================
#  Backup de TIC KENTH (BD Moodle + moodledata). Sin sudo.
#  Programar via crontab del usuario, p.ej. diario 3am:
#    0 3 * * * /srv/kenneth/tic-kenth/deploy/backup.sh >> /srv/kenneth/backups/backup.log 2>&1
#  Restaurar BD:  zcat moodle-db-XXXX.sql.gz | docker exec -i tic-mariadb mariadb -uroot -p<PASS> moodle
# ============================================================================
set -euo pipefail

PROJECT_DIR="/srv/kenneth/tic-kenth"
DEST="/srv/kenneth/backups"
KEEP=7                      # cuantas copias retener de cada tipo
TS="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$DEST"
# Cargar secretos del .env (MARIADB_ROOT_PASSWORD)
set -a; . "$PROJECT_DIR/.env"; set +a

echo "[$(date)] backup start ($TS)"

# 1) Dump de la BD (consistente, comprimido)
docker exec tic-mariadb sh -c \
  "mariadb-dump -uroot -p\"$MARIADB_ROOT_PASSWORD\" --single-transaction --quick --no-tablespaces --routines --triggers --events moodle" \
  | gzip > "$DEST/moodle-db-$TS.sql.gz"
echo "  db   -> $(du -h "$DEST/moodle-db-$TS.sql.gz" | cut -f1)"

# 2) moodledata: solo lo NO regenerable (archivos reales + originales de perfil)
tar -cf "$DEST/moodledata-$TS.tar" \
  -C "$PROJECT_DIR/runtime/moodledata" filedir tesis_profile_originals 2>/dev/null || true
echo "  data -> $(du -h "$DEST/moodledata-$TS.tar" | cut -f1)"

# 3) Rotacion: conservar las KEEP mas recientes de cada tipo
ls -1t "$DEST"/moodle-db-*.sql.gz 2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm -f
ls -1t "$DEST"/moodledata-*.tar  2>/dev/null | tail -n +$((KEEP+1)) | xargs -r rm -f

echo "[$(date)] backup done"
