# Muestras interactivas de software

Las imágenes y los botones «Explorar demo» abren una página independiente para cada producto, en `/{idioma}/demos/{id}/`. El nombre del producto sigue abriendo su ficha comercial. Se conserva la invitación completa en su ruta existente. Las demos usan Astro y TypeScript; no arrancan servidores de producto ni importan sus bases de datos.

## Recorridos

| ID | Muestra | Interacciones |
| --- | --- | --- |
| `akashic-vault` | Reconstrucción visual independiente | Modos de chat, respuestas predefinidas, perfiles de modelo, historial y bóveda en memoria, bloqueo visual, estudio con imagen preparada y animación de video simulada, tema claro/oscuro. |
| `openmultipos` | Adaptación de la estructura y paleta del panel original | Dos negocios ficticios, filtros, inventario, clientes, cesta conjunta, descuento, cobro simulado, recibo desglosado por negocio e indicadores separados. Sin Frappe, SQLite, contabilidad o impresión. |
| `easy-drink` | Reconstrucción visual independiente | Panel con total por cobrar, caja, búsqueda/categorías, cantidades, descuento, pago ficticio o a crédito, inventario con unidades en bodega, recibo con logo, cuentas por cliente con abonos, saldo a favor y estado de cuenta, informes, copia en la nube simulada y acento visual. Sin IndexedDB, PWA, Capacitor, WhatsApp, nube ni dispositivos. |
| `akashic-tv` | Reconstrucción visual independiente | Catálogo local, películas/series, géneros/años, fichas, episodios, flechas del teclado, reproductor simulado con avance y ajustes. Sin proveedores, metadata remota, iframes ni películas. |
| `tasktone` | Portada adaptada y recorrido conceptual reconstruido | Roles de muestra, encargos, filtros, audio local preparado, propuesta/ejecución/revisión/aprobación, ajustes y comentarios en memoria. No implica que esas funciones estén implementadas en el backend del prototipo. |

Las etapas comerciales reales de los productos no cambian. Los importes, perfiles, operaciones y resultados de estas páginas son ficticios, no métricas ni pruebas de producción. Los audios anunciados por el selector de archivos de TaskTone tienen duración ilustrativa; la muestra audible es un recurso original breve y local, no un archivo de un cliente.

## Organización

- `src/data/catalog.ts`: rutas `interactiveDemos`, clasificación `demoKinds`, tipo `SoftwareDemoId` y función bilingüe `demoLabel`. La invitación conserva su etiqueta de sitio interactivo.
- `SoftwareDemo.astro`: documento independiente, salida al proyecto, idioma, reinicio, panel de accesibilidad, créditos y política de contenido. Las demos llevan `noindex, follow` y no se añaden al sitemap comercial.
- `src/components/demos/`: interfaces de Vault, negocios, TV y TaskTone. Las dos demos de negocios comparten estructura funcional y conservan identidades y navegación diferentes.
- `src/scripts/*-demo.ts` y `demo-core.ts`: estado por página, formularios locales, navegación por fragmentos, avisos, diálogos nativos y generación segura del DOM con `textContent`.
- `src/data/business-demo.ts` y `tv-demo.ts`: fixtures de catálogo y clientes, con traducciones. `software-demos.css` contiene los estilos aislados del portafolio.

Para cambiar los recorridos, modifica la interfaz y su script correspondiente. Para sumar una demo, añade su ruta/clasificación, componente y datos bilingües. Las categorías del portafolio se siguen configurando por separado; añadir una categoría no inventa una nueva demo.

## Aislamiento y privacidad

El estado de ventas, conversaciones, comentarios, temas de producto y encargos permanece únicamente en memoria. Recargar o pulsar «Reiniciar demo» restaura las muestras. No se usan cookies, IndexedDB, localStorage ni sessionStorage para información introducida; solo se guardan preferencias generales de accesibilidad en `sd-tech-accessibility-v1`.

Los scripts no contienen fetch, XHR, beacons, WebSockets ni SDK de producto. En producción, CSP bloquea conexiones, iframes y envío de formularios. Los recursos visuales y el audio son locales. Sin JavaScript los botones de envío permanecen deshabilitados. No hay registro/login ni campos de contraseñas, claves, tarjetas, fotos o carga de archivos.

No se modifican los repositorios originales. Las reconstrucciones de los dos productos privados no publican sus fuentes operativas, configuraciones, claves o URLs de proveedores. Atribuciones y licencias: `public/demos/ATTRIBUTIONS.txt` y `public/licenses/`.

## Verificación reproducible

```sh
npm ci
npx playwright install chromium
PAGES_BASE=/portfolio/ npm run build
npm run test:demos
```

El test inicia un preview temporal si no se define `DEMO_TEST_BASE`. Puede usar Chromium del sistema (`/usr/bin/chromium`) o `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`. Con `DEMO_SCREENSHOT_DIR` genera capturas fuera del sitio. `DEMO_TEST_IDS` y `DEMO_TEST_LANGS` restringen temporalmente una revisión.

Se prueban los recorridos ES/EN, validación y cancelación, entradas tratadas como texto, aislamiento de almacenamiento/red, reinicio, navegación por imagen/botón/idioma, diálogos, teclado, contraste mediante axe-core y reflow con texto al 150 % en cuatro anchos. La comprobación automática complementa la inspección visual; no constituye una certificación.
