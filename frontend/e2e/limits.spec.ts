import { Page } from '@playwright/test';

import { BACKEND_URL, createCustomer, customerBody, expectFieldRejected } from './support/backend';
import { expect, test } from './support/fixtures';
import { fact, historyCards, projection, resultCards } from './support/views';

// Known limitation L-09 (SPEC-04/E-41, E-22, E-50, E-53): the limits of the fields are written
// in the backend and again in the help of the browser, and nothing else checks that they match.
// Each case goes both ways against the real backend: the value on the limit is stored through
// the interface, and the value one step beyond is rejected by the help, which sends nothing,
// and by the backend when it is sent to it directly.

/** One text field of the sign-up form with its limit. */
interface AltaCase {
  readonly title: string;
  readonly field: 'company_name' | 'tax_id' | 'contact_email';
  readonly label: string;
  readonly taxId: string;
  readonly onLimit: string;
  readonly beyond: string;
  readonly help: string;
  readonly backendCode: string;
  /** What the detail shows once the value on the limit is stored. */
  readonly stored: string;
}

const EMAIL_DOMAIN = '@empresa.example';
const ALTA_CASES: readonly AltaCase[] = [
  {
    title: 'a name of 120 characters',
    field: 'company_name',
    label: 'Nombre de la empresa',
    taxId: '00000031P',
    onLimit: 'N'.repeat(120),
    beyond: 'N'.repeat(121),
    help: 'El nombre debe tener entre 2 y 120 caracteres.',
    backendCode: 'too_long',
    stored: 'N'.repeat(120),
  },
  {
    title: 'a name of 2 characters',
    field: 'company_name',
    label: 'Nombre de la empresa',
    taxId: '00000032D',
    onLimit: 'Ñu',
    beyond: 'Ñ',
    help: 'El nombre debe tener entre 2 y 120 caracteres.',
    backendCode: 'too_short',
    stored: 'Ñu',
  },
  {
    title: 'an email of 254 characters',
    field: 'contact_email',
    label: 'Email de contacto',
    taxId: '00000033X',
    onLimit: `${'e'.repeat(238)}${EMAIL_DOMAIN}`,
    beyond: `${'e'.repeat(239)}${EMAIL_DOMAIN}`,
    help: 'El email admite 254 caracteres como máximo.',
    backendCode: 'too_long',
    stored: `${'e'.repeat(238)}${EMAIL_DOMAIN}`,
  },
  {
    title: 'a tax id of 30 characters',
    field: 'tax_id',
    label: 'Identificador fiscal',
    taxId: '00000034B',
    // Measured untrimmed: the spaces count, and the backend drops them when it normalizes.
    onLimit: `00000034B${' '.repeat(21)}`,
    beyond: `00000034B${' '.repeat(22)}`,
    help: 'El identificador fiscal admite 30 caracteres como máximo.',
    backendCode: 'too_long',
    stored: '00000034B',
  },
];

/** The requests of that method and path the page sends to the backend from now on. */
function watchRequests(page: Page, method: string, path: string): string[] {
  const seen: string[] = [];
  page.on('request', (request) => {
    const url = new URL(request.url());
    if (
      request.method() === method &&
      request.url().startsWith(BACKEND_URL) &&
      url.pathname === path
    ) {
      seen.push(request.url());
    }
  });
  return seen;
}

async function fillAlta(page: Page, body: ReturnType<typeof customerBody>): Promise<void> {
  await page.getByLabel('Nombre de la empresa').fill(body.company_name);
  await page.getByLabel('Identificador fiscal').fill(body.tax_id);
  await page.getByLabel('Email de contacto').fill(body.contact_email);
  await page.getByLabel('País').selectOption(body.country);
  await page.getByLabel('Plan').selectOption(body.plan);
}

