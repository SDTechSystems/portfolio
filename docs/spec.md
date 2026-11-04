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
    tienda.ts         ← nombre, WhatsApp, moneda/locale, beneficios, ids de "Estrenos"
  assets/Catalogo_Nintendo_Switch_Colombia/
    productos.json    ← la lista de títulos (lo único que edita el dueño a diario)
    imagenes/<id>.webp← portadas 16:9 (Astro genera 320/480/640/960 px en webp)
  lib/catalogo.ts     ← lee productos.json, tipos, filtros, formato de precio, enlaces wa.me, item()
  components/
    Portada.astro     ← <Image> optimizada o bloque de color sin imagen
    Pedido.astro      ← barra "Tu pedido" + script de selección (compartido)
  layouts/Layout.astro← <head>, fuente de Google Fonts, reset global
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

Orden: el del archivo (por `puesto_ranking`). **Estrenos** se eligen en `tienda.ts → estrenos`
(lista de ids, en orden: el primero es la portada grande). El diseño está pensado para
**exactamente 3 estrenos**. La sección "DLC y updates" solo aparece si hay alguno.

### Contrato de `Pedido.astro`

Cualquier elemento con los atributos que devuelve `item(p)` (`href`, `data-item`,
`data-nombre`, `data-precio`, `data-detalle`) se vuelve seleccionable. Al seleccionarlo
recibe la clase `.en-pedido` y `aria-pressed="true"`. La barra toma colores de las variables
CSS `--pedido-bg`, `--pedido-ink`, `--pedido-accent` y debe ir **dentro** del `<main>` del
diseño para heredarlas.

## 5. Estado (actualizar al cerrar cada sesión)

**Última actualización:** 2026-11-04, rama `claude/keen-ramanujan-5bab3k` (incluye `main` con los assets).

Hecho:
- [x] Entrevista y requisitos (sección 3).
- [x] Diseño A · Tablero como página principal `/` (celular y escritorio). Diseños B y C y selector borrados.
- [x] Catálogo real de Colombia: 24 juegos de `productos.json` (23 Switch 1, 1 Switch 2), sin DLC ni updates.
- [x] Portadas reales optimizadas por Astro (de 70–175 KB a 12–130 KB por variante, webp).
- [x] Tienda en `es-CO` / `COP`. Barra "Arma tu pedido" probada: 3 títulos → `$ 799.700` correcto; "Vaciar" limpia.
- [x] Verificado a 390 px y 1440 px: sin scroll horizontal, sin huecos en filas, 24/24 imágenes cargan.

Pendiente de datos del dueño: número de WhatsApp real (hoy `573001234567`), nombre de la tienda,
y confirmar si los precios mostrados (referencia eShop) son los de venta (D5).

## 6. Tareas pendientes (en orden)

- [x] **T1. Consolidar el diseño A.**
- [~] **T2. Datos reales de la tienda:** país/moneda listos (Colombia). Faltan nombre y WhatsApp (D2).
- [x] **T3. Catálogo real** (con la salvedad de precios, D5).
- [x] **T4. Portadas reales.**
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
| D3 | ¿Volver a poner las píldoras rojas "NUEVO" de la referencia? | No (ver `diseno.md` §6). Se muestran como sección "Estrenos". |
| D4 | ¿Dónde se publicará? | Sin definir. |
| D5 | ¿Los precios de venta son los de referencia de la eShop? `productos.json` dice que **no** representan tu precio. | Se muestran los de referencia. Para usar el tuyo, añade `"precio_venta_cop"` a cada producto. |
| D6 | ¿Marcar los juegos de Switch 1 como "Switch 1 y 2"? (casi todos corren en Switch 2) | Solo "Switch 1", tal como dice `plataforma`. |
| D7 | Ring Fit Adventure no tiene precio digital y necesita el accesorio Ring-Con. ¿Se vende? | Se muestra con "Consultar" y abre WhatsApp para preguntar; no entra al pedido. |
| D8 | ¿Qué títulos van en "Estrenos"? | Los 3 más recientes: Mario Kart World (2025), Super Mario Bros. Wonder (2023), Zelda: Tears of the Kingdom (2023). |

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
| 2026-11-04 | `alt=""` en portadas | El nombre ya está escrito en el mosaico; evita que el lector de pantalla lo lea dos veces. |

## 9. Cómo verificar un cambio

1. `npm run build` termina sin errores.
2. `astro dev --background` y abrir `/` a 390 px
   y a 1440 px de ancho: sin scroll horizontal, títulos en ≤ 2 líneas, sin huecos raros en el tablero.
3. Tocar 2–3 títulos: la barra muestra cantidad y total correctos; el enlace `wa.me`
   contiene la lista y el total; "Vaciar" limpia todo.
4. Revisar contra las reglas de `docs/diseno.md` §6.
