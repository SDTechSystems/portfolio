// Brand design showcase. Generated content lives in brand-showcase.json
// (tools/brand-showcase/build.py writes it together with the SVGs in public/marcas/).
import showcase from './brand-showcase.json';
import type { Locale } from './catalog';

export type Brand = (typeof showcase.brands)[number] & {
  editorial?: { file: string; small: string; label: Record<Locale, string> };
  mascot?: { name: string; description: Record<Locale, string> };
};
export const brands: Brand[] = showcase.brands;
export const brandStyles = showcase.styles;
export const styleLabel = (id: string, locale: Locale) => brandStyles.find(s => s.id === id)?.label[locale] ?? id;

export const featuredBrands = brands.slice(0, 6);

export const brandAsset = (base: string, slug: string, file: string) => `${base}marcas/${slug}/${file}`;

export const versionLabels: Record<string, Record<Locale, string>> = {
  horizontal: { es: 'Principal', en: 'Primary' },
  vertical: { es: 'Vertical', en: 'Stacked' },
  simbolo: { es: 'Símbolo', en: 'Symbol' },
  inversa: { es: 'Inversa', en: 'Reversed' },
  negro: { es: 'Una tinta negra', en: 'One color black' },
  blanco: { es: 'Una tinta blanca', en: 'One color white' },
};

export const kitPieces = [
  { file: 'perfil.svg', w: 1080, h: 1080, label: { es: 'Imagen de perfil', en: 'Profile image' } },
  { file: 'banner-portada.svg', w: 1640, h: 624, label: { es: 'Portada de Facebook', en: 'Facebook cover' } },
  { file: 'post-lanzamiento.svg', w: 1080, h: 1350, label: { es: 'Publicación de lanzamiento', en: 'Launch post' } },
  { file: 'sticker-logo.svg', w: 1200, h: 1200, label: { es: 'Sticker con logo', en: 'Logo sticker' } },
  { file: 'sticker-simbolo.svg', w: 1200, h: 1200, label: { es: 'Sticker troquelado', en: 'Die-cut sticker' } },
  { file: 'sticker-frase.svg', w: 1200, h: 1200, label: { es: 'Sticker con frase', en: 'Slogan sticker' } },
];

export const misuses = [
  { file: 'no-deformar.svg', label: { es: 'No deformar ni estirar', en: 'Do not stretch or distort' } },
  { file: 'no-rotar.svg', label: { es: 'No rotar', en: 'Do not rotate' } },
  { file: 'no-colores.svg', label: { es: 'No cambiar los colores', en: 'Do not change the colors' } },
  { file: 'no-contraste.svg', label: { es: 'No usar sobre fondos sin contraste', en: 'Do not use on low-contrast backgrounds' } },
];

// What a client receives. Mirrors the standard package; corporate identity is quoted separately.
export const packageItems: Record<Locale, string[]> = {
  es: [
    '2 propuestas de logo y desarrollo de la elegida',
    'Hasta 2 rondas de ajustes',
    'Logo principal, vertical, símbolo, versión inversa y a una tinta',
    'Paleta de color con HEX, RGB y CMYK',
    'Tipografías con licencia libre para uso comercial',
    'Mini guía de marca en PDF',
    'Imagen de perfil, 2 banners y 3 stickers',
    'Archivos PNG transparentes y SVG, entregados en ZIP',
  ],
  en: [
    '2 logo proposals and development of the chosen one',
    'Up to 2 revision rounds',
    'Primary, stacked, symbol, reversed and one-color logos',
    'Color palette with HEX, RGB and CMYK',
    'Typefaces licensed for free commercial use',
    'Mini brand guide in PDF',
    'Profile image, 2 banners and 3 stickers',
    'Transparent PNG and SVG files delivered in a ZIP',
  ],
};

export const corporateItems: Record<Locale, string[]> = {
  es: ['Tarjetas de presentación', 'Hoja membretada y sobre', 'Firma de correo', 'Plantilla de presentación', 'Carné, uniforme y señalética', 'Empaques, etiquetas y avisos'],
  en: ['Business cards', 'Letterhead and envelope', 'Email signature', 'Presentation template', 'ID badge, uniforms and signage', 'Packaging, labels and signs'],
};

export const zipTree = (name: string) => [
  `${name.replace(/\s+/g, '_')}_Kit_de_Marca/`,
  '  01_Logotipos/  SVG · PNG transparente · PNG con fondo',
  '  02_Colores/  Paleta.png · Paleta.txt · colores.css',
  '  03_Tipografias/  Tipografias.txt',
  '  04_Redes_sociales/  perfil · portada · publicación',
  '  05_Guia_de_marca/  Guía de marca.pdf',
  '  06_Stickers/',
  '  LEEME.txt',
];
