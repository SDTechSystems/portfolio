// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import { tienda } from './src/data/tienda.ts';

// Se revisa aquí y no en lib/catalogo.ts porque Astro lee `site` antes que todo lo demás.
if (tienda.url && !/^https:\/\/[^/\s]+\.[^/\s]+\/?$/.test(tienda.url)) {
  throw new Error(`Revisa el catálogo:\n- tienda.ts: "url" es "${tienda.url}"; debe ser la dirección del sitio con https:// y sin ruta (ej. "https://tutienda.pages.dev").`);
}

// https://astro.build/config
export default defineConfig({
  // Dirección pública del sitio (tienda.ts → url). Hace falta para la imagen de vista previa al compartir.
  site: tienda.url || undefined,
  // Tipografía del portafolio de SD Tech: DejaVu Sans y DejaVu Sans Mono (licencia libre de Bitstream Vera
  // y dominio público), servidas desde el propio sitio. Recortadas a latín (á, é, ñ, ¿, ¡, ✓) en woff2.
  // La regular sirve el peso 500 del diseño y la negrita el 800 (docs/diseno.md §2).
  fonts: [
    {
      provider: fontProviders.local(),
      name: 'SD Sans',
      cssVariable: '--fuente',
      fallbacks: ['system-ui', 'sans-serif'],
      options: {
        variants: [
          { weight: 400, style: 'normal', src: ['./src/assets/marca/sd-sans.woff2'] },
          { weight: 700, style: 'normal', src: ['./src/assets/marca/sd-sans-bold.woff2'] },
        ],
      },
    },
    {
      provider: fontProviders.local(),
      name: 'SD Mono',
      cssVariable: '--mono',
      fallbacks: ['ui-monospace', 'monospace'],
      options: { variants: [{ weight: 400, style: 'normal', src: ['./src/assets/marca/sd-mono.woff2'] }] },
    },
  ],
});
