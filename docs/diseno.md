# Diseño A · Tablero: directrices

> Diseño elegido por el dueño. Archivo fuente: `src/pages/disenos/tablero.astro`
> (pasará a `src/pages/index.astro`, ver tarea T1 en `docs/spec.md`).
> Leer completo antes de cambiar o agregar cualquier cosa visual.

## 1. Idea

**La página es un tablero de mosaicos planos encajados borde a borde**, como el póster
original de la tienda, pero ordenado. Cada mosaico es **una sola cosa**: el nombre de la
tienda, el botón de pedir, un estreno, un juego con su precio, un beneficio. No hay "hero"
con bandas: el tablero empieza arriba y termina en el nombre de la tienda en grande.

Dirección de arte tomada de taste-skill: `dense-tiles`. Las portadas de los juegos son el
contenido visual; el diseño no agrega adornos alrededor.

## 2. Tokens

Definidos en `.tablero` (no en `:root`). Usar **solo** estos.

| Token | Valor | Uso |
|---|---|---|
| `--suelo` | `#e9e9ec` | Fondo de la página (entre mosaicos). |
| `--mosaico` | `#ffffff` | Fondo de cada mosaico normal. |
| `--tinta` | `#121214` | Texto; fondo del botón "Pedir", del texto de ayuda y de mosaicos seleccionados. |
| `--suave` | `#5b5b63` | Texto secundario (consola). Nada más. |
| `--rojo` | `#e60012` | Acento: encabezado, "¿No ves tu juego?", nombre final, ✓ de seleccionado, botón de la barra. |

Proporción: el suelo gris claro domina, los mosaicos blancos llevan el contenido, el rojo
aparece en **4 lugares fijos** (encabezado, mosaico "¿No ves tu juego?", cierre con el
nombre, acción del pedido). No agregar rojo en otros sitios.

**Tipografía:** una sola familia, **Schibsted Grotesk**, pesos **500** y **800**
(cargada en `Layout.astro` por defecto). Respaldo: `system-ui, sans-serif`.

| Rol | Tamaño | Peso | Otros |
|---|---|---|---|
| Título `h1` | `clamp(38px, 11vw, 88px)` | 800 | interlineado .95, tracking -0.035em, máx. 12ch → siempre 2 líneas |
| Títulos de sección `h2` | `clamp(26px, 6.4vw, 44px)` | 800 | tracking -0.03em |
| Precio | 22px (estreno grande: 30px) | 800 | tracking -0.02em, **sin** `tabular-nums` (deja huecos en la coma) |
| Nombre del juego | 14px (grande: 18px/800) | 500 | máximo 2 líneas con `line-clamp` |
| Consola / tipo | 13px | 500 | color `--suave` |
| Texto de apoyo | 17–20px | 500 | interlineado 1.4–1.45 |
| Nombre final | `clamp(56px, 19vw, 200px)` | 800 | tracking -0.05em, interlineado .85 |

## 3. Retícula

| | Celular (< 760px) | Escritorio (≥ 760px) |
|---|---|---|
| Columnas | 6 | 10 |
| Separación entre mosaicos | 8px | 8px |
| Margen exterior | 10px | 12px |
| Radio de esquina | 8px en todos los mosaicos (único valor) | igual |
| `grid-auto-flow` | `dense` (rellena huecos) | igual |

Tamaños de mosaico (clases) y cuántas columnas ocupan:

| Mosaico | Clase | Celular | Escritorio |
|---|---|---|---|
| Encabezado (tienda + h1 + apoyo) | `.t.nombre` | 6 | 7 |
| Pedir por WhatsApp | `.t.accion` | 6 | 3 |
| Título de sección | `.t.titulo` | 6 (sin fondo) | 10 |
| Estreno grande | `.t.juego.grande` | 6, imagen 2:1 | 6 × 2 filas, imagen llena el alto |
| Estrenos chicos | `.t.juego.medio` | 3 | 4, imagen 2.1:1 |
| Juego / DLC / update | `.t.juego` | 3 (2 por fila) | 2 (5 por fila) |
| ¿No ves tu juego? | `.t.mas` | 3 | 2 |
| Cierre | `footer.t.cierre` | ayuda 100%, 3 beneficios, nombre 100% | ayuda 4fr + 3 beneficios 2fr, nombre 100% |

Estructura de un mosaico de juego (no cambiar el orden):

```
┌──────────────────────┐
│ portada 16:9         │  .img  (object-fit: cover)
├──────────────────────┤
│ Nombre (2 líneas)    │  .n
│ Switch 1 y 2         │  .c   (para DLC/update: "DLC · Switch 2")
│ $1,299               │  strong (abajo del todo, margin-top: auto)
└──────────────────────┘
```

El precio va **debajo** de la portada, nunca encima de la imagen.

