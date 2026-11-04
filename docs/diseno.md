# Diseño A · Tablero: directrices

> Diseño elegido por el dueño. Archivos: `src/pages/index.astro` (tablero) y `src/components/Mosaico.astro` (producto).
> Leer completo antes de cambiar o agregar cualquier cosa visual.

## 1. Idea

**La página es un tablero de mosaicos planos encajados borde a borde**, como el póster
original de la tienda, pero ordenado. Cada mosaico es **una sola cosa**: el nombre de la
tienda o un juego con su precio. El tablero empieza en la cabecera roja y termina en
"¿No ves tu juego?".

**Sin texto que explique la pantalla.** Nada de eslóganes, ayudas, beneficios ni etiquetas
repetidas. Si algo necesita una frase para entenderse, se cambia el diseño (ej.: el "+" en
cada precio sustituye a "Toca varios títulos para armar tu pedido").

Dirección de arte tomada de taste-skill: `dense-tiles`. Las portadas de los juegos son el
contenido visual; el diseño no agrega adornos alrededor.

## 2. Tokens

Definidos en `:root` (`Layout.astro`). Usar **solo** estos.

| Token | Valor | Uso |
|---|---|---|
| `--suelo` | `#e9e9ec` | Fondo de la página (entre mosaicos). |
| `--mosaico` | `#ffffff` | Fondo de cada mosaico normal. |
| `--tinta` | `#121214` | Texto; fondo de la barra de pedido y de mosaicos seleccionados. |
| `--suave` | `#5b5b63` | La línea bajo el nombre (consola y/o nota). Nada más. |
| `--rojo` | `#e60012` | Acento: cabecera, "¿No ves tu juego?", ✓ de seleccionado, botón de la barra. |

Proporción: el suelo gris claro domina, los mosaicos blancos llevan el contenido, el rojo
aparece en **4 lugares fijos** (cabecera, "¿No ves tu juego?", ✓, acción del pedido).
No agregar rojo en otros sitios.

**Tipografía:** una sola familia, **Schibsted Grotesk**, pesos **500** y **800**
(cargada en `Layout.astro` por defecto). Respaldo: `system-ui, sans-serif`.

| Rol | Tamaño | Peso | Otros |
|---|---|---|---|
| Título `h1` | `clamp(38px, 11vw, 88px)` | 800 | interlineado .95, tracking -0.035em, máx. 12ch → siempre 2 líneas |
| Títulos de sección `h2` | `clamp(26px, 6.4vw, 44px)` | 800 | tracking -0.03em |
| Precio | 22px (destacado grande: 30px) | 800 | tracking -0.02em, **sin** `tabular-nums` (deja huecos en la coma) |
| Nombre del juego | 14px (grande: 18px/800) | 500 | máximo 2 líneas con `line-clamp` |
| Consola / nota | 13px | 500 | color `--suave` |
| "¿No ves tu juego?" | 22px | 800 | tracking -0.02em |

## 3. Retícula

| | Celular (< 760px) | Escritorio (≥ 760px) |
|---|---|---|
| Columnas | 6 | 10 |
| Separación entre mosaicos | 8px | 8px |
| Margen exterior | 10px | 12px |
| Radio de esquina | 8px en todos los mosaicos; 999px solo en controles (barra, "+") | igual |
| `grid-auto-flow` | `dense` (rellena huecos) | igual |

Tamaños de mosaico (clases) y cuántas columnas ocupan:

| Mosaico | Clase | Celular | Escritorio |
|---|---|---|---|
| Cabecera (tienda + h1) | `.cabecera` | 6 | 10 |
| Título de sección ("Switch 2", "Switch 1", "DLC y updates") | `h2` | 6 (sin fondo) | 10 |
| Destacado grande | `<Mosaico tamano="grande">` | 6, imagen 2:1 | 6 × 2 filas, imagen llena el alto |
| Destacados chicos | `<Mosaico tamano="medio">` | 3 | 4, imagen 2.1:1 |
| Juego / DLC / update | `<Mosaico>` | 3 (2 por fila) | 2 (5 por fila) |
| ¿No ves tu juego? | `.mas` | lo que falte para cerrar la fila (3 o 6) | lo que falte (2–10) |

Estructura de un mosaico de juego (no cambiar el orden):

