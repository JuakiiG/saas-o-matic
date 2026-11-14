// Replaces `environment.ts` in development builds (`ng serve`). Both point at the local backend:
// the project only runs locally.
export const environment = {
  apiBaseUrl: 'http://127.0.0.1:8000',
  ratesUrl: 'https://api.frankfurter.dev/v2/rates?base=EUR&quotes=USD,GBP,CHF',
};
