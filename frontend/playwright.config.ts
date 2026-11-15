import { join } from 'node:path';

import { defineConfig, devices } from '@playwright/test';

import { temporaryFolder } from './e2e/support/temporary-folder';

// End-to-end tests of SPEC-04 (CA-13 and CA-14), against the real backend and the real frontend
// on their default ports, 8000 and 4200: what CA-14 checks is the backend with its default CORS,
// which only admits `http://localhost:4200`.
//
// Playwright starts both servers and never reuses one that is already running: with a port in
// use the run fails before starting anything on it (CLAUDE.md, rule 8). `port`, and not `url`,
// so that anything listening there counts as "in use", whatever it answers.
const BACKEND_PORT = 8000;
const FRONTEND_PORT = 4200;
const SERVER_START_TIMEOUT_MS = 120_000;

// The backend of the tests must run with its defaults: a variable of whoever runs them would
// replace the default CORS that CA-14 is about.
delete process.env['CORS_ORIGINS'];

export default defineConfig({
  testDir: './e2e',
  outputDir: './test-results',
  // One database for the whole run: the tests go one after another, in the order of the files.
  fullyParallel: false,
  workers: 1,
  retries: 0,
  forbidOnly: true,
  reporter: 'list',
  use: {
    baseURL: `http://localhost:${FRONTEND_PORT}`,
    // Dates with time are shown in the time zone of the browser: fixed, so that the result
    // does not depend on the machine.
    locale: 'es-ES',
    timezoneId: 'Europe/Madrid',
    trace: 'retain-on-failure',
    // No test calls an external service: the browser cannot resolve any host but the two of
    // the local servers. The API of exchange rates is answered before that, inside the browser
    // (`e2e/support/fixtures.ts`).
    launchOptions: {
      args: ['--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost, EXCLUDE 127.0.0.1'],
    },
  },
  projects: [
    {
      // What `npm run e2e` runs, and with it the oracle (`uv run scripts/check.py --e2e`).
      name: 'pruebas',
      testIgnore: '**/capturas/**',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      // Writes the screenshots of CA-15; only on request (`npm run e2e:capturas`).
      name: 'capturas',
      testMatch: '**/capturas/*.spec.ts',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      name: 'backend',
      command: 'uv run --locked uvicorn --factory app.main:create_app',
      cwd: '../backend',
      port: BACKEND_PORT,
      reuseExistingServer: false,
      timeout: SERVER_START_TIMEOUT_MS,
      env: { DATABASE_PATH: join(temporaryFolder(), 'e2e.db') },
    },
    {
      name: 'frontend',
      command: 'npm start',
      port: FRONTEND_PORT,
      reuseExistingServer: false,
      timeout: SERVER_START_TIMEOUT_MS,
    },
  ],
});
