import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';

import { BACKEND_BASE_URL } from '../../core/backend-api';
import { DisplayCurrency } from '../../core/display-currency';
import { formatDateTime } from '../../core/format';
import { MetaStore } from '../../core/meta-store';
import { Detalle } from './detalle';

const META_URL = `${BACKEND_BASE_URL}/meta`;
const CUSTOMERS_URL = `${BACKEND_BASE_URL}/customers/`;
const ARABIC_DIGIT_ONE = String.fromCodePoint(0x661);
const UNAVAILABLE = 'El servicio no está disponible en este momento.';
const UNEXPECTED = 'Se ha producido un error inesperado.';
const OFFLINE = 'No se ha podido conectar con el servidor.';

const META = {
  countries: [
    { code: 'ES', name: 'España', tax_rate_bp: 2100 },
    { code: 'PT', name: 'Portugal', tax_rate_bp: 2300 },
  ],
  plans: [
    { code: 'starter', name: 'Básico' },
    { code: 'professional', name: 'Profesional' },
  ],
};

// The simulation of SPEC-03, 4.1 (15 users), and the row of 51 users of SPEC-02, 5.1.
const OF_15_USERS = {
  id: 1,
  customer_id: 1,
  active_users: 15,
  storage_gb: 500,
  estimated_api_calls: 250000,
  currency: 'EUR',
  tiers: [
    { from_users: 1, to_users: 10, unit_price_cents: 1000, users: 10, subtotal_cents: 10000 },
    { from_users: 11, to_users: 50, unit_price_cents: 800, users: 5, subtotal_cents: 4000 },
    { from_users: 51, to_users: null, unit_price_cents: 500, users: 0, subtotal_cents: 0 },
  ],
  base_cents: 14000,
  country: 'ES',
  tax_rate_bp: 2100,
  tax_cents: 2940,
  total_cents: 16940,
  created_at: '2026-11-12T15:00:00Z',
};
const OF_51_USERS = {
  ...OF_15_USERS,
  id: 2,
  active_users: 51,
  storage_gb: 0,
  estimated_api_calls: 0,
  tiers: [
    { from_users: 1, to_users: 10, unit_price_cents: 1000, users: 10, subtotal_cents: 10000 },
    { from_users: 11, to_users: 50, unit_price_cents: 800, users: 40, subtotal_cents: 32000 },
    { from_users: 51, to_users: null, unit_price_cents: 500, users: 1, subtotal_cents: 500 },
  ],
  base_cents: 42500,
  tax_cents: 8925,
  total_cents: 51425,
  created_at: '2026-11-12T15:05:00Z',
};
// The example of SPEC-03, 4.2: the last one saved comes first.
const CUSTOMER = {
  id: 1,
  company_name: 'Ejemplo Uno SL',
  tax_id: 'B12345674',
  contact_email: 'compras@ejemplo-uno.example',
  country: 'ES',
  plan: 'professional',
  created_at: '2026-11-12T14:30:00Z',
  simulation_count: 2,
  simulations: [OF_51_USERS, OF_15_USERS],
};
const WITHOUT_SIMULATIONS = { ...CUSTOMER, simulation_count: 0, simulations: [] };

@Component({ template: '', changeDetection: ChangeDetectionStrategy.OnPush })
class Blank {}

interface Page {
  readonly harness: RouterTestingHarness;
  readonly element: HTMLElement;
  readonly controller: HttpTestingController;
}

async function open(url: string, meta: 'answered' | 'failed' = 'answered'): Promise<Page> {
  TestBed.configureTestingModule({
    providers: [
      provideRouter([
        { path: 'clientes/:id', component: Detalle },
        { path: 'clientes/:id/simulacion', component: Blank },
        { path: '', component: Blank },
      ]),
      provideHttpClient(),
      provideHttpClientTesting(),
    ],
  });
  const controller = TestBed.inject(HttpTestingController);
  TestBed.inject(MetaStore).load();
  for (const request of controller.match(META_URL)) {
    if (meta === 'answered') {
      request.flush(META);
    } else {
      request.flush({ code: 'internal_error' }, { status: 500, statusText: 'Error' });
    }
  }
  const harness = await RouterTestingHarness.create(url);
  const element = harness.routeNativeElement;
  expect(element).not.toBeNull();
  return { harness, element: element as HTMLElement, controller };
}

