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
  // La fuente se sirve desde el propio sitio, tomada del paquete npm @fontsource/schibsted-grotesk
  // (licencia OFL). No depende de Google ni al compilar ni en cada visita.
  // Solo el subconjunto "latin" (incluye á, é, ñ, ¿, ¡) y los dos pesos del diseño (docs/diseno.md §2).
  fonts: [{
    provider: fontProviders.local(),
    name: 'Schibsted Grotesk',
    cssVariable: '--fuente',
    fallbacks: ['system-ui', 'sans-serif'],
    options: {
      variants: [500, 800].map((weight) => ({
        weight,
        style: 'normal',
        src: [`@fontsource/schibsted-grotesk/files/schibsted-grotesk-latin-${weight}-normal.woff2`],
      })),
    },
  }],
});
