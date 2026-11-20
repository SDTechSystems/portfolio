// Gallery covers for /paginas/: screenshots the top of each sample site (without the SD Tech bar)
// into public/muestras/<site>/portada.webp. Needs a running preview: npm run build && npm run preview.
// Usage: node tools/sample-sites/covers.cjs [base-url]
const { chromium } = require("playwright");
const sharp = require("sharp");
const path = require("node:path");
const base = process.argv[2] || "http://localhost:4321/";
const sites = ["brasa-brava", "sereno", "aurelia", "orbita", "arco", "la-navaja", "michi-firulais", "ebano"];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, reducedMotion: "reduce" });
  for (const slug of sites) {
    await page.goto(`${base}muestras/${slug}/`, { waitUntil: "networkidle" });
    await page.evaluate(() => document.querySelector(".sd-bar")?.remove());
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    const png = await page.screenshot();
    await sharp(png).resize(1200, 750).webp({ quality: 74, effort: 5 }).toFile(path.join(__dirname, "../../public/muestras", slug, "portada.webp"));
    console.log("cover", slug);
  }
  await browser.close();
})();
