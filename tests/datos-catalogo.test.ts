import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { validarCatalogo } from '../src/lib/datos-catalogo.ts';
import { tienda } from '../src/data/tienda.ts';

const catalogo = JSON.parse(readFileSync(new URL('../src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json', import.meta.url), 'utf8'));
const validar = (datos: unknown) => validarCatalogo(datos, tienda, () => true);

test('el catálogo actual sigue siendo válido (#20)', () => {
  assert.deepEqual(validar(catalogo), catalogo.productos.filter((f: { publicar?: boolean }) => f.publicar !== false));
});

test('valida también los productos ocultos y rechaza destacados sin publicar (#20)', () => {
  const datos = structuredClone(catalogo);
  datos.productos.push({ id: 'oculto', titulo: 'Oculto', plataforma: 'Nintendo Switch', tipo_producto: 'juego_digital', publicar: false });
  assert.ok(!validar(datos).some((f) => f.id === 'oculto'));
  datos.productos.at(-1).titulo = 123;
  assert.throws(() => validar(datos), /"titulo" debe ser un texto/);
  datos.productos.at(-1).titulo = 'Oculto';
  datos.productos.at(-1).precio_venta_cop = -1;
  assert.throws(() => validar(datos), /"precio_venta_cop" debe ser un número entero/);
  datos.productos.at(-1).precio_venta_cop = 100;
  datos.productos.at(-1).publicar = 'false';
  assert.throws(() => validar(datos), /"publicar" debe ser true o false/);
  datos.productos.at(-1).publicar = false;
  assert.throws(() => validarCatalogo(datos, { ...tienda, destacados: [tienda.destacados[0], tienda.destacados[1], 'oculto'] }, () => true), /"oculto" tiene "publicar": false/);
});

for (const datos of [null, [], {}, { productos: null }, { productos: {} }, { productos: 'juegos' }]) {
  test(`rechaza la estructura raíz ${JSON.stringify(datos)} con diagnóstico (#20)`, () => {
    assert.throws(() => validar(datos), /^Error: Revisa el catálogo:\n- productos.json: "productos" debe ser una lista/);
  });
}

test('acumula errores de entradas y campos sin lanzar TypeError (#20)', () => {
  const datos = structuredClone(catalogo);
  datos.productos[0] = null;
  datos.productos[1] = 42;
  datos.productos[2] = [];
  Object.assign(datos.productos[3], { id: 123, titulo: 123, plataforma: {}, tipo_producto: false, grupo: {}, imagen: { ruta: 42, recorte: null }, precio_venta_cop: '239900' });
  datos.productos[4].imagen = null;
  assert.throws(() => validar(datos), (e: Error) => {
    assert.equal(e.constructor, Error);
    assert.match(e.message, /^Revisa el catálogo:/);
    for (const n of [1, 2, 3]) assert.match(e.message, new RegExp(`Producto ${n}: debe ser un objeto`));
    for (const campo of ['id', 'titulo', 'plataforma', 'tipo_producto', 'grupo', 'imagen.ruta', 'imagen.recorte', 'precio_venta_cop']) {
      assert.ok(e.message.includes(`Producto 4: "${campo}"`), campo);
    }
    assert.match(e.message, /Producto 5: "imagen" debe ser un objeto/);
    return true;
  });
});

test('se mantienen los diagnósticos de ids, títulos, precios, imágenes y plataforma (#20)', () => {
  const datos = structuredClone(catalogo);
  Object.assign(datos.productos[0], { id: 'ID MALO', titulo: ' ', plataforma: 'Switch', tipo_producto: 'otro', precio_venta_cop: -1, imagen: { ruta: 'no-existe.webp', recorte: 'invalido' } });
  datos.productos[1].precio_referencia_eshop_colombia_cop = 2.5;
  datos.productos[2].id = datos.productos[3].id;
  assert.throws(() => validarCatalogo(datos, tienda, () => false), (e: Error) => {
    for (const texto of ['"id" debe', 'falta "titulo"', '"plataforma" es', '"tipo_producto" es', '"precio_venta_cop" debe', '"precio_referencia_eshop_colombia_cop" debe', 'no existe la portada', '"recorte" de la imagen', 'está repetido']) {
      assert.ok(e.message.includes(texto), texto);
    }
    return true;
  });
});

test('se mantienen las reglas de grupos y destacados (#20)', () => {
  const juego = (id: string, plataforma: string, tipo_producto = 'juego_digital', grupo = 'grupo') => ({ id, titulo: id, plataforma, tipo_producto, grupo });
  const productos = [
    juego('uno', 'Nintendo Switch'), juego('dos', 'Nintendo Switch'),
    juego('tres', 'Nintendo Switch 2', 'dlc'),
    juego('mejora', 'Nintendo Switch', 'paquete_mejora', ''),
    juego('solo', 'Nintendo Switch 2', 'juego_digital', 'solo'),
    juego('sin-base', 'Nintendo Switch 2', 'juego_digital', 'sin-base'),
    juego('sin-base-mejora', 'Nintendo Switch 2', 'paquete_mejora', 'sin-base'),
  ];
  assert.throws(() => validarCatalogo({ productos }, { destacados: ['uno', 'dos', 'inexistente'], whatsapp: '123' }, () => true), (e: Error) => {
    for (const texto of ['2 filas de juego de Switch 1', 'DLC y updates no se agrupan', 'necesita "grupo"', 'un "paquete_mejora" lleva', '"grupo" debe', 'solo lo tiene', 'le falta el juego de Switch 1', 'dos destacados son versiones', '"inexistente" no existe', '"whatsapp" debe']) {
      assert.ok(e.message.includes(texto), texto);
    }
    return true;
  });
  assert.throws(() => validarCatalogo(catalogo, { ...tienda, destacados: [tienda.destacados[0], tienda.destacados[0]] }, () => true), /exactamente 3 ids[\s\S]*id repetido/);
});
