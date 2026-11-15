import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  TestRequest,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';

import { BACKEND_BASE_URL } from '../../core/backend-api';
import { MetaStore } from '../../core/meta-store';
import { Alta } from './alta';

const META_URL = `${BACKEND_BASE_URL}/meta`;
const CUSTOMERS_URL = `${BACKEND_BASE_URL}/customers`;
const SPACE = String.fromCodePoint(0x20);
const TAB = String.fromCodePoint(0x09);
const NO_BREAK_SPACE = String.fromCodePoint(0xa0);
const DOUBLE_STRUCK_A = String.fromCodePoint(0x1d538);
const HIGH_SURROGATE = String.fromCharCode(0xd800);

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
const UNAVAILABLE = 'El servicio no está disponible en este momento.';
const UNEXPECTED = 'Se ha producido un error inesperado.';
const OFFLINE = 'No se ha podido conectar con el servidor.';
const TIMED_OUT = 'El servidor tarda demasiado en responder.';
const ALREADY_EXISTS = 'Ya existe un cliente con ese identificador fiscal en ese país.';

interface Values {
  readonly name: string;
  readonly taxId: string;
  readonly email: string;
  readonly country: string;
  readonly plan: string;
}

// The request and the responses of SPEC-01, 4.1. The name is the one of the example once
// trimmed; the row of 5.4 with its spaces is in the table of the values that are sent.
const VALID: Values = {
  name: 'Ejemplo Uno SL',
  taxId: 'b-1234567 4',
  email: 'compras@ejemplo-uno.example',
  country: 'ES',
  plan: 'professional',
};
const VALID_BODY = {
  company_name: VALID.name,
  tax_id: VALID.taxId,
  contact_email: VALID.email,
  country: VALID.country,
  plan: VALID.plan,
};
const CREATED = { ...VALID_BODY, id: 7, tax_id: 'B12345674', created_at: '2026-11-12T14:30:00Z' };
const CONFLICT = {
  type: 'about:blank',
  title: 'Conflict',
  status: 409,
  code: 'customer_already_exists',
  detail: 'Ya existe un cliente con ese identificador fiscal en ese país.',
};
const BAD_CHECK_CHARACTER = fieldError(
  'tax_id',
  'invalid_tax_id_check_character',
  'El carácter de control del identificador fiscal no es correcto.',
);
const BAD_FORMAT = fieldError(
  'tax_id',
  'invalid_tax_id_format',
  'El identificador fiscal no tiene un formato válido.',
);
const SHORT_NAME = fieldError('company_name', 'too_short', 'Debe tener entre 2 y 120 caracteres.');
const BAD_EMAIL = fieldError(
  'contact_email',
  'invalid_email',
  'El email no tiene un formato válido.',
);
const BAD_NAME = fieldError(
  'company_name',
  'invalid_characters',
  'Contiene caracteres no admitidos.',
);
const BAD_PLAN = fieldError('plan', 'unsupported_plan', 'El plan no existe.');

const CONTROL_IDS: Record<keyof Values, string> = {
  name: 'alta-name',
  taxId: 'alta-tax-id',
  email: 'alta-email',
  country: 'alta-country',
  plan: 'alta-plan',
};

interface FieldErrorBody {
  readonly field: string;
  readonly code: string;
  readonly message: string;
}

function fieldError(field: string, code: string, message: string): FieldErrorBody {
  return { field, code, message };
}

/** The 422 of SPEC-01, 4.1, with the given `errors`. */
function invalid(errors: unknown[]): object {
  return {
    type: 'about:blank',
    title: 'Unprocessable Content',
    status: 422,
    code: 'validation_error',
    detail: 'La petición contiene datos no válidos.',
    errors,
  };
}

@Component({ template: '', changeDetection: ChangeDetectionStrategy.OnPush })
class Blank {}

interface Page {
  readonly fixture: ComponentFixture<Alta>;
  readonly element: HTMLElement;
  readonly controller: HttpTestingController;
}

