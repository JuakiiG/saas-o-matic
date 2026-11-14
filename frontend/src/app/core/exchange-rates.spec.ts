import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { ExchangeRates, parseRates } from './exchange-rates';

const RATES_URL = 'https://api.frankfurter.dev/v2/rates?base=EUR&quotes=USD,GBP,CHF';
// The real response of SPEC-04, 4.2.
const CHF = { date: '2026-11-12', base: 'EUR', quote: 'CHF', rate: 0.92316 };
const GBP = { date: '2026-11-12', base: 'EUR', quote: 'GBP', rate: 0.83583 };
const USD = { date: '2026-11-12', base: 'EUR', quote: 'USD', rate: 1.1139 };
const RESPONSE = [CHF, GBP, USD];
const RATES = {
  USD: { rate: 1.1139, date: '2026-11-12' },
  GBP: { rate: 0.83583, date: '2026-11-12' },
  CHF: { rate: 0.92316, date: '2026-11-12' },
};

interface Started {
  readonly rates: ExchangeRates;
  readonly controller: HttpTestingController;
}

function start(): Started {
  TestBed.configureTestingModule({
    providers: [provideHttpClient(), provideHttpClientTesting()],
  });
  const started = {
    rates: TestBed.inject(ExchangeRates),
    controller: TestBed.inject(HttpTestingController),
  };
  started.rates.load();
  return started;
}

/** The requests made, to anywhere, since the last time they were asked for. */
function requests(started: Started): TestRequest[] {
  return started.controller.match(() => true);
}

function only(found: TestRequest[]): TestRequest {
  expect(found.length).toBe(1);
  return found[0];
}

// CA-02: every row of the table of SPEC-04, 5.2, at the service.
describe('ExchangeRates · SPEC-04/E-26, E-30 (CA-02, CA-10)', () => {
  afterEach(() => vi.useRealTimers());

  it('should ask the public API once, straight from the browser, for the three rates', () => {
    const started = start();
    started.rates.load();

    const request = only(requests(started)).request;

    expect(request.method).toBe('GET');
    expect(request.urlWithParams).toBe(RATES_URL);
    expect(request.headers.keys()).toEqual([]);
    expect(request.withCredentials).toBe(false);
  });

  it('should be loading while the request is in flight', () => {
    const started = start();

    expect(only(requests(started)).cancelled).toBe(false);
    expect(started.rates.state()).toEqual({ status: 'loading' });
  });

  it('should hold the rate and the date of each currency when the response of 4.2 arrives', () => {
    const started = start();

    only(requests(started)).flush(RESPONSE);

    expect(started.rates.state()).toEqual({ status: 'data', data: RATES });
  });

  it('should ignore the object of a currency that was not asked for', () => {
    const started = start();

    only(requests(started)).flush([
      ...RESPONSE,
      { date: '2026-11-12', base: 'EUR', quote: 'JPY', rate: 171.2 },
    ]);

    expect(started.rates.state()).toEqual({ status: 'data', data: RATES });
  });

  it('should be a network error when no response arrives', () => {
    const started = start();

    only(requests(started)).error(new ProgressEvent('error'));

    expect(started.rates.state()).toEqual({
      status: 'error',
      error: { code: 'network_error', fieldErrors: [] },
    });
  });

  it('should wait 5 s for the response, and no longer', () => {
    vi.useFakeTimers();
    const started = start();
    const request = only(requests(started));

    vi.advanceTimersByTime(4_999);
    const before = started.rates.state().status;
    vi.advanceTimersByTime(1);

    expect(before).toBe('loading');
    expect(started.rates.state()).toEqual({
      status: 'error',
      error: { code: 'timeout', fieldErrors: [] },
    });
    expect(request.cancelled).toBe(true);
  });

  it.each([404, 422, 500])('should be an error when the API answers %i', (status) => {
    const started = start();

    only(requests(started)).flush(
      { status, message: 'invalid currency: XXX' },
      { status, statusText: 'Error' },
    );

    expect(started.rates.state().status).toBe('error');
  });

  it.each<[string, unknown]>([
    ['a list without the object of GBP', [CHF, USD]],
    ['a list with two objects of USD', [CHF, GBP, USD, USD]],
    ['an empty list', []],
    ['a rate of 0', [CHF, GBP, { ...USD, rate: 0 }]],
    ['a negative rate', [CHF, GBP, { ...USD, rate: -1.1 }]],
    ['a rate that is null', [CHF, GBP, { ...USD, rate: null }]],
    ['a rate that is a text', [CHF, GBP, { ...USD, rate: '1.1' }]],
    ['a base that is not EUR', [CHF, { ...GBP, base: 'USD' }, USD]],
    ['no date in one currency', [{ base: 'EUR', quote: 'CHF', rate: 0.92316 }, GBP, USD]],
    ['a date without the shape of a date', [{ ...CHF, date: '12/11/2026' }, GBP, USD]],
    ['an object, as the one of the v1, instead of a list', { base: 'EUR', rates: { USD: 1.1 } }],
    ['a body that is not JSON', '<html>Bad Gateway</html>'],
    ['null', null],
  ])('should be an error, with no rate at all, when the response is %s', (_case, body) => {
    const started = start();

    only(requests(started)).flush(body as object | null);

    expect(started.rates.state()).toEqual({
      status: 'error',
      error: { code: 'invalid_rates', fieldErrors: [] },
    });
  });

  it('should ask again, once, when it is told to retry after an error, and hold the rates', () => {
    const started = start();
    only(requests(started)).flush([]);

    started.rates.retry();
    const whileRetrying = started.rates.state().status;
    only(requests(started)).flush(RESPONSE);

    expect(whileRetrying).toBe('loading');
    expect(started.rates.state()).toEqual({ status: 'data', data: RATES });
  });

  it('should not ask again when it is told to retry without an error', () => {
    const started = start();
    only(requests(started)).flush(RESPONSE);

    started.rates.retry();
    started.rates.load();

    expect(requests(started).length).toBe(0);
  });
});

describe('parseRates · SPEC-04 2.6', () => {
  it('should read the list of 4.2 whatever the order of its objects', () => {
    expect(parseRates([USD, CHF, GBP])).toEqual(RATES);
  });

  it.each<[string, unknown]>([
    ['an entry that is not an object', [CHF, GBP, USD, 'USD']],
    ['an entry that is null', [null, CHF, GBP, USD]],
  ])('should ignore %s, which is no currency that was asked for', (_case, body) => {
    expect(parseRates(body)).toEqual(RATES);
  });

  it.each<[string, unknown]>([
    ['a rate that is not finite', [CHF, GBP, { ...USD, rate: Number.POSITIVE_INFINITY }]],
    ['a date with a time', [CHF, GBP, { ...USD, date: '2026-11-12T00:00:00Z' }]],
    ['a date that is a number', [CHF, GBP, { ...USD, date: 20261112 }]],
    ['no base', [CHF, GBP, { date: '2026-11-12', quote: 'USD', rate: 1.1139 }]],
  ])('should reject the whole response when it has %s', (_case, body) => {
    expect(parseRates(body)).toBeNull();
  });
});
