import assert from 'node:assert/strict';
import { test } from 'node:test';
import { precioVenta } from '../src/lib/precio-venta.ts';

test('el precio explícito, incluso null, tiene prioridad sobre la referencia (#18)', () => {
  assert.equal(precioVenta({ precio_venta_cop: null, precio_referencia_eshop_colombia_cop: 239900 }), null);
  assert.equal(precioVenta({ precio_venta_cop: 199900, precio_referencia_eshop_colombia_cop: 239900 }), 199900);
  assert.equal(precioVenta({ precio_venta_cop: 199900, precio_referencia_eshop_colombia_cop: null }), 199900);
  assert.equal(precioVenta({ precio_venta_cop: 199900 }), 199900);
});

test('solo la ausencia de precio de venta permite usar la referencia (#18)', () => {
  assert.equal(precioVenta({ precio_referencia_eshop_colombia_cop: 239900 }), 239900);
  assert.equal(precioVenta({ precio_referencia_eshop_colombia_cop: null }), null);
  assert.equal(precioVenta({ precio_venta_cop: null }), null);
  assert.equal(precioVenta({}), null);
});

