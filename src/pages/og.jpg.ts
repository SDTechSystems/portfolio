// Imagen de vista previa al compartir el enlace (og:image, 1200×630), generada al compilar con
// las portadas de los 3 destacados (tienda.ts → destacados), armadas como el tablero:
// la primera grande a la izquierda y las otras dos apiladas a la derecha, sobre el gris del suelo.
// Sin texto: WhatsApp ya muestra el nombre y la descripción junto a la imagen.
// JPEG y no PNG: WhatsApp no muestra imágenes de vista previa de más de ~300 KB.
import sharp from 'sharp';
import { destacados } from '../lib/catalogo';

const ANCHO = 1200, ALTO = 630, MARGEN = 16, SEPARACION = 12, RADIO = 12;
const SUELO = '#e9e9ec', SIN_PORTADA = '#d6d6dc'; // tokens --suelo y fondo de .img

// Celdas: [x, y, ancho, alto]
// 60/40 como el tablero de escritorio: las celdas de la derecha quedan cerca de 16:9 y no cortan los logos.
const derecha = Math.round((ANCHO - 2 * MARGEN - SEPARACION) * 0.4);
const izquierda = ANCHO - 2 * MARGEN - SEPARACION - derecha;
const altoCompleto = ALTO - 2 * MARGEN;
const altoMitad = (altoCompleto - SEPARACION) / 2;
const xDerecha = MARGEN + izquierda + SEPARACION;
const celdas = [
  [MARGEN, MARGEN, izquierda, altoCompleto],
  [xDerecha, MARGEN, derecha, Math.floor(altoMitad)],
  [xDerecha, MARGEN + Math.ceil(altoMitad) + SEPARACION, derecha, Math.floor(altoMitad)],
];

const esquinas = (w: number, h: number) =>
  Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="${w}" height="${h}" rx="${RADIO}"/></svg>`);

async function mosaico(archivo: string | undefined, w: number, h: number) {
  const base = archivo
    ? sharp(archivo).resize(w, h, { fit: 'cover' })
    : sharp({ create: { width: w, height: h, channels: 3, background: SIN_PORTADA } });
  return base.ensureAlpha().composite([{ input: esquinas(w, h), blend: 'dest-in' }]).png().toBuffer();
}

export async function GET() {
  const capas = await Promise.all(
    celdas.map(async ([x, y, w, h], i) => ({ input: await mosaico(destacados[i]?.archivo, w, h), left: x, top: y })),
  );
  const jpg = await sharp({ create: { width: ANCHO, height: ALTO, channels: 3, background: SUELO } })
    .composite(capas)
    .jpeg({ quality: 82, mozjpeg: true })
    .toBuffer();
  return new Response(new Uint8Array(jpg), { headers: { 'Content-Type': 'image/jpeg' } });
}
