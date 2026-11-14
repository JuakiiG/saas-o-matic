// SPEC-04, 2.9: the URLs the application calls live here, not spread over the code.
export const environment = {
  // Where `uv run uvicorn --factory app.main:create_app` listens by default.
  apiBaseUrl: 'http://127.0.0.1:8000',
  // The public API of exchange rates, in its current version, with the three currencies in a
  // single request (SPEC-04, 2.6).
  ratesUrl: 'https://api.frankfurter.dev/v2/rates?base=EUR&quotes=USD,GBP,CHF',
};
