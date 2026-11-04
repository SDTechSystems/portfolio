# Pruebas del catálogo en navegador

Prueba de humo de #34: Chromium sobre el sitio estático compilado, a 320, 390 y
1440 px (altos 568, 844 y 900 px). No usa el servidor de desarrollo ni envía mensajes a WhatsApp.

```sh
npm ci
npx playwright install --only-shell chromium
npm test
npm run build
npm run test:navegador
```

En Linux, si faltan bibliotecas del sistema, usar
`npx playwright install --with-deps --only-shell chromium` (requiere permisos para
instalarlas). Node debe coincidir con `.nvmrc`.

Playwright inicia y cierra `npm run preview` en `127.0.0.1:4327`. El puerto debe estar
libre; no reutiliza un servidor existente para evitar comprobar otro checkout.
`--ignore-lock` evita que Astro se separe en segundo plano al detectar un agente.
Volver a compilar después de cambiar código o datos: las pruebas leen el JSON actual
y lo contrastan con `dist/`.

La suite contiene 27 casos (9 flujos en tres anchos) y comprueba:

- Carga de todas las imágenes declaradas, sin desborde horizontal y sin huecos entre
  piezas de la retícula; «¿No ves tu juego?» cierra la sección.
- Selección de dos títulos, color de selección, total y mensaje completo, recarga y
  deselección. Los importes, nombres, variantes y destinatario salen de los datos del repo.
- Panel real: selección con Espacio, anuncio del total, Escape y devolución del foco.
- Selección de todos los productos vendibles, total y botón dentro de la barra.
- Fallo parcial del panel: se retira solo su módulo del HTML o se bloquea su petición;
  el pedido sigue funcionando y las versiones permanecen visibles.
- Sin JavaScript: todos los productos publicados mantienen enlaces de WhatsApp visibles,
  incluyendo variantes y productos de consulta. Los ocultos no deben aparecer.

- Detalles con teclado sin alterar la selección, condiciones confirmadas e idiomas
  pendientes, enlace de consulta y ausencia de controles interactivos anidados.
- Requisito de mejora visible, detalles dentro del panel, foco/Escape y WhatsApp.
- Desplegables nativos y selección directa sin JavaScript.

No compara capturas píxel a píxel ni sustituye toda la revisión visual de
`docs/diseno.md` §8: nitidez del recorte, contraste, calidad de textos y pruebas en
un celular real con WhatsApp siguen requiriendo revisión humana.

## CI y diagnóstico

El job `build` conserva su nombre y ejecuta las pruebas de Node y el build. Guarda
`dist/` durante un día; `navegador` descarga ese artefacto de la misma ejecución,
instala Chromium con caché por sistema/arquitectura/versión de Playwright y ejecuta
la suite. Las bibliotecas del sistema se instalan también cuando hay caché.

Los checks que deben exigirse en la protección de `main` son `build` y `navegador`.
Agregar el workflow no modifica esa configuración de GitHub. Al revisar #34, el
ruleset exige PR pero su lista de checks obligatorios está vacía. Cloudflare despliega
independientemente en cada push a `main`: la protección previa a la fusión es la
que evita publicar un cambio con pruebas fallidas.

Objetivo: aproximadamente tres minutos de CI, sujeto a medir en GitHub con caché
fría y caliente. El límite de seguridad del job es cinco minutos; no se ocultan
fallos con reintentos automáticos. Si falla una prueba, `fallos-navegador` conserva
sus capturas, contexto y trazas durante siete días. Localmente quedan en
`test-results/` (ignorado por Git).

```sh
# Ejecutar solo celular estrecho
npm run test:navegador -- --project=chromium-320
# Inspeccionar una traza fallida (sustituir por su ruta real)
npx playwright show-trace test-results/<prueba>/trace.zip
```

## Validación de esta implementación

En #34, con Node 22.23.4, las 22 pruebas de lógica y las 18 de Chromium pasaron. Se comprobó
que la suite falla ante tres regresiones temporales independientes: sumar un peso
extra por producto, dejar incompleto el cierre de la retícula y ocultar las versiones
cuando falta el script del panel. Cada fallo generó captura y traza. Las fuentes
originales fueron restauradas y el build regenerado después de la comprobación.
