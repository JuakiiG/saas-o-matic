import { Injectable, inject, signal } from '@angular/core';

import { BackendApi } from './backend-api';
import { MetaData } from './models';
import { Remote } from './remote';

/**
 * Names of the countries and plans (SPEC-04, 2.1). `GET /meta` is asked once, when the
 * application starts, and its answer is kept in memory for the session (E-39). The four views
 * that show a country or a plan read it from here, and show its loading or error state instead
 * of their content while there is no data (E-40).
 */
@Injectable({ providedIn: 'root' })
export class MetaStore {
  private readonly api = inject(BackendApi);
  private readonly current = signal<Remote<MetaData>>({ status: 'loading' });
  private requested = false;

  readonly state = this.current.asReadonly();

  /** Asks for `/meta` the first time it is called; later calls do nothing. */
  load(): void {
    if (!this.requested) {
      this.request();
    }
  }

  /** «Reintentar»: asks again, but only after a failure. */
  retry(): void {
    if (this.current().status === 'error') {
      this.request();
    }
  }

  /** Name of a country, or its code as it arrives when `/meta` does not bring it (E-35). */
  countryName(code: string): string {
    return this.data()?.countries.find((country) => country.code === code)?.name ?? code;
  }

  /** Name of a plan, or its code as it arrives when `/meta` does not bring it (E-35). */
  planName(code: string): string {
    return this.data()?.plans.find((plan) => plan.code === code)?.name ?? code;
  }

  private data(): MetaData | null {
    const state = this.current();
    return state.status === 'data' ? state.data : null;
  }

  private request(): void {
    this.requested = true;
    // The request ends by itself, in data or in an error, so there is nothing to unsubscribe.
    this.api.getMeta().subscribe((state) => this.current.set(state));
  }
}
