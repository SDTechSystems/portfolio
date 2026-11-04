import type { ImageMetadata } from 'astro';
import datos from '../assets/Catalogo_Nintendo_Switch_Colombia/productos.json';
import { tienda } from '../data/tienda';

export type Tipo = 'juego' | 'dlc' | 'update';
export type Consola = 'switch1' | 'switch2';
export interface Producto {
  id: string;
  nombre: string;
  /** null = sin precio: se muestra "Consultar" y no se puede sumar al pedido. */
  precio: number | null;
  tipo: Tipo;
  consolas: Consola[];
  /** Aviso corto bajo la consola (ej. "Necesita Ring-Con"). */
  nota?: string;
  estreno: boolean;
  imagen?: ImageMetadata;
  color?: string;
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
const portada = (ruta?: string) =>
  ruta ? portadas[`../assets/Catalogo_Nintendo_Switch_Colombia/${ruta}`]?.default : undefined;

const consolasDe = (plataforma: string): Consola[] =>
  plataforma === 'Nintendo Switch 2' ? ['switch2'] : ['switch1'];

const tipoDe = (t: string): Tipo => (t === 'dlc' ? 'dlc' : t === 'update' ? 'update' : 'juego');

export const productos: Producto[] = (datos.productos as Fila[]).map((f) => ({
  id: f.id,
  nombre: f.titulo,
  precio: f.precio_venta_cop ?? f.precio_referencia_eshop_colombia_cop ?? null,
  tipo: tipoDe(f.tipo_producto),
  consolas: consolasDe(f.plataforma),
  nota: f.tipo_producto === 'juego_con_accesorios' ? 'Necesita Ring-Con' : undefined,
  estreno: tienda.estrenos.includes(f.id),
  imagen: portada(f.imagen?.ruta),
}));

export const estrenos = tienda.estrenos
  .map((id) => productos.find((p) => p.id === id))
  .filter((p): p is Producto => !!p);
export const porTipo = (t: Tipo) => productos.filter((p) => p.tipo === t);

const fmt = new Intl.NumberFormat(tienda.locale, {
  style: 'currency',
  currency: tienda.moneda,
  maximumFractionDigits: 0,
});
export const precio = (n: number | null) => (n === null ? 'Consultar' : fmt.format(n));

export const etiquetaTipo: Record<Tipo, string> = { juego: 'Juego', dlc: 'DLC', update: 'Update' };
export const etiquetaConsola = (c: Consola[]) =>
  c.length === 2 ? 'Switch 1 y 2' : c[0] === 'switch2' ? 'Switch 2' : 'Switch 1';

export const linkWhatsApp = (p?: Producto) => {
  const texto = !p
    ? 'Hola, quiero información del catálogo'
    : p.precio === null
      ? `Hola, quiero saber el precio de ${p.nombre} (${detalle(p)})`
      : `Hola, quiero ${p.nombre} (${etiquetaTipo[p.tipo]}, ${etiquetaConsola(p.consolas)}) a ${precio(p.precio)}`;
  return `https://wa.me/${tienda.whatsapp}?text=${encodeURIComponent(texto)}`;
};

export const detalle = (p: Producto) => `${etiquetaTipo[p.tipo]} · ${etiquetaConsola(p.consolas)}`;

/** Atributos para que un elemento se pueda sumar al pedido (ver components/Pedido.astro).
 *  Sin precio, el mosaico solo abre su propio WhatsApp para consultar. */
export const item = (p: Producto) =>
  p.precio === null
    ? { href: linkWhatsApp(p), target: '_blank', rel: 'noopener' }
    : {
        href: linkWhatsApp(p),
        'data-item': p.id,
        'data-nombre': p.nombre,
        'data-precio': p.precio,
        'data-detalle': detalle(p),
      };
