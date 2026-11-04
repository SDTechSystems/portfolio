import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
import { test } from 'node:test';
import { runInNewContext } from 'node:vm';

// Ejecuta el script real del componente; el DOM mínimo permite probar restauración y
// selección sin descargar otro framework ni depender de un navegador en CI.
const componente = readFileSync(new URL('../src/components/Pedido.astro', import.meta.url), 'utf8');
const script = stripTypeScriptTypes(componente.match(/<script>([\s\S]*?)<\/script>/)![1]);

function iniciar(guardado: string | null, bloqueado = false) {
  let persistido = guardado;
  const atributos = new Map<string, string>();
  const eventos = new Map<string, (e: { preventDefault(): void }) => void>();
  const item = {
    dataset: { item: 'juego', nombre: 'Juego de prueba', precio: '239900', detalle: 'Juego · Switch 1' },
    setAttribute: (k: string, v: string) => atributos.set(k, v),
    getAttribute: (k: string) => atributos.get(k),
    addEventListener: (k: string, fn: (e: { preventDefault(): void }) => void) => eventos.set(k, fn),
  };
  const total = { textContent: '' }, cta = { href: '' }, anuncio = { textContent: '' };
  const vaciar = { addEventListener() {} };
  const partes: Record<string, unknown> = { '.total': total, '.cta': cta, '.vaciar': vaciar };
  const bar = { dataset: { locale: 'es-CO', moneda: 'COP', wa: '573058147293' }, hidden: true, querySelector: (s: string) => partes[s] };
  runInNewContext(script, {
    document: {
      getElementById: (id: string) => id === 'pedido' ? bar : anuncio,
      querySelectorAll: () => [item],
      querySelector: () => null,
    },
    sessionStorage: {
      getItem: () => { if (bloqueado) throw new Error('almacenamiento bloqueado'); return guardado; },
      setItem: (_k: string, v: string) => { if (bloqueado) throw new Error('almacenamiento bloqueado'); persistido = v; },
    },
    Intl,
  });
  return { bar, total, cta, atributos, eventos, persistido: () => persistido };
}

for (const valor of ['null', '{}', '42', 'true', '"juego"', '{malformado', null]) {
  test(`pedido inválido ${valor} permite iniciar y seleccionar (#19)`, () => {
    const p = iniciar(valor);
    assert.equal(p.atributos.get('aria-pressed'), 'false');
    assert.equal(p.bar.hidden, true);
    p.eventos.get('click')!({ preventDefault() {} });
    assert.equal(p.atributos.get('aria-pressed'), 'true');
    assert.equal(p.bar.hidden, false);
    assert.match(new URL(p.cta.href).searchParams.get('text')!, /Juego de prueba.*239\.900/);
    assert.deepEqual(JSON.parse(p.persistido()!), ['juego']);
  });
}

test('una lista mixta restaura solo los identificadores existentes (#19)', () => {
  const p = iniciar('[null,42,{},"juego","ya-no-existe","juego"]');
  assert.equal(p.atributos.get('aria-pressed'), 'true');
  assert.match(p.total.textContent, /239\.900/);
  assert.deepEqual(JSON.parse(p.persistido()!), ['juego']);
});

test('el almacenamiento bloqueado no impide seleccionar ni quitar (#19)', () => {
  const p = iniciar(null, true);
  p.eventos.get('click')!({ preventDefault() {} });
  assert.equal(p.bar.hidden, false);
  p.eventos.get('click')!({ preventDefault() {} });
  assert.equal(p.bar.hidden, true);
});
