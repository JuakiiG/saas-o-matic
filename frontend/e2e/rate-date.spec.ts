import { createCustomer, customerBody, saveSimulation } from './support/backend';
import { expect, test } from './support/fixtures';
import { RATES_DATE } from './support/rates';
import { currencySelect, projection, rateApplied } from './support/views';

// SPEC-04, 5.5, the row of the time zone (E-29; 2.6): the date of a rate has no time and is
// shown as it comes. A browser behind UTC that read it as a moment would show the day before.

const RATE_NOTE = '1 EUR = 1,1139 USD · tipo del 12/11/2026';

test.describe('Date of the exchange rate', () => {
  test.use({ timezoneId: 'America/Los_Angeles' });

  test('should show the date the rate brings when the browser is in a time zone behind UTC (SPEC-04/E-29, 5.5)', async ({
    page,
    request,
  }) => {
    const id = await createCustomer(request, customerBody('00000041H'));
    await saveSimulation(request, {
      customer_id: id,
      active_users: 15,
      storage_gb: 0,
      estimated_api_calls: 0,
    });

    await page.goto(`/clientes/${id}/simulacion`);
    // The premise of the test: in this browser, midnight UTC of that date is still the 11th.
    const dayHere = await page.evaluate(
      (date) => new Date(`${date}T00:00:00Z`).getDate(),
      RATES_DATE,
    );
    expect(dayHere).toBe(11);

    await currencySelect(page).selectOption('USD');
    await expect(rateApplied(projection(page))).toHaveText(RATE_NOTE);

    // The same note, over the history of the detail.
    await page.getByRole('link', { name: 'Volver al detalle' }).click();
    await expect(rateApplied(page)).toHaveText(RATE_NOTE);
  });
});
