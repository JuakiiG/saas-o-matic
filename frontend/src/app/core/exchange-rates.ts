import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { map } from 'rxjs';

import { environment } from '../../environments/environment';
import { ForeignCurrencyCode } from './display-currency';
import { Remote, toRemote } from './remote';

/** The public API has 5 s to answer (SPEC-04, 2.6). */
export const RATES_TIMEOUT_MS = 5_000;
/** Code of the error state when the API answers something that is not the three rates. */
export const INVALID_RATES = 'invalid_rates';

const BASE = 'EUR';
const DATE_SHAPE = /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/;

/** The rate from euros to another currency, and the day it is of: each rate brings its own. */
export interface Rate {
  readonly rate: number;
  readonly date: string;
}

export type Rates = Readonly<Record<ForeignCurrencyCode, Rate>>;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

/** The rate of one currency: exactly one object must bring it, and bring it well formed. */
function rateOf(list: readonly unknown[], currency: ForeignCurrencyCode): Rate | null {
  const found = list.filter((entry) => isRecord(entry) && entry['quote'] === currency);
  const [entry] = found;
  if (found.length !== 1 || !isRecord(entry) || entry['base'] !== BASE) {
    return null;
  }
  const { rate, date } = entry;
  if (typeof rate !== 'number' || !Number.isFinite(rate) || rate <= 0) {
    return null;
  }
  if (typeof date !== 'string' || !DATE_SHAPE.test(date)) {
    return null;
  }
  return { rate, date };
}

/**
 * The three rates of a response of the API, or `null` when it is not valid (SPEC-04, 2.6): a
 * list with exactly one well-formed object per currency asked for. A partial response is no
 * response: with one rate missing or wrong, none is used. Objects of other currencies are ignored.
 */
export function parseRates(body: unknown): Rates | null {
  if (!Array.isArray(body)) {
    return null;
  }
  const usd = rateOf(body, 'USD');
  const gbp = rateOf(body, 'GBP');
  const chf = rateOf(body, 'CHF');
  return usd === null || gbp === null || chf === null ? null : { USD: usd, GBP: gbp, CHF: chf };
}

function validated(state: Remote<unknown>): Remote<Rates> {
  if (state.status !== 'data') {
    return state;
  }
  const rates = parseRates(state.data);
  return rates === null
    ? { status: 'error', error: { code: INVALID_RATES, fieldErrors: [] } }
    : { status: 'data', data: rates };
}

/**
 * Exchange rates from euros to the other currencies (SPEC-04, 2.6). The public API is asked
 * once, when the application starts, straight from the browser and in a single request; the
 * rates stay in memory for the session, so changing the currency asks for nothing (E-26, E-27).
 * If it fails, the application goes on in euros (E-30).
 *
 * No header is set and no credential travels: the API allows any origin for a plain `GET`.
 */
@Injectable({ providedIn: 'root' })
export class ExchangeRates {
  private readonly http = inject(HttpClient);
  private readonly current = signal<Remote<Rates>>({ status: 'loading' });
  private requested = false;

  readonly state = this.current.asReadonly();

  /** Asks for the rates the first time it is called; later calls do nothing. */
  load(): void {
    if (!this.requested) {
      this.request();
    }
  }

  /** «Reintentar»: asks again, but only after a failure. */
  retry(): void {
    if (this.current().status === 'error') {
      this.request();
    }
  }

  private request(): void {
    this.requested = true;
    // The request ends by itself, in data or in an error, so there is nothing to unsubscribe.
    toRemote(this.http.get<unknown>(environment.ratesUrl), RATES_TIMEOUT_MS)
      .pipe(map(validated))
      .subscribe((state) => this.current.set(state));
  }
}