## 4. Estados e interacción

- **Seleccionado** (`.en-pedido`): mosaico en `--tinta`, texto blanco, consola en `#b9b9c2`,
  y un ✓ rojo después del precio. Es la única señal: no agregar bordes ni sombras.
- **Al tocar:** `transform: scale(.98)` (150 ms). La flecha de "Pedir" se mueve 4px al pasar el mouse.
- **Barra de pedido** (`Pedido.astro`): píldora negra fija abajo, con "N títulos" en una
  línea y el total en otra, "Vaciar" y el botón rojo "Pedir por WhatsApp". Es el **único**
  elemento con sombra, porque flota sobre la página. Aparece con una subida de 250 ms.
- `prefers-reduced-motion`: se quitan transiciones y la animación de la barra.
- Foco visible: `outline: 3px solid currentColor` (global en `Layout.astro`).

## 5. Textos

- Título: **"Juegos para Switch 1 y 2"**. Apoyo: *"Códigos oficiales de juegos, DLC y
  updates. Lo activas en tu propia cuenta."*
- Secciones: "Estrenos", "Juegos disponibles", "DLC y updates".
- Ayuda: *"Toca varios títulos para armar tu pedido y te enviamos el total por WhatsApp."*
- Beneficios (de `tienda.beneficios`): "Código oficial", "Actívalo en tu propia cuenta",
  "Sin riesgo de baneos".
- Tono: tuteo, frases cortas, español neutro latinoamericano. Botones que dicen lo que
  hacen ("Pedir por WhatsApp", "Vaciar"). Nada de "Descubre", "Increíble", emojis.

## 6. Reglas (adaptadas de taste-skill; obligatorias)

| No hacer | En su lugar |
|---|---|
| Degradados (fondos, botones, texto) | Colores planos de los tokens o la portada. |
| Sombras en elementos quietos | Cambio de tono entre suelo y mosaico. La única sombra es la barra de pedido. |
| Bordes finos o líneas divisorias de 1px | Separación de 8px del tablero. |
| Píldoras/etiquetas sobre títulos ("NUEVO", "HOT", "-20%") | Decirlo en el título de la sección ("Estrenos"). *Decisión abierta D3 en el spec.* |
| Letras chiquitas en MAYÚSCULAS con espaciado | Texto normal, legible, en minúsculas con mayúscula inicial. |
| Monospace, numeración 01/02/03 | Orden por posición y tamaño. |
| Más de una familia tipográfica, o tamaños intermedios nuevos | La tabla del §2. |
| Emojis, íconos decorativos, formas de relleno | Una portada real o nada. |
| Títulos de más de 2 líneas | Recortar palabras; luego ensanchar; el tamaño, al final. |
| Una palabra del título con otro color o cursiva | Un color, un peso. |
| Mosaicos vacíos o de relleno | Cada mosaico tiene contenido real; si sobra hueco, lo cubre `grid-auto-flow: dense` o un mosaico "¿No ves tu juego?". |

## 7. Cómo extender sin romper el diseño

- **Agregar un juego:** solo una entrada en `catalogo.json` y su portada en
  `public/portadas/<id>.jpg`. No tocar el diseño.
- **Nueva sección** (ej. "Tarjetas eShop"): un `<h2 class="t titulo">` y mosaicos
  `.t.juego` con `{...item(p)}`. Terminar con un mosaico `.t.mas` si la última fila queda incompleta.
- **Un nuevo tipo de mosaico:** usar uno de los tamaños existentes (2/3/4/6/10 columnas),
  fondo de un token, radio de 8px, texto alineado arriba a la izquierda con 16–22px de
  relleno. Nunca centrado ni con borde.
- **Logo de la tienda:** va dentro del mosaico `.nombre`, en el lugar de `.marca`, blanco
  sobre rojo, alto máx. 40px. No usar el logo de Nintendo.
- **Ofertas** (si el dueño las pide): precio anterior tachado en `--suave` a 14px junto
  al precio; sin píldora de "%".

## 8. Lista de revisión visual (antes de cada push)

- [ ] 390px y 1440px: sin scroll horizontal; márgenes iguales a ambos lados.
- [ ] `h1` y cada `h2` en ≤ 2 líneas a todo ancho.
- [ ] Ninguna fila del tablero con un hueco mayor a un mosaico.
- [ ] Todos los precios visibles y sin cortar; nombres largos cortados a 2 líneas con "…".
- [ ] Seleccionar 2 títulos: se ven en negro con ✓ y la barra muestra el total correcto.
- [ ] Contraste: blanco sobre `--rojo` (4.8:1), `--suave` sobre blanco (6.7:1) y `#b9b9c2` sobre `--tinta` (9.6:1) cumplen AA.
- [ ] Ningún elemento de la tabla "No hacer" del §6.
