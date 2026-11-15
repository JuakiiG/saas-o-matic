import { defineConfig } from '@playwright/test';

import tests from './playwright.config';

// The screenshots of SPEC-04/CA-15: the same servers, browser and rules as the end-to-end tests,
// pointed at `e2e/capturas/`. They overwrite the versioned files of
// `ai-workspace/04-calidad/capturas/`, so they run only on request, with `npm run e2e:capturas`
// (`playwright test -c playwright.capturas.config.ts`), and never with the default configuration.
export default defineConfig({
  ...tests,
  testDir: './e2e/capturas',
  // The default configuration leaves this folder out; here it is the only one.
  testIgnore: [],
});
