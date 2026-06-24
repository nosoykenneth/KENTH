#!/usr/bin/env bash
# ============================================================================
#  setup-server.sh  -  Provisiona el HOST del servidor (Ubuntu) para TIC KENTH.
#
#  Despliegue HIBRIDO:
#    - Instala/configura OLLAMA NATIVO (GPU) y descarga modelos.
#    - Instala Docker + compose plugin.
#    - Construye y levanta el APP TIER (fastapi + frontend + gateway + observabilidad).
#
#  NO instala Moodle/MariaDB ni el driver NVIDIA (ver runbook: requieren pasos
#  manuales / transferencia de datos). Este script SOLO toca lo automatizable.
#
#  Uso:   bash scripts/setup-server.sh
#  Requiere: usuario con sudo. Idempotente (se puede re-correr).
# ============================================================================
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

TEXT_MODEL="${KENTH_TEXT_MODEL:-llama3.1:8b}"
ALT_TEXT_MODEL="qwen2.5:14b-instruct"   # opcion mas fuerte para el LLM-juez; pull opcional
VISION_MODEL="${KENTH_VISION_MODEL:-qwen3-vl:4b-instruct}"
EMBED_MODEL="${KENTH_EMBED_MODEL:-nomic-embed-text}"

say()  { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m[!] %s\033[0m\n' "$*"; }
ok()   { printf '\033[1;32m[ok] %s\033[0m\n' "$*"; }

# ---------------------------------------------------------------------------
#  Firewall (ufw). El servidor tiene IP publica fija: solo SSH + HTTP/HTTPS deben
#  entrar desde internet. El gateway nginx (:80/:443) es la UNICA puerta publica.
#  Los servicios NATIVOS del host (Ollama:11434, MariaDB, Moodle:8081) solo deben
#  ser alcanzables por los CONTENEDORES (subred docker), nunca desde fuera.
#
#  OJO 1: SSH se permite ANTES de habilitar ufw para no cerrarte la sesion.
#  OJO 2: Docker publica sus puertos SALTANDOSE ufw; por eso los puertos sensibles
#         del compose (Grafana) van atados a 127.0.0.1 (ver docker-compose.server.yml).
#  Opt-out:  KENTH_SKIP_FIREWALL=1 bash scripts/setup-server.sh
configure_firewall() {
  if [ "${KENTH_SKIP_FIREWALL:-0}" = "1" ]; then
    warn "KENTH_SKIP_FIREWALL=1 -> me salto la configuracion de ufw."
    return 0
  fi
  if ! command -v ufw >/dev/null 2>&1; then
    sudo apt-get update -y && sudo apt-get install -y ufw
  fi

  # 1) Politica por defecto: nada entra, todo sale.
  sudo ufw default deny incoming
  sudo ufw default allow outgoing

  # 2) SSH PRIMERO (evita auto-bloqueo al habilitar ufw).
  sudo ufw allow OpenSSH 2>/dev/null || sudo ufw allow 22/tcp

  # 3) Unica entrada publica: el gateway (HTTP y, con TLS, HTTPS).
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp

  # 4) Permitir que los CONTENEDORES (subred bridge de Docker) alcancen los
  #    servicios NATIVOS del host. Sin esto, ufw rompe fastapi -> Ollama/MariaDB/Moodle.
  #    Estas reglas se anaden ANTES de los deny, asi que ganan para la subred docker.
  for p in 11434 3306 3307 8081; do
    sudo ufw allow from 172.16.0.0/12 to any port "$p" proto tcp
  done

  # 5) Denegacion EXPLICITA desde el exterior (defensa en profundidad + auditable;
  #    la policy default ya los cierra). 8000=backend, 11434=Ollama, 3306/3307=MariaDB,
  #    8081=Moodle, 3000=Grafana.
  for p in 8000 11434 3306 3307 8081 3000; do
    sudo ufw deny "$p"/tcp || true
  done

  sudo ufw --force enable
  ok "ufw activo. Exterior: solo SSH/80/443. Cerrados: 8000/11434/3306/3307/8081/3000."
  sudo ufw status numbered || true
}

# ---------------------------------------------------------------------------
say "1/7  Comprobando GPU NVIDIA (RTX 5070 Ti = Blackwell, sm_120)"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader || true
  ok "nvidia-smi responde."
  warn "Blackwell (5070 Ti) necesita driver >= 570 y CUDA 12.8+. Si el modelo corre en CPU, actualiza el driver ANTES de seguir."
else
  warn "nvidia-smi NO encontrado. Instala el driver NVIDIA (>=570) y reinicia:"
  warn "    sudo ubuntu-drivers install   # o el .run oficial de NVIDIA para Blackwell"
  warn "El resto del script sigue, pero Ollama correra en CPU hasta que haya driver."
fi

# ---------------------------------------------------------------------------
say "2/7  Instalando / verificando Ollama (nativo)"
if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
else
  ok "Ollama ya instalado: $(ollama --version 2>/dev/null || echo '?')"
fi

# Ollama debe escuchar en 0.0.0.0 para que el contenedor fastapi lo alcance via
# host.docker.internal. Se configura con un override de systemd (idempotente).
say "     Configurando OLLAMA_HOST=0.0.0.0:11434 (acceso desde contenedores)"
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf >/dev/null <<'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF
sudo systemctl daemon-reload
sudo systemctl enable ollama >/dev/null 2>&1 || true
sudo systemctl restart ollama
sleep 2
ok "Ollama escuchando: $(curl -s http://localhost:11434/api/version || echo 'NO responde aun')"

# ---------------------------------------------------------------------------
say "3/7  Descargando modelos (esto puede tardar varios minutos)"
ollama pull "$TEXT_MODEL"
ollama pull "$VISION_MODEL"
ollama pull "$EMBED_MODEL"
warn "Opcional (mas fuerte, ~9GB): ollama pull $ALT_TEXT_MODEL   # para el LLM-juez"
ollama list

# ---------------------------------------------------------------------------
say "4/7  Verificando que el modelo usa GPU"
ollama run "$TEXT_MODEL" "responde solo: ok" >/dev/null 2>&1 || true
if ollama ps 2>/dev/null | grep -qiE "GPU|100%/0%"; then
  ok "Ollama esta usando GPU."
else
  warn "No se confirma GPU en 'ollama ps'. Revisa driver/CUDA. (En CPU funciona pero lento.)"
  ollama ps || true
fi

# ---------------------------------------------------------------------------
say "5/7  Instalando Docker Engine + compose plugin"
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER" || true
  warn "Te agregue al grupo docker. Cierra sesion y vuelve a entrar para usar docker sin sudo."
else
  ok "Docker ya instalado: $(docker --version)"
fi
docker compose version >/dev/null 2>&1 && ok "compose plugin OK" || warn "Falta 'docker compose' plugin."

# ---------------------------------------------------------------------------
say "6/7  Firewall (ufw): solo SSH y 80/443 al exterior; el resto cerrado"
configure_firewall

# ---------------------------------------------------------------------------
say "7/7  Levantando el APP TIER (fastapi + frontend + gateway + observabilidad)"
if [ ! -f .env ]; then
  warn "No existe .env. Crealo antes de levantar:  cp .env.server.example .env && nano .env"
  warn "Saltando 'up'. Cuando el .env este listo, corre:"
  echo  "    docker compose -f docker-compose.server.yml up -d --build"
  exit 0
fi
docker compose -f docker-compose.server.yml up -d --build
echo
ok "App tier arriba. Verifica:"
echo "    docker compose -f docker-compose.server.yml ps"
echo "    curl -s http://localhost/api/ai/health || true   # ajustar al endpoint real de salud"
echo "    Gateway:  http://<IP_DEL_SERVIDOR>/        Grafana: http://<IP>:3000"
warn "Recuerda: Moodle (Apache:8081) + MariaDB(:3306) van NATIVOS y deben estar arriba (ver runbook)."
