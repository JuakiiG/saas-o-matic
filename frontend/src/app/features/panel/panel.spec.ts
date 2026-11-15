import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { BACKEND_BASE_URL } from '../../core/backend-api';
import { MetaStore } from '../../core/meta-store';
import { Panel } from './panel';

const META_URL = `${BACKEND_BASE_URL}/meta`;
const CUSTOMERS_URL = `${BACKEND_BASE_URL}/customers`;
const SPACE = String.fromCodePoint(0x20);
const GRINNING_FACE = String.fromCodePoint(0x1f600);
const HIGH_SURROGATE = String.fromCharCode(0xd800);
const REPLACEMENT = String.fromCodePoint(0xfffd);

const META = {
  countries: [{ code: 'ES', name: 'España', tax_rate_bp: 2100 }],
  plans: [{ code: 'professional', name: 'Profesional' }],
};
const UNAVAILABLE = 'El servicio no está disponible en este momento.';
const UNEXPECTED = 'Se ha producido un error inesperado.';
const OFFLINE = 'No se ha podido conectar con el servidor.';
const TOO_SLOW = 'El servidor tarda demasiado en responder.';
const LIMIT = 'El texto de búsqueda admite 100 caracteres como máximo';
const NO_MATCHES = 'No hay clientes que coincidan';
const NO_CUSTOMERS_YET = 'Todavía no hay clientes';
const AT_MAXIMUM =
  'Se muestran como máximo 20 clientes. Escribe más texto para afinar la búsqueda.';

interface Page {
  readonly fixture: ComponentFixture<Panel>;
  readonly element: HTMLElement;
  readonly controller: HttpTestingController;
}

function customer(id: number, name: string, country = 'ES', plan = 'professional'): object {
  return { id, company_name: name, tax_id: `B${id}`, country, plan };
}

function customers(count: number): object[] {
  return Array.from({ length: count }, (_, index) => customer(index + 1, `Cliente ${index + 1}`));
}

function problem(status: number, code: string, detail = 'Texto del backend.'): [object, object] {
  return [
    { status, code, detail },
    { status, statusText: 'Error' },
  ];
}

/** Opens the panel with `/meta` already answered, failed or still pending. */
function open(meta: 'answered' | 'failed' | 'pending' = 'answered'): Page {
  TestBed.configureTestingModule({
    providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()],
  });
  const controller = TestBed.inject(HttpTestingController);
  TestBed.inject(MetaStore).load();
  if (meta === 'answered') {
    controller.match(META_URL).forEach((request) => request.flush(META));
  } else if (meta === 'failed') {
    controller
      .match(META_URL)
      .forEach((request) => request.flush(...problem(500, 'internal_error')));
  }
  const fixture = TestBed.createComponent(Panel);
  fixture.detectChanges();
  return { fixture, element: fixture.nativeElement as HTMLElement, controller };
}

/** The requests to `/customers` made since the last time they were asked for. */
function searches(page: Page): TestRequest[] {
  return page.controller.match((request) => request.url === CUSTOMERS_URL);
}

/** Checks that exactly one search is waiting and returns it. */
function onlySearch(page: Page): TestRequest {
  const requests = searches(page);
  expect(requests.length).toBe(1);
  return requests[0];
}

function answer(page: Page, items: object[]): TestRequest['request'] {
  const request = onlySearch(page);
  request.flush({ items });
  page.fixture.detectChanges();
  return request.request;
}

function fail(page: Page, status: number, code: string, detail?: string): void {
  onlySearch(page).flush(...problem(status, code, detail));
  page.fixture.detectChanges();
}

function type(page: Page, text: string): void {
  const input = page.element.querySelector<HTMLInputElement>('#panel-search');
  expect(input).not.toBeNull();
  if (input) {
    input.value = text;
    input.dispatchEvent(new Event('input'));
  }
  page.fixture.detectChanges();
}

function wait(page: Page, milliseconds: number): void {
  vi.advanceTimersByTime(milliseconds);
  page.fixture.detectChanges();
}

