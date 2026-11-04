// QR en imagen de 1024 px para mandar por chat o pegar en un diseño: /qr.png (ver lib/qr.ts).
import { qrPng } from '../lib/qr';

export const GET = async () =>
  new Response(new Uint8Array(await qrPng()), { headers: { 'Content-Type': 'image/png' } });
