# Catálogo Nintendo Switch

Página de una sola pantalla, pensada para celular, con los códigos digitales de juegos para
Switch 1 y Switch 2 y su precio. El cliente toca los juegos que quiere y envía el pedido por
WhatsApp con la lista y el total.

## Cómo cambiar el catálogo

Todo se edita en dos archivos. No hace falta tocar el diseño.

### Precios y juegos: `src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json`

Cada juego es un bloque como este:

```json
{
  "id": "mario-kart-world",
  "titulo": "Mario Kart World",
  "plataforma": "Nintendo Switch 2",
  "tipo_producto": "juego_digital",
  "precio_venta_cop": 299900,
  "precio_referencia_eshop_colombia_cop": 319900,
  "imagen": { "ruta": "imagenes/mario-kart-world.webp" }
}
```

| Campo | Qué poner |
|---|---|
| `id` | Nombre único en minúsculas con guiones. Igual al nombre de la portada. |
| `titulo` | El nombre que ve el cliente. |
| `plataforma` | `"Nintendo Switch"` (Switch 1) o `"Nintendo Switch 2"`. |
| `tipo_producto` | `"juego_digital"`, `"juego_con_accesorios"` (muestra "Necesita Ring-Con"), `"dlc"`, `"update"` o `"paquete_mejora"` (ver abajo). |
| `grupo` | Opcional. Solo para juegos con versión de Switch 1 y de Switch 2 (ver abajo). |
| `precio_venta_cop` | **Tu precio**, sin puntos: `299900`. Opcional; si no está, se usa el de referencia; `null` fuerza «Consultar». |
| `precio_referencia_eshop_colombia_cop` | Precio de la eShop; solo se usa si falta `precio_venta_cop`. Si tampoco hay referencia, muestra «Consultar». |
| `publicar` | Opcional. `false` oculta el producto de la página sin borrarlo (ej. precio pendiente). |
| `imagen` | Opcional. Sin imagen, la portada queda gris. |

- **Cambiar un precio:** edita `precio_venta_cop` (o agrégalo).
- **Retirar un precio sin perder la referencia:** pon `"precio_venta_cop": null`; muestra «Consultar» y no entra al pedido. Solo un campo ausente usa el precio de referencia.
- **Agregar un juego:** copia un bloque, cambia los datos y pon su portada (imagen 16:9, ideal 1920×1080 para que se vea nítida en computador)
  en `src/assets/Catalogo_Nintendo_Switch_Colombia/imagenes/<id>.webp`.
- **Quitar un juego:** borra su bloque (y las comas sobrantes).
- **Juego con versión de Switch 1 y de Switch 2** (y paquete de mejora): pon un bloque por cada
  versión que vendes, cada uno con su `id` y su precio, y en todos el mismo `"grupo"` (ej.
  `"grupo": "zelda-totk"`). La página los muestra en **un solo mosaico** con un precio por versión.
  - Versión de Switch 2: `"plataforma": "Nintendo Switch 2"`, `"tipo_producto": "juego_digital"`.
  - Paquete de mejora (pasa el juego de Switch 1 a Switch 2): `"plataforma": "Nintendo Switch 2"`,
    `"tipo_producto": "paquete_mejora"`.
  - El mosaico usa la portada de la versión de Switch 2: ponle `imagen` a ese bloque. En celular la
    portada se recorta y se conserva la parte de abajo; si el logo está arriba, agrega
    `"recorte": "arriba"` dentro de `imagen` (también vale `"centro"`). Si el juego es el destacado grande y en
    computador se corta el logo por un lado, usa `"izquierda"` o `"derecha"` (el lado donde está el logo).
  - Ejemplos en el archivo: los dos Zelda, Mario Wonder y Animal Crossing.

### Datos de la tienda: `src/data/tienda.ts`

Nombre de la tienda, número de WhatsApp (solo dígitos con código de país: `57` + 10 dígitos),
los 3 juegos destacados de arriba y si se muestra la sección "DLC y updates".

`url` es la dirección pública del sitio (ej. `'https://tutienda.pages.dev'`). Mientras esté vacía,
al compartir el enlace por WhatsApp no aparece la imagen de vista previa. Esa imagen se arma sola
con las portadas de los 3 destacados.

### Si algo está mal escrito

`npm run build` revisa los dos archivos y se detiene con una lista en español de lo que hay que
corregir, por ejemplo:

```
Revisa el catálogo:
- Producto 15 (mario-kart-world): "plataforma" es "Nintendo switch 2"; debe ser "Nintendo Switch" o "Nintendo Switch 2".
- Producto 3 (super-smash-bros-ultimate): no existe la portada "imagenes/smash.webp" (revisa el nombre del archivo en la carpeta imagenes/).
```

## Comandos

Requiere Node 22.23.4 o más reciente.

| Comando | Qué hace |
|---|---|
| `npm install` | Instala lo necesario (una sola vez). |
| `npm run dev` | Abre la página en `http://localhost:4321` mientras editas. |
| `npm test` | Pruebas de regresión con el runner de Node. |
| `npm run build` | Revisa el catálogo y genera el sitio listo para publicar en `dist/`. |
| `npm run preview` | Muestra el sitio de `dist/` tal como quedará publicado. |

## Publicación

El sitio se publica solo en Cloudflare Workers cada vez que algo llega a `main` (1–2 minutos).
`wrangler.jsonc` le dice a Cloudflare que suba la carpeta `dist/` tal cual. Si se cambia el nombre del
Worker en el panel de Cloudflare, hay que cambiar también `"name"` en ese archivo.

## Para quien desarrolla

Antes de cambiar código lee `docs/spec.md` (requisitos, estado y decisiones) y `docs/diseno.md`
(reglas del diseño A · Tablero). Está hecho con [Astro](https://docs.astro.build), sin frameworks de UI.

## Condiciones de canje y entrega

En `productos.json`, `condiciones_generales` define la regla del catálogo. El dueño
confirmó códigos japoneses: el comprador cambia la región de su cuenta y recibe
una guía para cambiarla y canjear el artículo. El código se canjea en su cuenta.
Los idiomas siguen sin confirmar; la región no determina el idioma del juego.

Cada producto puede añadir `condiciones` con excepciones a la regla general:

```json
"condiciones": {
  "region_canje": "Japón",
  "idiomas": null,
  "requiere_cambio_region": true,
  "modalidad_entrega": "Código japonés con guía de canje",
  "codigo_cuenta_propia": true
}
```

Campos opcionales: `region_canje`, `modalidad_entrega` y `requisitos` son textos
(de 1 a 160 caracteres); `idiomas` es una lista de nombres de idiomas (1–20,
hasta 40 caracteres cada uno); `requiere_cambio_region` y `codigo_cuenta_propia`
son `true` o `false`. No se admiten textos vacíos ni saltos de línea.
Omitir un campo hereda la regla general; poner `null` la anula y deja ese dato
por confirmar. Añade idiomas solo cuando estén verificados para esa versión.

«Detalles» gira la tarjeta individual para consultar las condiciones antes de elegir,
sin mover el tablero. «Volver» o Escape recuperan la portada. Si el contenido no cabe,
se puede desplazar dentro del reverso. Sin JavaScript funciona como desplegable;
las versiones conservan sus detalles en el panel. Las mejoras indican siempre que requieren el juego base de Switch 1
y que se usan en Switch 2. «Consultar condiciones» abre una consulta independiente
por WhatsApp; el pedido también incluye la variante y sus condiciones.
