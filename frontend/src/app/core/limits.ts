// The only limits of the backend that the frontend writes down, to warn before calling it.

/** Longest text the search accepts, in code points and untrimmed (SPEC-01, 2.12 and 4.3). */
export const SEARCH_MAX_LENGTH = 100;

/**
 * Most customers a search returns (SPEC-01/E-26). The API does not say how many there are, so
 * with this many on screen there may be more.
 */
export const SEARCH_MAX_RESULTS = 20;
