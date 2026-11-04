import datos from '../data/catalogo.json';
import { tienda } from '../data/tienda';

export type Tipo = 'juego' | 'dlc' | 'update';
export type Consola = 'switch1' | 'switch2';
export interface Producto {
  id: string;
  nombre: string;
  precio: number;
  tipo: Tipo;
  consolas: Consola[];
  estreno?: boolean;
  /** Ruta en /public, ej. "/portadas/zelda-oot.jpg". Sin imagen se usa un marcador de color. */
  imagen?: string;
  color?: string;
}

export const productos = datos as Producto[];
export const estrenos = productos.filter((p) => p.estreno);
export const porTipo = (t: Tipo) => productos.filter((p) => p.tipo === t);

const fmt = new Intl.NumberFormat(tienda.locale, {
  style: 'currency',
  currency: tienda.moneda,
  maximumFractionDigits: 0,
});
export const precio = (n: number) => fmt.format(n);

export const etiquetaTipo: Record<Tipo, string> = { juego: 'Juego', dlc: 'DLC', update: 'Update' };
export const etiquetaConsola = (c: Consola[]) =>
  c.length === 2 ? 'Switch 1 y 2' : c[0] === 'switch2' ? 'Switch 2' : 'Switch 1';

export const linkWhatsApp = (p?: Producto) => {
  const texto = p
    ? `Hola, quiero ${p.nombre} (${etiquetaTipo[p.tipo]}, ${etiquetaConsola(p.consolas)}) a ${precio(p.precio)}`
    : `Hola, quiero información del catálogo`;
  return `https://wa.me/${tienda.whatsapp}?text=${encodeURIComponent(texto)}`;
};
