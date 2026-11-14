import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayCurrency } from '../core/display-currency';
import { ExchangeRates } from '../core/exchange-rates';
import { CurrencySelector } from './currency-selector';

// The real response of SPEC-04, 4.2.
const CHF = { date: '2026-11-12', base: 'EUR', quote: 'CHF', rate: 0.92316 };
const GBP = { date: '2026-11-12', base: 'EUR', quote: 'GBP', rate: 0.83583 };
const USD = { date: '2026-11-12', base: 'EUR', quote: 'USD', rate: 1.1139 };
const RESPONSE = [CHF, GBP, USD];
const FAILED = 'No se han podido cargar los tipos de cambio. Los importes se muestran en EUR.';

interface Page {
  readonly fixture: ComponentFixture<CurrencySelector>;
  readonly element: HTMLElement;
  readonly controller: HttpTestingController;
}

/** The selector as the header shows it, with the request for the rates in flight. */
function open(): Page {
  TestBed.configureTestingModule({
    providers: [provideHttpClient(), provideHttpClientTesting()],
  });
  const controller = TestBed.inject(HttpTestingController);
  // What the application does when it starts.
  TestBed.inject(ExchangeRates).load();
  const fixture = TestBed.createComponent(CurrencySelector);
  fixture.detectChanges();
  return { fixture, element: fixture.nativeElement as HTMLElement, controller };
}

function requests(page: Page): TestRequest[] {
  return page.controller.match(() => true);
}

function only(found: TestRequest[]): TestRequest {
  expect(found.length).toBe(1);
  return found[0];
}

function answer(page: Page, body: object, status = 200): void {
  only(requests(page)).flush(body, { status, statusText: status < 400 ? 'OK' : 'Error' });
  page.fixture.detectChanges();
}

function openWithRates(): Page {
  const page = open();
  answer(page, RESPONSE);
  return page;
}

function select(page: Page): HTMLSelectElement | null {
  return page.element.querySelector('select');
}

function offered(page: Page): string[] {
  return Array.from(select(page)?.options ?? []).map((option) => option.value);
}

function choose(page: Page, code: string): void {
  const box = select(page);
  expect(box).not.toBeNull();
  if (box) {
    box.value = code;
    box.dispatchEvent(new Event('change'));
  }
  page.fixture.detectChanges();
}

function textOf(page: Page, selector: string): string {
  return (page.element.querySelector(selector)?.textContent ?? '').replace(/\s+/g, ' ').trim();
}

function shown(): object {
  return TestBed.inject(DisplayCurrency).current();
}

// The rows of SPEC-04, 5.2, as the selector shows them. Each row of the response is in the
// tests of the service.
describe('CurrencySelector · SPEC-04/E-26, E-27, E-30 (CA-02)', () => {
  afterEach(() => vi.useRealTimers());

  it('should offer only EUR and say that the rates are loading while the request is in flight', () => {
    const page = open();

    expect(offered(page)).toEqual(['EUR']);
    expect(textOf(page, '[role="status"]')).toBe('Cargando tipos…');
    expect(page.element.querySelector('[role="alert"]')).toBeNull();
  });

  it('should offer the four currencies, with EUR chosen, when the rates arrive', () => {
    const page = openWithRates();

    expect(offered(page)).toEqual(['EUR', 'USD', 'GBP', 'CHF']);
    expect(select(page)?.value).toBe('EUR');
    expect(page.element.querySelector('[role="status"]')).toBeNull();
    expect(page.element.querySelector('[role="alert"]')).toBeNull();
    expect(shown()).toEqual({ code: 'EUR' });
  });

  it.each<[string, object, number]>([
    ['the API answers 500', { message: 'error' }, 500],
    ['the list lacks the object of GBP', [CHF, USD], 200],
    ['the list is empty', [], 200],
  ])('should offer only EUR and show a notice with a retry when %s', (_case, body, status) => {
    const page = open();

    answer(page, body, status);

    expect(offered(page)).toEqual(['EUR']);
    expect(textOf(page, '[role="alert"] p')).toBe(FAILED);
    expect(textOf(page, '[role="alert"] button')).toBe('Reintentar');
    expect(page.element.querySelector('[role="status"]')).toBeNull();
    expect(shown()).toEqual({ code: 'EUR' });
  });

  it('should offer only EUR and show the notice when the network fails', () => {
    const page = open();

    only(requests(page)).error(new ProgressEvent('error'));
    page.fixture.detectChanges();

    expect(offered(page)).toEqual(['EUR']);
    expect(textOf(page, '[role="alert"] p')).toBe(FAILED);
  });

  it('should offer only EUR and show the notice when no response arrives in 5 s', () => {
    vi.useFakeTimers();
    const page = open();

    vi.advanceTimersByTime(5_000);
    page.fixture.detectChanges();

    expect(offered(page)).toEqual(['EUR']);
    expect(textOf(page, '[role="alert"] p')).toBe(FAILED);
  });

  it('should ask once more on «Reintentar» and, with the rates, drop the notice', () => {
    const page = open();
    answer(page, []);

    page.element.querySelector<HTMLButtonElement>('[role="alert"] button')?.click();
    page.fixture.detectChanges();
    const whileRetrying = [offered(page), textOf(page, '[role="status"]')];
    answer(page, RESPONSE);

    expect(whileRetrying).toEqual([['EUR'], 'Cargando tipos…']);
    expect(offered(page)).toEqual(['EUR', 'USD', 'GBP', 'CHF']);
    expect(page.element.querySelector('[role="alert"]')).toBeNull();
  });

  it.each([
    ['USD', { code: 'USD', rate: 1.1139, date: '2026-11-12' }],
    ['GBP', { code: 'GBP', rate: 0.83583, date: '2026-11-12' }],
    ['CHF', { code: 'CHF', rate: 0.92316, date: '2026-11-12' }],
  ])(
    'should show the amounts in %s, with its rate and its date, when it is chosen',
    (code, expected) => {
      const page = openWithRates();

      choose(page, code);

      expect(shown()).toEqual(expected);
    },
  );

  it('should go back to exact euros when EUR is chosen again', () => {
    const page = openWithRates();
    choose(page, 'USD');

    choose(page, 'EUR');

    expect(shown()).toEqual({ code: 'EUR' });
  });

  it('should ask for nothing when the currency changes ten times', () => {
    const page = openWithRates();

    for (const code of ['USD', 'GBP', 'CHF', 'EUR', 'USD', 'EUR', 'CHF', 'GBP', 'USD', 'EUR']) {
      choose(page, code);
    }

    expect(requests(page).length).toBe(0);
    expect(shown()).toEqual({ code: 'EUR' });
  });

  it('should label the selector', () => {
    const page = open();

    const box = select(page);

    expect(box?.id).toBe('currency-select');
    expect(textOf(page, 'label[for="currency-select"]')).toBe('Divisa');
  });
});
