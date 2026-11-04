# Diseño A · Tablero: directrices

> Diseño elegido por el dueño. Archivos: `src/pages/index.astro` (tablero) y `src/components/Mosaico.astro` (producto).
> Leer completo antes de cambiar o agregar cualquier cosa visual.

## 1. Idea

**La página es un tablero de mosaicos planos encajados borde a borde**, como el póster
original de la tienda, pero ordenado. Cada mosaico es **una sola cosa**: el nombre de la
tienda o un juego con su precio (y la pestaña de su consola). El tablero empieza en la cabecera roja y termina en
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
| `--suave` | `#5b5b63` | La línea bajo el nombre (consola y/o nota, o "N versiones · desde"). Nada más. |
| `--rojo` | `#e60012` | Acento: cabecera, "¿No ves tu juego?", pestaña y sello de Switch 2, ✓ de seleccionado, botón de la barra. |

Proporción: el suelo gris claro domina, los mosaicos blancos llevan el contenido, el rojo
aparece en **5 lugares fijos** (cabecera, "¿No ves tu juego?", pestaña y sello de Switch 2, ✓, acción del pedido).
No agregar rojo en otros sitios.

**Tipografía:** una sola familia, **Schibsted Grotesk**, pesos **500** y **800**
(servida desde el propio sitio: `astro.config.mjs` → `fonts`, variable `--fuente`). Respaldo: `system-ui, sans-serif`.

| Rol | Tamaño | Peso | Otros |
|---|---|---|---|
| Título `h1` | `clamp(38px, 11vw, 88px)` | 800 | interlineado .95, tracking -0.035em; celular: máx. 12ch → 2 líneas; escritorio: 1 línea |
| Títulos de sección `h2` | `clamp(26px, 6.4vw, 44px)` | 800 | tracking -0.03em |
| Precio | 22px (destacado grande: 30px) | 800 | tracking -0.02em, **sin** `tabular-nums` (deja huecos en la coma) |
| Nombre del juego | 14px (grande: 18px) | 800 | máximo 2 líneas con `line-clamp`. En 800 porque casi todos los precios son iguales: el nombre es lo que distingue un mosaico de otro. |
| Nota ("Necesita Ring-Con", "3 versiones · desde") | 13px | 500 | color `--suave` |
| Pestaña de consola | logo 17px; "2" 17px | 800 | 32px de alto, relleno 0 9px |
| Sello de versión (juego con versiones) | logo 17px; "2" 17px; "Mejora a" 13px | 800 | 28px de alto, relleno 0 8px, radio 6px; fondo `--suelo` (Switch 2: `--rojo`) |
| "¿No ves tu juego?" | 22px | 800 | tracking -0.02em |
| Botones de la barra ("Pedir por WhatsApp") y "Listo" del panel | 15px | 800 | |
| Título del panel de versiones | 18px | 800 | máximo 2 líneas |

## 3. Retícula

| | Celular (< 760px) | Escritorio (≥ 760px) |
|---|---|---|
| Columnas | 6 | 10 |
| Separación entre mosaicos | 8px | 8px |
| Margen exterior | 10px | 12px; el tablero mide como máximo 1440px y se centra (más ancho, los mosaicos crecen de más) |
| Radio de esquina | 8px en todos los mosaicos; 6px en las filas y sellos de versión (van dentro de un mosaico); 999px solo en controles (barra, "+") | igual |
| `grid-auto-flow` | `dense` (rellena huecos) | igual |

Tamaños de mosaico (clases) y cuántas columnas ocupan:

| Mosaico | Clase | Celular | Escritorio |
|---|---|---|---|
| Cabecera (tienda + h1) | `.cabecera` | 6 | 10 |
| Título de sección (solo "DLC y updates") | `h2` | 6 (sin fondo) | 10 |
| Destacado grande | `<Mosaico tamano="grande">` | 6, imagen 2:1 | 6 × 2 filas, imagen llena el alto |
| Destacados chicos | `<Mosaico tamano="medio">` | 3 | 4, imagen 2.1:1 con alto máx. `50svh − 182px` (los 3 precios destacados se ven sin desplazar desde 768 px de alto) |
| Juego / DLC / update | `<Mosaico>` | 3 (2 por fila) | 2 (5 por fila) |
| Juego con varias versiones | `.ancho` (lo pone `Mosaico` si hay `grupo`) | 3, igual a un juego; las versiones van en el panel (`.panel`; sin JavaScript: 6 con las filas a la vista) | 2, igual a un juego (destacado chico: 4); las versiones van en el panel (sin JavaScript: 4 con las filas a la vista). Destacado chico con versiones: portada con alto máx. `50svh − 199px` (una línea más en el pie) |
| ¿No ves tu juego? | `.mas` | lo que falte para cerrar la sección (3 o 6) | lo que falte (2–10); lo calcula `lib/reticula.ts` |

