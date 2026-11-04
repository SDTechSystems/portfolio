/** Un precio de venta nulo fuerza «Consultar»; solo su ausencia permite usar la referencia. */
export function precioVenta(f: {
  precio_venta_cop?: number | null;
  precio_referencia_eshop_colombia_cop?: number | null;
}): number | null {
  return f.precio_venta_cop === undefined ? f.precio_referencia_eshop_colombia_cop ?? null : f.precio_venta_cop;
}
