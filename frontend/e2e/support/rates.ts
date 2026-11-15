// The public API of exchange rates, as the tests see it: no test calls an external service.

/** Host of the API of exchange rates (SPEC-04, 2.6). */
export const RATES_HOST = 'api.frankfurter.dev';

/** The date every fixed rate brings; the one the interface must show, in any time zone. */
export const RATES_DATE = '2026-11-12';

/** The real answer written down in SPEC-04, 4.2: the rates of the test cases of the spec. */
export const FIXED_RATES = [
  { date: RATES_DATE, base: 'EUR', quote: 'CHF', rate: 0.92316 },
  { date: RATES_DATE, base: 'EUR', quote: 'GBP', rate: 0.83583 },
  { date: RATES_DATE, base: 'EUR', quote: 'USD', rate: 1.1139 },
] as const;