Estructura de un mosaico de juego (no cambiar el orden):

```
┌──────────────────────┐
│[⊞2]                  │  .consola: pestaña pegada a la esquina (logo; Switch 2 en rojo + "2")
│ portada 16:9         │  .img  (object-fit: cover)
├──────────────────────┤
│ Nombre (2 líneas)    │  .n
│ Necesita Ring-Con    │  .c   solo si hay nota
│ $ 279.900        (+) │  strong (abajo del todo); "+"/"✓" sale de aria-pressed
└──────────────────────┘
```

Juego con varias versiones (Switch 1, Switch 2, paquete de mejora), un solo mosaico.

Celular y escritorio: mosaico normal; tocarlo (en cualquier parte) abre el panel con las versiones:

```
┌──────────────┐      ┌─ panel (PanelVersiones.astro) ─┐
│[⊞|⊞2]        │ tap  │ Nombre (18px, 800)             │
│ portada 16:9 │ ───▶ │ [⊞]            $ 279.900  (+)  │
│ Nombre       │      │ [⊞2]           $ 319.900  (+)  │
│ 3 vers.·desde│      │ [Mejora a ⊞2]   $ 39.900  (+)  │
│ $ 279.900 (+)│      │ [        Listo         ]       │
└──────────────┘      └────────────────────────────────┘
```

Panel: `<dialog>` modal, fondo `--mosaico`, fondo de atrás `--tinta` al 50 %, máx. 85svh de alto. Celular: pegado
abajo, radio 8px solo arriba, máx. 560px de ancho. Escritorio: centrado, radio 8px, máx. 420px de ancho. "Listo": píldora `--tinta` de 44px (no roja: no es la acción del
pedido). Sin sombra. Sube en 250 ms, como la barra.

Sin JavaScript (y en el destacado grande), las filas van dentro del mosaico:

```
┌──────────────────────────────────┐
│[⊞|⊞2]                            │  .consola.doble: pestaña doble (Switch 2 en rojo)
│ portada de Switch 2              │
├──────────────────────────────────┤
│ Nombre                           │  .n
│ [⊞]                $ 279.900 (+) │  .version: cada fila es su propio botón
│ [⊞2]               $ 319.900 (+) │  .sello a la izquierda; precio alineado a la derecha,
│ [Mejora a ⊞2]       $ 45.000 (+) │  junto al "+" (se comparan como en una lista)
└──────────────────────────────────┘
```

El precio va **debajo** de la portada, nunca encima de la imagen.

## 4. Estados e interacción

Las filas de versiones son visibles por defecto (6 columnas en celular y 4 en escritorio).
El script activa el mosaico compacto con `data-panel-listo` solo después de instalar los eventos.
Así el respaldo también funciona si el script falla. Si falla `showModal`, se restauran las filas visibles.

- **Se puede elegir** (`[aria-pressed]`, lo pone el script): círculo de 28px en `--suelo`
  con "+" a la derecha del precio. Sin JavaScript no aparece.
- **Sin precio** ("Consultar"): en lugar del "+" lleva un círculo igual con "↗", porque al tocarlo abre WhatsApp en vez de sumarse al pedido.
- **Pestaña de consola:** esquina sólida arriba a la izquierda, radio solo en la esquina de
  abajo a la derecha (8px). Switch 1: fondo del mosaico (`--fondo`) y logo en tinta; Switch 2:
  `--rojo`, logo y "2" en blanco. Sin sombra ni borde.
- **Seleccionado** (`[aria-pressed="true"]`): mosaico en `--tinta` (la pestaña de Switch 1 lo
  sigue porque usa `--fondo`), texto blanco, nota en `#b9b9c2`, círculo rojo con ✓. Es la única señal: no agregar bordes ni sombras.
- **Juego con varias versiones:** el estado es de cada fila: la fila elegida se pone en `--tinta` con su ✓.
  Como las filas no están a la vista, el mosaico se pone en
  `--tinta` con ✓ si hay al menos una versión elegida (`:has()`, sin estado aparte). Al cerrar el panel
  (Listo, Escape o tocar afuera) el foco vuelve al mosaico; con el panel abierto el total se anuncia desde él. El lector de pantalla lee cada fila como
  "Nombre del juego, Nintendo Switch 2, $ …" (el nombre va oculto dentro de la fila).
- **Al tocar:** `transform: scale(.98)` (150 ms).
- **Barra de pedido** (`Pedido.astro`): píldora negra fija abajo con el total, "Vaciar" y el
  botón rojo "Pedir por WhatsApp". Hasta 420px "Vaciar" se oculta (se vacía tocando los
  mosaicos) para que quepa un total de 7 cifras. Es el **único** elemento con sombra, porque
  flota. Aparece con una subida de 250 ms.
