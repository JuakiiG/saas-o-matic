import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';

import { DisplayCurrency } from '../core/display-currency';
import { formatRate, formatRateDate } from '../core/format';

/**
 * What goes with converted amounts (SPEC-04, 2.6): the rate applied, with the date that rate
 * brings, and the warning that they are only a guide, because each one is converted on its own
 * and the base plus the tax can differ from the total by a cent. Nothing is shown in euros.
 */
@Component({
  selector: 'app-rate-note',
  template: `
    @if (applied(); as rate) {
      <p class="rate-note">
        <span class="rate-applied">{{ rate }}</span>
        <span class="rate-warning">Importes orientativos: cada uno se convierte por separado.</span>
      </p>
    }
  `,
  styleUrl: './rate-note.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RateNote {
  private readonly display = inject(DisplayCurrency);

  protected readonly applied = computed(() => {
    const currency = this.display.current();
    if (currency.code === 'EUR') {
      return null;
    }
    const rate = formatRate(currency.rate);
    return `1 EUR = ${rate} ${currency.code} · tipo del ${formatRateDate(currency.date)}`;
  });
}