/** The requests for a customer made since the last time they were asked for. */
function customerRequests(page: Page): TestRequest[] {
  return page.controller.match((request) => request.url.startsWith(CUSTOMERS_URL));
}

function onlyCustomerRequest(page: Page): TestRequest {
  const requests = customerRequests(page);
  expect(requests.length).toBe(1);
  return requests[0];
}

function answer(page: Page, body: object): void {
  onlyCustomerRequest(page).flush(body);
  page.harness.detectChanges();
}

function reject(page: Page, status: number, body: object | string): void {
  onlyCustomerRequest(page).flush(body, { status, statusText: 'Error' });
  page.harness.detectChanges();
}

async function openWith(body: object, url = '/clientes/1'): Promise<Page> {
  const page = await open(url);
  answer(page, body);
  return page;
}

/** Text with every run of white space, the no-break one included, as a single space. */
function clean(text: string | null | undefined): string {
  return (text ?? '').replace(/\s+/g, ' ').trim();
}

function heading(page: Page): string {
  return clean(page.element.querySelector('h1')?.textContent);
}

/** The terms of a description list with their values. */
function facts(list: Element | null): Record<string, string> {
  const found: Record<string, string> = {};
  for (const term of Array.from(list?.querySelectorAll('dt') ?? [])) {
    found[clean(term.textContent)] = clean(term.nextElementSibling?.textContent);
  }
  return found;
}

function simulationCards(page: Page): Element[] {
  return Array.from(page.element.querySelectorAll('.simulation'));
}

function link(page: Page, label: string): string | null {
  const links = Array.from(page.element.querySelectorAll('a'));
  return (
    links.find((candidate) => clean(candidate.textContent) === label)?.getAttribute('href') ?? null
  );
}

function press(page: Page, label: string): void {
  const buttons = Array.from(page.element.querySelectorAll('button'));
  const button = buttons.find((candidate) => clean(candidate.textContent) === label);
  expect(button).toBeDefined();
  button?.click();
  page.harness.detectChanges();
}