function press(page: Page, label: string): void {
  const buttons = Array.from(page.element.querySelectorAll('button'));
  const button = buttons.find((candidate) => candidate.textContent?.trim() === label);
  expect(button).toBeDefined();
  button?.click();
  page.fixture.detectChanges();
}

function names(page: Page): string[] {
  const titles = Array.from(page.element.querySelectorAll('.results a'));
  return titles.map((title) => title.textContent?.trim() ?? '');
}

function text(page: Page): string {
  return page.element.textContent ?? '';
}

// CA-04: every row of the table of SPEC-04, 5.3, with simulated timers.
describe('Panel · SPEC-04/E-01 a E-04, E-35, E-40, E-50, E-51, E-53, E-54 (CA-04)', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it('should ask for the initial list, without q, and show it when the panel opens', () => {
    const page = open();
    expect(text(page)).toContain('Cargando clientes');

    const request = answer(page, [customer(1, 'Ejemplo Uno SL')]);

    expect(request.urlWithParams).toBe(CUSTOMERS_URL);
    expect(names(page)).toEqual(['Ejemplo Uno SL']);
    expect(text(page)).not.toContain('Cargando clientes');
  });

  it('should search once, 300 ms after the last change, when the text is typed quickly', () => {
    const page = open();
    answer(page, []);

    type(page, 'e');
    wait(page, 100);
    type(page, 'ej');
    wait(page, 100);
    type(page, 'eje');
    wait(page, 299);
    expect(searches(page).length).toBe(0);
    wait(page, 1);

    const request = answer(page, [customer(2, 'Ejemplo Dos SL')]);
    expect(request.params.get('q')).toBe('eje');
    expect(request.urlWithParams).toBe(`${CUSTOMERS_URL}?q=eje`);
    expect(names(page)).toEqual(['Ejemplo Dos SL']);
  });

  it('should cancel the search in flight and show only the newest when the text changes', () => {
    const page = open();
    answer(page, []);
    type(page, 'eje');
    wait(page, 300);
    const first = onlySearch(page);

    type(page, 'ejem');
    wait(page, 300);

    expect(first.cancelled).toBe(true);
    const request = answer(page, [customer(3, 'Ejemplo Tres SL')]);
    expect(request.params.get('q')).toBe('ejem');
    expect(request.urlWithParams).toBe(`${CUSTOMERS_URL}?q=ejem`);
    expect(names(page)).toEqual(['Ejemplo Tres SL']);
  });

  it('should say that nothing matches when a search with text brings no customers', () => {
    const page = open();
    answer(page, [customer(1, 'Ejemplo Uno SL')]);
    type(page, 'noexiste');
    wait(page, 300);

    const request = answer(page, []);

    expect(request.params.get('q')).toBe('noexiste');
    expect(request.urlWithParams).toBe(`${CUSTOMERS_URL}?q=noexiste`);
    expect(text(page)).toContain(NO_MATCHES);
    expect(text(page)).not.toContain(NO_CUSTOMERS_YET);
  });

  it('should say there are no customers yet, with a link to the sign-up, when the initial list is empty', () => {
    const page = open();

    const request = answer(page, []);

    expect(request.params.has('q')).toBe(false);
    expect(request.urlWithParams).toBe(CUSTOMERS_URL);
    expect(text(page)).toContain(NO_CUSTOMERS_YET);
    expect(text(page)).not.toContain(NO_MATCHES);
    expect(page.element.querySelector('.empty a')?.getAttribute('href')).toBe('/clientes/nuevo');
  });

  it('should warn that 20 is the maximum when the list brings 20 customers', () => {
    const page = open();

    answer(page, customers(20));

    expect(names(page).length).toBe(20);
    expect(text(page)).toContain(AT_MAXIMUM);
  });

  it('should not warn about the maximum when the list brings 19 customers', () => {
    const page = open();

    answer(page, customers(19));

    expect(names(page).length).toBe(19);
    expect(text(page)).not.toContain('Se muestran como máximo');
  });

  it('should keep the order of the API, which is not the alphabetical one', () => {
    const page = open();

    answer(page, [
      customer(1, 'Zeta Datos SL'),
      customer(2, 'alfa Ejemplo SA'),
      customer(3, 'Ñandú Pruebas SL'),
    ]);

    expect(names(page)).toEqual(['Zeta Datos SL', 'alfa Ejemplo SA', 'Ñandú Pruebas SL']);
  });

  it('should show the names of the country and the plan, the tax id and a link to the detail', () => {
    const page = open();

    answer(page, [customer(7, 'Ejemplo Uno SL', 'ES', 'professional')]);

    const card = page.element.querySelector('.results li');
    expect(card?.textContent).toContain('España');
    expect(card?.textContent).toContain('Profesional');
    expect(card?.textContent).toContain('B7');
    expect(card?.querySelector('a')?.getAttribute('href')).toBe('/clientes/7');
  });

  it('should show a code as it arrives, unmarked, when /meta does not bring it', () => {
    const page = open();

    answer(page, [customer(8, 'Ejemplo Ocho SL', 'XX', 'legacy')]);

    const card = page.element.querySelector('.results li');
    expect(card?.textContent).toContain('XX');
    expect(card?.textContent).toContain('legacy');
  });

  it('should show the loading state instead of the search box while /meta is loading', () => {
    const page = open('pending');

    expect(page.element.querySelector('[role="status"]')).not.toBeNull();
    expect(page.element.querySelector('#panel-search')).toBeNull();
  });

  it('should show the error with a retry, and no search box, list or code, when /meta fails', () => {
    const page = open('failed');
    answer(page, [customer(7, 'Ejemplo Uno SL', 'ES', 'professional')]);

    expect(page.element.querySelector('[role="alert"]')?.textContent).toContain(UNEXPECTED);
    expect(page.element.querySelector('#panel-search')).toBeNull();
    expect(page.element.querySelector('.results')).toBeNull();
    expect(text(page)).not.toContain('ES');
    expect(text(page)).not.toContain('professional');
    const retry = page.element.querySelector('[role="alert"] button');
    expect(retry?.textContent?.trim()).toBe('Reintentar');
  });

  it('should turn the spell checker of the browser off in the search box (SPEC-04 2.8)', () => {
    const page = open();

    const input = page.element.querySelector('#panel-search');
    expect(input?.getAttribute('spellcheck')).toBe('false');
  });

  it('should ask for the list without waiting for /meta and show it when /meta arrives', () => {
    const page = open('pending');
    answer(page, [customer(7, 'Ejemplo Uno SL', 'ES', 'professional')]);
    expect(page.element.querySelector('.results')).toBeNull();

    page.controller.match(META_URL).forEach((request) => request.flush(META));
    page.fixture.detectChanges();

    expect(names(page)).toEqual(['Ejemplo Uno SL']);
    expect(text(page)).toContain('España');
    expect(searches(page).length).toBe(0);
  });

  it('should ask for /meta once more and show the list with names when the retry succeeds', () => {
    const page = open('failed');
    answer(page, [customer(7, 'Ejemplo Uno SL', 'ES', 'professional')]);

    press(page, 'Reintentar');
    const retries = page.controller.match(META_URL);
    retries.forEach((request) => request.flush(META));
    page.fixture.detectChanges();

    expect(retries.length).toBe(1);
    expect(names(page)).toEqual(['Ejemplo Uno SL']);
    expect(text(page)).toContain('España');
  });

  // SPEC-04, 2.2 and 5.3: `/meta` and the list are two requests, and each notice retries its
  // own. The two fail with different errors here, to tell one notice from the other.
  it('should show the notice of the list, with its own retry, when the list failed too and the retry of /meta succeeds', () => {
    const page = open('failed');
    fail(page, 503, 'service_unavailable');
    expect(page.element.querySelector('[role="alert"]')?.textContent).toContain(UNEXPECTED);

    press(page, 'Reintentar');
    const retries = page.controller.match(META_URL);
    retries.forEach((request) => request.flush(META));
    page.fixture.detectChanges();

    expect(retries.length).toBe(1);
    expect(searches(page).length).toBe(0);
    expect(page.element.querySelector('#panel-search')).not.toBeNull();
    expect(page.element.querySelector('.results')).toBeNull();
    const notices = page.element.querySelectorAll('[role="alert"]');
    expect(notices.length).toBe(1);
    expect(notices[0].textContent).toContain(UNAVAILABLE);
    expect(notices[0].querySelector('button')?.textContent?.trim()).toBe('Reintentar');

    press(page, 'Reintentar');

    expect(page.controller.match(META_URL).length).toBe(0);
    const request = answer(page, [customer(7, 'Ejemplo Uno SL', 'ES', 'professional')]);
    expect(request.params.has('q')).toBe(false);
    expect(names(page)).toEqual(['Ejemplo Uno SL']);
    expect(text(page)).toContain('España');
    expect(page.element.querySelector('[role="alert"]')).toBeNull();
  });

  it('should not ask for /meta again when the panel is opened a second time', () => {
    const page = open();
    answer(page, []);
    page.fixture.destroy();

    const again = TestBed.createComponent(Panel);
    again.detectChanges();

    expect(page.controller.match(META_URL).length).toBe(0);
    expect(searches(page).length).toBe(1);
  });

  it('should repeat the same search when it failed and the retry is pressed', () => {
    const page = open();
    answer(page, []);
    type(page, 'eje');
    wait(page, 300);
    fail(page, 500, 'internal_error');
    expect(page.element.querySelector('[role="alert"]')?.textContent).toContain(UNEXPECTED);

    press(page, 'Reintentar');

    expect(answer(page, [customer(2, 'Ejemplo Dos SL')]).params.get('q')).toBe('eje');
    expect(names(page)).toEqual(['Ejemplo Dos SL']);
  });

  it('should ask for the initial list again when the text is deleted after a search', () => {
    const page = open();
    answer(page, []);
    type(page, 'eje');
    wait(page, 300);
    answer(page, [customer(2, 'Ejemplo Dos SL')]);

    type(page, '');
    wait(page, 300);

    expect(answer(page, [customer(1, 'Ejemplo Uno SL')]).urlWithParams).toBe(CUSTOMERS_URL);
    expect(names(page)).toEqual(['Ejemplo Uno SL']);
  });

  it.each([
    ['three spaces, untrimmed', SPACE.repeat(3), `${CUSTOMERS_URL}?q=%20%20%20`],
    ['reserved characters', '100% a+b&c#d', `${CUSTOMERS_URL}?q=100%25%20a%2Bb%26c%23d`],
  ])('should send the text as it is written when it has %s', (_case, written, url) => {
    const page = open();
    answer(page, []);

    type(page, written);
    wait(page, 300);

    const request = answer(page, []);
    expect(request.params.getAll('q')).toEqual([written]);
    expect(request.urlWithParams).toBe(url);
  });

  it('should search when the text has 100 code points, even in 200 UTF-16 units', () => {
    const page = open();
    answer(page, []);

    type(page, GRINNING_FACE.repeat(100));
    wait(page, 300);

    const request = answer(page, []);
    expect(request.params.get('q')).toBe(GRINNING_FACE.repeat(100));
    expect(request.urlWithParams).toBe(`${CUSTOMERS_URL}?q=${'%F0%9F%98%80'.repeat(100)}`);
    expect(text(page)).not.toContain(LIMIT);
  });

  it.each([
    ['101 characters', 'x'.repeat(101)],
    ['100 characters and a space, measured untrimmed', 'x'.repeat(100) + SPACE],
  ])('should warn next to the field and not search when the text has %s', (_case, written) => {
    const page = open();
    answer(page, [customer(1, 'Ejemplo Uno SL')]);

    type(page, written);
    wait(page, 300);

    expect(searches(page).length).toBe(0);
    expect(page.element.querySelector('.search [role="alert"]')?.textContent).toContain(LIMIT);
    expect(page.element.querySelector('.results')).toBeNull();
  });

  it('should search and drop the warning when the text goes back to 100 characters', () => {
    const page = open();
    answer(page, []);
    type(page, 'x'.repeat(101));

    type(page, 'x'.repeat(100));
    wait(page, 300);

    const request = answer(page, []);
    expect(request.params.get('q')).toBe('x'.repeat(100));
    expect(request.urlWithParams).toBe(`${CUSTOMERS_URL}?q=${'x'.repeat(100)}`);
    expect(text(page)).not.toContain(LIMIT);
  });

  it('should send U+FFFD in place of a lone surrogate', () => {
    const page = open();
    answer(page, []);

    type(page, 'a' + HIGH_SURROGATE + 'b');
    wait(page, 300);

    const request = answer(page, []);
    expect(request.params.get('q')).toBe('a' + REPLACEMENT + 'b');
    expect(request.urlWithParams).toBe(`${CUSTOMERS_URL}?q=a%EF%BF%BDb`);
  });

  it('should cancel the search in flight and warn at once when a text over the limit is pasted', () => {
    const page = open();
    answer(page, [customer(1, 'Ejemplo Uno SL')]);
    type(page, 'eje');
    wait(page, 300);
    const inFlight = onlySearch(page);

    type(page, 'x'.repeat(101));

    expect(inFlight.cancelled).toBe(true);
    expect(text(page)).toContain(LIMIT);
    expect(page.element.querySelector('.results')).toBeNull();
    wait(page, 300);
    expect(searches(page).length).toBe(0);
  });
});