function open(meta: 'answered' | 'failed' = 'answered'): Page {
  TestBed.configureTestingModule({
    providers: [
      provideRouter([{ path: 'clientes/:id', component: Blank }]),
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
  const fixture = TestBed.createComponent(Alta);
  fixture.detectChanges();
  return { fixture, element: fixture.nativeElement as HTMLElement, controller };
}

function control(page: Page, field: keyof Values): HTMLInputElement | HTMLSelectElement | null {
  return page.element.querySelector(`#${CONTROL_IDS[field]}`);
}

function fill(page: Page, values: Partial<Values>): void {
  for (const [field, value] of Object.entries(values) as [keyof Values, string][]) {
    const element = control(page, field);
    expect(element).not.toBeNull();
    if (element) {
      element.value = value;
      element.dispatchEvent(new Event(element instanceof HTMLSelectElement ? 'change' : 'input'));
    }
  }
  page.fixture.detectChanges();
}

function press(page: Page, label: string): void {
  const buttons = Array.from(page.element.querySelectorAll('button'));
  const button = buttons.find((candidate) => candidate.textContent?.trim() === label);
  expect(button).toBeDefined();
  button?.click();
  page.fixture.detectChanges();
}

/** The sign-up requests made since the last time they were asked for. */
function posts(page: Page): TestRequest[] {
  return page.controller.match(
    (request) => request.method === 'POST' && request.url === CUSTOMERS_URL,
  );
}

function onlyPost(page: Page): TestRequest {
  const requests = posts(page);
  expect(requests.length).toBe(1);
  return requests[0];
}

/** Fills the form with valid values plus the given ones and presses «Guardar». */
function send(page: Page, values: Partial<Values> = {}): void {
  fill(page, { ...VALID, ...values });
  press(page, 'Guardar');
}

function reject(page: Page, status: number, body: object | string): void {
  onlyPost(page).flush(body, { status, statusText: 'Error' });
  page.fixture.detectChanges();
}

function errorOf(page: Page, field: keyof Values): string {
  return page.element.querySelector(`#${CONTROL_IDS[field]}-error`)?.textContent?.trim() ?? '';
}

function notice(page: Page): string {
  return page.element.querySelector('.form-notice')?.textContent ?? '';
}

function written(page: Page): Values {
  return {
    name: control(page, 'name')?.value ?? '',
    taxId: control(page, 'taxId')?.value ?? '',
    email: control(page, 'email')?.value ?? '',
    country: control(page, 'country')?.value ?? '',
    plan: control(page, 'plan')?.value ?? '',
  };
}

function url(): string {
  return TestBed.inject(Router).url;
}

// CA-05: every row of the table of SPEC-04, 5.4. CA-16: the rows of 5.6 for `POST /customers`.
describe('Alta · SPEC-04/E-05 a E-11, E-40 a E-46 (CA-05, CA-06, CA-16)', () => {
  afterEach(() => vi.useRealTimers());

  it('should offer exactly the countries and plans of /meta, by name and in its order', () => {
    const page = open();

    const options = (field: keyof Values): string[][] =>
      Array.from(control(page, field)?.querySelectorAll('option:not([disabled])') ?? []).map(
        (option) => [(option as HTMLOptionElement).value, option.textContent?.trim() ?? ''],
      );

    expect(options('country')).toEqual(
      META.countries.map((country) => [country.code, country.name]),
    );
    expect(options('plan')).toEqual(META.plans.map((plan) => [plan.code, plan.name]));
  });

  it('should send the codes of the chosen country and plan, and go to the detail on 201', async () => {
    const page = open();

    send(page, { country: 'PT', plan: 'starter' });
    const request = onlyPost(page);
    // No `Location` header: the id is the one of the body (E-46).
    request.flush(
      { ...CREATED, country: 'PT', plan: 'starter' },
      { status: 201, statusText: 'Created' },
    );
    await page.fixture.whenStable();

    expect(request.request.body).toEqual({ ...VALID_BODY, country: 'PT', plan: 'starter' });
    expect(url()).toBe('/clientes/7');
  });

  it.each([
    ['61 characters outside the basic plane', { name: DOUBLE_STRUCK_A.repeat(61) }, {}],
    ['a tab before the name', { name: TAB + 'AB' }, {}],
    ['a no-break space after the name', { name: 'AB' + NO_BREAK_SPACE }, {}],
    [
      'spaces around the name',
      { name: SPACE + SPACE + 'Ejemplo Uno SL' + SPACE },
      { name: 'Ejemplo Uno SL' },
    ],
    ['an email with a letter that is not ASCII', { email: 'josé@empresa.example' }, {}],
    ['an email without a dot in the domain', { email: 'a@b' }, {}],
    ['an email with a no-break space', { email: 'a' + NO_BREAK_SPACE + 'b@c.example' }, {}],
    [
      'an email of 254 characters between spaces',
      { email: SPACE + 'a'.repeat(241) + '@empresa.test' + SPACE },
      { email: 'a'.repeat(241) + '@empresa.test' },
    ],
    ['a tax id of 30 characters with its spaces', { taxId: '12345678Z' + SPACE.repeat(21) }, {}],
    ['a tax id of only spaces', { taxId: SPACE.repeat(3) }, {}],
  ])('should send it, with no help in the way, when the form has %s', (_case, values, trimmed) => {
    const page = open();

    send(page, values);

    const sent = { ...VALID, ...values, ...trimmed };
    expect(onlyPost(page).request.body).toEqual({
      ...VALID_BODY,
      company_name: sent.name,
      tax_id: sent.taxId,
      contact_email: sent.email,
    });
  });

  it.each<[string, Partial<Values>, FieldErrorBody, keyof Values]>([
    ['a tab before the name', { name: TAB + 'AB' }, BAD_NAME, 'name'],
    ['an email without a dot in the domain', { email: 'a@b' }, BAD_EMAIL, 'email'],
    [
      'an email with a no-break space',
      { email: 'a' + NO_BREAK_SPACE + 'b@c.example' },
      BAD_EMAIL,
      'email',
    ],
    ['a tax id of only spaces', { taxId: SPACE.repeat(3) }, BAD_FORMAT, 'taxId'],
  ])(
    'should show the 422 of the backend next to the field when the help let through %s',
    (_case, values, verdict, field) => {
      const page = open();
      send(page, values);

      reject(page, 422, invalid([verdict]));

      expect(errorOf(page, field)).toBe(verdict.message);
      expect(control(page, field)?.getAttribute('aria-invalid')).toBe('true');
      expect(written(page)).toEqual({ ...VALID, ...values });
    },
  );

  it.each<[string, Partial<Values>, keyof Values]>([
    ['a name of 121 characters', { name: 'ñ'.repeat(121) }, 'name'],
    ['a name of one character after trimming', { name: SPACE + 'A' + SPACE }, 'name'],
    ['a name with a lone surrogate', { name: 'AB' + HIGH_SURROGATE }, 'name'],
    ['no name', { name: '' }, 'name'],
    ['an email without an at sign', { email: 'sin-arroba.example' }, 'email'],
    ['an email that starts with the at sign', { email: '@b.example' }, 'email'],
    ['an email that ends with the at sign', { email: 'a@' }, 'email'],
    [
      'an email of 255 characters after trimming',
      { email: 'a'.repeat(242) + '@empresa.test' },
      'email',
    ],
    ['an email with a lone surrogate', { email: 'a' + HIGH_SURROGATE + '@b.example' }, 'email'],
    ['no email', { email: SPACE }, 'email'],
    ['a tax id of 31 characters, untrimmed', { taxId: '12345678Z' + SPACE.repeat(22) }, 'taxId'],
    ['a tax id with a lone surrogate', { taxId: 'B1234567' + HIGH_SURROGATE }, 'taxId'],
    ['no tax id', { taxId: '' }, 'taxId'],
    ['no country', { country: '' }, 'country'],
    ['no plan', { plan: '' }, 'plan'],
  ])(
    'should show the help next to the field and not send when the form has %s',
    (_case, values, field) => {
      const page = open();

      send(page, values);

      expect(posts(page).length).toBe(0);
      expect(errorOf(page, field)).not.toBe('');
      expect(control(page, field)?.getAttribute('aria-invalid')).toBe('true');
    },
  );

  it('should show no help before the first attempt to send', () => {
    const page = open();

    fill(page, { name: 'A' });

    expect(errorOf(page, 'name')).toBe('');
    expect(control(page, 'name')?.getAttribute('aria-invalid')).toBe('false');
  });

  it('should send once the help has nothing left to say', () => {
    const page = open();
    send(page, { name: 'A' });

    fill(page, { name: 'AB' });
    press(page, 'Guardar');

    expect(errorOf(page, 'name')).toBe('');
    expect(onlyPost(page).request.body).toEqual({ ...VALID_BODY, company_name: 'AB' });
  });

  it.each([
    ['invalid_tax_id_format', BAD_FORMAT],
    ['invalid_tax_id_check_character', BAD_CHECK_CHARACTER],
  ])(
    'should show the message of the backend next to the tax id when it answers 422 %s',
    (_code, error) => {
      const page = open();
      send(page);

      reject(page, 422, invalid([error]));

      expect(errorOf(page, 'taxId')).toBe(error.message);
      expect(written(page)).toEqual(VALID);
      expect(notice(page)).toBe('');
    },
  );

  it('should show each message in its field when it answers 422 with two fields', () => {
    const page = open();
    send(page);

    reject(page, 422, invalid([SHORT_NAME, BAD_EMAIL]));

    expect(errorOf(page, 'name')).toBe(SHORT_NAME.message);
    expect(errorOf(page, 'email')).toBe(BAD_EMAIL.message);
    expect(written(page)).toEqual(VALID);
  });

  it('should show next to its field an error whose code it does not know', () => {
    const page = open();
    send(page);

    reject(page, 422, invalid([fieldError('country', 'a_code_of_tomorrow', 'Un mensaje nuevo.')]));

    expect(errorOf(page, 'country')).toBe('Un mensaje nuevo.');
  });

  it('should show in the general notice the error of a field the form does not have', () => {
    const page = open();
    send(page);

    reject(
      page,
      422,
      invalid([BAD_PLAN, fieldError('zeta', 'unknown_field', 'Campo no reconocido.')]),
    );

    expect(errorOf(page, 'plan')).toBe(BAD_PLAN.message);
    expect(notice(page)).toContain('Campo no reconocido.');
    expect(notice(page)).not.toContain(BAD_PLAN.message);
    // Sending the same again would bring the same 422: no «Reintentar» (SPEC-04, 2.3).
    expect(page.element.querySelector('.form-notice button')).toBeNull();
  });

  it('should ignore an entry of errors without the shape of the contract', () => {
    const page = open();
    send(page);

    reject(page, 422, invalid([BAD_PLAN, { field: 'tax_id', code: 'invalid_tax_id_format' }]));

    expect(errorOf(page, 'plan')).toBe(BAD_PLAN.message);
    expect(errorOf(page, 'taxId')).toBe('');
    expect(notice(page)).toBe('');
  });

  it('should keep the first error of a field and show a second one in the general notice', () => {
    const page = open();
    send(page);

    reject(page, 422, invalid([BAD_FORMAT, fieldError('tax_id', 'too_long', 'Segundo mensaje.')]));

    expect(errorOf(page, 'taxId')).toBe(BAD_FORMAT.message);
    expect(notice(page)).toContain('Segundo mensaje.');
  });

  it('should show the unexpected error notice when a 422 brings nothing that can be shown', () => {
    const page = open();
    send(page);

    reject(page, 422, invalid([{ field: 'x' }, 'texto']));

    expect(notice(page)).toContain(UNEXPECTED);
    expect(written(page)).toEqual(VALID);
  });

  it('should drop the message of the backend once the field is edited', () => {
    const page = open();
    send(page);
    reject(page, 422, invalid([BAD_FORMAT]));

    fill(page, { taxId: 'B12345674' });

    expect(errorOf(page, 'taxId')).toBe('');
  });

  it('should warn that the customer exists, keep the values and stay, when it answers 409', async () => {
    const page = open();
    send(page);

    reject(page, 409, CONFLICT);
    await page.fixture.whenStable();

    expect(notice(page)).toContain(ALREADY_EXISTS);
    // Sending the same again cannot help: no «Reintentar» (SPEC-04, 2.3).
    expect(page.element.querySelector('.form-notice button')).toBeNull();
    expect(written(page)).toEqual(VALID);
    expect(url()).not.toContain('/clientes/');
  });

  it('should not change when only the text of the error changes: the code decides (CA-06)', () => {
    const page = open();
    send(page);
    reject(page, 409, CONFLICT);
    const before = notice(page);

    press(page, 'Guardar');
    reject(page, 409, { ...CONFLICT, detail: 'Otro texto distinto.' });

    expect(before).not.toBe('');
    expect(notice(page)).toBe(before);
  });

  it.each<[string, number, object | string, string]>([
    ['500 internal_error', 500, { code: 'internal_error' }, UNEXPECTED],
    ['503 service_unavailable', 503, { code: 'service_unavailable' }, UNAVAILABLE],
    ['400 malformed_request', 400, { code: 'malformed_request' }, UNEXPECTED],
    ['a code it does not know', 418, { code: 'teapot' }, UNEXPECTED],
    ['502 with a body that is not JSON', 502, '<html>Bad Gateway</html>', UNEXPECTED],
  ])(
    'should show the general notice with a retry, keep the values and stay, when it answers %s',
    async (_case, status, body, expected) => {
      const page = open();
      send(page);

      reject(page, status, body);
      await page.fixture.whenStable();

      expect(notice(page)).toContain(expected);
      expect(written(page)).toEqual(VALID);
      expect(url()).not.toContain('/clientes/');
      press(page, 'Reintentar');
      expect(onlyPost(page).request.body).toEqual(VALID_BODY);
    },
  );

  it('should show the connection notice with a retry when no response arrives', () => {
    const page = open();
    send(page);

    onlyPost(page).error(new ProgressEvent('error'));
    page.fixture.detectChanges();

    expect(notice(page)).toContain(OFFLINE);
    expect(notice(page)).toContain('Reintentar');
  });

  it('should show the timeout notice with a retry when no response arrives in 10 s', () => {
    vi.useFakeTimers();
    const page = open();
    send(page);

    vi.advanceTimersByTime(10_000);
    page.fixture.detectChanges();

    expect(notice(page)).toContain(TIMED_OUT);
    expect(notice(page)).toContain('Reintentar');
    expect(written(page)).toEqual(VALID);
  });

  it('should send what the form holds now when «Reintentar» is pressed after an edit', () => {
    const page = open();
    send(page);
    reject(page, 500, { code: 'internal_error' });

    fill(page, { name: 'Ejemplo Dos SL' });
    press(page, 'Reintentar');

    expect(onlyPost(page).request.body).toEqual({ ...VALID_BODY, company_name: 'Ejemplo Dos SL' });
  });

  it('should send a single request when «Guardar» is pressed twice', () => {
    const page = open();
    send(page);

    press(page, 'Guardar');

    expect(posts(page).length).toBe(1);
  });

  it('should show the error of /meta with a retry instead of the form when /meta fails', () => {
    const page = open('failed');

    const alert = page.element.querySelector('[role="alert"]');
    expect(alert?.textContent ?? '').toContain(UNEXPECTED);
    expect(alert?.querySelector('button')?.textContent?.trim()).toBe('Reintentar');
    expect(page.element.querySelector('form')).toBeNull();
  });

  it('should leave the measuring to the help: no maxlength, no email type, no spell checker', () => {
    const page = open();

    for (const field of ['name', 'taxId', 'email'] as const) {
      expect(control(page, field)?.getAttribute('type')).toBe('text');
      expect(control(page, field)?.hasAttribute('maxlength')).toBe(false);
      expect(control(page, field)?.getAttribute('spellcheck')).toBe('false');
    }
  });
});

// The rows of the focus of SPEC-04, 5.4.
// SPEC-04, 2.7: the message next to a field of the sign-up is read with its field, which points
// at it; as an alert, an empty form would announce its five messages at once.
describe('Alta · los mensajes de campo no son alertas · SPEC-04 2.7', () => {
  const FIELDS = Object.keys(CONTROL_IDS) as (keyof Values)[];

  it('should show the five messages without role="alert", each one described by its field, when the form is sent empty', () => {
    const page = open();

    press(page, 'Guardar');

    for (const field of FIELDS) {
      const message = page.element.querySelector(`#${CONTROL_IDS[field]}-error`);
      expect(message?.textContent?.trim()).toBeTruthy();
      expect(message?.getAttribute('role')).toBeNull();
      expect(control(page, field)?.getAttribute('aria-invalid')).toBe('true');
      expect(control(page, field)?.getAttribute('aria-describedby')).toBe(
        `${CONTROL_IDS[field]}-error`,
      );
    }
    expect(page.element.querySelectorAll('[role="alert"]').length).toBe(0);
  });

  it('should show the 422 of the backend next to its field without role="alert"', () => {
    const page = open();
    send(page);

    reject(page, 422, invalid([BAD_PLAN]));

    const message = page.element.querySelector(`#${CONTROL_IDS.plan}-error`);
    expect(message?.textContent?.trim()).toBe(BAD_PLAN.message);
    expect(message?.getAttribute('role')).toBeNull();
    expect(control(page, 'plan')?.getAttribute('aria-describedby')).toBe(
      `${CONTROL_IDS.plan}-error`,
    );
  });
});

describe('Alta · el foco tras un envío con errores · SPEC-04/E-56 (CA-05)', () => {
  function focused(): string {
    return document.activeElement?.id ?? '';
  }

  it.each<[string, Partial<Values>, keyof Values]>([
    ['neither a name nor an email', { name: '', email: '' }, 'name'],
    ['only the email wrong', { email: 'sin-arroba.example' }, 'email'],
    ['no plan', { plan: '' }, 'plan'],
  ])(
    'should move the focus to the first field with help when the form has %s',
    (_case, values, field) => {
      const page = open();

      send(page, values);

      expect(posts(page).length).toBe(0);
      expect(focused()).toBe(CONTROL_IDS[field]);
    },
  );

  it.each<[string, FieldErrorBody[], keyof Values]>([
    ['the name and the email', [SHORT_NAME, BAD_EMAIL], 'name'],
    ['the email and the name, in that order', [BAD_EMAIL, SHORT_NAME], 'name'],
    ['the tax id', [BAD_FORMAT], 'taxId'],
    ['the plan', [BAD_PLAN], 'plan'],
  ])(
    'should move the focus to the first field of the form with an error when a 422 rejects %s',
    (_case, errors, field) => {
      const page = open();
      send(page);

      reject(page, 422, invalid(errors));

      expect(focused()).toBe(CONTROL_IDS[field]);
    },
  );

  it.each<[string, number, object]>([
    ['409 customer_already_exists', 409, CONFLICT],
    ['500 internal_error', 500, { code: 'internal_error' }],
    [
      'a 422 with only an unknown field',
      422,
      invalid([fieldError('zeta', 'unknown_field', 'Campo no reconocido.')]),
    ],
  ])('should leave the focus where it was when it answers %s', (_case, status, body) => {
    const page = open();
    send(page);
    const before = document.activeElement;

    reject(page, status, body);

    expect(notice(page)).not.toBe('');
    expect(document.activeElement).toBe(before);
  });
});
