import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Observable, Subject, map, of, switchMap, timer } from 'rxjs';

import { ApiError } from '../../core/api-error';
import { BackendApi } from '../../core/backend-api';
import { SEARCH_MAX_LENGTH, SEARCH_MAX_RESULTS } from '../../core/limits';
import { MetaStore } from '../../core/meta-store';
import { CustomerList } from '../../core/models';
import { Remote } from '../../core/remote';
import { codePointLength } from '../../core/text';
import { ErrorNotice } from '../../shared/error-notice';
import { LoadingNotice } from '../../shared/loading-notice';

/** A search is sent this long after the last change of the text (SPEC-04/E-02). */
const DEBOUNCE_MS = 300;

/** A search that has been sent: the text it carried and the state of its request. */
interface Search {
  readonly text: string;
  readonly state: Remote<CustomerList>;
}

interface SearchRequest {
  readonly text: string;
  readonly waitMs: number;
}

/** One customer as the list shows it: with the names of its country and plan. */
interface Row {
  readonly id: number;
  readonly name: string;
  readonly taxId: string;
  readonly country: string;
  readonly plan: string;
  readonly link: string;
}

type ListView = 'none' | 'loading' | 'error' | 'empty-initial' | 'empty-search' | 'list';

function isTooLong(text: string): boolean {
  return codePointLength(text) > SEARCH_MAX_LENGTH;
}

function errorOf(state: Remote<unknown> | undefined): ApiError | null {
  return state?.status === 'error' ? state.error : null;
}

function listViewOf(search: Search | null): ListView {
  if (search === null) {
    return 'none';
  }
  if (search.state.status !== 'data') {
    return search.state.status;
  }
  if (search.state.data.items.length > 0) {
    return 'list';
  }
  // Only a request without `q` is the initial list (SPEC-04/E-54).
  return search.text === '' ? 'empty-initial' : 'empty-search';
}

/** Panel: the customer search and the way into the sign-up (SPEC-04, 2.2). */
@Component({
  selector: 'app-panel',
  imports: [ReactiveFormsModule, RouterLink, ErrorNotice, LoadingNotice],
  templateUrl: './panel.html',
  styleUrl: './panel.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Panel {
  private readonly api = inject(BackendApi);
  private readonly meta = inject(MetaStore);

  protected readonly searchBox = new FormControl('', { nonNullable: true });
  private readonly text = toSignal(this.searchBox.valueChanges, { initialValue: '' });
  private readonly requests = new Subject<SearchRequest>();
  private readonly search = signal<Search | null>(null);

  protected readonly metaError = computed(() => errorOf(this.meta.state()));
  protected readonly metaLoading = computed(() => this.meta.state().status === 'loading');
  protected readonly tooLong = computed(() => isTooLong(this.text()));
  protected readonly searchErrorId = computed(() => (this.tooLong() ? 'panel-search-error' : null));
  protected readonly listView = computed(() => listViewOf(this.search()));
  protected readonly listError = computed(() => errorOf(this.search()?.state));
  protected readonly rows = computed(() => this.toRows(this.search()));
  protected readonly atMaximum = computed(() => this.rows().length === SEARCH_MAX_RESULTS);

  constructor() {
    // `switchMap` drops the search in flight when a newer one arrives, which cancels its
    // request: an old answer never paints over a newer one (E-02).
    this.requests
      .pipe(
        switchMap((request) => this.run(request)),
        takeUntilDestroyed(),
      )
      .subscribe((search) => this.search.set(search));
    this.searchBox.valueChanges
      .pipe(takeUntilDestroyed())
      .subscribe((text) => this.requests.next({ text, waitMs: DEBOUNCE_MS }));
    this.requests.next({ text: '', waitMs: 0 });
  }

  protected retryMeta(): void {
    this.meta.retry();
  }

  /** Repeats the search that failed, with the same text and without waiting. */
  protected retrySearch(): void {
    this.requests.next({ text: this.search()?.text ?? '', waitMs: 0 });
  }

  private run(request: SearchRequest): Observable<Search | null> {
    // Over the limit there is no request: the list goes away at once, and so does the search
    // in flight, so that its answer cannot bring the list back (E-50).
    if (isTooLong(request.text)) {
      return of(null);
    }
    const states = this.api
      .searchCustomers(request.text)
      .pipe(map((state): Search => ({ text: request.text, state })));
    return request.waitMs === 0 ? states : timer(request.waitMs).pipe(switchMap(() => states));
  }

  /** The items in the order of the API: the frontend neither filters nor sorts (E-03). */
  private toRows(search: Search | null): Row[] {
    if (search?.state.status !== 'data') {
      return [];
    }
    return search.state.data.items.map((customer) => ({
      id: customer.id,
      name: customer.company_name,
      taxId: customer.tax_id,
      country: this.meta.countryName(customer.country),
      plan: this.meta.planName(customer.plan),
      link: `/clientes/${customer.id}`,
    }));
  }
}
