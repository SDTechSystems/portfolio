#!/bin/bash
# PreToolUse (Edit|Write): impide editar a mano archivos que se generan solos.
# Salir con código 2 bloquea la edición y le muestra el motivo a Claude.
set -euo pipefail

ruta=$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{process.stdout.write(JSON.parse(s).tool_input?.file_path??"")}catch{}})')
rel=${ruta#"${CLAUDE_PROJECT_DIR:-$PWD}/"}

case "$rel" in
  package-lock.json)
    echo "package-lock.json no se edita a mano: usa npm install / npm uninstall para cambiar dependencias." >&2
    exit 2 ;;
  dist/*|.astro/*|node_modules/*)
    echo "$rel es generado (build, tipos de Astro o dependencias): cambia el código fuente en src/ en su lugar." >&2
    exit 2 ;;
esac
exit 0
