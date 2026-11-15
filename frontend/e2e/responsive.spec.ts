import { Page } from '@playwright/test';

import { createCustomer, customerBody, saveSimulation } from './support/backend';
import { expect, test } from './support/fixtures';
import { currencySelect, fact, historyCards, projection, resultCards } from './support/views';

// SPEC-04/CA-13 (E-16): at 375 px of width none of the four views scrolls sideways. Each view
// is checked with the content that stretches it most: the longest name and email the backend
// stores, written without a space to break at, the largest amounts and another currency.

const WIDTH = 375;
const LONGEST_NAME = 'W'.repeat(120);
const LONGEST_EMAIL = `${'w'.repeat(238)}@empresa.example`;
const MOST_USERS = 100_000;

/** The page is as wide as the window: nothing sticks out to the right. */
async function expectNoHorizontalScroll(page: Page): Promise<void> {
  const widths = await page.evaluate(() => ({
    window: window.innerWidth,
    visible: document.documentElement.clientWidth,
    content: document.documentElement.scrollWidth,
  }));
  expect(widths.window).toBe(WIDTH);
  expect(widths.content, 'width of the content, in px').toBeLessThanOrEqual(widths.visible);
}

test.describe('Width of 375 px', () => {
  test.use({ viewport: { width: WIDTH, height: 667 } });

  test('should not scroll sideways in the panel when it lists a customer with the longest name (SPEC-04/CA-13)', async ({
    page,
    request,
  }) => {
    await createCustomer(request, customerBody('00000021K', { company_name: LONGEST_NAME }));

    await page.goto('/');
    await page.getByLabel('Buscar cliente').fill(LONGEST_NAME.slice(0, 100));

    await expect(resultCards(page)).toHaveCount(1);
    await expectNoHorizontalScroll(page);
  });

  test('should not scroll sideways in the sign-up form when it shows the help of every field (SPEC-04/CA-13)', async ({
    page,
  }) => {
    await page.goto('/clientes/nuevo');
    await expect(page.getByLabel('Nombre de la empresa')).toBeVisible();
    await expectNoHorizontalScroll(page);

    await page.getByRole('button', { name: 'Guardar' }).click();

    await expect(page.getByText('Elige un plan.')).toBeVisible();
    await expectNoHorizontalScroll(page);
  });

  test('should not scroll sideways in the detail when it shows the longest texts and an open breakdown in another currency (SPEC-04/CA-13)', async ({
    page,
    request,
  }) => {
    const body = customerBody('00000022E', {
      company_name: LONGEST_NAME,
      contact_email: LONGEST_EMAIL,
    });
    const id = await createCustomer(request, body);
    await saveSimulation(request, {
      customer_id: id,
      active_users: MOST_USERS,
      storage_gb: 1_000_000,
      estimated_api_calls: 1_000_000_000,
    });

    await page.goto(`/clientes/${id}`);
    await expect(historyCards(page)).toHaveCount(1);
    await expectNoHorizontalScroll(page);

    await currencySelect(page).selectOption('USD');
    await historyCards(page).nth(0).getByText('Desglose por tramos').click();

    await expect(fact(historyCards(page).nth(0), 'Total en EUR')).toHaveText('605.205,70 EUR');
    await expectNoHorizontalScroll(page);
  });

  test('should not scroll sideways in the simulator when it projects the largest amounts in another currency (SPEC-04/CA-13)', async ({
    page,
    request,
  }) => {
    const id = await createCustomer(
      request,
      customerBody('00000023T', { company_name: LONGEST_NAME }),
    );

    await page.goto(`/clientes/${id}/simulacion`);
    await page.getByLabel('Usuarios activos', { exact: true }).fill(String(MOST_USERS));
    await expect(fact(projection(page), 'Total')).toHaveText('605.205,70 EUR');
    await expectNoHorizontalScroll(page);

    await currencySelect(page).selectOption('USD');

    await expect(fact(projection(page), 'Total en EUR')).toHaveText('605.205,70 EUR');
    await expectNoHorizontalScroll(page);
  });

  test.describe('with the exchange rates down', () => {
    test.use({ ratesDown: true });

    test('should not scroll sideways when the header shows the notice of the failure of the rates (SPEC-04/CA-13, E-30)', async ({
      page,
    }) => {
      await page.goto('/');

      await expect(
        page.getByText(
          'No se han podido cargar los tipos de cambio. Los importes se muestran en EUR.',
        ),
      ).toBeVisible();
      await expect(
        page.getByRole('banner').getByRole('button', { name: 'Reintentar' }),
      ).toBeVisible();
      await expectNoHorizontalScroll(page);
    });
  });
});
