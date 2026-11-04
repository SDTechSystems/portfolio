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
| R5 | Moneda | Pesos ($). **País sin confirmar** → hoy se usa formato `es-MX` / `MXN`. |
| R6 | Tamaño | Menos de 30 títulos → no hace falta buscador ni paginación. |
| R7 | Portadas | Las sube el dueño a `public/portadas/`. |
| R8 | Marca | Por ahora marcadores: "Tu Tienda" y un número de ejemplo. |
| R9 | Diseño | Elegido: **A · Tablero** (ver `docs/diseno.md`). |

### Funcionalidades

- **F1. Secciones:** Estrenos (`estreno: true`), Juegos disponibles (`tipo: juego`),
  DLC y updates (`tipo: dlc` y `update`).
- **F2. Arma tu pedido:** tocar un título lo marca y lo suma a una barra fija inferior
  ("2 títulos · $1,648 · Vaciar · Pedir por WhatsApp"). El botón envía un solo mensaje:
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
- **F5. Sin portada:** si un título no tiene `imagen`, se muestra un bloque de color plano
  (`color`) con el nombre.

### Fuera de alcance (no hacer sin que el dueño lo pida)

Pagos en línea, cuentas de usuario, inventario/stock en tiempo real, panel de
administración, buscador, varias páginas, multi-idioma.

## 4. Arquitectura

- **Stack:** Astro 7 (`astro@^7.4.5`), Node ≥ 22.23.4, salida estática (`npm run build` → `dist/`).
  Sin frameworks de UI ni Tailwind: CSS con alcance por componente.
- **Dev server:** `astro dev --background` (ver `AGENTS.md`); `astro dev stop|status|logs`.

```
src/
  data/
    tienda.ts         ← nombre, WhatsApp, moneda/locale, beneficios
    catalogo.json     ← la lista de títulos (lo único que edita el dueño a diario)
  lib/catalogo.ts     ← tipos, filtros (estrenos, porTipo), formato de precio, enlaces wa.me, item()
  components/
    Portada.astro     ← imagen o bloque de color sin imagen
    Pedido.astro      ← barra "Tu pedido" + script de selección (compartido)
  layouts/Layout.astro← <head>, fuente de Google Fonts, reset global
  pages/
    index.astro       ← HOY: selector temporal de diseños (ver tarea T1)
    disenos/tablero.astro  ← DISEÑO ELEGIDO (A)
    disenos/poster.astro   ← descartado (B), borrar en T1
    disenos/codigos.astro  ← descartado (C), borrar en T1
public/portadas/      ← imágenes de portada (jpg/webp)
docs/                 ← este spec y las directrices de diseño
```

### Modelo de datos (`src/data/catalogo.json`)

```jsonc
{
  "id": "mario-wonder",          // único, kebab-case; se usa también como nombre de archivo de portada
  "nombre": "Super Mario Bros. Wonder",
  "precio": 999,                 // número entero en la moneda de tienda.ts, sin símbolo
  "tipo": "juego",               // "juego" | "dlc" | "update"
  "consolas": ["switch1", "switch2"], // uno o ambos
  "estreno": true,               // opcional; los 3 primeros estrenos llenan el bloque superior
  "imagen": "/portadas/mario-wonder.jpg", // opcional
  "color": "#d93a2b"             // opcional; fondo cuando no hay imagen
}
```

Reglas: el **primer** estreno es la portada grande; los dos siguientes, las chicas. El
diseño está pensado para **exactamente 3 estrenos**: con más, los extra se muestran
como mosaicos medianos debajo y el bloque pierde su forma (revisar que se vea bien).

### Contrato de `Pedido.astro`

Cualquier elemento con los atributos que devuelve `item(p)` (`href`, `data-item`,
`data-nombre`, `data-precio`, `data-detalle`) se vuelve seleccionable. Al seleccionarlo
recibe la clase `.en-pedido` y `aria-pressed="true"`. La barra toma colores de las variables
CSS `--pedido-bg`, `--pedido-ink`, `--pedido-accent` y debe ir **dentro** del `<main>` del
diseño para heredarlas.

## 5. Estado (actualizar al cerrar cada sesión)

