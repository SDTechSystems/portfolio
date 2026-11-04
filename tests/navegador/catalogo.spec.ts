import { expect, test, type Locator, type Page } from '@playwright/test';
import datos from '../../src/assets/Catalogo_Nintendo_Switch_Colombia/productos.json' with { type: 'json' };
import { tienda } from '../../src/data/tienda';
import type { Fila } from '../../src/lib/datos-catalogo';

// Oráculo independiente del DOM y de catalogo.ts: un error de renderizado no debe
// cambiar a la vez el resultado esperado. Los importes nunca están escritos a mano.
const productos = (datos.productos as Fila[]).filter((p) => p.publicar !== false && (
  tienda.mostrarDlcUpdates || !['dlc', 'update'].includes(p.tipo_producto) || tienda.destacados.includes(p.id)
));
const precio = (p: Fila) => Object.hasOwn(p, 'precio_venta_cop')
  ? p.precio_venta_cop! : p.precio_referencia_eshop_colombia_cop ?? null;
const vendibles = productos.filter((p) => precio(p) !== null);
const moneda = (n: number) => new Intl.NumberFormat(tienda.locale, {
  style: 'currency', currency: tienda.moneda, maximumFractionDigits: 0,
}).format(n);
const detalle = (p: Fila) => {
  const tipo = p.tipo_producto === 'paquete_mejora' ? 'Paquete de mejora'
    : p.tipo_producto === 'dlc' ? 'DLC' : p.tipo_producto === 'update' ? 'Update' : 'Juego completo';
  const lineas = [`${tipo} · ${p.plataforma === 'Nintendo Switch 2' ? 'Switch 2' : 'Switch 1'}`];
  if (tipo === 'Paquete de mejora') {
    const base = productos.find((b) => b.grupo === p.grupo && b.plataforma === 'Nintendo Switch')!;
    lineas.push(`Requiere tener el juego base: ${base.titulo} (Switch 1). Se usa en Switch 2.`);
  } else if (tipo === 'DLC' || tipo === 'Update') lineas.push('Requiere tener el juego base compatible.');
  const c = { ...datos.condiciones_generales, ...p.condiciones };
  const campos: [string, string | null | undefined][] = [
    ['Región de canje', c.region_canje], ['Idiomas', c.idiomas?.join(', ')],
    ['Cambio de región', c.requiere_cambio_region == null ? undefined : c.requiere_cambio_region ? 'Requiere cambiar la región de la cuenta' : 'No requiere cambiar la región de la cuenta'],
    ['Entrega', c.modalidad_entrega],
    ['Canje en tu cuenta', c.codigo_cuenta_propia == null ? undefined : c.codigo_cuenta_propia ? 'Código para canjear en tu cuenta' : 'No es un código para canjear en tu cuenta'],
  ];
  for (const [nombre, valor] of campos) if (valor != null) lineas.push(`${nombre}: ${valor}`);
  if (c.requisitos) lineas.push(`Requisitos: ${c.requisitos}`);
  const pendientes = campos.filter(([, valor]) => valor == null).map(([nombre]) => nombre.toLowerCase());
  if (pendientes.length) lineas.push(`Por confirmar: ${pendientes.join(', ')}`);
  return lineas.join('; ');
};
const item = (page: Page, id: string) => page.locator(`[data-item="${id}"]`);

async function sinDesborde(page: Page) {
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(
    await page.evaluate(() => document.documentElement.clientWidth),
  );
}

async function contenidoDentro(interior: Locator, exterior: Locator) {
  await expect(interior).toBeVisible();
  await expect.poll(async () => {
    const a = await interior.boundingBox();
    const b = await exterior.boundingBox();
    return !!a && !!b && a.x >= b.x - 1 && a.x + a.width <= b.x + b.width + 1
      && a.y >= b.y - 1 && a.y + a.height <= b.y + b.height + 1;
  }).toBe(true);
}

function comprobarDestino(href: string) {
  const url = new URL(href);
  expect(url.origin).toBe('https://wa.me');
  expect(url.pathname).toBe(`/${tienda.whatsapp}`);
  return url.searchParams.get('text');
}

