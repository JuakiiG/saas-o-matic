import { test as base, expect, Page } from '@playwright/test';

import { FIXED_RATES, RATES_HOST } from './rates';

// What every test shares: the browser only reaches the two local servers, and the API of
// exchange rates is answered inside the browser with fixed rates.
//
// The rates are NOT intercepted with `page.route()`. With any route in place Playwright answers
// every CORS preflight by itself, admitting whatever the page asks for, so the preflight never
// reaches the backend and CA-14 would prove nothing about its CORS (seen with a mutation: a
// header of the application on every `POST` went through). Instead, the debugging protocol of
// Chromium pauses the requests to the URL of the rates and only those: everything that goes to
// the backend, preflights included, travels untouched.

const LOCAL_HOSTS: readonly string[] = ['localhost', '127.0.0.1'];
const WEB_PROTOCOLS: readonly string[] = ['http:', 'https:'];
const RATES_PATTERN = `https://${RATES_HOST}/*`;
const RATES_HEADERS = [
  { name: 'content-type', value: 'application/json; charset=utf-8' },
  // The real API allows any origin (SPEC-04, 4.2); without it the browser hides the answer.
  { name: 'access-control-allow-origin', value: '*' },
];
// The protocol takes the body in base64.
const RATES_BODY = Buffer.from(JSON.stringify(FIXED_RATES), 'utf-8').toString('base64');

interface Options {
  /** With `true` the API of exchange rates fails, as when it is down. */
  ratesDown: boolean;
}

/** What went wrong around a test without being one of its assertions. */
interface Incidents {
  /** Requests to a host that is neither local nor the API of exchange rates. */
  readonly outside: string[];
  /** Failures when answering a request to the API of exchange rates. */
  readonly unanswered: string[];
}

function watchOutsideRequests(page: Page, incidents: Incidents): void {
  page.on('request', (request) => {
    const url = new URL(request.url());
    const leaves = WEB_PROTOCOLS.includes(url.protocol) && !LOCAL_HOSTS.includes(url.hostname);
    if (leaves && url.hostname !== RATES_HOST) {
      incidents.outside.push(url.href);
    }
  });
}

/** Answers every request of the page to the API of exchange rates: fixed rates, or a failure. */
async function answerRates(page: Page, down: boolean, incidents: Incidents): Promise<void> {
  const session = await page.context().newCDPSession(page);
  session.on('Fetch.requestPaused', ({ requestId }) => {
    const answer = down
      ? session.send('Fetch.failRequest', { requestId, errorReason: 'ConnectionRefused' })
      : session.send('Fetch.fulfillRequest', {
          requestId,
          responseCode: 200,
          responseHeaders: RATES_HEADERS,
          body: RATES_BODY,
        });
    // Not swallowed: the test fails with it when it ends.
    answer.catch((error: unknown) => incidents.unanswered.push(String(error)));
  });
  await session.send('Fetch.enable', { patterns: [{ urlPattern: RATES_PATTERN }] });
}

export const test = base.extend<Options>({
  ratesDown: [false, { option: true }],
  page: async ({ page, ratesDown }, use) => {
    const incidents: Incidents = { outside: [], unanswered: [] };
    watchOutsideRequests(page, incidents);
    await answerRates(page, ratesDown, incidents);
    await use(page);
    expect(incidents, 'no request leaves the machine and every rate is answered').toEqual({
      outside: [],
      unanswered: [],
    });
  },
});

export { expect };
