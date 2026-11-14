import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, ParamMap, convertToParamMap } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

import { BACKEND_BASE_URL } from './backend-api';
import { CustomerLoader } from './customer-loader';

// The example of SPEC-03, 4.2, for a customer without simulations.
const CUSTOMER = {
  id: 1,
  company_name: 'Ejemplo Uno SL',
  tax_id: 'B12345674',
  contact_email: 'compras@ejemplo-uno.example',
  country: 'ES',
  plan: 'professional',
  created_at: '2026-11-12T14:30:00Z',
  simulation_count: 0,
  simulations: [],
};

interface Started {
  readonly loader: CustomerLoader;
  readonly controller: HttpTestingController;
  readonly params: BehaviorSubject<ParamMap>;
}

function start(id: string): Started {
  const params = new BehaviorSubject<ParamMap>(convertToParamMap({ id }));
  TestBed.configureTestingModule({
    providers: [
      provideHttpClient(),
      provideHttpClientTesting(),
      CustomerLoader,
      { provide: ActivatedRoute, useValue: { paramMap: params } },
    ],
  });
  return {
    loader: TestBed.inject(CustomerLoader),
    controller: TestBed.inject(HttpTestingController),
    params,
  };
}

function customerUrl(id: string): string {
  return `${BACKEND_BASE_URL}/customers/${id}`;
}

function fail(started: Started, id: string, status: number, code: string): void {
  const requests = started.controller.match(customerUrl(id));
  expect(requests.length).toBe(1);
  requests[0].flush({ status, code, detail: 'Un texto.' }, { status, statusText: 'Error' });
}

describe('CustomerLoader · SPEC-04/E-15, E-47, E-32, E-33 (CA-10)', () => {
  afterEach(() => vi.useRealTimers());

  it('should ask for the customer of the route and be loading while it does not arrive', () => {
    const started = start('1');

    expect(started.controller.match(customerUrl('1')).length).toBe(1);
    expect(started.loader.state()).toEqual({ status: 'loading' });
  });

  it('should hold the customer when it arrives', () => {
    const started = start('1');

    const requests = started.controller.match(customerUrl('1'));
    expect(requests.length).toBe(1);
    requests[0].flush(CUSTOMER);

    expect(started.loader.state()).toEqual({ status: 'data', data: CUSTOMER });
  });

  it('should ask with the exact text of the id, never turned into a number', () => {
    const started = start('9007199254740991');

    const requests = started.controller.match(() => true);

    expect(requests.map((request) => request.request.urlWithParams)).toEqual([
      customerUrl('9007199254740991'),
    ]);
    expect(requests.map((request) => request.request.method)).toEqual(['GET']);
  });

  it.each(['abc', '01', '0', '-1', '+1', '1.0', '1e0', '9007199254740993', ''])(
    'should be «not found» without asking when the id of the route is «%s»',
    (id) => {
      const started = start(id);

      expect(started.loader.state()).toEqual({ status: 'not-found' });
      expect(started.controller.match(() => true).length).toBe(0);
    },
  );

  it('should be «not found» when the backend answers 404 customer_not_found', () => {
    const started = start('999');

    fail(started, '999', 404, 'customer_not_found');

    expect(started.loader.state()).toEqual({ status: 'not-found' });
  });

  it.each([
    [404, 'not_found'],
    [422, 'validation_error'],
    [503, 'service_unavailable'],
    [500, 'internal_error'],
  ])('should be an error, and not «not found», when the backend answers %i %s', (status, code) => {
    const started = start('7');

    fail(started, '7', status, code);

    expect(started.loader.state()).toEqual({ status: 'error', error: { code, fieldErrors: [] } });
  });

  it('should be an error when the customer does not arrive in 10 s', () => {
    vi.useFakeTimers();
    const started = start('7');

    vi.advanceTimersByTime(10_000);

    expect(started.loader.state()).toEqual({
      status: 'error',
      error: { code: 'timeout', fieldErrors: [] },
    });
  });

  it('should ask for the same customer again when it is told to retry', () => {
    const started = start('7');
    fail(started, '7', 503, 'service_unavailable');

    started.loader.retry();

    expect(started.controller.match(customerUrl('7')).length).toBe(1);
    expect(started.loader.state()).toEqual({ status: 'loading' });
  });

  it('should drop the request in flight and ask for the new customer when the route changes', () => {
    const started = start('7');
    const first = started.controller.match(customerUrl('7'));

    started.params.next(convertToParamMap({ id: '8' }));

    expect(first.map((request) => request.cancelled)).toEqual([true]);
    expect(started.controller.match(customerUrl('8')).length).toBe(1);
  });
});
