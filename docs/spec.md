# Spec: Catálogo de precios Nintendo Switch

> Documento vivo. Cualquier sesión de Claude (o persona) que retome el proyecto debe leer
> este archivo y `docs/diseno.md` antes de tocar código, y actualizar la sección
> **Estado** y **Registro de decisiones** al terminar su trabajo.

## 1. Qué es

Una web de una sola página, pensada para celular, que muestra el catálogo de **códigos
digitales** de juegos, DLC y updates para **Nintendo Switch 1 y Switch 2**, con su precio.

- Es **solo un catálogo de precios**: no hay carrito con pago, ni login, ni base de datos.
- La venta se cierra por **WhatsApp**: el cliente elige uno o varios títulos y se abre un
  chat con el mensaje ya escrito (lista + total).
- Referencia visual de partida: el póster de la tienda (encabezado rojo, "Estrenos" con
  1 portada grande + 2 chicas, mosaico de "Juegos disponibles", fila de "DLC y
  expansiones", barra final de beneficios: código oficial, actívalo en tu cuenta, sin
  riesgo de baneos).

## 2. Usuarios y objetivo

| Quién | Qué necesita |
|---|---|
| Cliente final (celular, llega por enlace o QR) | Ver rápido qué hay, cuánto cuesta y para qué consola; pedir sin fricción. |
| Dueño de la tienda (no técnico) | Cambiar precios, agregar juegos y portadas editando un archivo, sin servidor ni costos. |

**Métrica de éxito:** el cliente pasa de abrir el enlace a enviar un WhatsApp con su pedido
en menos de 30 segundos.

## 3. Requisitos (de la entrevista con el dueño)

| # | Requisito | Respuesta del dueño |
|---|---|---|
| R1 | Canal | Página web vista en celular (mobile-first). |
| R2 | Datos por título | Precio, consola (Switch 1 / Switch 2 / ambas), tipo (Juego / DLC / Update). |
| R3 | Contacto | Botón de WhatsApp por juego, con mensaje prellenado. |
| R4 | Edición | Archivo simple dentro del proyecto (JSON), sin panel ni Google Sheets. |
| R5 | Moneda | Pesos colombianos: `es-CO` / `COP` (formato `$ 239.900`). |
| R6 | Tamaño | Menos de 30 títulos → no hace falta buscador ni paginación. |
| R7 | Portadas | Las pone el dueño en `src/assets/Catalogo_Nintendo_Switch_Colombia/imagenes/`; Astro las optimiza. |
| R8 | Marca | Por ahora marcadores: "Tu Tienda" y un número de ejemplo. |
| R9 | Diseño | Elegido: **A · Tablero** (ver `docs/diseno.md`). |

### Funcionalidades

- **F1. Orden:** 3 destacados en grande (`tienda.ts → destacados`), luego el resto de juegos
  juntos y sin título, en el orden del archivo. "DLC y updates" es la única sección con título
  (oculta hoy). Un juego con versión para cada consola es **un solo mosaico** con un precio por
  versión (Switch 1, Switch 2 y paquete de mejora): en `productos.json` cada versión es su propia
  entrada y comparten `"grupo"`. Cada precio se elige por separado y llega al pedido con su consola.
  En celular y escritorio el mosaico es de tamaño normal ("3 versiones · desde $ …") y al tocarlo las
  versiones se eligen en un panel (abajo en celular, centrado en escritorio); sin JavaScript se ven en el mosaico.
- **F2. Arma tu pedido:** cada precio lleva un "+"; tocar el mosaico lo marca (✓) y lo suma
  a una barra fija inferior ("$ 1.648 · Vaciar · Pedir por WhatsApp"). El "+" sustituye al
  texto de ayuda. El botón envía un solo mensaje:
  ```
  Hola, quiero pedir:
  • Super Mario Bros. Wonder (Juego · Switch 1 y 2) $999
  • Resident Evil 2 (Juego · Switch 2) $649
  Total: $1,648
  ```
- **F3. Sin JavaScript:** cada título es un enlace `wa.me` con su propio mensaje, así que
  sigue funcionando si el script falla.
- **F4. Mosaico "¿No ves tu juego?"** al final de Juegos y de DLC → WhatsApp genérico
  (sustituye al "Y muchos más" de la referencia).
- **F5. Sin portada:** si un título no tiene `imagen`, queda el fondo gris de la portada.
- **F6. Sin textos secundarios:** ni eslogan, ni ayuda, ni beneficios. La **consola** la marca
  una **pestaña con el logo de Switch** en la esquina de cada portada (Switch 2: en rojo y con
  "2"). Bajo el nombre solo va la nota si hay ("Necesita Ring-Con").

### Fuera de alcance (no hacer sin que el dueño lo pida)

Pagos en línea, cuentas de usuario, inventario/stock en tiempo real, panel de
administración, buscador, varias páginas, multi-idioma.

## 4. Arquitectura

- **Stack:** Astro 7 (`astro@^7.4.5`), Node ≥ 22.23.4, salida estática (`npm run build` → `dist/`).
- **Publicación:** Cloudflare Workers (Worker `sdtechimport`) conectado a GitHub: cada push a `main`
  ejecuta `npm run build` y `npx wrangler deploy`. `wrangler.jsonc` sube `dist/` como sitio estático;
  sin él, Wrangler intenta autoconfigurar el proyecto con el adaptador de servidor de Astro y falla.
  Variable `NODE_VERSION=22.23.4` en el panel, además de `.nvmrc`. Las ramas que no son `main` (PR)
  se publican con `npx wrangler preview`, que exige `"previews": {}` en `wrangler.jsonc`.
- **Fuente:** API de fuentes de Astro con proveedor local (`astro.config.mjs`), archivos del paquete
  `@fontsource/schibsted-grotesk` (OFL): solo `latin`, pesos 500 y 800, precargados, con respaldo de
  métricas ajustadas. Ni el build ni la visita dependen de Google.
- **Vista previa al compartir:** `pages/og.jpg.ts` genera con `sharp` una imagen 1200×630 con los 3
  destacados (60/40 como el tablero de escritorio). Las etiquetas `og:*` y `twitter:card` de
  `Layout.astro` solo incluyen imagen, `og:url` y `canonical` si `tienda.ts → url` está lleno.
  Sin frameworks de UI ni Tailwind: CSS con alcance por componente.
- **Dev server:** `astro dev --background` (ver `AGENTS.md`); `astro dev stop|status|logs`.
- **GitHub:** `.github/workflows/build.yml` compila (y valida el catálogo) en cada PR y push a
  `main`, con la versión de Node de `.nvmrc` (exacta: 22.23.4, el mínimo de Astro 7). `.github/dependabot.yml` abre PRs de actualización los
  lunes (npm agrupado salvo versiones mayores; Actions agrupadas; `cooldown` de 3 días, 7 en mayores). El CI cancela
  ejecuciones viejas solo en los PR, nunca en `main`, y se puede relanzar a mano desde Actions. Plantilla de PR con la lista
  de revisión de `diseno.md` §8. El repo es privado: GitHub Pages y la protección de ramas
  requieren plan de pago, así que el CI avisa pero no bloquea la fusión.

