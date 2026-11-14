import { formatInteger } from '../../core/format';

// Help of the three number fields of the simulator (SPEC-04, 2.5). The limits are the ones of
// the contracts: SPEC-02, 4, for the users, and SPEC-03, 4.1, for the storage and the calls.

export const MAX_ACTIVE_USERS = 100_000;
export const MAX_STORAGE_GB = 1_000_000;
export const MAX_API_CALLS = 1_000_000_000;
/** The slider covers the usual range; the text box next to it, the whole of it. */
export const SLIDER_MAX_USERS = 500;

/** The number fields of the form, named as the fields of the contract. */
export type SimuladorField = 'active_users' | 'storage_gb' | 'estimated_api_calls';

/** What each field holds as a number; `null` when its text is not a valid one. */
export type Counts = Readonly<Record<SimuladorField, number | null>>;

const LIMITS: Readonly<Record<SimuladorField, number>> = {
  active_users: MAX_ACTIVE_USERS,
  storage_gb: MAX_STORAGE_GB,
  estimated_api_calls: MAX_API_CALLS,
};
const ONLY_ASCII_DIGITS = /^[0-9]+$/;

/**
 * The number a text box holds, or `null` when its text is not valid. The text decides, not the
 * number it would make: only ASCII digits, at least one, with a value from 0 to `max`. So `015`
 * is 15, while `15.0`, `1e3`, `+15` or `100000.000000000001`, which JavaScript reads as whole
 * numbers, are not valid.
 */
export function parseCount(text: string, max: number): number | null {
  if (!ONLY_ASCII_DIGITS.test(text)) {
    return null;
  }
  // Digits only, so this is a whole number; too many of them give a value over any limit.
  const value = Number(text);
  return value <= max ? value : null;
}

/** The numbers the three text boxes hold. */
export function countsOf(users: string, storage: string, calls: string): Counts {
  return {
    active_users: parseCount(users, LIMITS.active_users),
    storage_gb: parseCount(storage, LIMITS.storage_gb),
    estimated_api_calls: parseCount(calls, LIMITS.estimated_api_calls),
  };
}

/** What the help says next to a field whose text is not valid. */
export function helpFor(field: SimuladorField): string {
  return `Escribe un número entero de 0 a ${formatInteger(LIMITS[field])}, solo con cifras.`;
}
