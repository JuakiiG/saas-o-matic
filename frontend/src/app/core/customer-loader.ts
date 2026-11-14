import { Injectable, Signal, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute } from '@angular/router';
import { Observable, Subject, combineLatest, map, of, startWith, switchMap } from 'rxjs';

import { BackendApi } from './backend-api';
import { isRouteCustomerId } from './customer-id';
import { CustomerDetail } from './models';
import { Remote } from './remote';

/** The only code that means «there is no such customer»; `not_found` is a wrong URL (2.7). */
export const CUSTOMER_NOT_FOUND = 'customer_not_found';

/** The customer of a route: the three states of its request, or «not found». */
export type LoadedCustomer = { readonly status: 'not-found' } | Remote<CustomerDetail>;

const NOT_FOUND: LoadedCustomer = { status: 'not-found' };
const LOADING: LoadedCustomer = { status: 'loading' };

/**
 * Loads the customer whose id the route carries (SPEC-04, 2.1 and 2.4), for the detail and for
 * the simulator. Each of those views provides its own, so it sees the route of its view.
 *
 * The id is the text of the route and is never turned into a number: a text without the shape
 * of an id is «not found» without asking (E-47), and so is the `404` `customer_not_found` of
 * the backend (E-15). Any other error stays an error, with its code.
 */
@Injectable()
export class CustomerLoader {
  private readonly api = inject(BackendApi);
  private readonly route = inject(ActivatedRoute);
  private readonly retries = new Subject<void>();

  // `switchMap` drops the request in flight when the route changes or a retry is asked for.
  readonly state: Signal<LoadedCustomer> = toSignal(
    combineLatest([
      this.route.paramMap.pipe(map((params) => params.get('id') ?? '')),
      this.retries.pipe(startWith(undefined)),
    ]).pipe(switchMap(([id]) => this.load(id))),
    { initialValue: LOADING },
  );

  /** «Reintentar»: asks again for the customer of the route. */
  retry(): void {
    this.retries.next();
  }

  private load(id: string): Observable<LoadedCustomer> {
    if (!isRouteCustomerId(id)) {
      return of(NOT_FOUND);
    }
    return this.api.getCustomer(id).pipe(map((state) => (isMissing(state) ? NOT_FOUND : state)));
  }
}

function isMissing(state: Remote<CustomerDetail>): boolean {
  return state.status === 'error' && state.error.code === CUSTOMER_NOT_FOUND;
}
