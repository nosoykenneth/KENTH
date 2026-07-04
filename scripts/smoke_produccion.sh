#!/usr/bin/env bash
# ============================================================================
#  smoke_produccion.sh — Smoke test de disponibilidad del despliegue TIC KENTH.
#
#  Verifica, SIN exponer secretos, que el stack responde por el gateway:
#    - gateway "/" (SPA)                       -> 200
#    - FastAPI OpenAPI (/api/ai/openapi.json)  -> 200
#    - /api/ai/health                          -> 200 + status
#    - Moodle por el gateway (/api/lms/)       -> 200/303
#    - chat sin token                          -> 401
#    - rebuild del indice sin token            -> 401/403
#    - un asset del frontend referenciado      -> 200
#    - contenedores docker "tic-*" arriba      (si hay docker)
#
#  Con MOODLE_TOKEN (opcional) añade pruebas autenticadas:
#    - /api/ai/moodle/me con token            -> 200
#    - /api/ai/chat con token                 -> 200
#
#  Uso:
#    BASE_URL=http://localhost:8090 ./scripts/smoke_produccion.sh
#    MOODLE_TOKEN=xxxxx ./scripts/smoke_produccion.sh          # + pruebas auth
#
#  El token NUNCA se imprime ni se hardcodea. Sale con código !=0 si algo falla.
# ============================================================================
set -u

BASE_URL="${BASE_URL:-http://localhost:8090}"
CURL="curl -sS --max-time ${CURL_TIMEOUT:-15}"
PASS=0
FAIL=0

c_green="\033[0;32m"; c_red="\033[0;31m"; c_yellow="\033[0;33m"; c_reset="\033[0m"

ok()   { printf "  ${c_green}PASS${c_reset}  %s\n" "$1"; PASS=$((PASS+1)); }
bad()  { printf "  ${c_red}FAIL${c_reset}  %s\n" "$1"; FAIL=$((FAIL+1)); }
skip() { printf "  ${c_yellow}SKIP${c_reset}  %s\n" "$1"; }

# status_of METHOD URL [EXTRA_CURL_ARGS...] -> imprime el código HTTP
status_of() {
  local method="$1"; local url="$2"; shift 2
  $CURL -o /dev/null -w "%{http_code}" -X "$method" "$@" "$url" 2>/dev/null || echo "000"
}

# expect_status DESC METHOD URL CODES... (CODES = lista de aceptables, ej "200 303")
expect_status() {
  local desc="$1"; local method="$2"; local url="$3"; shift 3
  local codes="$*"
  local got; got="$(status_of "$method" "$url")"
  case " $codes " in
    *" $got "*) ok "$desc  [$got]" ;;
    *)          bad "$desc  (esperaba: $codes, obtuvo: $got)  $url" ;;
  esac
}

echo "== Smoke TIC KENTH =="
echo "Base: $BASE_URL"
echo

echo "-- Disponibilidad publica --"
expect_status "gateway / (SPA)"                 GET  "$BASE_URL/"                        200
expect_status "FastAPI OpenAPI"                 GET  "$BASE_URL/api/ai/openapi.json"     200
expect_status "Moodle via gateway"              GET  "$BASE_URL/api/lms/"                200 303 302

echo
echo "-- Health --"
health_json="$($CURL "$BASE_URL/api/ai/health" 2>/dev/null)"
health_code="$(status_of GET "$BASE_URL/api/ai/health")"
if [ "$health_code" = "200" ]; then
  # Extrae el campo status sin depender de jq.
  hstatus="$(printf '%s' "$health_json" | sed -n 's/.*"status"[[:space:]]*:[[:space:]]*"\([a-z]*\)".*/\1/p')"
  case "$hstatus" in
    ok)       ok "/api/ai/health  [200, status=ok]" ;;
    degraded) ok "/api/ai/health  [200, status=degraded]  (revisar dependencias no-criticas)" ;;
    error)    bad "/api/ai/health  [200, status=error]  (dependencia critica caida)" ;;
    *)        bad "/api/ai/health  [200, status desconocido]" ;;
  esac
else
  bad "/api/ai/health  (esperaba 200, obtuvo $health_code)"
fi

echo
echo "-- Seguridad (sin token) --"
expect_status "chat sin token -> 401"           POST "$BASE_URL/api/ai/chat"             401
expect_status "rebuild indice sin token -> 401/403" POST "$BASE_URL/api/ai/documents/rebuild" 401 403
expect_status "authoring blocks sin token -> 401" PUT "$BASE_URL/api/ai/authoring/lessons/X/blocks" 401 403 405 422

echo
echo "-- Frontend assets --"
index_html="$($CURL "$BASE_URL/" 2>/dev/null)"
asset_path="$(printf '%s' "$index_html" | grep -oE '/assets/[A-Za-z0-9._-]+\.(js|css)' | head -n1)"
if [ -n "$asset_path" ]; then
  expect_status "asset referenciado ($asset_path)" GET "$BASE_URL$asset_path" 200
else
  skip "no se hallo /assets/*.js|css en index.html (build sin hash o SPA distinta)"
fi

echo
echo "-- Contenedores Docker --"
if command -v docker >/dev/null 2>&1; then
  up="$(docker ps --filter 'name=tic-' --format '{{.Names}} {{.Status}}' 2>/dev/null)"
  if [ -n "$up" ]; then
    printf '%s\n' "$up" | sed 's/^/     /'
    n="$(printf '%s\n' "$up" | grep -c . )"
    ok "contenedores tic-* arriba: $n"
  else
    skip "docker presente pero sin contenedores 'tic-*' (¿otro host?)"
  fi
else
  skip "docker no disponible en este host (se omite chequeo de contenedores)"
fi

echo
echo "-- Pruebas autenticadas (MOODLE_TOKEN) --"
if [ -n "${MOODLE_TOKEN:-}" ]; then
  me_code="$(status_of GET "$BASE_URL/api/ai/moodle/me" -H "Authorization: Bearer $MOODLE_TOKEN")"
  case "$me_code" in
    200) ok "/api/ai/moodle/me con token  [200]" ;;
    *)   bad "/api/ai/moodle/me con token  (esperaba 200, obtuvo $me_code)" ;;
  esac
  chat_code="$(status_of POST "$BASE_URL/api/ai/chat" \
      -H "Authorization: Bearer $MOODLE_TOKEN" -H "Content-Type: application/json" \
      --data '{"pregunta":"hola","course_id":"2"}')"
  case "$chat_code" in
    200) ok "/api/ai/chat con token  [200]" ;;
    *)   bad "/api/ai/chat con token  (esperaba 200, obtuvo $chat_code)" ;;
  esac
else
  skip "MOODLE_TOKEN no definido -> se omiten pruebas autenticadas"
fi

echo
echo "== Resumen: ${PASS} PASS, ${FAIL} FAIL =="
[ "$FAIL" -eq 0 ]
