import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router, convertToParamMap, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of } from 'rxjs';

import { BACKEND_BASE_URL } from '../../core/backend-api';
import { DisplayCurrency, DisplayedCurrency } from '../../core/display-currency';
import { MetaStore } from '../../core/meta-store';
import { Simulador } from './simulador';

const META_URL = `${BACKEND_BASE_URL}/meta`;
const CUSTOMERS_URL = `${BACKEND_BASE_URL}/customers/`;
const QUOTE_URL = `${BACKEND_BASE_URL}/pricing/quote`;
const SIMULATIONS_URL = `${BACKEND_BASE_URL}/simulations`;
const ARABIC_DIGIT_ONE = String.fromCodePoint(0x661);
const UNAVAILABLE = 'El servicio no está disponible en este momento.';
const UNEXPECTED = 'Se ha producido un error inesperado.';
const OFFLINE = 'No se ha podido conectar con el servidor.';
const TIMED_OUT = 'El servidor tarda demasiado en responder.';
const USERS = 'simulador-users';
const SLIDER = 'simulador-users-slider';
const STORAGE = 'simulador-storage';
const CALLS = 'simulador-calls';
const PROJECTION_NOTICE = '.projection-notice';
const SAVE_NOTICE = '.save-notice';

const META = {
  countries: [
    { code: 'ES', name: 'España', tax_rate_bp: 2100 },
    { code: 'PT', name: 'Portugal', tax_rate_bp: 2300 },
  ],
  plans: [{ code: 'professional', name: 'Profesional' }],
};
const CUSTOMER = {
  id: 7,
  company_name: 'Ejemplo Uno SL',
  tax_id: 'B12345674',
  contact_email: 'compras@ejemplo-uno.example',
  country: 'ES',
  plan: 'professional',
  created_at: '2026-11-12T14:30:00Z',
  simulation_count: 0,
  simulations: [],
};

/** A quote with the shape of SPEC-02, 4, and the amounts of a row of its table 5.1. */
function quoteOf(users: number, perTier: number[], subtotals: number[], amounts: number[]): object {
  const [base, tax, total] = amounts;
  return {
    currency: 'EUR',
    active_users: users,
    tiers: [
      {
        from_users: 1,
        to_users: 10,
        unit_price_cents: 1000,
        users: perTier[0],
        subtotal_cents: subtotals[0],
      },
      {
        from_users: 11,
        to_users: 50,
        unit_price_cents: 800,
        users: perTier[1],
        subtotal_cents: subtotals[1],
      },
      {
        from_users: 51,
        to_users: null,
        unit_price_cents: 500,
        users: perTier[2],
        subtotal_cents: subtotals[2],
      },
    ],
    base_cents: base,
    country: 'ES',
    tax_rate_bp: 2100,
    tax_cents: tax,
    total_cents: total,
  };
}
const OF_10 = quoteOf(10, [10, 0, 0], [10000, 0, 0], [10000, 2100, 12100]);
const OF_15 = quoteOf(15, [10, 5, 0], [10000, 4000, 0], [14000, 2940, 16940]);
const OF_51 = quoteOf(51, [10, 40, 1], [10000, 32000, 500], [42500, 8925, 51425]);
const OF_20000 = quoteOf(
  20000,
  [10, 40, 19950],
  [10000, 32000, 9975000],
  [10017000, 2103570, 12120570],
);
// The response of SPEC-03, 4.1, for the simulation these tests save.
const SAVED = {
  ...OF_10,
  id: 3,
  customer_id: 7,
  storage_gb: 500,
  estimated_api_calls: 250000,
  created_at: '2026-11-12T15:00:00Z',
};
const SAVED_BODY = {
  customer_id: 7,
  active_users: 10,
  storage_gb: 500,
  estimated_api_calls: 250000,
};

@Component({ template: '', changeDetection: ChangeDetectionStrategy.OnPush })
class Blank {}

interface Page {
  readonly fixture: ComponentFixture<Simulador>;
  readonly element: HTMLElement;
  readonly controller: HttpTestingController;
}

