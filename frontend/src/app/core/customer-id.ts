// Shape of the `id` that a route carries after `/clientes/` (SPEC-04, 2.1).

// 1 to 16 ASCII digits, the first one not `0`: neither `01` nor `0` alone.
const SHAPE = /^[1-9][0-9]{0,15}$/;
// 2^53 − 1, the largest integer JavaScript represents exactly (known limitation L-06).
const LARGEST_EXACT_INTEGER = '9007199254740991';

/**
 * True when the text can be sent to the API as a customer id.
 *
 * The text is never turned into a number: JavaScript reads `01`, `+1` or `1.0` as 1, and one
 * customer would then have several addresses. Two digit strings of the same length compare as
 * numbers do, so the upper bound is checked on the text itself.
 */
export function isRouteCustomerId(text: string): boolean {
  if (!SHAPE.test(text)) {
    return false;
  }
  return text.length < LARGEST_EXACT_INTEGER.length || text <= LARGEST_EXACT_INTEGER;
}
