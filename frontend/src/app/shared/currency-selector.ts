import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

import { DisplayCurrency, ForeignCurrencyCode } from '../core/display-currency';
import { ExchangeRates } from '../core/exchange-rates';

const EURO = 'EUR';
const FOREIGN: readonly ForeignCurrencyCode[] = ['USD', 'GBP', 'CHF'];
const ONLY_EURO: readonly string[] = [EURO];
const EVERY_CURRENCY: readonly string[] = [EURO, ...FOREIGN];

function isForeign(code: string): code is ForeignCurrencyCode {
  return FOREIGN.some((currency) => currency === code);
}

/**
 * Currency selector of the header (SPEC-04, 2.1 and 2.6). It offers the four currencies only
 * with the rates in hand: while they load, or if the public API fails, it offers euros alone,
 * and on a failure it says so and offers «Reintentar». The rest of the application works the
 * same (E-30). Choosing a currency asks for nothing: the rates are in memory (E-27).
 */
@Component({
  selector: 'app-currency-selector',
  imports: [ReactiveFormsModule],
  template: `
    <div class="currency">
      <label for="currency-select">Divisa</label>
      <select id="currency-select" [formControl]="choice">
        @for (code of offered(); track code) {
          <option [value]="code">{{ code }}</option>
        }
      </select>
      @if (loading()) {
        <p class="currency-status" role="status">Cargando tipos…</p>
      }
    </div>
    @if (failed()) {
      <div class="currency-error" role="alert">
        <p>No se han podido cargar los tipos de cambio. Los importes se muestran en EUR.</p>
        <button type="button" (click)="retry()">Reintentar</button>
      </div>
    }
  `,
  styleUrl: './currency-selector.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CurrencySelector {
  private readonly rates = inject(ExchangeRates);
  private readonly display = inject(DisplayCurrency);

  protected readonly choice = new FormControl<string>(this.display.current().code, {
    nonNullable: true,
  });
  protected readonly loading = computed(() => this.rates.state().status === 'loading');
  protected readonly failed = computed(() => this.rates.state().status === 'error');
  protected readonly offered = computed(() =>
    this.rates.state().status === 'data' ? EVERY_CURRENCY : ONLY_EURO,
  );

  constructor() {
    this.choice.valueChanges.pipe(takeUntilDestroyed()).subscribe((code) => this.show(code));
  }

  protected retry(): void {
    this.rates.retry();
  }

  /** The amounts go to the chosen currency with the rate in memory; without it, to euros. */
  private show(code: string): void {
    const state = this.rates.state();
    if (isForeign(code) && state.status === 'data') {
      this.display.show({ code, ...state.data[code] });
    } else {
      this.display.show({ code: EURO });
    }
  }
}
