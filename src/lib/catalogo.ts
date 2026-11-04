import { precioVenta } from './precio-venta';
import type { ImageMetadata } from 'astro';
import datos from '../assets/Catalogo_Nintendo_Switch_Colombia/productos.json';
import { tienda } from '../data/tienda';
import { validarCatalogo } from './datos-catalogo';

export type Tipo = 'Juego' | 'DLC' | 'Update' | 'Mejora';
export type Consola = 'Switch 1' | 'Switch 2';
export type Recorte = 'arriba' | 'centro' | 'abajo' | 'izquierda' | 'derecha';
export interface Producto {
  id: string;
  nombre: string;
  /** null = sin precio: se muestra "Consultar" y no se puede sumar al pedido. */
  precio: number | null;
  tipo: Tipo;
  consola: Consola;
  /** Requisito extra para jugar (ej. "Necesita Ring-Con"); se muestra bajo el nombre. */
  nota?: string;
  imagen?: ImageMetadata;
  /** Ruta del archivo de la portada en el disco (la usa pages/og.jpg.ts). */
  archivo?: string;
  /** Qué parte de la portada se conserva cuando el mosaico la recorta más ancha (juego con versiones). */
  recorte?: Recorte;
  /** Filas con el mismo grupo (un juego con versión de Switch 1, de Switch 2 y paquete de mejora) van en un mosaico. */
  grupo?: string;
}

/** Un mosaico del tablero: un juego con una o varias versiones (cada una con su precio y su "+"). */
export interface Ficha {
  id: string;
  nombre: string;
  tipo: Tipo;
  nota?: string;
  imagen?: ImageMetadata;
  archivo?: string;
  recorte?: Recorte;
  /** Edición del precio "desde": el juego completo más barato con precio (el paquete de mejora no cuenta). */
  desde?: Producto;
  /** En orden: Switch 1, Switch 2, paquete de mejora. Con una sola versión, el mosaico es como siempre. */
  versiones: Producto[];
}

// Portadas: Astro las optimiza (tamaño y formato) al compilar.
const portadas = import.meta.glob<{ default: ImageMetadata }>(
  '../assets/Catalogo_Nintendo_Switch_Colombia/imagenes/*.{webp,jpg,jpeg,png}',
  { eager: true },
);

const CARPETA = 'Catalogo_Nintendo_Switch_Colombia';
const ruta = (r: string) => `../assets/${CARPETA}/${r}`;
const filas = validarCatalogo(datos, tienda, (r) => !!portadas[ruta(r)]);

const tapa = (img?: { ruta: string; recorte?: string }) => img && {
  imagen: portadas[ruta(img.ruta)]?.default,
  archivo: `src/assets/${CARPETA}/${img.ruta}`,
  recorte: img.recorte as Recorte | undefined,
};
// Portadas generales de grupo (opcionales, ya validadas): productos.json → "grupos".
const portadasGrupo = (datos as { grupos?: Record<string, { imagen: { ruta: string; recorte?: string } }> }).grupos ?? {};

const productos: Producto[] = filas.map((f) => ({
  id: f.id,
  nombre: f.titulo,
  precio: precioVenta(f),
  tipo: f.tipo_producto === 'dlc' ? 'DLC' : f.tipo_producto === 'update' ? 'Update' : f.tipo_producto === 'paquete_mejora' ? 'Mejora' : 'Juego',
  consola: f.plataforma === 'Nintendo Switch 2' ? 'Switch 2' : 'Switch 1',
  nota: f.tipo_producto === 'juego_con_accesorios' ? 'Necesita Ring-Con' : undefined,
  ...tapa(f.imagen),
  grupo: f.grupo,
}));

// Un mosaico por juego, en el lugar de la primera fila de su grupo. Nombre y nota: los del juego de
// Switch 1. Portada: la general del grupo si la hay; si no, la de la edición del precio "desde" (si esa
// edición no tiene imagen, queda gris: la portada de otra edición haría pensar que cuesta eso).
const orden = (p: Producto) => (p.tipo === 'Mejora' ? 2 : p.consola === 'Switch 2' ? 1 : 0);
const fichas: Ficha[] = [];
productos.forEach((p) => {
  if (p.grupo && fichas.some((f) => f.versiones.some((v) => v.grupo === p.grupo))) return;
  const versiones = p.grupo ? productos.filter((v) => v.grupo === p.grupo).sort((a, b) => orden(a) - orden(b)) : [p];
  const base = versiones[0];
  const desde = versiones.filter((v) => v.tipo !== 'Mejora' && v.precio !== null).sort((a, b) => a.precio! - b.precio!)[0];
  const portada = (p.grupo && tapa(portadasGrupo[p.grupo]?.imagen)) || (desde ?? base);
  fichas.push({ id: base.id, nombre: base.nombre, tipo: base.tipo, nota: base.nota, imagen: portada.imagen, archivo: portada.archivo, recorte: portada.recorte, desde, versiones });
});
const fichaDe = (id: string) => fichas.find((f) => f.versiones.some((v) => v.id === id));

// Un destacado puede nombrar cualquier versión del juego: se destaca el mosaico entero.
export const destacados = tienda.destacados.map(fichaDe).filter((f): f is Ficha => !!f);

/** Bloques bajo los destacados. La consola la marca la pestaña de cada mosaico, así que los juegos
 *  van juntos y sin título; un juego con versión para cada consola es un mosaico con un precio por versión. */
export interface Seccion { titulo?: string; fichas: Ficha[]; mas: string; mensaje: string }
const resto = fichas.filter((f) => !destacados.includes(f));
export const secciones: Seccion[] = [
  { fichas: resto.filter((f) => f.tipo === 'Juego'), mas: '¿No ves tu juego?', mensaje: 'Hola, busco un juego' },
  { titulo: 'DLC y updates', fichas: tienda.mostrarDlcUpdates ? resto.filter((f) => f.tipo !== 'Juego') : [], mas: '¿Buscas otro DLC?', mensaje: 'Hola, busco un DLC' },
].filter((s) => s.fichas.length > 0);

const fmt = new Intl.NumberFormat(tienda.locale, { style: 'currency', currency: tienda.moneda, maximumFractionDigits: 0 });
export const precio = (n: number | null) => (n === null ? 'Consultar' : fmt.format(n));

const detalle = (p: Producto) => (p.tipo === 'Mejora' ? 'Paquete de mejora a Switch 2' : `${p.tipo} · ${p.consola}`);

export const whatsapp = (texto: string) => `https://wa.me/${tienda.whatsapp}?text=${encodeURIComponent(texto)}`;
const linkWhatsApp = (p: Producto) =>
  whatsapp(p.precio === null
    ? `Hola, quiero saber el precio de ${p.nombre} (${detalle(p)})`
    : `Hola, quiero ${p.nombre} (${detalle(p)}) a ${precio(p.precio)}`);

/** Atributos para que un elemento se pueda sumar al pedido (ver components/Pedido.astro).
 *  Sin precio, el mosaico solo abre su propio WhatsApp para consultar. */
export const item = (p: Producto) =>
  p.precio === null
    ? { href: linkWhatsApp(p), target: '_blank', rel: 'noopener' }
    : { href: linkWhatsApp(p), 'data-item': p.id, 'data-nombre': p.nombre, 'data-precio': p.precio, 'data-detalle': detalle(p) };
