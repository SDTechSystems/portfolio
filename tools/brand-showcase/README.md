# Portafolio de diseño de marca

Genera las 24 marcas de ejemplo que se muestran en `/es/marcas/` y `/en/marcas/`: logos y versiones, piezas del paquete, guía de uso, mockups de productos e imagen corporativa. Todo sale como SVG con el texto convertido a trazos, así que se ve igual en cualquier navegador sin cargar fuentes.

Las marcas son ficticias y así se indica en el sitio. Las tipografías son de Google Fonts con licencia SIL Open Font License 1.1 o Apache 2.0, ambas libres para uso comercial.

## Regenerar

Requiere Python 3.11 o posterior, Node.js (para descargar las fuentes con npm) y estas librerías:

```sh
pip install fonttools brotli uharfbuzz
cd tools/brand-showcase
python3 fonts.py          # descarga las fuentes a .cache/ (una sola vez)
python3 build.py          # todas las marcas
python3 build.py sereno   # o solo algunas
```

`build.py` escribe los SVG en `public/marcas/<marca>/` y los datos del sitio en `src/data/brand-showcase.json`. Después basta con `npm run build`.

## Dónde se edita cada cosa

| Archivo | Contenido |
|---|---|
| `brands1.py`, `brands2.py`, `brands3.py` | Cada marca: nombre, sector, concepto, eslogan, paleta, tipografías, símbolo, logotipo y productos (es/en). |
| `model.py` | Versiones del logo (principal, vertical, símbolo, inversa, una tinta) y ayudas de dibujo. |
| `pieces.py` | Perfil, portada, publicación, stickers, muestras tipográficas, área de protección, usos incorrectos y portada de galería. |
| `mockups.py` | Plantillas de productos y de imagen corporativa (papelería, firma de correo y presentación). |
| `notes.py` | Detalles de producto por marca (sabores de lata, pesos de empaque, secciones de menú). |
| `fonts.py` | Lista de tipografías y descarga desde Fontsource. |
| `lib.py` | Texto a trazos con kerning (HarfBuzz), composición y utilidades de color. |

Los textos de la galería (paquete, imagen corporativa, etiquetas) están en `src/data/brands.ts` y las páginas en `src/components/BrandGallery.astro`, `BrandPage.astro` y `BrandCard.astro`.

## Agregar una marca

1. Copia una marca existente en `brands3.py`, cambia `slug`, textos, colores, fuentes, `symbol` y `wordmark`, y agrégala a `BRANDS`.
2. Si usa una fuente nueva, añádela en `fonts.py` y ejecuta `python3 fonts.py`.
3. Elige 6 productos de `TEMPLATES` en `mockups.py` para `mockups`.
4. Ejecuta `python3 build.py <slug>`, revisa los SVG y compila el sitio.

El botón de WhatsApp de cada marca usa `waMessages.brand` en `src/data/catalog.ts` y envía el nombre del diseño y su enlace.
