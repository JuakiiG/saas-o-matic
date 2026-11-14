import { Injectable, Signal, inject, signal } from '@angular/core';
import { takeUntilDestroyed, toObservable } from '@angular/core/rxjs-interop';
import { FormControl } from '@angular/forms';
import { Observable, Subject, map, merge, of, startWith, switchMap, timer } from 'rxjs';

import { BackendApi } from '../../core/backend-api';
import { Quote } from '../../core/models';
import { Remote } from '../../core/remote';
import { MAX_ACTIVE_USERS, parseCount } from './simulador-help';

/** A projection is asked for this long after the last change of the users (SPEC-04/E-18). */
const DEBOUNCE_MS = 200;

/** A projection that has been asked for: for how many users, and the state of its request. */
export interface Projection {
  readonly users: number;
  readonly state: Remote<Quote>;
}

/**
 * The live projection of the simulator (SPEC-04, 2.5): it asks `POST /pricing/quote` for the
 * users written, 200 ms after their last change, and keeps what is to be shown. Every amount is
 * the one the backend returned: nothing is calculated here (E-19).
 */
@Injectable()
export class Projector {
  private readonly api = inject(BackendApi);
  private readonly retries = new Subject<void>();
  private readonly asked = signal<Projection | null>(null);
  private readonly amounts = signal<Quote | null>(null);

  /** The projection last asked for; `null` while there is no customer or no valid number. */
  readonly projection = this.asked.asReadonly();
  /** The amounts on screen: the last ones that arrived, until an error or an invalid text. */
  readonly quote = this.amounts.asReadonly();

  /**
   * Starts projecting for the customer, from the moment it arrives, each time the text of the
   * users changes. Called once, while the view that owns the text box is being created.
   */
  start(customerId: Signal<number | null>, users: FormControl<string>): void {
    // No projection before the customer arrives; the first one, as soon as it does (E-38).
    toObservable(customerId)
      .pipe(
        switchMap((id) => (id === null ? of(null) : this.projectionsFor(id, users))),
        takeUntilDestroyed(),
      )
      .subscribe((projection) => this.follow(projection));
  }

  /** «Reintentar»: asks again for the users written, without waiting. */
  retry(): void {
    this.retries.next();
  }

  private projectionsFor(
    customerId: number,
    users: FormControl<string>,
  ): Observable<Projection | null> {
    const waits = merge(
      users.valueChanges.pipe(map(() => DEBOUNCE_MS)),
      this.retries.pipe(map(() => 0)),
    );
    // `switchMap` drops the projection in flight when a newer one is due, which cancels its
    // request: an old answer never paints over a newer one (E-18).
    return waits.pipe(
      startWith(0),
      switchMap((waitMs) => this.project(customerId, users.value, waitMs)),
    );
  }

  private project(customerId: number, text: string, waitMs: number): Observable<Projection | null> {
    const users = parseCount(text, MAX_ACTIVE_USERS);
    // Not a valid number: no request, and none left in flight either (E-22).
    if (users === null) {
      return of(null);
    }
    // The id is the one of the customer that was loaded, not the text of the route (E-49).
    const states = this.api
      .quote({ customer_id: customerId, active_users: users })
      .pipe(map((state): Projection => ({ users, state })));
    if (waitMs === 0) {
      return states;
    }
    const waiting: Projection = { users, state: { status: 'loading' } };
    return timer(waitMs).pipe(
      switchMap(() => states),
      startWith(waiting),
    );
  }

  private follow(projection: Projection | null): void {
    this.asked.set(projection);
    // An amount never stays on screen as if it were current after an error (E-20, E-22).
    if (projection === null || projection.state.status === 'error') {
      this.amounts.set(null);
    } else if (projection.state.status === 'data') {
      this.amounts.set(projection.state.data);
    }
  }
}
