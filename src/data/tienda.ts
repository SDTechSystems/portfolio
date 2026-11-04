// Datos de la tienda: cambia aquí nombre, WhatsApp y formato de precio.
export const tienda = {
  nombre: 'Tu Tienda',
  // Número con código de país, solo dígitos (Colombia: 57 + 10 dígitos). PENDIENTE: número real.
  whatsapp: '573001234567',
  // Dirección pública donde se publica el sitio, con https:// (ej. 'https://tutienda.pages.dev').
  // Hasta tenerla, el enlace compartido no muestra la imagen de vista previa. PENDIENTE (D4).
  url: '',
  moneda: 'COP',
  locale: 'es-CO',
  // Ids de productos.json que van arriba en grande, en orden: el primero es el más grande.
  destacados: ['mario-kart-world', 'super-mario-bros-wonder', 'the-legend-of-zelda-tears-of-the-kingdom'],
  // Sección "DLC y updates": false = oculta aunque productos.json tenga DLC o updates.
  mostrarDlcUpdates: false,
};
