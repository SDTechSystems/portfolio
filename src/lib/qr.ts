// Código QR de la tienda para carteles, empaques y estados de WhatsApp.
// Apunta a tienda.url; si está vacía, al chat de WhatsApp de la tienda, para que el QR siempre sirva.
// Se genera al compilar: si cambia el dominio en tienda.ts, el QR se actualiza solo.
import QRCode from 'qrcode';
import { tienda } from '../data/tienda';

export const destinoQr = () => tienda.url.trim() || `https://wa.me/${tienda.whatsapp}`;

// Negro sobre blanco y margen de 4 módulos: lo que piden las cámaras para leerlo sin fallar.
// Corrección "M" (15 %): aguanta manchas o dobleces de un cartel impreso sin agrandar mucho el código.
export const opcionesQr = {
  errorCorrectionLevel: 'M',
  margin: 4,
  color: { dark: '#000000', light: '#ffffff' },
} as const;

export const qrSvg = () => QRCode.toString(destinoQr(), { ...opcionesQr, type: 'svg' });

// 1024 px: nítido impreso hasta ~8 cm a 300 ppp y liviano para mandarlo por chat.
export const qrPng = () => QRCode.toBuffer(destinoQr(), { ...opcionesQr, type: 'png', width: 1024 });
