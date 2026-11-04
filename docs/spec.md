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

- **F1. Orden:** 3 destacados en grande (`tienda.ts → destacados`), luego secciones
  **"Switch 2"**, **"Switch 1"** y "DLC y updates" (oculta hoy). Una sección sin productos no
  se muestra. Un juego con versión para cada consola son dos entradas en `productos.json`
  y aparece en las dos secciones, cada una con su precio.
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
- **F6. Sin textos secundarios:** ni eslogan, ni ayuda, ni beneficios. La **consola siempre
  se distingue**: la dice el título de la sección o, en los destacados (que mezclan
  consolas) y en "DLC y updates", la línea bajo el nombre. Esa línea suma la nota si hay
  ("Switch 1 · Necesita Ring-Con").

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
    tienda.ts         ← nombre, WhatsApp, moneda/locale, ids destacados, mostrarDlcUpdates
  assets/Catalogo_Nintendo_Switch_Colombia/
    productos.json    ← la lista de títulos (lo único que edita el dueño a diario)
    imagenes/<id>.webp← portadas 16:9 (Astro genera 320/480/640/960 px en webp)
  lib/catalogo.ts     ← lee productos.json → destacados, secciones; precio(), whatsapp(), item()
  components/
    Mosaico.astro     ← un producto: portada optimizada, nombre, consola/nota, precio con "+"/"✓"
    Pedido.astro      ← barra del pedido + script de selección
  layouts/Layout.astro← <head>, fuente, tokens de color en :root, reset global
  pages/
    index.astro       ← la página: diseño A · Tablero
