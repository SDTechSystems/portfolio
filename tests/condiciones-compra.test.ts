import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { informacionCompra } from '../src/lib/condiciones-compra.ts';
import { validarCatalogo } from '../src/lib/datos-catalogo.ts';
import { tienda } from '../src/data/tienda.ts';

const original = JSON.parse(readFileSync(new URL('../src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json', import.meta.url), 'utf8'));
const validar = (datos: unknown) => validarCatalogo(datos, tienda, () => true);

test('sin datos no promete región, idioma ni código para la cuenta del comprador', () => {
  const compra = informacionCompra('Juego', 'Switch 1');
  assert.equal(compra.tipo, 'Juego completo');
  assert.deepEqual(compra.datos, []);
  assert.equal(compra.pendientes.length, 5);
  assert.match(compra.resumen, /Por confirmar: región de canje, idiomas, cambio de región, entrega, canje en tu cuenta/);
  assert.doesNotMatch(compra.resumen, /Código para canjear/);
});

test('la mejora identifica el juego base y la plataforma sin confundirse con juego completo', () => {
  const compra = informacionCompra('Mejora', 'Switch 2', {}, 'Juego de ejemplo');
  assert.equal(compra.tipo, 'Paquete de mejora');
  assert.match(compra.requisitoBase!, /Requiere tener el juego base: Juego de ejemplo \(Switch 1\).*Switch 2/);
  assert.match(compra.resumen, /Paquete de mejora · Switch 2/);
  assert.doesNotMatch(compra.resumen, /Juego completo/);
  assert.match(informacionCompra('DLC', 'Switch 1').requisitoBase!, /juego base compatible/);
});

test('condiciones generales confirmadas y excepciones false/null son distintas de ausencia', () => {
  const generales = original.condiciones_generales;
  const compra = informacionCompra('Juego', 'Switch 2', generales);
  assert.deepEqual(compra.pendientes, ['idiomas']);
  assert.match(compra.resumen, /Japón/);
  assert.match(compra.resumen, /Requiere cambiar la región/);
  assert.match(compra.resumen, /guía/);
  assert.match(compra.resumen, /Código para canjear en tu cuenta/);
  const excepcion = informacionCompra('Juego', 'Switch 2', {
    ...generales, region_canje: null, requiere_cambio_region: false, codigo_cuenta_propia: null,
    idiomas: ['Español', 'Japonés'], requisitos: 'Requisito confirmado',
  });
  assert.ok(excepcion.pendientes.includes('región de canje'));
  assert.ok(excepcion.pendientes.includes('canje en tu cuenta'));
  assert.match(excepcion.resumen, /No requiere cambiar la región/);
  assert.match(excepcion.resumen, /Español, Japonés/);
  assert.match(excepcion.resumen, /Requisito confirmado/);
  assert.doesNotMatch(excepcion.resumen, /Región de canje: Japón|Código para canjear en tu cuenta/);
});

test('valida las condiciones generales y las excepciones, incluso en productos ocultos', () => {
  const datos = structuredClone(original);
  datos.condiciones_generales.idiomas = ['Español'];
  datos.productos.find((p: { publicar?: boolean }) => p.publicar === false).condiciones = {
    region_canje: null, requiere_cambio_region: false, codigo_cuenta_propia: null,
  };
  assert.doesNotThrow(() => validar(datos));
  datos.condiciones_generales.region_canje = 123;
  datos.productos.find((p: { publicar?: boolean }) => p.publicar === false).condiciones.idiomas = 'Español';
  assert.throws(() => validar(datos), (e: Error) => {
    assert.match(e.message, /Catálogo.*condiciones.region_canje/);
    assert.match(e.message, /Producto.*condiciones.idiomas/);
    return true;
  });
});

for (const condiciones of [null, [], 'Japón', { requiere_cambio_region: 'sí' }, { codigo_cuenta_propia: 1 },
  { region_canje: ' ' }, { modalidad_entrega: 'x'.repeat(161) }, { requisitos: 'a\nb' },
  { idiomas: [] }, { idiomas: [null] }, { idiomas: [''] }, { idiomas: ['a\nb'] }, { idioma: 'Español' }]) {
  test(`rechaza condiciones inválidas: ${JSON.stringify(condiciones)}`, () => {
    const datos = structuredClone(original);
    datos.productos[0].condiciones = condiciones;
    assert.throws(() => validar(datos), /^Error: Revisa el catálogo:[\s\S]*condiciones/);
  });
}
