# Portafolio de diseño de marca: resumen para continuar el trabajo

Este documento resume la sección de marcas del portafolio de **SD Tech Systems** (Juan Sebastián Duque Valencia) para que cualquier agente o persona pueda retomarla sin el historial de la conversación original.

- Sitio en vivo: https://sdtechsystems.dev/es/marcas/ (también en `/en/marcas/`)
- Repositorio: `SDTechSystems/portfolio`. Cada push a `main` se publica en GitHub Pages.
- WhatsApp Business del negocio: +57 305 814 7293

## Objetivo

Mostrar a clientes potenciales un portafolio de **36 marcas de ejemplo**, todas ficticias y señaladas así en el sitio. Cada marca trae su paquete completo: logos y versiones, paleta, tipografías, guía de uso, piezas para redes, mockups de productos e imagen corporativa. Los estilos varían entre lujo, llamativo, sobrio, minimalista, etc. Cada marca tiene un botón de WhatsApp que envía al cliente con el nombre del diseño que le interesó.

## Estado actual (noviembre de 2026)

| Pieza | Estado |
|---|---|
| 36 marcas (12 de lujo primero, luego 24 más) | Publicado |
| Acceso desde la portada y el menú, filtros por estilo, página por marca | Publicado |
| Imagen corporativa (papelería, firma de correo, presentación) | Publicado |
| Botón de WhatsApp por marca | Publicado |
| Fotos 3D realistas: todos los mockups de producto e imagen corporativa | Publicado |
| Logos sin superposiciones ni líneas divisorias (Maison Velour, Sable & Co., Casa Duvall, Ludovica, Regalia, Villa Serena) y subtítulo de Miel de Monte | Publicado |

Todas las piezas tienen foto 3D: camisetas, tote bags, gorras y delantales (tela con textura y pliegues), fachadas, vans, empaques flexibles, chocolate, paleta y la pieza digital (presentación en portátil y firma de correo en tableta). Los frascos son de vidrio real en Blender.

## Cómo está construido

### Sitio (Astro 5, español e inglés)
- `src/data/brand-showcase.json`: datos de las 36 marcas. Se **genera**; no se edita a mano.
- `src/data/brands.ts`: tipos, textos de la galería y el ayudante `mockFile()`, que usa la foto 3D si existe y si no la ilustración SVG.
- `src/components/BrandGallery.astro`, `BrandPage.astro`, `BrandCard.astro`: la galería, la página de cada marca y la tarjeta.
- `src/pages/[lang]/marcas/`: rutas.
- `src/data/catalog.ts`: mensajes de WhatsApp (`waMessages.brand`).
- `public/marcas/<slug>/`: SVG de logos, piezas y mockups, y las fotos `foto-<producto>.webp` de 1600×1200.

### Generador de marcas (Python): `tools/brand-showcase/`
Su `README.md` tiene el detalle. En resumen:
- `brands1.py` a `brands3.py` contienen 24 marcas y `brands4.py` las 12 de lujo. `ornaments.py` tiene los monogramas y ornamentos; `pair()` pone dos letras lado a lado sin superponerlas.
- El texto se convierte a trazos con HarfBuzz y fontTools usando fuentes libres (OFL/Apache) de Fontsource, así que los SVG no dependen de fuentes instaladas.
- `python3 fonts.py` (una vez), luego `python3 build.py [slug ...]`.

### Fotos 3D (sin servicios de IA): `tools/brand-showcase/render3d/`
- `art.py`: arte de impresión con las tipografías de cada marca (tarjetas, hoja membretada, etiquetas, latas, menús…).
- `studio.html`: 28 escenas en Three.js 0.169: tarjetas, taza, caja, bolsa, vaso, lata, frasco, envases cosméticos, papelería, afiche, menú, aviso de pared, celular, app, portátil, etiqueta colgante, tarjeta de pago, carnet con lanyard, camiseta, tote, gorra, delantal, empaque flexible, chocolate, paleta, fachada, van y pieza digital.
- `render.cjs`: render por lotes en Chromium sin ventana con supersampling 2×. Uso: `node render.cjs [slug | escena | slug/escena] [--force]`.
- `bottle_cycles.py` y `bottles.sh`: botellas de vino, cerveza y jugo (Orvieto, Casa Duvall, Páramo, Guayaba Club) y frascos de vidrio con crema, cera o miel (Alma Botánica, Sereno, Lino, Miel de Monte, La Navaja) en **Blender Cycles** (módulo `bpy`). `BOTTLES=0` o `JARS=0` omite un grupo.
- `publish.py`: convierte los PNG a WebP en `public/marcas/` y regenera el JSON.
- `sheet.py`: hoja de contactos para revisar los renders.
- Requisitos: Node.js, Python 3.11+, Pillow, Chromium/Playwright; `bpy` solo para las botellas. Un render tarda unos 10 a 50 s; una botella en Blender, 1 a 3 min.

### Verificación y despliegue
```sh
npm ci
npm run build
npm run test:demos   # incluye la galería de marcas: filtros, 5 páginas, WhatsApp, zoom, imágenes, axe (WCAG A/AA) y reflow
```
El workflow `.github/workflows/` corre lo mismo antes de publicar en Pages.

## Lecciones aprendidas sobre calidad visual

- **Nunca superponer letras en un monograma.** Los entrelazados se veían rotos: fragmentos sueltos y una línea fina en la unión. Usar `pair()` o composiciones sin cruces.
- **Revisar cada render con ojo de cliente** antes de publicar: encuadres cortados, brillos quemados, objetos flotando, logos estirados.
- **Ajustes del estudio 3D:** tono `NeutralToneMapping`, entorno bajo (0,22 a 0,32) para que no se vea lavado, sombras suaves VSM, supersampling 2× contra bordes pixelados y trazos del logo engrosados para que se lean.
- **Afiches y letreros** deben ir pegados a la pared, con su sombra. El dorado sobre cajas oscuras necesita un material más claro y menos metálico para que se lea.
- El lanyard se aprobó con esta composición de referencia: carnets flotando en distintas orientaciones, mosquetón real y textura de tela.

## Decisiones del cliente

- La colección de lujo va primero.
- Las imágenes **no** se generan con IA por ahora. Se probó Gemini por API: el plan gratuito tiene cuota 0 para imágenes y el cliente decidió no activar facturación. Tampoco quiere usar ElevenLabs.
- Los logos se hacen en vector, porque deben ser editables y escalables para entregarlos a un cliente.

## Próximos pasos sugeridos

1. Generación de imágenes con IA: queda pendiente; el cliente buscará otra opción. Si se retoma, usarla solo para mockups (el logo real como referencia), nunca para los logos.
2. Si se agregan marcas, revisar sus logos con la hoja de contactos (sin letras superpuestas) y renderizar sus mockups con `render.cjs <slug>`.
3. Posibles mejoras de las escenas 3D: ropa colgada en gancho (hoy es plegada), van con más detalle de carrocería y fachadas con variantes de material (ladrillo, madera).

## Convenciones del repositorio

- Commits y textos del sitio en español, con la versión en inglés en las páginas `/en/`.
- Antes de publicar, pasar `npm run build` y `npm run test:demos`.
- No tocar `src/data/brand-showcase.json` a mano: regenerarlo con `build.py` o `publish.py`.
