import { join } from 'node:path';

import { APIRequestContext, Page } from '@playwright/test';

import { createCustomer, saveSimulation } from '../support/backend';
import { expect, test } from '../support/fixtures';
import { currencySelect, fact, historyCards, projection, resultCards } from '../support/views';

// SPEC-04/CA-15 (E-16): screenshots of the four views at 375 px and at 1280 px, with example
// data, as a complement of CA-13. They are written to `ai-workspace/04-calidad/capturas/` and
// reviewed by a person; this file asserts only what it needs to know that a view is complete
// before taking its picture. Not part of `npm run e2e`: run it with `npm run e2e:capturas`.

const FOLDER = join(__dirname, '..', '..', '..', 'ai-workspace', '04-calidad', 'capturas');
const SIZES = [
  { width: 375, height: 667 },
  { width: 1280, height: 800 },
] as const;
const RATES_NOTICE =
  'No se han podido cargar los tipos de cambio. Los importes se muestran en EUR.';

/** The customer whose detail and simulator are captured; set once, before the first test. */
let customerId = 0;

/** Three example customers; the first one, with three simulations. Gives the id of the first. */
async function createExampleData(request: APIRequestContext): Promise<number> {
  const id = await createCustomer(request, {
    company_name: 'Ejemplo Uno SL',
    tax_id: 'B12345674',
    contact_email: 'compras@ejemplo-uno.example',
    country: 'ES',
    plan: 'professional',
  });
  await createCustomer(request, {
    company_name: 'Ejemplo Dos SL',
    tax_id: '12345678Z',
    contact_email: 'administracion@ejemplo-dos.example',
    country: 'ES',
    plan: 'starter',
  });
  await createCustomer(request, {
    company_name: 'Ejemplo Tres SA',
    tax_id: '00000051M',
    contact_email: 'contacto@ejemplo-tres.example',
    country: 'ES',
    plan: 'enterprise',
  });
  for (const [users, storage, calls] of [
    [10, 0, 0],
    [51, 2000, 1_000_000],
    [15, 500, 250_000],
  ] as const) {
    await saveSimulation(request, {
      customer_id: id,
      active_users: users,
      storage_gb: storage,
      estimated_api_calls: calls,
    });
  }
  return id;
}

async function capture(page: Page, name: string): Promise<void> {
  const width = page.viewportSize()?.width;
  await page.screenshot({
    path: join(FOLDER, `${name}-${width}.png`),
    fullPage: true,
    animations: 'disabled',
  });
}

test.beforeAll(async ({ playwright }) => {
  const request = await playwright.request.newContext();
  try {
    customerId = await createExampleData(request);
  } finally {
    await request.dispose();
  }
});

for (const size of SIZES) {
  test.describe(`Screenshots at ${size.width} px`, () => {
    test.use({ viewport: size });

    test(`should capture the four views and the simulator in another currency at ${size.width} px (SPEC-04/CA-15)`, async ({
      page,
    }) => {
      await page.goto('/');
      await expect(resultCards(page)).toHaveCount(3);
      await capture(page, 'panel');

      await page.goto('/clientes/nuevo');
      await page.getByLabel('Nombre de la empresa').fill('Ejemplo Cuatro SL');
      await page.getByLabel('Identificador fiscal').fill('00000052Y');
      await page.getByLabel('Email de contacto').fill('compras@ejemplo-cuatro.example');
      await page.getByLabel('País').selectOption({ label: 'España' });
      await page.getByLabel('Plan').selectOption({ label: 'Básico' });
      await capture(page, 'alta');

      await page.goto(`/clientes/${customerId}`);
      await expect(historyCards(page)).toHaveCount(3);
      await capture(page, 'detalle');

      await page.goto(`/clientes/${customerId}/simulacion`);
      await page.getByLabel('Usuarios activos', { exact: true }).fill('15');
      await page.getByLabel('Almacenamiento (GB)').fill('500');
      await page.getByLabel('Llamadas a la API estimadas').fill('250000');
      await expect(fact(projection(page), 'Total')).toHaveText('169,40 EUR');
      await capture(page, 'simulador');

      await currencySelect(page).selectOption('USD');
      await expect(fact(projection(page), 'Total')).toHaveText('188,69 USD');
      await capture(page, 'simulador-usd');
    });

    test.describe('with the exchange rates down', () => {
      test.use({ ratesDown: true });

      test(`should capture the header with the notice of the failure of the rates at ${size.width} px (SPEC-04/CA-15, E-30)`, async ({
        page,
      }) => {
        await page.goto('/');
        await expect(page.getByText(RATES_NOTICE)).toBeVisible();
        await expect(resultCards(page)).toHaveCount(3);
        await capture(page, 'cabecera-aviso');
      });
    });
  });
}
