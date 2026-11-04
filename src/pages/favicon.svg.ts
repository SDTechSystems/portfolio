// Ícono de la pestaña del navegador: la inicial de la tienda en blanco sobre el rojo del diseño.
// Se genera al compilar desde tienda.nombre, así que cambia solo cuando cambia el nombre.
import { tienda } from '../data/tienda';

const inicial = (tienda.nombre.trim()[0] ?? '·').toUpperCase().replace(/[<>&"']/g, '');

export const GET = () =>
  new Response(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#e60012"/><text x="32" y="45" text-anchor="middle" font-family="system-ui, sans-serif" font-size="40" font-weight="800" fill="#fff">${inicial}</text></svg>`,
    { headers: { 'Content-Type': 'image/svg+xml' } },
  );