docs/                 ← este spec y las directrices de diseño
```

### Modelo de datos (`src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json`)

Cada entrada de `productos` (campos que usa la web; el resto se ignora):

```jsonc
{
  "id": "mario-kart-world",          // único, kebab-case
  "titulo": "Mario Kart World",
  "plataforma": "Nintendo Switch 2", // "Nintendo Switch" → "Switch 1"; "Nintendo Switch 2" → "Switch 2"
  "tipo_producto": "juego_digital",  // "dlc" | "update" | otro → Juego. "juego_con_accesorios" añade "Necesita Ring-Con"
  "precio_venta_cop": 299900,        // OPCIONAL: tu precio. Si falta, se usa el de referencia
  "precio_referencia_eshop_colombia_cop": 319900, // null → muestra "Consultar" y no entra al pedido
  "imagen": { "ruta": "imagenes/mario-kart-world.webp" } // opcional; sin imagen: bloque de color
}
```

Orden: el del archivo (por `puesto_ranking`). Los **destacados** se eligen en `tienda.ts → destacados`
(lista de ids, en orden: el primero es la portada grande). El diseño está pensado para
**exactamente 3 destacados**. La sección "DLC y updates" está **oculta** con
`tienda.ts → mostrarDlcUpdates: false`; con `true` aparece si hay al menos un DLC o update
(`tipo_producto: "dlc"` o `"update"`). Mientras está oculta, esos productos no se muestran.

### Contrato de `Pedido.astro`

Cualquier elemento con los atributos que devuelve `item(p)` (`href`, `data-item`,
`data-nombre`, `data-precio`, `data-detalle`) se vuelve seleccionable: el script le pone
`role="button"` y `aria-pressed`. **`aria-pressed` es el único estado** (no hay clases ni
`Set` aparte): el CSS de `Mosaico.astro` dibuja "+" o "✓" a partir de él, así que sin
JavaScript no aparece ningún "+" y el enlace `wa.me` funciona solo. Los colores salen de los
tokens globales de `Layout.astro`.

## 5. Estado (actualizar al cerrar cada sesión)

**Última actualización:** 2026-11-04 (simplificación), rama `claude/keen-ramanujan-5bab3k` (incluye `main` con los assets).

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
- [x] Secciones por consola. Probado con 3 "Switch 2 Edition" de prueba (no guardadas): aparecen
      en "Switch 2" junto a su versión de Switch 1, sin huecos, total y mensaje correctos.

Pendiente de datos del dueño: número de WhatsApp real (hoy `573001234567`), nombre de la tienda,
y confirmar si los precios mostrados (referencia eShop) son los de venta (D5).

## 6. Tareas pendientes (en orden)

- [x] **T1. Consolidar el diseño A.**
- [~] **T2. Datos reales de la tienda:** país/moneda listos (Colombia). Faltan nombre y WhatsApp (D2).
- [x] **T3. Catálogo real** (con la salvedad de precios, D5).
- [x] **T4. Portadas reales.**
- [ ] **T4b. Contenido de DLC y updates:** agregarlos a `productos.json` (con portada) y
      poner `mostrarDlcUpdates: true`. Revisar que la fila final no deje huecos.
- [ ] **T5. Metadatos para compartir:** `og:title`, `og:description`, `og:image` (imagen
      1200×630 del tablero). Necesita la URL final (D4) para la ruta absoluta de la imagen.
- [ ] **T6. Publicación:** elegir hosting estático (Netlify, Vercel, Cloudflare Pages o
      GitHub Pages) y generar el QR del enlace final.
- [ ] **T7. Auditoría:** accesibilidad (contraste, foco, `aria-pressed`), peso de imágenes,
      y prueba en un celular real con WhatsApp instalado.

## 7. Decisiones abiertas (preguntar al dueño)

| # | Pregunta | Supuesto actual |
|---|---|---|
| D1 | ~~¿País de venta?~~ | **Resuelta:** Colombia (`es-CO`, `$ 239.900`). |
| D2 | Nombre de la tienda, logo y número de WhatsApp | "Tu Tienda", `573001234567` (falso). |
| D3 | ¿Volver a poner las píldoras rojas "NUEVO" de la referencia? | No (ver `diseno.md` §6). Los destacados se distinguen por tamaño. |
| D4 | ¿Dónde se publicará? | Sin definir. |
| D5 | ¿Los precios de venta son los de referencia de la eShop? `productos.json` dice que **no** representan tu precio. | Se muestran los de referencia. Para usar el tuyo, añade `"precio_venta_cop"` a cada producto. |
| D6 | ¿Marcar los juegos de Switch 1 como "Switch 1 y 2"? (casi todos corren en Switch 2) | No: van en la sección "Switch 1", tal como dice `plataforma`. |
| D7 | Ring Fit Adventure no tiene precio digital y necesita el accesorio Ring-Con. ¿Se vende? | Se muestra con "Consultar" y abre WhatsApp para preguntar; no entra al pedido. |
| D8 | ¿Qué títulos van destacados? | Los 3 más recientes: Mario Kart World (2025), Super Mario Bros. Wonder (2023), Zelda: Tears of the Kingdom (2023). |

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
| 2026-11-04 | ~~Consola solo como aviso cuando es Switch 2~~ → **secciones "Switch 2" / "Switch 1"** | Corrección del dueño: un mismo juego tiene versión de Switch 1 y de Switch 2, así que la consola debe distinguirse siempre. Agrupar la dice una vez por sección en vez de 24 veces; solo los destacados (mezclados) la escriben en el mosaico. |
| 2026-11-04 | `aria-pressed` como único estado del pedido; tokens en `:root` | Una sola fuente de verdad para CSS, script y lector de pantalla; los componentes ya no dependen de estar dentro de `<main>`. |
| 2026-11-04 | Barra sin "N títulos"; "Vaciar" oculto ≤ 420 px | Los mosaicos marcados ya muestran qué se eligió; así cabe un total de 7 cifras a 320 px. |

## 9. Cómo verificar un cambio

1. `npm run build` termina sin errores.
2. `astro dev --background` y abrir `/` a 390 px
   y a 1440 px de ancho: sin scroll horizontal, títulos en ≤ 2 líneas, sin huecos raros en el tablero.
3. Tocar 2–3 títulos: la barra muestra cantidad y total correctos; el enlace `wa.me`
   contiene la lista y el total; "Vaciar" limpia todo.
4. Revisar contra las reglas de `docs/diseno.md` §6.
