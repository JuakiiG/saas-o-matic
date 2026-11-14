import { ChangeDetectionStrategy, Component, computed, inject, input, output } from '@angular/core';

import { FormNoticeView } from '../../core/api-error';
import { DisplayCurrency } from '../../core/display-currency';
import { formatPercent } from '../../core/format';
import { Quote } from '../../core/models';
import { FormNotice } from '../../shared/form-notice';
import { LoadingNotice } from '../../shared/loading-notice';
import { MoneyPipe } from '../../shared/money-pipe';
import { RateNote } from '../../shared/rate-note';
import { TierList } from '../../shared/tier-list';

/**
 * The projection of the simulator, in its three states (SPEC-04, 2.5): the tiers, the base, the
 * tax with its rate and the total, exactly as the backend returned them (E-19); the loading of
 * the first one; or the notice of the one that failed. While a newer one is on its way the
 * amounts stay, marked as not current (E-21).
 */
@Component({
  selector: 'app-quote-panel',
  imports: [FormNotice, LoadingNotice, MoneyPipe, RateNote, TierList],
  templateUrl: './quote-panel.html',
  styleUrl: './quote-panel.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class QuotePanel {
  readonly quote = input.required<Quote | null>();
  readonly updating = input(false);
  readonly projecting = input(false);
  readonly notice = input<FormNoticeView | null>(null);
  readonly retry = output<void>();

  private readonly display = inject(DisplayCurrency);
  /** In another currency the total is also shown in euros, the exact one (E-29). */
  protected readonly converted = computed(() => this.display.current().code !== 'EUR');

  protected readonly taxLabel = computed(() => {
    const quote = this.quote();
    return quote === null ? '' : `Impuesto (${formatPercent(quote.tax_rate_bp)})`;
  });
}
