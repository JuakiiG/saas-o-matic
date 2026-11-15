import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { MetaStore } from './meta-store';

const META_URL = `${environment.apiBaseUrl}/meta`;

// The example of SPEC-01, 4.4.
const META = {
  countries: [
    { code: 'ES', name: 'España', tax_rate_bp: 2100 },
    { code: 'PT', name: 'Portugal', tax_rate_bp: 2300 },
    { code: 'FR', name: 'Francia', tax_rate_bp: 2000 },
    { code: 'DE', name: 'Alemania', tax_rate_bp: 1900 },
    { code: 'IT', name: 'Italia', tax_rate_bp: 2200 },
    { code: 'NL', name: 'Países Bajos', tax_rate_bp: 2100 },
    { code: 'IE', name: 'Irlanda', tax_rate_bp: 2300 },
    { code: 'BE', name: 'Bélgica', tax_rate_bp: 2100 },
    { code: 'GB', name: 'Reino Unido', tax_rate_bp: 2000 },
  ],
  plans: [
    { code: 'starter', name: 'Básico' },
    { code: 'professional', name: 'Profesional' },
    { code: 'enterprise', name: 'Empresa' },
  ],
};
const SERVER_ERROR = { status: 500, statusText: 'Internal Server Error' };

describe('MetaStore · SPEC-04/E-33, E-35, E-39, E-40', () => {
  afterEach(() => vi.useRealTimers());

  function setUp(): { store: MetaStore; controller: HttpTestingController } {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    return { store: TestBed.inject(MetaStore), controller: TestBed.inject(HttpTestingController) };
  }

  /** Loads the store and answers its request with the example. */
  function loaded(): { store: MetaStore; controller: HttpTestingController } {
    const context = setUp();
    context.store.load();
    context.controller.match(META_URL).forEach((request) => request.flush(META));
    return context;
  }

  it('should be loading, with one request in flight, when it is loaded', () => {
    const { store, controller } = setUp();

    store.load();

    expect(store.state()).toEqual({ status: 'loading' });
    expect(controller.match(META_URL).length).toBe(1);
  });

  it('should keep the answer in memory and not ask again when it is loaded twice', () => {
    const { store, controller } = loaded();

    store.load();

    expect(store.state()).toEqual({ status: 'data', data: META });
    expect(controller.match(META_URL).length).toBe(0);
  });

  it('should not ask twice when it is loaded again before the answer arrives', () => {
    const { store, controller } = setUp();

    store.load();
    store.load();

    expect(controller.match(META_URL).length).toBe(1);
  });

  it.each([
    ['ES', 'España'],
    ['GB', 'Reino Unido'],
    ['XX', 'XX'],
  ])('should name the country %s as %s', (code, expected) => {
    expect(loaded().store.countryName(code)).toBe(expected);
  });

  it.each([
    ['professional', 'Profesional'],
    ['starter', 'Básico'],
    ['legacy', 'legacy'],
  ])('should name the plan %s as %s', (code, expected) => {
    expect(loaded().store.planName(code)).toBe(expected);
  });

  it('should end in an error state, with its code, when the request fails', () => {
    const { store, controller } = setUp();
    store.load();

    controller.match(META_URL)[0]?.flush({ code: 'internal_error' }, SERVER_ERROR);

    const error = { code: 'internal_error', fieldErrors: [] };
    expect(store.state()).toEqual({ status: 'error', error });
  });

  // CA-10 (E-33): the wait of 10 s belongs to `BackendApi`; the store has to end in its error,
  // so that the four views show the notice with «Reintentar» instead of loading for ever.
  it('should end in an error state with `timeout`, and ask again on a retry, when /meta does not answer in 10 s', () => {
    vi.useFakeTimers();
    const { store, controller } = setUp();
    store.load();
    const request = controller.match(META_URL)[0];

    vi.advanceTimersByTime(9_999);
    expect(store.state()).toEqual({ status: 'loading' });
    vi.advanceTimersByTime(1);

    expect(store.state()).toEqual({
      status: 'error',
      error: { code: 'timeout', fieldErrors: [] },
    });
    expect(request?.cancelled).toBe(true);
    store.retry();
    expect(controller.match(META_URL).length).toBe(1);
  });

  it('should ask once more when it is retried after a failure, and hold the data then', () => {
    const { store, controller } = setUp();
    store.load();
    controller.match(META_URL)[0]?.flush({ code: 'internal_error' }, SERVER_ERROR);

    store.retry();
    const retries = controller.match(META_URL);
    retries[0]?.flush(META);

    expect(retries.length).toBe(1);
    expect(store.state()).toEqual({ status: 'data', data: META });
  });

  it('should not ask again when it is retried with the data already there', () => {
    const { store, controller } = loaded();

    store.retry();

    expect(controller.match(META_URL).length).toBe(0);
    expect(store.state()).toEqual({ status: 'data', data: META });
  });
});