describe('Detalle · SPEC-04/E-12 a E-15, E-35, E-40, E-47 (CA-07, CA-16, CA-17)', () => {
  it('should ask for the customer of the route and show the loading state meanwhile', async () => {
    const page = await open('/clientes/1');

    const urls = customerRequests(page).map((request) => request.request.urlWithParams);

    expect(urls).toEqual([`${CUSTOMERS_URL}1`]);
    expect(clean(page.element.querySelector('[role="status"]')?.textContent)).toBe(
      'Cargando el cliente…',
    );
  });

  it('should show the data of the customer, with the names of its country and plan', async () => {
    const page = await openWith(CUSTOMER);

    const card = page.element.querySelector('.customer');

    expect(clean(card?.querySelector('h2')?.textContent)).toBe('Ejemplo Uno SL');
    expect(facts(card)).toEqual({
      'Identificador fiscal': 'B12345674',
      'Email de contacto': 'compras@ejemplo-uno.example',
      País: 'España',
      Plan: 'Profesional',
      'Fecha de alta': formatDateTime(CUSTOMER.created_at),
    });
  });

  it('should carry in each date the moment the backend sent', async () => {
    const page = await openWith(CUSTOMER);

    const moments = Array.from(page.element.querySelectorAll('time')).map((time) =>
      time.getAttribute('datetime'),
    );

    expect(moments).toEqual([CUSTOMER.created_at, OF_51_USERS.created_at, OF_15_USERS.created_at]);
  });

  it('should show the code as it arrives when /meta does not bring that country or plan', async () => {
    const page = await openWith({ ...CUSTOMER, country: 'XX', plan: 'legacy' });

    const shown = facts(page.element.querySelector('.customer'));

    expect(shown['País']).toBe('XX');
    expect(shown['Plan']).toBe('legacy');
  });

  it('should show one card per simulation, in the order of the API', async () => {
    const page = await openWith(CUSTOMER);

    const totals = simulationCards(page).map((card) => facts(card.querySelector('dl'))['Total']);

    expect(totals).toEqual(['514,25 EUR', '169,40 EUR']);
  });

  it('should show of a simulation its date, what was asked and what it costs', async () => {
    const page = await openWith(CUSTOMER);

    const card = simulationCards(page)[1];

    expect(clean(card.querySelector('time')?.textContent)).toBe(
      formatDateTime(OF_15_USERS.created_at),
    );
    expect(facts(card.querySelector('dl'))).toEqual({
      'Usuarios activos': '15',
      Almacenamiento: '500 GB',
      'Llamadas a la API': '250.000',
      'Coste base': '140,00 EUR',
      'Impuesto (21 %)': '29,40 EUR',
      Total: '169,40 EUR',
    });
  });

  it('should keep the tiers of a simulation in a block that starts folded', async () => {
    const page = await openWith(CUSTOMER);

    const block = simulationCards(page)[1].querySelector('details');
    const tiers = Array.from(block?.querySelectorAll('.tier') ?? []).map((tier) =>
      Array.from(tier.children).map((part) => clean(part.textContent)),
    );

    expect(block?.open).toBe(false);
    expect(clean(block?.querySelector('summary')?.textContent)).toBe('Desglose por tramos');
    expect(tiers).toEqual([
      ['del 1 al 10', '10 × 10,00 EUR', '100,00 EUR'],
      ['del 11 al 50', '5 × 8,00 EUR', '40,00 EUR'],
      ['del 51 en adelante', '0 × 5,00 EUR', '0,00 EUR'],
    ]);
  });

  it('should say how many it shows when the customer has more simulations than arrived', async () => {
    const fifty = Array.from({ length: 50 }, (_unused, index) => ({
      ...OF_15_USERS,
      id: 55 - index,
    }));

    const page = await openWith({ ...CUSTOMER, simulation_count: 55, simulations: fifty });

    expect(simulationCards(page).length).toBe(50);
    expect(clean(page.element.querySelector('.history-note')?.textContent)).toBe(
      'Se muestran las 50 últimas de 55',
    );
  });

  it('should not say how many it shows when all of them arrived', async () => {
    const page = await openWith(CUSTOMER);

    expect(simulationCards(page).length).toBe(2);
    expect(page.element.querySelector('.history-note')).toBeNull();
  });

  it('should show a message and a link to the simulator when there are no simulations', async () => {
    const page = await openWith(WITHOUT_SIMULATIONS);

    expect(clean(page.element.querySelector('.empty')?.textContent)).toContain(
      'Este cliente todavía no tiene simulaciones.',
    );
    expect(link(page, 'Crear la primera simulación')).toBe('/clientes/1/simulacion');
    expect(simulationCards(page).length).toBe(0);
  });

  it('should offer the simulator of this customer', async () => {
    const page = await openWith({ ...CUSTOMER, id: 7 }, '/clientes/7');

    expect(link(page, 'Nueva simulación')).toBe('/clientes/7/simulacion');
  });

  // SPEC-04, 5.7: the rows that never reach the API.
  it.each([
    '/clientes/abc',
    '/clientes/01',
    '/clientes/+1',
    '/clientes/1.0',
    '/clientes/1e0',
    '/clientes/1_0',
    '/clientes/1%20',
    '/clientes/0',
    '/clientes/-1',
    `/clientes/${ARABIC_DIGIT_ONE}`,
    '/clientes/9007199254740993',
    '/clientes/99999999999999999',
  ])('should show «Cliente no encontrado» without asking when the route is %s', async (url) => {
    const page = await open(url);

    expect(customerRequests(page).length).toBe(0);
    expect(heading(page)).toBe('Cliente no encontrado');
    expect(link(page, 'Volver al panel')).toBe('/');
  });

  // SPEC-04, 5.7: the filter sees the segment the router has already decoded, so an encoded
  // digit is that digit and a matrix parameter is not part of the id.
  it.each(['/clientes/%31', '/clientes/1;x=y'])(
    'should ask for /customers/1 and show its detail when the route is %s',
    async (url) => {
      const page = await open(url);

      const request = onlyCustomerRequest(page);
      request.flush(CUSTOMER);
      page.harness.detectChanges();

      expect(request.request.urlWithParams).toBe(`${CUSTOMERS_URL}1`);
      expect(clean(page.element.querySelector('.customer h2')?.textContent)).toBe('Ejemplo Uno SL');
    },
  );

  it.each(['999', '9007199254740991'])(
    'should ask for /customers/%s, with that exact text, and show «Cliente no encontrado» on its 404',
    async (id) => {
      const page = await open(`/clientes/${id}`);

      const request = onlyCustomerRequest(page);
      request.flush(
        { status: 404, code: 'customer_not_found', detail: 'Un texto.' },
        { status: 404, statusText: 'Not Found' },
      );
      page.harness.detectChanges();

      expect(request.request.urlWithParams).toBe(`${CUSTOMERS_URL}${id}`);
      expect(heading(page)).toBe('Cliente no encontrado');
      expect(link(page, 'Volver al panel')).toBe('/');
    },
  );

  it.each<[string, number, object | string, string]>([
    ['422 validation_error', 422, { code: 'validation_error', errors: [] }, UNEXPECTED],
    ['404 not_found', 404, { code: 'not_found' }, UNEXPECTED],
    ['503 service_unavailable', 503, { code: 'service_unavailable' }, UNAVAILABLE],
    ['500 internal_error', 500, { code: 'internal_error' }, UNEXPECTED],
    ['a code it does not know', 418, { code: 'teapot' }, UNEXPECTED],
    ['502 with a body that is not JSON', 502, '<html>Bad Gateway</html>', UNEXPECTED],
  ])(
    'should show its notice with a retry, and not «Cliente no encontrado», on %s',
    async (_case, status, body, expected) => {
      const page = await open('/clientes/7');

      reject(page, status, body);

      expect(clean(page.element.querySelector('[role="alert"]')?.textContent)).toContain(expected);
      expect(heading(page)).not.toBe('Cliente no encontrado');
      press(page, 'Reintentar');
      expect(onlyCustomerRequest(page).request.urlWithParams).toBe(`${CUSTOMERS_URL}7`);
    },
  );

  it('should show the connection notice with a retry when no response arrives', async () => {
    const page = await open('/clientes/7');

    onlyCustomerRequest(page).error(new ProgressEvent('error'));
    page.harness.detectChanges();

    const alert = page.element.querySelector('[role="alert"]');
    expect(clean(alert?.textContent)).toContain(OFFLINE);
    expect(clean(alert?.querySelector('button')?.textContent)).toBe('Reintentar');
  });

  it('should show the customer once a retry brings it', async () => {
    const page = await open('/clientes/1');
    reject(page, 503, { code: 'service_unavailable' });

    press(page, 'Reintentar');
    answer(page, CUSTOMER);

    expect(page.element.querySelector('[role="alert"]')).toBeNull();
    expect(clean(page.element.querySelector('.customer h2')?.textContent)).toBe('Ejemplo Uno SL');
  });

  it('should show the error of /meta with a retry, and no bare code, when /meta fails', async () => {
    const page = await open('/clientes/1', 'failed');
    answer(page, CUSTOMER);

    const alert = page.element.querySelector('[role="alert"]');

    expect(clean(alert?.textContent)).toContain(UNEXPECTED);
    expect(clean(alert?.querySelector('button')?.textContent)).toBe('Reintentar');
    expect(page.element.querySelector('.customer')).toBeNull();
    expect(clean(page.element.textContent)).not.toContain('professional');
  });

  // SPEC-04, 2.1: `/meta` and the customer are two requests, and each notice retries its own.
  // The two fail with different errors here, to tell one notice from the other.
  it('should show the notice of the customer, with its own retry, when the customer failed too and the retry of /meta succeeds', async () => {
    const page = await open('/clientes/1', 'failed');
    reject(page, 503, { code: 'service_unavailable' });
    expect(clean(page.element.querySelector('[role="alert"]')?.textContent)).toContain(UNEXPECTED);

    press(page, 'Reintentar');
    const retries = page.controller.match(META_URL);
    retries.forEach((request) => request.flush(META));
    page.harness.detectChanges();

    expect(retries.length).toBe(1);
    expect(customerRequests(page).length).toBe(0);
    expect(page.element.querySelector('.customer')).toBeNull();
    const notices = page.element.querySelectorAll('[role="alert"]');
    expect(notices.length).toBe(1);
    expect(clean(notices[0].textContent)).toContain(UNAVAILABLE);
    expect(clean(notices[0].querySelector('button')?.textContent)).toBe('Reintentar');

    press(page, 'Reintentar');

    expect(page.controller.match(META_URL).length).toBe(0);
    const request = onlyCustomerRequest(page);
    request.flush(CUSTOMER);
    page.harness.detectChanges();
    expect(request.request.urlWithParams).toBe(`${CUSTOMERS_URL}1`);
    expect(page.element.querySelector('[role="alert"]')).toBeNull();
    expect(clean(page.element.querySelector('.customer h2')?.textContent)).toBe('Ejemplo Uno SL');
    expect(facts(page.element.querySelector('.customer'))['País']).toBe('España');
  });

  it('should load the other customer when the route changes to it', async () => {
    const page = await openWith(CUSTOMER);

    await page.harness.navigateByUrl('/clientes/2');
    answer(page, { ...WITHOUT_SIMULATIONS, id: 2, company_name: 'Ejemplo Dos SL' });

    expect(clean(page.element.querySelector('.customer h2')?.textContent)).toBe('Ejemplo Dos SL');
  });
});

