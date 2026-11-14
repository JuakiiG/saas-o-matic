// Shapes of the backend contract, written by hand from the specs (ADR-001), not generated from
// the OpenAPI. Field names are the ones of the API. Amounts are integers in euro cents.

/** A country of `GET /meta` (SPEC-01, 4.4). Its tax rate arrives and is not used (ADR-002). */
export interface Country {
  readonly code: string;
  readonly name: string;
  readonly tax_rate_bp: number;
}

export interface Plan {
  readonly code: string;
  readonly name: string;
}

/** Response of `GET /meta`: the countries and plans, in the order in which they are offered. */
export interface MetaData {
  readonly countries: readonly Country[];
  readonly plans: readonly Plan[];
}

/** One result of `GET /customers` (SPEC-01, 4.3). */
export interface CustomerSummary {
  readonly id: number;
  readonly company_name: string;
  readonly tax_id: string;
  readonly country: string;
  readonly plan: string;
}

export interface CustomerList {
  readonly items: readonly CustomerSummary[];
}

/** Body of `POST /customers` (SPEC-01, 4.1): these five fields and nothing else. */
export interface NewCustomer {
  readonly company_name: string;
  readonly tax_id: string;
  readonly contact_email: string;
  readonly country: string;
  readonly plan: string;
}

/** Response of `POST /customers`: what was stored, with the tax id normalized by the backend. */
export interface Customer extends NewCustomer {
  readonly id: number;
  readonly created_at: string;
}

/** One pricing tier of a quote (SPEC-02, 4). The last one has no upper limit. */
export interface Tier {
  readonly from_users: number;
  readonly to_users: number | null;
  readonly unit_price_cents: number;
  readonly users: number;
  readonly subtotal_cents: number;
}

/** Body of `POST /pricing/quote`: JSON integers only. */
export interface QuoteRequest {
  readonly customer_id: number;
  readonly active_users: number;
}

/** Response of `POST /pricing/quote` (SPEC-02, 4). */
export interface Quote {
  readonly currency: string;
  readonly active_users: number;
  readonly tiers: readonly Tier[];
  readonly base_cents: number;
  readonly country: string;
  readonly tax_rate_bp: number;
  readonly tax_cents: number;
  readonly total_cents: number;
}

/** Body of `POST /simulations` (SPEC-03, 4.1): JSON integers only. */
export interface NewSimulation extends QuoteRequest {
  readonly storage_gb: number;
  readonly estimated_api_calls: number;
}

/** A stored simulation: the quote it was saved with, plus what was asked (SPEC-03, 4.1). */
export interface Simulation extends Quote {
  readonly id: number;
  readonly customer_id: number;
  readonly storage_gb: number;
  readonly estimated_api_calls: number;
  readonly created_at: string;
}

/** Response of `GET /customers/{id}` (SPEC-03, 4.2): the customer and its latest simulations. */
export interface CustomerDetail extends Customer {
  readonly simulation_count: number;
  readonly simulations: readonly Simulation[];
}