async function comprobarPedido(page: Page, elegidos: Fila[]) {
  const total = elegidos.reduce((suma, p) => suma + precio(p)!, 0);
  await expect(page.locator('#pedido')).toBeVisible();
  await expect(page.locator('#pedido .total')).toHaveText(moneda(total));
  // El orden del mensaje puede ser el del tablero; la lista debe ser exacta, sin omisiones ni duplicados.
  const mensaje = comprobarDestino((await page.locator('#pedido .cta').getAttribute('href'))!);
  const [saludo, ...lineas] = mensaje!.split('\n');
  expect(saludo).toBe('Hola, quiero pedir:');
  expect(lineas.pop()).toBe(`Total: ${moneda(total)}`);
  expect(lineas.sort()).toEqual(elegidos.map((p) => `• ${p.titulo} (${detalle(p)}) ${moneda(precio(p)!)}`).sort());
}

async function elegir(page: Page, p: Fila) {
  const opcion = item(page, p.id);
  // Las filas se mueven al dialog: conservar el locator por id, no por posición.
  const mosaico = page.locator(`.mosaico[data-item="${p.id}"], .mosaico:has([data-item="${p.id}"])`);
  // El evento close devuelve las filas después de ocultar el diálogo.
  await expect(mosaico).toHaveCount(1);
  const abrir = mosaico.locator('.abrir');
  if (await abrir.isVisible()) {
    await abrir.click();
    await expect(page.getByRole('dialog')).toBeVisible();
    await opcion.click();
    await page.getByRole('button', { name: 'Listo', exact: true }).click();
    await expect(page.getByRole('dialog')).toBeHidden();
    await expect(mosaico).toHaveCount(1);
  } else {
    await opcion.click();
  }
  await expect(opcion).toHaveAttribute('aria-pressed', 'true');
}

test('tablero sin desbordes, portadas cargadas y filas cerradas', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('[data-item][aria-pressed]')).toHaveCount(vendibles.length);
  await page.evaluate(() => document.fonts.ready);
  const imagenes = page.locator('.mosaico img');
  const fichasConImagen = new Set(productos.filter((p) => p.imagen).map((p) => p.grupo ?? p.id));
  await expect(imagenes).toHaveCount(fichasConImagen.size);
  // Activar lazy loading mediante desplazamiento real antes de comprobar naturalWidth.
  for (const imagen of await imagenes.all()) {
    await imagen.scrollIntoViewIfNeeded();
    await expect.poll(() => imagen.evaluate((img: HTMLImageElement) => img.complete && img.naturalWidth > 0)).toBe(true);
  }
  await sinDesborde(page);
  await expect(page.getByRole('link', { name: '¿No ves tu juego?', exact: true })).toBeVisible();
  // Medir cada banda horizontal del grid, incluidos destacados de dos filas y cierres.
  // No reutilizar reticula.ts: así se detectan errores del algoritmo o del CSS.
  const huecos = await page.locator('.tablero').evaluate((tablero) => {
    const estilo = getComputedStyle(tablero);
    const caja = tablero.getBoundingClientRect();
    const izquierda = caja.left + parseFloat(estilo.paddingLeft);
    const derecha = caja.right - parseFloat(estilo.paddingRight);
    const separacion = parseFloat(estilo.columnGap);
    const piezas = [...tablero.children].map((el) => el.getBoundingClientRect()).filter((r) => r.width && r.height);
    return [...new Set(piezas.map((r) => r.top + 1))].flatMap((y) => {
      const fila = piezas.filter((r) => r.top <= y && r.bottom > y).sort((a, b) => a.left - b.left);
      const fallos: string[] = [];
      let borde = izquierda;
      fila.forEach((r, i) => {
        if (Math.abs(r.left - borde - (i ? separacion : 0)) > 1) fallos.push(`Hueco o solapamiento en y=${y}, x=${r.left}`);
        borde = r.right;
      });
      if (Math.abs(derecha - borde) > 1) fallos.push(`Fila sin cerrar en y=${y}`);
      return fallos;
    });
  });
  expect(huecos).toEqual([]);
});

test('dos títulos: selección, total, WhatsApp y restauración', async ({ page }) => {
  await page.goto('/');
  const dos = vendibles.filter((p) => !p.grupo).slice(0, 2);
  expect(dos).toHaveLength(2);
  for (const p of dos) await elegir(page, p);
  await comprobarPedido(page, dos);
  for (const p of dos) await expect(page.locator('.mosaico').filter({ has: item(page, p.id) })).toHaveCSS('background-color', 'rgb(18, 18, 20)');
  await page.reload();
  for (const p of dos) await expect(item(page, p.id)).toHaveAttribute('aria-pressed', 'true');
  await comprobarPedido(page, dos);
  for (const p of dos) await item(page, p.id).click();
  await expect(page.locator('#pedido')).toBeHidden();
});

