import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { BackendApi } from './backend-api';
import { RouteCustomerId, isRouteCustomerId } from './customer-id';
import { NewCustomer } from './models';
import { Remote } from './remote';

const BASE = environment.apiBaseUrl;
const SPACE = String.fromCodePoint(0x20);
const NO_BREAK_SPACE = String.fromCodePoint(0xa0);
const GRINNING_FACE = String.fromCodePoint(0x1f600);
const HIGH_SURROGATE = String.fromCharCode(0xd800);
const REPLACEMENT = String.fromCodePoint(0xfffd);
const LOADING = { status: 'loading' };

// Examples of the contracts: SPEC-01 (4.1 and 4.3), SPEC-02 (4) and SPEC-03 (4.1 and 4.2).
const NEW_CUSTOMER: NewCustomer = {
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
};
const QUOTE = {
  currency: 'EUR',
  active_users: 15,
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
};
const NEW_SIMULATION = {
  customer_id: 7,
  active_users: 15,
  storage_gb: 500,
  estimated_api_calls: 250000,
};
const SIMULATION = { ...QUOTE, ...NEW_SIMULATION, id: 1, created_at: '2026-11-12T15:00:00Z' };

function routeId(text: string): RouteCustomerId {
  if (!isRouteCustomerId(text)) {
    throw new Error(`test setup: ${text} is not a route customer id`);
  }
  return text;
}

interface Call {
  readonly name: string;
  readonly start: (api: BackendApi) => Observable<Remote<unknown>>;
  readonly method: string;
  readonly url: string;
  readonly body: unknown;
  readonly response: object;
}

// The six calls to the backend of SPEC-04, 4.1.
const CALLS: Call[] = [
  {
    name: 'getMeta',
    start: (api) => api.getMeta(),
    method: 'GET',
    url: `${BASE}/meta`,
    body: null,
    response: {
      countries: [{ code: 'ES', name: 'España', tax_rate_bp: 2100 }],
      plans: [{ code: 'starter', name: 'Básico' }],
    },
  },
  {
    name: 'searchCustomers',
    start: (api) => api.searchCustomers('eje'),
    method: 'GET',
    url: `${BASE}/customers?q=eje`,
    body: null,
    response: { items: [{ id: 7, company_name: 'Ejemplo Uno SL', tax_id: 'B12345674' }] },
  },
  {
    name: 'createCustomer',
    start: (api) => api.createCustomer(NEW_CUSTOMER),
    method: 'POST',
    url: `${BASE}/customers`,
    body: NEW_CUSTOMER,
    response: CUSTOMER,
  },
  {
    name: 'getCustomer',
    start: (api) => api.getCustomer(routeId('7')),
    method: 'GET',
    url: `${BASE}/customers/7`,
    body: null,
    response: { ...CUSTOMER, simulation_count: 1, simulations: [SIMULATION] },
  },
  {
    name: 'quote',
    start: (api) => api.quote({ customer_id: 7, active_users: 15 }),
    method: 'POST',
    url: `${BASE}/pricing/quote`,
    body: { customer_id: 7, active_users: 15 },
    response: QUOTE,
  },
  {
    name: 'saveSimulation',
    start: (api) => api.saveSimulation(NEW_SIMULATION),
    method: 'POST',
    url: `${BASE}/simulations`,
    body: NEW_SIMULATION,
    response: SIMULATION,
  },
];

function setUp(): { api: BackendApi; controller: HttpTestingController } {
  TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
  return { api: TestBed.inject(BackendApi), controller: TestBed.inject(HttpTestingController) };
}

function record<T>(source: Observable<Remote<T>>): Remote<T>[] {
  const states: Remote<T>[] = [];
  source.subscribe((state) => states.push(state));
  return states;
}

function onlyRequest(controller: HttpTestingController): TestRequest {
  const requests = controller.match(() => true);
  expect(requests.length).toBe(1);
  return requests[0];
}