**Última actualización:** 2026-11-04, rama `claude/keen-ramanujan-5bab3k`.

Hecho:
- [x] Entrevista y requisitos (sección 3).
- [x] Datos de ejemplo: 23 títulos (17 juegos, 4 DLC, 2 updates), precios **inventados**.
- [x] Diseño A · Tablero funcionando en `/disenos/tablero` (celular y escritorio).
- [x] Barra "Arma tu pedido" probada (sumas y mensaje correctos).
- [x] Vista previa interactiva de A/B/C publicada como artifact privado (solo revisión).

Portadas actuales: **recortes de baja resolución** del póster de referencia, solo para
maquetar. Los 2 updates no tienen portada.

## 6. Tareas pendientes (en orden)

- [ ] **T1. Consolidar el diseño A.** Mover `disenos/tablero.astro` a `src/pages/index.astro`,
      borrar `disenos/poster.astro`, `disenos/codigos.astro` y el selector temporal.
      Ajustar imports relativos. Verificar con `npm run build`.
- [ ] **T2. Datos reales de la tienda** en `tienda.ts`: nombre, WhatsApp (solo dígitos con
      código de país), país → `locale` y `moneda` (ej. `es-CO`/`COP`, `es-CL`/`CLP`,
      `es-AR`/`ARS`, `es-MX`/`MXN`).
- [ ] **T3. Catálogo real:** reemplazar `catalogo.json` con los títulos y precios del dueño.
- [ ] **T4. Portadas reales** en buena resolución (16:9, ~800 px de ancho, < 150 KB, webp o jpg),
      nombradas `<id>.jpg`.
- [ ] **T5. Metadatos para compartir:** `og:title`, `og:description`, `og:image` (imagen
      1200×630 del tablero) para que el enlace se vea bien en WhatsApp.
- [ ] **T6. Publicación:** elegir hosting estático (Netlify, Vercel, Cloudflare Pages o
      GitHub Pages) y generar el QR del enlace final.
- [ ] **T7. Auditoría:** accesibilidad (contraste, foco, `aria-pressed`), peso de imágenes,
      y prueba en un celular real con WhatsApp instalado.

## 7. Decisiones abiertas (preguntar al dueño)

| # | Pregunta | Supuesto actual |
|---|---|---|
| D1 | ¿País de venta? (formato `$1,299` vs `$1.299`) | México (`es-MX`). |
| D2 | Nombre de la tienda, logo y número de WhatsApp | "Tu Tienda", `5215512345678`. |
| D3 | ¿Volver a poner las píldoras rojas "NUEVO" de la referencia? | No (ver `diseno.md` §6). Se muestran como sección "Estrenos". |
| D4 | ¿Dónde se publicará? | Sin definir. |

## 8. Registro de decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-11-04 | Astro estático + JSON en el repo | El dueño edita un archivo; sin costo ni servidor. |
| 2026-11-04 | Primera ronda (Bento, Vitrina oscura, Lista) **rechazada** | Muy genérica, poco fiel a la referencia, portadas falsas. |
| 2026-11-04 | Segunda ronda guiada por [taste-skill](https://github.com/Leonxlnx/taste-skill): A Tablero, B Póster, C Códigos | Reglas anti-"diseño genérico" + portadas reales. Sus scripts no se ejecutaron (bloqueados por permisos); se usó como lectura. |
| 2026-11-04 | **Elegido A · Tablero** | Fiel a la estructura del póster original. |
| 2026-11-04 | Pedido múltiple con un solo WhatsApp | Un cliente suele comprar juego + DLC; un mensaje con total reduce idas y vueltas. |

## 9. Cómo verificar un cambio

1. `npm run build` termina sin errores.
2. `astro dev --background` y abrir `/` (o `/disenos/tablero` hasta completar T1) a 390 px
   y a 1440 px de ancho: sin scroll horizontal, títulos en ≤ 2 líneas, sin huecos raros en el tablero.
3. Tocar 2–3 títulos: la barra muestra cantidad y total correctos; el enlace `wa.me`
   contiene la lista y el total; "Vaciar" limpia todo.
4. Revisar contra las reglas de `docs/diseno.md` §6.