test('panel: versión, total, Escape y devolución del foco', async ({ page }) => {
  await page.goto('/');
  const abrir = page.locator('.abrir:visible').first();
  await expect(abrir).toBeVisible();
  await abrir.click();
  const dialogo = page.getByRole('dialog');
  await expect(dialogo).toBeVisible();
  const opcion = dialogo.locator('[data-item]').first();
  const id = await opcion.getAttribute('data-item');
  const p = vendibles.find((p) => p.id === id)!;
  expect(p).toBeDefined();
  await opcion.press('Space');
  await expect(opcion).toHaveAttribute('aria-pressed', 'true');
  await expect(dialogo.locator('[data-anuncio]')).toHaveText(`Total del pedido: ${moneda(precio(p)!)}`);
  await page.keyboard.press('Escape');
  await expect(dialogo).toBeHidden();
  await expect(abrir).toBeFocused();
  await comprobarPedido(page, [p]);
});

test('todos los productos: total y botón dentro de la barra', async ({ page }) => {
  await page.goto('/');
  expect((await page.locator('[data-item]').evaluateAll((els) => els.map((el) => el.getAttribute('data-item')))).sort())
    .toEqual(vendibles.map((p) => p.id).sort());
  for (const p of vendibles) await elegir(page, p);
  await comprobarPedido(page, vendibles);
  await contenidoDentro(page.locator('#pedido .cta'), page.locator('#pedido'));
  await contenidoDentro(page.locator('#pedido .total'), page.locator('#pedido'));
  const barra = (await page.locator('#pedido').boundingBox())!;
  expect(barra.x).toBeGreaterThanOrEqual(0);
  expect(barra.x + barra.width).toBeLessThanOrEqual(page.viewportSize()!.width);
  const total = (await page.locator('#pedido .total').boundingBox())!;
  const boton = (await page.locator('#pedido .cta').boundingBox())!;
  expect(total.x + total.width).toBeLessThanOrEqual(boton.x);
  await sinDesborde(page);
});

test('si no carga el script del panel, las versiones siguen accesibles', async ({ page }) => {
  let bloqueados = 0;
  await page.route('**/*', async (route) => {
    const tipo = route.request().resourceType();
    if (tipo !== 'document' && tipo !== 'script') return route.continue();
    const respuesta = await route.fetch();
    const codigo = await respuesta.text();
    const esPanel = (s: string) => s.includes('showModal') && s.includes('data-panel-listo');
    // Astro inserta los módulos pequeños en el HTML; los grandes pueden ir aparte.
    // Retirar solo ese script conserva Pedido y comprueba el fallo parcial real de #17.
    if (tipo === 'script' && esPanel(codigo)) {
      bloqueados++;
      return route.abort('failed');
    }
    const body = tipo === 'document' ? codigo.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, (script) => {
      if (!esPanel(script)) return script;
      bloqueados++;
      return '';
    }) : codigo;
    await route.fulfill({ response: respuesta, body });
  });
  await page.goto('/');
  expect(bloqueados).toBe(1);
  await expect(page.locator('[data-panel-listo]')).toHaveCount(0);
  const versiones = page.locator('.version');
  expect(await versiones.count()).toBeGreaterThan(0);
  for (const version of await versiones.all()) {
    await expect(version).toBeVisible();
    comprobarDestino((await version.getAttribute('href'))!);
  }
  // Pedido sigue funcionando: no se ha desactivado JavaScript entero para simular el fallo.
  const p = vendibles.find((p) => p.grupo)!;
  await item(page, p.id).click();
  await comprobarPedido(page, [p]);
  await sinDesborde(page);
});

test.describe('sin JavaScript', () => {
  test.use({ javaScriptEnabled: false });
  test('cada producto conserva su enlace de WhatsApp visible', async ({ page }) => {
    await page.goto('/');
    const enlaces = page.locator('a.seleccion, a.version');
    await expect(enlaces).toHaveCount(productos.length);
    const mensajes: string[] = [];
    for (const enlace of await enlaces.all()) {
      await expect(enlace).toBeVisible();
      await expect(enlace).not.toHaveAttribute('role', 'button');
      mensajes.push(comprobarDestino((await enlace.getAttribute('href'))!)!);
    }
    expect(mensajes.sort()).toEqual(productos.map((p) => precio(p) === null
      ? `Hola, quiero saber el precio de ${p.titulo} (${detalle(p)})`
      : `Hola, quiero ${p.titulo} (${detalle(p)}) a ${moneda(precio(p)!)}`).sort());
    await expect(page.locator('#pedido')).toBeHidden();
    await sinDesborde(page);
  });
});