test.describe('Limits of the fields (L-09)', () => {
  for (const limit of ALTA_CASES) {
    test(`should store ${limit.title} and reject one step beyond, in the help and in the backend (L-09; SPEC-04/E-41)`, async ({
      page,
      request,
    }) => {
      const beyond = customerBody(limit.taxId, { [limit.field]: limit.beyond });
      const sent = watchRequests(page, 'POST', '/customers');
      await page.goto('/clientes/nuevo');

      // One step beyond: the help says so next to the field and nothing is sent.
      await fillAlta(page, beyond);
      await page.getByRole('button', { name: 'Guardar' }).click();
      await expect(page.getByText(limit.help)).toBeVisible();
      await expect(page).toHaveURL(/\/clientes\/nuevo$/);
      expect(sent).toEqual([]);

      // The backend rejects that same body.
      const rejected = await request.post(`${BACKEND_URL}/customers`, { data: beyond });
      await expectFieldRejected(rejected, limit.field, limit.backendCode);

      // On the limit: the help lets it through and the backend stores it.
      await page.getByLabel(limit.label).fill(limit.onLimit);
      await page.getByRole('button', { name: 'Guardar' }).click();
      await expect(page).toHaveURL(/\/clientes\/[0-9]+$/);
      await expect(page.getByText(limit.stored, { exact: true })).toBeVisible();
      expect(sent).toHaveLength(1);
    });
  }

  test('should store the largest counts and reject one more, in the help and in the backend (L-09; SPEC-04/E-22, E-36)', async ({
    page,
    request,
  }) => {
    const id = await createCustomer(request, customerBody('00000035N'));
    const counts = { customer_id: id, active_users: 15, storage_gb: 0, estimated_api_calls: 0 };
    const save = page.getByRole('button', { name: 'Guardar' });
    const users = page.getByLabel('Usuarios activos', { exact: true });
    const storage = page.getByLabel('Almacenamiento (GB)');
    const calls = page.getByLabel('Llamadas a la API estimadas');
    await page.goto(`/clientes/${id}/simulacion`);
    await expect(fact(projection(page), 'Total')).toHaveText('121,00 EUR');

    // One more than the limit of each field: the help says so and «Guardar» is disabled.
    await users.fill('100001');
    await expect(
      page.getByText('Escribe un número entero de 0 a 100.000, solo con cifras.'),
    ).toBeVisible();
    await expect(save).toBeDisabled();
    await users.fill('100000');
    await storage.fill('1000001');
    await expect(
      page.getByText('Escribe un número entero de 0 a 1.000.000, solo con cifras.'),
    ).toBeVisible();
    await expect(save).toBeDisabled();
    await storage.fill('1000000');
    await calls.fill('1000000001');
    await expect(
      page.getByText('Escribe un número entero de 0 a 1.000.000.000, solo con cifras.'),
    ).toBeVisible();
    await expect(save).toBeDisabled();
    await calls.fill('1000000000');

    // The backend rejects each of them: the users, both when projecting and when saving.
    const quote = { customer_id: id, active_users: 100_001 };
    const quoted = await request.post(`${BACKEND_URL}/pricing/quote`, { data: quote });
    await expectFieldRejected(quoted, 'active_users', 'out_of_range');
    for (const [field, value] of [
      ['active_users', 100_001],
      ['storage_gb', 1_000_001],
      ['estimated_api_calls', 1_000_000_001],
    ] as const) {
      const body = { ...counts, [field]: value };
      const rejected = await request.post(`${BACKEND_URL}/simulations`, { data: body });
      await expectFieldRejected(rejected, field, 'out_of_range');
    }

    // The three limits at once: projected, saved and shown in the detail.
    await expect(fact(projection(page), 'Total')).toHaveText('605.205,70 EUR');
    await save.click();
    await expect(historyCards(page)).toHaveCount(1);
    const card = historyCards(page).nth(0);
    await expect(fact(card, 'Usuarios activos')).toHaveText('100.000');
    await expect(fact(card, 'Almacenamiento')).toHaveText('1.000.000 GB');
    await expect(fact(card, 'Llamadas a la API')).toHaveText('1.000.000.000');
    await expect(fact(card, 'Total')).toHaveText('605.205,70 EUR');
  });

  test('should search with 100 characters and reject 101, in the help and in the backend (L-09; SPEC-04/E-50)', async ({
    page,
    request,
  }) => {
    const sent = watchRequests(page, 'GET', '/customers');
    await page.goto('/');
    await expect(page.getByLabel('Buscar cliente')).toBeVisible();
    const initial = sent.length;

    await page.getByLabel('Buscar cliente').fill('x'.repeat(101));
    await expect(
      page.getByText('El texto de búsqueda admite 100 caracteres como máximo'),
    ).toBeVisible();
    const rejected = await request.get(`${BACKEND_URL}/customers`, {
      params: { q: 'x'.repeat(101) },
    });
    await expectFieldRejected(rejected, 'q', 'too_long');

    await page.getByLabel('Buscar cliente').fill('x'.repeat(100));
    await expect(page.getByText('No hay clientes que coincidan.')).toBeVisible();
    // The only search sent is the one of 100 characters: the one of 101 never left.
    expect(sent.slice(initial)).toEqual([`${BACKEND_URL}/customers?q=${'x'.repeat(100)}`]);
  });

  test('should show 20 customers and the note of the maximum when 21 match (L-09; SPEC-04/E-53)', async ({
    page,
    request,
  }) => {
    const taxIds = [
      ...[
        '00000101D',
        '00000102X',
        '00000103B',
        '00000104N',
        '00000105J',
        '00000106Z',
        '00000107S',
      ],
      ...[
        '00000108Q',
        '00000109V',
        '00000110H',
        '00000111L',
        '00000112C',
        '00000113K',
        '00000114E',
      ],
      ...[
        '00000115T',
        '00000116R',
        '00000117W',
        '00000118A',
        '00000119G',
        '00000120M',
        '00000121Y',
      ],
    ];
    for (const taxId of taxIds) {
      await createCustomer(request, customerBody(taxId, { company_name: `Tope ${taxId} SL` }));
    }

    await page.goto('/');
    await page.getByLabel('Buscar cliente').fill('Tope');

    await expect(resultCards(page)).toHaveCount(20);
    await expect(
      page.getByText(
        'Se muestran como máximo 20 clientes. Escribe más texto para afinar la búsqueda.',
      ),
    ).toBeVisible();
  });
});
