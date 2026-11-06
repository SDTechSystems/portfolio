// Búsqueda del catálogo: sin tildes ni mayúsculas, y cada palabra escrita debe aparecer.
export const normalizar = (texto: string) =>
  texto.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().replace(/\s+/g, ' ').trim();

/** `indice` ya normalizado (data-buscar); `consulta`, lo que escribió el cliente. */
export const coincide = (indice: string, consulta: string) =>
  normalizar(consulta).split(' ').every((palabra) => indice.includes(palabra));
