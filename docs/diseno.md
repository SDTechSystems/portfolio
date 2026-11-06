# Diseño A · Tablero (Vitrina oscura): directrices

> Diseño elegido por el dueño. Archivos: `src/pages/index.astro` (tablero) y `src/components/Mosaico.astro` (producto).
> Leer completo antes de cambiar o agregar cualquier cosa visual.

## 1. Idea

**La página es un tablero de mosaicos planos encajados borde a borde**, como el póster
original de la tienda, pero ordenado. Cada mosaico es **una sola cosa**: el nombre de la
tienda o un juego con su precio (y la pestaña de su consola). Desde 2026-11-05 el tablero es una **vitrina oscura**: suelo casi negro y mosaicos grafito para que las portadas
resalten como en una tienda de consola. Desde 2026-11-06 lleva la **marca SD Tech Imports** con el aire del
portafolio de SD Tech (https://sdtechsystems.dev): paleta navy y cian, tipografía DejaVu, ceja en mono y título en dos
tonos. El tablero empieza en la cabecera (logo de SD Tech Imports en su placa blanca, ceja y título) y termina en
"¿No ves tu juego?"; debajo va el pie de contacto (`Pie.astro`: WhatsApp y Facebook de `tienda.ts`).

**Sin texto que explique la pantalla.** Nada de eslóganes, ayudas, beneficios ni etiquetas
repetidas. Si algo necesita una frase para entenderse, se cambia el diseño (ej.: el "+" en
cada precio sustituye a "Toca varios títulos para armar tu pedido").

Dirección de arte tomada de taste-skill: `dense-tiles`. Las portadas de los juegos son el
contenido visual; el diseño no agrega adornos alrededor.

## 2. Tokens

Definidos en `:root` (`Layout.astro`). Usar **solo** estos.

| Token | Valor | Uso |
|---|---|---|
Dos modos, **claro** y **oscuro**. Al abrir por primera vez se usa el del sistema (`prefers-color-scheme`);
el botón de la cabecera (luna/sol, 44px, fondo `--mosaico`) lo cambia y se recuerda en `localStorage['tema']`.
Un script en `<head>` pone `data-tema` en `<html>` antes de pintar (sin parpadeo). Sin JavaScript el botón no
sale y manda el sistema. Los componentes solo usan tokens: nunca un color fijo que cambie con el modo.

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--suelo` | `#eef5fb` | `#07111f` | Fondo de la página (entre mosaicos); texto de mosaicos elegidos, barra y "Listo". |
| `--mosaico` | `#ffffff` | `#0f1e36` | Fondo de cada mosaico normal y del botón de tema. |
| `--tinta` | `#0d1b33` | `#f4f8fc` | Texto; fondo de la barra de pedido, de "Listo" y de mosaicos seleccionados (contraste invertido). |
| `--suave` | `#5d6778` | `#a7b9cd` | La línea bajo el nombre (consola y/o nota, o "N versiones · Switch 1 desde"). Nada más. |
| `--suave-sel` | `#a7b9cd` | `#4a5b72` | Esa misma línea dentro de un mosaico elegido. |
| `--sin-portada` | `#d6e2ee` | `#1a2b47` | Fondo del hueco de la portada mientras carga. |
| `--sombra` | navy 25% | negro 60% | Solo lo que flota: barra de pedido, lupa y campo de búsqueda. |
| `--vidrio` | `--mosaico` al 40% | `--mosaico` al 40% | Vidrio líquido de la lupa (el campo usa `--mosaico` al 65%: lleva texto). Nada más. |
| `--brillo` | blanco 95% | blanco 45% | Reflejo del vidrio, arriba a la izquierda. |
| `--brillo-suave` | blanco 40% | blanco 12% | Canto y resplandor interior del vidrio. |
| `--canto` | negro 14% | negro 40% | Lado en sombra del grosor del vidrio (abajo a la derecha). |
| `--acento` | `#00bfef` | `#00bfef` | Cian de SD Tech Imports. Acento: parte del título y punto final, rayita de las cejas, "¿No ves tu juego?", pestaña y sello de Switch 2, ✓ de seleccionado, botón de la barra. |
| `--acento-texto` | `#0094c6` | `#00bfef` | El acento cuando es texto (parte del título, "Escríbenos."): en claro, el cian oscuro de la marca (3,2:1 sobre `--suelo`, solo texto grande). |
| `--sobre-acento` | `#001b44` | `#001b44` | Navy de SD Tech Imports: texto e íconos sobre `--acento` (nunca blanco sobre cian: no llega a AA). |
| `--linea` | `#d6e2ee` | `#2c405b` | Líneas finas bajo la ceja de la cabecera y sobre la firma del pie. Nada más. |

El logo maestro (`src/assets/marca/logo-sd-tech-imports.png`) va siempre sobre una placa blanca (`#fff`, única
excepción fija): sus letras navy no se leen sobre el suelo oscuro. No recolorearlo, estirarlo ni redibujarlo.
El favicon (`public/favicon.png` y `apple-touch-icon.png`) es el símbolo SD con la órbita y el avión recortado del mismo logo.

Proporción: el suelo domina, los mosaicos llevan el contenido, el cian
aparece en **lugares fijos** (título y cejas, "¿No ves tu juego?", pestaña y sello de Switch 2, ✓, acción del pedido, frase del pie).
No agregar cian en otros sitios.

**Tipografía:** la del portafolio de SD Tech: **DejaVu Sans** ("SD Sans", regular y negrita; en CSS los pesos 500 y 800
caen en esas dos) y **DejaVu Sans Mono** ("SD Mono", variable `--mono`) solo para cejas, redes del pie y firma, en
mayúsculas con tracking .12em. Servidas desde el propio sitio y recortadas a latín (`src/assets/marca/*.woff2`,
`astro.config.mjs` → `fonts`). DejaVu es más ancha que la anterior: el precio de los mosaicos usa
`clamp(17px, 5.4vw, 22px)` y a 360px o menos el botón de la barra dice solo «Pedir».

| Rol | Tamaño | Peso | Otros |
|---|---|---|---|
| Título `h1` | `clamp(36px, 10vw, 76px)` | 800 | interlineado 1, tracking -0.045em; "Switch 1 y 2" y el punto en `--acento`; celular: máx. 12ch → 2 líneas; escritorio: 1 línea |
| Títulos de sección `h2` | `clamp(26px, 6.4vw, 44px)` | 800 | tracking -0.03em |
| Precio | `clamp(17px, 5.4vw, 22px)` (destacado grande: 30px) | 800 | tracking -0.02em, **sin** `tabular-nums` (deja huecos en la coma) |
| Nombre del juego | 14px (grande: 18px) | 800 | máximo 2 líneas con `line-clamp`. En 800 porque casi todos los precios son iguales: el nombre es lo que distingue un mosaico de otro. |
| Nota ("Necesita Ring-Con", "3 versiones · Switch 1 desde"; la edición no se parte de línea) | 13px | 500 | color `--suave` |
| Pestaña de consola | logo 17px; "2" 17px | 800 | 32px de alto, relleno 0 9px |
| Sello de versión (juego con versiones) | logo 17px; "2" 17px; "Mejora a" 13px | 800 | 28px de alto, relleno 0 8px, radio 6px; fondo `--suelo` (Switch 2: `--acento`) |
| "¿No ves tu juego?" | 22px | 800 | tracking -0.02em |
| Botones de la barra ("Pedir por WhatsApp") y "Listo" del panel | 15px | 800 | |
| Título del panel de versiones | 18px | 800 | máximo 2 líneas |

## 3. Retícula

| | Celular (< 760px) | Escritorio (≥ 760px) |
|---|---|---|
| Columnas | 6 | 10 |
| Separación entre mosaicos | 10px | 12px |
| Margen exterior | 10px | 12px; el tablero mide como máximo 1440px y se centra (más ancho, los mosaicos crecen de más) |
| Radio de esquina | 12px en todos los mosaicos; 6px en las filas y sellos de versión (van dentro de un mosaico); 999px solo en controles (barra, "+") | igual |
| `grid-auto-flow` | `dense` (rellena huecos) | igual |

Tamaños de mosaico (clases) y cuántas columnas ocupan:

| Mosaico | Clase | Celular | Escritorio |
|---|---|---|---|
| Cabecera (tienda + h1) | `.cabecera` | 6 | 10 |
| Título de sección (solo "DLC y updates") | `h2` | 6 (sin fondo) | 10 |
| Destacado grande (portada de cine) | `<Mosaico tamano="grande">` | 6, imagen 16:9; el pie es un panel sólido (`--fondo`, radio 8px) que sube 44px sobre la portada | 10 (todo el ancho), imagen 21:9 con alto máx. `max(360px, 100svh − 280px)`; el pie flota abajo a la izquierda (16px del borde, ancho `min(440px, 45%)`). Sin degradado. |
| Destacados chicos | `<Mosaico tamano="medio">` | 3 | 5 (dos lado a lado bajo la portada de cine), imagen 2.1:1; asoman bajo el pliegue para invitar a bajar |
| Juego / DLC / update | `<Mosaico>` | 3 (2 por fila) | 2 (5 por fila) |
| Juego con varias versiones | `.ancho` (lo pone `Mosaico` si hay `grupo`) | 3, igual a un juego; las versiones van en el panel (`.panel`; sin JavaScript: 6 con las filas a la vista) | 2, igual a un juego (destacado chico: 4); las versiones van en el panel (sin JavaScript: 4 con las filas a la vista). Destacado chico con versiones: portada con alto máx. `50svh − 199px` (una línea más en el pie) |
| ¿No ves tu juego? | `.mas` | lo que falte para cerrar la sección (3 o 6) | lo que falte (2–10); lo calcula `lib/reticula.ts` |

Estructura de un mosaico de juego (no cambiar el orden):

```
┌──────────────────────┐
│[⊞2]                  │  .consola: pestaña pegada a la esquina (logo; Switch 2 en cian + "2")
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

Panel: `<dialog>` modal, fondo `--mosaico`, fondo de atrás negro al 70 %, máx. 85svh de alto. Celular: pegado
abajo, radio 16px solo arriba, máx. 560px de ancho. Escritorio: centrado, radio 16px, máx. 420px de ancho. "Listo": píldora `--tinta` de 44px (no roja: no es la acción del
pedido). Sin sombra. Sube en 250 ms, como la barra. En el panel, cada versión de juego con imagen lleva
su portada (96 px, 16:9, radio 6px) con el sello encima en la esquina, como la pestaña del mosaico; la
mejora y las versiones sin imagen, solo el sello.

Sin JavaScript (y en el destacado grande), las filas van dentro del mosaico:

```
┌──────────────────────────────────┐
│[⊞|⊞2]                            │  .consola.doble: pestaña doble (Switch 2 en cian)
│ portada general o de la edición  │  la del precio "desde" si no hay general
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
  `--acento`, logo y "2" en `--sobre-acento`. Sin sombra ni borde.
- **Seleccionado** (`[aria-pressed="true"]`): mosaico en `--tinta` (la pestaña de Switch 1 lo
  sigue porque usa `--fondo`), texto `--suelo`, nota en `--suave-sel`, círculo cian con ✓ en `--sobre-acento`. Es la única señal: no agregar bordes ni sombras.
- **Juego con varias versiones:** el estado es de cada fila: la fila elegida se pone en `--tinta` con su ✓.
  Como las filas no están a la vista, el mosaico se pone en
  `--tinta` con ✓ si hay al menos una versión elegida (`:has()`, sin estado aparte). Al cerrar el panel
  (Listo, Escape o tocar afuera) el foco vuelve al mosaico; con el panel abierto el total se anuncia desde él. El lector de pantalla lee cada fila como
  "Nombre del juego, Nintendo Switch 2, $ …" (el nombre va oculto dentro de la fila).
- **Al tocar:** `transform: scale(.98)` (150 ms).
- **Barra de pedido** (`Pedido.astro`): píldora clara (`--tinta`) fija abajo con el total, "Vaciar" y el
  botón cian "Pedir por WhatsApp". Hasta 420px "Vaciar" se oculta (se vacía tocando los
  mosaicos) para que quepa un total de 7 cifras. Lleva sombra porque flota (como
  la lupa y el campo de búsqueda). Aparece con una subida de 250 ms.
- **Buscador** (`Buscador.astro`), estilo vidrio líquido: casi transparente, desenfoque corto (10px,
  saturación 1,8), canto de luz con reflejo arriba a la izquierda (`--brillo`), lado en sombra abajo a la
  derecha (`--canto`) y la sombra de lo que flota. Ícono en `--tinta`, nunca cian. Sin desenfoque en el
  navegador: fondo `--mosaico`.
  - Lupa redonda de 52px abajo a la derecha. Entra con rebote al cargar, crece a 1,07 con el ratón y se
    hunde a 0,88 al tocarla. Con la barra de pedido visible sube con rebote a `bottom: 84px`.
  - Al tocarla, la lupa se encoge y desaparece. El campo nace arriba a la derecha como un círculo de 52px y
    se estira con rebote (0,6 s, `cubic-bezier(.34, 1.4, .64, 1)`) hasta la píldora (máx. 560px). El texto
    y el ✕ aparecen al final. Al cerrar se recoge sin rebote (0,35 s) y la lupa vuelve.
  - Al abrir, la página se coloca al inicio del catálogo, para que bajo el vidrio queden portadas y no la
    marca roja. Texto a 18px/500 (con menos, iOS acerca la página) y ✕ propio. El campo no lleva contorno de
    foco (el cursor lo marca y taparía el canto); el ✕ sí, con Tab.
  - Con texto se ocultan la cabecera y los `h2`, y queda un solo "¿No ves tu juego?" al final, con el ancho
    que cierra la fila. Lo que reaparece sube con un fundido corto (`@starting-style`), solo después de usar
    el buscador: al cargar, la página sale quieta.
- `prefers-reduced-motion`: se quitan transiciones y animaciones (barra, lupa, campo y fundido de resultados).
- Foco visible: `outline: 3px solid var(--tinta)` con 2px de separación (global en `Layout.astro`), que queda
  sobre el suelo oscuro (18:1) aunque el mosaico esté elegido o sea cian. Dentro de la barra de pedido va en `--suelo`.
  No usar `currentColor`: en mosaicos elegidos el contorno quedaría oscuro sobre el suelo oscuro.
- Mientras la barra de pedido está visible, `scroll-padding-bottom` evita que tape el mosaico con foco.
- Lector de pantalla: el "+" / "✓" es decorativo (`content: '+' / ''`); el estado lo da `aria-pressed`. Al
  cambiar el pedido se anuncia "Total del pedido: $ …" desde un párrafo oculto (`#anuncio`), no desde la barra.

## 5. Textos

Todo el texto de la página: nombre de la tienda, **"Códigos para Switch 1 y 2"** (dice que se venden códigos digitales, no juegos físicos), nombres,
nota, precios, "Mejora a" (sello del paquete de mejora), "N versiones · Switch 1 desde" y "Listo" (juego con versiones, celular), "¿No ves tu juego?", y en la barra "Vaciar" / "Pedir por WhatsApp". Con DLC
visibles, además "DLC y updates" y "¿Buscas otro DLC?". El campo de búsqueda lleva "Buscar juego" como marcador (solo se ve al abrirlo). **No agregar más.**

**La consola siempre se distingue, con la pestaña y no con texto:** cada mosaico, en cualquier
lugar del tablero, lleva la pestaña de su consola. El lector de pantalla la lee como
"Nintendo Switch 1/2".

- Tono: tuteo, frases cortas, español neutro latinoamericano. Botones que dicen lo que
  hacen ("Pedir por WhatsApp", "Vaciar"). Nada de "Descubre", "Increíble", emojis.

## 6. Reglas (adaptadas de taste-skill; obligatorias)

| No hacer | En su lugar |
|---|---|
| Degradados (fondos, botones, texto) | Colores planos de los tokens o la portada. |
| Vidrio/desenfoque en mosaicos, cabecera o tablero | Solo en lo que flota sobre el contenido (lupa y campo de búsqueda). |
| Sombras en elementos quietos | Cambio de tono entre suelo y mosaico. La sombra es solo de lo que flota: barra de pedido, lupa y campo de búsqueda. Con ratón, la portada se acerca (escala 1,04, 300 ms; nada con movimiento reducido). |
| Bordes finos o líneas divisorias de 1px | Separación de 10/12px del tablero. Única excepción: el canto de luz del vidrio líquido (sombra interior), que es su grosor y no un borde. |
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
  fondo de un token, radio de 12px, texto alineado arriba a la izquierda con 16–22px de
  relleno. Nunca centrado ni con borde.
- **Logo de la tienda:** el maestro de SD Tech Imports, dentro de `.cabecera` en `.marca`, sobre su placa
  blanca; 40px de alto en celular y 48px en escritorio. No usar el logo de Nintendo.
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
- [ ] Seleccionar 2 títulos: se encienden en `--tinta` con ✓ y la barra muestra el total correcto.
- [ ] A 320px con todos elegidos, la barra no se desborda.
- [ ] Contraste: `--sobre-acento` sobre `--acento` (7.8:1), `--suave` sobre `--mosaico` (5.7:1 claro, 8.3:1 oscuro), `--tinta` sobre `--mosaico` (17:1 claro, 15.6:1 oscuro), `--suave-sel` sobre `--tinta` (6.5:1 / 8.6:1) y `--acento-texto` sobre `--suelo` en texto grande (3.2:1 claro, 8.7:1 oscuro) cumplen AA.
- [ ] Con Tab: el contorno de foco se ve en mosaicos grafito, elegidos y cian, y ninguno queda bajo la barra.
- [ ] Ningún elemento de la tabla "No hacer" del §6.
- [ ] Buscador a 390px, con y sin pedido: la lupa no tapa la barra; buscar "zelda" y "xyz" no deja huecos y el cierre cian queda al final; Escape devuelve el tablero; la lupa se lee sobre portadas claras y cian.
- [ ] Juegos con versiones: a 320px las filas de precio no se salen; los precios quedan alineados a la derecha junto al "+"; elegir una versión enciende solo esa fila en `--tinta`. En celular y escritorio: el mosaico mide lo mismo que un juego, el panel abre al tocar, y al cerrar el mosaico queda encendido con ✓.
