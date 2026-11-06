// Imagen de vista previa al compartir el enlace (og:image, 1200×630), generada al compilar con
// las portadas de los 3 destacados (tienda.ts → destacados), armadas como el tablero:
// la primera a todo el ancho (portada de cine) y las otras dos debajo, lado a lado, sobre el suelo oscuro.
// Sin texto: WhatsApp ya muestra el nombre y la descripción junto a la imagen.
// JPEG y no PNG: WhatsApp no muestra imágenes de vista previa de más de ~300 KB.
import sharp from 'sharp';
import { destacados } from '../lib/catalogo';

const ANCHO = 1200, ALTO = 630, MARGEN = 16, SEPARACION = 12, RADIO = 12;
const SUELO = '#0e0e10', SIN_PORTADA = '#26262c'; // tokens --suelo y fondo de .img

// Celdas: [x, y, ancho, alto]
// Portada de cine arriba (3,2:1): con el recorte centrado conserva el 56 % central del alto, donde va el
// logo de las portadas (el de Ocarina ocupa del 19 al 73 %). Abajo, dos de 2,7:1 lado a lado.
const anchoCompleto = ANCHO - 2 * MARGEN;
const altoCine = 370;
const altoAbajo = ALTO - 2 * MARGEN - SEPARACION - altoCine;
const anchoMitad = (anchoCompleto - SEPARACION) / 2;
const yAbajo = MARGEN + altoCine + SEPARACION;
const celdas = [
  [MARGEN, MARGEN, anchoCompleto, altoCine],
  [MARGEN, yAbajo, anchoMitad, altoAbajo],
  [MARGEN + anchoMitad + SEPARACION, yAbajo, anchoMitad, altoAbajo],
];

const esquinas = (w: number, h: number) =>
  Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><rect width="${w}" height="${h}" rx="${RADIO}"/></svg>`);

// Mismo encuadre que Mosaico.astro: el `recorte` del JSON o, en juegos con versiones, abajo (franja de Switch 2 Edition).
const POSICION = { arriba: 'top', centro: 'centre', abajo: 'bottom', izquierda: 'left', derecha: 'right' } as const;

async function mosaico(f: (typeof destacados)[number] | undefined, w: number, h: number) {
  const posicion = f?.recorte ? POSICION[f.recorte] : f && f.versiones.length > 1 ? 'bottom' : 'centre';
  const base = f?.archivo
    ? sharp(f.archivo).resize(w, h, { fit: 'cover', position: posicion })
    : sharp({ create: { width: w, height: h, channels: 3, background: SIN_PORTADA } });
  return base.ensureAlpha().composite([{ input: esquinas(w, h), blend: 'dest-in' }]).png().toBuffer();
}

export async function GET() {
  const capas = await Promise.all(
    celdas.map(async ([x, y, w, h], i) => ({ input: await mosaico(destacados[i], w, h), left: x, top: y })),
  );
  const jpg = await sharp({ create: { width: ANCHO, height: ALTO, channels: 3, background: SUELO } })
    .composite(capas)
    .jpeg({ quality: 82, mozjpeg: true })
    .toBuffer();
  return new Response(new Uint8Array(jpg), { headers: { 'Content-Type': 'image/jpeg' } });
}
