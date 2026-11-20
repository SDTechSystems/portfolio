// Genera docs/vista-previa.zip: una copia del sitio que se abre con doble clic,
// sin servidor. Uso: npm run build && node tools/vista-previa/build.mjs
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execFileSync } from 'node:child_process';
import { build } from 'esbuild';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');
const dist = path.join(root, 'dist');
const out = path.join(root, 'docs', 'vista-previa.zip');
if (!fs.existsSync(path.join(dist, 'index.html'))) throw Error('Ejecuta primero npm run build (sin PAGES_BASE).');

const work = fs.mkdtempSync(path.join(os.tmpdir(), 'vista-previa-'));
const site = path.join(work, 'sitio');
fs.cpSync(dist, site, { recursive: true });

const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
  const p = path.join(dir, e.name);
  return e.isDirectory() ? walk(p) : [p];
});
const files = walk(site);

// Convierte "/ruta/" del sitio en una ruta relativa al archivo que la usa.
function relative(from, value) {
  if (!value.startsWith('/') || value.startsWith('//')) return value;
  const match = value.match(/^([^?#]*)(.*)$/);
  let target = match[1];
  const rest = match[2];
  if (target.endsWith('/')) target += 'index.html';
  else if (!path.extname(target) && fs.existsSync(path.join(site, target, 'index.html'))) target += '/index.html';
  let rel = path.relative(path.dirname(from), path.join(site, target)).split(path.sep).join('/');
  if (!rel) rel = path.basename(target);
  return rel + rest;
}
const fixSrcset = (from, v) => v.split(',').map((part) => {
  const [url, ...size] = part.trim().split(/\s+/);
  return [relative(from, url), ...size].join(' ');
}).join(', ');

for (const file of files.filter((f) => f.endsWith('.css'))) {
  const css = fs.readFileSync(file, 'utf8').replace(/url\((['"]?)(\/[^)'"]+)\1\)/g, (_, q, u) => `url(${q}${relative(file, u)}${q})`);
  fs.writeFileSync(file, css);
}

let pages = 0;
for (const file of files.filter((f) => f.endsWith('.html'))) {
  let html = fs.readFileSync(file, 'utf8');
  // Los módulos no cargan desde file://: se empaquetan como script clásico al final del body.
  const modules = [];
  html = html.replace(/<script type="module"( src="([^"]+)")?>([\s\S]*?)<\/script>/g, (_, __, src, code) => {
    modules.push(src ? `import ${JSON.stringify(path.join(site, src))};` : code);
    return '';
  });
  let bundled = '';
  for (const [i, code] of modules.entries()) {
    const entry = path.join(work, `entrada-${pages}-${i}.mjs`);
    fs.writeFileSync(entry, code.replace(/(from\s*|import\s*)(["'])(\/_astro\/[^"']+)\2/g, (_, k, q, u) => `${k}${q}${path.join(site, u)}${q}`));
    const result = await build({ entryPoints: [entry], bundle: true, format: 'iife', write: false, minify: true, target: 'es2020', logLevel: 'silent' });
    bundled += `<script>${result.outputFiles[0].text.replace(/<\/script/gi, '<\\/script')}</script>`;
  }
  html = html
    .replace(/\s(href|src|data-full|data-zoom|poster)="(\/[^"]*)"/g, (_, a, v) => ` ${a}="${relative(file, v)}"`)
    .replace(/\s(srcset)="([^"]*)"/g, (_, a, v) => ` ${a}="${fixSrcset(file, v)}"`)
    .replace(/url\((&#34;|&quot;|['"]?)(\/[^)'"&]+)\1\)/g, (_, q, u) => `url(${q}${relative(file, u)}${q})`)
    .replace('</body>', `${bundled}</body>`)
    // Chrome no carga fuentes de otra carpeta desde file:// en estilos de la página: se incrustan.
    .replace(/<link rel="preload"[^>]*as="font"[^>]*>/g, '')
    .replace(/url\((["']?)([^)"']+\.woff2?)\1\)/g, (m, q, u) => {
      if (/^(data:|https?:)/.test(u)) return m;
      const font = path.resolve(path.dirname(file), u);
      if (!fs.existsSync(font)) return m;
      return `url("data:font/${u.endsWith('2') ? 'woff2' : 'woff'};base64,${fs.readFileSync(font).toString('base64')}")`;
    });
  fs.writeFileSync(file, html);
  pages++;
}

// Los scripts ya quedaron dentro de cada página.
for (const f of fs.readdirSync(path.join(site, '_astro'))) if (f.endsWith('.js')) fs.rmSync(path.join(site, '_astro', f));

fs.writeFileSync(path.join(site, 'LEEME.txt'), [
  'SD Tech Systems — Vista previa ES/EN',
  '',
  'Abre index.html para español o en/index.html para inglés. Funciona con doble clic, sin instalar nada ni usar un servidor.',
  'Incluye proyectos, demos interactivas, páginas web de ejemplo, marcas y formularios. Los formularios y botones de WhatsApp necesitan internet.',
  'Las demos usan datos ficticios y no guardan lo que escribes.',
  `Generada el ${new Date().toISOString().slice(0, 10)} desde el repositorio del portafolio.`,
  '',
].join('\r\n'));

fs.rmSync(out, { force: true });
execFileSync('zip', ['-q', '-r', '-9', out, '.'], { cwd: site });
console.log(`${pages} páginas → ${path.relative(root, out)} (${(fs.statSync(out).size / 1048576).toFixed(1)} MB)`);
console.log(`Carpeta sin comprimir: ${site}`);
