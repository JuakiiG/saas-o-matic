import { Injectable, signal } from '@angular/core';

export type ForeignCurrencyCode = 'USD' | 'GBP' | 'CHF';

/** What the amounts are shown in: euros, or another currency with the rate that converts them. */
export type DisplayedCurrency =
  | { readonly code: 'EUR' }
  | { readonly code: ForeignCurrencyCode; readonly rate: number; readonly date: string };

/**
 * The currency chosen for the whole application (SPEC-04, 2.1 and 2.6). It lives in memory only:
 * reloading the page goes back to EUR, and it is never sent to the backend (E-31).
 */
@Injectable({ providedIn: 'root' })
export class DisplayCurrency {
  private readonly chosen = signal<DisplayedCurrency>({ code: 'EUR' });

  readonly current = this.chosen.asReadonly();

  show(currency: DisplayedCurrency): void {
    this.chosen.set(currency);
  }
}