/** Opens the simulator on the route `/clientes/{routeId}/simulacion`; the customer is pending. */
function open(routeId = '7', meta: 'answered' | 'failed' = 'answered'): Page {
  TestBed.configureTestingModule({
    providers: [
      provideRouter([{ path: 'clientes/:id', component: Blank }]),
      provideHttpClient(),
      provideHttpClientTesting(),
      { provide: ActivatedRoute, useValue: { paramMap: of(convertToParamMap({ id: routeId })) } },
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
  const fixture = TestBed.createComponent(Simulador);
  fixture.detectChanges();
  return { fixture, element: fixture.nativeElement as HTMLElement, controller };
}

interface RoutedPage {
  readonly harness: RouterTestingHarness;
  readonly controller: HttpTestingController;
}

/** Opens the simulator by its address, so its id is the segment the router has decoded. */
async function openThroughRouter(url: string): Promise<RoutedPage> {
  TestBed.configureTestingModule({
    providers: [
      provideRouter([{ path: 'clientes/:id/simulacion', component: Simulador }]),
      provideHttpClient(),
      provideHttpClientTesting(),
    ],
  });
  const controller = TestBed.inject(HttpTestingController);
  TestBed.inject(MetaStore).load();
  for (const request of controller.match(META_URL)) {
    request.flush(META);
  }
  const harness = await RouterTestingHarness.create(url);
  return { harness, controller };
}

function customerRequests(page: Page): TestRequest[] {
  return page.controller.match((request) => request.url.startsWith(CUSTOMERS_URL));
}

function quoteRequests(page: Page): TestRequest[] {
  return page.controller.match((request) => request.url === QUOTE_URL);
}

function simulationRequests(page: Page): TestRequest[] {
  return page.controller.match((request) => request.url === SIMULATIONS_URL);
}

function only(requests: TestRequest[]): TestRequest {
  expect(requests.length).toBe(1);
  return requests[0];
}

function flush(page: Page, request: TestRequest, body: object | string, status = 200): void {
  request.flush(body, { status, statusText: status < 400 ? 'OK' : 'Error' });
  page.fixture.detectChanges();
}

/** The customer of the route arrives. */
function arrive(page: Page, customer: object = CUSTOMER): void {
  flush(page, only(customerRequests(page)), customer);
}

/** The simulator of customer 7 with the projection of its 10 initial users on screen. */
function openWithProjection(): Page {
  const page = open();
  arrive(page);
  flush(page, only(quoteRequests(page)), OF_10);
  return page;
}

function wait(page: Page, milliseconds: number): void {
  vi.advanceTimersByTime(milliseconds);
  page.fixture.detectChanges();
}

function input(page: Page, id: string): HTMLInputElement | null {
  return page.element.querySelector<HTMLInputElement>(`#${id}`);
}

function write(page: Page, id: string, text: string): void {
  const box = input(page, id);
  expect(box).not.toBeNull();
  if (box) {
    box.value = text;
    box.dispatchEvent(new Event('input'));
  }
  page.fixture.detectChanges();
}

/** Writes a number of users and lets the 200 ms without changes go by. */
function settleUsers(page: Page, text: string): void {
  write(page, USERS, text);
  wait(page, 200);
}

function press(page: Page, label: string, within = 'form'): void {
  const buttons = Array.from(page.element.querySelectorAll(`${within} button`));
  const button = buttons.find((candidate) => clean(candidate.textContent) === label);
  expect(button).toBeDefined();
  (button as HTMLButtonElement | undefined)?.click();
  page.fixture.detectChanges();
}

/** Text with every run of white space, the no-break one included, as a single space. */
function clean(text: string | null | undefined): string {
  return (text ?? '').replace(/\s+/g, ' ').trim();
}

function textOf(page: Page, selector: string): string {
  return clean(page.element.querySelector(selector)?.textContent);
}

function errorOf(page: Page, id: string): string {
  return textOf(page, `#${id}-error`);
}

/** The amounts of the projection on screen; empty when there is none. */
function amounts(page: Page): Record<string, string> {
  const found: Record<string, string> = {};
  for (const term of Array.from(page.element.querySelectorAll('.quote dt'))) {
    found[clean(term.textContent)] = clean(term.nextElementSibling?.textContent);
  }
  return found;
}

function saveButton(page: Page): HTMLButtonElement | null {
  const buttons = Array.from(page.element.querySelectorAll<HTMLButtonElement>('form button'));
  return buttons.find((candidate) => clean(candidate.textContent) === 'Guardar') ?? null;
}

function written(page: Page): string[] {
  return [USERS, STORAGE, CALLS].map((id) => input(page, id)?.value ?? '');
}

function heading(page: Page): string {
  return textOf(page, 'h1');
}

function spyOnNavigation(): ReturnType<typeof vi.spyOn> {
  return vi.spyOn(TestBed.inject(Router), 'navigateByUrl').mockResolvedValue(true);
}

/** The simulator ready to save the simulation of `SAVED_BODY`, with «Guardar» pressed. */
function openAndSave(): Page {
  const page = openWithProjection();
  write(page, STORAGE, '500');
  write(page, CALLS, '250000');
  press(page, 'Guardar');
  return page;
}

function invalid(errors: object[]): object {
  return {
    status: 422,
    code: 'validation_error',
    detail: 'La petición contiene datos no válidos.',
    errors,
  };
}

const OUT_OF_RANGE = 'Debe estar entre los límites admitidos.';

beforeEach(() => vi.useFakeTimers());
afterEach(() => vi.useRealTimers());

// CA-08: the rows of SPEC-04, 5.5, but its two rows of currency, which arrive with the currencies.
describe('Simulador · proyección · SPEC-04/E-17 a E-22, E-35, E-38, E-40, E-48, E-49 (CA-08)', () => {
  it('should ask for one projection, with the 10 initial users, and show its total and the country by name', () => {
    const page = open();
    arrive(page);

    const request = only(quoteRequests(page));
    flush(page, request, OF_10);

    expect(request.request.body).toEqual({ customer_id: 7, active_users: 10 });
    expect(amounts(page)['Total']).toBe('121,00 EUR');
    expect(textOf(page, '.simulator-customer')).toBe('Ejemplo Uno SL · España');
  });

  it('should ask for no projection while the customer has not arrived, and for one when it does', () => {
    const page = open();

    wait(page, 500);
    const before = quoteRequests(page).length;
    const status = textOf(page, '[role="status"]');
    arrive(page);

    expect(before).toBe(0);
    expect(status).toBe('Cargando el cliente…');
    expect(only(quoteRequests(page)).request.body).toEqual({ customer_id: 7, active_users: 10 });
  });

  it('should send as customer_id the id of the customer that arrived, as a JSON number', () => {
    const page = open('7');
    arrive(page, { ...CUSTOMER, id: 70 });

    const body: unknown = only(quoteRequests(page)).request.body;

    expect(JSON.stringify(body)).toBe('{"customer_id":70,"active_users":10}');
  });

  it('should show the error of /meta with a retry instead of the simulator when /meta fails', () => {
    const page = open('7', 'failed');
    arrive(page);

    const alert = page.element.querySelector('[role="alert"]');

    expect(clean(alert?.textContent)).toContain(UNEXPECTED);
    expect(clean(alert?.querySelector('button')?.textContent)).toBe('Reintentar');
    expect(page.element.querySelector('form')).toBeNull();
    expect(page.element.querySelector('.simulator-customer')).toBeNull();
  });

  it('should ask once, with 15, when the slider is dragged from 10 to 15 in less than 200 ms', () => {
    const page = openWithProjection();

    for (const users of ['11', '12', '13', '14', '15']) {
      write(page, SLIDER, users);
      wait(page, 30);
    }
    const whileDragging = quoteRequests(page).length;
    wait(page, 200);
    const request = only(quoteRequests(page));
    flush(page, request, OF_15);

    expect(whileDragging).toBe(0);
    expect(request.request.body).toEqual({ customer_id: 7, active_users: 15 });
    expect(amounts(page)['Total']).toBe('169,40 EUR');
    expect(input(page, USERS)?.value).toBe('15');
  });

  it('should keep the slider and the text box in step', () => {
    const page = openWithProjection();

    write(page, USERS, '300');
    const sliderAfterText = input(page, SLIDER)?.value;
    write(page, SLIDER, '42');

    expect(sliderAfterText).toBe('300');
    expect(input(page, USERS)?.value).toBe('42');
    expect(input(page, SLIDER)?.getAttribute('max')).toBe('500');
    expect(input(page, SLIDER)?.getAttribute('min')).toBe('0');
  });

  it('should mark the amounts as «actualizando», with «Guardar» disabled, until the new ones arrive', () => {
    const page = openWithProjection();

    write(page, USERS, '15');
    const waiting = [
      amounts(page)['Total'],
      textOf(page, '.quote-updating'),
      saveButton(page)?.disabled,
    ];
    wait(page, 199);
    const askedBeforeTheWait = quoteRequests(page).length;
    wait(page, 1);
    const request = only(quoteRequests(page));
    const inFlight = [
      amounts(page)['Total'],
      textOf(page, '.quote-updating'),
      saveButton(page)?.disabled,
    ];
    flush(page, request, OF_15);

    expect(waiting).toEqual(['121,00 EUR', 'Actualizando…', true]);
    // The row of the 200 ms of 5.5: «0 todavía», and then one, for the 15 users.
    expect(askedBeforeTheWait).toBe(0);
    expect(request.request.body).toEqual({ customer_id: 7, active_users: 15 });
    expect(inFlight).toEqual(['121,00 EUR', 'Actualizando…', true]);
    expect(amounts(page)['Total']).toBe('169,40 EUR');
    expect(page.element.querySelector('.quote-updating')).toBeNull();
    expect(saveButton(page)?.disabled).toBe(false);
  });

  it('should cancel the projection of 15 and show only the one of 51 when 51 comes first', () => {
    const page = openWithProjection();
    settleUsers(page, '15');
    const of15 = only(quoteRequests(page));

    settleUsers(page, '51');
    const of51 = only(quoteRequests(page));
    flush(page, of51, OF_51);

    expect(of15.cancelled).toBe(true);
    expect(of51.request.body).toEqual({ customer_id: 7, active_users: 51 });
    expect(amounts(page)['Total']).toBe('514,25 EUR');
  });

  it('should project 20000 users and leave the slider at its maximum', () => {
    const page = openWithProjection();

    settleUsers(page, '20000');
    const request = only(quoteRequests(page));
    flush(page, request, OF_20000);

    expect(request.request.body).toEqual({ customer_id: 7, active_users: 20000 });
    expect(input(page, SLIDER)?.value).toBe('500');
    expect(amounts(page)['Total']).toBe('121.205,70 EUR');
  });

  it('should send 15, with no decimals in the body, when «015» is written', () => {
    const page = openWithProjection();

    settleUsers(page, '015');
    const request = only(quoteRequests(page));
    flush(page, request, OF_15);

    expect(JSON.stringify(request.request.body)).toBe('{"customer_id":7,"active_users":15}');
    expect(amounts(page)['Total']).toBe('169,40 EUR');
  });

  it.each(['-1', '1,5', '100001', '', '15.0', '1e3', '+15', '1 5', '100000.000000000001'])(
    'should show the error next to the field, with no call and no amounts, when the users are «%s»',
    (text) => {
      const page = openWithProjection();

      settleUsers(page, text);

      expect(quoteRequests(page).length).toBe(0);
      expect(errorOf(page, USERS)).not.toBe('');
      expect(input(page, USERS)?.getAttribute('aria-invalid')).toBe('true');
      expect(amounts(page)).toEqual({});
      expect(saveButton(page)?.disabled).toBe(true);
    },
  );

  it('should cancel the projection in flight when the users stop being valid', () => {
    const page = openWithProjection();
    settleUsers(page, '15');
    const of15 = only(quoteRequests(page));

    write(page, USERS, '-1');

    expect(of15.cancelled).toBe(true);
  });

  it.each<[string, number, object | string, string]>([
    ['500 internal_error', 500, { code: 'internal_error' }, UNEXPECTED],
    ['503 service_unavailable', 503, { code: 'service_unavailable' }, UNAVAILABLE],
    ['500 tax_rate_not_defined', 500, { code: 'tax_rate_not_defined' }, UNEXPECTED],
    ['400 malformed_request', 400, { code: 'malformed_request' }, UNEXPECTED],
    ['a code it does not know', 418, { code: 'teapot' }, UNEXPECTED],
    ['502 with a body that is not JSON', 502, '<html>Bad Gateway</html>', UNEXPECTED],
  ])(
    'should take the amounts away and show its notice with a retry when the projection fails with %s',
    (_case, status, body, expected) => {
      const page = openWithProjection();
      settleUsers(page, '15');

      flush(page, only(quoteRequests(page)), body, status);

      expect(amounts(page)).toEqual({});
      expect(textOf(page, PROJECTION_NOTICE)).toContain(expected);
      expect(saveButton(page)?.disabled).toBe(true);
      press(page, 'Reintentar', PROJECTION_NOTICE);
      expect(only(quoteRequests(page)).request.body).toEqual({ customer_id: 7, active_users: 15 });
    },
  );

  it('should take the amounts away and show the connection notice when no response arrives', () => {
    const page = openWithProjection();
    settleUsers(page, '15');

    only(quoteRequests(page)).error(new ProgressEvent('error'));
    page.fixture.detectChanges();

    expect(amounts(page)).toEqual({});
    expect(textOf(page, PROJECTION_NOTICE)).toContain(OFFLINE);
    press(page, 'Reintentar', PROJECTION_NOTICE);
    expect(only(quoteRequests(page)).request.body).toEqual({ customer_id: 7, active_users: 15 });
  });

  it('should take the amounts away and show the timeout notice when the projection takes 10 s', () => {
    const page = openWithProjection();
    settleUsers(page, '15');

    wait(page, 10_000);

    expect(amounts(page)).toEqual({});
    expect(textOf(page, PROJECTION_NOTICE)).toContain(TIMED_OUT);
    expect(textOf(page, PROJECTION_NOTICE)).toContain('Reintentar');
  });

  it('should show the amounts again once a retry brings them', () => {
    const page = openWithProjection();
    settleUsers(page, '15');
    flush(page, only(quoteRequests(page)), { code: 'service_unavailable' }, 503);

    press(page, 'Reintentar', PROJECTION_NOTICE);
    flush(page, only(quoteRequests(page)), OF_15);

    expect(amounts(page)['Total']).toBe('169,40 EUR');
    expect(page.element.querySelector(PROJECTION_NOTICE)).toBeNull();
  });

  it('should show the tiers, the base, the tax with its rate and the total of the projection', () => {
    const page = openWithProjection();
    settleUsers(page, '15');
    flush(page, only(quoteRequests(page)), OF_15);

    const tiers = Array.from(page.element.querySelectorAll('.quote .tier')).map((tier) =>
      Array.from(tier.children).map((part) => clean(part.textContent)),
    );

    expect(tiers).toEqual([
      ['del 1 al 10', '10 × 10,00 EUR', '100,00 EUR'],
      ['del 11 al 50', '5 × 8,00 EUR', '40,00 EUR'],
      ['del 51 en adelante', '0 × 5,00 EUR', '0,00 EUR'],
    ]);
    expect(amounts(page)).toEqual({
      'Coste base': '140,00 EUR',
      'Impuesto (21 %)': '29,40 EUR',
      Total: '169,40 EUR',
    });
  });

  it('should show the message of the backend next to the users when a projection answers 422', () => {
    const page = openWithProjection();
    settleUsers(page, '15');

    const request = only(quoteRequests(page));
    flush(
      page,
      request,
      invalid([{ field: 'active_users', code: 'out_of_range', message: OUT_OF_RANGE }]),
      422,
    );

    expect(request.request.body).toEqual({ customer_id: 7, active_users: 15 });
    expect(errorOf(page, USERS)).toBe(OUT_OF_RANGE);
    expect(amounts(page)).toEqual({});
    expect(saveButton(page)?.disabled).toBe(true);
    expect(page.element.querySelector(PROJECTION_NOTICE)).toBeNull();
  });

  it('should list in the notice of the projection the errors of a 422 that have no field here', () => {
    const page = openWithProjection();
    settleUsers(page, '15');

    flush(
      page,
      only(quoteRequests(page)),
      invalid([
        { field: 'customer_id', code: 'out_of_range', message: 'El cliente no es válido.' },
      ]),
      422,
    );

    expect(textOf(page, PROJECTION_NOTICE)).toContain('El cliente no es válido.');
    // Asking the same again would bring the same 422: no «Reintentar» (SPEC-04, 2.5).
    expect(page.element.querySelector(`${PROJECTION_NOTICE} button`)).toBeNull();
    expect(amounts(page)).toEqual({});
  });

  it('should ask for no projection, and keep the one on screen, when storage or calls change', () => {
    const page = openWithProjection();

    write(page, STORAGE, '500');
    write(page, CALLS, '250000');
    wait(page, 1000);

    expect(quoteRequests(page).length).toBe(0);
    expect(amounts(page)['Total']).toBe('121,00 EUR');
    expect(page.element.querySelector('.quote-updating')).toBeNull();
    expect(saveButton(page)?.disabled).toBe(false);
  });

  it.each([
    [STORAGE, '-1'],
    [STORAGE, '1,5'],
    [STORAGE, '2.0'],
    [STORAGE, '1e2'],
    [STORAGE, '1000001'],
    [CALLS, ''],
    [CALLS, '1000000001'],
  ])(
    'should show the error next to the field and disable «Guardar», keeping the projection, when #%s is «%s»',
    (id, text) => {
      const page = openWithProjection();

      write(page, id, text);
      wait(page, 1000);

      expect(quoteRequests(page).length).toBe(0);
      expect(errorOf(page, id)).not.toBe('');
      expect(input(page, id)?.getAttribute('aria-invalid')).toBe('true');
      expect(amounts(page)['Total']).toBe('121,00 EUR');
      expect(saveButton(page)?.disabled).toBe(true);
    },
  );

  it('should start with 10 users, no storage and no calls, in text boxes for numbers', () => {
    const page = openWithProjection();

    expect(written(page)).toEqual(['10', '0', '0']);
    for (const id of [USERS, STORAGE, CALLS]) {
      expect(input(page, id)?.getAttribute('type')).toBe('text');
      expect(input(page, id)?.getAttribute('inputmode')).toBe('numeric');
    }
  });

  it('should keep «Guardar» disabled until the first projection arrives', () => {
    const page = open();
    arrive(page);
    const before = saveButton(page)?.disabled;

    flush(page, only(quoteRequests(page)), OF_10);

    expect(before).toBe(true);
    expect(saveButton(page)?.disabled).toBe(false);
  });
});

describe('Simulador · guardar · SPEC-04/E-23 a E-25, E-37, E-48, E-49, E-55 (CA-08, CA-16)', () => {
  it('should save what the form holds, as JSON integers, and go to the detail on 201', () => {
    const page = openWithProjection();
    const navigate = spyOnNavigation();
    write(page, STORAGE, '0500');
    write(page, CALLS, '250000');

    press(page, 'Guardar');
    const request = only(simulationRequests(page));
    flush(page, request, SAVED, 201);

    expect(request.request.method).toBe('POST');
    expect(JSON.stringify(request.request.body)).toBe(JSON.stringify(SAVED_BODY));
    expect(navigate).toHaveBeenCalledWith('/clientes/7');
  });

  it('should send a single request when «Guardar» is pressed twice before the answer', () => {
    const page = openAndSave();

    const disabledWhileSaving = saveButton(page)?.disabled;
    saveButton(page)?.click();
    page.fixture.detectChanges();

    expect(disabledWhileSaving).toBe(true);
    // `only` checks that there is one request and no more.
    expect(only(simulationRequests(page)).request.body).toEqual(SAVED_BODY);
  });

  it.each<[string, number, object, string]>([
    ['500 internal_error', 500, { code: 'internal_error' }, UNEXPECTED],
    ['503 service_unavailable', 503, { code: 'service_unavailable' }, UNAVAILABLE],
    ['500 tax_rate_not_defined', 500, { code: 'tax_rate_not_defined' }, UNEXPECTED],
    ['a code it does not know', 418, { code: 'teapot' }, UNEXPECTED],
  ])(
    'should show its notice with a retry, keep the values and stay, when saving fails with %s',
    (_case, status, body, expected) => {
      const page = openAndSave();
      const navigate = spyOnNavigation();

      flush(page, only(simulationRequests(page)), body, status);

      expect(textOf(page, SAVE_NOTICE)).toContain(expected);
      expect(written(page)).toEqual(['10', '500', '250000']);
      expect(amounts(page)['Total']).toBe('121,00 EUR');
      expect(navigate).not.toHaveBeenCalled();
      press(page, 'Reintentar', SAVE_NOTICE);
      expect(only(simulationRequests(page)).request.body).toEqual(SAVED_BODY);
    },
  );

  // SPEC-04, 2.7 and 5.5: «Reintentar» in a form sends what the form holds at that moment, not
  // the body of the request that failed.
  it('should save what the form holds now when «Reintentar» is pressed after an edit', () => {
    const page = openAndSave();
    flush(page, only(simulationRequests(page)), { code: 'internal_error' }, 500);

    write(page, STORAGE, '400');
    write(page, CALLS, '300000');
    press(page, 'Reintentar', SAVE_NOTICE);

    expect(only(simulationRequests(page)).request.body).toEqual({
      ...SAVED_BODY,
      storage_gb: 400,
      estimated_api_calls: 300000,
    });
  });

  it('should warn that it may have been saved, with a retry and a link to the detail, on a timeout', () => {
    const page = openAndSave();
    const request = only(simulationRequests(page));

    wait(page, 10_000);

    const notice = page.element.querySelector(SAVE_NOTICE);
    expect(request.request.body).toEqual(SAVED_BODY);
    expect(clean(notice?.textContent)).toContain(TIMED_OUT);
    expect(clean(notice?.textContent)).toContain('puede haberse guardado');
    expect(clean(notice?.querySelector('button')?.textContent)).toBe('Reintentar');
    expect(notice?.querySelector('a')?.getAttribute('href')).toBe('/clientes/7');
    expect(written(page)).toEqual(['10', '500', '250000']);
  });

  it('should show the connection notice with a retry, keep the values and stay, when saving gets no response', () => {
    const page = openAndSave();
    const navigate = spyOnNavigation();

    only(simulationRequests(page)).error(new ProgressEvent('error'));
    page.fixture.detectChanges();

    expect(textOf(page, SAVE_NOTICE)).toContain(OFFLINE);
    expect(written(page)).toEqual(['10', '500', '250000']);
    expect(navigate).not.toHaveBeenCalled();
    press(page, 'Reintentar', SAVE_NOTICE);
    expect(only(simulationRequests(page)).request.body).toEqual(SAVED_BODY);
  });

  it('should offer no link to the detail in the notice of an error that is not a timeout', () => {
    const page = openAndSave();

    flush(page, only(simulationRequests(page)), { code: 'internal_error' }, 500);

    expect(page.element.querySelector(`${SAVE_NOTICE} a`)).toBeNull();
  });

  it('should show each error of a 422 next to its field, or in the notice if it has none here', () => {
    const page = openAndSave();

    const request = only(simulationRequests(page));
    flush(
      page,
      request,
      invalid([
        { field: 'storage_gb', code: 'out_of_range', message: OUT_OF_RANGE },
        { field: 'customer_id', code: 'out_of_range', message: 'El cliente no es válido.' },
      ]),
      422,
    );

    expect(request.request.body).toEqual(SAVED_BODY);
    expect(errorOf(page, STORAGE)).toBe(OUT_OF_RANGE);
    expect(textOf(page, SAVE_NOTICE)).toContain('El cliente no es válido.');
    expect(textOf(page, SAVE_NOTICE)).not.toContain(OUT_OF_RANGE);
    // Saving the same again would bring the same 422: no «Reintentar» (SPEC-04, 2.5).
    expect(page.element.querySelector(`${SAVE_NOTICE} button`)).toBeNull();
    expect(written(page)).toEqual(['10', '500', '250000']);
  });

  it('should drop the message of the backend once its field is edited', () => {
    const page = openAndSave();
    flush(
      page,
      only(simulationRequests(page)),
      invalid([{ field: 'storage_gb', code: 'out_of_range', message: OUT_OF_RANGE }]),
      422,
    );

    write(page, STORAGE, '400');

    expect(errorOf(page, STORAGE)).toBe('');
  });

  it('should show «Cliente no encontrado» when saving answers 404 customer_not_found', () => {
    const page = openAndSave();

    const request = only(simulationRequests(page));
    flush(page, request, { code: 'customer_not_found' }, 404);

    expect(request.request.body).toEqual(SAVED_BODY);
    expect(heading(page)).toBe('Cliente no encontrado');
  });

  it('should show «Cliente no encontrado» when a projection answers 404 customer_not_found', () => {
    const page = openWithProjection();
    settleUsers(page, '15');

    const request = only(quoteRequests(page));
    flush(page, request, { code: 'customer_not_found' }, 404);

    expect(request.request.body).toEqual({ customer_id: 7, active_users: 15 });
    expect(heading(page)).toBe('Cliente no encontrado');
    expect(clean(page.element.querySelector('a')?.textContent)).toBe('Volver al panel');
  });

  it('should not save while the projection on screen is not the one of the users written', () => {
    const page = openWithProjection();

    write(page, USERS, '15');
    saveButton(page)?.click();
    page.fixture.detectChanges();

    expect(simulationRequests(page).length).toBe(0);
  });
});

// CA-17: the rows of SPEC-04, 5.7, in the simulator. Only those of customer 1 reach a projection.
describe('Simulador · el id de la ruta · SPEC-04/E-15, E-47 (CA-17, CA-16)', () => {
  it('should ask for the customer with the text of the route and then for its projection', () => {
    const page = open('1');

    const request = only(customerRequests(page));
    flush(page, request, { ...CUSTOMER, id: 1 });

    expect(request.request.urlWithParams).toBe(`${CUSTOMERS_URL}1`);
    expect(only(quoteRequests(page)).request.body).toEqual({ customer_id: 1, active_users: 10 });
  });

  // The filter sees the segment the router has already decoded, so an encoded digit is that
  // digit and a matrix parameter is not part of the id. These two go through the real router.
  it.each(['/clientes/%31/simulacion', '/clientes/1;x=y/simulacion'])(
    'should ask for /customers/1 and then for its projection when the route is %s',
    async (url) => {
      const { harness, controller } = await openThroughRouter(url);

      const request = only(controller.match((sent) => sent.url.startsWith(CUSTOMERS_URL)));
      request.flush({ ...CUSTOMER, id: 1 });
      harness.detectChanges();

      expect(request.request.urlWithParams).toBe(`${CUSTOMERS_URL}1`);
      expect(only(controller.match(QUOTE_URL)).request.body).toEqual({
        customer_id: 1,
        active_users: 10,
      });
    },
  );

  it.each([
    'abc',
    '01',
    '+1',
    '1.0',
    '1e0',
    '1_0',
    '1 ',
    '0',
    '-1',
    ARABIC_DIGIT_ONE,
    '9007199254740993',
    '99999999999999999',
  ])(
    'should show «Cliente no encontrado» and ask for nothing when the id of the route is «%s»',
    (id) => {
      const page = open(id);

      wait(page, 500);

      expect(customerRequests(page).length).toBe(0);
      expect(quoteRequests(page).length).toBe(0);
      expect(heading(page)).toBe('Cliente no encontrado');
      expect(clean(page.element.querySelector('a')?.textContent)).toBe('Volver al panel');
    },
  );

  it.each(['999', '9007199254740991'])(
    'should ask for /customers/%s, show «Cliente no encontrado» on its 404 and project nothing',
    (id) => {
      const page = open(id);

      const request = only(customerRequests(page));
      flush(page, request, { code: 'customer_not_found' }, 404);
      wait(page, 500);

      expect(request.request.urlWithParams).toBe(`${CUSTOMERS_URL}${id}`);
      expect(quoteRequests(page).length).toBe(0);
      expect(heading(page)).toBe('Cliente no encontrado');
    },
  );

  it.each<[string, number, object, string]>([
    ['422 validation_error', 422, { code: 'validation_error', errors: [] }, UNEXPECTED],
    ['404 not_found', 404, { code: 'not_found' }, UNEXPECTED],
    ['503 service_unavailable', 503, { code: 'service_unavailable' }, UNAVAILABLE],
  ])(
    'should show its notice with a retry, not «Cliente no encontrado», when the customer answers %s',
    (_case, status, body, expected) => {
      const page = open('7');

      flush(page, only(customerRequests(page)), body, status);
      wait(page, 500);

      expect(textOf(page, '[role="alert"]')).toContain(expected);
      expect(heading(page)).not.toBe('Cliente no encontrado');
      expect(quoteRequests(page).length).toBe(0);
      press(page, 'Reintentar', '[role="alert"]');
      expect(only(customerRequests(page)).request.urlWithParams).toBe(`${CUSTOMERS_URL}7`);
    },
  );
});

// The two rows of currency of SPEC-04, 5.5: with them CA-08 is complete.
describe('Simulador · divisa · SPEC-04/E-27, E-29, E-31 (CA-08)', () => {
  function openWith15Users(): Page {
    const page = openWithProjection();
    settleUsers(page, '15');
    flush(page, only(quoteRequests(page)), OF_15);
    return page;
  }

  function show(page: Page, currency: DisplayedCurrency): void {
    TestBed.inject(DisplayCurrency).show(currency);
    page.fixture.detectChanges();
  }

  it('should show the amounts in USD at once, with the rate, its date and the total in EUR, asking for nothing', () => {
    const page = openWith15Users();

    show(page, { code: 'USD', rate: 1.1139, date: '2026-11-12' });

    expect(quoteRequests(page).length).toBe(0);
    expect(amounts(page)).toEqual({
      'Coste base': '155,95 USD',
      'Impuesto (21 %)': '32,75 USD',
      Total: '188,69 USD',
      'Total en EUR': '169,40 EUR',
    });
    expect(textOf(page, '.quote .rate-applied')).toBe('1 EUR = 1,1139 USD · tipo del 12/11/2026');
    expect(textOf(page, '.quote .rate-warning')).toContain('orientativos');
  });

  it('should show the date of the rate as it comes: the first of January stays the first of January', () => {
    const page = openWith15Users();

    show(page, { code: 'USD', rate: 1.1139, date: '2026-01-01' });

    expect(textOf(page, '.quote .rate-applied')).toBe('1 EUR = 1,1139 USD · tipo del 01/01/2026');
  });

  it('should show neither a rate nor a total in EUR while the currency is EUR', () => {
    const page = openWith15Users();

    show(page, { code: 'USD', rate: 1.1139, date: '2026-11-12' });
    show(page, { code: 'EUR' });

    expect(page.element.querySelector('.rate-note')).toBeNull();
    expect(amounts(page)).toEqual({
      'Coste base': '140,00 EUR',
      'Impuesto (21 %)': '29,40 EUR',
      Total: '169,40 EUR',
    });
  });

  it('should save the same body, with no currency and no converted amount, while USD is shown', () => {
    const page = openWith15Users();
    show(page, { code: 'USD', rate: 1.1139, date: '2026-11-12' });

    press(page, 'Guardar');

    expect(JSON.stringify(only(simulationRequests(page)).request.body)).toBe(
      '{"customer_id":7,"active_users":15,"storage_gb":0,"estimated_api_calls":0}',
    );
  });
});

// SPEC-04, 2.5: with `/meta` in error the simulator still loads behind the notice.
describe('Simulador · /meta en error · SPEC-04/E-38, E-40 (2.5)', () => {
  it('should ask for the customer and its first projection all the same, and appear loaded when /meta comes back', () => {
    const page = open('7', 'failed');

    const customer = only(customerRequests(page));
    flush(page, customer, CUSTOMER);
    const projection = only(quoteRequests(page));
    flush(page, projection, OF_10);
    const hiddenForm = page.element.querySelector('form');
    press(page, 'Reintentar', '[role="alert"]');
    flush(page, only(page.controller.match(META_URL)), META);

    expect(customer.request.urlWithParams).toBe(`${CUSTOMERS_URL}7`);
    expect(projection.request.body).toEqual({ customer_id: 7, active_users: 10 });
    expect(hiddenForm).toBeNull();
    expect(textOf(page, '.simulator-customer')).toBe('Ejemplo Uno SL · España');
    expect(amounts(page)['Total']).toBe('121,00 EUR');
    expect(quoteRequests(page).length).toBe(0);
  });
});