```
src/
  data/
    tienda.ts         ← nombre, url pública, WhatsApp, moneda/locale, ids destacados, mostrarDlcUpdates
  assets/switch.svg   ← logo de Switch de la pestaña (reemplazable por el archivo oficial, D9)
  assets/Catalogo_Nintendo_Switch_Colombia/
    productos.json    ← la lista de títulos (lo único que edita el dueño a diario)
    imagenes/<id>.webp← portadas 16:9 (Astro genera 320/400/480/560/640/800/960 px en webp)
  lib/catalogo.ts     ← lee productos.json → destacados, secciones; precio(), whatsapp(), item()
  components/
    Mosaico.astro     ← un producto: portada optimizada + pestaña de consola, nombre, nota, precio con "+"/"✓"
    Pedido.astro      ← barra del pedido + script de selección
  layouts/Layout.astro← <head> (fuente, og:*), tokens de color en :root, reset global
  pages/
    index.astro       ← la página: diseño A · Tablero
    favicon.svg.ts    ← ícono de pestaña: inicial de tienda.nombre en blanco sobre rojo
    og.jpg.ts         ← imagen de vista previa al compartir (1200×630, ~165 KB)
docs/                 ← este spec y las directrices de diseño
```

### Modelo de datos (`src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json`)

Cada entrada de `productos` (campos que usa la web; el resto se ignora):

```jsonc
{
  "id": "mario-kart-world",          // único, kebab-case
  "titulo": "Mario Kart World",
  "plataforma": "Nintendo Switch 2", // "Nintendo Switch" → "Switch 1"; "Nintendo Switch 2" → "Switch 2"
  "tipo_producto": "juego_digital",  // "juego_digital" | "juego_con_accesorios" (añade "Necesita Ring-Con") | "dlc" | "update" | "paquete_mejora"
  "grupo": "zelda-totk",              // OPCIONAL: igual en las versiones de un mismo juego → un mosaico con un precio por versión
  "precio_venta_cop": 299900,        // OPCIONAL: tu precio. Si falta, se usa el de referencia
  "precio_referencia_eshop_colombia_cop": 319900, // null → muestra "Consultar" y no entra al pedido
  "publicar": false,                 // OPCIONAL: false = no sale en la página (se valida igual)
  "imagen": { "ruta": "imagenes/mario-kart-world.webp" } // opcional; sin imagen: bloque de color
}
```

**Validación al compilar** (`lib/catalogo.ts`): `npm run build` se detiene con una lista en español
si un `id` no es kebab-case o está repetido, falta `titulo`, `plataforma` o `tipo_producto` no son
uno de los valores de arriba, un precio no es entero positivo o `null`, la portada no existe, o en
`tienda.ts` los destacados no son 3 ids existentes y distintos o el WhatsApp no son 11–15 dígitos.
También revisa los grupos: cada `grupo` lleva el juego de Switch 1 y al menos otra versión, como
máximo uno de cada clase (Switch 1, Switch 2, paquete de mejora); el `paquete_mejora` va con
`"plataforma": "Nintendo Switch 2"` y siempre en un grupo; DLC y updates no se agrupan; y dos destacados
no pueden ser versiones del mismo juego.

**Versiones de un juego** (ej. Zelda: Tears of the Kingdom): una entrada por cosa que se vende, con
el mismo `grupo`. El mosaico usa el nombre y la nota del juego de Switch 1, la portada de la versión
de Switch 2 si la tiene (si no, la primera que haya) y va en el lugar de la primera entrada del
grupo. Un destacado puede nombrar cualquiera de sus ids.

Orden: el del archivo (por `puesto_ranking`). Los **destacados** se eligen en `tienda.ts → destacados`
(lista de ids, en orden: el primero es la portada grande). El diseño está pensado para
**exactamente 3 destacados**. La sección "DLC y updates" está **oculta** con
`tienda.ts → mostrarDlcUpdates: false`; con `true` aparece si hay al menos un DLC o update
(`tipo_producto: "dlc"` o `"update"`). Mientras está oculta, esos productos no se muestran.

### Contrato de `Pedido.astro`

Cualquier elemento con los atributos que devuelve `item(p)` (`href`, `data-item`,
`data-nombre`, `data-precio`, `data-detalle`) se vuelve seleccionable: el script le pone
`role="button"` y `aria-pressed`, y responde a Enter y Espacio. **`aria-pressed` es el único estado** (no hay clases ni
`Set` aparte): el CSS de `Mosaico.astro` dibuja "+" o "✓" a partir de él, así que sin
JavaScript no aparece ningún "+" y el enlace `wa.me` funciona solo. Los colores salen de los
tokens globales de `Layout.astro`. La selección (lista de `data-item`) se guarda en
`sessionStorage` bajo la clave `pedido`, para que sobreviva si el celular recarga la pestaña al
volver de WhatsApp; si el almacenamiento está bloqueado, todo funciona igual sin guardar.

## 5. Estado (actualizar al cerrar cada sesión)

**Última actualización:** 2026-11-04 (escritorio simétrico y portadas de 1920 px), rama `claude/beautiful-cannon-3a7uu7` (sale de `main`).

Hecho:
- [x] Entrevista y requisitos (sección 3).
- [x] Diseño A · Tablero como página principal `/` (celular y escritorio). Diseños B y C y selector borrados.
- [x] Catálogo real de Colombia: 24 juegos de `productos.json` (23 Switch 1, 1 Switch 2), sin DLC ni updates.
- [x] Portadas reales optimizadas por Astro (de 70–175 KB a 12–130 KB por variante, webp).
- [x] Tienda en `es-CO` / `COP`. Barra "Arma tu pedido" probada: 3 títulos → `$ 799.700` correcto; "Vaciar" limpia.
- [x] Verificado a 390 px y 1440 px: sin scroll horizontal, sin huecos en filas, 24/24 imágenes cargan.
- [x] Simplificación (F6): fuera eslogan, ayuda, beneficios, nombre gigante final, mosaico
      "Pedir por WhatsApp" de arriba, títulos "Estrenos"/"Juegos disponibles" y "Switch 1" repetido.
      `Portada.astro` se fundió en `Mosaico.astro`. Barra verificada de 320 a 1440 px con los
      23 juegos elegidos ($ 6.117.700): no se desborda.
- [x] Pestaña de consola con logo (propuesta A elegida por el dueño en el artifact "Sello de consola").
      Verificado en navegador a 320, 390 y 1440 px: 24/24 pestañas, Switch 2 en rojo, al elegir
      la pestaña de Switch 1 se vuelve negra con el mosaico, sin scroll horizontal ni huecos,
      barra sin desbordes, mensaje con la consola de cada juego.