describe.each(CALLS)('BackendApi.$name · SPEC-04/E-32, E-33, E-52', (call) => {
  afterEach(() => vi.useRealTimers());

  it('should be loading until the response arrives and then hold its data', () => {
    const { api, controller } = setUp();
    const states = record(call.start(api));
    const request = onlyRequest(controller);

    expect(states).toEqual([LOADING]);
    request.flush(call.response);

    expect(states).toEqual([LOADING, { status: 'data', data: call.response }]);
  });

  it('should end in an error with the code of the API when it answers 503', () => {
    const { api, controller } = setUp();
    const states = record(call.start(api));

    onlyRequest(controller).flush(
      { status: 503, code: 'service_unavailable', detail: 'No disponible.' },
      { status: 503, statusText: 'Service Unavailable' },
    );

    const error = { code: 'service_unavailable', fieldErrors: [] };
    expect(states).toEqual([LOADING, { status: 'error', error }]);
  });

  it('should end in a network error when no response arrives', () => {
    const { api, controller } = setUp();
    const states = record(call.start(api));

    onlyRequest(controller).error(new ProgressEvent('error'));

    const error = { code: 'network_error', fieldErrors: [] };
    expect(states).toEqual([LOADING, { status: 'error', error }]);
  });

  it('should end in a timeout and cancel the request when 10 s pass in silence', () => {
    vi.useFakeTimers();
    const { api, controller } = setUp();
    const states = record(call.start(api));
    const request = onlyRequest(controller);

    vi.advanceTimersByTime(9_999);
    expect(states).toEqual([LOADING]);
    vi.advanceTimersByTime(1);

    expect(states).toEqual([
      LOADING,
      { status: 'error', error: { code: 'timeout', fieldErrors: [] } },
    ]);
    expect(request.cancelled).toBe(true);
  });

  it('should send only what the contract says: method, URL, JSON body, no headers of its own', () => {
    const { api, controller } = setUp();
    record(call.start(api));
    const request = onlyRequest(controller).request;

    expect(request.method).toBe(call.method);
    expect(request.urlWithParams).toBe(call.url);
    expect(request.body).toEqual(call.body);
    expect(request.headers.keys()).toEqual([]);
    expect(request.responseType).toBe('json');
    expect(request.withCredentials).toBe(false);
  });
});

describe('BackendApi.searchCustomers · SPEC-04/E-51', () => {
  function requestFor(text: string): TestRequest['request'] {
    const { api, controller } = setUp();
    record(api.searchCustomers(text));
    return onlyRequest(controller).request;
  }

  it('should send no q when the text is empty', () => {
    const request = requestFor('');

    expect(request.urlWithParams).toBe(`${BASE}/customers`);
    expect(request.params.has('q')).toBe(false);
  });

  it('should send the text as it is written, without trimming it, when it is only spaces', () => {
    const request = requestFor(SPACE.repeat(3));

    expect(request.urlWithParams).toBe(`${BASE}/customers?q=%20%20%20`);
  });

  it('should leave the encoding to the HTTP client when the text has reserved characters', () => {
    const request = requestFor('100% a+b&c#d');

    expect(request.params.getAll('q')).toEqual(['100% a+b&c#d']);
    expect(request.urlWithParams).toBe(`${BASE}/customers?q=100%25%20a%2Bb%26c%23d`);
  });

  it('should send U+FFFD in place of a lone surrogate, which a URL cannot carry', () => {
    const request = requestFor('a' + HIGH_SURROGATE + 'b');

    expect(request.params.get('q')).toBe('a' + REPLACEMENT + 'b');
  });

  it('should send a well-formed emoji untouched', () => {
    const request = requestFor(GRINNING_FACE.repeat(100));

    expect(request.params.get('q')).toBe(GRINNING_FACE.repeat(100));
  });
});

describe('BackendApi.createCustomer · SPEC-04/E-46', () => {
  function bodyFor(customer: NewCustomer): unknown {
    const { api, controller } = setUp();
    record(api.createCustomer(customer));
    return onlyRequest(controller).request.body;
  }

  it('should trim U+0020 from the name and the email and send the tax id as written', () => {
    const body = bodyFor({
      ...NEW_CUSTOMER,
      company_name: SPACE + SPACE + 'Ejemplo Uno SL' + SPACE,
      contact_email: SPACE + 'compras@ejemplo-uno.example' + SPACE,
      tax_id: '12345678Z' + SPACE.repeat(21),
    });

    expect(body).toEqual({ ...NEW_CUSTOMER, tax_id: '12345678Z' + SPACE.repeat(21) });
  });

  it('should trim nothing but U+0020', () => {
    const body = bodyFor({ ...NEW_CUSTOMER, company_name: 'AB' + NO_BREAK_SPACE });

    expect(body).toEqual({ ...NEW_CUSTOMER, company_name: 'AB' + NO_BREAK_SPACE });
  });

  it('should send the five fields of the contract and nothing else', () => {
    const withExtra = { ...NEW_CUSTOMER, zeta: 'de más' };

    expect(bodyFor(withExtra)).toEqual(NEW_CUSTOMER);
  });
});

describe('BackendApi · SPEC-04/E-47, E-49', () => {
  it('should ask for a customer with the exact text of its id', () => {
    const { api, controller } = setUp();
    record(api.getCustomer(routeId('9007199254740991')));

    expect(onlyRequest(controller).request.url).toBe(`${BASE}/customers/9007199254740991`);
  });

  it('should send the numbers of a quote and of a simulation as JSON integers', () => {
    const { api, controller } = setUp();
    record(api.quote({ customer_id: 7, active_users: 15 }));
    record(api.saveSimulation({ ...NEW_SIMULATION, zeta: 1 } as typeof NEW_SIMULATION));

    const [quote, simulation] = controller.match(() => true);
    expect(JSON.stringify(quote?.request.body)).toBe('{"customer_id":7,"active_users":15}');
    expect(JSON.stringify(simulation?.request.body)).toBe(
      '{"customer_id":7,"active_users":15,"storage_gb":500,"estimated_api_calls":250000}',
    );
  });
});
