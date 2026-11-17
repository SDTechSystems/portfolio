const { chromium } = require("playwright");
const { default: AxeBuilder } = require("@axe-core/playwright");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const { spawn } = require("node:child_process");
const path = require("node:path");
const base = process.env.DEMO_TEST_BASE || "http://127.0.0.1:4455/";
const ids = (
  process.env.DEMO_TEST_IDS ||
  "akashic-vault,openmultipos,easy-drink,akashic-tv,tasktone"
).split(",");
const shotDir = process.env.DEMO_SCREENSHOT_DIR;
const stored = (page) =>
  page.evaluate(() => ({
    local: { ...localStorage },
    session: { ...sessionStorage },
  }));
let preview, browser;
async function ready() {
  if (process.env.DEMO_TEST_BASE) return;
  preview = spawn(
    process.execPath,
    [
      "node_modules/astro/astro.js",
      "preview",
      "--host",
      "127.0.0.1",
      "--port",
      "4455",
    ],
    {
      stdio: "ignore",
      env: {
        ...process.env,
        PAGES_BASE: new URL(base).pathname,
        ASTRO_TELEMETRY_DISABLED: "1",
      },
    },
  );
  for (let i = 0; i < 80; i++) {
    try {
      if ((await fetch(base)).ok) return;
    } catch {}
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error("Preview server did not start");
}
async function screenshot(page, id, suffix = "") {
  if (!shotDir) return;
  await page.evaluate(() => {
    document.activeElement?.blur();
    window.scrollTo(0, 0);
  });
  fs.mkdirSync(shotDir, { recursive: true });
  await page.screenshot({
    path: path.join(shotDir, id + suffix + ".png"),
    fullPage: true,
  });
}
async function checkLayout(page, id, lang) {
  const screens = await page
    .locator("[data-screen]")
    .evaluateAll((nodes) => nodes.map((n) => n.dataset.screen));
  for (const width of [360, 390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const name of screens) {
      await page.evaluate((name) => {
        location.hash = name;
      }, name);
      await page.waitForFunction(
        (name) => !document.querySelector(`[data-screen="${name}"]`).hidden,
        name,
      );
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth > innerWidth,
      );
      if (overflow) {
        const bad = await page.locator("body *:visible").evaluateAll((els) =>
          els
            .filter((e) => e.getBoundingClientRect().right > innerWidth + 1)
            .slice(0, 6)
            .map((e) => ({
              tag: e.tagName,
              cls: e.className,
              right: e.getBoundingClientRect().right,
            })),
        );
        throw Error(
          `${lang}/${id}/${name} overflow at ${width}: ${JSON.stringify(bad)}`,
        );
      }
    }
  }
}
async function business(page, id) {
  await page.locator("[data-nav=sales]:visible").first().click();
  await page.locator("#product-search").fill("no-match-zz");
  assert.equal(await page.locator(".product-tile").count(), 0);
  assert.ok(await page.locator("#product-empty").isVisible());
  await page.locator("#product-search").fill("DEMO-101");
  assert.equal(await page.locator(".product-tile").count(), 1);
  await page.locator(".product-tile").click();
  await page.locator(".quantity-button").last().click();
  assert.equal(await page.locator("#cart-count").innerText(), "2");
  assert.ok(
    await page
      .locator(".quantity-button")
      .last()
      .evaluate((e) => e === document.activeElement),
  );
  await page.locator(".quantity-button").first().click();
  assert.equal(await page.locator("#cart-count").innerText(), "1");
  await page.locator("#sale-discount").fill("10");
  if (id === "openmultipos") {
    await page.locator("#business-picker").selectOption("b");
    await page.locator("#product-search").fill("DEMO-201");
    await page.locator(".product-tile").click();
    assert.equal(await page.locator("#cart-count").innerText(), "2");
  }
  await page.locator("#start-checkout").click();
  assert.ok(await page.locator("#checkout-dialog").evaluate((d) => d.open));
  await page.locator("[name=payment][value=card]").check();
  await page.locator("#checkout-form button[type=submit]").click();
  assert.ok(await page.locator("#receipt-dialog").evaluate((d) => d.open));
  const receipt = await page.locator("#receipt-total").innerText();
  assert.ok(receipt.includes(id === "openmultipos" ? "66" : "7"));
  assert.equal(await page.locator("#cart-count").innerText(), "0");
  await page.keyboard.press("Escape");
  await page.locator("[data-nav=inventory]:visible").first().click();
  await page.locator("#inventory-search").fill("DEMO-10");
  if (id === "openmultipos") {
    assert.equal(await page.locator("#inventory-rows tr").count(), 0);
    await page.locator("#business-picker").selectOption("a");
  }
  await page.locator("#inventory-search").fill("DEMO-101");
  assert.equal(await page.locator("#inventory-rows tr").count(), 1);
  assert.equal(
    await page.locator("#inventory-rows tr td").nth(3).innerText(),
    "31",
  );
  await page.locator("#inventory-rows button").click();
  assert.ok(await page.locator("#product-dialog").evaluate((d) => d.open));
  await page.keyboard.press("Escape");
  await page.locator("[data-nav=reports]:visible").first().click();
  const before = await page.locator("#report-revenue").innerText();
  await page.locator("#report-period").selectOption("week");
  assert.notEqual(await page.locator("#report-revenue").innerText(), before);
  await page.locator("[data-nav=settings]:visible").first().click();
  await page.locator("[data-accent]").nth(1).click();
  assert.equal(
    await page.locator("[data-accent]").nth(1).getAttribute("aria-pressed"),
    "true",
  );
  await page
    .locator("[data-nav=customers]:visible")
    .first()
    .count()
    .then(async (count) => {
      if (count) {
        await page.locator("[data-nav=customers]:visible").first().click();
        await page.locator("[data-customer]").nth(1).click();
        assert.equal(await page.locator("#sale-customer").inputValue(), "c2");
      }
    });
  await page.locator("[data-nav=sales]:visible").first().click();
  await page.locator("#product-search").fill("");
  await screenshot(page, id, "-checkout");
}
async function vault(page) {
  await page.locator("[data-prompt=ideas]").click();
  assert.equal(await page.locator(".message").count(), 2);
  const unsafe = "<img src=x onerror=alert(1)>";
  await page.locator("#chat-input").fill(unsafe);
  await page.locator("#chat-form button[type=submit]").click();
  assert.equal(await page.locator(".message").count(), 4);
  assert.equal(await page.locator(".message img").count(), 0);
  assert.ok(
    (await page.locator(".message.user").last().innerText()).includes(unsafe),
  );
  await page.locator("#save-chat").click();
  await page.locator("[data-nav=vault]").click();
  assert.equal(await page.locator(".vault-record").count(), 3);
  await page.locator("#toggle-vault").click();
  assert.ok(await page.locator("#vault-locked").isVisible());
  await page.locator("#toggle-vault").click();
  await page.locator(".vault-record button").last().click();
  assert.equal(await page.locator(".message").count(), 4);
  await page.locator("[data-nav=models]").click();
  await page.locator("[data-model=coder]").click();
  assert.equal(
    await page.locator("[data-mode=code]").getAttribute("aria-pressed"),
    "true",
  );
  await page.locator("[data-nav=studio]").click();
  await page.locator("#studio-prompt").fill("A fictional mountain landscape");
  await page.locator("#studio-style").selectOption("mono");
  await page.locator("#studio-type").selectOption("video");
  await page.locator("#studio-form button[type=submit]").click();
  assert.ok(await page.locator("#studio-result").isVisible());
  assert.equal(
    await page.locator(".generated-landscape").getAttribute("data-style"),
    "mono",
  );
  await screenshot(page, "akashic-vault", "-studio");
  await page.locator("#vault-theme").click();
  assert.ok(
    await page
      .locator("body")
      .evaluate((e) => e.classList.contains("vault-light")),
  );
  await page.locator("[data-nav=settings]").click();
  await page.locator("#vault-appearance").selectOption("dark");
  await page.locator("#new-chat").click();
  assert.equal(await page.locator(".message").count(), 0);
}
async function tv(page) {
  await page.locator("#tv-search").fill("no-match-zz");
  assert.equal(await page.locator(".poster-card:visible").count(), 0);
  await page.locator("#tv-clear").click();
  assert.equal(await page.locator(".poster-card:visible").count(), 5);
  await page.locator(".poster-card:visible").first().focus();
  await page.keyboard.press("ArrowRight");
  assert.ok(
    await page
      .locator(".poster-card:visible")
      .nth(1)
      .evaluate((e) => e === document.activeElement),
  );
  await page.keyboard.press("Enter");
  assert.ok(await page.locator("#tv-details").evaluate((d) => d.open));
  await page.keyboard.press("Escape");
  assert.ok(
    await page
      .locator(".poster-card:visible")
      .nth(1)
      .evaluate((e) => e === document.activeElement),
  );
  await page.locator(".tv-header [data-kind=series]").click();
  assert.equal(await page.locator(".poster-card:visible").count(), 3);
  await page.locator(".poster-card:visible").first().click();
  await page.locator("#tv-season").selectOption("2");
  await page.locator(".episode-button").nth(1).click();
  await page.waitForFunction(
    () => !document.querySelector("[data-screen=player]").hidden,
  );
  assert.ok(
    (await page.locator("#player-title").innerText()).includes("T2 E2"),
  );
  await page.locator("#player-toggle").click();
  await page.waitForFunction(
    () => document.querySelector("#player-progress").value !== "0",
  );
  await page.locator("#player-toggle").click();
  await page.locator("#player-progress").fill("60");
  assert.ok((await page.locator("#player-time").innerText()).includes("1:00"));
  await page.locator("#player-subtitles").selectOption("es");
  assert.ok(await page.locator("#player-subtitle-preview").isVisible());
  await page.locator("#player-provider").selectOption("b");
  await screenshot(page, "akashic-tv", "-player");
  await page.keyboard.press("Escape");
  await page.waitForFunction(
    () => !document.querySelector("[data-screen=catalog]").hidden,
  );
  assert.ok(await page.locator("[data-screen=catalog]").isVisible());
  await page.locator("#tv-genre").selectOption("scifi");
  assert.equal(await page.locator(".poster-card:visible").count(), 1);
}
async function tasktone(page) {
  await page.locator("[data-enter-role=creator]").click();
  assert.equal(await page.locator(".tt-order-card").count(), 3);
  await page.locator("#tt-search").fill("no-match-zz");
  assert.ok(await page.locator("#tt-empty").isVisible());
  await page.locator("#tt-search").fill("");
  await page.locator("#view-professional").click();
  assert.ok(await page.locator("#tt-profile-dialog").evaluate((d) => d.open));
  await page.keyboard.press("Escape");
  await page.locator("#new-order").click();
  await page.locator("#tt-new-name").fill("Demo order <script>sample</script>");
  await page.locator("#tt-new-service").selectOption("mix");
  await page.locator("#tt-new-notes").fill("Fictional brief");
  await page.locator("#tt-new-form button[type=submit]").click();
  await page.waitForFunction(
    () => !document.querySelector("[data-screen=order]").hidden,
  );
  assert.ok(
    (await page.locator("#tt-order-title").innerText()).includes("<script>"),
  );
  assert.equal(await page.locator("#tt-order-title script").count(), 0);
  for (const stage of ["progress", "review", "done"]) {
    await page.locator("#tt-order-actions .primary").click();
    assert.ok(
      (await page.locator("#tt-order-status").getAttribute("class")).includes(
        "stage-" + stage,
      ),
    );
  }
  await page.locator("#tt-message").fill("Sample feedback <img src=x>");
  await page.locator("#tt-message-form button[type=submit]").click();
  assert.ok(
    (await page.locator(".tt-comment").last().innerText()).includes(
      "<img src=x>",
    ),
  );
  assert.equal(await page.locator(".tt-comment img").count(), 0);
  await page.locator("#sample-audio").evaluate((a) => a.play());
  await page.waitForFunction(
    () => document.querySelector("#sample-audio").currentTime > 0,
  );
  await page.locator("#sample-audio").evaluate((a) => a.pause());
  await screenshot(page, "tasktone", "-order");
  await page.locator('a[href="#workspace"]:visible').last().click();
  assert.equal(await page.locator(".tt-order-card").count(), 4);
  await page.locator("[data-role=professional]").click();
  assert.equal(
    await page.locator("[data-role=professional]").getAttribute("aria-pressed"),
    "true",
  );
  await page.locator("#tt-filter").selectOption("review");
  await page.locator(".tt-order-card button").first().click();
  await page.locator("#tt-order-actions .secondary").click();
  assert.ok(
    (await page.locator("#tt-order-status").getAttribute("class")).includes(
      "stage-progress",
    ),
  );
}
async function run() {
  await ready();
  const executable =
    process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ||
    (fs.existsSync("/usr/bin/chromium") ? "/usr/bin/chromium" : undefined);
  browser = await chromium.launch({
    executablePath: executable,
    args: ["--no-sandbox"],
    headless: true,
  });
  for (const lang of (process.env.DEMO_TEST_LANGS || "es,en").split(","))
    for (const id of ids) {
      const context = await browser.newContext({
        viewport: { width: 1440, height: 1000 },
        reducedMotion: "reduce",
      });
      const page = await context.newPage();
      const requests = [],
        errors = [],
        failed = [];
      page.on("request", (r) =>
        requests.push({
          url: r.url(),
          method: r.method(),
          type: r.resourceType(),
        }),
      );
      page.on("requestfailed", (r) => failed.push(r.url()));
      page.on("pageerror", (e) => errors.push(e.message));
      page.on("console", (m) => {
        if (
          m.type() === "error" &&
          /Content Security Policy|Refused to/.test(m.text())
        )
          errors.push(m.text());
      });
      await context.addInitScript(() => {
        localStorage.setItem("portfolio-test-sentinel", "unchanged");
        sessionStorage.setItem("portfolio-test-sentinel", "unchanged");
      });
      const response = await page.goto(`${base}${lang}/demos/${id}/`, {
        waitUntil: "networkidle",
      });
      assert.equal(response.status(), 200);
      assert.equal(await page.locator("html").getAttribute("lang"), lang);
      await page.evaluate(() => document.fonts.ready);
      const initial = await stored(page);
      assert.equal(
        await page
          .locator("iframe,form[action],input[type=password],input[type=file]")
          .count(),
        0,
      );
      assert.ok(
        (
          await page
            .locator('meta[http-equiv="Content-Security-Policy"]')
            .getAttribute("content")
        ).includes("connect-src 'none'"),
      );
      if (lang === "es") await screenshot(page, id);
      if (id === "openmultipos" || id === "easy-drink")
        await business(page, id);
      else if (id === "akashic-vault") await vault(page);
      else if (id === "akashic-tv") await tv(page);
      else await tasktone(page);
      assert.deepEqual(
        await stored(page),
        initial,
        `${id}: interaction persisted visitor input`,
      );
      await page.locator("#reset-demo").click();
      await page.waitForLoadState("networkidle");
      if (id === "akashic-vault")
        assert.equal(await page.locator(".vault-record").count(), 2);
      if (id === "tasktone")
        assert.equal(await page.locator(".tt-order-card").count(), 3);
      if (id === "openmultipos" || id === "easy-drink") {
        assert.equal(await page.locator("#cart-count").innerText(), "0");
        assert.equal(
          await page.locator("[data-metric=transactions]").innerText(),
          lang === "es" ? "2 ventas de ejemplo" : "2 sample sales",
        );
      }
      const auditScreens =
        lang === "es"
          ? await page
              .locator("[data-screen]")
              .evaluateAll((els) => els.map((e) => e.dataset.screen))
          : [
              await page
                .locator("[data-screen]:visible")
                .getAttribute("data-screen"),
            ];
      for (const screen of auditScreens) {
        await page.evaluate((screen) => (location.hash = screen), screen);
        await page.waitForFunction(
          (screen) =>
            !document.querySelector(`[data-screen="${screen}"]`).hidden,
          screen,
        );
        const axe = await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
          .analyze();
        assert.deepEqual(
          axe.violations.map((v) => ({
            id: v.id,
            nodes: v.nodes.map((n) => n.target),
          })),
          [],
          `${lang}/${id}/${screen}: accessibility violations`,
        );
      }
      await page.locator("#accessibility-open").click();
      await page.locator("#accessibility-size").selectOption("1.5");
      for (const key of ["motion", "spacing", "links", "contrast"])
        await page.locator("#accessibility-" + key).check();
      await page.keyboard.press("Escape");
      assert.ok(
        await page
          .locator("#accessibility-open")
          .evaluate((e) => e === document.activeElement),
      );
      await checkLayout(page, id, lang);
      await page.locator("#accessibility-open").click();
      await page.locator("#accessibility-reset").click();
      await page.keyboard.press("Escape");
      await page.setViewportSize({ width: 390, height: 844 });
      await page.evaluate(
        () =>
          (location.hash =
            document.querySelector("[data-screen]").dataset.screen),
      );
      await page.waitForFunction(
        () => !document.querySelector("[data-screen]").hidden,
      );
      if (lang === "es") await screenshot(page, id, "-mobile");
      const other = lang === "es" ? "en" : "es";
      await page.locator(`.demo-toolbar a[hreflang=${other}]`).click();
      assert.ok(page.url().includes(`/${other}/demos/${id}/`));
      await page.locator(".demo-back").click();
      assert.ok(page.url().includes(`/${other}/proyectos/${id}/`));
      assert.equal(await page.locator("form").count(), 0);
      assert.equal(await page.locator(".open-demo").count(), 1);
      await page.locator(".demo-image-link").click();
      assert.ok(page.url().includes(`/${other}/demos/${id}/`));
      assert.deepEqual(errors, [], `${lang}/${id}: browser errors`);
      assert.deepEqual(failed, [], `${lang}/${id}: failed requests`);
      assert.ok(
        requests.every(
          (r) =>
            r.url.startsWith(new URL(base).origin) || r.url.startsWith("data:"),
        ),
        `${id}: external request`,
      );
      assert.ok(
        requests.every(
          (r) =>
            r.method === "GET" &&
            !["fetch", "xhr", "websocket", "eventsource"].includes(r.type),
        ),
        `${id}: backend-like request attempted`,
      );
      assert.equal(context.serviceWorkers().length, 0);
      console.log(
        `PASS ${lang}/${id}: workflow, isolation, reset, accessibility, 150% reflow, language and image/button navigation`,
      );
      await context.close();
    }
  const nojs = await browser.newContext({ javaScriptEnabled: false });
  const page = await nojs.newPage();
  for (const id of ids) {
    await page.goto(`${base}es/demos/${id}/`);
    assert.equal(
      await page.locator("form button[type=submit]:not([disabled])").count(),
      0,
    );
  }
  await nojs.close();
  console.log("PASS: all five bilingual demos and no-JavaScript form safety");
  await testIntakeForms();
  await testBrandShowcase();
}

