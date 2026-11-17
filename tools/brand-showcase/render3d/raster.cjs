// Rasterise SVG art to PNG (transparent background kept): node raster.cjs in.svg out.png width height
const path = require('path'), fs = require('fs');
const { chromium } = require(path.resolve(__dirname, '../../../node_modules/playwright'));
(async () => {
  const [inp, out, w, h] = process.argv.slice(2); const W = +w, H = +h;
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome' });
  const p = await b.newPage({ viewport: { width: W, height: H } });
  const data = 'data:image/svg+xml;base64,' + fs.readFileSync(inp).toString('base64');
  await p.setContent(`<html><body style="margin:0;background:transparent"><img src="${data}" style="display:block;width:${W}px;height:${H}px"></body></html>`);
  await p.waitForFunction(() => document.images[0].complete);
  await p.screenshot({ path: out, omitBackground: true });
  await b.close();
})();
