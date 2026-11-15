import { expect, test } from './support/fixtures';
import { fact, historyCards, projection } from './support/views';

// SPEC-04/CA-14 (E-08, E-12, E-24, E-52): the whole journey in a real browser, against the real
// backend with its default CORS. A header of the application or a method the backend does not
// admit would make the preflight of the browser fail, and the journey with it.

test.describe('Journey', () => {
  test('should show the new simulation first in the detail when a customer is created and two simulations are saved (SPEC-04/CA-14)', async ({
    page,
  }) => {
    await page.goto('/');
    await page.getByRole('link', { name: 'Nuevo cliente' }).click();

    await page.getByLabel('Nombre de la empresa').fill('Recorrido Uno SL');
    await page.getByLabel('Identificador fiscal').fill('00000001r');
    await page.getByLabel('Email de contacto').fill('compras@recorrido-uno.example');
    await page.getByLabel('País').selectOption({ label: 'España' });
    await page.getByLabel('Plan').selectOption({ label: 'Profesional' });
    await page.getByRole('button', { name: 'Guardar' }).click();

    // The detail of the customer just created, with what the backend stored (E-08).
    await expect(page).toHaveURL(/\/clientes\/[0-9]+$/);
    await expect(page.getByRole('heading', { name: 'Recorrido Uno SL' })).toBeVisible();
    await expect(page.getByText('00000001R', { exact: true })).toBeVisible();
    await expect(page.getByText('Este cliente todavía no tiene simulaciones.')).toBeVisible();

    // A first simulation, with the 10 users the simulator opens with.
    await page.getByRole('link', { name: 'Nueva simulación' }).click();
    await expect(fact(projection(page), 'Total')).toHaveText('121,00 EUR');
    await page.getByRole('button', { name: 'Guardar' }).click();
    await expect(historyCards(page)).toHaveCount(1);

    // A second one, with other values: it must come first (E-12, E-24).
    await page.getByRole('link', { name: 'Nueva simulación' }).click();
    await page.getByLabel('Usuarios activos', { exact: true }).fill('15');
    await page.getByLabel('Almacenamiento (GB)').fill('500');
    await page.getByLabel('Llamadas a la API estimadas').fill('250000');
    await expect(fact(projection(page), 'Total')).toHaveText('169,40 EUR');
    await page.getByRole('button', { name: 'Guardar' }).click();

    await expect(page).toHaveURL(/\/clientes\/[0-9]+$/);
    await expect(historyCards(page)).toHaveCount(2);
    const newest = historyCards(page).nth(0);
    await expect(fact(newest, 'Usuarios activos')).toHaveText('15');
    await expect(fact(newest, 'Almacenamiento')).toHaveText('500 GB');
    await expect(fact(newest, 'Llamadas a la API')).toHaveText('250.000');
    await expect(fact(newest, 'Total')).toHaveText('169,40 EUR');
    const oldest = historyCards(page).nth(1);
    await expect(fact(oldest, 'Usuarios activos')).toHaveText('10');
    await expect(fact(oldest, 'Total')).toHaveText('121,00 EUR');
  });
});
