// The limits of the search of the backend, written down to warn before calling it. Those of the
// two forms are next to their help (`alta-help.ts` and `simulador-help.ts`); nothing checks
// that any of them matches the backend but the end-to-end tests of the limits (L-09).

/** Longest text the search accepts, in code points and untrimmed (SPEC-01, 2.12 and 4.3). */
export const SEARCH_MAX_LENGTH = 100;

/**
 * Most customers a search returns (SPEC-01/E-26). The API does not say how many there are, so
 * with this many on screen there may be more.
 */
export const SEARCH_MAX_RESULTS = 20;
