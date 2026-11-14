import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { CustomerLoader } from '../../core/customer-loader';
import { formatDateTime, formatInteger, formatPercent } from '../../core/format';
import { MetaStore } from '../../core/meta-store';
import { CustomerDetail, Simulation, Tier } from '../../core/models';
import { CustomerNotFound } from '../../shared/customer-not-found';
import { ErrorNotice } from '../../shared/error-notice';
import { LoadingNotice } from '../../shared/loading-notice';
import { MetaGate } from '../../shared/meta-gate';
import { MoneyPipe } from '../../shared/money-pipe';
import { TierList } from '../../shared/tier-list';

/** The customer as its card shows it: with the names of its country and plan. */
interface CustomerCard {
  readonly name: string;
  readonly taxId: string;
  readonly email: string;
  readonly country: string;
  readonly plan: string;
  readonly createdAt: string;
  readonly createdAtText: string;
  readonly simulatorLink: string;
}

/** One stored simulation as its card shows it. The amounts stay in cents for the money pipe. */
interface SimulationCard {
  readonly id: number;
  readonly createdAt: string;
  readonly createdAtText: string;
  readonly users: string;
  readonly storage: string;
  readonly apiCalls: string;
  readonly baseCents: number;
  readonly taxLabel: string;
  readonly taxCents: number;
  readonly totalCents: number;
  readonly tiers: readonly Tier[];
}

function toSimulationCard(simulation: Simulation): SimulationCard {
  return {
    id: simulation.id,
    createdAt: simulation.created_at,
    createdAtText: formatDateTime(simulation.created_at),
    users: formatInteger(simulation.active_users),
    storage: `${formatInteger(simulation.storage_gb)} GB`,
    apiCalls: formatInteger(simulation.estimated_api_calls),
    baseCents: simulation.base_cents,
    taxLabel: `Impuesto (${formatPercent(simulation.tax_rate_bp)})`,
    taxCents: simulation.tax_cents,
    totalCents: simulation.total_cents,
    tiers: simulation.tiers,
  };
}

/** The backend sends at most its latest simulations; the count is of all of them (E-14). */
function shownOfTotalNote(detail: CustomerDetail | null): string | null {
  if (detail === null || detail.simulation_count <= detail.simulations.length) {
    return null;
  }
  const shown = formatInteger(detail.simulations.length);
  return `Se muestran las ${shown} últimas de ${formatInteger(detail.simulation_count)}`;
}

/**
 * Detail of a customer: its data and its history of simulations (SPEC-04, 2.4). Everything it
 * shows is what the backend returned, in the order in which it returned it.
 */
@Component({
  selector: 'app-detalle',
  imports: [
    RouterLink,
    CustomerNotFound,
    ErrorNotice,
    LoadingNotice,
    MetaGate,
    MoneyPipe,
    TierList,
  ],
  providers: [CustomerLoader],
  templateUrl: './detalle.html',
  styleUrl: './detalle.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Detalle {
  private readonly loader = inject(CustomerLoader);
  private readonly meta = inject(MetaStore);

  private readonly detail = computed(() => {
    const state = this.loader.state();
    return state.status === 'data' ? state.data : null;
  });

  protected readonly notFound = computed(() => this.loader.state().status === 'not-found');
  protected readonly loading = computed(() => this.loader.state().status === 'loading');
  protected readonly error = computed(() => {
    const state = this.loader.state();
    return state.status === 'error' ? state.error : null;
  });
  protected readonly customer = computed(() => this.toCustomerCard(this.detail()));
  protected readonly simulations = computed(() =>
    (this.detail()?.simulations ?? []).map(toSimulationCard),
  );
  protected readonly hasSimulations = computed(() => this.simulations().length > 0);
  protected readonly shownOfTotal = computed(() => shownOfTotalNote(this.detail()));

  /** «Reintentar»: asks again for the customer of the route. */
  protected retry(): void {
    this.loader.retry();
  }

  private toCustomerCard(detail: CustomerDetail | null): CustomerCard | null {
    if (detail === null) {
      return null;
    }
    return {
      name: detail.company_name,
      taxId: detail.tax_id,
      email: detail.contact_email,
      country: this.meta.countryName(detail.country),
      plan: this.meta.planName(detail.plan),
      createdAt: detail.created_at,
      createdAtText: formatDateTime(detail.created_at),
      simulatorLink: `/clientes/${detail.id}/simulacion`,
    };
  }
}
