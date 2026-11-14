import { ApiError, FieldError, FormErrors, FormNoticeView, TIMEOUT } from '../../core/api-error';
import { NewSimulation, Simulation } from '../../core/models';
import { Remote } from '../../core/remote';
import { Counts, SimuladorField, helpFor } from './simulador-help';

// What the simulator shows of its fields and of a failed save, as pure functions of its state.

const MAY_HAVE_BEEN_SAVED =
  'La simulación puede haberse guardado: compruébalo en el detalle del cliente antes de reintentar.';

/** Where the template shows the error of each field: the `id` its control points to. */
const ERROR_IDS: Readonly<Record<SimuladorField, string>> = {
  active_users: 'simulador-users-error',
  storage_gb: 'simulador-storage-error',
  estimated_api_calls: 'simulador-calls-error',
};

/** The fields of the form, by the names of the contract: an error finds its field by them. */
export const SIMULADOR_FIELDS = Object.keys(ERROR_IDS) as SimuladorField[];

/** A simulation that has been sent to be saved: what was sent and the state of its request. */
export interface Saving {
  readonly sent: NewSimulation;
  readonly state: Remote<Simulation>;
}

export interface FieldView {
  readonly error: string;
  readonly invalid: boolean;
  readonly errorId: string | null;
}

/** The notice of a failed save; on a timeout it also offers the detail of the customer. */
export interface SaveNotice extends FormNoticeView {
  readonly detailLink: string | null;
}

/** What the errors of the two requests of the simulator say about its fields. */
export interface SimuladorErrors {
  readonly projection: FormErrors;
  readonly save: FormErrors;
  /** What the failed save had sent: its messages stand while the fields still hold it. */
  readonly sent: NewSimulation | null;
}

/** The error of a request that ended in one; `null` in any other state. */
export function errorOf(
  state: { readonly status: string; readonly error?: ApiError } | undefined,
): ApiError | null {
  return state?.status === 'error' ? (state.error ?? null) : null;
}

function messageOf(errors: FormErrors, field: SimuladorField): string | null {
  const fieldError: FieldError | undefined = errors.byField[field];
  return fieldError?.message ?? null;
}

function fieldView(field: SimuladorField, counts: Counts, errors: SimuladorErrors): FieldView {
  const help = counts[field] === null ? helpFor(field) : null;
  const judged = errors.sent === null ? null : errors.sent[field];
  const fromSave = judged === counts[field] ? messageOf(errors.save, field) : null;
  const error = help ?? messageOf(errors.projection, field) ?? fromSave ?? '';
  const invalid = error !== '';
  return { error, invalid, errorId: invalid ? ERROR_IDS[field] : null };
}

/** The help of each field first; if it has nothing to say, the message of the backend. */
export function fieldViews(
  counts: Counts,
  errors: SimuladorErrors,
): Readonly<Record<SimuladorField, FieldView>> {
  return {
    active_users: fieldView('active_users', counts, errors),
    storage_gb: fieldView('storage_gb', counts, errors),
    estimated_api_calls: fieldView('estimated_api_calls', counts, errors),
  };
}

/** The notice of a failed save, with the link to the detail when the wait ran out (E-55). */
export function saveNoticeOf(
  error: ApiError | null,
  notice: FormNoticeView | null,
  customerId: number | null,
): SaveNotice | null {
  if (notice === null) {
    return null;
  }
  if (error?.code !== TIMEOUT || customerId === null) {
    return { ...notice, detailLink: null };
  }
  // The frontend stopped waiting, but the server may have finished: a blind retry would save
  // the same simulation twice.
  const messages = [...notice.messages, MAY_HAVE_BEEN_SAVED];
  return { messages, retryable: true, detailLink: `/clientes/${customerId}` };
}
