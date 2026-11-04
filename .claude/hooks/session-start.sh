#!/bin/bash
# Instala las dependencias al abrir una sesión de Claude Code en la nube, para que
# `npm run build` y `astro dev` funcionen desde el primer mensaje.
set -euo pipefail

# Solo en sesiones en la nube; en un equipo local cada quien instala con `npm ci`.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# Instala solo si cambió algo que decide qué se instala desde la última vez que salió bien.
hashes=node_modules/.session-start.sha256
if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  # Se borra antes: si la instalación falla, la próxima sesión vuelve a intentarlo.
  rm -f "$hashes"
  npm install --no-audit --no-fund
  sha256sum .claude/hooks/session-start.sh package.json package-lock.json .nvmrc > "$hashes" || rm -f "$hashes"
fi
