import { HttpRequest } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { environment } from '../environments/environment';
import { App } from './app';
import { appConfig } from './app.config';

// Whole journeys through the real application: its configuration, its router and its lazy
// routes, with only the network replaced. No test goes out.

const BACKEND = environment.apiBaseUrl;
const SEARCH_DEBOUNCE_MS = 300;

const META = {
  countries: [{ code: 'ES', name: 'España', tax_rate_bp: 2100 }],
  plans: [{ code: 'professional', name: 'Profesional' }],
};
// The response of SPEC-04, 4.2.
const RATES = [
  { date: '2026-11-12', base: 'EUR', quote: 'CHF', rate: 0.92316 },
  { date: '2026-11-12', base: 'EUR', quote: 'GBP', rate: 0.83583 },
  { date: '2026-11-12', base: 'EUR', quote: 'USD', rate: 1.1139 },
];
const NEW_CUSTOMER = {
  company_name: 'Ejemplo Uno SL',
  tax_id: 'b-1234567 4',
  contact_email: 'compras@ejemplo-uno.example',
  country: 'ES',
  plan: 'professional',
};
const CUSTOMER = {
  ...NEW_CUSTOMER,
  id: 7,
  tax_id: 'B12345674',
  created_at: '2026-11-12T14:30:00Z',
  simulation_count: 0,
  simulations: [],
};
// The row of 10 users of SPEC-02, 5.1, with the shape of its contract.
const QUOTE = {
  currency: 'EUR',
  active_users: 10,
  tiers: [
    { from_users: 1, to_users: 10, unit_price_cents: 1000, users: 10, subtotal_cents: 10000 },
    { from_users: 11, to_users: 50, unit_price_cents: 800, users: 0, subtotal_cents: 0 },
    { from_users: 51, to_users: null, unit_price_cents: 500, users: 0, subtotal_cents: 0 },
  ],
  base_cents: 10000,
  country: 'ES',
  tax_rate_bp: 2100,
  tax_cents: 2100,
  total_cents: 12100,
};
const SIMULATION = {
  ...QUOTE,
  id: 1,
  customer_id: 7,
  storage_gb: 500,
  estimated_api_calls: 250000,
  created_at: '2026-11-12T15:00:00Z',
};
const WITH_SIMULATION = { ...CUSTOMER, simulation_count: 1, simulations: [SIMULATION] };

interface Journey {
  readonly fixture: ComponentFixture<App>;
  readonly page: HTMLElement;
  readonly controller: HttpTestingController;
  /** Every request to the backend, in the order in which the journey answered it. */
  readonly seen: HttpRequest<unknown>[];
}

async function settle(journey: Journey): Promise<void> {
  journey.fixture.detectChanges();
  await journey.fixture.whenStable();
  journey.fixture.detectChanges();
}

/** Starts the application at the panel, with `/meta` answered and the rates as given. */
async function start(rates: 'answered' | 'failed'): Promise<Journey> {
  TestBed.configureTestingModule({
    imports: [App],
    providers: [...appConfig.providers, provideHttpClientTesting()],
  });
  const fixture = TestBed.createComponent(App);
  const journey: Journey = {
    fixture,
    page: fixture.nativeElement as HTMLElement,
    controller: TestBed.inject(HttpTestingController),
    seen: [],
  };
  await go(journey, '/');
  const ratesRequests = journey.controller.match(environment.ratesUrl);
  expect(ratesRequests.length).toBe(1);
  if (rates === 'answered') {
    ratesRequests[0].flush(RATES);
  } else {
    ratesRequests[0].flush({ message: 'error' }, { status: 500, statusText: 'Error' });
  }
  await answer(journey, 'GET', '/meta', META);
  return journey;
}

async function go(journey: Journey, url: string): Promise<void> {
  await expect(TestBed.inject(Router).navigateByUrl(url)).resolves.toBe(true);
  await settle(journey);
}

/** Answers the one request to the backend that is waiting at that method and path. */
async function answer(
  journey: Journey,
  method: string,
  pathAndQuery: string,
  body: object,
  status = 200,
): Promise<void> {
  const waiting = journey.controller.match(
    (request) => request.method === method && request.urlWithParams === BACKEND + pathAndQuery,
  );
  expect(waiting.length).toBe(1);
  journey.seen.push(waiting[0].request);
  waiting[0].flush(body, { status, statusText: 'OK' });
  await settle(journey);
}

async function write(journey: Journey, id: string, text: string): Promise<void> {
  const control = journey.page.querySelector<HTMLInputElement | HTMLSelectElement>(`#${id}`);
  expect(control).not.toBeNull();
  if (control) {
    control.value = text;
    control.dispatchEvent(new Event(control instanceof HTMLSelectElement ? 'change' : 'input'));
  }
  await settle(journey);
}

async function press(journey: Journey, label: string): Promise<void> {
  const buttons = Array.from(journey.page.querySelectorAll<HTMLButtonElement>('main button'));
  const button = buttons.find((candidate) => candidate.textContent?.trim() === label);
  expect(button).toBeDefined();
  button?.click();
  await settle(journey);
}

async function pause(milliseconds: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, milliseconds));
}

/** Text with every run of white space, the no-break one included, as a single space. */
function clean(text: string | null | undefined): string {
  return (text ?? '').replace(/\s+/g, ' ').trim();
}

function fact(journey: Journey, term: string): string {
  const terms = Array.from(journey.page.querySelectorAll('main dt'));
  const found = terms.find((candidate) => clean(candidate.textContent) === term);
  return clean(found?.nextElementSibling?.textContent);
}