- `prefers-reduced-motion`: se quitan transiciones y la animación de la barra.
- Foco visible: `outline: 3px solid var(--tinta)` con 2px de separación (global en `Layout.astro`), que queda
  sobre el suelo gris (15,4:1) aunque el mosaico sea negro o rojo. Dentro de la barra de pedido va en blanco.
  No usar `currentColor`: en mosaicos con texto blanco el contorno quedaba blanco sobre gris (1,2:1).
- Mientras la barra de pedido está visible, `scroll-padding-bottom` evita que tape el mosaico con foco.
- Lector de pantalla: el "+" / "✓" es decorativo (`content: '+' / ''`); el estado lo da `aria-pressed`. Al
  cambiar el pedido se anuncia "Total del pedido: $ …" desde un párrafo oculto (`#anuncio`), no desde la barra.

## 5. Textos

Todo el texto de la página: nombre de la tienda, **"Códigos para Switch 1 y 2"** (dice que se venden códigos digitales, no juegos físicos), nombres,
nota, precios, "Mejora a" (sello del paquete de mejora), "N versiones · desde" y "Listo" (juego con versiones, celular), "¿No ves tu juego?", y en la barra "Vaciar" / "Pedir por WhatsApp". Con DLC
visibles, además "DLC y updates" y "¿Buscas otro DLC?". **No agregar más.**

**La consola siempre se distingue, con la pestaña y no con texto:** cada mosaico, en cualquier
lugar del tablero, lleva la pestaña de su consola. El lector de pantalla la lee como
"Nintendo Switch 1/2".

- Tono: tuteo, frases cortas, español neutro latinoamericano. Botones que dicen lo que
  hacen ("Pedir por WhatsApp", "Vaciar"). Nada de "Descubre", "Increíble", emojis.

## 6. Reglas (adaptadas de taste-skill; obligatorias)

| No hacer | En su lugar |
|---|---|
| Degradados (fondos, botones, texto) | Colores planos de los tokens o la portada. |
| Sombras en elementos quietos | Cambio de tono entre suelo y mosaico. La única sombra es la barra de pedido. |
| Bordes finos o líneas divisorias de 1px | Separación de 8px del tablero. |
| Píldoras/etiquetas sobre títulos ("NUEVO", "HOT", "-20%") | Destacar por tamaño. *Decisión abierta D3 en el spec.* La **única** marca sobre la portada es la pestaña de consola. |
| Letras chiquitas en MAYÚSCULAS con espaciado | Texto normal, legible, en minúsculas con mayúscula inicial. |
| Monospace, numeración 01/02/03 | Orden por posición y tamaño. |
| Más de una familia tipográfica, o tamaños intermedios nuevos | La tabla del §2. |
| Emojis, íconos decorativos, formas de relleno | Una portada real o nada. |
| Títulos de más de 2 líneas | Recortar palabras; luego ensanchar; el tamaño, al final. |
| Una palabra del título con otro color o cursiva | Un color, un peso. |
| Eslóganes, textos de ayuda, beneficios, etiquetas que se repiten en todos los mosaicos | Cambiar el diseño hasta que no hagan falta (ej.: la pestaña con logo en vez de escribir "Switch 1" en cada mosaico). |
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
- **Logo de consola:** `src/assets/switch.svg` (`fill="currentColor"`). Para usar el oficial,
  reemplazar ese archivo por uno cuadrado de una sola tinta; el "2" de Switch 2 lo pone `Mosaico.astro`.

## 8. Lista de revisión visual (antes de cada push)

- [ ] 390px y 1440px: sin scroll horizontal; márgenes iguales a ambos lados. En escritorio, todas las filas de juegos con 5 mosaicos del mismo alto.
- [ ] Portadas nítidas en escritorio ×2: el navegador baja una variante ≥ 90 % del ancho dibujado (originales de 1920px).
- [ ] `h1` y cada `h2` en ≤ 2 líneas a todo ancho.
- [ ] Ninguna fila del tablero con un hueco mayor a un mosaico.
- [ ] Todos los precios visibles y sin cortar; nombres largos cortados a 2 líneas con "…".
- [ ] Seleccionar 2 títulos: se ven en negro con ✓ y la barra muestra el total correcto.
- [ ] A 320px con todos elegidos, la barra no se desborda.
- [ ] Contraste: blanco sobre `--rojo` (4.8:1), `--suave` sobre blanco (6.7:1) y `#b9b9c2` sobre `--tinta` (9.6:1) cumplen AA.
- [ ] Con Tab: el contorno de foco se ve en mosaicos blancos, elegidos y rojos, y ninguno queda bajo la barra.
- [ ] Ningún elemento de la tabla "No hacer" del §6.
- [ ] Juegos con versiones: a 320px las filas de precio no se salen; los precios quedan alineados a la derecha junto al "+"; elegir una versión pone solo esa fila en negro. En celular y escritorio: el mosaico mide lo mismo que un juego, el panel abre al tocar, y al cerrar el mosaico queda en negro con ✓.