// CA-16: the rows of SPEC-04, 5.6, that the panel can receive.
describe('Panel · SPEC-04/E-11, E-32, E-33, E-42, E-43 (CA-16)', () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  function alert(page: Page): string {
    return page.element.querySelector('.results-region [role="alert"]')?.textContent ?? '';
  }

  it('should show the unavailable notice instead of the list, and repeat the search on retry', () => {
    const page = open();

    fail(page, 503, 'service_unavailable');

    expect(alert(page)).toContain(UNAVAILABLE);
    expect(page.element.querySelector('.results')).toBeNull();
    press(page, 'Reintentar');
    expect(answer(page, [customer(1, 'Ejemplo Uno SL')]).urlWithParams).toBe(CUSTOMERS_URL);
    expect(names(page)).toEqual(['Ejemplo Uno SL']);
  });

  it.each([
    [500, 'internal_error'],
    [422, 'validation_error'],
    [400, 'malformed_request'],
    [404, 'not_found'],
    [418, 'teapot'],
  ])(
    'should show the unexpected error notice, with a retry, when it answers %d %s',
    (status, code) => {
      const page = open();

      fail(page, status, code);

      expect(alert(page)).toContain(UNEXPECTED);
      expect(alert(page)).toContain('Reintentar');
      expect(alert(page)).not.toContain(UNAVAILABLE);
    },
  );

  it('should show the connection notice when no response arrives', () => {
    const page = open();

    onlySearch(page).error(new ProgressEvent('error'));
    page.fixture.detectChanges();

    expect(alert(page)).toContain(OFFLINE);
    press(page, 'Reintentar');
    expect(onlySearch(page).request.urlWithParams).toBe(CUSTOMERS_URL);
  });

  it('should show the timeout notice when 10 s pass without a response', () => {
    const page = open();
    const abandoned = onlySearch(page);

    wait(page, 10_000);

    expect(alert(page)).toContain(TOO_SLOW);
    expect(abandoned.cancelled).toBe(true);
    press(page, 'Reintentar');
    expect(onlySearch(page).request.urlWithParams).toBe(CUSTOMERS_URL);
  });

  it('should not change when only the text of the error changes: the code decides', () => {
    const page = open();
    fail(page, 503, 'service_unavailable', 'Un texto.');
    const before = alert(page);

    press(page, 'Reintentar');
    fail(page, 503, 'service_unavailable', 'Otro texto completamente distinto.');

    expect(alert(page)).toBe(before);
  });
});
