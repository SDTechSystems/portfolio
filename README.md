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
| `tipo_producto` | `"juego_digital"`, `"juego_con_accesorios"` (muestra "Necesita Ring-Con"), `"dlc"` o `"update"`. |
| `precio_venta_cop` | **Tu precio**, sin puntos: `299900`. Opcional; si no está, se usa el de referencia. |
| `precio_referencia_eshop_colombia_cop` | Precio de la eShop. `null` muestra "Consultar" y el juego no entra al pedido. |
| `imagen` | Opcional. Sin imagen, la portada queda gris. |

- **Cambiar un precio:** edita `precio_venta_cop` (o agrégalo).
- **Agregar un juego:** copia un bloque, cambia los datos y pon su portada (imagen 16:9, ej. 960×540)
  en `src/assets/Catalogo_Nintendo_Switch_Colombia/imagenes/<id>.webp`.
- **Quitar un juego:** borra su bloque (y las comas sobrantes).

### Datos de la tienda: `src/data/tienda.ts`

Nombre de la tienda, número de WhatsApp (solo dígitos con código de país: `57` + 10 dígitos),
los 3 juegos destacados de arriba y si se muestra la sección "DLC y updates".

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
| `npm run build` | Revisa el catálogo y genera el sitio listo para publicar en `dist/`. |
| `npm run preview` | Muestra el sitio de `dist/` tal como quedará publicado. |

## Para quien desarrolla

Antes de cambiar código lee `docs/spec.md` (requisitos, estado y decisiones) y `docs/diseno.md`
(reglas del diseño A · Tablero). Está hecho con [Astro](https://docs.astro.build), sin frameworks de UI.
