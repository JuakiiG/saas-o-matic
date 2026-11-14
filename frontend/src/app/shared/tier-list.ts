import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

import { formatInteger, tierLabel } from '../core/format';
import { Tier } from '../core/models';
import { MoneyPipe } from './money-pipe';

/** One tier as it is shown: its limits, how many users fall in it, and what they cost. */
interface TierRow {
  readonly label: string;
  readonly users: string;
  readonly unitPriceCents: number;
  readonly subtotalCents: number;
}

/**
 * The tiers of a quote or of a stored simulation (SPEC-04, 2.4 and 2.5), as the backend sent
 * them: nothing is calculated here (E-19). A list and not a table, so that it wraps at 375 px.
 */
@Component({
  selector: 'app-tier-list',
  imports: [MoneyPipe],
  template: `
    <ul class="tiers">
      @for (row of rows(); track row.label) {
        <li class="tier">
          <span class="tier-label">{{ row.label }}</span>
          <span class="tier-detail">{{ row.users }} × {{ row.unitPriceCents | money }}</span>
          <span class="tier-subtotal">{{ row.subtotalCents | money }}</span>
        </li>
      }
    </ul>
  `,
  styleUrl: './tier-list.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TierList {
  readonly tiers = input.required<readonly Tier[]>();

  protected readonly rows = computed(() =>
    this.tiers().map((tier): TierRow => ({
      label: tierLabel(tier.from_users, tier.to_users),
      users: formatInteger(tier.users),
      unitPriceCents: tier.unit_price_cents,
      subtotalCents: tier.subtotal_cents,
    })),
  );
}
