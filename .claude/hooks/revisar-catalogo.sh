#!/bin/bash
# PostToolUse (Edit|Write): tras editar el catálogo, compila para que la validación de
# src/lib/catalogo.ts avise de inmediato (id repetido, precio con puntos, portada que no existe…).
# Salir con código 2 le devuelve a Claude la lista de errores para que los corrija.
set -uo pipefail

ruta=$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{process.stdout.write(JSON.parse(s).tool_input?.file_path??"")}catch{}})')

case "$ruta" in
  */Catalogo_Nintendo_Switch_Colombia/productos.json|*/src/data/tienda.ts|*/src/lib/catalogo.ts|*/astro.config.mjs) ;;
  *) exit 0 ;;
esac

cd "${CLAUDE_PROJECT_DIR:-.}"
[ -d node_modules ] || { echo "revisar-catalogo: falta node_modules (corre npm ci); no se revisó el catálogo." >&2; exit 0; }

if ! salida=$(npm run build --silent 2>&1); then
  echo "npm run build falló después de editar ${ruta##*/}:" >&2
  # La validación imprime "Revisa el catálogo:" seguido de la lista; si no está, muestra el final.
  if grep -q "Revisa el catálogo" <<<"$salida"; then
    # Astro repite el error varias veces: se muestra solo el primer bloque.
    awk '/Revisa el catálogo/ && !v {v=1; print "Revisa el catálogo:"; next} v && /^- / {print; next} v {exit}' <<<"$salida" >&2
  else
    tail -n 25 <<<"$salida" >&2
  fi
  exit 2
fi
exit 0
