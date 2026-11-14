import { Pipe, PipeTransform, inject } from '@angular/core';

import { DisplayCurrency } from '../core/display-currency';
import { formatConverted, formatEuroCents } from '../core/format';

/**
 * The only place where an amount becomes text (`.claude/rules/frontend.md`). It takes euro cents
 * and shows them in the currency chosen for the application.
 *
 * It is not pure on purpose: its result changes when the chosen currency does, not only when
 * the amount does, and reading the signal here is what makes the template notice.
 */
@Pipe({ name: 'money', pure: false })
export class MoneyPipe implements PipeTransform {
  private readonly displayCurrency = inject(DisplayCurrency);

  /** With `only` set to `'EUR'` the amount is shown in exact euros whatever the currency chosen. */
  transform(cents: number, only?: 'EUR'): string {
    const currency = this.displayCurrency.current();
    if (only === 'EUR' || currency.code === 'EUR') {
      return formatEuroCents(cents);
    }
    return formatConverted(cents, currency.code, currency.rate);
  }
}
