#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

TEXT_MODEL="${KENTH_TEXT_MODEL:-llama3.1:8b}"
VISION_MODEL="${KENTH_VISION_MODEL:-qwen3-vl:4b-instruct}"
EMBED_MODEL="${KENTH_EMBED_MODEL:-nomic-embed-text}"

say() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m[!] %s\033[0m\n' "$*"; }
ok() { printf '\033[1;32m[ok] %s\033[0m\n' "$*"; }

require_sudo() {
  if ! sudo -v; then
    echo "Este script requiere sudo." >&2
    exit 1
  fi
}

install_docker() {
  say "Instalando/verificando Docker Engine + compose"
  if ! command -v docker >/dev/null 2>&1; then
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker "$USER" || true
    warn "Usuario agregado al grupo docker. Cierra sesion y vuelve a entrar para usar docker sin sudo."
  else
    ok "Docker ya instalado: $(docker --version)"
  fi

  if docker compose version >/dev/null 2>&1; then
    ok "docker compose disponible: $(docker compose version)"
  else
    warn "No se encontro el plugin docker compose. Instala docker-compose-plugin."
  fi
}

install_ollama() {
  say "Instalando/verificando Ollama nativo"
  if ! command -v ollama >/dev/null 2>&1; then
    curl -fsSL https://ollama.com/install.sh | sh
  else
    ok "Ollama ya instalado: $(ollama --version 2>/dev/null || echo '?')"
  fi

  say "Configurando OLLAMA_HOST=0.0.0.0:11434"
  sudo mkdir -p /etc/systemd/system/ollama.service.d
  sudo tee /etc/systemd/system/ollama.service.d/override.conf >/dev/null <<'EOF'
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF
  sudo systemctl daemon-reload
  sudo systemctl enable ollama >/dev/null 2>&1 || true
  sudo systemctl restart ollama
  sleep 2
  curl -s http://localhost:11434/api/version >/dev/null && ok "Ollama responde en localhost:11434" || warn "Ollama aun no responde. Revisa systemctl status ollama."

  say "Descargando modelos"
  ollama pull "$TEXT_MODEL"
  ollama pull "$VISION_MODEL"
  ollama pull "$EMBED_MODEL"
}

configure_firewall() {
  say "Configurando ufw seguro"
  if [ "${KENTH_SKIP_FIREWALL:-0}" = "1" ]; then
    warn "KENTH_SKIP_FIREWALL=1: no se modifica firewall."
    return 0
  fi
  if ! command -v ufw >/dev/null 2>&1; then
    sudo apt-get update -y
    sudo apt-get install -y ufw
  fi

  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw allow OpenSSH 2>/dev/null || sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw allow from 172.16.0.0/12 to any port 11434 proto tcp
  for p in 3306 8000 8080 11434 3000; do
    sudo ufw deny "$p"/tcp || true
  done
  sudo ufw --force enable
  sudo ufw status numbered || true
}

prepare_runtime() {
  say "Creando runtime/ persistente"
  mkdir -p runtime/mariadb runtime/moodle runtime/moodledata runtime/chroma runtime/fastapi-chat
  ok "runtime listo. No se creo .env real. Usa: cp .env.server.example .env"
}

main() {
  require_sudo
  say "Comprobando GPU NVIDIA"
  if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader || true
  else
    warn "nvidia-smi no encontrado. Ollama puede correr en CPU hasta instalar driver NVIDIA."
  fi

  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg
  install_docker
  install_ollama
  configure_firewall
  prepare_runtime

  cat <<'EOF'

Siguiente paso manual:
  cp .env.server.example .env
  openssl rand -hex 32
  nano .env
  docker compose -f docker-compose.full.yml --env-file .env up -d --build
EOF
}

main "$@"