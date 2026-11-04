import type { ImageMetadata } from 'astro';
import datos from '../assets/Catalogo_Nintendo_Switch_Colombia/productos.json';
import { tienda } from '../data/tienda';

export type Tipo = 'Juego' | 'DLC' | 'Update';
export interface Producto {
  id: string;
  nombre: string;
  /** null = sin precio: se muestra "Consultar" y no se puede sumar al pedido. */
  precio: number | null;
  tipo: Tipo;
  consola: 'Switch 1' | 'Switch 2';
  /** Lo único que el cliente debe saber antes de comprar; se muestra bajo el nombre. */
  aviso?: string;
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

const productos: Producto[] = (datos.productos as Fila[]).map((f) => {
  const consola = f.plataforma === 'Nintendo Switch 2' ? 'Switch 2' : 'Switch 1';
  return {
    id: f.id,
    nombre: f.titulo,
    precio: f.precio_venta_cop ?? f.precio_referencia_eshop_colombia_cop ?? null,
    tipo: f.tipo_producto === 'dlc' ? 'DLC' : f.tipo_producto === 'update' ? 'Update' : 'Juego',
    consola,
    // "Switch 1" no se escribe: es lo normal y también corre en Switch 2.
    aviso: f.tipo_producto === 'juego_con_accesorios' ? 'Necesita Ring-Con' : consola === 'Switch 2' ? 'Switch 2' : undefined,
    imagen: f.imagen && portadas[`../assets/Catalogo_Nintendo_Switch_Colombia/${f.imagen.ruta}`]?.default,
  };
});

export const destacados = tienda.destacados
  .map((id) => productos.find((p) => p.id === id))
  .filter((p): p is Producto => !!p);
export const juegos = productos.filter((p) => p.tipo === 'Juego' && !tienda.destacados.includes(p.id));
export const extras = tienda.mostrarDlcUpdates ? productos.filter((p) => p.tipo !== 'Juego') : [];

const fmt = new Intl.NumberFormat(tienda.locale, { style: 'currency', currency: tienda.moneda, maximumFractionDigits: 0 });
export const precio = (n: number | null) => (n === null ? 'Consultar' : fmt.format(n));

const detalle = (p: Producto) => `${p.tipo} · ${p.consola}`;

export const linkWhatsApp = (p?: Producto) => {
  const texto = !p
    ? 'Hola, quiero información del catálogo'
    : p.precio === null
      ? `Hola, quiero saber el precio de ${p.nombre} (${detalle(p)})`
      : `Hola, quiero ${p.nombre} (${detalle(p)}) a ${precio(p.precio)}`;
  return `https://wa.me/${tienda.whatsapp}?text=${encodeURIComponent(texto)}`;
};

/** Atributos para que un elemento se pueda sumar al pedido (ver components/Pedido.astro).
 *  Sin precio, el mosaico solo abre su propio WhatsApp para consultar. */
export const item = (p: Producto) =>
  p.precio === null
    ? { href: linkWhatsApp(p), target: '_blank', rel: 'noopener' }
    : { href: linkWhatsApp(p), 'data-item': p.id, 'data-nombre': p.nombre, 'data-precio': p.precio, 'data-detalle': detalle(p) };
