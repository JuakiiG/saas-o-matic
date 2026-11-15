import { APIRequestContext, APIResponse, expect } from '@playwright/test';

// The backend, called directly: to prepare the data a test needs without going through the
// interface, and to ask it what it does with a value that the interface would not send.

/** Where the backend of the tests listens: the default of `uvicorn`. */
export const BACKEND_URL = 'http://127.0.0.1:8000';

const CREATED = 201;
const UNPROCESSABLE = 422;

/** One entry of `errors` in a `422` (index of specs, «Errores de validación»). */
interface FieldError {
  readonly field: string;
  readonly code: string;
}

/** The response is a `422` whose errors include that code for that field. */
export async function expectFieldRejected(
  response: APIResponse,
  field: string,
  code: string,
): Promise<void> {
  expect(response.status(), await response.text()).toBe(UNPROCESSABLE);
  const problem: { errors: FieldError[] } = await response.json();
  const found = problem.errors.map((error) => ({ field: error.field, code: error.code }));
  expect(found).toContainEqual({ field, code });
}

/** Body of `POST /customers` (SPEC-01, 4.1). */
export interface CustomerBody {
  readonly company_name: string;
  readonly tax_id: string;
  readonly contact_email: string;
  readonly country: string;
  readonly plan: string;
}

/** Body of `POST /simulations` (SPEC-03, 4.1). */
export interface SimulationBody {
  readonly customer_id: number;
  readonly active_users: number;
  readonly storage_gb: number;
  readonly estimated_api_calls: number;
}

/**
 * A valid Spanish customer with the given tax id. The database is one for the whole run, so
 * each test brings a tax id of its own: a repeated one would be a `409`.
 */
export function customerBody(taxId: string, changes: Partial<CustomerBody> = {}): CustomerBody {
  return {
    company_name: `Ejemplo ${taxId} SL`,
    tax_id: taxId,
    contact_email: 'compras@ejemplo.example',
    country: 'ES',
    plan: 'professional',
    ...changes,
  };
}

/** Creates a customer through the API and gives its id; anything but a `201` fails the test. */
export async function createCustomer(
  request: APIRequestContext,
  body: CustomerBody,
): Promise<number> {
  const response = await request.post(`${BACKEND_URL}/customers`, { data: body });
  expect(response.status(), await response.text()).toBe(CREATED);
  const created: { id: number } = await response.json();
  return created.id;
}

/** Saves a simulation through the API; anything but a `201` fails the test. */
export async function saveSimulation(
  request: APIRequestContext,
  body: SimulationBody,
): Promise<void> {
  const response = await request.post(`${BACKEND_URL}/simulations`, { data: body });
  expect(response.status(), await response.text()).toBe(CREATED);
}