// Quote forms: answer on a phone, reload mid-way, resume, send and see the WhatsApp hand-off.
// Google Forms is intercepted, so the tests never write to the real spreadsheets.
async function testIntakeForms() {
  for (const slug of ["diseno-de-marca", "pagina-web", "software-a-medida"]) {
    const context = await browser.newContext({
      viewport: { width: 375, height: 812 },
      isMobile: true,
      hasTouch: true,
      reducedMotion: "reduce",
    });
    const page = await context.newPage();
    const errors = [];
    let posted = null;
    page.on("pageerror", (e) => errors.push(e.message));
    await page.route("https://docs.google.com/**", (route) => {
      posted = new URLSearchParams(route.request().postData() || "");
      route.fulfill({ status: 200, body: "ok" });
    });
    const url = `${base}es/formularios/${slug}/`;
    await page.goto(url);
    const active = () =>
      page.locator(".intake-form > .intake-step.is-active").getAttribute("data-step");
    // Answer the current question (text, or the first option) and continue.
    const answerAndNext = async () => {
      const step = page.locator(".intake-form > .intake-step.is-active");
      const input = step.locator(".intake-input:not([data-other-text])");
      if (await input.count()) {
        const tel = (await step.getAttribute("data-input")) === "tel";
        await input.fill(tel ? "57 300 000 0000" : `Prueba ${await active()}`);
      } else {
        const radio = (await step.getAttribute("data-kind")) === "radio";
        await step.locator(".intake-choice").first().click();
        if (radio) { await page.waitForFunction((s) => document.querySelector(".intake-form > .intake-step.is-active")?.getAttribute("data-step") !== s, await step.getAttribute("data-step")); return; }
      }
      await step.locator(".intake-btn-primary[data-next]").click();
    };
    await page.locator(".intake-intro [data-start]").last().click();
    for (let i = 0; i < 6; i++) await answerAndNext();
    const before = await active();
    assert.equal(before, "6", `${slug}: should be on question 7`);
    // Accidental reload: back on the same question with the answers kept.
    await page.reload();
    assert.equal(await active(), before, `${slug}: reload must resume on the same question`);
    assert.equal(await page.locator(".intake-toast").count(), 1, `${slug}: resume banner`);
    assert.equal(await page.locator(".intake-step[data-entry]").first().locator(".intake-input").inputValue(), "Prueba 0");
    const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    assert.deepEqual(results.violations.map((v) => v.id), [], `${slug}: accessibility violations`);
    // Finish: answer the rest, review and send.
    while ((await active()) !== "review") await answerAndNext();
    await page.locator("[data-send]").click();
    await page.waitForSelector(".intake-done.is-active");
    assert.ok(posted && [...posted.keys()].some((k) => k.startsWith("entry.")), `${slug}: answers posted to Google Forms`);
    assert.equal(posted.getAll([...posted.keys()].find((k) => k.startsWith("entry.")))[0], "Prueba 0");
    const wa = await page.locator("[data-done-wa]").getAttribute("href");
    assert.ok(wa.startsWith("https://wa.me/573058147293?text=") && decodeURIComponent(wa).includes("acabo de llenar el formulario de"), `${slug}: WhatsApp hand-off`);
    // After sending, a reload starts fresh instead of resuming.
    await page.reload();
    assert.equal(await active(), "intro", `${slug}: draft cleared after sending`);
    assert.deepEqual(errors, [], `${slug}: browser errors`);
    console.log(`PASS formularios/${slug}: mobile flow, resume after reload, accessibility, send and WhatsApp hand-off`);
    await context.close();
  }
}
// Brand design showcase: gallery filters, brand pages, WhatsApp hand-off, zoom, assets and accessibility.
async function testBrandShowcase() {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, "../src/data/brand-showcase.json"), "utf8"));
  assert.equal(data.brands.length, 36, "36 sample brands");
  for (const lang of ["es", "en"]) {
    const context = await browser.newContext({ reducedMotion: "reduce" });
    const page = await context.newPage();
    const errors = [], failed = [];
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("requestfailed", (r) => failed.push(r.url()));
    page.on("response", (r) => { if (r.status() >= 400) failed.push(`${r.status()} ${r.url()}`); });
    await page.goto(`${base}${lang}/`);
    const nav = page.locator(`.main-navigation a[href$="/${lang}/marcas/"]`);
    assert.equal(await nav.count(), 1, `${lang}: brands link in the main menu`);
    assert.equal(await page.locator("#marcas .brand-card").count(), 6, `${lang}: home teaser shows 6 brands`);
    await nav.click();
    await page.waitForURL(`**/${lang}/marcas/`);
    assert.equal(await page.locator(".brand-card").count(), data.brands.length, `${lang}: gallery lists every brand`);
    for (const style of data.styles) {
      await page.locator(`[data-brand-filter="${style.id}"]`).click();
      const visible = await page.locator(".brand-card:not([hidden])").count();
      assert.equal(visible, data.brands.filter((b) => b.style === style.id).length, `${lang}: filter ${style.id}`);
    }
    await page.locator('[data-brand-filter="all"]').click();
    const axe = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
    assert.deepEqual(axe.violations.map((v) => v.id), [], `${lang}: gallery accessibility`);
    for (const slug of ["sereno", "voltio", "la-navaja", "maison-velour", "villa-serena"]) {
      const brand = data.brands.find((b) => b.slug === slug);
      await page.goto(`${base}${lang}/marcas/${slug}/`);
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 30)); } });
      const broken = await page.evaluate(() => [...document.images].filter((i) => i.getAttribute("src") && i.complete && i.naturalWidth === 0).map((i) => i.src));
      assert.deepEqual(broken, [], `${lang}/${slug}: images load`);
      const wa = await page.locator(".bp-hero a.brand-btn.wa").getAttribute("href");
      assert.ok(wa.startsWith("https://wa.me/573058147293?text="), `${lang}/${slug}: WhatsApp number`);
      const text = decodeURIComponent(wa.split("text=")[1]);
      assert.ok(text.includes(`«${brand.name}»`) && text.includes(`/${lang}/marcas/${slug}/`), `${lang}/${slug}: message names the design and its link`);
      assert.equal(await page.locator(".mockup-grid .mock").count(), brand.mockups.length + brand.corporate.length, `${lang}/${slug}: product and corporate mockups`);
      await page.locator(".mockup-grid .mock button").first().click();
      assert.ok(await page.locator("#brand-zoom").evaluate((d) => d.open), `${lang}/${slug}: zoom opens`);
      await page.keyboard.press("Escape");
      assert.ok(!(await page.locator("#brand-zoom").evaluate((d) => d.open)), `${lang}/${slug}: zoom closes`);
      const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
      assert.deepEqual(results.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target).join(" ")}`), [], `${lang}/${slug}: accessibility`);
      for (const width of [360, 390, 768, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        assert.ok(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), `${lang}/${slug}: no horizontal scroll at ${width}px`);
      }
      await page.setViewportSize({ width: 1280, height: 720 });
      const other = lang === "es" ? "en" : "es";
      assert.ok((await page.locator(`.language-switch a[lang=${other}]`).getAttribute("href")).endsWith(`/${other}/marcas/${slug}/`), `${lang}/${slug}: language switch keeps the brand`);
    }
    assert.deepEqual(errors, [], `${lang}: browser errors`);
    assert.deepEqual(failed, [], `${lang}: failed requests`);
    console.log(`PASS ${lang}/marcas: menu, filters, 5 brand pages, WhatsApp hand-off, zoom, images, accessibility and reflow`);
    await context.close();
  }
}
run()
  .catch((e) => {
    console.error(e);
    process.exitCode = 1;
  })
  .finally(async () => {
    await browser?.close();
    preview?.kill();
  });