describe('Detalle · divisa · SPEC-04/E-27, E-29 (2.4, 2.6)', () => {
  it('should show each amount converted, the total in EUR of each simulation and the rate once, asking for nothing', async () => {
    const page = await openWith(CUSTOMER);

    TestBed.inject(DisplayCurrency).show({ code: 'USD', rate: 1.1139, date: '2026-11-12' });
    page.harness.detectChanges();

    expect(customerRequests(page).length).toBe(0);
    expect(facts(simulationCards(page)[1].querySelector('dl'))).toEqual({
      'Usuarios activos': '15',
      Almacenamiento: '500 GB',
      'Llamadas a la API': '250.000',
      'Coste base': '155,95 USD',
      'Impuesto (21 %)': '32,75 USD',
      Total: '188,69 USD',
      'Total en EUR': '169,40 EUR',
    });
    const rates = Array.from(page.element.querySelectorAll('.rate-applied'));
    expect(rates.map((rate) => clean(rate.textContent))).toEqual([
      '1 EUR = 1,1139 USD · tipo del 12/11/2026',
    ]);
  });

  it('should show neither a rate nor a total in EUR while the currency is EUR', async () => {
    const page = await openWith(CUSTOMER);

    expect(page.element.querySelector('.rate-note')).toBeNull();
    expect(Object.keys(facts(simulationCards(page)[1].querySelector('dl')))).not.toContain(
      'Total en EUR',
    );
  });
});
