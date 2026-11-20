// Converts the generated PNGs (tools/sample-sites/images-src/<site>/<slot>.png) into the WebP files
// the sample websites use: public/muestras/<site>/<slot>.webp (1600px) and <slot>-sm.webp (720px).
// Square product photos are capped at 900px and get no small copy.
// Usage: node tools/sample-sites/convert.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const here = path.dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(fs.readFileSync(path.join(here, 'images.json'), 'utf8'));
const out = path.join(here, '..', '..', 'public', 'muestras');
let done = 0, missing = [];
for (const site of manifest.sites) {
  fs.mkdirSync(path.join(out, site.site), { recursive: true });
  for (const img of site.images) {
    const src = path.join(here, 'images-src', site.site, `${img.slot}.png`);
    if (!fs.existsSync(src)) { missing.push(`${site.site}/${img.slot}`); continue; }
    const [w, h] = img.ratio.split(':').map(Number);
    const square = w === h;
    const big = square ? 900 : 1600;
    const pipe = () => sharp(src).resize({ width: big, height: Math.round(big * h / w), fit: 'cover', position: 'attention' });
    await pipe().webp({ quality: 78, effort: 5 }).toFile(path.join(out, site.site, `${img.slot}.webp`));
    if (!square) await sharp(src).resize({ width: 720, height: Math.round(720 * h / w), fit: 'cover', position: 'attention' }).webp({ quality: 74, effort: 5 }).toFile(path.join(out, site.site, `${img.slot}-sm.webp`));
    done++;
  }
}
console.log(`Converted ${done} images.${missing.length ? ` Missing: ${missing.join(', ')}` : ''}`);
