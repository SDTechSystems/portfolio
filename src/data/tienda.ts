// Datos de la tienda: cambia aquí nombre, WhatsApp y formato de precio.
export const tienda = {
  nombre: 'SD Tech Import',
  // Número de WhatsApp Business con código de país, solo dígitos (Colombia: 57 + 10 dígitos).
  whatsapp: '573058147293',
  // Dirección pública donde se publica el sitio, con https:// (ej. 'https://tutienda.pages.dev').
  url: 'https://catalogo-juegos-sdtechimports.sdtechsystems.dev',
  moneda: 'COP',
  locale: 'es-CO',
  // Ids de productos.json que van arriba en grande, en orden: el primero es el más grande.
  destacados: ['the-legend-of-zelda-ocarina-of-time', 'super-mario-bros-wonder', 'the-legend-of-zelda-tears-of-the-kingdom'],
  // Sección "DLC y updates": false = oculta aunque productos.json tenga DLC o updates.
  mostrarDlcUpdates: false,
};