/** Panel, search, sign-up, detail, projection and saving, in that order. */
async function fullJourney(journey: Journey): Promise<void> {
  await answer(journey, 'GET', '/customers', { items: [] });
  await write(journey, 'panel-search', 'ejemplo');
  await pause(SEARCH_DEBOUNCE_MS + 50);
  await settle(journey);
  await answer(journey, 'GET', '/customers?q=ejemplo', { items: [] });

  await go(journey, '/clientes/nuevo');
  await write(journey, 'alta-name', NEW_CUSTOMER.company_name);
  await write(journey, 'alta-tax-id', NEW_CUSTOMER.tax_id);
  await write(journey, 'alta-email', NEW_CUSTOMER.contact_email);
  await write(journey, 'alta-country', NEW_CUSTOMER.country);
  await write(journey, 'alta-plan', NEW_CUSTOMER.plan);
  await press(journey, 'Guardar');
  await answer(journey, 'POST', '/customers', CUSTOMER, 201);
  await answer(journey, 'GET', '/customers/7', CUSTOMER);

  await go(journey, '/clientes/7/simulacion');
  await answer(journey, 'GET', '/customers/7', CUSTOMER);
  await answer(journey, 'POST', '/pricing/quote', QUOTE);
  await write(journey, 'simulador-storage', '500');
  await write(journey, 'simulador-calls', '250000');
}

async function saveAndSeeTheDetail(journey: Journey): Promise<void> {
  await press(journey, 'Guardar');
  await answer(journey, 'POST', '/simulations', SIMULATION, 201);
  await answer(journey, 'GET', '/customers/7', WITH_SIMULATION);
}

function bodies(journey: Journey): unknown[] {
  return journey.seen.filter((request) => request.method === 'POST').map((request) => request.body);
}

describe('Journeys · SPEC-04/E-31, E-52 (CA-09, CA-18)', () => {
  it('should call the backend only with GET and POST, no header of its own and the bodies of the contract', async () => {
    const journey = await start('answered');

    await fullJourney(journey);
    await saveAndSeeTheDetail(journey);

    expect(
      journey.seen.map(
        (request) => `${request.method} ${request.urlWithParams.replace(BACKEND, '')}`,
      ),
    ).toEqual([
      'GET /meta',
      'GET /customers',
      'GET /customers?q=ejemplo',
      'POST /customers',
      'GET /customers/7',
      'GET /customers/7',
      'POST /pricing/quote',
      'POST /simulations',
      'GET /customers/7',
    ]);
    expect(journey.seen.flatMap((request) => request.headers.keys())).toEqual([]);
    expect(journey.seen.map((request) => request.withCredentials)).not.toContain(true);
    expect(bodies(journey)).toEqual([
      NEW_CUSTOMER,
      { customer_id: 7, active_users: 10 },
      { customer_id: 7, active_users: 10, storage_gb: 500, estimated_api_calls: 250000 },
    ]);
    expect(journey.controller.match((request) => request.url.startsWith(BACKEND)).length).toBe(0);
    expect(TestBed.inject(Router).url).toBe('/clientes/7');
    expect(fact(journey, 'Total')).toBe('121,00 EUR');
  });

  it('should send neither the currency nor a converted amount while USD is shown', async () => {
    const journey = await start('answered');
    await write(journey, 'currency-select', 'USD');

    await fullJourney(journey);
    const shownBeforeSaving = [fact(journey, 'Total'), fact(journey, 'Total en EUR')];
    await saveAndSeeTheDetail(journey);

    expect(shownBeforeSaving).toEqual(['134,78 USD', '121,00 EUR']);
    expect(fact(journey, 'Total')).toBe('134,78 USD');
    expect(JSON.stringify(bodies(journey))).toBe(
      JSON.stringify([
        NEW_CUSTOMER,
        { customer_id: 7, active_users: 10 },
        { customer_id: 7, active_users: 10, storage_gb: 500, estimated_api_calls: 250000 },
      ]),
    );
    expect(journey.seen.map((request) => request.urlWithParams).join(' ')).not.toContain('USD');
  });
});

describe('Journeys · the public API of rates in error · SPEC-04/E-28, E-30 (CA-03)', () => {
  it('should show the panel, the detail and the simulator in EUR, with the notice in the header', async () => {
    const journey = await start('failed');

    await answer(journey, 'GET', '/customers', {
      items: [
        {
          id: 7,
          company_name: 'Ejemplo Uno SL',
          tax_id: 'B12345674',
          country: 'ES',
          plan: 'professional',
        },
      ],
    });
    const panel = clean(journey.page.querySelector('main .results')?.textContent);
    await go(journey, '/clientes/7');
    await answer(journey, 'GET', '/customers/7', WITH_SIMULATION);
    const detail = fact(journey, 'Total');
    await go(journey, '/clientes/7/simulacion');
    await answer(journey, 'GET', '/customers/7', WITH_SIMULATION);
    await answer(journey, 'POST', '/pricing/quote', QUOTE);

    expect(panel).toContain('Ejemplo Uno SL');
    expect(panel).toContain('España');
    expect(detail).toBe('121,00 EUR');
    expect(fact(journey, 'Total')).toBe('121,00 EUR');
    expect(journey.page.querySelector('main .rate-note')).toBeNull();
    const options = Array.from(journey.page.querySelectorAll('header select option'));
    expect(options.map((option) => option.textContent?.trim())).toEqual(['EUR']);
    expect(clean(journey.page.querySelector('header [role="alert"]')?.textContent)).toContain(
      'No se han podido cargar los tipos de cambio',
    );
  });
});
