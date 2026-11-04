import type { ImageMetadata } from 'astro';
import datos from '../assets/Catalogo_Nintendo_Switch_Colombia/productos.json';
import { tienda } from '../data/tienda';

export type Tipo = 'Juego' | 'DLC' | 'Update';
export type Consola = 'Switch 1' | 'Switch 2';
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
}

/** Forma de cada entrada en productos.json (lo que edita el dueño). */
interface Fila {
  id: string;
  titulo: string;
  plataforma: string;
  tipo_producto: string;
  /** Opcional: precio de venta propio. Si no está, se usa el de referencia de la eShop. */
  precio_venta_cop?: number | null;
  precio_referencia_eshop_colombia_cop: number | null;
  imagen?: { ruta: string };
}

// Portadas: Astro las optimiza (tamaño y formato) al compilar.
const portadas = import.meta.glob<{ default: ImageMetadata }>(
  '../assets/Catalogo_Nintendo_Switch_Colombia/imagenes/*.{webp,jpg,jpeg,png}',
  { eager: true },
);

const productos: Producto[] = (datos.productos as Fila[]).map((f) => ({
  id: f.id,
  nombre: f.titulo,
  precio: f.precio_venta_cop ?? f.precio_referencia_eshop_colombia_cop ?? null,
  tipo: f.tipo_producto === 'dlc' ? 'DLC' : f.tipo_producto === 'update' ? 'Update' : 'Juego',
  consola: f.plataforma === 'Nintendo Switch 2' ? 'Switch 2' : 'Switch 1',
  nota: f.tipo_producto === 'juego_con_accesorios' ? 'Necesita Ring-Con' : undefined,
  imagen: f.imagen && portadas[`../assets/Catalogo_Nintendo_Switch_Colombia/${f.imagen.ruta}`]?.default,
}));

export const destacados = tienda.destacados
  .map((id) => productos.find((p) => p.id === id))
  .filter((p): p is Producto => !!p);

/** Secciones bajo los destacados. `consola`: la sección ya la dice, así que sus mosaicos no la repiten.
 *  Un juego con versión para cada consola aparece en las dos secciones, cada una con su precio. */
export interface Seccion { titulo: string; consola?: Consola; productos: Producto[]; mas: string; mensaje: string }
const resto = productos.filter((p) => !tienda.destacados.includes(p.id));
const juegosDe = (c: Consola) => resto.filter((p) => p.tipo === 'Juego' && p.consola === c);
export const secciones: Seccion[] = [
  { titulo: 'Switch 2', consola: 'Switch 2' as const, productos: juegosDe('Switch 2'), mas: '¿No ves tu juego?', mensaje: 'Hola, busco un juego de Switch 2' },
  { titulo: 'Switch 1', consola: 'Switch 1' as const, productos: juegosDe('Switch 1'), mas: '¿No ves tu juego?', mensaje: 'Hola, busco un juego de Switch 1' },
  { titulo: 'DLC y updates', productos: tienda.mostrarDlcUpdates ? resto.filter((p) => p.tipo !== 'Juego') : [], mas: '¿Buscas otro DLC?', mensaje: 'Hola, busco un DLC' },
].filter((s) => s.productos.length > 0);

const fmt = new Intl.NumberFormat(tienda.locale, { style: 'currency', currency: tienda.moneda, maximumFractionDigits: 0 });
export const precio = (n: number | null) => (n === null ? 'Consultar' : fmt.format(n));

const detalle = (p: Producto) => `${p.tipo} · ${p.consola}`;

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
