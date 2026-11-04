# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Qué es

Catálogo de precios de una sola página (celular primero) para la tienda **SD Tech Import**: códigos
digitales de Nintendo Switch 1 y 2 en pesos colombianos. Sin carrito de pago, login ni base de datos:
el pedido se cierra por WhatsApp. Sitio estático en Astro 7, sin frameworks de UI ni Tailwind.
Todo (interfaz, código, comentarios, commits, docs) está en **español**; mantenlo así.

Fuente de verdad: `docs/spec.md` (requisitos F1–F6, fuera de alcance, decisiones D*, estado) y
`docs/diseno.md` (Diseño A · Tablero: tokens, retícula, tabla "No hacer" §6, lista visual §8).

## Comandos

| Comando | Para qué |
|---|---|
| `npm ci` | Instalar (Node 22.23.4 exacto, ver `.nvmrc`). En la nube lo hace el hook de inicio. |
| `npm run build` | Compila a `dist/` **y valida el catálogo**. |
| `astro dev --background` | Servidor de desarrollo en `http://localhost:4321` (`astro dev stop\|status\|logs`). |
| `npm run preview` | Sirve `dist/` tal como se publica. |

Hay pruebas con `npm test` (runner de Node), sin dependencias adicionales. No hay linter ni `astro check` (no está instalado `@astrojs/check`). El CI
(`.github/workflows/build.yml`) corre `npm ci`, `npm test` y `npm run build`.

## Arquitectura

**Flujo de datos:** `src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json` (lo edita el dueño)
+ `src/data/tienda.ts` (nombre, WhatsApp, `url`, 3 `destacados`, `mostrarDlcUpdates`) →
`src/lib/catalogo.ts` → `src/pages/index.astro`.

- **Validación al importar:** `catalogo.ts` revisa todas las filas al cargarse y lanza
  `Error("Revisa el catálogo:\n- …")`, lo que detiene el build. Si agregas un campo o una regla,
  hazlo ahí con un mensaje en español para alguien no técnico. `tienda.url` se valida aparte en
  `astro.config.mjs`, porque Astro lee `site` antes que todo.
- **Traducción de campos:** las filas del JSON (`titulo`, `plataforma`, `tipo_producto`,
  `precio_venta_cop ?? precio_referencia_eshop_colombia_cop`) se convierten al tipo `Producto`
  (las filas con `publicar: false` se validan pero no salen en la página)
  (`nombre`, `consola`, `tipo`, `precio`). Las filas con el mismo `grupo` (versión de Switch 1, de
  Switch 2 y `paquete_mejora`) se juntan en una `Ficha` = un mosaico. Los componentes solo ven `Ficha`/`Producto`. Los demás campos del
  JSON se ignoran y no se tocan. `precio: null` → "Consultar" y no entra al pedido.
- **Pedido (`components/Pedido.astro`):** `item(p)` devuelve un `href` `wa.me` y atributos
  `data-item/nombre/precio/detalle`. El script vuelve seleccionable todo lo que tenga `data-item`.
  `aria-pressed` es el **único** estado (el CSS de `Mosaico.astro` dibuja "+"/"✓" a partir de él).
  La selección se guarda en `sessionStorage['pedido']`, envuelta en try/catch. Sin JavaScript,
  cada mosaico sigue siendo un enlace de WhatsApp (F3): no rompas esa mejora progresiva.
  En celular, las filas de un juego con versiones se **mueven** (no se copian) al `<dialog>` de
  `PanelVersiones.astro` y vuelven al cerrar; sin JavaScript, un `<noscript>` en `index.astro` las muestra.
- **Retícula:** grid de 6/10 columnas con `grid-auto-flow: dense`. El mosaico "¿No ves tu juego?"
  calcula su ancho con `lib/reticula.ts`, que simula `dense` con los anchos de cada mosaico (los juegos
  con versiones miden 2): si cambias tamaños de mosaico, actualiza las piezas en `index.astro`.
- **Endpoints estáticos:** `pages/og.jpg.ts` compone con `sharp` la imagen para compartir a partir
  de los 3 destacados, que debe quedar en menos de ~300 KB para WhatsApp. `pages/favicon.svg.ts`
  usa la inicial de `tienda.nombre`. Las etiquetas `og:*`/`canonical` de `Layout.astro` solo salen
  si `tienda.url` está lleno.
- **Estilos:** CSS con alcance por componente. Los tokens de color viven en `:root` de
  `layouts/Layout.astro`: no agregues colores, sombras, bordes ni tamaños de letra fuera de
  `docs/diseno.md` §2. La fuente (Schibsted Grotesk 500/800) se sirve localmente mediante la API
  `fonts` de `astro.config.mjs`, sin Google.
- **Portadas:** `import.meta.glob` sobre `imagenes/*.{webp,jpg,jpeg,png}`. Astro genera las variantes
  webp de 320 a 1920 px (originales de 1920×1080). Agregar un juego es solo datos + portada; no hay que tocar el diseño.

## Publicación

Cloudflare Workers (Worker `sdtechimport`): cada push a `main` corre `npm run build` +
`npx wrangler deploy` y publica `dist/` (https://sdtechimport.madaeauchija.workers.dev). Los PR
corren `wrangler preview`, que necesita `"previews": {}` en `wrangler.jsonc`. No agregues el
adaptador de servidor de Astro: el sitio es estático a propósito.

## Automatizaciones de Claude Code (`.claude/`)

- Al editar `productos.json`, `tienda.ts`, `catalogo.ts` o `astro.config.mjs`, un hook corre el build
  (~5 s) y devuelve los errores de validación: corrígelos antes de seguir.
- Un hook bloquea editar `package-lock.json`, `dist/`, `.astro/` y `node_modules/`.
- `/nuevo-producto` y `/cerrar-sesion` (actualiza el spec) solo los invoca el usuario. Usa el
  subagente `revisor-diseno` después de cambios visuales.

## Verificar un cambio

`npm run build`. Si es visual, revisa a 320, 390 y 1440 px: sin scroll horizontal, sin huecos en el
tablero, y al elegir 2 títulos el total correcto en la barra (Chromium y Playwright ya están
instalados en la nube). La lista completa está en `docs/diseno.md` §8 y en la plantilla de PR.
