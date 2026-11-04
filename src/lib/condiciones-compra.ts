/** Datos comerciales confirmados por el dueño; ausencia = pendiente de consulta. */
export interface CondicionesCompra {
  region_canje?: string | null;
  idiomas?: string[] | null;
  requiere_cambio_region?: boolean | null;
  modalidad_entrega?: string | null;
  codigo_cuenta_propia?: boolean | null;
  requisitos?: string | null;
}

export interface InformacionCompra {
  tipo: string;
  requisitoBase?: string;
  datos: { nombre: string; valor: string }[];
  pendientes: string[];
  /** Resumen que acompaña a la variante en WhatsApp. */
  resumen: string;
}

export function informacionCompra(
  tipo: string,
  consola: string,
  condiciones: CondicionesCompra = {},
  juegoBase?: string,
): InformacionCompra {
  const nombreTipo = tipo === 'Juego' ? 'Juego completo' : tipo === 'Mejora' ? 'Paquete de mejora' : tipo;
  const requisitoBase = tipo === 'Mejora'
    ? `Requiere tener el juego base${juegoBase ? `: ${juegoBase} (Switch 1)` : ''}. Se usa en Switch 2.`
    : tipo === 'DLC' || tipo === 'Update' ? 'Requiere tener el juego base compatible.' : undefined;
  const datos: InformacionCompra['datos'] = [];
  const pendientes: string[] = [];
  const agregar = (nombre: string, valor?: string) => {
    if (valor !== undefined) datos.push({ nombre, valor });
    else pendientes.push(nombre.toLowerCase());
  };
  agregar('Región de canje', condiciones.region_canje ?? undefined);
  agregar('Idiomas', condiciones.idiomas?.join(', '));
  agregar('Cambio de región', condiciones.requiere_cambio_region == null ? undefined
    : condiciones.requiere_cambio_region ? 'Requiere cambiar la región de la cuenta' : 'No requiere cambiar la región de la cuenta');
  agregar('Entrega', condiciones.modalidad_entrega ?? undefined);
  agregar('Canje en tu cuenta', condiciones.codigo_cuenta_propia == null ? undefined
    : condiciones.codigo_cuenta_propia ? 'Código para canjear en tu cuenta' : 'No es un código para canjear en tu cuenta');
  if (condiciones.requisitos) datos.push({ nombre: 'Requisitos', valor: condiciones.requisitos });
  const resumen = [
    `${nombreTipo} · ${consola}`, requisitoBase,
    ...datos.map(({ nombre, valor }) => `${nombre}: ${valor}`),
    ...(pendientes.length ? [`Por confirmar: ${pendientes.join(', ')}`] : []),
  ].filter(Boolean).join('; ');
  return { tipo: nombreTipo, requisitoBase, datos, pendientes, resumen };
}
