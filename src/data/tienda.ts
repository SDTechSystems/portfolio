// Datos de la tienda: cambia aquí nombre, WhatsApp y formato de precio.
export const tienda = {
  nombre: 'Tu Tienda',
  eslogan: 'Códigos digitales de juegos',
  // Número con código de país, solo dígitos (Colombia: 57 + 10 dígitos). PENDIENTE: número real.
  whatsapp: '573001234567',
  moneda: 'COP',
  locale: 'es-CO',
  beneficios: ['Código oficial', 'Actívalo en tu propia cuenta', 'Sin riesgo de baneos'],
  // Sección "DLC y updates": false = oculta aunque productos.json tenga DLC o updates.
  // Cámbialo a true cuando el contenido esté listo.
  mostrarDlcUpdates: false,
  // Ids de productos.json que van en "Estrenos", en orden: el primero es la portada grande.
  estrenos: ['mario-kart-world', 'super-mario-bros-wonder', 'the-legend-of-zelda-tears-of-the-kingdom'],
};
