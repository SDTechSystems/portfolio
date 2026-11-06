import assert from 'node:assert/strict';
import { test } from 'node:test';
import { coincide, normalizar } from '../src/lib/buscar.ts';

test('normalizar quita tildes, mayúsculas y espacios de más', () => {
  assert.equal(normalizar('Pokémon Leyendas'), 'pokemon leyendas');
  assert.equal(normalizar('  ZELDA   Tears '), 'zelda tears');
});

test('coincide si aparecen todas las palabras, en cualquier orden y aunque sean parciales', () => {
  const indice = normalizar('The Legend of Zelda: Tears of the Kingdom');
  assert.equal(coincide(indice, 'zelda tears'), true);
  assert.equal(coincide(indice, 'kingdom zelda'), true);
  assert.equal(coincide(indice, 'zelda mario'), false);
  assert.equal(coincide('mario kart world', 'kar'), true);
  assert.equal(coincide('pokemon', 'Pokémon'), true);
});

test('una consulta vacía muestra todo', () => {
  assert.equal(coincide('mario', '   '), true);
  assert.equal(coincide('mario', ''), true);
});
