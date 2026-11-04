import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/navegador',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 2,
  timeout: 30_000,
  expect: { timeout: 5_000 },
  reporter: process.env.CI ? [['github'], ['list']] : 'list',
  use: {
    browserName: 'chromium',
    baseURL: 'http://127.0.0.1:4327',
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [320, 390, 1440].map((width) => ({
    name: `chromium-${width}`,
    use: { viewport: { width, height: width === 320 ? 568 : width === 390 ? 844 : 900 } },
  })),
  // Usa el build real; rechaza un puerto ocupado para no probar otro checkout por accidente.
  webServer: {
    // --ignore-lock evita el segundo plano automático de Astro al detectar un agente;
    // Playwright conserva el proceso y lo cierra al terminar.
    command: 'npm run preview -- --host 127.0.0.1 --port 4327 --ignore-lock',
    url: 'http://127.0.0.1:4327',
    reuseExistingServer: false,
    timeout: 30_000,
  },
});