- [x] Robustez (rama `mejoras/pedido-y-validacion`): validación de `productos.json` y `tienda.ts`
      al compilar (probada con 6 errores a propósito: los 6 se reportan y el build falla); Espacio
      selecciona un mosaico; el pedido sobrevive a recargar (probado: 3 títulos, mismo total y
      mismo enlace tras recargar; "Vaciar" + recargar deja la barra oculta; con `sessionStorage`
      bloqueado la barra funciona); favicon propio (fuera los de la plantilla de Astro); README
      reescrito como guía para el dueño.

- [x] Robustez fusionada en `main` (PR #3).
- [x] Repo: CI de build, `.nvmrc` (Node 22.23.4), Dependabot y plantilla de PR (rama `ci/build-y-dependabot`).
      Verificado: YAML válido; `npm ci` + `npm run build` desde una copia limpia pasan (0 vulnerabilidades).
      El CI solo se verá correr en GitHub al abrir el PR. Fusionado (PR #4).
- [x] Vista previa al compartir (rama `mejoras/vista-previa-y-fuente`): `og.jpg` de 164 KB (< ~300 KB
      que acepta WhatsApp); con `url` lleno salen 13 etiquetas con direcciones absolutas; sin `url`, no
      sale ninguna imagen rota; 3 URLs mal escritas (sin https, http, con ruta) detienen el build con
      mensaje claro.
- [x] Publicado en Cloudflare Workers: **https://sdtechimport.madaeauchija.workers.dev** (PR #7). El
      primer despliegue falló al publicar (`public/.assetsignore` no existe: `public/` desapareció al
      borrar los favicons de la plantilla, y Wrangler intentó autoconfigurar); arreglado con
      `wrangler.jsonc`. El dueño confirmó el despliegue; desde el entorno de trabajo `workers.dev`
      está bloqueado, así que no se verificó en vivo.
- [x] `tienda.ts → url` con la dirección pública: el build genera `og:image`, `og:url` y `canonical`
      absolutos (rama `mejoras/url-publica`).
- [x] Fuente propia: 0 peticiones a Google (antes 2); 49 KB de fuente (antes 46); la página se ve
      igual que `main` (0,12 % de píxeles distintos a 390 px, 0,05 % a 1440 px: suavizado de letra).
      Probado con `astro build` y `astro dev`.

- [x] Sitio publicado revisado en vivo (PR #8): HTML idéntico al de `main` compilado; 26/26 comprobaciones
      de navegador a 320, 390 y 1440 px (retícula, 24/24 portadas, pestañas, fuente propia, 0 peticiones
      externas, pedido, recarga, barra con los 23 elegidos); `og.jpg` 200 `image/jpeg` 164 KB; `/no-existe` → 404.
- [x] WhatsApp real: `573058147293` (WhatsApp Business del dueño). Verificado en el build: 25 enlaces
      `wa.me` y la barra del pedido usan el número nuevo; 0 restos del falso.

- [~] Check "Workers Builds: sdtechimport" en rojo en todos los PR (#7–#9): el sitio compila, pero en
      ramas que no son `main` Cloudflare ejecuta `npx wrangler preview`, que falla sin un bloque
      `previews` en `wrangler.jsonc`. Agregado `"previews": {}`; `wrangler deploy --dry-run` sigue
      leyendo los 105 archivos. `wrangler preview` no tiene modo simulado: se confirma en el próximo PR.
- [x] Nombre real: **SD Tech Import** (título, cabecera, `og:title`/`og:site_name`, favicon "S").
      Verificado a 320, 390 y 1440 px: el nombre cabe en 1 línea, sin scroll horizontal.
- [x] Ajustes de repo (rama `ccr-1435d390-b65ozp`): Dependabot espera 3 días (7 en versiones mayores)
      antes de proponer una versión nueva; el CI ya no cancela builds en `main`, no deja el token en el
      runner y se puede relanzar a mano; `.gitignore` ignora `.wrangler/` y `.dev.vars*`; `.gitattributes`
      fija finales LF. Pendiente en Settings (lo hace el dueño): borrar ramas al fusionar y activar alertas
      de Dependabot.
- [x] Automatizaciones de Claude Code en `.claude/` (rama `ccr-1435d390-b65ozp`):
      hook de inicio que instala dependencias en sesiones en la nube (5 s la primera vez, 0,005 s si no
      cambió nada; reinstala al cambiar `package.json`, `package-lock.json` o `.nvmrc`); hook que compila
      al editar `productos.json`, `tienda.ts`, `catalogo.ts` o `astro.config.mjs` y devuelve la lista
      "Revisa el catálogo" (probado con 2 errores a propósito: los 2 se reportan; build ~5 s); hook que
      bloquea editar `package-lock.json`, `dist/`, `.astro/` y `node_modules/`; skills `/nuevo-producto`
      y `/cerrar-sesion`; subagente `revisor-diseno`. Sin `.mcp.json`: `mcp.docs.astro.build` está
      bloqueado por la red del entorno en la nube.
- [x] `CLAUDE.md` con comandos y arquitectura para Claude Code; importa `AGENTS.md` en vez de repetirlo.
- [x] Auditoría de accesibilidad WCAG 2.1 AA (axe-core + Chromium a 320, 390 y 1440 px), rama
      `a11y/foco-y-lector`. Ya cumplía: contraste de texto (mínimo 4,80:1, blanco sobre rojo), teclado
      (Enter y Espacio), orden de foco igual al visual, sin scroll horizontal a 320 px, `reduced-motion`.
      Corregido: contorno de foco en tinta (antes blanco sobre gris, 1,21:1, en mosaicos elegidos y
      "¿No ves tu juego?"); la barra ya no tapa el mosaico con foco (26 casos → 0); barra como `<aside
      aria-label="Tu pedido">` (axe `region` → 0); anuncio "Total del pedido: $ …" (antes solo el monto, y
      no se anunciaba al aparecer la barra); "+"/"✓" fuera del nombre del botón. axe: 0 fallos. Aspecto:
      0 % de píxeles distintos a 320, 390 y 1440 px. No se probó con VoiceOver/NVDA reales.
- [x] Crítica de diseño aplicada (rama `diseno/critica`). Escritorio: precios destacados visibles sin
      desplazar 1/3 → 3/3 a 1366×768, 1440×900 y 1920×1080 (cabecera 304 → 171 px, `h1` en 1 línea, imagen de
      los destacados chicos con alto máx. `50svh − 182px`; a 1366×768 queda en 2,63:1 y recorta el logo de
      Wonder por abajo). `h1` "Códigos para Switch 1 y 2" (también en `og:title`). Nombres en 800: a 320 px se
      cortan 3 de 24 (antes 2), a 390 px y más, 0. "Consultar" con "↗". Portadas de Let's Go Pikachu/Eevee sin
      el cartel "Demo Available" (pintado con el cielo de alrededor). axe: 0 fallos. Celular sin cambios de
      retícula (a 320×568 los destacados chicos ya quedaban bajo el pliegue y siguen igual).
      No hecho: "¿No ves tu juego?" más angosto en escritorio (con 21 juegos deja un hueco de 4 columnas, =2
      mosaicos, y rompe `diseno.md` §8); insignias "WINNER" de 3 portadas y caja de Ring Fit (hace falta otra
      imagen; `assets.nintendo.com` está bloqueado en el entorno).

- [x] Juegos con varias versiones en un solo mosaico (rama `catalogo/dos-versiones`): campo `grupo` y
      `tipo_producto: "paquete_mejora"` en `productos.json`; mosaico ancho con pestaña doble y una fila por
      versión (sello de consola o "Mejora a ⊞2", precio y su propio "+"). Cargados los dos Zelda con Switch 2
      Edition y paquete de mejora, con precios de referencia de la eShop de Colombia
      (`nintendo.com/es-co`, precio regular, sin descuento): TotK $ 279.900 / $ 319.900 / $ 39.900;
      BotW $ 239.900 / $ 279.900 / $ 39.900. Los de Switch 1 coinciden con los que ya tenía el archivo.
      Portadas oficiales de Switch 2 Edition (2400×1350 → 960×540 webp, 99 y 86 KB); en celular se recortan
      desde abajo para conservar la franja "Nintendo Switch 2 Edition". Elegir 3 versiones → `$ 639.700`
      correcto. `og.jpg` con la portada nueva de TotK: 168 KB.
      Agregados también **Super Mario Bros. Wonder** (Switch 2 Edition + Meetup in Bellabel Park $ 319.900,
      mejora $ 79.900) y **Animal Crossing: New Horizons** (Switch 2 Edition $ 259.900, mejora $ 19.900), con
      sus portadas oficiales. Ahora son 4 juegos con versiones (24 mosaicos, 32 cosas a la venta). La franja
      de Animal Crossing está arriba: campo opcional `imagen.recorte` ("arriba" | "centro" | "abajo", validado).
      Con los 2 destacados chicos con versiones, en escritorio llevan alto mínimo `max(190px, 50svh − 140px)`
      para que la portada grande no se recorte: Mario Kart World 2,01:1 a 1366×768 (era 2,58:1) y los 9 precios
      destacados visibles sin desplazar desde 1100×700 hasta 1920×1080. axe: 0 fallos.
      Precio de Wonder (Switch 1) actualizado de $ 279.900 a **$ 239.900**, como lo muestra hoy
      `nintendo.com/es-co` (regular, sin descuento); decisión del dueño. Sin grupos, el HTML es igual al de `main` (solo cambia el orden
      de los atributos). Verificado a 320, 390, 1000, 1366, 1440 y 1920 px: sin scroll horizontal, sin
      filas que se salgan, precios alineados; los 3 destacados con su primer precio visibles sin
      desplazar a 1366×768, 1440×900 y 1920×1080 (todas las filas de Zelda TotK también). Pedido: elegir
      Switch 1 de dos juegos → `$ 519.800` y el mensaje dice "(Juego · Switch 1)"; las filas "Consultar"
      no se suman. Validación probada con 5 errores a propósito: se reportan los 5. axe: 0 fallos a 390 y
      1440 px; cada fila se lee como "Nombre del juego, Nintendo Switch 2, $ …". Retícula: el cierre
      "¿No ves tu juego?" lo calcula `lib/reticula.ts` (simula `grid-auto-flow: dense`); con 21 chicos da
      lo mismo que la fórmula anterior (3 y 8 columnas).
      Tras la crítica de diseño: precios alineados a la derecha junto al "+" (mismo borde derecho en las 3
      filas a 320 y 390 px) y portada 3:1 en celular (mosaico 341 → 310 px a 390 px; página −93 px; luego
      reemplazado por el panel de versiones, ver abajo).
      **Celular rehecho con panel** (el dueño: "el sitio va más enfocado a mobile"): con los mosaicos a todo
      el ancho la página pasó de 3,4 a 4,4 pantallas a 390 px y la primera mostraba 2 mosaicos enteros en
      vez de 3. Ahora el juego con versiones es un mosaico normal ("3 versiones · desde $ 279.900" y "+");
      tocarlo abre un `<dialog>` desde abajo (`PanelVersiones.astro`) al que se mueven sus filas. Resultado
      a 390 px: 2.901 px de alto = 3,4 pantallas (`main`: 2.847) y 3 mosaicos enteros en la primera, como
      en `main`; ya no crece con más juegos con versiones. Probado a 320 y 390 px: abre al tocar la portada,
      con Enter y con Tab; elegir Switch 2 + mejora de TotK → `$ 359.800` y mensaje correcto; "Listo",
      Escape y tocar el fondo cierran; el foco vuelve al mosaico; las filas vuelven a su lugar; el mosaico
      queda en negro con ✓; el pedido sobrevive a recargar. Sin JavaScript (`<noscript>`) las 12 filas se
      ven en el mosaico a todo el ancho y son enlaces `wa.me`. Escritorio sin cambios (mismas medidas).
      axe: 0 fallos a 390 y 1440 px y con el panel abierto; el total se anuncia desde el panel.
      Revisión de diseño aplicada: el panel se cierra si el ancho pasa a escritorio (girar el teléfono); el ✓
      del mosaico se lee "versión elegida"; título del panel en 2 líneas máx.; sin JavaScript la portada a
      todo el ancho va 3:1; tamaños de "Listo" y "N versiones · desde" documentados en `diseno.md` §2.
      Contrapartidas: elegir versión en celular cuesta un toque más; "3 versiones · desde" es texto nuevo;
      sin JavaScript, en celular el juego con versiones ocupa todo el ancho; entre 760 y 1099 px el mosaico ancho es más alto
      que sus vecinos y los estira (~130 px en blanco a 1000 px); si el archivo termina con varios juegos
      con versiones, puede quedar un hueco de un mosaico (lo permite §8); un grupo con solo Switch 1 +
      paquete de mejora muestra igual la pestaña doble (el juego se puede jugar en Switch 2 con la mejora).

- [x] **Peso de portadas** (T7, rama `claude/beautiful-cannon-3a7uu7`): `sizes` con el ancho exacto de cada
      mosaico (antes `50vw`, un 8 % de más) y variantes cada 80–160 px (320, 400, 480, 560, 640, 800, 960).
      Medido con Playwright, sumando el archivo que elige el navegador en cada portada (24/24):
      iPhone 13, Pixel 5 y Galaxy S8 1.057 → 898 KB (−15 %); iPhone 14 Pro Max 1.964 → 1.057 KB (−46 %;
      con `50vw` creía necesitar 645 px y bajaba la de 960); escritorio ×2 1.057 → 898 KB; iPhone SE y
      escritorio ×1 sin cambio. Nitidez igual: el mínimo de píxeles servidos por píxel en pantalla no
      cambia (0,57–1,13 según el equipo; lo limita el original de 960 px del destacado grande), el
      máximo baja de 1,59 a ≤ 1,12. HTML idéntico salvo `srcset`/`sizes`; mismo alto de página a 320,
      390 y 1440 px, sin scroll horizontal, 2 títulos → `$ 559.800`. `dist/` 4,9 → 7,6 MB (72 variantes
      más; no las baja nadie). Build en caché ~4 s.
      **AVIF probado y descartado** (ver registro): con la misma nitidez ahorra 4 % y el build pasa de
      ~5 s a 1 min 16 s.

- [x] **Escritorio simétrico y nítido** (rama `claude/beautiful-cannon-3a7uu7`, pedido del dueño: "en celular se ve
      perfecto, en escritorio horrible"). Tres problemas medidos a 1440 px y corregidos:
      1. *Asimetría:* los juegos con versiones medían 4 columnas con la portada a un lado; las filas mezclaban
         mosaicos de 2 y 4, `dense` desordenaba el catálogo y quedaban zonas en blanco. Ahora miden lo mismo que
         cualquier juego y abren el **mismo panel que en celular** (centrado en escritorio): 5 mosaicos por fila,
         del mismo alto en cada fila (medido a 1024 y 1920 px), en el orden del archivo.
      2. *Portadas borrosas:* los originales eran de 960×540. El grande a 1440 px se dibuja a 1.123 px (×2:
         2.247 px) y recibía 960; los de versiones con portada vertical se dibujaban a 551 px y recibían 320
         (`sizes` no contaba el recorte). Se reemplazaron las 28 portadas por las originales de Nintendo
         (`fuente_imagen` sin transformación, 1920×1080, webp q86; misma imagen: diferencia media 3–6 de 255;
         `ancho`/`alto` actualizados en `productos.json`). Pikachu y Eevee traían la etiqueta "Demo Available":
         se tapó con la franja limpia de la versión anterior. Variantes hasta 1920 y `sizes` medidos.
         Ahora cada portada recibe ≥ 90 % de los píxeles que dibuja (1440 ×1 y ×2, 1024 ×2, 1920).
      3. *Tablero sin límite:* a 1920 px los mosaicos crecían de más; ahora el tablero mide máx. 1440 px, centrado.
      Celular **sin cambios**: posición y tamaño de todos los elementos idénticos a 320, 390 y 759 px (comparado
      contra el build anterior); solo el destacado grande en celulares de densidad 3 baja 1.120 px en vez de 960.
      Los 3 precios destacados se ven sin desplazar a 1280×800, 1366×768 y 1440×900. 2 títulos → `$ 559.800`.
      `src/assets/…/imagenes` 2,9 → 9 MB en el repo. Sin JavaScript, en escritorio el juego con versiones mide
      4 columnas (las filas no caben en 2) y "¿No ves tu juego?" puede no cerrar exacto la fila, como ya pasaba en celular.

- [x] **Precios de venta** (merge de `main` con `Precios_Finales_Catalogo_Nintendo.json`, 38 productos): a los 32 de
      `productos.json` se les copiaron todos los campos del listado (precio de venta, 14 precios de referencia corregidos
      de 279.900 a 239.900, `estado_precio`, `publicar`, `requiere_juego_base`), conservando `imagen` (1920×1080).
      Verificado: los 31 precios de la página = `precio_venta_cop` del listado; Ring Fit (`publicar: false`, sin precio)
      no sale; 20 juegos → filas completas (escritorio 4×5, celular 10×2) y "¿No ves tu juego?" a todo el ancho;
      2 títulos → `$ 332.800`. `publicar` se valida (probado: `"no"` y un destacado oculto detienen el build).
      Los 6 productos nuevos del listado (Ocarina of Time, Pokopia, Jamboree Switch 1 + Switch 2, Metroid Prime 4,
      Splatoon Raiders) se agregaron al final con su portada oficial (`og:image` de su página en nintendo.com/us,
      original 1920×1080, sin etiquetas; fuentes en `imagen.fuente_*`). A los 4 con un `grupo` de un solo producto se
      les quitó el grupo (el build lo rechaza). Página: 37/37 productos publicables del listado con su precio exacto;
      escritorio 5 filas de 5 + "¿No ves tu juego?" a todo el ancho; `og.jpg` 183 KB.

Pendiente de datos del dueño: logo de la tienda (opcional, va en lugar del nombre en `.cabecera`, ver `diseno.md` §7).

## 6. Tareas pendientes (en orden)

- [x] **T1. Consolidar el diseño A.**
- [x] **T2. Datos reales de la tienda:** país/moneda, WhatsApp (`573058147293`) y nombre (SD Tech Import).
- [x] **T3. Catálogo real** (con la salvedad de precios, D5).
- [x] **T4. Portadas reales.**
- [ ] **T4b. Contenido de DLC y updates:** agregarlos a `productos.json` (con portada) y
      poner `mostrarDlcUpdates: true`. Revisar que la fila final no deje huecos.
- [~] **T5. Metadatos para compartir:** hecho (`og:*`, imagen 1200×630, URL puesta). Falta probar
      el enlace en un chat de WhatsApp real.
- [~] **T6. Publicación:** hecho en Cloudflare Workers. Falta el QR del enlace (en el entorno de
      trabajo no hay generador de QR instalado ni permiso para descargar uno).
- [~] **T7. Auditoría:** hecho: Espacio en los mosaicos; fuente alojada en el sitio; accesibilidad WCAG 2.1 AA
      (contraste, foco, lector de pantalla); peso de portadas (−15 % en celular, −46 % en iPhone grande, sin
      perder nitidez). Falta: prueba en un celular real con WhatsApp. Opcional (decide el dueño): bajar la
      calidad webp de 78 a 70 ahorraría otro ~11 % con una pérdida pequeña de nitidez (SSIM 0,991 → 0,984).

## 7. Decisiones abiertas (preguntar al dueño)

| # | Pregunta | Supuesto actual |
|---|---|---|
| D1 | ~~¿País de venta?~~ | **Resuelta:** Colombia (`es-CO`, `$ 239.900`). |
| D2 | ~~Nombre y WhatsApp~~ · Logo | **Resuelta en parte:** "SD Tech Import", `573058147293`. Falta solo el logo (opcional); hoy la cabecera muestra el nombre en texto. |
| D3 | ¿Volver a poner las píldoras rojas "NUEVO" de la referencia? | No (ver `diseno.md` §6). Los destacados se distinguen por tamaño. |
| D4 | ~~¿Dónde se publicará?~~ | **Resuelta:** Cloudflare Workers, https://sdtechimport.madaeauchija.workers.dev (en `tienda.ts → url`). Si se agrega un dominio propio, cambiar `url` y regenerar el QR. El repo es privado: GitHub Pages exige plan de pago; Cloudflare Pages y Netlify publican gratis desde repo privado y leen `.nvmrc`. |
| D5 | ~~¿Los precios de venta son los de referencia de la eShop?~~ | **Resuelta:** el dueño entregó `Precios_Finales_Catalogo_Nintendo.json` con `precio_venta_cop` para todo; se muestran esos. |
| D6 | ¿Marcar los juegos de Switch 1 como "Switch 1 y 2"? (casi todos corren en Switch 2) | No: van en la sección "Switch 1", tal como dice `plataforma`. |
| D7 | Ring Fit Adventure no tiene precio digital y necesita el accesorio Ring-Con. ¿Se vende? | Se muestra con "Consultar" y abre WhatsApp para preguntar; no entra al pedido. |
| D9 | Logos oficiales de Switch y Switch 2, y permiso para usarlos | Ícono de Simple Icons; Switch 2 compuesto (ícono + "2"). Pedir los archivos al distribuidor y confirmar que la tienda puede mostrarlos. |
| D8 | ¿Qué títulos van destacados? | Pedido del dueño: Zelda: Ocarina of Time (Switch 2) como estelar, en lugar de Mario Kart World (vuelve al catálogo); siguen Super Mario Bros. Wonder y Zelda: Tears of the Kingdom. |

## 8. Registro de decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-11-04 | Astro estático + JSON en el repo | El dueño edita un archivo; sin costo ni servidor. |
| 2026-11-04 | Primera ronda (Bento, Vitrina oscura, Lista) **rechazada** | Muy genérica, poco fiel a la referencia, portadas falsas. |
| 2026-11-04 | Segunda ronda guiada por [taste-skill](https://github.com/Leonxlnx/taste-skill): A Tablero, B Póster, C Códigos | Reglas anti-"diseño genérico" + portadas reales. Sus scripts no se ejecutaron (bloqueados por permisos); se usó como lectura. |
| 2026-11-04 | **Elegido A · Tablero** | Fiel a la estructura del póster original. |
| 2026-11-04 | Pedido múltiple con un solo WhatsApp | Un cliente suele comprar juego + DLC; un mensaje con total reduce idas y vueltas. |
| 2026-11-04 | La web lee `productos.json` directamente; se borró `catalogo.json` y `public/portadas/` | Una sola fuente de datos: el archivo que entregó el dueño. Evita copias desincronizadas. |
| 2026-11-04 | Portadas vía `astro:assets` (`<Image>`, 4 anchos webp) en vez de `public/` | El dueño las dejó en `src/assets`; Astro las reduce de peso automáticamente. |
| 2026-11-04 | Estrenos definidos por ids en `tienda.ts` | `productos.json` no tiene campo de estreno; así no se altera el archivo del dueño y el orden es explícito. |
| 2026-11-04 | Campo opcional `precio_venta_cop` | Permite poner el precio propio sin perder el de referencia (D5). |
| 2026-11-04 | El mosaico "¿No ves tu juego?" se ensancha hasta cerrar la última fila | Con 21 juegos quedaba un hueco de 3 mosaicos en escritorio (regla §8 de `diseno.md`). |
| 2026-11-04 | Sección "DLC y updates" oculta con `mostrarDlcUpdates: false` | Pedido del dueño: se conserva para agregar contenido después sin que se publique a medias. |
| 2026-11-04 | `alt=""` en portadas | El nombre ya está escrito en el mosaico; evita que el lector de pantalla lo lea dos veces. |
| 2026-11-04 | Fuera eslogan, texto de ayuda, beneficios y nombre final | Pedido del dueño: propósito y diseño mínimos. La ayuda "Toca varios títulos…" se sustituye por el "+" en cada precio. |
| 2026-11-04 | Fuera el mosaico "Pedir por WhatsApp" de la cabecera | Duplicaba la barra del pedido; el contacto general queda en "¿No ves tu juego?". Una acción por intención. |
| 2026-11-04 | Sin títulos "Estrenos" ni "Juegos disponibles" | El tamaño ya marca los destacados y todo lo que se ve está disponible. `estrenos` → `destacados`. |
| 2026-11-04 | ~~Consola solo como aviso cuando es Switch 2~~ → ~~secciones "Switch 2" / "Switch 1"~~ → **pestaña con logo en la portada** | Corrección del dueño: un mismo juego tiene versión de Switch 1 y de Switch 2, así que la consola debe verse siempre. No le gustaron los títulos de sección; de 3 propuestas (pestaña, franja de caja, logo directo) eligió la pestaña: se lee en cualquier portada, sin sombra, y el rojo separa Switch 2 de un vistazo. |
| 2026-11-04 | Logo de Switch desde Simple Icons (CC0); Switch 2 = mismo ícono + "2" | No hay archivo abierto del logo de Switch 2 y los sitios de Nintendo/Wikimedia no eran accesibles. Vive en `src/assets/switch.svg` para cambiarlo por el oficial sin tocar código. |
| 2026-11-04 | `aria-pressed` como único estado del pedido; tokens en `:root` | Una sola fuente de verdad para CSS, script y lector de pantalla; los componentes ya no dependen de estar dentro de `<main>`. |
| 2026-11-04 | Barra sin "N títulos"; "Vaciar" oculto ≤ 420 px | Los mosaicos marcados ya muestran qué se eligió; así cabe un total de 7 cifras a 320 px. |
| 2026-11-04 | Validar `productos.json` y `tienda.ts` al compilar; `tipo_producto` desconocido ya no cae en "Juego" | El dueño no es técnico: un error de tipeo (ej. `"Nintendo switch 2"`, `"DLC"`) publicaba el juego mal sin aviso. Mejor que el build falle con un mensaje claro. |
| 2026-11-04 | Pedido guardado en `sessionStorage` (no `localStorage`) | Basta para sobrevivir a la ida y vuelta a WhatsApp; no deja un pedido viejo marcado días después. |
| 2026-11-04 | Favicon generado desde `tienda.nombre` | Los de `public/` eran el logo de Astro; así se actualiza solo con el nombre real (D2) sin diseñar un archivo. No usa el logo de Nintendo (`diseno.md` §7). |
| 2026-11-04 | Cloudflare **Workers** con `wrangler.jsonc` de solo assets, y no Pages | El dueño creó el proyecto como Worker desde el panel (Cloudflare lo propone por defecto). Un archivo de 6 líneas lo deja funcionando sin rehacer el proyecto; es el mismo sitio estático, sin servidor. |
| 2026-11-04 | `"previews": {}` en `wrangler.jsonc` en vez de apagar las compilaciones de ramas | Una línea arregla el check rojo y deja una dirección de prueba por PR para ver los cambios antes de fusionar. |
| 2026-11-04 | `wrangler` sin fijar en `package.json` | Lo instala `npx` en cada despliegue; fijarlo agregaría cientos de paquetes a cada `npm ci` del CI. Si una versión nueva rompe el despliegue, fijarlo entonces. |
| 2026-11-04 | Fuente desde npm (Fontsource) con el proveedor local, no el de Google | El proveedor de Google, si no puede descargar, compila igual con otra fuente y sin avisar (pasó en el entorno de trabajo). Desde npm queda fijada en `package-lock.json` y Dependabot la actualiza. |
| 2026-11-04 | Imagen de vista previa sin texto, solo las 3 portadas destacadas | WhatsApp ya muestra título y descripción al lado; dibujar texto con `sharp` dependería de las fuentes instaladas en la máquina del build. Se regenera sola al cambiar los destacados. |
| 2026-11-04 | `og.jpg` en JPEG y no PNG | WhatsApp no muestra imágenes de vista previa de más de ~300 KB; en PNG pesaría varias veces más. |
| 2026-11-04 | `url` en `tienda.ts` (no en `astro.config.mjs`) y validada en la configuración | El dueño edita un solo archivo; Astro lee `site` antes que nada, así que el error claro tiene que salir ahí. |
| 2026-11-04 | CI con `npm run build` en cada PR y push a `main` | La validación del catálogo solo protege si alguien compila; el CI lo hace siempre. |
| 2026-11-04 | Dependabot semanal agrupado; versiones mayores aparte | Pocos PRs, y un salto mayor de Astro se revisa a propósito. Con el CI, cada actualización llega ya probada. |
| 2026-11-04 | ~~`.nvmrc` = `22`~~ → **`.nvmrc` = `22.23.4`** | Astro 7 exige Node ≥ 22.23.4 y la imagen de compilación de Cloudflare Pages trae por defecto un 22.x más viejo (22.16); con solo `22` no hay garantía de que elija uno suficiente. Subir a mano cuando Astro lo pida. |
| 2026-11-04 | README como guía del dueño | El de la plantilla no explicaba cómo cambiar precios o agregar juegos. |
| 2026-11-04 | `cooldown` de Dependabot (3 días; 7 en mayores) | Las versiones comprometidas en npm suelen retirarse en horas o días; las actualizaciones de seguridad no esperan. |
| 2026-11-04 | CI: cancelar solo en PR, `persist-credentials: false`, `workflow_dispatch` | En `main` cada fusión debe quedar con su build; el job no hace push, así que no necesita el token guardado. |
| 2026-11-04 | `.gitattributes` con `eol=lf` | Editar `productos.json` desde Windows no debe cambiar los finales de línea de todo el archivo. |
| 2026-11-04 | Hook de Claude Code que corre `npm run build` al editar el catálogo | La validación de `catalogo.ts` ya existe pero solo se veía en el CI; así el error aparece al editar. Un build completo (~5 s) en vez de un validador aparte: una sola fuente de reglas. |
| 2026-11-04 | Skills `/nuevo-producto` y `/cerrar-sesion` solo a pedido del usuario | Editan el catálogo y el spec; no deben dispararse sin que el usuario lo pida. |
| 2026-11-04 | Sin servidor MCP de documentación de Astro en el repo | Su host está bloqueado en el entorno en la nube; en el repo daría un error de conexión en cada sesión. Se agrega localmente con `claude mcp add`. |
| 2026-11-04 | `CLAUDE.md` importa `AGENTS.md` (`@AGENTS.md`) | Una sola copia de las reglas del flujo de trabajo; `CLAUDE.md` solo agrega lo que exige leer varios archivos (validación, contrato del pedido, publicación). |
| 2026-11-04 | Contorno de foco en `--tinta` y no en `currentColor` | Con texto blanco (mosaico elegido, "¿No ves tu juego?") el contorno quedaba blanco sobre el suelo gris: 1,21:1, invisible. En tinta da 15,4:1 en todo el tablero. |
| 2026-11-04 | Anuncio del total en un párrafo oculto fuera de la barra | Una región `aria-live` dentro de un elemento `hidden` no se anuncia al mostrarse; y el monto solo ("$ 559.800") no decía de qué era. Texto invisible: no rompe la regla de textos (`diseno.md` §5). Al recargar no se anuncia. |
| 2026-11-04 | `h1` "Códigos para Switch 1 y 2" | Ningún texto visible decía que se venden códigos digitales; cambiar una palabra lo dice sin agregar textos (F6). |
| 2026-11-04 | Escritorio: cabecera de 1 línea y destacados con alto según la pantalla | Con 304 px de cabecera y destacados de 2 filas, en escritorio solo se veía 1 precio de 24 al abrir. Se prefirió recortar más ancha la portada (hasta 2,63:1 a 768 px de alto) antes que poner el precio sobre la imagen (§3). |
| 2026-11-04 | Nombre del juego en 800 | 15 de 24 títulos cuestan $ 279.900 y 6 $ 239.900: el precio no distingue; el nombre sí. Peso que ya existía (sin tamaños nuevos). |
| 2026-11-04 | "↗" en mosaicos sin precio | "Consultar" sale a WhatsApp y los demás se suman al pedido; sin señal, el mismo gesto hacía dos cosas distintas. |
| 2026-11-04 | "¿No ves tu juego?" sigue cerrando la fila | Limitarlo a 4 columnas dejaría un hueco de 2 mosaicos con 21 juegos (§8). Su peso visual se acepta. |
| 2026-11-04 | ~~Un juego con versión para cada consola son dos mosaicos~~ → **un mosaico con un precio por versión** (`grupo`) | Pedido del dueño: muchos juegos tienen versión de Switch 1 y de Switch 2, más el paquete de mejora; con un mosaico por versión el catálogo crecería un 17 % solo con los juegos actuales que la tienen. De 3 ideas (un mosaico con 2–3 precios, selector de consola, mosaicos pegados) eligió la primera. |
| 2026-11-04 | Cada versión sigue siendo su propia entrada en `productos.json`, unidas por `grupo` | Cada cosa que se vende tiene su id, precio y mensaje de pedido; no se agrupan por nombre porque los títulos no coinciden ("… Nintendo Switch 2 Edition") y podría juntar juegos equivocados. |
| 2026-11-04 | Portada de la versión de Switch 2 en el mosaico con versiones | Elección del dueño: la caja de Switch 2 (franja roja) dice de un vistazo que hay versión nueva. Hasta que la agregue se usa la de Switch 1. |
| 2026-11-04 | Paquete de mejora con sello "Mejora a ⊞2" (único texto nuevo) | El dueño lo vende. Un logo no basta para decir "pasar de Switch 1 a Switch 2"; dos palabras sí. |
| 2026-11-04 | ~~Celular: juego con versiones a todo el ancho~~ → **mosaico normal + panel de versiones** | El sitio es sobre todo para celular: a todo el ancho la página crecía +31 % (3,4 → 4,4 pantallas) y crecería con cada juego con versiones. De 2 propuestas (mosaico compacto horizontal, −35 % de alto; mosaico normal + panel) el dueño eligió el panel: la página vuelve a medir como `main` y no crece. Cuesta un toque más, una vez por juego. |
| 2026-11-04 | "N versiones · desde $ …" con el precio del juego más barato (sin el paquete de mejora) | Sin las filas a la vista, el mosaico tiene que decir que hay varias opciones y cuánto cuesta entrar. La mejora no cuenta: solo sirve a quien ya tiene el juego, y "desde $ 39.900" engañaría. |
| 2026-11-04 | Las filas se **mueven** al panel (no se copian) | Siguen siendo los mismos botones: conservan `aria-pressed`, los eventos de `Pedido.astro` y `sessionStorage` sin duplicar estado. |
| 2026-11-04 | ~~Juego con versiones = ancho de 2 mosaicos (en escritorio, 4 columnas)~~ → **en escritorio también mosaico normal + panel** (ver abajo) | Sello + precio de 22 px + "+" piden ~180 px y un mosaico chico a 320 px deja 122 px. Desde 1100 px la portada va a la izquierda y el mosaico mide lo mismo que sus vecinos. |
| 2026-11-04 | Filas de versión: sello a la izquierda y precio alineado a la derecha junto al "+"; ~~portada 3:1 en celular~~ (con el panel, en celular la portada vuelve a 16:9) | Crítica de diseño: con el precio después del sello más ancho ("Mejora a ⊞2", 106 px) los precios empezaban a mitad del mosaico y el sello de Switch 1 flotaba solo; alineados a la derecha se comparan como en una lista. La portada a 3:1 baja el mosaico de 341 a 310 px a 390 px (3 versiones sueltas ocuparían ~290 px). |
| 2026-11-04 | Mario Wonder (Switch 1) a $ 239.900 | Nintendo Colombia lo bajó de $ 279.900 (precio regular, sin descuento); el dueño pidió seguir la referencia. |
| 2026-11-04 | Precios de Switch 2 y paquete de mejora tomados de `nintendo.com/es-co` | Mismo origen que los demás (referencia eShop Colombia, D5): los precios de Switch 1 de esa página coinciden con los del archivo. Se usó el precio regular (`discounted: false`). |
| 2026-11-04 | Portada del mosaico con versiones anclada abajo (`object-position: 50% 100%`) | Las cajas de Switch 2 Edition llevan la franja "Nintendo Switch 2 Edition" abajo; el recorte 3:1 centrado la cortaba. Desde 1100 px (portada a la izquierda) el recorte es por los lados y la franja o el logo pueden cortarse: la pestaña ⊞2 ya marca la versión. |
| 2026-11-04 | Campo opcional `imagen.recorte` en vez de un recorte fijo | La franja "Nintendo Switch 2 Edition" va abajo en Zelda y Wonder pero arriba en Animal Crossing; no hay un recorte que sirva para todas. Por defecto "abajo" (el caso común). |
| 2026-11-04 | ~~Alto mínimo de los destacados chicos con versiones en escritorio~~ (ya no aplica: van en el panel) | En horizontal miden menos y el destacado grande (que ocupa las 2 filas) se encogía hasta recortar el logo de Mario Kart World. |
| 2026-11-04 | Ancho de "¿No ves tu juego?" calculado simulando la retícula (`lib/reticula.ts`) | Con mosaicos de dos anchos, contar mosaicos ya no dice cuánto falta para cerrar la fila. |
| 2026-11-04 | Sin `flex-wrap` en el precio para WCAG 1.4.12 | Probado: a 320 px el "+" bajaba de línea siempre (+369 px de alto). Con espaciado aumentado el "+" se recorta, pero es decorativo: el precio sigue visible y el estado lo dan el color y `aria-pressed`. |
| 2026-11-04 | **Sin AVIF**: las portadas siguen solo en webp q78 | Medido en las 28 portadas a 640 px (SSIM en luminancia, 1 = idéntica): con la misma nitidez AVIF casi no ahorra (q60: 926 KB y 0,9805 contra webp q65: 968 KB y 0,9806, −4 %); igualar a webp q78 (0,9912) cuesta +14 % (q72). Los originales ya son webp con pérdida a 960 px, así que AVIF no tiene detalle que comprimir mejor. Además el build pasaba de ~5 s a 1 min 16 s. El "~18 %" anterior comparaba con el mismo número de calidad, que no significa lo mismo en los dos formatos. Revisar si el dueño entrega portadas sin pérdida y más grandes. |
| 2026-11-04 | `sizes` con el ancho exacto del mosaico y variantes cada 80–160 px | Casi todo el peso estaba en 23 mosaicos de ~181 px que en celulares de densidad 3 bajaban 640 px (necesitan 543). Con escalones más finos cada equipo baja la variante justa por encima de lo que necesita: −15 % a −46 % sin perder nitidez. Las fórmulas de `sizes` salen de la retícula (comentario en `Mosaico.astro`): si cambian márgenes, separación o columnas, actualizarlas. |
| 2026-11-04 | **Escritorio igual que celular:** juego con versiones del tamaño de un juego, versiones en el panel (centrado) | El dueño veía el escritorio asimétrico: mosaicos de 2 y 4 columnas, portadas recortadas en vertical, catálogo desordenado por `dense`. Con el panel todas las filas tienen 5 mosaicos iguales. Cuesta un clic más por juego con versiones, como en celular. |
| 2026-11-04 | Portadas originales de 1920×1080 (antes 960×540) | Con 960 px ninguna variante alcanzaba para el destacado grande ni para pantallas ×2: se veían borrosas. Son las mismas imágenes de `fuente_imagen`, sin recorte de Nintendo. El repo crece de 2,9 a 9 MB; el visitante solo baja la variante que necesita. |
| 2026-11-04 | Tablero de máx. 1440 px, centrado | Más ancho los mosaicos se agrandan sin sumar información y las portadas pierden nitidez. |
| 2026-11-04 | Precios del listado copiados a `productos.json` (no se cambió el archivo que lee la web) | `productos.json` sigue siendo la única fuente; el listado nuevo trae portadas de 960 y sin los datos de las 6 portadas agregadas. Si el dueño prefiere editar el listado nuevo, se puede apuntar `catalogo.ts` a él y borrar el otro. |
| 2026-11-04 | Campo `publicar` (por defecto true) | El listado lo trae: Ring Fit tiene precio pendiente y `publicar: false`. Ocultar sin borrar deja los datos listos para cuando haya precio. |
| 2026-11-04 | `recorte`: "izquierda" / "derecha" (7 % / 93 % horizontal) | El destacado grande en escritorio deja ver 72–85 % del ancho (es más alto que 16:9). El logo de Ocarina llega al 96,7 % del ancho y se cortaba con el centro; con 93 % queda entero a 1024, 1280, 1440 y 1920 px (medido), a cambio de recortar un poco la mochila de Link a 1024 y 1920. En celular no recorta los lados. |

## 9. Cómo verificar un cambio

1. `npm run build` termina sin errores (incluye la validación del catálogo).
2. `astro dev --background` y abrir `/` a 390 px
   y a 1440 px de ancho: sin scroll horizontal, títulos en ≤ 2 líneas, sin huecos raros en el tablero.
3. Tocar 2–3 títulos: la barra muestra cantidad y total correctos; el enlace `wa.me`
   contiene la lista y el total; "Vaciar" limpia todo.
4. Revisar contra las reglas de `docs/diseno.md` §6.