```
┌──────────────────────┐
│ portada 16:9         │  .img  (object-fit: cover)
├──────────────────────┤
│ Nombre (2 líneas)    │  .n
│ Switch 1             │  .c   consola (si la sección no la dice) · nota
│ $ 279.900        (+) │  strong (abajo del todo); "+"/"✓" sale de aria-pressed
└──────────────────────┘
```

El precio va **debajo** de la portada, nunca encima de la imagen.

## 4. Estados e interacción

- **Se puede elegir** (`[aria-pressed]`, lo pone el script): círculo de 28px en `--suelo`
  con "+" a la derecha del precio. Sin JavaScript no aparece.
- **Seleccionado** (`[aria-pressed="true"]`): mosaico en `--tinta`, texto blanco, consola/nota en
  `#b9b9c2`, círculo rojo con ✓. Es la única señal: no agregar bordes ni sombras.
- **Al tocar:** `transform: scale(.98)` (150 ms).
- **Barra de pedido** (`Pedido.astro`): píldora negra fija abajo con el total, "Vaciar" y el
  botón rojo "Pedir por WhatsApp". Hasta 420px "Vaciar" se oculta (se vacía tocando los
  mosaicos) para que quepa un total de 7 cifras. Es el **único** elemento con sombra, porque
  flota. Aparece con una subida de 250 ms.
- `prefers-reduced-motion`: se quitan transiciones y la animación de la barra.
- Foco visible: `outline: 3px solid currentColor` (global en `Layout.astro`).

## 5. Textos

Todo el texto de la página: nombre de la tienda, **"Juegos para Switch 1 y 2"**, secciones
"Switch 2" / "Switch 1", nombres, consola/nota, precios, "¿No ves tu juego?", y en la barra
"Vaciar" / "Pedir por WhatsApp". Con DLC visibles, además "DLC y updates" y "¿Buscas otro
DLC?". **No agregar más.**

**La consola siempre se distingue, y una sola vez:** si el título de la sección la dice, el
mosaico no la repite (`conConsola={false}`); si no (destacados, DLC), va bajo el nombre.

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
| Eslóganes, textos de ayuda, beneficios, etiquetas que se repiten en todos los mosaicos | Cambiar el diseño hasta que no hagan falta (ej.: agrupar por consola en vez de etiquetar cada mosaico). |
| Mosaicos vacíos o de relleno | Cada mosaico tiene contenido real; si sobra hueco, lo cubre `grid-auto-flow: dense` o un mosaico "¿No ves tu juego?". |

## 7. Cómo extender sin romper el diseño

- **Agregar un juego:** solo una entrada en `productos.json` y su portada en
  `src/assets/Catalogo_Nintendo_Switch_Colombia/imagenes/<id>.webp`. No tocar el diseño.
- **Nueva sección** (ej. "Tarjetas eShop"): una entrada más en `secciones` de
  `lib/catalogo.ts`. La página la dibuja sola (`h2`, mosaicos y `.mas` que cierra la fila).
- **Un nuevo tipo de mosaico:** usar uno de los tamaños existentes (2/3/4/6/10 columnas),
  fondo de un token, radio de 8px, texto alineado arriba a la izquierda con 16–22px de
  relleno. Nunca centrado ni con borde.
- **Logo de la tienda:** va dentro de `.cabecera`, en el lugar de `.marca`, blanco
  sobre rojo, alto máx. 40px. No usar el logo de Nintendo.
- **Ofertas** (si el dueño las pide): precio anterior tachado en `--suave` a 14px junto
  al precio; sin píldora de "%".

## 8. Lista de revisión visual (antes de cada push)

- [ ] 390px y 1440px: sin scroll horizontal; márgenes iguales a ambos lados.
- [ ] `h1` y cada `h2` en ≤ 2 líneas a todo ancho.
- [ ] Ninguna fila del tablero con un hueco mayor a un mosaico.
- [ ] Todos los precios visibles y sin cortar; nombres largos cortados a 2 líneas con "…".
- [ ] Seleccionar 2 títulos: se ven en negro con ✓ y la barra muestra el total correcto.
- [ ] A 320px con todos elegidos, la barra no se desborda.
- [ ] Contraste: blanco sobre `--rojo` (4.8:1), `--suave` sobre blanco (6.7:1) y `#b9b9c2` sobre `--tinta` (9.6:1) cumplen AA.
- [ ] Ningún elemento de la tabla "No hacer" del §6.
