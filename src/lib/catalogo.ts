import type { ImageMetadata } from 'astro';
import datos from '../assets/Catalogo_Nintendo_Switch_Colombia/productos.json';
import { tienda } from '../data/tienda';

export type Tipo = 'Juego' | 'DLC' | 'Update' | 'Mejora';
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
  /** En orden: Switch 1, Switch 2, paquete de mejora. Con una sola versión, el mosaico es como siempre. */
  versiones: Producto[];
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
  /** Opcional: mismo texto en las filas de un juego con versión para cada consola, ej. "zelda-totk". */
  grupo?: string;
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
const TIPOS = ['juego_digital', 'juego_con_accesorios', 'dlc', 'update', 'paquete_mejora'];
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
  if (f.grupo !== undefined && !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(f.grupo)) errores.push(`${quien}: "grupo" debe ir en minúsculas y con guiones, ej. "zelda-totk".`);
  if (f.tipo_producto === 'paquete_mejora' && f.plataforma !== 'Nintendo Switch 2') errores.push(`${quien}: un "paquete_mejora" lleva "plataforma": "Nintendo Switch 2".`);
  if (f.tipo_producto === 'paquete_mejora' && !f.grupo) errores.push(`${quien}: un "paquete_mejora" necesita "grupo", el mismo de su juego de Switch 1.`);
});
// Un grupo = el juego de Switch 1 + su versión de Switch 2 y/o su paquete de mejora (uno de cada uno).
const clase = (f: Fila) => (f.tipo_producto === 'paquete_mejora' ? 'paquete de mejora' : f.plataforma === 'Nintendo Switch 2' ? 'juego de Switch 2' : 'juego de Switch 1');
const grupos = new Map<string, Fila[]>();
filas.forEach((f) => f.grupo && grupos.set(f.grupo, [...(grupos.get(f.grupo) ?? []), f]));
grupos.forEach((g, nombre) => {
  const donde = `Grupo "${nombre}"`;
  if (g.length < 2) errores.push(`${donde}: solo lo tiene "${g[0].id}"; ponlo también en la otra versión del juego, o bórralo.`);
  ['juego de Switch 1', 'juego de Switch 2', 'paquete de mejora'].forEach((c) => {
    const n = g.filter((f) => clase(f) === c).length;
    if (n > 1) errores.push(`${donde}: tiene ${n} filas de ${c}; debe haber una sola.`);
  });
  if (g.length >= 2 && !g.some((f) => clase(f) === 'juego de Switch 1')) errores.push(`${donde}: le falta el juego de Switch 1.`);
  if (g.some((f) => f.tipo_producto === 'dlc' || f.tipo_producto === 'update')) errores.push(`${donde}: los DLC y updates no se agrupan.`);
});
if (tienda.destacados.length !== 3) errores.push(`tienda.ts: "destacados" debe tener exactamente 3 ids (tiene ${tienda.destacados.length}).`);
if (new Set(tienda.destacados).size !== tienda.destacados.length) errores.push('tienda.ts: hay un id repetido en "destacados".');
tienda.destacados.filter((id) => !vistos.has(id)).forEach((id) => errores.push(`tienda.ts: el destacado "${id}" no existe en productos.json.`));
const juegoDe = (id: string) => filas.find((f) => f.id === id)?.grupo ?? id;
if (new Set(tienda.destacados.map(juegoDe)).size < new Set(tienda.destacados).size) errores.push('tienda.ts: dos destacados son versiones del mismo juego; elige 3 juegos distintos.');
if (!/^\d{11,15}$/.test(tienda.whatsapp)) errores.push('tienda.ts: "whatsapp" debe ser solo dígitos con código de país (Colombia: 57 + 10 dígitos).');
if (errores.length) throw new Error(`Revisa el catálogo:\n- ${errores.join('\n- ')}`);

const productos: Producto[] = filas.map((f) => ({
  id: f.id,
  nombre: f.titulo,
  precio: f.precio_venta_cop ?? f.precio_referencia_eshop_colombia_cop ?? null,
  tipo: f.tipo_producto === 'dlc' ? 'DLC' : f.tipo_producto === 'update' ? 'Update' : f.tipo_producto === 'paquete_mejora' ? 'Mejora' : 'Juego',
  consola: f.plataforma === 'Nintendo Switch 2' ? 'Switch 2' : 'Switch 1',
  nota: f.tipo_producto === 'juego_con_accesorios' ? 'Necesita Ring-Con' : undefined,
  imagen: f.imagen && portadas[ruta(f.imagen.ruta)]?.default,
  archivo: f.imagen && `src/assets/${CARPETA}/${f.imagen.ruta}`,
  grupo: f.grupo,
}));

// Un mosaico por juego, en el lugar de la primera fila de su grupo. Nombre y nota: los del juego de
// Switch 1. Portada: la de Switch 2 si la tiene (la caja con la franja roja), si no, la primera que haya.
const orden = (p: Producto) => (p.tipo === 'Mejora' ? 2 : p.consola === 'Switch 2' ? 1 : 0);
const fichas: Ficha[] = [];
productos.forEach((p) => {
  if (p.grupo && fichas.some((f) => f.versiones.some((v) => v.grupo === p.grupo))) return;
  const versiones = p.grupo ? productos.filter((v) => v.grupo === p.grupo).sort((a, b) => orden(a) - orden(b)) : [p];
  const base = versiones[0];
  const portada = versiones.find((v) => v.tipo === 'Juego' && v.consola === 'Switch 2' && v.imagen) ?? versiones.find((v) => v.imagen);
  fichas.push({ id: base.id, nombre: base.nombre, tipo: base.tipo, nota: base.nota, imagen: portada?.imagen, archivo: portada?.archivo, versiones });
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
