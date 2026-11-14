import { HttpErrorResponse } from '@angular/common/http';
import { TimeoutError } from 'rxjs';

import {
  ApiError,
  FieldError,
  formErrors,
  noticeFor,
  splitFieldErrors,
  toApiError,
} from './api-error';

const UNAVAILABLE =
  'El servicio no está disponible en este momento. Inténtalo de nuevo dentro de unos minutos.';
const UNEXPECTED = 'Se ha producido un error inesperado.';
const OFFLINE = 'No se ha podido conectar con el servidor.';
const TOO_SLOW = 'El servidor tarda demasiado en responder.';

/** A response with the shape of the error example of the common conventions (specs index). */
function problem(status: number, code: string, extra: object = {}): HttpErrorResponse {
  const body = { type: 'about:blank', title: 'Error', status, code, detail: 'Texto.', ...extra };
  return new HttpErrorResponse({ status, error: body });
}

function fieldError(field: string, code: string): FieldError {
  return { field, code, message: `Mensaje de ${field}.` };
}

describe('toApiError · SPEC-04/E-11, E-42, E-43', () => {
  it.each([
    [503, 'service_unavailable'],
    [500, 'internal_error'],
    [500, 'tax_rate_not_defined'],
    [400, 'malformed_request'],
    [415, 'unsupported_media_type'],
    [405, 'method_not_allowed'],
    [404, 'not_found'],
    [404, 'customer_not_found'],
    [409, 'customer_already_exists'],
    [418, 'teapot'],
  ])('should keep the code of the API when it answers %d with %s', (status, code) => {
    expect(toApiError(problem(status, code))).toEqual({ code, fieldErrors: [] });
  });

  it('should keep the errors of each field, in their order, when it answers 422', () => {
    const errors = [fieldError('company_name', 'too_short'), fieldError('zeta', 'unknown_field')];

    const error = toApiError(problem(422, 'validation_error', { errors }));

    expect(error).toEqual({ code: 'validation_error', fieldErrors: errors });
  });

  it.each([
    ['a body that is not JSON', 'Bad Gateway'],
    ['an empty body', null],
    ['a JSON body without a code', { status: 502 }],
    ['a code that is not a text', { code: 7 }],
  ])('should say unknown_error when the response has %s', (_case, body) => {
    const response = new HttpErrorResponse({ status: 502, error: body });

    expect(toApiError(response)).toEqual({ code: 'unknown_error', fieldErrors: [] });
  });

  it('should say network_error when there is no response', () => {
    const response = new HttpErrorResponse({ status: 0, error: new ProgressEvent('error') });

    expect(toApiError(response)).toEqual({ code: 'network_error', fieldErrors: [] });
  });

  it('should say timeout when the wait runs out', () => {
    expect(toApiError(new TimeoutError())).toEqual({ code: 'timeout', fieldErrors: [] });
  });

  it('should ignore errors of a field that do not have the shape of the contract', () => {
    const errors = [fieldError('plan', 'not_a_valid_choice'), { field: 'x' }, 'texto', null];

    const error = toApiError(problem(422, 'validation_error', { errors }));

    expect(error.fieldErrors).toEqual([fieldError('plan', 'not_a_valid_choice')]);
  });

  it('should not change when only the texts of the response change (CA-06)', () => {
    const one = problem(503, 'service_unavailable', { detail: 'Un texto.', title: 'Uno' });
    const other = problem(503, 'service_unavailable', { detail: 'Otro distinto.', title: 'Dos' });

    expect(toApiError(one)).toEqual(toApiError(other));
  });
});

// The table of SPEC-04, 2.7, and the rows of 5.6 that do not depend on a view.
describe('noticeFor · SPEC-04/E-42, E-43', () => {
  it.each([
    ['service_unavailable', UNAVAILABLE],
    ['internal_error', UNEXPECTED],
    ['tax_rate_not_defined', UNEXPECTED],
    ['malformed_request', UNEXPECTED],
    ['unsupported_media_type', UNEXPECTED],
    ['method_not_allowed', UNEXPECTED],
    ['not_found', UNEXPECTED],
    ['validation_error', UNEXPECTED],
    ['teapot', UNEXPECTED],
    ['unknown_error', UNEXPECTED],
    ['network_error', OFFLINE],
    ['timeout', TOO_SLOW],
  ])('should choose the notice by the code when it is %s', (code, expected) => {
    const error: ApiError = { code, fieldErrors: [] };

    expect(noticeFor(error)).toBe(expected);
  });
});