test('detalles del juego: condiciones confirmadas, consulta y selección independiente', async ({ page }) => {
  await page.goto('/');
  const p = vendibles.find((p) => !p.grupo)!;
  const detalles = page.locator(`[data-condiciones="${p.id}"]`);
  await detalles.locator('summary').press('Enter');
  await expect(detalles).toHaveAttribute('open', '');
  await expect(detalles).toContainText('Juego completo');
  await expect(detalles).toContainText('Japón');
  await expect(detalles).toContainText('Requiere cambiar la región de la cuenta');
  await expect(detalles).toContainText('guía para cambiar la región');
  await expect(detalles).toContainText('Código para canjear en tu cuenta');
  await expect(detalles).toContainText('Por confirmar: idiomas');
  await expect(item(page, p.id)).toHaveAttribute('aria-pressed', 'false');
  const consulta = comprobarDestino((await detalles.getByRole('link', { name: 'Consultar condiciones' }).getAttribute('href'))!);
  expect(consulta).toBe(`Hola, quiero confirmar las condiciones de ${p.titulo} (${detalle(p)})`);
  // Nada interactivo anidado dentro de los controles de selección o apertura.
  await expect(page.locator('[data-item] a, [data-item] button, [data-item] summary, button summary')).toHaveCount(0);
  await detalles.locator('summary').press('Space');
  await expect(detalles).not.toHaveAttribute('open');
  await elegir(page, p);
  await comprobarPedido(page, [p]);
  await detalles.locator('summary').click();
  await expect(item(page, p.id)).toHaveAttribute('aria-pressed', 'true');
  await sinDesborde(page);
});

test('mejora: requisito visible y detalles accesibles dentro del panel', async ({ page }) => {
  await page.goto('/');
  const p = vendibles.find((p) => p.tipo_producto === 'paquete_mejora')!;
  const mosaico = page.locator('.mosaico').filter({ has: item(page, p.id) });
  const abrir = mosaico.locator('.abrir');
  await abrir.click();
  const dialogo = page.getByRole('dialog');
  await expect(dialogo).toBeVisible();
  await expect(item(page, p.id)).toContainText('Paquete de mejora');
  await expect(item(page, p.id)).toContainText('Requiere tener el juego base');
  const detalles = dialogo.locator(`[data-condiciones="${p.id}"]`);
  await detalles.locator('summary').click();
  await expect(detalles).toContainText('Japón');
  await expect(item(page, p.id)).toHaveAttribute('aria-pressed', 'false');
  await expect.poll(() => dialogo.evaluate((el) => el.scrollWidth <= el.clientWidth)).toBe(true);
  await detalles.getByRole('link', { name: 'Consultar condiciones' }).focus();
  await page.keyboard.press('Tab');
  expect(await dialogo.evaluate((el) => el.contains(document.activeElement))).toBe(true);
  await page.keyboard.press('Escape');
  await expect(dialogo).toBeHidden();
  await expect(abrir).toBeFocused();
  await elegir(page, p);
  await comprobarPedido(page, [p]);
});

test.describe('detalles sin JavaScript', () => {
  test.use({ javaScriptEnabled: false });
  test('el desplegable funciona y conserva la selección rápida por WhatsApp', async ({ page }) => {
    await page.goto('/');
    for (const p of [vendibles.find((p) => !p.grupo)!, vendibles.find((p) => p.tipo_producto === 'paquete_mejora')!]) {
      const detalles = page.locator(`[data-condiciones="${p.id}"]`);
      await detalles.locator('summary').click();
      await expect(detalles).toHaveAttribute('open', '');
      await expect(detalles).toContainText('Japón');
      await expect(detalles.getByRole('link', { name: 'Consultar condiciones' })).toBeVisible();
      await expect(item(page, p.id)).toBeVisible();
      expect(comprobarDestino((await item(page, p.id).getAttribute('href'))!)).toContain(detalle(p));
    }
    await sinDesborde(page);
  });
});
