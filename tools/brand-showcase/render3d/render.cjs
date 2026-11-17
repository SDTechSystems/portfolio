// Batch renderer: serves the repo, opens studio.html?scene=&brand= in headless Chromium (2x supersampling)
// and writes PNG frames to .cache/renders/<slug>/<scene>.png. Usage: node render.cjs [slug|scene ...]
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const OUT = path.resolve(__dirname, '../.cache/renders');
const { chromium } = require(path.join(ROOT, 'node_modules/playwright'));
const SCENES = new Set(['cards', 'mug', 'box', 'bag', 'cup', 'can', 'jar', 'bottles', 'stationery', 'poster', 'menu', 'wallsign', 'phone', 'app', 'laptop', 'hangtag', 'paycard', 'idbadge', 'tshirt', 'tote', 'cap', 'apron']);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
});
(async () => {
  await new Promise((ok) => server.listen(0, '127.0.0.1', ok));
  const port = server.address().port;
  const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/data/brand-showcase.json'), 'utf8'));
  const args = process.argv.slice(2), force = args.includes('--force');
  const want = args.filter((a) => !a.startsWith('--'));
  const jobs = [];
  for (const b of data.brands) for (const k of [...b.mockups.map((m) => m.key), 'stationery']) {
    if (!SCENES.has(k)) continue;
    if (want.length && !want.includes(b.slug) && !want.includes(k) && !want.includes(b.slug + '/' + k)) continue;
    const out = path.join(OUT, b.slug, k + '.png');
    if (!force && fs.existsSync(out)) continue;
    jobs.push([b.slug, k, out]);
  }
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const conc = Number(process.env.CONC || 3); let i = 0, fails = 0;
  async function worker() {
    while (i < jobs.length) {
      const [slug, k, out] = jobs[i++]; const t = Date.now();
      const page = await browser.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2 });
      page.on('pageerror', (e) => console.log(`  ${slug}/${k} pageerror:`, e.message));
      try {
        await page.goto(`http://127.0.0.1:${port}/tools/brand-showcase/render3d/studio.html?scene=${k}&brand=${slug}`);
        await page.waitForFunction(() => window.done === true, null, { timeout: 600000 });
        const err = await page.evaluate(() => window.failed);
        if (err) throw new Error(err);
        fs.mkdirSync(path.dirname(out), { recursive: true });
        await page.screenshot({ path: out });
        console.log(`ok ${slug}/${k} ${((Date.now() - t) / 1000).toFixed(1)}s`);
      } catch (e) { fails++; console.log(`FAIL ${slug}/${k}: ${String(e.message).slice(0, 400)}`); }
      await page.close();
    }
  }
  await Promise.all(Array.from({ length: conc }, worker));
  await browser.close(); server.close();
  console.log(`${jobs.length - fails}/${jobs.length} rendered`);
  process.exit(fails ? 1 : 0);
})();