describe('splitFieldErrors · SPEC-04/E-09, E-48', () => {
  const FORM = ['company_name', 'tax_id', 'contact_email', 'country', 'plan'];

  it('should put each error next to its field when the form has it (5.4)', () => {
    const name = fieldError('company_name', 'too_short');
    const email = fieldError('contact_email', 'invalid_email');

    const split = splitFieldErrors([name, email], FORM);

    expect(split).toEqual({ byField: { company_name: name, contact_email: email }, general: [] });
  });

  it('should send to the general notice the errors of fields the form does not have (5.4)', () => {
    const plan = fieldError('plan', 'not_a_valid_choice');
    const unknown = fieldError('zeta', 'unknown_field');

    const split = splitFieldErrors([plan, unknown], FORM);

    expect(split).toEqual({ byField: { plan }, general: [unknown] });
  });

  it('should keep the first error of a field and not lose a second one', () => {
    const first = fieldError('tax_id', 'invalid_tax_id_format');
    const second = fieldError('tax_id', 'too_long');

    const split = splitFieldErrors([first, second], FORM);

    expect(split).toEqual({ byField: { tax_id: first }, general: [second] });
  });

  it('should return nothing when there are no errors', () => {
    expect(splitFieldErrors([], FORM)).toEqual({ byField: {}, general: [] });
  });
});

describe('formErrors · SPEC-04/E-09, E-48 (2.3)', () => {
  const FORM = ['active_users', 'storage_gb'];

  it('should show nothing when there is no error', () => {
    expect(formErrors(null, FORM)).toEqual({ byField: {}, notice: null });
  });

  it('should give each field its error, with no notice, when every error has its field', () => {
    const users = fieldError('active_users', 'out_of_range');
    const error: ApiError = { code: 'validation_error', fieldErrors: [users] };

    expect(formErrors(error, FORM)).toEqual({ byField: { active_users: users }, notice: null });
  });

  it('should list in a notice without retry the errors of fields the form does not have', () => {
    const storage = fieldError('storage_gb', 'out_of_range');
    const customer = fieldError('customer_id', 'out_of_range');
    const unknown = fieldError('zeta', 'unknown_field');
    const error: ApiError = { code: 'validation_error', fieldErrors: [storage, customer, unknown] };

    expect(formErrors(error, FORM)).toEqual({
      byField: { storage_gb: storage },
      notice: { messages: [customer.message, unknown.message], retryable: false },
    });
  });

  it('should treat as unexpected a validation error that leaves nothing to show', () => {
    const error: ApiError = { code: 'validation_error', fieldErrors: [] };

    expect(formErrors(error, FORM)).toEqual({
      byField: {},
      notice: { messages: [UNEXPECTED], retryable: true },
    });
  });

  it.each([
    ['service_unavailable', UNAVAILABLE],
    ['network_error', OFFLINE],
    ['timeout', TOO_SLOW],
    ['internal_error', UNEXPECTED],
    ['teapot', UNEXPECTED],
  ])('should give the notice of the code %s, with a retry and no field', (code, expected) => {
    const error: ApiError = { code, fieldErrors: [] };

    expect(formErrors(error, FORM)).toEqual({
      byField: {},
      notice: { messages: [expected], retryable: true },
    });
  });

  it('should not read the field errors of an error that is not a validation error', () => {
    const stray = fieldError('active_users', 'out_of_range');
    const error: ApiError = { code: 'internal_error', fieldErrors: [stray] };

    expect(formErrors(error, FORM)).toEqual({
      byField: {},
      notice: { messages: [UNEXPECTED], retryable: true },
    });
  });
});
