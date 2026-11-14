import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { RouteCustomerId } from './customer-id';
import {
  Customer,
  CustomerDetail,
  CustomerList,
  MetaData,
  NewCustomer,
  NewSimulation,
  Quote,
  QuoteRequest,
  Simulation,
} from './models';
import { BACKEND_TIMEOUT_MS, Remote, toRemote } from './remote';
import { replaceLoneSurrogates, trimSpaces } from './text';

/**
 * The calls to the backend (SPEC-04, 4.1). Components never see a URL.
 *
 * What the CORS configuration of the backend demands (SPEC-04, 2.9, and E-52): only `GET` and
 * `POST`, no header set by the application (so no interceptor either), JSON bodies, and no
 * response header is read. Every body is built here from the fields of its contract, so an
 * extra property of the argument never travels.
 */
@Injectable({ providedIn: 'root' })
export class BackendApi {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = environment.apiBaseUrl;

  /** Countries and plans with their names. It does not read the database (SPEC-04, 4.1). */
  getMeta(): Observable<Remote<MetaData>> {
    return this.get<MetaData>('/meta', new HttpParams());
  }

  /**
   * Customers matching a text, or the initial list when it is empty. The text goes as written,
   * untrimmed, in a single `q` parameter that the HTTP client encodes (SPEC-04/E-51).
   */
  searchCustomers(text: string): Observable<Remote<CustomerList>> {
    const params =
      text === '' ? new HttpParams() : new HttpParams().set('q', replaceLoneSurrogates(text));
    return this.get<CustomerList>('/customers', params);
  }

  /** Name and email travel trimmed, as the form has measured them; the tax id, as written (E-46). */
  createCustomer(customer: NewCustomer): Observable<Remote<Customer>> {
    return this.post<Customer>('/customers', {
      company_name: trimSpaces(customer.company_name),
      tax_id: customer.tax_id,
      contact_email: trimSpaces(customer.contact_email),
      country: customer.country,
      plan: customer.plan,
    });
  }

  /** The id is the text of the route, already checked and never turned into a number (E-47). */
  getCustomer(id: RouteCustomerId): Observable<Remote<CustomerDetail>> {
    return this.get<CustomerDetail>(`/customers/${id}`, new HttpParams());
  }

  quote(request: QuoteRequest): Observable<Remote<Quote>> {
    return this.post<Quote>('/pricing/quote', {
      customer_id: request.customer_id,
      active_users: request.active_users,
    });
  }

  saveSimulation(simulation: NewSimulation): Observable<Remote<Simulation>> {
    return this.post<Simulation>('/simulations', {
      customer_id: simulation.customer_id,
      active_users: simulation.active_users,
      storage_gb: simulation.storage_gb,
      estimated_api_calls: simulation.estimated_api_calls,
    });
  }

  private get<T>(path: string, params: HttpParams): Observable<Remote<T>> {
    return toRemote(this.http.get<T>(this.baseUrl + path, { params }), BACKEND_TIMEOUT_MS);
  }

  private post<T>(path: string, body: object): Observable<Remote<T>> {
    return toRemote(this.http.post<T>(this.baseUrl + path, body), BACKEND_TIMEOUT_MS);
  }
}
