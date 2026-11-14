import { HttpErrorResponse } from '@angular/common/http';
import { TimeoutError } from 'rxjs';

// Errors of the API, told apart by their stable `code` and never by their text (SPEC-04, 2.7).
// The texts of the notices belong to the frontend: the `detail` of the backend decides nothing.

/** Codes the frontend gives to a failure that brings no code of the API. */
export const NETWORK_ERROR = 'network_error';
export const TIMEOUT = 'timeout';
export const UNKNOWN_ERROR = 'unknown_error';
/** Generic code of the backend with a notice of its own: waiting is enough. */
export const SERVICE_UNAVAILABLE = 'service_unavailable';

const NOTICE_UNAVAILABLE =
  'El servicio no está disponible en este momento. Inténtalo de nuevo dentro de unos minutos.';
const NOTICE_OFFLINE = 'No se ha podido conectar con el servidor.';
const NOTICE_TIMEOUT = 'El servidor tarda demasiado en responder.';
const NOTICE_UNEXPECTED = 'Se ha producido un error inesperado.';

/** One entry of `errors` in a validation error: which field, why, and a text to show. */
export interface FieldError {
  readonly field: string;
  readonly code: string;
  readonly message: string;
}

/** Error state of a remote call. `code` is the one of the API when the response brings it. */
export interface ApiError {
  readonly code: string;
  readonly fieldErrors: readonly FieldError[];
}

export interface SplitFieldErrors {
  readonly byField: Readonly<Record<string, FieldError>>;
  readonly general: readonly FieldError[];
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isFieldError(value: unknown): value is FieldError {
  return (
    isRecord(value) &&
    typeof value['field'] === 'string' &&
    typeof value['code'] === 'string' &&
    typeof value['message'] === 'string'
  );
}

function fromResponseBody(body: unknown): ApiError {
  // A body that is not the one of the API (a proxy answering in HTML, for instance) has no code.
  if (!isRecord(body) || typeof body['code'] !== 'string') {
    return { code: UNKNOWN_ERROR, fieldErrors: [] };
  }
  const errors = Array.isArray(body['errors']) ? body['errors'] : [];
  return { code: body['code'], fieldErrors: errors.filter(isFieldError) };
}

/** Turns whatever a remote call failed with into an error state; nothing is swallowed. */
export function toApiError(failure: unknown): ApiError {
  if (failure instanceof TimeoutError) {
    return { code: TIMEOUT, fieldErrors: [] };
  }
  if (failure instanceof HttpErrorResponse) {
    // Status 0 is how the browser reports that no response arrived at all.
    return failure.status === 0
      ? { code: NETWORK_ERROR, fieldErrors: [] }
      : fromResponseBody(failure.error);
  }
  return { code: UNKNOWN_ERROR, fieldErrors: [] };
}

/** Text of the generic notice for an error that its view does not treat by its code. */
export function noticeFor(error: ApiError): string {
  switch (error.code) {
    case SERVICE_UNAVAILABLE:
      return NOTICE_UNAVAILABLE;
    case NETWORK_ERROR:
      return NOTICE_OFFLINE;
    case TIMEOUT:
      return NOTICE_TIMEOUT;
    default:
      return NOTICE_UNEXPECTED;
  }
}

/**
 * Shares the errors of a validation error between the fields of a form and its general notice.
 * The backend sends one error per field; a field the form does not have, or a second error of
 * the same field, goes to the general notice so that nothing is lost.
 */
export function splitFieldErrors(
  errors: readonly FieldError[],
  formFields: readonly string[],
): SplitFieldErrors {
  const byField: Record<string, FieldError> = {};
  const general: FieldError[] = [];
  for (const error of errors) {
    if (formFields.includes(error.field) && !(error.field in byField)) {
      byField[error.field] = error;
    } else {
      general.push(error);
    }
  }
  return { byField, general };
}
