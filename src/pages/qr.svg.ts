// QR en vectores para imprimir a cualquier tamaño: /qr.svg (ver lib/qr.ts).
import { qrSvg } from '../lib/qr';

export const GET = async () =>
  new Response(await qrSvg(), { headers: { 'Content-Type': 'image/svg+xml' } });
