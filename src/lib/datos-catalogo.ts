/** Forma de cada entrada en productos.json (lo que edita el dueño). */
export interface Fila {
  id: string;
  titulo: string;
  plataforma: string;
  tipo_producto: string;
  /** Opcional: precio de venta propio. Si no está, se usa el de referencia de la eShop. */
  precio_venta_cop?: number | null;
  precio_referencia_eshop_colombia_cop?: number | null;
  /** recorte: opcional, dónde está el logo de la portada ("arriba", "centro" o "abajo"; por defecto "abajo").
   *  "izquierda"/"derecha": para el destacado grande, que en escritorio recorta los lados. */
  imagen?: { ruta: string; recorte?: string };
  /** Opcional: mismo texto en las filas de un juego con versión para cada consola, ej. "zelda-totk". */
  grupo?: string;
  /** Opcional: false = no se muestra en la página (ej. precio pendiente). Por defecto se muestra. */
  publicar?: boolean;
}

const esObjeto = (valor: unknown): valor is Record<string, unknown> =>
  typeof valor === 'object' && valor !== null && !Array.isArray(valor);

function fallar(errores: string[]): never {
  throw new Error(`Revisa el catálogo:\n- ${errores.join('\n- ')}`);
}

/** Comprueba los tipos antes de acceder a cadenas, imágenes o grupos. */
function leerFilas(datos: unknown): Fila[] {
  if (!esObjeto(datos) || !Array.isArray(datos.productos)) {
    fallar(['productos.json: "productos" debe ser una lista de productos.']);
  }
  const errores: string[] = [];
  datos.productos.forEach((f: unknown, i: number) => {
    const quien = `Producto ${i + 1}`;
    if (!esObjeto(f)) {
      errores.push(`${quien}: debe ser un objeto con los datos del producto.`);
      return;
    }
    for (const campo of ['id', 'titulo', 'plataforma', 'tipo_producto']) {
      if (typeof f[campo] !== 'string') errores.push(`${quien}: "${campo}" debe ser un texto.`);
    }
    for (const campo of ['precio_venta_cop', 'precio_referencia_eshop_colombia_cop']) {
      const valor = f[campo];
      if (valor !== undefined && valor !== null && typeof valor !== 'number') {
        errores.push(`${quien}: "${campo}" debe ser un número entero sin puntos (ej. 239900) o null.`);
      }
    }
    if (f.publicar !== undefined && typeof f.publicar !== 'boolean') errores.push(`${quien}: "publicar" debe ser true o false (sin comillas).`);
    if (f.grupo !== undefined && typeof f.grupo !== 'string') errores.push(`${quien}: "grupo" debe ser un texto.`);
    if (f.imagen !== undefined) {
      if (!esObjeto(f.imagen)) {
        errores.push(`${quien}: "imagen" debe ser un objeto con "ruta", o elimina el campo si no hay portada.`);
      } else {
        if (typeof f.imagen.ruta !== 'string') errores.push(`${quien}: "imagen.ruta" debe ser un texto.`);
        if (f.imagen.recorte !== undefined && typeof f.imagen.recorte !== 'string') errores.push(`${quien}: "imagen.recorte" debe ser un texto.`);
      }
    }
  });
  if (errores.length) fallar(errores);
  // El cast se hace únicamente después de comprobar todos los campos usados por la web.
  return datos.productos as Fila[];
}

/** Valida la estructura antes de filtrar y aplicar las reglas; devuelve solo filas publicadas. */
export function validarCatalogo(
  datos: unknown,
  tienda: { destacados: string[]; whatsapp: string },
  existePortada: (ruta: string) => boolean,
): Fila[] {
  const todas = leerFilas(datos);
  const filas = todas.filter((f) => f.publicar !== false);
  // Revisión de productos.json y tienda.ts: un error de tipeo detiene `npm run build` con un
  // mensaje claro, en vez de publicar un juego en la consola equivocada o sin portada.
  const PLATAFORMAS = ['Nintendo Switch', 'Nintendo Switch 2'];
  const TIPOS = ['juego_digital', 'juego_con_accesorios', 'dlc', 'update', 'paquete_mejora'];
  const RECORTES = ['arriba', 'centro', 'abajo', 'izquierda', 'derecha'];
  const precioValido = (n: unknown) => n === null || (typeof n === 'number' && Number.isInteger(n) && n > 0);
  const errores: string[] = [];
  const vistos = new Set<string>();
  todas.forEach((f, i) => {
    const quien = `Producto ${i + 1} (${f.id || 'sin id'})`;
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(f.id ?? '')) errores.push(`${quien}: "id" debe ir en minúsculas y con guiones, ej. "mario-kart-world".`);
    if (vistos.has(f.id)) errores.push(`${quien}: el id "${f.id}" está repetido.`);
    vistos.add(f.id);
    if (!f.titulo?.trim()) errores.push(`${quien}: falta "titulo".`);
    if (!PLATAFORMAS.includes(f.plataforma)) errores.push(`${quien}: "plataforma" es "${f.plataforma}"; debe ser ${PLATAFORMAS.map((x) => `"${x}"`).join(' o ')}.`);
    if (!TIPOS.includes(f.tipo_producto)) errores.push(`${quien}: "tipo_producto" es "${f.tipo_producto}"; debe ser uno de ${TIPOS.map((x) => `"${x}"`).join(', ')}.`);
    if (!precioValido(f.precio_referencia_eshop_colombia_cop ?? null)) errores.push(`${quien}: "precio_referencia_eshop_colombia_cop" debe ser un número entero sin puntos (ej. 239900) o null.`);
    if (f.precio_venta_cop !== undefined && !precioValido(f.precio_venta_cop)) errores.push(`${quien}: "precio_venta_cop" debe ser un número entero sin puntos (ej. 239900) o null.`);
    if (f.imagen && !existePortada(f.imagen.ruta)) errores.push(`${quien}: no existe la portada "${f.imagen.ruta}" (revisa el nombre del archivo en la carpeta imagenes/).`);
    if (f.imagen?.recorte !== undefined && !RECORTES.includes(f.imagen.recorte)) errores.push(`${quien}: "recorte" de la imagen es "${f.imagen.recorte}"; debe ser ${RECORTES.map((x) => `"${x}"`).join(', ')}.`);
    if (f.publicar !== undefined && typeof f.publicar !== 'boolean') errores.push(`${quien}: "publicar" debe ser true o false (sin comillas).`);
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
  tienda.destacados.filter((id) => todas.some((f) => f.id === id && f.publicar === false)).forEach((id) => errores.push(`tienda.ts: el destacado "${id}" tiene "publicar": false; elige otro o publícalo.`));
  const juegoDe = (id: string) => filas.find((f) => f.id === id)?.grupo ?? id;
  if (new Set(tienda.destacados.map(juegoDe)).size < new Set(tienda.destacados).size) errores.push('tienda.ts: dos destacados son versiones del mismo juego; elige 3 juegos distintos.');
  if (!/^\d{11,15}$/.test(tienda.whatsapp)) errores.push('tienda.ts: "whatsapp" debe ser solo dígitos con código de país (Colombia: 57 + 10 dígitos).');
  if (errores.length) fallar(errores);

  return filas;
}
