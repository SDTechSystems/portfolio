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
  /** Ruta del archivo de la portada en el disco (la usa pages/og.jpg.ts). */
  archivo?: string;
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

const CARPETA = 'Catalogo_Nintendo_Switch_Colombia';
const ruta = (r: string) => `../assets/${CARPETA}/${r}`;
const filas = datos.productos as Fila[];

// Revisión de productos.json y tienda.ts: un error de tipeo detiene `npm run build` con un
// mensaje claro, en vez de publicar un juego en la consola equivocada o sin portada.
const PLATAFORMAS = ['Nintendo Switch', 'Nintendo Switch 2'];
const TIPOS = ['juego_digital', 'juego_con_accesorios', 'dlc', 'update'];
const precioValido = (n: unknown) => n === null || (typeof n === 'number' && Number.isInteger(n) && n > 0);
const errores: string[] = [];
const vistos = new Set<string>();
filas.forEach((f, i) => {
  const quien = `Producto ${i + 1} (${f.id || 'sin id'})`;
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(f.id ?? '')) errores.push(`${quien}: "id" debe ir en minúsculas y con guiones, ej. "mario-kart-world".`);
  if (vistos.has(f.id)) errores.push(`${quien}: el id "${f.id}" está repetido.`);
  vistos.add(f.id);
  if (!f.titulo?.trim()) errores.push(`${quien}: falta "titulo".`);
  if (!PLATAFORMAS.includes(f.plataforma)) errores.push(`${quien}: "plataforma" es "${f.plataforma}"; debe ser ${PLATAFORMAS.map((x) => `"${x}"`).join(' o ')}.`);
  if (!TIPOS.includes(f.tipo_producto)) errores.push(`${quien}: "tipo_producto" es "${f.tipo_producto}"; debe ser uno de ${TIPOS.map((x) => `"${x}"`).join(', ')}.`);
  if (!precioValido(f.precio_referencia_eshop_colombia_cop ?? null)) errores.push(`${quien}: "precio_referencia_eshop_colombia_cop" debe ser un número entero sin puntos (ej. 239900) o null.`);
  if (f.precio_venta_cop !== undefined && !precioValido(f.precio_venta_cop)) errores.push(`${quien}: "precio_venta_cop" debe ser un número entero sin puntos (ej. 239900) o null.`);
  if (f.imagen && !portadas[ruta(f.imagen.ruta)]) errores.push(`${quien}: no existe la portada "${f.imagen.ruta}" (revisa el nombre del archivo en la carpeta imagenes/).`);
});
if (tienda.destacados.length !== 3) errores.push(`tienda.ts: "destacados" debe tener exactamente 3 ids (tiene ${tienda.destacados.length}).`);
if (new Set(tienda.destacados).size !== tienda.destacados.length) errores.push('tienda.ts: hay un id repetido en "destacados".');
tienda.destacados.filter((id) => !vistos.has(id)).forEach((id) => errores.push(`tienda.ts: el destacado "${id}" no existe en productos.json.`));
if (!/^\d{11,15}$/.test(tienda.whatsapp)) errores.push('tienda.ts: "whatsapp" debe ser solo dígitos con código de país (Colombia: 57 + 10 dígitos).');
if (errores.length) throw new Error(`Revisa el catálogo:\n- ${errores.join('\n- ')}`);

const productos: Producto[] = filas.map((f) => ({
  id: f.id,
  nombre: f.titulo,
  precio: f.precio_venta_cop ?? f.precio_referencia_eshop_colombia_cop ?? null,
  tipo: f.tipo_producto === 'dlc' ? 'DLC' : f.tipo_producto === 'update' ? 'Update' : 'Juego',
  consola: f.plataforma === 'Nintendo Switch 2' ? 'Switch 2' : 'Switch 1',
  nota: f.tipo_producto === 'juego_con_accesorios' ? 'Necesita Ring-Con' : undefined,
  imagen: f.imagen && portadas[ruta(f.imagen.ruta)]?.default,
  archivo: f.imagen && `src/assets/${CARPETA}/${f.imagen.ruta}`,
}));

export const destacados = tienda.destacados
  .map((id) => productos.find((p) => p.id === id))
  .filter((p): p is Producto => !!p);

/** Bloques bajo los destacados. La consola la marca la pestaña de cada mosaico, así que los juegos
 *  van juntos y sin título; un juego con versión para cada consola son dos mosaicos. */
export interface Seccion { titulo?: string; productos: Producto[]; mas: string; mensaje: string }
const resto = productos.filter((p) => !tienda.destacados.includes(p.id));
export const secciones: Seccion[] = [
  { productos: resto.filter((p) => p.tipo === 'Juego'), mas: '¿No ves tu juego?', mensaje: 'Hola, busco un juego' },
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
