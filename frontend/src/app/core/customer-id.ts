// Shape of the `id` that a route carries after `/clientes/` (SPEC-04, 2.1).

// 1 to 16 ASCII digits, the first one not `0`: neither `01` nor `0` alone.
const SHAPE = /^[1-9][0-9]{0,15}$/;
// 2^53 − 1, the largest integer JavaScript represents exactly (known limitation L-06).
const LARGEST_EXACT_INTEGER = '9007199254740991';

/**
 * A text that has passed `isRouteCustomerId`. The service that asks for a customer only takes
 * this type, so the compiler keeps an unchecked text from ever reaching a URL.
 */
export type RouteCustomerId = string & { readonly routeCustomerId: unique symbol };

/**
 * True when the text can be sent to the API as a customer id.
 *
 * The text is never turned into a number: JavaScript reads `01`, `+1` or `1.0` as 1, and one
 * customer would then have several addresses. Two digit strings of the same length compare as
 * numbers do, so the upper bound is checked on the text itself.
 */
export function isRouteCustomerId(text: string): text is RouteCustomerId {
  if (!SHAPE.test(text)) {
    return false;
  }
  return text.length < LARGEST_EXACT_INTEGER.length || text <= LARGEST_EXACT_INTEGER;
}
